import asyncio
import logging
import sys
import tempfile
import textwrap
from pathlib import Path
from typing import Optional, Sequence, Tuple

import click
import neuro_sdk
from neuro_cli.formatters.images import DockerImageProgress
from neuro_sdk import Client
from rich.console import Console

from .cli import main
from .const import EX_OK, EX_PLATFORMERROR
from .image_builder import (
    MIN_BUILD_PRESET_CPU,
    MIN_BUILD_PRESET_MEM,
    DockerConfigAuth,
    ImageBuilder,
    create_docker_config_auth,
)
from .utils import get_neuro_client, select_job_preset


logger = logging.getLogger(__name__)


@main.group()
def image() -> None:
    """
    Job container image operations.
    """
    pass


@image.command("transfer")
@click.argument("source")
@click.argument("destination")
@click.option(
    "-F",
    "--force-overwrite",
    default=False,
    is_flag=True,
    help="Transfer even if the destination image already exists.",
)
def image_transfer(source: str, destination: str, force_overwrite: bool) -> None:
    """
    Copy images between clusters.
    """
    exit_code = asyncio.run(_image_transfer(source, destination, force_overwrite))
    sys.exit(exit_code)


@image.command(
    "build", help="Build Job container image remotely on cluster using Kaniko."
)
@click.argument("path", metavar="CONTEXT_PATH")
@click.argument("image_uri")
@click.option(
    "-f",
    "--file",
    default="Dockerfile",
    show_default=True,
    help=(
        "Relative (w.r.t. context) path to the dockerfile. "
        "The dockerfile should be within the context directory."
    ),
)
@click.option(
    "--build-arg",
    multiple=True,
    metavar="VAR=VAL",
    help=(
        "Build-time variables passed in ARG values, similarly to Docker. "
        "Could be used multiple times for multiple arguments."
    ),
)
@click.option(
    "-v",
    "--volume",
    metavar="MOUNT",
    multiple=True,
    help=(
        "Mounts directory from vault into container. "
        "Use multiple options to mount more than one volume. "
        "Use --volume=ALL to mount all accessible storage directories."
    ),
)
@click.option(
    "-e",
    "--env",
    metavar="VAR=VAL",
    multiple=True,
    help=(
        "Set environment variable in container "
        "Use multiple options to define more than one variable"
    ),
)
@click.option(
    "-s",
    "--preset",
    metavar="PRESET",
    help=(
        "Predefined resource configuration (to see available values, "
        "run `neuro config show`)"
    ),
)
@click.option(
    "-F",
    "--force-overwrite",
    default=False,
    show_default=True,
    is_flag=True,
    help="Overwrite if the destination image already exists.",
)
@click.option(
    "--cache/--no-cache",
    default=True,
    show_default=True,
    help="Use Kaniko cache while building image.",
)
@click.option(
    "--verbose",
    type=bool,
    default=False,
    help="If specified, run Kaniko with 'debug' verbosity, otherwise 'info' (default).",
)
@click.option(
    "--build-tag",
    multiple=True,
    metavar="VAR=VAL",
    help=(
        "Set tag(s) for image builder job. "
        "We will add tag 'kaniko-builds:{image-name}' authomatically."
    ),
)
def image_build(
    path: str,
    image_uri: str,
    file: str,
    build_arg: Tuple[str],
    volume: Tuple[str],
    env: Tuple[str],
    preset: str,
    force_overwrite: bool,
    cache: bool,
    verbose: bool,
    build_tag: Tuple[str],
) -> None:
    try:
        sys.exit(
            asyncio.run(
                _build_image(
                    dockerfile_path=Path(file),
                    context=path,
                    image_uri_str=image_uri,
                    use_cache=cache,
                    build_args=build_arg,
                    volume=volume,
                    env=env,
                    preset=preset,
                    force_overwrite=force_overwrite,
                    verbose=verbose,
                    local=False,
                    build_tags=build_tag,
                )
            )
        )
    except (ValueError, click.ClickException) as e:
        logger.error(f"Failed to build image: {e}")
        sys.exit(EX_PLATFORMERROR)


@image.command(
    "local-build", help="Build Job container image locally (requires Docker daemon)."
)
@click.argument("path", metavar="CONTEXT_PATH")
@click.argument("image_uri")
@click.option(
    "-f",
    "--file",
    default="Dockerfile",
    show_default=True,
    help=(
        "Relative (w.r.t. context) path to the dockerfile. "
        "The dockerfile should be within the context directory."
    ),
)
@click.option(
    "--build-arg",
    multiple=True,
    metavar="VAR=VAL",
    help=(
        "Build-time variables passed in ARG values. "
        "Could be used multiple times for multiple arguments."
    ),
)
@click.option(
    "-F",
    "--force-overwrite",
    default=False,
    show_default=True,
    is_flag=True,
    help="Overwrite if the destination image already exists.",
)
@click.option(
    "--verbose",
    type=bool,
    default=False,
    help="If specified, provide verbose output (default False).",
)
def image_build_local(
    path: str,
    image_uri: str,
    file: str,
    build_arg: Tuple[str],
    force_overwrite: bool,
    verbose: bool,
) -> None:
    try:
        sys.exit(
            asyncio.run(
                _build_image(
                    dockerfile_path=Path(file),
                    context=path,
                    image_uri_str=image_uri,
                    use_cache=True,
                    build_args=build_arg,
                    volume=(),
                    env=(),
                    force_overwrite=force_overwrite,
                    verbose=verbose,
                    local=True,
                    build_tags=(),
                )
            )
        )
    except (ValueError, click.ClickException) as e:
        logger.error(f"Failed to build image: {e}")
        sys.exit(EX_PLATFORMERROR)


async def _parse_neuro_image(image: str) -> neuro_sdk.RemoteImage:
    async with get_neuro_client() as client:
        return client.parse.remote_image(image)


def _get_cluster_from_uri(
    client: neuro_sdk.Client, image_uri: str, *, scheme: str
) -> Optional[str]:
    try:
        uri = client.parse.str_to_uri(image_uri, allowed_schemes=[scheme])
        return uri.host
    except ValueError:
        # seems like the image scheme was not provided, since it's hosted in dockerhub
        logger.warning(f"Unable to parse the cluster name from URI '{image_uri}' ")
        return None


async def _image_transfer(
    src_uri_str: str, dst_uri_str: str, force_overwrite: bool
) -> int:
    async with get_neuro_client() as client:
        src_cluster: Optional[str] = _get_cluster_from_uri(
            client, src_uri_str, scheme="image"
        )
        dst_cluster: Optional[str] = _get_cluster_from_uri(
            client, dst_uri_str, scheme="image"
        )
        if not dst_cluster:
            raise ValueError(
                f"Invalid destination image {dst_uri_str}: missing cluster name"
            )

    with tempfile.TemporaryDirectory() as tmpdir:
        async with get_neuro_client(cluster=src_cluster) as src_client:
            src_image = src_client.parse.remote_image(image=src_uri_str)
            src_reg_auth = await create_docker_config_auth(src_client.config)

        dockerfile = Path(f"{tmpdir}/Dockerfile")
        dockerfile.write_text(
            textwrap.dedent(
                f"""\
                FROM {src_image.as_docker_url()}
                LABEL neu.ro/source-image-uri={src_uri_str}
                """
            )
        )
        migration_job_tags = (
            f"src-image:{src_image}",
            f"neuro-extras:image-transfer",
        )
        return await _build_image(
            dockerfile_path=Path(dockerfile.name),
            context=tmpdir,
            image_uri_str=dst_uri_str,
            use_cache=True,
            build_args=(),
            volume=(),
            env=(),
            build_tags=migration_job_tags,
            force_overwrite=force_overwrite,
            registry_auths=[src_reg_auth],
        )


async def _build_image(
    dockerfile_path: Path,
    context: str,
    image_uri_str: str,
    use_cache: bool,
    build_args: Tuple[str, ...],
    volume: Tuple[str, ...],
    env: Tuple[str, ...],
    build_tags: Tuple[str, ...],
    force_overwrite: bool,
    preset: Optional[str] = None,
    registry_auths: Sequence[DockerConfigAuth] = (),
    local: bool = False,
    verbose: bool = False,
) -> int:
    async with get_neuro_client() as client:
        cluster = _get_cluster_from_uri(client, image_uri_str, scheme="image")
    async with get_neuro_client(cluster=cluster) as client:
        context_uri = client.parse.str_to_uri(
            context,
            allowed_schemes=("file",) if local else ("file", "storage"),
        )
        image_exists = await _check_image_exists(image_uri_str, client)
        if image_exists:
            if force_overwrite:
                logger.warning(
                    f"Target image '{image_uri_str}' exists and will be overwritten."
                )
            else:
                raise click.ClickException(
                    f"Target image '{image_uri_str}' exists. "
                    f"Use -F/--force-overwrite flag to enforce overwriting."
                )

        preset = select_job_preset(
            preset=preset,
            client=client,
            min_cpu=MIN_BUILD_PRESET_CPU,
            min_mem=MIN_BUILD_PRESET_MEM,
        )

        builder_cls = ImageBuilder.get(local=local)
        builder = builder_cls(
            client, extra_registry_auths=registry_auths, verbose=verbose
        )
        exit_code = await builder.build(
            dockerfile_path=dockerfile_path,
            context_uri=context_uri,
            image_uri_str=image_uri_str,
            use_cache=use_cache,
            build_args=build_args,
            volumes=volume,
            envs=env,
            job_preset=preset,
            build_tags=build_tags,
        )
        if exit_code == EX_OK:
            logger.info(f"Successfully built {image_uri_str}")
            if local:
                logger.info(f"Pushing image to registry")
                remote_image = await _parse_neuro_image(image_uri_str)
                console = Console()
                progress = DockerImageProgress.create(
                    console=console, quiet=not verbose
                )
                local_image = client.parse.local_image(remote_image.as_docker_url())
                try:
                    await client.images.push(
                        local_image, remote_image, progress=progress
                    )
                    logger.info(
                        f"Image {image_uri_str} pushed to the platform registry "
                        f"as {remote_image}"
                    )
                except Exception as e:
                    if local:
                        logger.exception("Image push failed.")
                        logger.info(
                            f"You may try to repeat the push process by running "
                            f"'neuro image push {local_image} {image_uri_str}'"
                        )
                    raise e
            return EX_OK
        else:
            raise click.ClickException(f"Failed to build image: {exit_code}")


async def _check_image_exists(image_uri_str: str, client: Client) -> bool:
    image = await _parse_neuro_image(image_uri_str)
    if image.registry is None:
        # TODO (y.s.): we might need to implement this check later.
        logger.warning(
            f"Skipping check if image '{image}' exists. "
            "If it does exist - it will be overwritten!"
        )
        return False
    try:
        existing_images = await client.images.tags(
            neuro_sdk.RemoteImage(
                name=image.name,
                project_name=image.project_name,
                cluster_name=image.cluster_name,
                registry=image.registry,
                tag=None,
            )
        )
        return image in existing_images
    except neuro_sdk.ResourceNotFound:
        # image does not exists on platform registry
        return False

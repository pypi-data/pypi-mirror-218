"""MLflow Docker helpers."""
import io
import json
import logging
import warnings
from contextlib import redirect_stderr, redirect_stdout

import docker
import mlflow

logger = logging.getLogger(__package__)


def _mlflow_build_docker_image(model_uri: str, image: str) -> None:
    with warnings.catch_warnings(), redirect_stdout(io.StringIO()), redirect_stderr(
        io.StringIO()
    ) as output:
        warnings.simplefilter("once")
        mlflow.models.build_docker(
            model_uri=model_uri,
            name=image,
            enable_mlserver=True,
        )
        build_log = output.getvalue()
        if "ERROR" in build_log:
            raise mlflow.exceptions.MlflowException(build_log)


def _docker_safe_push_image(client, repository: str, tag: str | None = None) -> None:
    response = client.images.push(repository, tag=tag)
    data = json.loads(response.strip().split("\n").pop())
    if "error" in data and data["error"]:
        raise docker.errors.APIError(data["error"])


def get_model_as_image(
    client,
    model_uri: str,
    repository: str,
    tag: str | None = None,
    force_update: bool = False,
) -> str:
    """Build a Docker image from a MLFlow model, push it to a Docker repository."""
    image = f"{repository}:{tag}" if tag else repository

    try:
        client.images.get_registry_data(image)
        if not force_update:
            logger.info(
                "Image '%s' is already available from the registry, skipping build.",
                image,
            )
            return image
    except docker.errors.NotFound:
        # Just ignore the "cache miss" case!
        pass
    except docker.errors.APIError as error:
        raise mlflow.exceptions.MlflowException(
            f"failed to get registry data for '{image}'."
        ) from error

    logger.info("Building image '%s' from '%s'", image, model_uri)
    _mlflow_build_docker_image(model_uri, image)

    try:
        logger.info("Pushing image '%s'", image)
        _docker_safe_push_image(client, repository, tag)
    except docker.errors.APIError as error:
        raise mlflow.exceptions.MlflowException(
            f"failed to push image '{image}'."
        ) from error

    return image

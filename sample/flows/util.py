import os
from typing import Optional

from docker.models.containers import Container
from prefect import flow, get_run_logger
from prefect_docker import DockerHost
from prefect_docker.containers import create_docker_container, get_docker_container_logs, remove_docker_container, start_docker_container

__all__ = ["IMAGE_1", "IMAGE_2", "IMAGE_3", "docker_tasks"]

DOCKER_HOST = os.environ.get("DOCKER_HOST", "unix:///var/run/docker.sock")

IMAGE_1 = "prefect-sample/task1"
IMAGE_2 = "prefect-sample/task2"
IMAGE_3 = "prefect-sample/task3"

ExitCode = int


async def docker_tasks(image: str, command: Optional[str] = None) -> ExitCode:
    logger = get_run_logger()

    host = DockerHost(base_url=DOCKER_HOST)

    created = await create_docker_container.submit(image=image, command=command, docker_host=host)
    container: Container = await created.result()

    started = await start_docker_container.submit(container_id=container.id, docker_host=host, wait_for=[created])
    container = await started.result()

    logger.info(f"Waiting for the completion of container {container.name}")
    result = container.wait()
    exit_code = int(result["StatusCode"])

    logs_future = await get_docker_container_logs.submit(container_id=container.id, docker_host=host)
    logs = await logs_future.result()

    removed = await remove_docker_container.submit(container_id=container.id, docker_host=host)
    await removed.wait()

    if exit_code == 0:
        logger.info(logs)
    else:
        raise RuntimeError(logs)

    return exit_code

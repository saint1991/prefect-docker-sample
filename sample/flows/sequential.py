from prefect import flow, get_run_logger

from .util import IMAGE_1, IMAGE_2, docker_tasks


@flow(name="seq_task1_flow")
async def task1_flow():
    return await docker_tasks(image=IMAGE_1)


@flow(name="seq_task2_flow")
async def task2_flow():
    return await docker_tasks(image=IMAGE_2)


@flow(name="sequential flow")
async def sequential():
    """
    a sample execute 2 tasks sequentially
    """
    logger = get_run_logger()

    await task1_flow()
    await task2_flow()

    logger.info("sequential flow has been completed.")

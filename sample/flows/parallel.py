import asyncio

from prefect import flow, get_run_logger

from .util import IMAGE_1, IMAGE_2, docker_tasks


@flow(name="task1_flow")
async def task1_flow():
    return await docker_tasks(image=IMAGE_1)


@flow(name="task2_flow")
async def task2_flow():
    return await docker_tasks(image=IMAGE_2)


@flow(name="parallel flow")
async def parallel():
    """
    a sample execute 2 tasks sequentially
    """
    logger = get_run_logger()

    # note: subflows must have the different names.
    result1 = task1_flow()
    result2 = task2_flow()

    await asyncio.gather(result1, result2)

    logger.info("parallel flow has been completed.")

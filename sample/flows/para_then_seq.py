import asyncio

from prefect import flow, get_run_logger

from .util import IMAGE_1, IMAGE_2, IMAGE_3, docker_tasks


@flow(name="paraseq_task1_flow")
async def task1_flow():
    return await docker_tasks(image=IMAGE_1)


@flow(name="paraseq_task2_flow")
async def task2_flow():
    return await docker_tasks(image=IMAGE_2)


@flow(name="paraseq_flow3_task")
async def task3_flow():
    return await docker_tasks(image=IMAGE_3)


@flow(name="para then sequential flow")
async def para_seq():
    """
    a sample execute 2 tasks sequentially
    """
    logger = get_run_logger()

    # note: subflows must have the different names.
    result1 = task1_flow()
    result2 = task2_flow()

    await asyncio.gather(result1, result2)

    state3 = await task3_flow(return_state=True)
    if state3.is_failed():
        logger.info("Success!")
        return True
    else:
        state3.result()

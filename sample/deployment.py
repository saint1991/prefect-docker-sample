import os
import time
from typing import List

from flows.para_then_seq import para_seq
from flows.parallel import parallel
from flows.sequential import sequential
from prefect.deployments import Deployment
from prefect.filesystems import LocalFileSystem


def _create_storage() -> LocalFileSystem:
    storage = LocalFileSystem(basepath=os.environ["STORAGE_PATH"])
    storage.save(name=os.environ["STORAGE_NAME"], overwrite=True)
    return storage


def _create_deployments(storage: LocalFileSystem) -> List[Deployment]:
    return [
        Deployment.build_from_flow(
            name="sequential sample",
            description="sample deployment of sequential flow",
            storage=storage,
            flow=sequential,
            work_queue_name=os.environ["WORK_QUEUE"],
            path=os.environ["STORAGE_PATH"],
        ),
        Deployment.build_from_flow(
            name="parallel sample",
            description="sample deployment of parallel flow",
            storage=storage,
            flow=parallel,
            work_queue_name=os.environ["WORK_QUEUE"],
            path=os.environ["STORAGE_PATH"],
        ),
        Deployment.build_from_flow(
            name="para then seq sample",
            description="sample deployment of para then seq flow",
            storage=storage,
            flow=para_seq,
            work_queue_name=os.environ["WORK_QUEUE"],
            path=os.environ["STORAGE_PATH"],
        ),
    ]


def main():
    time.sleep(5)

    storage = _create_storage()
    deployments = _create_deployments(storage=storage)
    for deployment in deployments:
        deployment.apply(upload=True)


if __name__ == "__main__":
    main()
    print("Deployments have been applied successfully.")

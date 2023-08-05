"""
Main interface for iot-roborunner service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_iot_roborunner import (
        Client,
        IoTRoboRunnerClient,
        ListDestinationsPaginator,
        ListSitesPaginator,
        ListWorkerFleetsPaginator,
        ListWorkersPaginator,
    )

    session = Session()
    client: IoTRoboRunnerClient = session.client("iot-roborunner")

    list_destinations_paginator: ListDestinationsPaginator = client.get_paginator("list_destinations")
    list_sites_paginator: ListSitesPaginator = client.get_paginator("list_sites")
    list_worker_fleets_paginator: ListWorkerFleetsPaginator = client.get_paginator("list_worker_fleets")
    list_workers_paginator: ListWorkersPaginator = client.get_paginator("list_workers")
    ```
"""
from .client import IoTRoboRunnerClient
from .paginator import (
    ListDestinationsPaginator,
    ListSitesPaginator,
    ListWorkerFleetsPaginator,
    ListWorkersPaginator,
)

Client = IoTRoboRunnerClient


__all__ = (
    "Client",
    "IoTRoboRunnerClient",
    "ListDestinationsPaginator",
    "ListSitesPaginator",
    "ListWorkerFleetsPaginator",
    "ListWorkersPaginator",
)

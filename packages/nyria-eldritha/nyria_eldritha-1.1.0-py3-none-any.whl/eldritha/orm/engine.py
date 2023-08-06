#  All Rights Reserved
#  Copyright (c) 2023 Nyria
#
#  This code, including all accompanying software, documentation, and related materials, is the exclusive property
#  of Nyria. All rights are reserved.
#
#  Any use, reproduction, distribution, or modification of the code without the express written
#  permission of Nyria is strictly prohibited.
#
#  No warranty is provided for the code, and Nyria shall not be liable for any claims, damages,
#  or other liability arising from the use or inability to use the code.

from sqlalchemy import create_engine
from zenith.components.pod import Pod
from zenith.components.pool import Pool
from zenith.services.pool_registry import PoolRegistry

from zenith.ext.exceptions import PoolNotFound
from zenith.stats.permission import Permission

from eldritha.ext.exceptions import EngineAlreadyExists
from sqlalchemy import Engine


class EldrithaEngine:
    @staticmethod
    def create_engine(url: str) -> None:

        """
        This method creates a new engine and adds it to the pool registry.

        Attributes
        ----------
        :param url: The url of the database to connect.
        :return: None
        ----------
        """

        pool: Pool = Pool(
            name="eldritha-orm",
            priority=0,
            permission=Permission.READ_ONLY
        )

        try:
            PoolRegistry.get_pool_by_name("eldritha-orm")
        except PoolNotFound:
            pool.register_pod(
                pod=Pod(
                    name="engine",
                    permission=Permission.READ_ONLY,
                    service_instance=create_engine(url)
                )
            )

            PoolRegistry.create_new_pool(
                pool=pool
            )
            return

        raise EngineAlreadyExists("Engine already exists")

    @staticmethod
    def get_engine() -> Engine:

        """
        This method returns the engine.

        Attributes
        ----------
        :return: Engine
        ----------
        """

        return PoolRegistry.get_pool_by_name("eldritha-orm").get_pod_by_name("engine").get_service()

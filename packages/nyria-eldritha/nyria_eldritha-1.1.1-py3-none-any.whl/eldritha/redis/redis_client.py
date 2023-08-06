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

from redis.client import Redis
from typing import Union
from eldritha.ext.exceptions import RedisAlreadyExists

from zenith.components.pod import Pod
from zenith.components.pool import Pool
from zenith.services.pool_registry import PoolRegistry

from zenith.ext.exceptions import PoolNotFound
from zenith.stats.permission import Permission

class EldrithaRedisClient:
    @staticmethod
    def create_redis(
            host: str,
            port: int,
            db: int,
            username: Union[None, str] = None,
            password: Union[None, str] = None,
            ssl: bool = False,
            ssl_certfile: Union[None, str] = None,
            ssl_keyfile: Union[None, str] = None,
            ssl_ca_certs: Union[None, str] = None
    ) -> None:

        pool: Pool = Pool(
            name="eldritha-redis",
            priority=0,
            permission=Permission.READ_ONLY
        )

        try:
            PoolRegistry.get_pool_by_name("eldritha-redis")
        except PoolNotFound:
            pool.register_pod(
                pod=Pod(
                    name="redis_client",
                    permission=Permission.READ_ONLY,
                    service_instance=Redis(
                        host=host,
                        port=port,
                        db=db,
                        username=username,
                        password=password,
                        ssl=ssl,
                        ssl_certfile=ssl_certfile,
                        ssl_keyfile=ssl_keyfile,
                        ssl_ca_certs=ssl_ca_certs
                    )
                )
            )

            PoolRegistry.create_new_pool(
                pool=pool
            )
            return

        raise RedisAlreadyExists("Engine already exists")

    @staticmethod
    def get_redis_client() -> Redis:

        """
        This method returns the engine.

        Attributes
        ----------
        :return: Redis
        ----------
        """

        return PoolRegistry.get_pool_by_name("eldritha-redis").get_pod_by_name("redis_client").get_service()

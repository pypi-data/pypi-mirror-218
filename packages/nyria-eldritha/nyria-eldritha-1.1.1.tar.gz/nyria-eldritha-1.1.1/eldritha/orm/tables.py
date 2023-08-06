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

from sqlalchemy import Table
from eldritha.orm.engine import EldrithaEngine

from sqlalchemy import Engine

from zenith.components.pool import Pool
from zenith.components.pod import Pod
from zenith.stats.permission import Permission
from zenith.services.pool_registry import PoolRegistry


class EldrithaTable:
    @staticmethod
    def create_tables(tables: list[Table]) -> None:

        """
        Creates all tables in the database.

        Attributes
        ----------
        :param tables: The tables to create.
        :return: None
        ----------
        """

        engine: Engine = EldrithaEngine.get_engine()
        pool = Pool(
            name="eldritha-orm-tables",
            priority=0,
            permission=Permission.READ_ONLY
        )

        for table in tables:
            pod = Pod(
                name=table.name,
                priority=0,
                permission=Permission.READ_ONLY,
                service_instance=table
            )
            pool.register_pod(pod=pod)

            try:
                table.create(bind=engine)
            except Exception:
                continue

        PoolRegistry.create_new_pool(pool=pool)

    @staticmethod
    def get_table_by_name(table_name: str) -> Table:

        """
        Gets a table by its name.

        Attributes
        ----------
        :param table_name: The name of the table.
        :return: The table.
        ----------
        """

        table: Table = PoolRegistry.get_pool_by_name("eldritha-orm-tables").get_pod_by_name(table_name).get_service()
        return table

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

        for table in tables:
            try:
                table.create(bind=engine)
            except Exception:
                continue

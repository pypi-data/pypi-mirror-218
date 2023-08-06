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

from sqlalchemy.orm import Session, sessionmaker
from eldritha.orm.engine import EldrithaEngine


class EldrithaSession:
    @staticmethod
    def create_session() -> Session:

        """
        Creates a session for the database.

        Attributes
        ----------
        :return: Session
        -----------
        """

        session = sessionmaker(bind=EldrithaEngine.get_engine())
        return session()
    
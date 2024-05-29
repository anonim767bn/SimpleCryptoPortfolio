import os
from sqlalchemy.orm import sessionmaker
from models import Base, Building, Street
from datetime import date
from sqlalchemy import select, join

import dotenv
from sqlalchemy import create_engine

from models import Base





def new_func(session):
    street = session.scalar(
                select(Street)
                .where(Street.name == 'Lenina str.')
            )
    if street:
        print([b.number for b in street.buildings])

if __name__ == '__main__':
    engine = create_engine(get_db_url())
    session_factory = sessionmaker(engine)
    Base.metadata.create_all(bind = engine)

    with session_factory() as session:
        with session.begin():
            # home1 = Building(number = 1, founded_date = date.today(), description = None)
            # home2 = Building(number = 2, founded_date = date.today(), description = None)

            # home3 = Building(number = 2, founded_date = date.today(), description = None) 
            # NOTE unique building name on street test

            # session.add(Street(name = 'Lenina str.', buildings = [home1, home2]))



            # dlinnoe_imya = ''.join('a' for _ in range(50))
            # print(dlinnoe_imya, '\n')
            # session.add(Street(name = dlinnoe_imya))
            # NOTE Street name length < 50 test
            new_func(session)
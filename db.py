from sqlalchemy import create_engine, insert
from sqlalchemy.orm import sessionmaker
from models import Base
from models import Portfolio, Asset, Currency, PriceHistory
from dateutil.parser import parse
from api import get_data



def create_db(engine):
    Base.metadata.create_all(bind = engine)

def update_db(session_factory, data):
    with session_factory() as session:
        with session.begin():
            for row in data:
                print(row)
                currency = session.query(Currency).filter_by(name=row['name']).first()
                if not currency:
                    currency = Currency(name=row['name'], symbol=row['symbol'])
                    session.add(currency)
                    session.flush()
                history = PriceHistory(currency_id = currency.id, price=row['price'], timestamp=parse(row['timestamp']))
                session.add(history)



            


if __name__ == '__main__':
    engine = create_engine('sqlite:///db.sqlite')
    SessionFactory = sessionmaker(engine)
    create_db(engine)
    print('DB created')
    data = get_data()
    print('Data fetched')
    update_db(SessionFactory, data)
    print('Data updated')




    

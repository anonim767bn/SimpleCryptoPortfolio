from sqlalchemy import create_engine, insert
from sqlalchemy.orm import sessionmaker
from models import Base
from models import Portfolio, Asset, Currency, PriceHistory, User
from dateutil.parser import parse
from api import get_data
from config import get_db_url


def create_db(engine):
    Base.metadata.create_all(bind=engine)


def update_db(session_factory, data):
    with session_factory() as session:
        with session.begin():
            for row in data:
                currency = session.query(Currency).filter_by(
                    name=row['name']).first()
                if not currency:
                    currency = Currency(name=row['name'], symbol=row['symbol'])
                    session.add(currency)
                    session.flush()
                history = PriceHistory(
                    currency_id=currency.id, price=row['price'], timestamp=parse(row['timestamp']))
                session.add(history)
    
def get_user_from_db(session_factory, username) -> User|None:
    with session_factory() as session:
        return session.query(User).filter_by(username=username).first()

def get_session_factory():
    engine = create_engine(get_db_url())
    Base.metadata.create_all(bind=engine)
    return sessionmaker(engine)

def create_user(session_factory, username, password):
    with session_factory() as session:
        with session.begin():
            user = User(username=username, hash_password=password)
            session.add(user)
            session.flush()
            return user


if __name__ == '__main__':
    engine = create_engine('sqlite:///db.sqlite')
    SessionFactory = sessionmaker(engine)
    create_db(engine)
    print('DB created')
    data = get_data()
    print('Data fetched')
    update_db(SessionFactory, data)
    print('Data updated')

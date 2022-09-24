from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine(
    "sqlite:///tempStorage/sqlite.db",
    connect_args={"check_same_thread": False},
)
db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)

Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    import model.User
    import model.Customer
    import model.File

    Base.metadata.create_all(bind=engine)

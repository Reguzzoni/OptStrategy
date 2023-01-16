import sqlalchemy as sqlalchemy_package
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from dbconfig import DATABASE_URI, DATABASE_SCHEMA

def get_session_from_db():
    # Connect to database and schema
    engine = create_engine(
        DATABASE_URI,
        connect_args={'options': '-csearch_path={}'.format(DATABASE_SCHEMA)}
    )

    # create session to the DB with acid property https://it.wikipedia.org/wiki/ACID
    Session = sessionmaker(bind=engine)
    s = Session()
    return s


if __name__ == "__main__":
    get_session_from_db()


get_session_from_db()
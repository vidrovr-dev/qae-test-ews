import os

from sqlalchemy import URL, create_engine

db_url = URL.create(
    "postgresql+psycopg2",
    username=os.environ['PG_USER'],
    password=os.environ['PG_PW'],
    host=os.environ['PG_HOST'],
    database=os.environ['PG_DB'],
)

engine = create_engine(db_url)

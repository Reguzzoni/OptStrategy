from sqlalchemy import create_engine
from importdata.dbconfig import DATABASE_URI,DATABASE_SCHEMA

import pandas as pd

connection = create_engine(DATABASE_URI,
                           connect_args={'options': '-csearch_path={}'.format(DATABASE_SCHEMA)}).connect()

df = pd.read_sql_table('market_data_2',connection)


df2 = df[0:20]


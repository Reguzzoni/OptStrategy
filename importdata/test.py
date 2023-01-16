# ********************************************************************** #
# * Sqlalchemy Project - Create DB                                     * #
# * Insert data into DB -> postgres_python_marketplace_market_data_3   * #
# ********************************************************************** #

# ******************************************** #
from datetime import datetime

from sqlalchemy import select

from marketDataModel import MarketDataEntity
from DBUtils import get_session_from_db
# ******************************************** #

file_name = "crud.py"

def log(log_value, method_name): (
    print(datetime.now(), " - ", file_name, " : ", method_name, " - ", log_value)
)

def insert_market_data():
    method_name = "insert_market_data"

    # Connect to database and schema
    session = get_session_from_db()
    log("Connected to DB and got session", method_name)

    # create rows to insert into DB
    market_data_to_save = []
    market_data_entity = []

    # *-----------------------------------------------------------------------------------------------------------------*
    # Import data

    # ********************* #
    import pandas as pd
    import numpy as np
    # ********************* #
    # Import Dataset
    file_name = r'C:\Users\rgiul\IdeaProjects\Giu_1\DATI\Output_tick\FX\6E\6E_full.txt'

    # Import data from txt into pandas -> numpy dataset
    def read_file(filename):
        df = pd.read_csv(filename)
        #df = df[10:20]                       # <-- filter for dimension of dataset
        df = df.reset_index(names='Index')
        df = np.array(df)
        return df

    df = read_file(file_name)

    # Create lists of attributes
    Index = []
    Date_Time = []
    Last = []
    Bid = []
    Ask = []
    Volume = []
    Candela = []

    for a in range(0,len(df)):
        Index.append(int(df[a,0]))
        Date_Time.append(str(df[a,1]))
        Last.append(float(df[a,2]))
        Bid.append(float(df[a,3]))
        Ask.append(float(df[a,4]))
        Volume.append(int(df[a,5]))
        Candela.append(int(df[a,6]))

    # Class from list
    for b in range(0,len(df)):
        marekt_data_entity = MarketDataEntity(
            Index = Index[b],
            Date_Time = Date_Time[b],
            Last = Last[b],
            Bid = Bid[b],
            Ask =Ask[b],
            Volume =Volume[b],
            Candela = Candela[b]
        )
        market_data_to_save.append(marekt_data_entity)

    # *-----------------------------------------------------------------------------------------------------------------*

    # insert rows (by bulk collection) into the session
    session.bulk_save_objects(market_data_to_save)
    # commit the transaction to the DB
    session.commit()
    log("Committed to DB", method_name)


    # close session
    session.close()
    log("Closed session", method_name)




def select_all_market_data():
    method_name = "select_all_market_data"

    # Connect to database and schema
    session = get_session_from_db()
    log("Connected to DB and got session", method_name)

    # get all market_data ordered by id
    result = session.execute(select(MarketDataEntity).order_by(MarketDataEntity.Index))
    log("Select results from market_data " + ' '.join(str(v) for v in result.scalars().all()), method_name)

    # close session
    session.close()
    log("Closed session", method_name)

    return result

if __name__ == "__main__":
    # test insert
    print("START insert_market_data")
    insert_market_data()
    print("FINISHED insert_market_data")

    print("START select_all_market_data")
    select_all_market_data()
    print("FINISHED select_all_market_data")





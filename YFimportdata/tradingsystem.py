from importdata import dataset
from metrics import enter_rules,exit_rules
from marketpositions import marketposition_generator
import numpy as np


COSTS = 0
INSTRUMENT = 1 # 1: equity/forex, 2: future
OPERATION_MONEY = 10000
DIRECTION = "long"
ORDER_TYPE = "market"
enter_level = dataset.open
# ----
# ----
def apply_trading_system(imported_dataframe, direction, order_type, enter_level, enter_rules, exit_rules):
    dataframe = imported_dataframe.copy()
    dataframe['enter_rules'] = enter_rules.apply(lambda x: 1 if x == True else 0)
    dataframe['exit_rules'] = exit_rules.apply(lambda x: -1 if x == True else 0)
    dataframe["mp"] = marketposition_generator(dataframe.enter_rules,dataframe.exit_rules)

    if ORDER_TYPE == "market":
        dataframe["entry_price"] = np.where((dataframe.mp.shift(1) == 0) &
                                            (dataframe.mp == 1), dataframe.open, np.nan)
        if INSTRUMENT == 1:
            dataframe["number_of_stocks"] = np.where((dataframe.mp.shift(1) == 0) &
                                                     (dataframe.mp == 1), OPERATION_MONEY / dataframe.open, np.nan)
    dataframe["entry_price"] = dataframe["entry_price"].fillna(method='ffill')
    if INSTRUMENT == 1:
        dataframe["number_of_stocks"] = dataframe["number_of_stocks"] \
            .apply(lambda x: round(x,0)).fillna(method='ffill')
    dataframe["events_in"] = np.where((dataframe.mp == 1) & (dataframe.mp.shift(1) == 0), "entry", "")

    if direction == "long":
        if INSTRUMENT == 1:
            dataframe["open_operations"] = (dataframe.close - dataframe.entry_price) * dataframe.number_of_stocks
            dataframe["open_operations"] = np.where((dataframe.mp == 1) & (dataframe.mp.shift(-1) == 0),
                                                    (dataframe.open.shift(-1) - dataframe.entry_price) * dataframe.number_of_stocks - 2 * COSTS,
                                                    dataframe.open_operations)
    else:
        if INSTRUMENT == 1:
            dataframe["open_operations"] = (dataframe.entry_price - dataframe.close) * dataframe.number_of_stocks
            dataframe["open_operations"] = np.where((dataframe.mp == 1) & (dataframe.mp.shift(-1) == 0),
                                                    (dataframe.entry_price - dataframe.open.shift(-1)) * dataframe.number_of_stocks - 2 * COSTS,
                                                    dataframe.open_operations)

    dataframe["open_operations"] = np.where(dataframe.mp == 1, dataframe.open_operations, 0)
    dataframe["events_out"] = np.where((dataframe.mp == 1) & (dataframe.exit_rules == -1), "exit", "")
    dataframe["operations"] = np.where((dataframe.exit_rules == -1) &
                                       (dataframe.mp == 1), dataframe.open_operations, np.nan)
    dataframe["closed_equity"] = dataframe.operations.fillna(0).cumsum()
    dataframe["open_equity"] = dataframe.closed_equity + \
                               dataframe.open_operations - dataframe.operations.fillna(0)
    dataframe.to_csv("trading_system_export.csv")
    return dataframe
# ----
# ----
trading_system = apply_trading_system(dataset, DIRECTION, ORDER_TYPE, enter_level, enter_rules, exit_rules)
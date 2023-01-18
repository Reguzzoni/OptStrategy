from importdata import dataset

def indicator(data):
    # bollinger band
    data["hhv20"] = data.high.rolling(20).max()
    data["llv20"] = data.low.rolling(20).min()

    # donchian channel
    data["hhv5"] = data.high.rolling(5).max()
    data["llv5"] = data.low.rolling(5).min()

    data.dropna(inplace=True)
    return data

def crossover(array1, array2):
    return (array1 > array2) & (array1.shift(1) < array2.shift(1))

def crossunder(array1, array2):
    return (array1 < array2) & (array1.shift(1) > array2.shift(1))


# define rule
enter_rules = crossover(dataset.close,dataset.hhv20.shift(1))
exit_rules = crossunder(dataset.close,dataset.llv5.shift(1)) | (dataset.day < dataset.day.shift(1))


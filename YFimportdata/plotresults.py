import matplotlib.pyplot as plt
from tradingsystem import trading_system

def plot_equity(equity,color):
    """
    print equity line
    """
    plt.figure(figsize=(14, 8), dpi=300)
    plt.plot(equity, color=color)
    plt.xlabel("Time")
    plt.ylabel("Profit/Loss")
    plt.title('Equity Line')
    plt.xticks(rotation='vertical')
    plt.grid(True)
    plt.show()
    return

plot_equity(trading_system.closed_equity,"red");
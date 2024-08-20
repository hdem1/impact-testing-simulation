import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.animation as animation

# The list of colors that are always used:
COLOR_LIST = ['r', 'b', 'g']

"""
Creating a simple graph with one data series:
"""
def plot_simple(x_values, y_values, x_label, y_label, plot_title):
    fig, ax = plt.subplots()
    ax.plot(x_values, y_values)
    ax.set(xlabel=x_label, ylabel=y_label, title=plot_title)
    ax.grid()
    plt.show()

"""
Creating a graph with multiple data series:
"""
def plot_mult(x_values, y_lists, x_label, y_labels, plot_title):
    fig, ax1 = plt.subplots()
    ax1.set_xlabel(x_label)

    for i, y_list in enumerate(y_lists):
        ax1.set_ylabel(y_labels[i], color = COLOR_LIST[i])
        ax1.tick_params(axis='y', color=COLOR_LIST[i],labelcolor=COLOR_LIST[i])
        ax1.plot(x_values, y_list, COLOR_LIST[i], lw=2, label=y_labels[i])
        if (i < len(y_lists) - 1):
            ax1 = ax1.twinx()

    plt.title(plot_title)
    plt.grid()
    plt.show()
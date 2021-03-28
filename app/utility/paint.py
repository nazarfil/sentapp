
import matplotlib.dates as mdates
import matplotlib as mpl
import pandas as pd
import numpy as np

mpl.use('Agg')

import matplotlib.pyplot as plt

def draw_graphs(all_scores, name, path="static/images"):
    fig, ax = plt.subplots()
    num_colors = 4
    cm = plt.get_cmap('Dark2')
    #ax.set_prop_cycle(color=[cm(1. * (i) / num_colors) for i in range(num_colors)])
    filename = '{}.png'.format(name)
    for key, curve in all_scores.items():
        df = pd.DataFrame(curve)
        plt.plot_date(df['date'], df[name], '-', label=key)
        plt.xticks(df['date'])

    plt.ylabel('Graph: {}'.format(name))
    format_months = mdates.DateFormatter('%B-%d')
    ax.xaxis.set_major_formatter(format_months)
    # Shrink current axis's height by 10% on the bottom
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.1,
                     box.width, box.height * 0.9])

    # Put a legend below current axis
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5),
              shadow=True)
    fig.autofmt_xdate()
    fig.savefig(filename, bbox_inches='tight')
    # format the ticks
    plt.close(fig)


def draw_sparkline(points, name, path="static/images"):
    filename = '{}/{}.png'.format(path, name)
    arr = np.array(points)
    fig, ax = plt.subplots(1,1,figsize=(3,1))
    plt.plot(arr, '-')
    plt.axis('off')
    fig.savefig(filename, bbox_inches='tight')
    plt.close(fig)
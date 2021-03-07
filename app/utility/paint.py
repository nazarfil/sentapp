
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd

def draw_graphs(all_scores, name):
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
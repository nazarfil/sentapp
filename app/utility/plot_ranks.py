from datetime import datetime
import matplotlib.dates as mdates
from matplotlib.backends.backend_pdf import PdfPages

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def energy_rank(data, marker_width=.5, color='blue'):
    y_data = np.repeat(data, 2)
    x_data = np.empty_like(y_data)
    x_data[0::2] = np.arange(1, len(data)+1) - (marker_width/2)
    x_data[1::2] = np.arange(1, len(data)+1) + (marker_width/2)
    lines = []
    lines.append(plt.Line2D(x_data, y_data, lw=1, linestyle='dashed', color=color))
    for x in range(0,len(data)*2, 2):
        lines.append(plt.Line2D(x_data[x:x+2], y_data[x:x+2], lw=2, linestyle='solid', color=color))
    return lines

data = np.random.rand(6,10) * 4 # 4 lines with 8 datapoints from 0 - 4

def other_rank(data, marker_width=.5, color='blue'):
    datelist=data[:0]
    converted_dates = list(map(datetime.strptime, datelist, len(datelist) * ['%Y-%m-%d']))
    x_data = converted_dates
    y_data = data[:2]
    lines = []
    for x in range(0,len(data)*2, 2):
        lines.append(plt.Line2D(x_data[x:x+2], y_data[x:x+2], lw=2, linestyle='solid', color=color))
    return lines


df = pd.read_csv('ranks.csv' ,header=None, index_col=False)
transformed_df = [df.iloc[(i)::6] for i in range(6)]
#print(transformed_df[2][:].to_string(index=False, header=False))

fig, ax = plt.subplots()
years = mdates.YearLocator()   # every year
months = mdates.MonthLocator()  # every month
months = mdates.DayLocator()  # every month
ax.format_xdata = mdates.DateFormatter('%m-%d')
for tdf in transformed_df:
    tdf.plot(kind='scatter', x=0, y=1, ax=ax, marker='o')
    tdf[[0, 1, 3]].apply(lambda row: ax.text(*row), axis=1);
fig.autofmt_xdate()
plt.gca().invert_yaxis()

#pdf = PdfPages('longplot.pdf')
#pdf.savefig()
#pdf.close()
plt.show()

"""

df = pd.read_csv('ranks.csv')
df.head()
plt.figure()
every_1 = df.iloc[::6]
every_2 = df.iloc[1::6]
every_3 = df.iloc[2::6]
every_4 = df.iloc[3::6]
print(every_4)
plt.plot()
plt.show()
"""
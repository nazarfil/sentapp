import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages


def create_lines(dfs):
    line_dict = {}
    for df in dfs:
        for index, row in df.iterrows():
            point = (row[0], row[1])
            label = row[3]
            if label in line_dict:
                line_dict[label].append(point)
            else:
                line_dict[label] = [point]
    return line_dict

def draw_pdf():
    pdf = PdfPages('longplot.pdf')
    pdf.savefig()
    pdf.close()

df = pd.read_csv('ranks.csv', header=None, index_col=False)

transformed_df = [df.iloc[(i)::6] for i in range(6)]
for df in transformed_df:
    df[0]= pd.to_datetime(df[0], format='%Y-%m-%d')

fig, ax = plt.subplots()
years = mdates.YearLocator()  # every year
months = mdates.MonthLocator()  # every month
months = mdates.DayLocator()  # every month
ax.format_xdata = mdates.DateFormatter('%m-%d')
lines_dict = create_lines(transformed_df)


for key,val in lines_dict.items():
    sorted_val = sorted(val,  key=lambda tup: tup[0])
    for item in val:
        ax.annotate(key,item)
    ax.plot(*zip(*sorted_val), linestyle='dashed', marker='o')


plt.gca().invert_yaxis()


plt.show()


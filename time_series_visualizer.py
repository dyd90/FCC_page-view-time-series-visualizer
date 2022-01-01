import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import os
from datetime import date
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

#Date order string
DATE_ORDER = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

def get_forward_month_list():
    now = date(date.today().year, 1, 1)
    return [(now + relativedelta(months=i)).strftime('%B') for i in range(12)]

# get full list of dates: 'January', 'February'...
DATE_ORDER_FULL = get_forward_month_list()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv(os.getcwd() +  "/fcc-forum-pageviews.csv")
df['date'] = df.apply (lambda row: datetime.strptime(row['date'], '%Y-%m-%d'), axis=1)
df.set_index('date', inplace=True, drop=False)


# Clean data
df = df[(df['value'] >= df['value'].quantile(0.025)) 
  & (df['value'] <= df['value'].quantile(0.975))]

def draw_line_plot():
    # Draw line plot
    fig = plt.figure()
    plt.plot(df['date'],df['value'])
    plt.xlabel("Date")
    plt.ylabel("Page Views")
    plt.title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    # add year and month
    df_bar['Years'] = df_bar.apply (lambda row: row['date'].year, axis=1)
    df_bar['Months'] = df_bar.apply (lambda row: row['date'].strftime("%B"), axis=1)
    df_piv = df_bar.groupby(['Years','Months'])['value'].sum().unstack().reset_index().set_index('Years')
    #re-order the columns
    df_piv = df_piv[DATE_ORDER_FULL].copy()
    # plot grouped bar chart
    fig = df_piv.plot(
            kind='bar',
            stacked=False,
            title='Months').get_figure()

    # Draw bar plot

    plt.xlabel("Years")
    plt.ylabel("Average Page Views")

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    #df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)

    fig, axes = plt.subplots(1, 2)
    sns.boxplot(
      x='year'
      , y='value'
      , orient='v'
      , ax=axes[0]
      , data=pd.melt(
          df_box
          , id_vars = ['year']
          , value_vars =['value']
        )
      )
    axes[0].set_title("Year-wise Box Plot (Trend)")
    axes[0].set_xlabel("Year")
    axes[0].set_ylabel("Page Views")
    sns.boxplot(
      x='month'
      , y='value'
      , orient='v'
      , ax=axes[1]
      , data=pd.melt(
          df_box
          , id_vars = ['month']
          , value_vars =['value']
        )
      , order=DATE_ORDER
      )
    axes[1].set_title("Month-wise Box Plot (Seasonality)")
    axes[1].set_xlabel("Month")
    axes[1].set_ylabel("Page Views")

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig

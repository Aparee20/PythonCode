
import csv
import sqlite3

def insert_csv_to_sqlite(db_name, table_name, columns):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Create the table with the specified columns
    create_table_query = f"CREATE TABLE {table_name} ({','.join(columns)})"
    cursor.execute(create_table_query)

    # Read the CSV file and insert the data into the table
    with open(f"{table_name}.csv", 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)  # skip the header row
        for row in csv_reader:
            insert_query = f"INSERT INTO {table_name} VALUES ({','.join(['?']*len(columns))})"
            cursor.execute(insert_query, row)

    conn.commit()
    conn.close()




from GoogleNews import GoogleNews
from newspaper import Article
import pandas as pd
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import os
import pandas as pd
import matplotlib.pyplot as plt
# %matplotlib inline

from nltk.sentiment.vader import *


TellmeAbout="AMP shares"

googlenews=GoogleNews(start='16/08/2020',end='19/08/2020')
googlenews.search(TellmeAbout)
result=googlenews.result()
df=pd.DataFrame(result)

if df.empty:
    print("No News for the time frame ")
    exit()
else:
    pd.DataFrame(result).assign(name=TellmeAbout)

print(df.head())
print(df.columns)



vader = SentimentIntensityAnalyzer()

# Set column names
columns = df.columns

# Convert the parsed_news list into a DataFrame called 'parsed_and_scored_news'
parsed_and_scored_news = df#pd.DataFrame(df, columns=columns)

# Iterate through the headlines and get the polarity scores using vader
scores = parsed_and_scored_news['title'].apply(vader.polarity_scores).tolist()
print(scores)

# Convert the 'scores' list of dicts into a DataFrame
scores_df = pd.DataFrame(scores)
print(scores_df.head())
#
# Join the DataFrames of the news and the list of dicts
parsed_and_scored_news = parsed_and_scored_news.join(scores_df, rsuffix='_right')

print(parsed_and_scored_news)

# Convert the date column from string to datetime
#parsed_and_scored_news['date'] = pd.to_datetime(parsed_and_scored_news.date).dt.date

print("\n ---Here are your details")
print(parsed_and_scored_news.head())

print(parsed_and_scored_news.head())


plt.rcParams['figure.figsize'] = [10, 6]

# Group by date and ticker columns from scored_news and calculate the mean
mean_scores = parsed_and_scored_news.groupby(['name','date']).mean()

# Unstack the column ticker
mean_scores = mean_scores.unstack()

# Get the cross-section of compound in the 'columns' axis
mean_scores = mean_scores.xs('compound', axis="columns").transpose()

# Plot a bar chart with pandas
mean_scores.plot(kind = 'bar')
plt.grid()

plt.show()
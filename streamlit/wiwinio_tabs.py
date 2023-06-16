import streamlit as st
import numpy as np
from typing import Any
import sqlite3
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt

conn = sqlite3.connect(r"data/vivino.db")
tab1, tab2, tab3, tab4 = st.tabs(["Highlights", "Country marketing", 'Best Winery', "Fine palates"])
cursor = conn.cursor()

with tab1:
    query = """SELECT wines.name, ROUND(vintages.price_euros, 2) AS price_euros,  wines.ratings_average, vintages.bottle_volume_ml, wines.ratings_count, wines.url, wines.id
FROM wines
INNER JOIN vintages
ON wines.id = vintages.wine_id
WHERE wines.ratings_count > 200 AND wines.ratings_average > 3.8
ORDER BY (vintages.price_euros/wines.ratings_average/vintages.bottle_volume_ml) ASC
LIMIT 10;"""
    cursor.execute(query)
    Names = []
    Prices = []
    Ratings = []
    RatingsCounts = []
    BottleMl = []
    for i in cursor:
        Names.append(i[0])
        Prices.append(i[1])
        Ratings.append(i[2])
        BottleMl.append(i[3])
        RatingsCounts.append(i[4])
    chart_data = pd.DataFrame(list(zip(Names, Prices, Ratings, RatingsCounts, BottleMl)),
                            columns =['name', 'price', 'rating','rating_count', 'bottle_ml'])
    chart_data.set_index('name', inplace=True)
    chart_data['price_per750ml']= chart_data['price'] / chart_data['bottle_ml'] *750
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax2 = ax.twinx()
    ax2.set_yscale('log')
    width = 0.4
    chart_data.price_per750ml.plot(kind='bar', color='#e8796d', ax=ax, width=width, position=1)
    chart_data.rating_count.plot(kind='bar', color='#5e850b', ax=ax2, width=width, position=0)

    ax.set_ylabel('Price normalized (€/750ml)')
    ax2.set_ylabel('Number of ratings')
    st.pyplot(fig)

with tab2:
    
    query = "SELECT name, users_count, wineries_count FROM countries WHERE wineries_count > 1200 ORDER BY users_count ASC;"

    cursor.execute(query)
    CountryName = []
    UsersCount = []
    WineriesCount = []
    PopCountry = [10600000, 9700000, 59390000, 19490000, 45810000, 25690000, 10330000, 
                8703000, 47420000, 83200000, 59110000, 67750000, 331900000]
    for i in cursor:
        CountryName.append(i[0])
        UsersCount.append(i[1])
        WineriesCount.append(i[2])


    chart_data = pd.DataFrame(list(zip(CountryName, UsersCount, PopCountry, WineriesCount)),
                columns =['countries', 'users', 'population','wineries'])
    #
    #'
    cols_to_melt = ['users', 'population', 'wineries']
    cols_to_keep = chart_data.columns.difference(cols_to_melt)
    chart_data['user_per_population']= chart_data['users']/chart_data['population']
    chart_data['winery_per_population']= chart_data['wineries']/chart_data['population']
    chart_data.set_index('countries', inplace=True)
    chart_data = chart_data.sort_values('user_per_population')
    #chart_data = chart_data.melt(id_vars='countries', value_vars=['user_per_population', 'user_per_winery'], var_name='type')

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax2 = ax.twinx()

    width = 0.4

    chart_data.user_per_population.plot(kind='bar', color='#1aa178', ax=ax, width=width, position=1)
    chart_data.winery_per_population.plot(kind='bar', color='#146491', ax=ax2, width=width, position=0)


    ax.set_ylabel('Users over total population')
    ax2.set_ylabel('Wineries over total population')
    plt.grid()
    st.pyplot(fig)

with tab3:
    query = """
SELECT wineries.name, 
ROUND(AVG(vintages.price_euros),2)  AS winery_avg_price, 
ROUND(AVG(vintages.ratings_average),2)  AS winery_avg_rating, 
ROUND(AVG(vintages.ratings_count),2) AS avg_ratings_count, 
AVG(vintages.price_euros/(vintages.ratings_average)) AS metric, 
COUNT(vintages.name) AS number_of_vintages
FROM vintages
INNER JOIN wines
ON vintages.wine_id = wines.id
INNER JOIN wineries
ON wines.winery_id = wineries.id 
GROUP BY wineries.name
HAVING ROUND(AVG(vintages.price_euros/vintages.ratings_average),2) IS NOT NULL
    AND AVG(vintages.ratings_count) > 50
    AND COUNT(*) > 1
    AND number_of_vintages > 3
    AND winery_avg_rating > 3
ORDER BY metric ASC
LIMIT 8;"""
    cursor.execute(query)
    Names = []
    Prices = []
    Ratings = []
    RatingsCounts = []
    NumberOfVintages = []
    for i in cursor:
        Names.append(i[0])
        Prices.append(i[1])
        Ratings.append(i[2])
        RatingsCounts.append(i[3])
        NumberOfVintages.append(i[5])
   
    chart_data = pd.DataFrame(list(zip(Names, Prices, Ratings, RatingsCounts, BottleMl)),
                            columns =['name', 'price', 'rating','rating_count', 'nb_of_vintages'])
    chart_data.set_index('name', inplace=True)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax2 = ax.twinx()
    width = 0.4
    chart_data.price.plot(kind='bar', color='#e8796d', ax=ax, width=width, position=1)
    chart_data.rating.plot(kind='bar', color='#5e850b', ax=ax2, width=width, position=0)

    ax.set_ylabel('Average bottle price (€)')
    ax2.set_ylabel('Average rating per vintage (out-of-5)')
    st.pyplot(fig)

with tab4:
    query = """
SELECT  wines.name, ROUND(vintages.price_euros, 2) AS price_euros,  wines.ratings_average, wines.ratings_count
FROM wines
JOIN keywords_wine
ON wines.id = keywords_wine.wine_id
JOIN vintages
ON wines.id = vintages.wine_id
JOIN keywords
ON keywords_wine.keyword_id =  keywords.id
WHERE keywords_wine.count > 10 
    AND keywords.name IN ('coffee','toast','green apple','cream','citrus')
    AND keywords_wine.keyword_type = 'primary'
GROUP BY wines.name
HAVING COUNT(wines.name)=5;"""
    cursor.execute(query)
    Names = []
    Prices = []
    Ratings = []
    RatingsCounts = []
    for i in cursor:
        Names.append(i[0])
        Prices.append(i[1])
        Ratings.append(i[2])
        RatingsCounts.append(i[3])

    chart_data = pd.DataFrame(list(zip(Names, Prices, Ratings, RatingsCounts)),
                            columns =['name', 'price', 'rating','rating_count'])
    chart_data.set_index('name', inplace=True)
    fig = plt.figure()
    ax = fig.add_subplot(111)

    width = 0.4

    #s = [20*4**n for n in range(len(x))]

    plt.scatter(x=chart_data['price'], y=chart_data['rating_count'], alpha=0.5,
            s=chart_data['rating']*30)
    #ax.set_ylim([0, 5])
    ax.set_ylabel('Avg rating')
    ax.set_xlabel('Price (€)')
    plt.grid()
    st.pyplot(fig)


# Streamlit widgets automatically run the script from top to bottom. Since
# this button is not connected to any other logic, it just causes a plain
# rerun.
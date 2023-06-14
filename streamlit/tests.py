import streamlit as st
import numpy as np
from typing import Any
import sqlite3
import pandas as pd
import altair as alt

conn = sqlite3.connect(r"data/vivino.db")
cursor = conn.cursor()
query = "SELECT name, users_count, wineries_count FROM countries WHERE wineries_count > 1200 ORDER BY users_count ASC;"

cursor.execute(query)
CountryName = []
UsersCount = []
WineriesCount = []
PopCountry = []
for i in cursor:
    CountryName.append(i[0])
    UsersCount.append(i[1])
    WineriesCount.append(i[2]*50)

chart_data = pd.DataFrame(list(zip(CountryName, UsersCount, WineriesCount)),
               columns =['Countries', 'Users', 'Wineries'])
chart_data.set_index('Countries')



alt.Chart(chart_data.melt('Countries', )).mark_bar(opacity=0.7).encode(
    x='Countries:O',
    y=alt.Y('Users:Q').stack(None),
    color="source",
)


# Streamlit widgets automatically run the script from top to bottom. Since
# this button is not connected to any other logic, it just causes a plain
# rerun.
st.button("Re-run")

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
               columns =['countries', 'users', 'wineries'])
#
#'
cols_to_melt = ['users', 'wineries']
cols_to_keep = chart_data.columns.difference(cols_to_melt)

chart_data = chart_data.melt(id_vars='countries', value_vars=['users', 'wineries'], var_name='type')
print(chart_data)
c= alt.Chart(chart_data).mark_bar(opacity=0.7).encode(
    x='countries:O',
    y=alt.Y('type:Q').stack(None),
    color = 'value'
)


st.altair_chart(c, use_container_width=True)

# Streamlit widgets automatically run the script from top to bottom. Since
# this button is not connected to any other logic, it just causes a plain
# rerun.
st.button("Re-run")

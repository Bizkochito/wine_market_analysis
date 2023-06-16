# wine_market_analysis
Wine market analysis, as mock-company simulation

## Introduction
This repository uses data scraped out of Vivino, and explores it a little.  
A SQL file shows some table results for some typical questions to be asked about the wine market, and the Vivino userbase.  
The streamlit repository holds a python file that runs mostly the same SQL requests, and plots them nicely inside different tabs on a streamlit app.
## Requirements
It is recommended to install the libraries listed in the requirements.txt,  
for instance using:  
```
pip install -r requirements.txt
```
## Streamlit
To get the best display, you can run, from your command line, localized in the base file of this repo:
```
streamlit run streamlit/tests_plt.py      
```
It opens inside your default browser. Browse the tabs to have a look at the different graphs.

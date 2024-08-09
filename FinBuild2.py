import requests
from bs4 import BeautifulSoup
import pandas as pd
import yfinance as yf


# Scrapes S%P 500 wikipedia page for up-to-date tickers
def scrape_sp500_tickers():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', {'id': 'constituents'})
    tickers = []
    for row in table.find_all('tr')[1:]:
        ticker = row.find_all('td')[0].text.strip()
        ticker = ticker.replace('.', '-') # Formats BRK.B and BF.B tickers correctly
        tickers.append(ticker)
    return tickers

tickers = scrape_sp500_tickers()

# Fetches current market cap value for each ticker
def fetch_market_cap(tickers):
    market_caps = {}
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            market_cap = stock.info['marketCap']
            market_caps[ticker] = market_cap
        except Exception as e:
            print(f"Failed to fetch data for {ticker}: {e}")
    return market_caps

market_caps_data = fetch_market_cap(tickers).items()

# Splitting into 'Ticker' and 'Market Cap' lists
tickers = []
market_caps = []
for ticker, market_cap in market_caps_data:
    tickers.append(ticker)
    market_caps.append(market_cap)

# Build dataframe
data = {
    'Ticker' : tickers,
    'Market Cap' : market_caps
}
df = pd.DataFrame(data)
df_sorted = df.sort_values(by='Market Cap', ascending=False)
df_sorted_reset = df_sorted.reset_index(drop=True)
df_sorted_reset.index = df_sorted_reset.index + 1

n = 20 # choose the number of stocks to be visible in our dataframe
top_n_companies = df_sorted_reset.head(n)
print(top_n_companies)
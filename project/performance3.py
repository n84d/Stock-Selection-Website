import pandas as pd
import numpy as np
import yfinance as yf
import warnings

# Suppress FutureWarnings from yfinance
warnings.simplefilter(action='ignore', category=FutureWarning)

q1 = pd.read_excel('C:/Users/nford1/Documents/StockPicks/PredictionsDatabase.xlsx', sheet_name='23q4')
q2 = pd.read_excel('C:/Users/nford1/Documents/StockPicks/PredictionsDatabase.xlsx', sheet_name='24q1')
q3 = pd.read_excel('C:/Users/nford1/Documents/StockPicks/PredictionsDatabase.xlsx', sheet_name='24q2')

# make a list of all predictions
dfs = [q1, q2, q3]

start_dates = ["2023-10-02", "2024-01-02", "2024-04-02"]

n_top = 10

# what would the returns be if you followed the top 10 stocks?
def top_ten_strategy_info():

    individual_cum_returns = []
    average_cumulative_returns = []
    daily_returns = []
    average_daily_returns = []

    for quarter_index, (quarter, start_date) in enumerate(zip(dfs, start_dates)):

        # after establishing how many we want to hold, we show what that strategy would have done
        selected_stocks = quarter.iloc[:n_top, 0]
        close_prices = []
        start_date_timestamp = pd.to_datetime(start_date)

        # Calculate the end date for this quarter
        if quarter_index < len(start_dates) - 1:
            end_date_timestamp = pd.to_datetime(start_dates[quarter_index + 1])
        else:
            end_date_timestamp = pd.Timestamp.now()

        # between the desired start and end, obtain the daily close prices
        for ticker in selected_stocks:
            stock = yf.Ticker(ticker)
            information = stock.history(start=start_date_timestamp, end=end_date_timestamp)
            close_prices.append(information['Close'])

        # make the close prices a nice dataframe
        close_prices = pd.DataFrame(close_prices).T
        close_prices.columns = selected_stocks
        pct_changes = pd.DataFrame(close_prices.pct_change() + 1)
        cum_ret = pd.DataFrame(pct_changes.cumprod())

        # individual stock cumulative returns
        individual_cum_returns.append(cum_ret)

        # portfolio cumulative returns
        average_cumulative_returns.append(cum_ret.mean(axis=1))

        # individual stock daily_returns
        daily_returns.append(pct_changes)

        # portfolio daily returns
        average_daily_returns.append(pct_changes.mean(axis=1))
    
    portfolio_cum_returns = []

    for quarter_index, returns in enumerate(average_daily_returns):
        for index, item in enumerate(returns):
            timestamp = returns.index[index]
            portfolio_cum_returns.append((timestamp, item))

    portfolio_cum_returns = pd.DataFrame(portfolio_cum_returns, columns=['Timestamp', 'Top 10 Returns'])
    portfolio_cum_returns['Top 10 Returns'] = portfolio_cum_returns['Top 10 Returns'].cumprod()

    return individual_cum_returns, portfolio_cum_returns

def benchmark_cum_returns(portfolio_cum_returns):

    benchmark = yf.Ticker('SPY')

    # this will expire, eventually we will need to change this to 5y
    information = benchmark.history(period='2y')
    information = information.iloc[-len(portfolio_cum_returns):, :]

    close_prices = information["Close"]
    
    # Make the close prices a nice dataframe
    close_prices = pd.DataFrame(close_prices)
    pct_changes = pd.DataFrame(close_prices.pct_change() + 1)
    cum_ret = pd.DataFrame(pct_changes.cumprod())

    return cum_ret

def compare_top_10():

    port = top_ten_strategy_info()[1]
    bench = benchmark_cum_returns(port)

    port.set_index('Timestamp', inplace=True)
    merged_df = pd.merge(port, bench, left_index=True, right_index=True)

    merged_df['Top 10 Returns']= merged_df['Top 10 Returns'].interpolate(method='linear')

    return merged_df

thresh = .55

# what would the returns be if you followed the top 10 stocks?
def threshold_strategy_info():

    individual_cum_returns = []
    average_cumulative_returns = []
    daily_returns = []
    average_daily_returns = []

    for quarter_index, (quarter, start_date) in enumerate(zip(dfs, start_dates)):

        if 'Prediction' not in quarter.columns:
            print("Error: 'Prediction' column not found in DataFrame.")
            continue
        
        if not quarter['Prediction'].dtype in ('float64', 'int64'):
            print("Error: 'Prediction' column does not contain numeric values.")
            continue

        # Filter stocks with 'Prediction' >= 0.55
        selected_stocks = quarter[quarter['Prediction'] >= thresh]['Ticker'].tolist()

        start_date_timestamp = pd.to_datetime(start_date)

        # Calculate the end date for this quarter
        if quarter_index < len(start_dates) - 1:
            end_date_timestamp = pd.to_datetime(start_dates[quarter_index + 1])
        else:
            end_date_timestamp = pd.Timestamp.now()

        # between the desired start and end, obtain the daily close prices    
        close_prices = []
        for ticker in selected_stocks:
            stock = yf.Ticker(ticker)
            information = stock.history(start=start_date_timestamp, end=end_date_timestamp)
            close_prices.append(information['Close'])

        # make the close prices a nice dataframe
        close_prices = pd.DataFrame(close_prices).T
        close_prices.columns = selected_stocks
        pct_changes = pd.DataFrame(close_prices.pct_change() + 1)
        cum_ret = pd.DataFrame(pct_changes.cumprod())

        # individual stock cumulative returns
        individual_cum_returns.append(cum_ret)

        # portfolio cumulative returns
        average_cumulative_returns.append(cum_ret.mean(axis=1))

        # individual stock daily_returns
        daily_returns.append(pct_changes)

        # portfolio daily returns
        average_daily_returns.append(pct_changes.mean(axis=1))
    
    portfolio_cum_returns = []

    for quarter_index, returns in enumerate(average_daily_returns):
        for index, item in enumerate(returns):
            timestamp = returns.index[index]
            portfolio_cum_returns.append((timestamp, item))

    portfolio_cum_returns = pd.DataFrame(portfolio_cum_returns, columns=['Timestamp', 'Threshold Returns'])
    portfolio_cum_returns['Threshold Returns'] = portfolio_cum_returns['Threshold Returns'].cumprod()

    return individual_cum_returns, portfolio_cum_returns

def compare_threshold():

    port = threshold_strategy_info()[1]
    bench = benchmark_cum_returns(port)

    port.set_index('Timestamp', inplace=True)
    merged_df = pd.merge(port, bench, left_index=True, right_index=True)

    merged_df['Threshold Returns']= merged_df['Threshold Returns'].interpolate(method='linear')

    return merged_df

def compare_strategies():
    
    top_10_comp = compare_top_10()
    thresh_comp = compare_threshold()
    bench = benchmark_cum_returns(top_10_comp)

    top_10_ret = top_10_comp['Top 10 Returns']
    thresh_ret = thresh_comp['Threshold Returns']
    
    comparison = pd.concat([bench, top_10_ret, thresh_ret], axis=1)

    return comparison.interpolate(method='linear').fillna(1)

def get_pred_lists():
    info = []
    for df in dfs:
        # Round values in the second column and create a copy of the DataFrame
        rounded_df = df.copy()
        rounded_df.iloc[:, 1] = rounded_df.iloc[:, 1].round(decimals=5)
        info.append(rounded_df.iloc[:10, :])
    
    return info

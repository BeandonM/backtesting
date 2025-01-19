import pandas as pd
import yfinance as yf

#Grabs the OHLCV data from Yahoo Finance
def get_yfinance_data(ticker: str, start: str, end: str, interval: str="1d") -> pd.DataFrame:
    """
    Fetches OHLCV (Open, High, Low, Close, Volume) data from Yahoo Finance for a given ticker.

    Parameters:
        ticker (str): The ticker symbol of the stock or asset (e.g., "AAPL" for Apple).
        start (str): The start date for the data in the format "YYYY-MM-DD".
        end (str): The end date for the data in the format "YYYY-MM-DD".
        interval (str): The time interval for the data. Default is "1d" (daily).
                       Supported intervals include "1m", "2m", "5m", "15m", "30m", "60m", "1h", 
                       "1d", "5d", "1wk", "1mo", "3mo".

    Returns:
        pd.DataFrame: A DataFrame containing the OHLCV data with the following columns:
                      - Open
                      - High
                      - Low
                      - Close
                      - Adj Close (adjusted close)
                      - Volume

    Example:
        >>> data = get_yfinance_data("AAPL", "2023-01-01", "2023-12-31", interval="1d")
        >>> print(data.head())
                  Open      High       Low     Close  Adj Close    Volume
        Date
        2023-01-03  130.26   130.90    124.17   125.07     125.07  123450000
    """
    data = yf.download(ticker, start=start, end=end, interval=interval)
    
    return data

def set_date_index(data: pd.DataFrame) -> pd.DataFrame:
    """
    Converts the 'Date' column of a DataFrame to a datetime object, sets it as the index, and removes the index name.

    Parameters:
        data (pd.DataFrame): A DataFrame containing a 'Date' column that needs to be set as the index.

    Returns:
        pd.DataFrame: The modified DataFrame with the 'Date' column converted to a datetime index and unnamed.

    Example:
        >>> data = pd.DataFrame({
        ...     'Date': ['2023-01-01', '2023-01-02'],
        ...     'Value': [100, 200]
        ... })
        >>> updated_data = set_date_index(data)
        >>> print(updated_data)
                          Value
        2023-01-01       100
        2023-01-02       200

    Notes:
        - The original index of the DataFrame is reset.
        - Ensure the 'Date' column exists and is properly formatted as a date-like string or object before using this function.
    """
    data = data.reset_index()
    data['Date'] = pd.to_datetime(data['Date'])
    data = data.set_index('Date')
    data.index.name = None
    return data

def flatten_and_select_columns(data: pd.DataFrame) -> pd.DataFrame:
    """
    Flattens MultiIndex columns (if present) in a DataFrame and selects specific OHLCV columns.

    Parameters:
        data (pd.DataFrame): A DataFrame containing financial data. If the columns are a MultiIndex, 
                             the second level will be dropped.

    Returns:
        pd.DataFrame: A DataFrame containing only the 'Open', 'High', 'Low', 'Close', and 'Volume' columns.

    Example:
        >>> data = pd.DataFrame({
        ...     ('Price', 'Open'): [100, 110],
        ...     ('Price', 'High'): [120, 115],
        ...     ('Price', 'Low'): [95, 105],
        ...     ('Price', 'Close'): [115, 108],
        ...     ('Data', 'Volume'): [1000, 1200]
        ... })
        >>> flattened_data = flatten_and_select_columns(data)
        >>> print(flattened_data)
             Open  High  Low  Close  Volume
        0    100   120   95    115    1000
        1    110   115  105    108    1200

    Notes:
        - If the DataFrame does not have a MultiIndex, no changes are made to the column structure.
        - The method assumes that the selected columns ('Open', 'High', 'Low', 'Close', 'Volume') 
          are present in the DataFrame.

    Raises:
        KeyError: If any of the selected columns ('Open', 'High', 'Low', 'Close', 'Volume') 
                  are missing from the DataFrame.
    """
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.droplevel(1)
    data = data[['Open', 'High', 'Low', 'Close', 'Volume']]
    return data

def get_ticker_data(ticker: str, start: str, end: str, interval: str="1d"):
    """
    Fetches and processes financial OHLCV data for a given ticker from Yahoo Finance.

    This method:
    1. Retrieves raw financial data for the specified ticker and date range using the Yahoo Finance API.
    2. Converts the 'Date' column to a datetime index.
    3. Flattens MultiIndex columns (if present) and selects only the 'Open', 'High', 'Low', 'Close', and 'Volume' columns.

    Parameters:
        ticker (str): The ticker symbol of the stock or asset (e.g., "AAPL" for Apple).
        start (str): The start date for the data in the format "YYYY-MM-DD".
        end (str): The end date for the data in the format "YYYY-MM-DD".
        interval (str): The time interval for the data. Default is "1d" (daily).
                       Supported intervals include "1m", "2m", "5m", "15m", "30m", "60m", "1h", 
                       "1d", "5d", "1wk", "1mo", "3mo".

    Returns:
        pd.DataFrame: A processed DataFrame containing the 'Open', 'High', 'Low', 'Close', and 'Volume' columns 
                      with a datetime index.

    Example:
        >>> data = get_ticker_data("AAPL", "2023-01-01", "2023-12-31", interval="1d")
        >>> print(data.head())
                       Open   High    Low  Close  Volume
        2023-01-03  130.26  130.90  124.17  125.07  123450000
        2023-01-04  126.36  126.88  124.48  126.36   90783000

    Notes:
        - Combines `get_yfinance_data`, `set_date_index`, and `flatten_and_select_columns` for streamlined processing.
        - Raises a `KeyError` if any of the required columns ('Open', 'High', 'Low', 'Close', 'Volume') are missing.

    Raises:
        KeyError: If the required OHLCV columns are not present in the retrieved data.
    """
    data = get_yfinance_data(ticker, start, end, interval)
    data = set_date_index(data)
    data = flatten_and_select_columns(data)
    return data
from src.fingpt_agents.agents.data_agent import DataIngestionAgent

def main():
    tickers = ["AAPL", "MSFT", "GOOGL"]  # you can customize tickers here
    agent = DataIngestionAgent(tickers, start="2022-01-01")
    agent.fetch_stock_data()
    agent.save_to_csv()
    
    # Print head of first ticker's dataframe as example
    first_ticker = tickers[0]
    df = agent.dataframes.get(first_ticker)
    if df is not None:
        print(f"Sample data for {first_ticker}:")
        print(df.head())
    else:
        print(f"No data found for {first_ticker}")

if __name__ == "__main__":
    main()

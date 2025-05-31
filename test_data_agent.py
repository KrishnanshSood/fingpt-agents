from src.fingpt_agents.agents.data_agent import DataIngestionAgent

agent = DataIngestionAgent("AAPL", start="2022-01-01")
df = agent.fetch_stock_data()
agent.save_to_csv()
print(df.head())

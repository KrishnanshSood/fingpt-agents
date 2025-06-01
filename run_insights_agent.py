# run_insights_agent.py

from src.fingpt_agents.utils.logger_utils import logger
from src.fingpt_agents.agents.insights_agent import InsightsAgent

def main():
    logger.info("[MAIN] Starting Insights Agent...")
    agent = InsightsAgent()
    agent.load_processed_data()
    summary = agent.generate_summary()

    logger.info("[DONE] Generated Insights:\n")
    for line in summary:
        print(f"  - {line}")

if __name__ == "__main__":
    main()

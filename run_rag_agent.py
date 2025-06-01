from src.fingpt_agents.agents.rag_agent import RAGAgent
from colorama import Fore, Style

def main():
    log(f"{Fore.GREEN}Starting RAG pipeline...{Style.RESET_ALL}")
    rag_agent = RAGAgent()
    pdf_path = "data/filings/APPLE_10K_2022.pdf"
    query = "What are the major risk factors Apple mentions in the 10-K report?"
    answer = rag_agent.run_rag(pdf_path, query)
    print(f"{Fore.GREEN}Answer:\n{Style.RESET_ALL}{answer}")

def log(message: str):
    print(message)

if __name__ == "__main__":
    main()

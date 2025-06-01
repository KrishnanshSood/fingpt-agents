from colorama import Fore, Style
from src.fingpt_agents.utils.logger_utils import logger  # use centralized logger

class MultiAgentController:
    def __init__(self):
        self.agents = {}
        self.context = {}

        logger.info(f"{Fore.CYAN}[INIT]{Style.RESET_ALL} MultiAgentController initialized.")

    def register(self, name: str, agent):
        self.agents[name] = agent
        logger.info(f"{Fore.BLUE}[REGISTER]{Style.RESET_ALL} Agent `{name}` registered successfully.")

    def run_agent(self, name: str):
        if name not in self.agents:
            logger.error(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Agent `{name}` not found!")
            raise ValueError(f"Agent `{name}` not registered.")
        
        logger.info(f"{Fore.GREEN}[EXEC]{Style.RESET_ALL} Executing agent `{name}`...")
        self.context = self.agents[name].run(self.context)
        logger.info(f"{Fore.GREEN}[DONE]{Style.RESET_ALL} Agent `{name}` execution complete.")

    def get_context(self):
        logger.info(f"{Fore.YELLOW}[CONTEXT]{Style.RESET_ALL} Returning final context.")
        return self.context

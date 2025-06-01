# src/fingpt_agents/agents/base_agent.py
from abc import ABC, abstractmethod

class Agent(ABC):
    @abstractmethod
    def run(self, context: dict) -> dict:
        pass

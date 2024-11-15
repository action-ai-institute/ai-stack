from abc import ABC, abstractmethod

def get_agent_agent():
    return LLMAgentAgent()

class AgentAgent(ABC):

    @abstractmethod
    def provide_options(self, warning, options):
        pass

    @abstractmethod
    def retrieve_analyst_choice(self, warning):
        pass

class LLMAgentAgent(AgentAgent):
    
    def __init__(self):
        super().__init__()
        self.resp = -1

    def provide_options(self, warning, options):
        print("Response agent recieved the following warning")
        print(warning)
        print("Planning found the following mitigation options:")
        for i, option in enumerate(options):
            print(f"{i+1}. {option}")

    def retrieve_analyst_choice(self, warning):
        return int(input("Select mitigation option: ")) - 1

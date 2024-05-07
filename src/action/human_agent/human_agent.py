from abc import ABC, abstractmethod

def get_human_agent():
    return SimpleHumanAgent()

class HumanAgent(ABC):

    @abstractmethod
    def provide_options(self, warning, options):
        pass

    @abstractmethod
    def retrieve_analyst_choice(self, warning):
        pass

class SimpleHumanAgent(HumanAgent):

    def provide_options(self, warning, options):
        print("Response agent recieved the following warning")
        print(warning)
        print("Planning found the following mitigation options:")
        for i, option in enumerate(options):
            print(f"{i+1}. {option}")

    def retrieve_analyst_choice(self, warning):
        return int(input("Select mitigation option: ")) - 1

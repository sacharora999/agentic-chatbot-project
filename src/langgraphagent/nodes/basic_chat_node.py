from src.langgraphagent.state.state import State


class BasicChatNode:
    def __init__(self, model):
        self.llm=model

    def process(self,state:State)->dict:
        return {"messages": self.llm.invoke(state["messages"])}    
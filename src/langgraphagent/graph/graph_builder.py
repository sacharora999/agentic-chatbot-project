from langgraph.graph import StateGraph, START, END
from src.langgraphagent.state.state import State
from src.langgraphagent.nodes.basic_chat_node import BasicChatNode

class GraphBuilder:
    def __init__(self, model):
        self.llm=model
        self.graph_builder=StateGraph(State)


    def basic_chatbot_build_graph(self):

        self.basic_chat_node=BasicChatNode(self.llm)

        self.graph_builder.add_node("chatbot", self.basic_chat_node.process)    
        self.graph_builder.add_edge(START, "chatbot")    
        self.graph_builder.add_edge("chatbot", END)   
        
    
    def setup_graph(self, usecase: str):
        if usecase == "Basic Chatbot":
            self.basic_chatbot_build_graph()
        return self.graph_builder.compile()
from langgraph.graph import StateGraph, START, END
from src.langgraphagent.state.state import State
from src.langgraphagent.nodes.basic_chat_node import BasicChatNode
from src.langgraphagent.tools.search_tool import get_tools, create_tool_node
from langgraph.prebuilt import ToolNode, tools_condition
from src.langgraphagent.nodes.chat_with_tool import ChatWithToolNode
from src.langgraphagent.nodes.ai_news_node import AINewsNode

class GraphBuilder:
    def __init__(self, model):
        self.llm=model
        self.graph_builder=StateGraph(State)


    def basic_chatbot_build_graph(self):

        self.basic_chat_node=BasicChatNode(self.llm)

        self.graph_builder.add_node("chatbot", self.basic_chat_node.process)    
        self.graph_builder.add_edge(START, "chatbot")    
        self.graph_builder.add_edge("chatbot", END)   

    def chat_with_tool_build_graph(self):
        tools=get_tools()
        tool_node=create_tool_node(tools)

        llm=self.llm

        obj_chatbot_with_node=ChatWithToolNode(llm)
        chatbot_node=obj_chatbot_with_node.create_chatbot(tools)


        self.graph_builder.add_node("chatbot", chatbot_node)
        self.graph_builder.add_node("tools", tool_node)

        self.graph_builder.add_edge(START, "chatbot")
        self.graph_builder.add_conditional_edges("chatbot", tools_condition)
        self.graph_builder.add_edge("tools", "chatbot")
        self.graph_builder.add_edge("chatbot", END)  

    
    def ai_news_builder_graph(self):

        ai_news_node=AINewsNode(self.llm)

        self.graph_builder.add_node("fetch_news", ai_news_node.fetch_news)
        self.graph_builder.add_node("summarize_news", ai_news_node.summarize_news)
        self.graph_builder.add_node("save_results", ai_news_node.save_result)

        self.graph_builder.set_entry_point("fetch_news")
        self.graph_builder.add_edge("fetch_news", "summarize_news")
        self.graph_builder.add_edge("summarize_news", "save_results")
        self.graph_builder.add_edge("save_results", END)




        
    
    def setup_graph(self, usecase: str):
        if usecase == "Basic Chatbot":
            self.basic_chatbot_build_graph()

        if usecase == "Chatbot with Tool":
            self.chat_with_tool_build_graph()

        if usecase == "AI News Summarizer":
            self.ai_news_builder_graph()
            
        return self.graph_builder.compile()
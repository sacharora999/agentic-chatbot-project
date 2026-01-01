from src.langgraphagent.state.state import State


class ChatWithToolNode:
    def __init__(self, model):
        self.llm=model

    def process(self,state:State)->dict:
        user_input = state["messages"][-1] if state["messages"] else ""
        llm_resp = self.llm.invoke([{"role": "user", "content": user_input}])
        tools_resp = f"Tool integraion for : '{user_input}'"
        return {"messages": [llm_resp, tools_resp]}   


    def create_chatbot(self, tools):
        llm_with_tools=self.llm.bind_tools(tools)
        def chatbot_node(state: State):
            return {"messages": [llm_with_tools.invoke(state["messages"])]}
        return chatbot_node
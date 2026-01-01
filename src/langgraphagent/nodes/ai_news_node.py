from src.langgraphagent.state.state import State
from tavily import TavilyClient
from langchain_core.prompts import ChatPromptTemplate



class AINewsNode:
    def __init__(self, llm):
        self.tavily = TavilyClient()
        self.llm = llm
        self.state = {}
    
    def fetch_news(self, state:dict) -> dict:

        frequency = state["messages"][0].content.lower()
        self.state["frequency"] = frequency
        time_range_map = {"daily": "d", "weekely": "w","monthly": "m","yearly": "y"}
        days_map = {"daily": 1, "weekely": 7, "monthly": 30, "year": 365}

        response = self.tavily.search(
            query="Top Artificial Intelligence News from India and Globally",
            topic="news",
            time_range=time_range_map[frequency],
            include_answer="advanced",
            max_results=15,
            days=days_map[frequency],
            include_domains=["techcrunch.com", "venturebeat.com/ai"]
        )


        state["news_data"] = response.get("result", [])
        self.state["news_data"] = state["news_data"]
        return state
    

    def summarize_news(self, state: dict) -> dict:
        """
        Summarize the fetched news using an LLM.
        
        Args:
            state (dict): The state dictionary containing 'news_data'.
        
        Returns:
            dict: Updated state with 'summary' key containing the summarized news.
        """

        news_items = self.state['news_data']

        prompt_template = ChatPromptTemplate.from_messages([
            ("system", """Summarize AI news articles into markdown format. For each item include:
            - Date in **YYYY-MM-DD** format in IST timezone
            - Concise sentences summary from latest news
            - Sort news by date wise (latest first)
            - Source URL as link
            Use format:
            ### [Date]
            - [Summary](URL)"""),
            ("user", "Articles:\n{articles}")
        ])

        articles_str = "\n\n".join([
            f"Content: {item.get('content', '')}\nURL: {item.get('url', '')}\nDate: {item.get('published_date', '')}"
            for item in news_items
        ])

        response = self.llm.invoke(prompt_template.format(articles=articles_str))
        state['summary'] = response.content
        self.state['summary'] = state['summary']
        return self.state
    
    def save_result(self,state):
        frequency = self.state['frequency']
        summary = self.state['summary']
        filename = f"./AINews/{frequency}_summary.md"
        with open(filename, 'w') as f:
            f.write(f"# {frequency.capitalize()} AI News Summary\n\n")
            f.write(summary)
        self.state['filename'] = filename
        return self.state





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
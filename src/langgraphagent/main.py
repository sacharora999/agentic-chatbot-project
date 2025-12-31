import streamlit as st
from src.langgraphagent.ui.streamlitui.loadui import LoadStreamlitUI
from src.langgraphagent.llms.groqllm import Groqllm
from src.langgraphagent.llms.openaillm import OpenAIllm
from src.langgraphagent.graph.graph_builder import GraphBuilder
from src.langgraphagent.ui.streamlitui.display import DisplayResultStreamlit

def load_langgraph_agentic_app():
    """
    Docstring for load_langgraph_agentic_app
    
    """
    ui=LoadStreamlitUI()
    user_input=ui.load_streamlit_ui()

    if user_input is None:
        return
    user_message = st.chat_input("Enter Your Message : ")

    if user_message:
        try:
            obj_llm_config_groq=Groqllm(user_controls_input=user_input)
            obj_llm_config_openai=OpenAIllm(user_controls_input=user_input)

            if user_input["selected_llm"] == "OpenAI":
                obj_llm_config=obj_llm_config_openai
            else:
                obj_llm_config=obj_llm_config_groq
            model=obj_llm_config.get_llm_models()
            if not model:
                st.error("Model could not be initialized")
                return
            
            usecase=user_input.get("selected_usecase")
            if not usecase:
                st.error("usecase could not be initialized")
                return
            
            graph_builder=GraphBuilder(model)
            try:
                graph=graph_builder.setup_graph(usecase)
                DisplayResultStreamlit(usecase, graph, user_message).display_result_on_ui()
            except Exception as e:
                st.error(f"Error Graph Setup failed : {e}")
                return
        except Exception as e:
            st.error(f"Error Loading main class : {e}")
            return
            




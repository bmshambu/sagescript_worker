import os
import json
from langchain_openai import AzureChatOpenAI
from langgraph.graph import MessagesState
from langgraph.graph import START, StateGraph
from langgraph.checkpoint.memory import MemorySaver
from config import AppConfig
from langchain_core.messages import HumanMessage, SystemMessage
#from Azure_openai_handler import initialize_azure_llm
from utils.google_llm_handler import initialize_llm
from constants.output_format import JSON_FORMAT
from constants.system_prompt import prompt
from langgraph.prebuilt import tools_condition, ToolNode
#from graph_initialize_functional_test import FunctionalTestCaseGraph
from utils.unit_test.graph_initialize_unit_test import UnitTestCaseGraph
import random


# Function to execute the workflow
def run_unit_test_case_generation(user_input,api_key,model_name):
    # Specify a thread
    # Initialize graph
    unit_test_case_graph = UnitTestCaseGraph(api_key, model_name)
    graph = unit_test_case_graph.get_graph()
    thread_id = random.randint(1, 1000000)
    print(f'thread_id: {thread_id}')
    config = {"configurable": {"thread_id": thread_id}}
    messages = [HumanMessage(content=user_input)]
    response = graph.invoke({"messages": messages},config)
    for m in response['messages']:
        m.pretty_print()
    return response['messages'][-1].content
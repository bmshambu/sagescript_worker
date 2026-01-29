import os
import json
import random
from langchain_openai import AzureChatOpenAI
from langgraph.graph import MessagesState
from langgraph.graph import START, StateGraph
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.prebuilt import tools_condition, ToolNode

from config import AppConfig
from utils.google_llm_handler import initialize_llm
from utils.functional_test.graph_initialize_functional_test import FunctionalTestCaseGraph
from utils.functional_test.functional_test_rag_pipeline import FunctionalTestCaseRAG

# New imports
from constants.output_format import JSON_FORMAT
from constants.system_prompt import prompt
from constants.examples import examples
from constants.framework_prompts import framework_prompts

retriever = FunctionalTestCaseRAG().retriever


# Function to execute the workflow
def run_functional_test_case_generation(
    user_story,
    acceptance_criteria,
    api_key,
    model_name,
    framework_choice="java_selenium"   # <-- NEW
):
    # Initialize graph
    functional_test_case_graph = FunctionalTestCaseGraph(api_key, model_name, framework_choice)
    graph = functional_test_case_graph.get_graph()

    # Generate random thread id
    thread_id = random.randint(1, 1000000)
    print(f'thread_id: {thread_id}')
    config = {"configurable": {"thread_id": thread_id}}

    # Retrieve metadata
    user_input = f"user story: {user_story}, acceptance criteria: {acceptance_criteria}"
    retrieved_docs = retriever.invoke(user_input, k=10)
    relevant_metadata = "\n\n".join(doc.page_content for doc in retrieved_docs)

    # Prepare messages
    messages = [
        HumanMessage(
            content=f"user story: {user_story}, acceptance criteria: {acceptance_criteria}, relevant metadata: {relevant_metadata}"
        )
    ]

    # Run graph
    response = graph.invoke({"messages": messages}, config)

    return response['messages'][-1].content


# if __name__ == "__main__":
#     run_test_case_generation(user_story, acceptance_criteria,thread_id='1')
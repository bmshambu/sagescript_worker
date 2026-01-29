import json
from langchain_openai import AzureChatOpenAI
from langgraph.graph import MessagesState
from langgraph.graph import START, StateGraph
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.prebuilt import tools_condition, ToolNode

from utils.google_llm_handler import initialize_llm
from constants.system_prompt import prompt
from constants.output_format import JSON_FORMAT
from constants.examples import examples
from constants.framework_prompts import framework_prompts


class FunctionalTestCaseGraph:
    def __init__(self, api_key: str, model_name: str, framework_choice: str = "java_selenium"):
        self.api_key = api_key
        self.model_name = model_name
        self.framework_choice = framework_choice
        self.llm = self.initialize_llm()
        self.graph = self.build_graph(framework_choice)

    def initialize_llm(self):
        return initialize_llm(self.api_key, self.model_name)

    def build_graph(self, framework_choice: str):
        # Get framework-specific instructions
        framework_instruction = framework_prompts.get(framework_choice, framework_prompts["java_selenium"])

        # Inject into prompt
        formatted_prompt = prompt.format(
            JSON_FORMAT=JSON_FORMAT,
            examples=json.dumps(examples, indent=2),
            FRAMEWORK_INSTRUCTION=framework_instruction
        )

        sys_msg = SystemMessage(content=formatted_prompt)

        # Bind tools (future extensibility)
        tools = []
        llm_with_tools = self.llm.bind_tools(tools)

        # Assistant node
        def assistant(state: MessagesState):
            return {"messages": [llm_with_tools.invoke([sys_msg] + state["messages"])]}

        # Build graph
        memory = MemorySaver()
        builder = StateGraph(MessagesState)

        builder.add_node("assistant", assistant)
        builder.add_node("tools", ToolNode(tools))

        builder.add_edge(START, "assistant")
        builder.add_conditional_edges("assistant", tools_condition)
        builder.add_edge("tools", "assistant")

        return builder.compile(checkpointer=memory)

    def get_graph(self):
        return self.graph

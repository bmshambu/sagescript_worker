from langchain_openai import AzureChatOpenAI
from langgraph.graph import MessagesState
from langgraph.graph import START, StateGraph
from langgraph.checkpoint.memory import MemorySaver # Adjust if loading from a file
from utils.google_llm_handler import initialize_llm
from constants.output_format import JSON_FORMAT
from constants.system_prompt_unit_test_case import prompt
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.prebuilt import tools_condition, ToolNode

class UnitTestCaseGraph:
    def __init__(self, api_key: str, model_name: str):
        self.api_key = api_key
        self.model_name = model_name
        self.llm = self.initialize_llm()
        self.graph = self.build_graph()

    def initialize_llm(self):
        # You must implement or import this based on your LLM provider
        from utils.google_llm_handler import initialize_llm  # Make sure this exists
        return initialize_llm(self.api_key, self.model_name)

    def build_graph(self):
        # Format the prompt
        #formatted_prompt = prompt.format(JSON_FORMAT=JSON_FORMAT)
        sys_msg = SystemMessage(content=prompt)

        # Bind tools
        tools = []
        llm_with_tools = self.llm.bind_tools(tools)

        # Define assistant node
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

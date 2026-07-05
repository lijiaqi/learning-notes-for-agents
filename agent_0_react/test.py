from langgraph.graph import StateGraph, START, END
from typing import TypedDict

class WorkflowState(TypedDict, total=False):
    data: str
    result: str

def fetch_data(state):
    return {
        "data": "sales_data"
    }

def analyze_data(state):
    return {
        "result": "sales_analysis"
    }

def save_data(state):
    print("Saved:", state["result"])
    return {}

workflow = StateGraph(WorkflowState)

workflow.add_node("fetch_data", fetch_data)
workflow.add_node("analyze_data", analyze_data)
workflow.add_node("save_data", save_data)

workflow.add_edge(START, "fetch_data")
workflow.add_edge("fetch_data", "analyze_data")
workflow.add_edge("analyze_data", "save_data")
workflow.add_edge("save_data", END)

app = workflow.compile()
app.invoke({})
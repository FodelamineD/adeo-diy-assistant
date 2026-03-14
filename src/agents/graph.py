from typing import Annotated, TypedDict, Union
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI
from src.tools.stock import check_stock_and_price
from src.tools.search import search_technical_guide
from langgraph.prebuilt import ToolNode, tools_condition

# 1. Définition de l'état (mémoire de travail de l'agent)
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]

# 2. Configuration des outils et du modèle
tools = [check_stock_and_price, search_technical_guide]
model = ChatOpenAI(model="gpt-4o", temperature=0).bind_tools(tools)

# 3. Nœud de décision (Le Cerveau)
def call_model(state: AgentState):
    response = model.invoke(state["messages"])
    return {"messages": [response]}

# 4. Construction du Graphe
workflow = StateGraph(AgentState)

# Ajout des nœuds
workflow.add_node("agent", call_model)
workflow.add_node("tools", ToolNode(tools))

# Définition des liens (Edges)
workflow.set_entry_point("agent")

# Condition : Si le modèle génère un tool_call -> nœud tools, sinon -> FIN
workflow.add_conditional_edges(
    "agent",
    tools_condition,
    {
        "tools": "tools",
        "__end__": END,
    }
)

# Après les outils, on revient toujours à l'agent pour synthétiser
workflow.add_edge("tools", "agent")

# Compilation
graph = workflow.compile()
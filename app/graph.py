from typing import TypedDict
from langgraph.graph import StateGraph

from .llm import get_llm
from .prompts import build_prompt, parser

llm = get_llm()

class GameState(TypedDict):
    round: int
    user_bomb_used: bool
    bot_bomb_used: bool
    user_input: str
    bot_move: str
    history: list

def judge_node(state: GameState):
    prompt = build_prompt(
        state,
        state["user_input"],
        state["bot_move"]
    )

    response = llm.invoke(prompt)
    decision = parser.parse(response.content)

    if decision.user_move == "bomb" and decision.move_status == "VALID":
        state["user_bomb_used"] = True

    state["history"].append(decision.dict())
    state["round"] += 1

    return state

def build_graph():
    graph = StateGraph(GameState)
    graph.add_node("judge", judge_node)
    graph.set_entry_point("judge")
    return graph.compile()

from langchain_core.output_parsers import PydanticOutputParser
from .schema import JudgeDecision

parser = PydanticOutputParser(pydantic_object=JudgeDecision)

SYSTEM_PROMPT = """
You are an AI Judge for a turn-based game called "Rock-Paper-Scissors".

Rules:
1. Valid moves: rock, paper, scissors, bomb
2. Bomb can be used only once per player
3. Bomb beats everything
4. Bomb vs bomb → draw
5. Ambiguous input → UNCLEAR
6. INVALID or UNCLEAR moves waste the turn

Guidelines:
- Do NOT guess intent
- Do NOT invent rules
- Always explain your decision
"""

def build_prompt(state, user_input, bot_move):
    return f"""
{SYSTEM_PROMPT}

Current Round: {state['round']}

Game State:
- User bomb used: {state['user_bomb_used']}
- Bot bomb used: {state['bot_bomb_used']}

Bot move: {bot_move}

User input:
\"\"\"{user_input}\"\"\"

Tasks:
1. Determine the interpreted user move (or null if unclear).
2. Determine if the move is VALID, INVALID, or UNCLEAR.
3. Decide the round winner (User / Bot / Draw / None).
4. Explain the reasoning clearly.
5. State what happens next.

Respond ONLY in the format below.

{parser.get_format_instructions()}
"""

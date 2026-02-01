from typing import Optional, Literal
from pydantic import BaseModel

class JudgeDecision(BaseModel):
    round: int
    user_move: Optional[Literal["rock", "paper", "scissors", "bomb"]]
    bot_move: Literal["rock", "paper", "scissors", "bomb"]
    move_status: Literal["VALID", "INVALID", "UNCLEAR"]
    winner: Optional[Literal["User", "Bot", "Draw"]]
    explanation: str

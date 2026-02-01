from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import random

from app.graph import build_graph
from app.state import initial_state

app = FastAPI()
graph = build_graph()
state = initial_state()

VALID_MOVES = ["rock", "paper", "scissors", "bomb"]

class Move(BaseModel):
    text: str

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
      <body>
        <h3>Rock Paper Scissors Judge</h3>
        <input id="move" placeholder="Enter your move"/>
        <button onclick="send()">Submit</button>
        <pre id="out"></pre>

        <script>
          async function send() {
            const res = await fetch("/move", {
              method: "POST",
              headers: {"Content-Type": "application/json"},
              body: JSON.stringify({text: document.getElementById("move").value})
            });
            document.getElementById("out").innerText =
              JSON.stringify(await res.json(), null, 2);
          }
        </script>
      </body>
    </html>
    """

@app.post("/move")
def play(move: Move):
    global state
    state["user_input"] = move.text
    state["bot_move"] = random.choice(VALID_MOVES)

    state = graph.invoke(state)
    return state["history"][-1]

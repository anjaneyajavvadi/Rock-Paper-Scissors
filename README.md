Rock–Paper–Scissors AI Judge

This project is a prompt-driven AI Judge for a simple game variant: Rock–Paper–Scissors Plus, where an additional move (bomb) exists with strict constraints.

The goal of this project is not to build a game engine.
The goal is to demonstrate how a Large Language Model can be used as a rule-following judge that:

understands free-text user input

applies given rules correctly

handles ambiguity and edge cases

explains why a decision was made

returns structured, machine-verifiable output

🧠 What this judge actually does

For every round:

The user enters a move in natural language

The bot secretly chooses a move

The AI Judge:

interprets the user’s intent (or rejects it)

checks validity against the rules

decides the winner (if any)

explains the reasoning clearly

The system stores minimal state (round number, bomb usage)

All decisions are made by the LLM via prompting, not hard-coded logic.

📌 Game rules (given to the AI, not coded)

Valid moves: rock, paper, scissors, bomb

bomb can be used only once per player in the entire game

bomb beats everything

bomb vs bomb → draw

Ambiguous or unclear input → UNCLEAR

INVALID or UNCLEAR moves waste the turn

The Python code does not re-implement these rules.
The model is instructed to follow them.

🏗️ Architecture (kept intentionally simple)
FastAPI (UI + API)
        |
        v
LangGraph
        |
        v
LLM Judge (Gemini)
        |
        v
Pydantic Output Parser

Why this structure?

Prompts handle reasoning

LangGraph handles orchestration

Pydantic enforces output correctness

Code only manages state and routing

This keeps responsibilities clean and debuggable.

📂 Project structure
ai_judge/
│
├── app/
│   ├── llm.py        # Gemini model setup
│   ├── schema.py     # Pydantic output contract
│   ├── prompts.py   # System + instruction prompts
│   ├── graph.py     # LangGraph judge agent
│   └── state.py     # Initial game state
│
├── api.py            # FastAPI app + minimal UI
├── requirements.txt
└── README.md


No databases.
No external APIs.
No unnecessary abstractions.

🧾 Why PydanticOutputParser is used

LLMs are not guaranteed to output clean JSON.

PydanticOutputParser is used to:

enforce a strict output schema

prevent silent failures

fail fast when the model misbehaves

make the agent safer and predictable

If parsing fails, the system intentionally errors instead of guessing.

⚠️ Edge cases handled intentionally

Some examples the agent handles correctly:

"I smash you with a stone" → UNCLEAR

"bomb again" after bomb was already used → INVALID

Empty input → UNCLEAR

Emojis / garbage text → UNCLEAR

The agent does not guess intent.
If it’s not clear, the turn is wasted — by design.

🚀 Running the project

Install dependencies

pip install -r requirements.txt


Set your Gemini API key

export GOOGLE_API_KEY=your_key_here


Start the server

uvicorn api:app --reload


Open in browser

http://127.0.0.1:8000

🔮 What could be improved next

If this were extended further:

Clarification follow-ups for UNCLEAR moves

Multi-round win tracking

Bot bomb usage tracking

Confidence scores for intent interpretation

Stateless / session-based gameplay

These were intentionally left out to keep the focus on prompt quality and agent behavior.

🧠 Final note

This project treats the LLM as a reasoning component, not a toy.

The rules live in the prompt.
The decisions are explained.
The output is enforced.

That’s the point of this agent.
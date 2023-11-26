# ampode
Agents Made to Plan, Orchestrate, Discuss, and Execute

### Introduction
AMPODE is a software module designed to allow a system of agents autonomously plan, orchestrate, and execute a dynamic series of tasks to reach an end goal provided by the user.  AMPODE hopes to harness language models' existing ability to parrot human processes in problem-solving and strategic planning in a lightweight framework that couples together a state machine and a purpose-made system of agents into a self-evolving decision-making mechanism.

What will hopefully make AMPODE function is good alignment between
- group chat orchestration
- dynamic prompting
- the model's reliability in responding with 
  - proper intent 
  - proper function calling

Hopefully a framework like this could
- expand to give access and awareness to agents to
  - local data access
  - web access
  - code execution environment
- expand to store goal/response related artifacts that can be used as input and output or dependencies between states and evolved as the states progress
- naturally perform task decomposition
- be allowed to explore a non-linear flow through states (non-linear problem solving)

### Components
StateMachine.py
- Basic State Machine (probably an unnecessary abstraction)
AgentDrivenStateMachine.py
- Handles instantiating AI Agents and CRUD that AI Agents can access 
- Dynamically generates system_message's based on the current state and role
  - with dynamically generated function calling headers
GroupPlanning.py
- Takes a user request, llm_config.json, and initial_state.json
- Builds an AgentDrivenStateMachine, and couples it to an autogen groupchat based on values in the current state

### Dependencies
- Local text generation api or an OpenAI API Key
- ```pip install -r requirements.txt```

### Usage
```python src/GroupPlanning.py initial_state.json llm_config.json```


### Disclaimer 
The author of this repo and any contributors bear no responsibility for it's use or misuse see DISCLAIMER.md
# ampode
Agents Made to Plan, Orchestrate, Discuss, and Execute

### Introduction
<<<<<<< HEAD
<<<<<<< HEAD
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
=======
AMPODE is a software module designed to allow a system of agents autonomously plan, orchestrate, and execute a dynamic series of tasks to reach an end goal provided by the user.  AMPODE hopes to harness language models existing ability to parrot human processes in problem-solving and strategic planning in a lightweight framework that couples together a state machine and a purpose-made system of agents into a self-evolving decision-making mechanism.
=======
AMPODE is a software module designed to allow a system of agents autonomously plan, orchestrate, and execute a dynamic series of tasks to reach an end goal provided by the user.  AMPODE hopes to harness language models' existing ability to parrot human processes in problem-solving and strategic planning in a lightweight framework that couples together a state machine and a purpose-made system of agents into a self-evolving decision-making mechanism.
>>>>>>> 29ce91c (Fix typoes)

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
<<<<<<< HEAD
- explore a non-linear flow through states
>>>>>>> 6319113 (Initial README.md)
=======
- be allowed to explore a non-linear flow through states (non-linear problem solving)
>>>>>>> 29ce91c (Fix typoes)

### Components
StateMachine.py
- Basic State Machine (probably an unnecessary abstraction)
AgentDrivenStateMachine.py
- Handles instantiating AI Agents and CRUD that AI Agents can access 
- Dynamically generates system_message's based on the current state and role
  - with dynamically generated function calling headers
GroupPlanning.py
<<<<<<< HEAD
<<<<<<< HEAD
- Takes a user request, llm_config.json, and initial_state.json
=======
- Takes a user request, llm_config.json, and intial_state.json
>>>>>>> 6319113 (Initial README.md)
=======
- Takes a user request, llm_config.json, and initial_state.json
>>>>>>> 29ce91c (Fix typoes)
- Builds an AgentDrivenStateMachine, and couples it to an autogen groupchat based on values in the current state

### Dependencies
- Local text generation api or an OpenAI API Key
- ```pip install -r requirements.txt```

### Usage
```python src/GroupPlanning.py initial_state.json llm_config.json```


### Disclaimer 
<<<<<<< HEAD
The author of this repo and any contributors bear no responsibility for it's use or misuse see DISCLAIMER.md
=======
The author of this repo and any contributors bear no responsibility for it's use or misuse see DISCLAIMER.md
>>>>>>> 29ce91c (Fix typoes)

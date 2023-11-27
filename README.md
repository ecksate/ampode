# AMPODE
**Agents Made to Plan, Orchestrate, Discuss, and Execute**

### Introduction

AMPODE is a software module designed to allow a system of agents to autonomously plan, orchestrate, and execute a dynamic series of tasks to reach an end goal provided by the user.  AMPODE hopes to harness language models' existing ability to parrot human  problem-solving and strategic planning in a lightweight framework that couples together a state machine and a purpose-made system of agents into a self-evolving decision-making mechanism.

What will hopefully make AMPODE function well is good alignment between the data structure, the prompt, and the language model.

Hopefully a framework similar to this could
- naturally perform task decomposition
- explore a non-linear flow through states (non-linear problem solving)
- store artifacts (task output) that evolve as the plan progresses
- interact with it's environment such as
  - a data store
  - code execution environment
  - the web / apis

## Components

### `StateMachine.py`
- Basic State Machine (probably an unnecessary abstraction)

### `AgentDrivenStateMachine.py`
- Handles instantiating AI Agents and CRUD functionality that AI Agents can access 
- Dynamically generates system_message's based on the current state and role
  - with dynamically generated function calling headers

### `GroupPlanning.py`
- Takes a user request, llm_config.json, and initial_state.json
- Builds an AgentDrivenStateMachine, and couples it to an autogen groupchat based on values in the current state

## Dependencies

- Local text generation api or an OpenAI API Key
- ```pip install -r requirements.txt```

## Usage

```python src/GroupPlanning.py initial_state.json llm_config.json```

## How it operates

See initial_state.json for some idea
and observe these responses from preliminary testing
- https://rentry.co/z8edam
- https://rentry.co/qanc7y


### Disclaimer 
The author of this repo and any contributors bear no responsibility for it's use or misuse see DISCLAIMER.md

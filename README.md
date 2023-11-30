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

### Components
Task.py
- It's a recursive tree of Goals, Participants, and Instructions. 
- It can generate a system message and a set of instructions for each participant based on the state (current_task)
- It automatically generate function headers from itself that go into the system message
- It handles the extremely annoying job of updating any task in the hierarchy

## Dependencies

- Local text generation api or an OpenAI API Key
- ```pip install -r requirements.txt```


### Usage
Test it out with TestTask.  Look in the main function, you can either interact with the module in a chat as just a user like you are the agent or you can test the functions for updating state.  Both of these are extremely boring and the actual point is to create a module that inherits Task and incoorporates whatever language model related software you might be running your agents in.

```python src/Task.py```

### Some example responses
See initial_state.json for some idea
and observe these responses from preliminary testing
- https://rentry.co/z8edam
- https://rentry.co/qanc7y


# History


v0.0.1:
  Yeeted the idea out there, it was three files, :ok:


v0.0.2:
  It's now a single abstract class for you to inherit and implement your own agent of choice.  At this point I realized my project is essentially the tape in a Turing machine and that it was a very small conceptual leap from this to a Markov chain tree generator which might also be useful for automatically generating options for Q-learning maybe idk


### Disclaimer 
The author of this repo and any contributors bear no responsibility for it's use or misuse see DISCLAIMER.md

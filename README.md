# AMPODE
**Agents Made to Plan, Orchestrate, Discuss, and Execute**

Finally found the place where this concept was basically fully implemented
https://github.com/microsoft/semantic-kernel/blob/main/python/semantic_kernel/planning/plan.py

### Introduction

The concept is an n-tree of Task nodes, each with the values (and methods) required to prompt a group chat of various roles to complete an action or produce an artifact and then update it's own Task hierarchy using function calling.  This structure is meant to allow your agents to create their own plan and follow it, with the initial state of the module being an instruction to form a plan by updating the data structure in pursuit of the user's goal, and the operation continues with the first task created in the plan.

How this would be best implemented into an agent or system of agents is an area ripe for exploration, therefore it is provided as an abstract class for you to inherit and add logic to.  The Task module is able to generate function call headers for the system message dynamically, making it easy to extend.  The update_task method handles arbitrary  properties (probably only works for simple values like int and str, etc, but not list or dicts, etc.)

If the minimal concept works, and agents are able to create plans and guide themselves through it with this simple tree of Turing tape, there are many possibilities for extending its usage including memory, web access, code execution, self-guided polymorphism through reflection, etc.

This structure has the following benefits:
 - allows task decomposition anywhere in the structure
 - allows non-linear plans
 - allows parallel execution
 - highly scalable structure
 - decouples the size of your plan from the size of the context window
 - opportunity to step through the graph to collect additional context from nearby Tasks as space permits
 - flexible: bring your own agent, bring your own logic

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

```python Task.py```

### Some example responses
Here are some responses from preliminary testing (different code/prompt), where I wanted to confirm that sometimes the agent could update it's own plan
- https://rentry.co/z8edam
- https://rentry.co/qanc7y


# History

v0.0.1:
  Yeeted the idea out there, it was three files, :ok:

v0.0.2:
  It's now a single abstract class for you to inherit and implement your own agent of choice.  At this point I realized my project is essentially the tape in a Turing machine and that it was a very small conceptual leap from this to a Markov chain tree generator which might also be useful for automatically generating options for Q-learning maybe idk


### Disclaimer 
The author of this repo and any contributors bear no responsibility for it's use or misuse see DISCLAIMER.md

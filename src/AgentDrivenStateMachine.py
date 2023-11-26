from StateMachine import StateMachine
from autogen import AssistantAgent


class AgentDrivenStateMachine:
    """
    A class representing a state machine for managing the states and transitions in a workflow, 
    with functionalities tailored for agent-driven interactions.
    """

    def __init__(self, initial_state=None, llm_config=None):
        """
        Initializes the AgentDrivenStateMachine with an instance of StateMachine.
        """
        self.state_machine = StateMachine(initial_state)
        self.llm_config = llm_config

    def get_state_machine(self):
        """
        Gets the underlying StateMachine instance.

        Returns:
            StateMachine: The underlying StateMachine instance.
        """
        return self.state_machine

    def get_current_state(self):
        """
        Finds the current state with incomplete goals.

        Returns:
            str: The name of the current state.
        """
        return self.state_machine.get_current_state()
    
    def get_current_state_details(self):
        """
        Finds the details for the current state.

        Returns:
            dict: The details for the current state.
        """
        return self.state_machine.retrieve_state(self.state_machine.get_current_state())

    def _create_agent(self, role: str) -> AssistantAgent:
        """
        Creates an agent for the given role with a Nexus Raven-compatible system message.

        Args:
            role (str): The role of the agent.

        Returns:
            AssistantAgent: The created agent with the specified role.
        """
        current_state = self.state_machine.get_current_state()
        state_details = self.state_machine.retrieve_state(current_state)
        system_message = self.get_system_message(role)

        # Create and return the AssistantAgent
        return AssistantAgent(
            name=role,
            llm_config=self.llm_config,
            system_message=system_message
        )

    def update_roles(self, state_name, new_roles):
        """
        Updates the roles for a given state, giving agents control over their operating plan.

        Args:
            state_name (str): The name of the state.
            new_roles (list of str): A list of new roles for the state.
        """
        state = self.state_machine.retrieve_state(state_name)
        state['roles'] = new_roles
        self.state_machine.update_state(state_name, state)

    def update_instructions(self, state_name, instructions, role=None):
        """
        Updates instructions for a given state. If a role is specified, updates individual instructions; 
        otherwise, updates group instructions.
        Gives agents control over the instructions for the a specific state and role's operating plan.

        Args:
            state_name (str): The name of the state.
            instructions (str): The updated instructions.
            role (str, optional): The specific role for which to update the instructions. 
                                  If None, updates the group instructions.
        """
        state = self.state_machine.retrieve_state(state_name)
        if role:
            state['individual_instructions'][role] = instructions
        else:
            state['group_instructions'] = instructions
        self.state_machine.update_state(state_name, state)

    def update_goal(self, state_name, goal):
        """
        Updates the goal for a given state, giving agents control over their operating plan.

        Args:
            state_name (str): The name of the state.
            goal (str): The updated goal for the state.
        """
        state = self.state_machine.retrieve_state(state_name)
        state['goal'] = goal
        self.state_machine.update_state(state_name, state)

    def update_transitions(self, state_name, transitions):
        """
        Updates the transitions for a given state, giving agents control over their operating plan.

        Args:
            state_name (str): The name of the state.
            transitions (dict): A dictionary of updated transitions for the state.
        """
        state = self.state_machine.retrieve_state(state_name)
        state['transitions'] = transitions
        self.state_machine.update_state(state_name, state)

    def execute_function(self, function_name, *args, **kwargs):
        """
        Executes a function by its name with provided arguments to modify the AgentDrivenStateMachine.

        Args:
            function_name (str): The name of the function to execute.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        # Lookup the function by name and execute it
        # This is a placeholder for the actual function call logic
        function = getattr(self, function_name, None)
        if callable(function):
            function(*args, **kwargs)
        else:
            raise ValueError(f"Function {function_name} is not callable or does not exist.")

    def get_system_message(self, role):
        """
        Constructs a Nexus Raven-compatible system messagefor an agent based on its role, combining group and individual instructions.
        This message includes all the functions of the state machine that the agent can call.
        Args:
            role (str): The role of the agent.

        Returns:
            str: The system message for the agent.
        """
        
        current_state = self.get_current_state()
        state_info = self.state_machine.retrieve_state(current_state)
        group_instructions = """
Example State:
{
  "name": "Initial_Assessment",
  "roles": ["Task_Analyzer", "Workflow_Planner"],
  "group_instructions": "Review the user request and collaboratively develop an initial plan.  Use the functions available in OPTIONS to update the workflow on which you are operating to plan tasks for successive phases.",
  "individual_instructions": {
      "Task_Analyzer": "Analyze the user's request, identify key objectives and potential challenges.",
      "Workflow_Planner": "Based on the analysis, propose an initial set of states and actions required to accomplish the objectives."
  },
  "goal": "To understand the user's request and create a preliminary plan for the workflow.",
  "completed": false,
  "transitions": {
      "Plan_Developed": "Plan_Development",
      "Need_More_Info": "Information_Gathering"
  }
}
You are directed to assert full control over your workflow by calling the functions provided. Your primary task is to populate the task state machine, outlining a detailed plan to address the user request. For each inquiry, you must:

Execute your plan by completing the goal and transitioning to the next step.
Each task required to complete the user's request is represented as a state in the state machine. Each state has a goal and transitions.

Instructions for this phase:
"""+state_info['group_instructions']
        if role == "Manager":
          individual_instructions = """
"""
          system_message = f"""Group Goal: 
{group_instructions}
Your role to play:
{individual_instructions}"""
        else: 
          individual_instructions = state_info['individual_instructions'].get(role, '')
          system_message = f"""Group Goal: 
{group_instructions}
Your role to play:
{individual_instructions}"""
        functions_list = [func for func in dir(self) if callable(getattr(self, func)) and not func.startswith("_") and not func.startswith("get") and not func.startswith("execute")]
        # get arguments for each function
        arguments_dict = {}
        for function_name in functions_list:
            arguments_dict[function_name] = []
            function = getattr(self, function_name, None)
            if callable(function):
                #arguments_dict[function_name] = function.__code__.co_varnames[1:function.__code__.co_argcount]
                arguments_dict[function_name] = (function.__code__.co_varnames[1:function.__code__.co_argcount],function.__doc__)
        
        nexus_raven_template = "Functions available for AI to execute:\n"
        for function_name, (arguments, doc) in arguments_dict.items():
            all_args = ["self"] + [f"{arg}=None" for arg in arguments]
            args_str = ", ".join(all_args)
            #nexus_raven_template += f"OPTION:\n"
            nexus_raven_template += f"# {function_name}\n"
            nexus_raven_template += f"def {function_name}({args_str}):\n"
            nexus_raven_template += "\n"
            nexus_raven_template += f"{trim_quotes_and_spaces(doc)}\n"
            nexus_raven_template += "\n\n"
        nexus_raven_system_message = nexus_raven_template + "\n" + system_message + "\n" + """
Manipulate the workflow (aka your plan) to fulfill the user's request:
```
function_name(arg1=value1, arg2=value2);
```"""
        print (nexus_raven_system_message)
        return nexus_raven_system_message

    def add_task_to_plan(self, state_name, state):
        """
        Adds a new state to the state machine with its associated details and transitions.
        """
        self.state_machine.add_state(state_name, state)

    def set_task_completed(self, state_name, completed=True):
        """
        Sets a state's completion status.

        Args:
            state_name (str): The name of the state.
            completed (bool): The completion status to set for the state.
        """
        if state_name in self.states:
            self.states[state_name]['completed'] = completed
        else:
            raise KeyError(f"State {state_name} does not exist.")

    def get_agents_for_current_state(self):
        """
        Gets the agents for the current state.

        Returns:
            list of AssistantAgent: The agents for the current state.
        """
        current_state = self.state_machine.get_current_state()
        state_info = self.state_machine.states[current_state]
        return [self._create_agent(role) for role in state_info['roles']]
    
    def search_the_web(self, query):
        """
        Searches the web for the given query.

        Args:
            query (str): The query to search the web for.
        """
        print(f"Searching the web for {query}...")
    
  #function to trim all quotes then trim all spaces
def trim_quotes_and_spaces(string):
  return string.replace('"', '').strip()
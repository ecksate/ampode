# Task.py
from typing import List, Dict, Optional, get_type_hints
import inspect
import Task
from abc import ABC, abstractmethod

agent_callable_functions = [
    'update_task'
]


class Task(ABC):
    def __init__(self, name: str, goal: str, participants: Dict[str, str], sub_tasks: Optional[List['Task']] = None, current_sub_task: Optional[str] = None) -> None:
        """
        Initializes a new Task object.

        Args:
            name (str): The name of the task.
            goal (str): The goal or objective of the task.
            participants (Dict[str, str]): A dictionary mapping role names to their instructions.
            sub_tasks (Optional[List[Task]]): An optional list of sub-tasks, for when this task needs to be broken down into smaller tasks.
            current_sub_task (Optional[str]): An optional current sub-task. Deprecated, in favor of making the current sub-task the first sub-task in the list of sub-tasks.
        """
        self.name = name
        self.goal = goal
        self.participants = participants
        self.sub_tasks = sub_tasks if sub_tasks else []
        self.current_sub_task = None if not sub_tasks else sub_tasks[0].name
        self.completed = False

    def _update_task(self, name: Optional[str] = None, goal: Optional[str] = None, participants: Optional[Dict[str, str]] = None, tasks:Optional[List['Task']] = None ) -> None:
        """
        This function updates this task and all tasks beneath it.  
        It might not be necessary to update all tasks beneath it
         because this method will probably only be called by on leaf nodes
         but just in case the agent tries it.

        The other function, update_task, is the one that should be called
         because it supports traversing the tree to and updating a single Task
         anywhere in the tree using a string path.

        Since the other function's docstring is automatically going into the
          system message of the agents, I put the full explanation here.           

        Args:
            name (Optional[str]): The new name of the task.
            goal (Optional[str]): The new goal of the task.
			      tasks (Optional[List[Task]]): The new sub-tasks.
            participants (Optional[Dict[str, str]]): New participating roles.
        """
        if name is not None:
            self.name = name
        if goal is not None:
            self.goal = goal
        if participants is not None:
            self.participants = participants
        if tasks:
          for t in tasks:
              if t not in self.sub_tasks:
                  self.sub_tasks.append(t)
              else:
                  self.sub_tasks[self.sub_tasks.index(t)].update_task(**t.__dict__)


    # This function is hot off the press and very lightly tested
    def update_task(self, task_updates: dict) -> None:
        """
        Update a named task in the Task hierarchy.

        Args:
            task_updates (dict): Dictionary with keys as field names to update and values as new values.
        """
        for key, val in task_updates.items():
            if key == "" or val == "" or key is None or val is None:
                print("Skipping update with empty key or value: ", key, val)
                continue
            elif not isinstance(key, str):
                raise TypeError(f"Key '{key}' must be a string.")
            
            # Strip leading dot if present
            key = key.lstrip('.')

            attrs = key.split(".")
            task = self
            print(f'Attempting to update {task.name}.{key} to {val}')

            # Navigate through the attributes, moving into sub-tasks if necessary
            for i, attr in enumerate(attrs):
                try:
                    print(f'Checking if {attr} is an attribute of {task.name}')
                    # Check if we are at the last attribute to update
                    if i == len(attrs) - 1:
                        if hasattr(task, attr):
                            print(f'Updating attribute: {task.name}.{attr} to {val}')
                            setattr(task, attr, val)
                        else:
                            # check if val is a code that evaluates to a Task
                            print(f'Checking if {val} evaluates to a Task')
                            first_word = val.split("(")[0]
                            if first_word == type(self).__name__:
                                # eval the code to get the Task
                                task = eval(val)
                                # add the task to the sub_tasks
                                task.sub_tasks.append(task)
                            else:
                              raise ValueError(f"'{attr}' is not an attribute of {task.name}.")
                    else:
                        # Navigate to the next sub-task
                        if attr == 'sub_tasks':
                            continue
                        else:
                            found = False
                            for sub_task in task.sub_tasks:
                                if sub_task.name == attr:
                                    task = sub_task
                                    found = True
                                    break
                            if not found:
                                raise ValueError(f"'{attr}' is not a valid Task name under {task.name}.")
                except AttributeError:
                    raise ValueError(f"'{key}' does not exist in the current task hierarchy.")


                
            





    def get_current_task(self) -> 'Task':
        """
        Recursively identifies the current active sub-task.

        Returns:
            Task: The current sub-task or self if this task has no sub-tasks.
        """
        if len(self.sub_tasks) == 0 or self.current_sub_task is None:
            return self
        else:
            for sub_task in self.sub_tasks:
                if sub_task.name == self.current_sub_task:
                    return sub_task.get_current_task()

    def generate_prompt(self,terminal_goal) -> Dict[str, str]:
        """
        Generates and returns prompts for each participant in current task.

        Args:
            terminal_goal (str): The terminal goal of the task, which is the goal that the user wants to accomplish.

        Returns:
            Dict[str, str]: A dictionary mapping participant names to prompts.
        """
        current_task = self.get_current_task()
        prompts = {}
        for participant,instructions in current_task.participants.items():
            prompt =  "You are an AI assistant taking the role of " + participant + " in a team that is working to accomplish a goal.\n"
            prompt += "The terminal goal is " + terminal_goal +"\n"
            prompt += "The current goal is: " + current_task.goal + ".\n"
            prompt += "Your instructions are: " + instructions + ".\n"
            prompt += "Accomplish the goal through discussion and agent callable functions.\n"
            prompts[participant] = prompt
        return prompts
    
    def generate_system_message(self) -> str:
        """
        Generates and returns the system message.

        Returns:
            str: The generated system message.
        """
        system_message =  "You are an AI agent that is a member of a collaborative team of AI agents operating within a framework of Task objects which you have access to create and to modify in pursuit of the user's goal.\n"
        system_message += "You will be assigned a role and a set of instructions for that role.\n"
        system_message += "Your goal is to accomplish the task by following your instructions and by communicating with your teammates.\n"
        system_message += "You must update your operational plan by responding with the agent callable function 'update_task' to modify the Task hierarchy when applicable.\n"
        system_message += "A Task hierarchy is a tree of Task objects where each Task object has a list of sub-Tasks.\n"
        system_message += "# agent callable functions\n"
        system_message += "\n".join(self.get_agent_callable_function_headers())
        system_message += "\n# Respond in the following format:\n"
        system_message += "# Team Discussion\n"
        system_message += " ... "
        system_message += "\n# agent callable functions\n"
        system_message += "\nHere are the Task updates that I think we should make to complete the user request\n"
        system_message += "```\n"
        system_message += "...\n"
        system_message += "```\n"
        return system_message

    def get_agent_callable_function_headers(self) -> List[str]:
        """
        Returns a list methods that we want to expose to the agent, created with the typing module.

        Returns:
            List[str]: A list of strings with only header, docstring, and type hints for the methods we want to expose to the agent with 
        """
        methods = []
        for name, method in inspect.getmembers(self, predicate=inspect.ismethod):
            # We do want to show the init method to the agents but we don't want them to call it
            if name in agent_callable_functions or name == "__init__":
                
                signature = inspect.signature(method)
                type_hints = get_type_hints(method)

                parameters = signature.parameters

                return_type = signature.return_annotation


                header = f"def {name}("
                for i, (param_name, param) in enumerate(parameters.items()):
                    header += f"{param_name}: {type_hints[param_name].__name__}, "

                # Remove the last comma and space
                header = header[:-2]

                header += f") -> {return_type}:"
                docstring = method.__doc__
                header += f"\n\t\"\"\"\n\t{docstring}\n\t\"\"\""
                header += "\n\t# The code to implement\n"
                header += "\n\tpass\n"

                methods.append(header)
        return methods
    
    def check_string_for_function_syntax(self, string: str) -> bool:
        """
        Checks if a string contains a function call with parameters in proper syntax.
        """
        return string.count("(") == string.count(")") and string.count("(") > 0 and string.count(")") > 0
    
    @abstractmethod
    def run(self):
        pass

#to string
    def __str__(self):
        sub_task_names=[]
        for sub_task in self.sub_tasks:
            sub_task_names.append(sub_task.name)

        return f"Task: {self.name}\nGoal: {self.goal}\nParticipants: {self.participants}\nSub Tasks: {sub_task_names}\nCurrent Sub Task: {self.current_sub_task}\nCompleted: {self.completed}"

class TestTask(Task): 
    def __init__(self, name: str, goal: str, participants: Dict[str, str], sub_tasks: Optional[List[Task]] = None, current_sub_task: Optional[str] = None) -> None:
        """
        Initializes a new Task object.

        Args:
            name (str): The name of the task.
            goal (str): The goal or objective of the task.
            participants (Dict[str, str]): A dictionary mapping role names to their instructions.
            sub_tasks (Optional[List[Task]]): An optional list of sub-tasks, for when this task needs to be broken down into smaller tasks.
            current_sub_task (Optional[str]): An optional current sub-task. Deprecated, in favor of making the current sub-task the first sub-task in the list of sub-tasks.
        """
        super().__init__(name, goal, participants, sub_tasks, current_sub_task)

    def run(self):
        """
        Runs the task.
        """
        while not self.completed:
            prompts = self.get_current_task().generate_prompt(self.goal)
            system_message = self.generate_system_message()

            for participant, prompt in prompts.items():
              # Send the messages to the user and prompt for a response
              response = input(system_message + "\n" + prompts[participant] + "\n")
              # Find the last code block in the response
              code_block = response.split("```")[-2]
              # Split the code block into lines
              lines = code_block.split("\n")
              # Loop
              for line in lines:
                  if not line.startswith("#") and self.check_string_for_function_syntax(line):
                      function_name = line.split("(")[0]
                      if function_name in [ 'update_task']:
                          try:
                              line= line.replace("update_task", "self.update_task")
                              print("Evaluating: ", line)
                              eval(line)
                          except Exception as e:
                              print("Error: ", e)
                      else:
                          print("Error: ", function_name, " is not a valid agent callable function.")
                  else:
                      print("Error: ", line, " is not a valid agent callable function call.")


if __name__ == "__main__":
    task = TestTask("RootTask", "Goal 1",
                     {"Role 1": "Instructions 1", "Role 2": "Instructions 2"},
                     sub_tasks=[
                         TestTask("Task2", "Goal 2", {"Role 1": "Instructions 1", "Role 2": "Instructions 2"},
                                  sub_tasks=[TestTask("Task3", "Goal 3", {"Role1": "Instructions 1", "Role 2": "Instructions 2"},
                                                      sub_tasks=[TestTask("Task4", "Goal 4", {"Role 1": "Instructions 1", "Role 2": "Instructions 2"},
                                                                          sub_tasks=[TestTask("Task5", "Goal 5", {"Role 1": "Instructions 1", "Role 2": "Instructions 2"})]
                                                                )]
                                            )]
                      )]
                  )

    # print(task)
    # print("\n\n\n\n")
    # # Uncomment this section to see update_task in action
    # # update the goal
    # task.update_task({'goal':"Goal6"})
    # # add a task
    # task.update_task({'Task7': 'TestTask("Task3", "Goal 3", {"Role 1": "Instructions 1", "Role 2": "Instructions 2"})'})
    # # Update Role 1's instructions in Task3
    # task.update_task({'Task2.Task3.participants': '{"User1":"New Instructions111111111111111"}'})
  
    # print(task)


    # Example of what a universal root task might look like, see if you can get agents to drive it
    # the RootTask is the task that the user wants to accomplish, and it starts with an initial task of planning the task hierarchy

    RootTask = TestTask("Fullfill_Request", 
                        "Fullfill the user's request: {user_request}",
                        {},
                        current_sub_task="Analyze_Request",
                        sub_tasks=[TestTask("Analyze_Request", "We want the Task hierarchy to be populated with a plan to satisfy the given request.",
                                            {
                                                "Task_Analyzer": "Analyze the given request, identify key goals and roles with relevant expertise.", 
                                                "Workflow_Planner": "Based on the analysis, propose a set of update_task calls that instruct the team to accomplish the goal."
                                            }
                                          )
                                  ]
                      )

    RootTask.run()



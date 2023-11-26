from AgentDrivenStateMachine import AgentDrivenStateMachine
from autogen import AssistantAgent, GroupChat, GroupChatManager, UserProxyAgent,Completion
import sys
import json
import argparse
from rich.console import Console
from rich.style import Style
from rich.table import Table
from rich import box

class GroupPlanning:
    def __init__(self, initial_state: dict, llm_config: dict,user_request:str):
        """
        Initializes the GroupPlanning module.

        Args:
            state_machine (AgentDrivenStateMachine): The state machine managing the workflow.
            llm_config (dict): Configuration for the language model.
        """
        self.state_machine = AgentDrivenStateMachine(initial_state, llm_config)
        self.llm_config = llm_config
        self.user_proxy = UserProxyAgent(
            name="User",
            system_message="A human user. Interact with the planner to discuss the plan. Plan execution needs to be approved by this admin.",
            code_execution_config=False,
            llm_config=self.llm_config
        )
        self.console = Console()
        self.user_request = user_request
        
        print("Initial State:")
        state_table=Table(title="Initial State", show_header=True, header_style="dim")
        state_table.add_column("Key")
        state_table.add_column("Value")
        goal=initial_state['goal']
        group_instructions=initial_state['group_instructions']
        individual_instructions=initial_state['individual_instructions']
        individual_instructions_str=""
        for role,instruction in individual_instructions.items():
            individual_instructions_str+=role+": "+instruction+"\n"
        state_table.add_row("Goal",goal)
        state_table.add_row("Group Instructions",group_instructions)
        state_table.add_row("Individual Instructions",individual_instructions_str)

        self.console.print(state_table)
        print("")


    def initiate_group_chat(self):
        """
        Initiates and manages a group chat based on the user's request, running in a loop until completion.

        Args:
            user_request (str): The user's request to be processed in the group chat.
        """
        # clear the openai cache
        Completion.clear_cache()
        agents = self.state_machine.get_agents_for_current_state()
        agents.append(self.user_proxy)  
        print(agents)
        group_chat = GroupChat(agents=agents, messages=[], max_round=20)
        system_message = self.state_machine.get_system_message("Manager")
        chat_manager = GroupChatManager(group_chat, llm_config=self.llm_config, system_message=system_message)
        state_details = self.state_machine.get_current_state_details()

     # Debug messages
        self._print_debug_messages( )
        # Start the chat loop
        while self.state_machine.get_state_machine().get_current_state() != 'complete':
            self.user_proxy.initiate_chat(chat_manager,config=group_chat,message= self.user_request)

            # Process messages for function calls
            for message in group_chat.messages:
                function_call = self.extract_function_call(message['content'])
                print(f"Function call: {function_call}")
                if function_call:
                    self.execute_function_call(function_call)

            # Reset messages after processing
            group_chat.messages = []
            # set current state to complete for testing
            self.state_machine.get_state_machine().current_state = 'complete'

    def _print_debug_messages(self):
        """
        Prints debug messages using rich in table format.

        Args:
            agents (list): List of agents in the group chat.
            state_details (dict): Details of the current state.
        """
        state_details=self.state_machine.get_current_state_details()
        # Table for Workflow Details
        workflow_table = Table(title="Workflow Details", show_header=False, header_style="bold magenta",box=box.SQUARE)
        workflow_table.add_column("" )
        workflow_table.add_column("")
        workflow_table.add_row("")
        workflow_table.add_row("Initial Request", self.user_request)
        workflow_table.add_row("")
        workflow_table.add_row("Current Goal", state_details['goal'])
        workflow_table.add_row("")
        workflow_table.add_row("Group Instruction", state_details['group_instructions'])
        workflow_table.add_row("")
        print("")
        print("")
        # Table for Roles and Individual Instructions
        roles_table = Table(title="Roles and Individual Instructions", show_header=True, header_style="dim")
        roles_table.add_column("Role")
        roles_table.add_column("Individual Instruction")

        roles_table.add_row("Manager", self.state_machine.get_system_message("Manager"))
        for role, instructions in state_details['individual_instructions'].items():
            roles_table.add_row("")
            roles_table.add_row(role, self.state_machine.get_system_message(role))
        roles_table.add_row("")
        # Print the tables
        self.console.print(workflow_table)
        self.console.print(roles_table)
        print("")


    def extract_function_call(self, message):
        """
        Extracts a function call from a message using the Nexus Raven pipeline.

        Args:
            message (str): The message to extract the function call from.
            nexus_raven_pipeline: The pipeline object for Nexus Raven.

        Returns:
            str: The extracted function call or None if not found.
        """
        start_str = "Initial Answer: "
        end_str = "\nReflection: "
        start_idx = message.find(start_str) + len(start_str)
        end_idx = message.find(end_str)
        
        if start_idx != -1 and end_idx != -1:
            return message[start_idx: end_idx]
        return None


def load_file(file_path: str) -> dict:
    try:
        with open(file_path) as f:
            return json.load(f)
    except:
        print(f"Error loading file from {file_path}.")
        sys.exit(1)

# Example usage
if __name__ == "__main__":
    # Parse arguments
    print()
    parser = argparse.ArgumentParser()
    parser.add_argument("initial_state", help="The path to the workflow config file.",default="initial_state.json")
    parser.add_argument("llm_config", help="The path to the LLM config and sampler settings.",default="llm_config.json")
    args = parser.parse_args()

    # Load the config files
    initial_state = load_file(args.initial_state)
    llm_config = load_file(args.llm_config)
    llm_config['cache_dir'] = None

    
    group_planning = GroupPlanning(initial_state, llm_config,"""Provide a data storage system that optimizes for cost, efficiency, and ease of use.  The data store will be small units of timeseries data related to distributed computing""")
    group_planning.initiate_group_chat()

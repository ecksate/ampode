class StateMachine:
    """
    A class representing a state machine for managing the states and transitions in a workflow, including roles, instructions, goals, and completion status.
    """

    def __init__(self,initial_state=None):
        """
        Initializes the StateMachine without any states.
        """
        self.states = {}
        self.states['init'] = initial_state
        self.current_state = 'init'

    def get_current_state(self):
        """
        Finds the current state with incomplete goals.

        Returns:
            str: The name of the current state.
        """
        return self.current_state
    def get_current_state_details(self):
        """
        Finds the details for the current state.

        Returns:
            dict: The details for the current state.
        """
        return self.states[self.current_state]
    def add_state(self, state_name, state):
        """
        Adds a new state to the state machine with its associated details and transitions.
        """
        self.states[state_name] = state
    
    def retrieve_state(self, state_name):
        """
        Finds the details for a given state.

        Args:
            state_name (str): The name of the state.

        Returns:
            dict: The details for the state.
        """
        if state_name in self.states:
            return self.states[state_name]
        else:
            raise KeyError(f"State {state_name} does not exist.")
        
    def update_state(self, state_name, state):
        """
        Updates the details for a given state.

        Args:
            state_name (str): The name of the state.
            state (dict): The updated details for the state.
        """
        if state_name in self.states:
            self.states[state_name] = state
        else:
            raise KeyError(f"State {state_name} does not exist.")

    def remove_state(self, state_name):
      """
      Removes a state from the state machine.
      """
      del self.states[state_name]

    def transition(self):
        """
        Transitions the state machine to a new state assuming the current state has been completed.
        Assumes self.state is an object that includes {"transition":"<name of next state>"}
        Assumes self.state is an object that includes {"completed":<bool>}
        """
        if self.states[self.current_state]['completed']:
            self.current_state = self.states[self.current_state]['transition']
            return True
        else:
            return False
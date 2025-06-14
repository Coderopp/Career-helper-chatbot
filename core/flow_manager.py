# Conversation flow logic

class CareerChatbotState:
    STATES = ['onboarding', 'preference_extraction', 'values_assessment', 
              'career_mapping', 'recommendations', 'refinement', 'next_steps']

    def __init__(self, initial_state='onboarding'):
        if initial_state not in self.STATES:
            raise ValueError(f"Invalid initial state: {initial_state}")
        self.current_state = initial_state

    def transition_to(self, next_state):
        if next_state not in self.STATES:
            raise ValueError(f"Invalid next state: {next_state}")
        # Add any transition logic/validation here if needed
        self.current_state = next_state
        return self.current_state

    def get_current_state(self):
        return self.current_state

# Example usage (can be removed or adapted later):
# if __name__ == '__main__':
#     flow = CareerChatbotState()
#     print(f"Initial state: {flow.get_current_state()}")
#     flow.transition_to('preference_extraction')
#     print(f"Next state: {flow.get_current_state()}")

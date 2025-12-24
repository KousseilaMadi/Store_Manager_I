class State:
    def __init__(self, auth_service):
        self.auth_service = auth_service
        self.state = {
            "current_register": 1,
            "max_register_number": 1,
            "registers": {"register-1":[]},
            "current_user": self.auth_service.get_current_user(),
            "filters":{}
        }

    def set_state(self, state):
        self.state = state
        print(self.state)
    
    def get_state(self):
        return self.state
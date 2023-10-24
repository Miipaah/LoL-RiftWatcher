

import requests

class ReplayManager:

    def __init__(self, base_url="https://127.0.0.1:2999"):
        self.base_url = base_url
        self.endpoint = f"{self.base_url}/replay/playback"
        self.state = None
        self.paused = False
        self.time = 0.0


    def get_state(self):
        response = requests.get(self.endpoint, verify=False)
        response.raise_for_status()
        self.state = response.json()
        return self.state

    def get_current_time(self):
        if self.state is None:
            self.get_state()

        current_time = self.state.get('time', 0) 
        return current_time

    def play(self):
        if self.state is None:
            self.get_state()
        
        response = requests.post(self.endpoint, json={'paused': False}, verify=False)
        response.raise_for_status()
        self.get_state()  # Update the local state after changing the server state
        return response.json()

    def pause(self):
        if self.state is None:
            self.get_state()
        
        response = requests.post(self.endpoint, json={'paused': True}, verify=False)
        response.raise_for_status()
        self.get_state()  # Update the local state after changing the server state
        return response.json()



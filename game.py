import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
class LiveGame:
    def __init__(self, base_url="https://127.0.0.1:2999"):
        self.base_url = base_url
        self.endpoint = f"{self.base_url}/liveclientdata/gamestats"
        self.state = None

    def __getstate__(self):
        response = requests.get(self.endpoint, verify=False)
        response.raise_for_status()
        self.state = response.json()
        return self.state
    
    def get_current_time(self):
        if self.state is None:
            self.__getstate__()

        current_time_buffer = self.state.get('gameTime', 0) 

        self.__getstate__()
        current_time = self.state.get('gameTime', 0)

        if current_time_buffer == current_time:
            return "paused"
        else:
            return current_time

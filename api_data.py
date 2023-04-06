import requests
from enum import Enum

headers = {
    "X-TBA-Auth-Key": "_"
}

class Alliance(Enum):
    BLUE = "blue"
    RED = "red"

class TBADataFetcher:
    def __init__(self, team_key, match_key):

        self._url = f"https://www.thebluealliance.com/api/v3/match/{match_key}"
        self._response = requests.request("GET", self._url, headers=headers, data={})

        blue_ls = self._response.json()["alliances"]["blue"]["team_keys"]
        red_ls = self._response.json()["alliances"]["red"]["team_keys"]

        if team_key in blue_ls: self.alliance = Alliance.BLUE
        elif team_key in red_ls: self.alliance = Alliance.RED

        self.robot_num = self._response.json()["alliances"][self.alliance.value]["team_keys"].index(team_key) + 1

    def get_charge(self):
        response = self._response.json()["score_breakdown"][self.alliance.value]
        return response[f"autoChargeStationRobot{self.robot_num}"]
    
    def get_mobility(self):
        response = self._response.json()["score_breakdown"][self.alliance.value]
        return response[f"mobilityRobot{self.robot_num}"]
    
def aggregate_data(team_num):
    team_key = "frc" + str(team_num)
    url = f"https://www.thebluealliance.com/api/v3/team/{team_key}/matches/2023/keys"
    response = requests.request("GET", url, headers=headers, data={})
    for match_key in response.json():
       print(TBADataFetcher(team_key, match_key).get_charge())
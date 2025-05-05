import os
import steam_web_api as SteamAPI
from dotenv import load_dotenv

class UserRegistration:

    KEY : str
    steam : SteamAPI.Steam
    client : SteamAPI.Client
    apps : SteamAPI.Apps
    users : SteamAPI.Users

    def __init__(self):
        load_dotenv()
        self.KEY = os.getenv("SteamKey")
        self.steam = SteamAPI.Steam(self.KEY)
        self.client = SteamAPI.Client(self.KEY)
        self.apps = SteamAPI.Apps(self.client)
        self.users = SteamAPI.Users(self.client)


    def _get_achievements_of_game(self, achievements : dict):
        result : list = []
        try:
            player_achievements = achievements["playerstats"]["achievements"]
            for ach in player_achievements:
                if ach["achieved"] == 1:
                    result.append(ach["apiname"])
            return result
        except Exception as e:
            e.with_traceback(None)

    def request_user_achievements(self, user_id : str):
        user = self.steam.users.search_user(user_id)
        if(user == "No Match") : 
            print("Wrong User ID")
            return
        games = self.users.get_owned_games(steam_id=user["player"]["steamid"])
        user_achievements_per_game_dict : dict = dict()
        if("games" not in games.keys()):
            return user_achievements_per_game_dict
        for game in games["games"]:
            achievements = None
            try:    
                achievements = self.apps.get_user_achievements(user["player"]["steamid"], game["appid"])
            except:
                pass
            if(achievements is None): continue
            unlocked_achievements = self._get_achievements_of_game(achievements)
            user_achievements_per_game_dict[game["appid"]] = unlocked_achievements
        return user_achievements_per_game_dict



#GetGlobalAchievementPercentagesForApp("Hollow Knight")
#print(achievements)






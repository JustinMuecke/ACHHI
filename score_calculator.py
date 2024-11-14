import steam_web_api as SteamAPI
from steamwebapi.api import ISteamUser, IPlayerService, ISteamUserStats
import os

def calculate_score(achievements : dict):
    result : int = 0
    steamUserStats = ISteamUserStats(steam_api_key=os.environ["SteamKey"])
    for entry in achievements.keys():
        globalPercentage = steamUserStats.get_global_achievement_percentages_for_app(entry)["achievementpercentages"]["achievements"]
        for achievement in globalPercentage:
            if achievement["name"] in achievements[entry]:
                percentage = achievement["percent"]
                name = achievement["name"]
                print(f"{name} has been achieved by {percentage}% of players")
                result += (100 - percentage)
    
    return result

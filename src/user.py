from userReg import UserRegistration
from score_calculator import calculate_score
class Hunter:

    name : str
    score : int
    last_updated : str
    achievements : dict # GameID : [Achievements]
    steam_id : str

    def __init__(self, name : str):
        self.name = name
        self.last_updated = None
        self.achievements = UserRegistration().request_user_achievements(self.name)
        self.score = calculate_score(self.achievements)

    
    def set_achievements(self, achievements : dict) -> None:
        self.achievements = achievements

    def update_achievements(self):
        self.achievements = UserRegistration().request_user_achievements(self.name)


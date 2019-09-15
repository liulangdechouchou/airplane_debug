class GameStats():
    """跟踪游戏的统计信息"""

    def __init__(self,ai_settings):
        self.ai_settings = ai_settings
        self.reset_stats()
        self.game_active = False
        self.score = 0
        self.high_score = 0
        self.level = 1
    def reset_stats(self):
        """初始化 统计信息"""
        self.ships_left = self.ai_settings.ship_limit # 这里left是剩余的意思
        self.level = 1
        self.score = 0


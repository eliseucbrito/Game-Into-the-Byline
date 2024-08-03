class Score:
    def __init__(self, highscore):
        self.highscore = highscore

    def set_highscore(self, value):
        self.highscore -= value

    def get_highscore(self):
        return self.highscore

    def reset_highscore(self):
        self.highscore = 0

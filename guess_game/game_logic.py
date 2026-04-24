import random

class Game:
    def __init__(self):
        self.secret = random.randint(1, 100)
        self.attempts = 0
        self.history = []
        self.low = 1
        self.high = 100

    def guess(self, number):
        self.attempts += 1

        if number < self.secret:
            self.low = max(self.low, number + 1)
            self.history.append((number, "low"))
            return "low"

        elif number > self.secret:
            self.high = min(self.high, number - 1)
            self.history.append((number, "high"))
            return "high"

        else:
            self.history.append((number, "correct"))
            return "correct"
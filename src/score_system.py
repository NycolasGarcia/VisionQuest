from .config import MAX_SCORE, BONUS_STREAK, MAX_LIVES


class ScoreSystem:
    def __init__(self):
        self.score = 0
        self.streak = 0
        self.lives = MAX_LIVES
        self.questions_answered = 0
        self.correct_count = 0
        self.wrong_count = 0

    def correct_answer(self):
        """Register a correct answer. Returns True if bonus was awarded."""
        self.score += 1
        self.streak += 1
        self.questions_answered += 1
        self.correct_count += 1
        bonus = self.streak % BONUS_STREAK == 0
        if bonus:
            self.score += 1
        self.score = min(self.score, MAX_SCORE)
        return bonus

    def incorrect_answer(self):
        """Register wrong answer. Returns remaining lives."""
        self.streak = 0
        self.lives -= 1
        self.questions_answered += 1
        self.wrong_count += 1
        return self.lives

    @property
    def progress(self):
        return self.score / MAX_SCORE

    @property
    def is_win(self):
        return self.score >= MAX_SCORE

    @property
    def is_loss(self):
        return self.lives <= 0

    @property
    def is_game_over(self):
        return self.is_win or self.is_loss

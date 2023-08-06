import random

class MotivationalQuotes:
    def __init__(self):
        self.quotes = [
            "Success is not the key to happiness. Happiness is the key to success. If you love what you are doing, you will be successful.",
            "Believe in yourself and all that you are. Know that there is something inside you that is greater than any obstacle.",
            "Don't watch the clock; do what it does. Keep going.",
            "The only limit to our realization of tomorrow will be our doubts of today.",
            "The future belongs to those who believe in the beauty of their dreams.",
            "The best way to predict the future is to create it.",
            "Your work is going to fill a large part of your life, and the only way to be truly satisfied is to do what you believe is great work. And the only way to do great work is to love what you do.",
            "The only way to do great work is to love what you do.",
            "Opportunities don't happen. You create them.",
            "Your time is limited, don't waste it living someone else's life.",
            "Success usually comes to those who are too busy to be looking for it.",
            "Hard work beats talent when talent doesn't work hard.",
            "The only place where success comes before work is in the dictionary.",
            "Don't be pushed around by the fears in your mind. Be led by the dreams in your heart."
        ]

    def get_random_quote(self):
        return random.choice(self.quotes)
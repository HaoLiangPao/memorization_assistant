import math
import json

import opencc


# Base class for any item to be memorized
class MemorizationItem:
    def __init__(self, content, source, difficulty=1):
        self.content = content
        self.source = source
        self.difficulty = difficulty
        self.review_schedule = []

    def set_review_schedule(self, intervals):
        self.review_schedule = intervals

    def get_content(self):
        return self.content


# Derived class for Chinese poems
class ChinesePoem(MemorizationItem):
    def __init__(self, content, author, title, tags, difficulty=2):
        super().__init__(content=content, source="Poem", difficulty=difficulty)
        self.author = author
        self.title = title
        self.tags = tags


# Derived class for Vocabulary words
class VocabularyWord(MemorizationItem):
    def __init__(self, word, difficulty=1):
        super().__init__(content=word, source="Vocabulary", difficulty=difficulty)


# Function to calculate the review intervals based on Ebbinghaus curve and user's configuration
def calculate_intervals_based_on_config(poem, config):
    memory_skill_factors = {
        "poor": 1.1,
        "average": 1.3,
        "good": 1.5,
        "excellent": 1.7
    }

    decay_factor = memory_skill_factors.get(config["memory_skill"], 1.3)
    initial_interval = 1  # First review the next day

    # Adjust based on the user's age
    age_adjustment = 1 + (config["age"] - 20) * 0.01

    # Commitment level affects frequency of reviews
    commitment_levels = {
        "low": 5,  # Review every 5 days
        "medium": 3,  # Review every 3 days
        "high": 1  # Review daily
    }
    review_frequency = commitment_levels.get(config["commitment_level"], 3)

    intervals = []
    for i in range(config["poems_per_week"]):
        next_interval = math.ceil(initial_interval * (decay_factor ** i) * age_adjustment)
        intervals.append(next_interval * review_frequency)

    poem.set_review_schedule(intervals)
    return intervals


# Function to load the poem data from a JSON file
def load_poems_from_json(json_file):
    with open(json_file, 'r') as file:
        poem_data = json.load(file)

    poems = []

    t2sConverter = opencc.OpenCC('t2s.json')

    for poem in poem_data:
        chinese_poem = ChinesePoem(
            content=t2sConverter(poem['paragraphs']),
            author=t2sConverter(poem['author']),
            title=t2sConverter(poem['title']),
            tags=t2sConverter(poem['tags'])
        )
        poems.append(chinese_poem)
    return poems


# Function to load the configuration file
def load_learning_config(config_file):
    with open(config_file, 'r') as file:
        config = json.load(file)
    return config
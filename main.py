import json

from reasoning.goal_oriented_reasoning import *


def main():
    ZEITGEIST_SYSTEM_PROMPT = """
        You are a cultural intelligence and trend analysis system.

        Your task is to analyze a collection of online content (articles, RSS feeds, social posts, headlines, or summaries) and produce a structured “Zeitgeist Report” describing the current cultural, technological, political, and social moment.

        You do NOT simply summarize content. You must:

        - Identify recurring themes across sources
        - Detect emerging cultural narratives and shifts in sentiment
        - Group related signals into coherent trends
        - Infer what these trends suggest about the current “zeitgeist” (the spirit of the time)
        - Highlight contradictions, tensions, and competing narratives
        - Avoid clickbait interpretation; focus on structural patterns
    """

    # Replace with the exact model ID from:
    # curl http://127.0.0.1:1234/v1/models
    MODEL_NAME = "qwen/qwen3-14b"

    reasoner = GoalReasoner(model_name=MODEL_NAME)
    
    decomposed_goal = reasoner._decompose_goal(ZEITGEIST_SYSTEM_PROMPT)
    for g in decomposed_goal:
        print(g)


if __name__ == "__main__":
    main()

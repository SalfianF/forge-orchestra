#!/usr/bin/env python3
"""Demo: create and register a custom agent with the orchestration engine."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from orchestrator.core.engine import OrchestrationEngine, Agent, Task


class CustomSentimentAgent:
    """A custom agent for sentiment analysis tasks."""

    def __init__(self):
        self.name = "sentiment-analyzer"
        self.role = "Sentiment Analysis"

    def analyze(self, text: str) -> dict:
        """Analyze sentiment of input text."""
        positive_words = ["good", "great", "excellent", "amazing", "love"]
        negative_words = ["bad", "terrible", "awful", "hate", "worst"]

        text_lower = text.lower()
        positive_count = sum(1 for w in positive_words if w in text_lower)
        negative_count = sum(1 for w in negative_words if w in text_lower)

        if positive_count > negative_count:
            sentiment = "positive"
        elif negative_count > positive_count:
            sentiment = "negative"
        else:
            sentiment = "neutral"

        return {
            "sentiment": sentiment,
            "score": positive_count - negative_count,
            "positive_signals": positive_count,
            "negative_signals": negative_count,
        }


def main():
    engine = OrchestrationEngine(max_concurrency=2)

    # Register custom agent
    sentiment_agent = CustomSentimentAgent()
    engine.register_agent(Agent(
        name=sentiment_agent.name,
        role=sentiment_agent.role,
        capabilities=["sentiment", "analysis", "nlp"],
    ))

    sample_text = "This project is great! I love the architecture and amazing features."
    task = Task(
        id="sentiment-1",
        description=f"Analyze sentiment: {sample_text[:50]}...",
        agent="sentiment-analyzer",
    )
    engine.create_task(task)

    result = sentiment_agent.analyze(sample_text)
    print(f"Sentiment Result: {result}")


if __name__ == "__main__":
    main()

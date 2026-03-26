"""
Shared data for the Mood Machine lab.

This file defines:
  - POSITIVE_WORDS: starter list of positive words
  - NEGATIVE_WORDS: starter list of negative words
  - SAMPLE_POSTS: short example posts for evaluation and training
  - TRUE_LABELS: human labels for each post in SAMPLE_POSTS
"""

# ---------------------------------------------------------------------
# Starter word lists
# ---------------------------------------------------------------------

POSITIVE_WORDS = [
    "happy",
    "great",
    "good",
    "love",
    "excited",
    "awesome",
    "fun",
    "chill",
    "relaxed",
    "amazing",
    # slang / extended
    "hopeful",
    "proud",
    "vibing",
    "slaps",
    "hyped",
    "blessed",
]

NEGATIVE_WORDS = [
    "sad",
    "bad",
    "terrible",
    "awful",
    "angry",
    "upset",
    "tired",
    "stressed",
    "hate",
    "boring",
    # slang / extended
    "rough",
    "destroyed",
    "exhausted",
    "drained",
]

# ---------------------------------------------------------------------
# Starter labeled dataset
# ---------------------------------------------------------------------

# Short example posts written as if they were social media updates or messages.
SAMPLE_POSTS = [
    "I love this class so much",
    "Today was a terrible day",
    "Feeling tired but kind of hopeful",
    "This is fine",
    "So excited for the weekend",
    "I am not happy about this",
    # --- added posts ---
    "no cap this assignment slaps 😂",                          # slang + emoji
    "I absolutely love sitting in traffic for two hours 🙃",    # sarcasm
    "lowkey stressed but highkey proud of myself ngl",          # slang, mixed
    "💀💀💀 that exam destroyed me",                            # emoji-heavy, negative
    "not bad I guess",                                          # understated, ambiguous
    "honestly could not care less at this point",               # negative/apathetic
    "today was rough but my friends showed up for me 🥲",       # mixed, emotional
    "vibing 😌",                                                # slang, minimal text
]

# Human labels for each post above.
# Allowed labels in the starter:
#   - "positive"
#   - "negative"
#   - "neutral"
#   - "mixed"
TRUE_LABELS = [
    "positive",  # "I love this class so much"
    "negative",  # "Today was a terrible day"
    "mixed",     # "Feeling tired but kind of hopeful"
    "neutral",   # "This is fine"
    "positive",  # "So excited for the weekend"
    "negative",  # "I am not happy about this"
    # --- added labels ---
    "positive",  # "no cap this assignment slaps 😂"             — slang for "this is great"
    "negative",  # "I absolutely love sitting in traffic 🙃"     — sarcasm; true meaning is negative
    "mixed",     # "lowkey stressed but highkey proud ngl"        — two competing emotions
    "negative",  # "💀💀💀 that exam destroyed me"               — skull emoji = overwhelmed/negative
    "neutral",   # "not bad I guess"                             — lukewarm, no strong signal
    "negative",  # "honestly could not care less at this point"  — apathy / disengagement
    "mixed",     # "today was rough but my friends showed up 🥲" — hard day softened by gratitude
    "positive",  # "vibing 😌"                                   — chill/content, slang positive
]


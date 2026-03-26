# Model Card: Mood Machine

This model card covers **both** versions of the Mood Machine classifier:

1. A **rule-based model** implemented in `mood_analyzer.py`
2. A **machine learning model** implemented in `ml_experiments.py` using scikit-learn

---

## 1. Model Overview

**Model type:**
Both models were built and compared. The rule-based model was developed first, then the ML model was trained on the same dataset.

**Intended purpose:**
Classify short text messages — social media posts, messages, one-liners — into one of four mood labels: `positive`, `negative`, `neutral`, or `mixed`.

**How it works (brief):**
- *Rule-based:* Each post is tokenized and scored by counting matches against `POSITIVE_WORDS` and `NEGATIVE_WORDS`. A negation rule flips the score when words like "not" or "never" precede a sentiment word. The final integer score maps to a label; if both positive and negative words appear (without negation cancelling them out), the post is labelled `mixed`.
- *ML model:* Posts are converted to bag-of-words vectors using `CountVectorizer`, then a logistic regression classifier learns which word patterns correspond to which labels from the training data.

---

## 2. Data

**Dataset description:**
`SAMPLE_POSTS` contains 14 posts total. The original 6 came with the starter code. 8 new posts were added to cover language styles not represented in the starter set.

**Labeling process:**
Labels for the original 6 posts were provided. The 8 new posts were labeled by reasoning about the dominant sentiment:
- Posts with clear positive or negative language were labeled `positive` or `negative`.
- Posts combining both feelings were labeled `mixed`.
- Posts with no clear sentiment signal were labeled `neutral`.

Some labels required judgment calls — for example, `"not bad I guess"` could reasonably be `neutral` or even slightly positive depending on context. These edge cases are noted below.

**Important characteristics of this dataset:**

- Contains slang: `"no cap"`, `"slaps"`, `"lowkey"`, `"highkey"`, `"ngl"`, `"vibing"`
- Contains emoji: `😂`, `🙃`, `💀`, `🥲`, `😌`
- Contains sarcasm: `"I absolutely love sitting in traffic for two hours 🙃"`
- Contains negation: `"I am not happy about this"`, `"not bad I guess"`
- Contains mixed feelings: `"Feeling tired but kind of hopeful"`, `"lowkey stressed but highkey proud"`
- Several posts are short or ambiguous: `"This is fine"`, `"vibing 😌"`

**Possible issues with the dataset:**

- **Very small (14 posts):** Not representative of real-world language diversity.
- **Label ambiguity:** Posts like `"not bad I guess"` and `"today was rough but my friends showed up"` could be labeled differently by different people.
- **Label imbalance:** The dataset has more `negative` and `positive` examples than `neutral` or `mixed`, which may bias learned models.
- **Sarcasm is not systematically covered:** Only one sarcasm example exists, which is not enough to teach any model to detect it.

---

## 3. How the Rule-Based Model Works

**Scoring rules:**

1. `preprocess(text)` lowercases the text, strips punctuation (except apostrophes), and splits on whitespace. Emojis are stripped as non-word characters.
2. `score_text(text)` loops over tokens:
   - Each token in `POSITIVE_WORDS` adds `+1` to the score.
   - Each token in `NEGATIVE_WORDS` subtracts `1` from the score.
   - **Negation enhancement:** if the token immediately before a sentiment word is a negator (`not`, `never`, `don't`, `doesn't`, `didn't`, `no`), the sign is flipped. So `"not happy"` scores `-1` instead of `+1`, and `"not bad"` scores `+1` instead of `-1`.
3. `predict_label(text)` maps the score to a label:
   - If both positive and negative words appear in the post (without being cancelled by negation), the label is `"mixed"` regardless of the net score.
   - Otherwise: score `> 0` → `"positive"`, score `< 0` → `"negative"`, score `== 0` → `"neutral"`.

Word lists were expanded beyond the starter set to include: `hopeful`, `proud`, `vibing`, `slaps`, `hyped`, `blessed` (positive) and `rough`, `destroyed`, `exhausted`, `drained` (negative).

**Strengths:**

- Transparent and inspectable — you can always trace exactly why a post received a score.
- Negation handling correctly catches `"I am not happy about this"` → `negative`.
- Mixed label detection correctly catches `"Feeling tired but kind of hopeful"` → `mixed`.
- Fast and requires no training data.

**Weaknesses:**

- **Sarcasm is invisible to it.** `"I absolutely love sitting in traffic for two hours 🙃"` scores `+1` (positive) because "love" is in `POSITIVE_WORDS`. The model has no way to detect that the intended meaning is the opposite.
- **Negation overcorrects.** `"not bad I guess"` scores `+1` (predicted: `positive`) because negation flips `bad` from `-1` to `+1`. The true label is `neutral` — "not bad" is lukewarm, not genuinely positive.
- **Blind to vocabulary it hasn't seen.** `"honestly could not care less at this point"` scores `0` → `neutral` because none of its words appear in either word list, even though the phrase clearly expresses apathy or disengagement.
- **Emojis carry no signal.** All emoji are stripped during preprocessing. `"💀💀💀"` alone would score `0`; only "destroyed" saves that post.
- **Context-free.** Words are scored one at a time with no understanding of sentence structure beyond single-step negation.

---

## 4. How the ML Model Works

**Features used:**
Bag-of-words vectors produced by `CountVectorizer`. Each post becomes a vector where each dimension represents a word in the vocabulary, and the value is how many times that word appears.

**Training data:**
The model trained on all 14 posts in `SAMPLE_POSTS` with labels from `TRUE_LABELS`.

**Training behavior:**
The ML model achieved **100% accuracy** on the training data. This is expected but misleading — the model is evaluated on the same data it trained on, so it has likely memorized the examples rather than learned general patterns. This is called **overfitting**.

**Strengths:**

- Learns patterns from labeled examples automatically — no need to hand-craft word lists.
- Can associate whole phrases or word co-occurrences with labels, not just individual words.
- Correctly labeled the sarcasm post (`"I absolutely love sitting in traffic"` → `negative`) — probably because other words in that post correlated with negative labels in the training data, not because it understood sarcasm.

**Weaknesses:**

- **100% training accuracy is a warning sign, not a success.** With only 14 examples, the model has more features (unique words) than training examples, making it trivial to memorize every post.
- **Will not generalize.** A new post using even slightly different wording than what it saw during training is likely to be mislabeled.
- **Sensitive to label choices.** Because the dataset is so small, changing one or two labels can significantly shift what the model learns. The labels you assign are not just annotations — they are the entire signal the model has.
- **No understanding of negation.** `CountVectorizer` treats `"not"` and `"happy"` as independent words. The model might learn `"not"` as a negative signal by coincidence rather than understanding that it modifies what follows.

---

## 5. Evaluation

**How the models were evaluated:**
Both models were evaluated on `SAMPLE_POSTS` against `TRUE_LABELS`. This is training-set accuracy for the ML model and a genuine test for the rule-based model (which was not trained on the data).

| Model | Accuracy |
|-------|----------|
| Rule-based | 10 / 14 = **71%** |
| ML (logistic regression) | 14 / 14 = **100%** (training accuracy — overfitted) |

**Examples of correct rule-based predictions:**

- `"I love this class so much"` → `positive` — "love" is a clear positive signal with no negation. Score `+1`.
- `"I am not happy about this"` → `negative` — negation correctly flips "happy" to `-1`. Score `-1`.
- `"Feeling tired but kind of hopeful"` → `mixed` — both "tired" (negative) and "hopeful" (positive) are detected. Score `0` but mixed label triggered.

**Examples of incorrect rule-based predictions:**

- `"I absolutely love sitting in traffic for two hours 🙃"` → predicted `positive`, true `negative`. "love" scores `+1` and no other sentiment word is present. The sarcastic tone and 🙃 emoji are both invisible to the model.
- `"not bad I guess"` → predicted `positive`, true `neutral`. Negation flips "bad" to `+1`, but "not bad" in English means lukewarm — not genuinely positive. The negation rule overcorrects here.
- `"today was rough but my friends showed up for me 🥲"` → predicted `negative`, true `mixed`. "rough" scores `-1`, but no positive word appears in the sentence, so mixed detection never triggers. The positive feeling is expressed through "showed up for me" and 🥲 — both invisible to the model.

---

## 6. Limitations

1. **The dataset is very small.** 14 examples is not enough to draw reliable conclusions about model behavior. A single mislabeled post shifts accuracy by 7 percentage points.

2. **Training accuracy is not real accuracy.** The ML model's 100% score means it memorized the data, not that it learned to classify mood. It would likely perform much worse on new posts it has never seen.

3. **Sarcasm is undetectable with these approaches.** Neither model has any mechanism to recognize when positive words are used with negative intent. This is a hard problem even for large language models.

4. **Emojis are effectively ignored.** The rule-based preprocessor strips all emoji. The ML model may retain them as tokens, but with only one or two occurrences of each, they carry no reliable weight.

5. **The model does not generalize beyond its vocabulary.** Any post using sentiment language not in `POSITIVE_WORDS` / `NEGATIVE_WORDS` (rule-based) or not seen during training (ML) will be misclassified or default to `neutral`.

---

## 7. Ethical Considerations

**Misclassifying distress.** A message expressing genuine distress through slang or sarcasm — `"I'm totally fine 🙂"`, `"it's fine lol"` — could be classified as `positive` or `neutral`. In any application that monitors wellbeing, this is a meaningful and potentially harmful failure.

**Dialect and cultural scope.** The dataset was written in a specific style of informal American English with Gen Z internet slang. The word lists and training examples reflect that narrow range. A speaker using AAVE, British English, or other dialects with different emotional vocabulary or tone markers would be more likely to receive incorrect labels. The model is implicitly optimized for one language community and may systematically misread others.

**Emoji interpretation varies.** Emoji like 🥲 (smiling face with tear) or 💀 (skull used to mean "I'm dead/this is hilarious") have culturally specific meanings that vary across communities and age groups. Neither model has any awareness of these meanings.

**Privacy.** Any real deployment of mood detection on personal messages raises significant privacy concerns. The model infers emotional state from private communication without the author's knowledge or consent.

---

## 8. Ideas for Improvement

- **Add more labeled data.** Even 50–100 diverse examples would make both models substantially more reliable.
- **Add a real test set.** Evaluate on posts the model was never trained on. Training accuracy tells you nothing about generalization.
- **Use TF-IDF instead of CountVectorizer.** This downweights very common words (`"the"`, `"a"`) and gives more weight to distinctive terms.
- **Add emoji mappings.** Build a small dictionary mapping common emoji to sentiment signals (`💀` → negative, `😌` → positive) and inject them as tokens during preprocessing.
- **Improve negation scope.** The current rule only checks the immediately preceding token. A window of 2–3 tokens would handle cases like `"I do not feel happy"`.
- **Add sarcasm markers.** Certain patterns (`"I absolutely love [negative thing]"`, inverted emoji like 🙃) could be treated as negative signals regardless of the words they contain.
- **Use a small pre-trained model.** A transformer-based model fine-tuned on sentiment data would handle slang, context, and sarcasm far better than either approach here — at the cost of much higher complexity.

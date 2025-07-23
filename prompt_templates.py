BIAS_DETECTOR_PROMPT = '''\
Analyze the following text for bias in the categories of race, gender, and mental health. For each biased or unfair word or phrase, flag it, specify the category, and suggest a more fair or neutral alternative. Return your answer as a JSON object with keys: flagged (list of flagged phrases), suggestions (list of suggested alternatives), and categories (list of categories for each flagged phrase, in order).

Text:
"""
{text}
"""
''' 
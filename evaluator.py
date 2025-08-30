def evaluate_answer(user_answer, keywords):
    if not user_answer.strip():
        return "Please provide an answer."

    keyword_list = [kw.strip().lower() for kw in keywords.split(",")]
    score = sum(1 for kw in keyword_list if kw in user_answer.lower())

    if score == len(keyword_list):
        return "Excellent! You covered all key points."
    elif score > 0:
        return f"Good attempt! You covered {score} out of {len(keyword_list)} key points."
    else:
        return "Try to include more relevant keywords in your answer."

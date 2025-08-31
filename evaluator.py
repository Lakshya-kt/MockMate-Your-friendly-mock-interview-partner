from sentence_transformers import SentenceTransformer, util

# Load model once
model = SentenceTransformer('all-MiniLM-L6-v2')

def evaluate_answer(user_answer, keywords, model_answer):
    # Keyword score calculation
    keyword_score = sum(1 for kw in keywords if kw.lower() in user_answer.lower())
    keyword_score_percentage = (keyword_score / len(keywords)) * 100 if keywords else 0

    # Semantic similarity using embeddings
    user_embedding = model.encode(user_answer, convert_to_tensor=True)
    model_embedding = model.encode(model_answer, convert_to_tensor=True)
    similarity = util.pytorch_cos_sim(user_embedding, model_embedding).item() * 100

    # Generate advanced feedback
    comments = []
    if keyword_score_percentage < 50:
        comments.append("Include more technical terms or relevant keywords.")
    else:
        comments.append("Good keyword coverage.")

    if similarity > 85:
        comments.append("Excellent explanation, very close to the expected answer.")
    elif similarity > 60:
        comments.append("Your answer is decent but can be improved with more detail.")
    else:
        comments.append("Your answer is significantly different; try to align with key concepts.")

    # Add specific suggestion if user missed any important keyword
    missing_keywords = [kw for kw in keywords if kw.lower() not in user_answer.lower()]
    if missing_keywords:
        comments.append(f"Consider adding these keywords: {', '.join(missing_keywords)}.")

    return {
        "keyword_score": round(keyword_score_percentage, 2),
        "similarity_score": round(similarity, 2),
        "comments": " ".join(comments)
    }

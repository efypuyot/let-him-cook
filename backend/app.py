# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import pandas as pd
# import faiss
# import joblib
# import re
# from sklearn.metrics.pairwise import cosine_similarity

# app = Flask(__name__)
# @app.before_request
# def before_request():
#     if request.headers.get('X-Forwarded-Host') == 'let-him-cook.loca.lt':
#         return  # Skip auth for LocalTunnel
# CORS(app, resources={
#     r"/recommend": {
#         "origins": [ 
#             "http://localhost:8080",
#             "https://let-him-cook-2025.vercel.app",  # Your Vercel URL
#             "https://a397-112-208-66-108.ngrok-free.app",  # Ngrok URL
#             "https://let-him-cook.loca.lt" # Localtunnel URL
#         ],
#         "methods": ["POST", "OPTIONS"],
#         "allow_headers": ["Content-Type", "bypass-tunnel-reminder", "User-Agent"],
#     }
# })

# # Load resources
# DATA_PATH = "/Users/ellen/Desktop/university/CMSC198.2F/let-him-cook/backend/final_filtered_recipes.json"
# TFIDF_PATH = "/Users/ellen/Desktop/university/CMSC198.2F/2/tfidf_vectorizer.pkl"
# FAISS_PATH = "/Users/ellen/Desktop/university/CMSC198.2F/2/faiss_index.bin"

# # Load the data
# df = pd.read_json(DATA_PATH, lines=True)

# # Ensure 'ner_str' column exists
# if 'ner_str' not in df.columns:
#     print("Generating 'ner_str' column...")
#     df['ner_str'] = df['NER'].apply(lambda tokens: ' '.join(tokens))

# # Load pre-trained models
# tfidf_vectorizer = joblib.load(TFIDF_PATH)
# faiss_index = faiss.read_index(FAISS_PATH)

# # Use sparse matrix to save memory
# tfidf_array = tfidf_vectorizer.transform(df['ner_str']).astype('float32')

# def clean_ingredients(raw_ingredients):
#     if isinstance(raw_ingredients, str):
#         raw_ingredients = [raw_ingredients]
#     pattern = re.compile(r"(\d+\.?\d*\s*[a-zA-Z]+)?\s*of\s*|\d+\.?\d*\s*[a-zA-Z]*")
#     cleaned = [re.sub(pattern, '', ing).strip().lower() for ing in raw_ingredients]
#     return ' '.join(cleaned)


# @app.route('/recommend', methods=['POST','OPTIONS'])
# def recommend():
#     print(app.url_map)
#     if request.method == 'OPTIONS':
#         response = jsonify({"status": "oasdk"})
#         response.headers.add("Access-Control-Allow-Headers", "bypass-tunnel-reminder, content-type")
#         return response
#     try:
#         data = request.get_json()
#         user_ingredients = data.get('ingredients', [])
#         print("Received ingredients:", user_ingredients)
        
#         # Validate input
#         if not user_ingredients or (len(user_ingredients) == 1 and not user_ingredients[0]):
#             return jsonify({"error": "Please provide at least one ingredient"}), 400
            
#         cleaned_input = clean_ingredients(user_ingredients)
        
#         # Transform to TF-IDF and convert to dense array
#         user_vec = tfidf_vectorizer.transform([cleaned_input]).astype('float32')
#         user_vec_dense = user_vec.toarray()  # Convert sparse to dense
        
#         # FAISS search
#         D, I = faiss_index.search(user_vec_dense, 10)
        
#         # Get cosine similarities
#         candidates = tfidf_array[I[0]].toarray()  # Convert to dense array
#         cosine_scores = cosine_similarity(user_vec_dense, candidates)[0]
        
#         # Sort results
#         sorted_indices = I[0][cosine_scores.argsort()[::-1]]
#         top_recipes = df.iloc[sorted_indices][['title', 'ingredients', 'directions', 'link']].to_dict(orient='records')
        
#         return jsonify(top_recipes)
        
#     except Exception as e:
#         print("Error in recommendation:", str(e))
#         return jsonify({"error": str(e)}), 500

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)

from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import joblib
import os

app = Flask(__name__)

@app.before_request
def before_request():
    if request.headers.get('X-Forwarded-Host') == 'let-him-cook.loca.lt':
        return  # Skip auth for LocalTunnel

CORS(app, resources={
    r"/recommend": {
        "origins": [ 
            "http://localhost:8080",
            "https://let-him-cook-2025.vercel.app",
            "https://a397-112-208-66-108.ngrok-free.app",
            "https://let-him-cook.loca.lt"
        ],
        "methods": ["POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "bypass-tunnel-reminder", "User-Agent"],
    }
})

# Load the dataset
DATA_PATH = os.path.join(os.path.dirname(__file__), "final_filtered_recipes.json")
df = pd.read_json(DATA_PATH, lines=True)

# Ensure required columns exist
if 'ner_str' not in df.columns:
    df['ner_str'] = df['NER'].apply(lambda tokens: ' '.join(tokens))

# Initialize TF-IDF Vectorizer
tfidf_vectorizer = TfidfVectorizer(max_features=10000)
tfidf_matrix = tfidf_vectorizer.fit_transform(df['ner_str'])

def clean_ingredients(raw_ingredients):
    """Clean and normalize input ingredients (accepts array of strings)"""
    pattern = re.compile(r"(\d+\.?\d*\s*[a-zA-Z]+)?\s*of\s*|\d+\.?\d*\s*[a-zA-Z]*")
    cleaned = [re.sub(pattern, '', ing).strip().lower() for ing in raw_ingredients]
    return ' '.join(cleaned)

def recommend_tfidf(user_ingredients, top_k=10):
    """Recommend recipes using TF-IDF and cosine similarity"""
    query = clean_ingredients(user_ingredients)
    user_vec = tfidf_vectorizer.transform([query])
    similarities = cosine_similarity(user_vec, tfidf_matrix).flatten()
    top_indices = similarities.argsort()[::-1][:top_k]
    return df.iloc[top_indices][['title', 'ingredients', 'directions', 'link']]

@app.route('/recommend', methods=['POST', 'OPTIONS'])
def recommend():
    if request.method == 'OPTIONS':
        response = jsonify({"status": "ok"})
        response.headers.add("Access-Control-Allow-Headers", "bypass-tunnel-reminder, content-type")
        return response
    
    try:
        data = request.get_json()
        user_ingredients = data.get('ingredients', [])
        print("Received ingredients:", user_ingredients)
        
        # Validate input is an array with at least one non-empty string
        if not isinstance(user_ingredients, list) or not user_ingredients or not any(ing.strip() for ing in user_ingredients):
            return jsonify({"error": "Please provide at least one valid ingredient"}), 400
            
        # Get top 10 recommendations
        recommendations = recommend_tfidf(user_ingredients, top_k=10)
        
        # Convert to list of dictionaries (maintaining order)
        results = []
        for _, row in recommendations.iterrows():
            results.append({
                'title': row['title'],
                'ingredients': row['ingredients'],
                'directions': row['directions'],
                'link': row['link']
            })
        
        return jsonify(results)
        
    except Exception as e:
        print("Error in recommendation:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
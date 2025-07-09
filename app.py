from flask import Flask, render_template, request, jsonify
from src.preprocess import preprocess_products, vectorize
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

app = Flask(__name__)

# Sample product dataset (same as main.py)
PRODUCTS = [
    # 👗 Female – Party
    {"name": "Sequin Dress", "category": "dress", "gender": "female", "occasion": "party"},
    {"name": "Off-shoulder Top", "category": "top", "gender": "female", "occasion": "party"},
    {"name": "Mini Skirt", "category": "skirt", "gender": "female", "occasion": "party"},
    {"name": "Party Heels", "category": "shoes", "gender": "female", "occasion": "party"},
    {"name": "Shimmer Bag", "category": "bag", "gender": "female", "occasion": "party"},

    # 👗 Female – Business
    {"name": "Formal Blazer", "category": "blazer", "gender": "female", "occasion": "business"},
    {"name": "Silk Blouse", "category": "top", "gender": "female", "occasion": "business"},
    {"name": "Tailored Pants", "category": "pants", "gender": "female", "occasion": "business"},
    {"name": "Business Heels", "category": "shoes", "gender": "female", "occasion": "business"},
    {"name": "Work Tote Bag", "category": "bag", "gender": "female", "occasion": "business"},

    # 👩 Female – Work
    {"name": "Linen Shirt", "category": "shirt", "gender": "female", "occasion": "work"},
    {"name": "Flat Loafers", "category": "shoes", "gender": "female", "occasion": "work"},
    {"name": "Pencil Skirt", "category": "skirt", "gender": "female", "occasion": "work"},
    {"name": "Canvas Backpack", "category": "bag", "gender": "female", "occasion": "work"},

    # 👩 Female – Casual
    {"name": "Graphic Tee", "category": "tshirt", "gender": "female", "occasion": "casual"},
    {"name": "Mom Jeans", "category": "jeans", "gender": "female", "occasion": "casual"},
    {"name": "Sneakers", "category": "shoes", "gender": "female", "occasion": "casual"},
    {"name": "Oversized Hoodie", "category": "hoodie", "gender": "female", "occasion": "casual"},

    # 👔 Male – Party
    {"name": "Black Shirt", "category": "shirt", "gender": "male", "occasion": "party"},
    {"name": "Fitted Trousers", "category": "pants", "gender": "male", "occasion": "party"},
    {"name": "Shiny Loafers", "category": "shoes", "gender": "male", "occasion": "party"},
    {"name": "Chain Necklace", "category": "accessory", "gender": "male", "occasion": "party"},

    # 👔 Male – Business
    {"name": "Slim Blazer", "category": "blazer", "gender": "male", "occasion": "business"},
    {"name": "White Oxford Shirt", "category": "shirt", "gender": "male", "occasion": "business"},
    {"name": "Formal Trousers", "category": "pants", "gender": "male", "occasion": "business"},
    {"name": "Oxford Shoes", "category": "shoes", "gender": "male", "occasion": "business"},
    {"name": "Leather Belt", "category": "accessory", "gender": "male", "occasion": "business"},

    # 👕 Male – Work
    {"name": "Polo T-Shirt", "category": "tshirt", "gender": "male", "occasion": "work"},
    {"name": "Chino Pants", "category": "pants", "gender": "male", "occasion": "work"},
    {"name": "Comfy Sneakers", "category": "shoes", "gender": "male", "occasion": "work"},
    {"name": "Tech Backpack", "category": "bag", "gender": "male", "occasion": "work"},

    # 👕 Male – Casual
    {"name": "Oversized Tee", "category": "tshirt", "gender": "male", "occasion": "casual"},
    {"name": "Joggers", "category": "pants", "gender": "male", "occasion": "casual"},
    {"name": "Slip-on Shoes", "category": "shoes", "gender": "male", "occasion": "casual"},
    {"name": "Baseball Cap", "category": "accessory", "gender": "male", "occasion": "casual"},
]

# 🔍 Recommend similar products
def recommend(df, vectors, item_index, top_n=4):
    similarities = cosine_similarity(vectors[item_index], vectors).flatten()
    similar_indices = np.argsort(similarities)[::-1][1:top_n + 1]
    return df.iloc[similar_indices]

# 🧠 Stylist-style descriptions
DESCRIPTIONS = {
    "dress": "Flowy and fierce, perfect for bold nights.",
    "top": "Soft on the skin, styled for spotlight.",
    "skirt": "A bold piece for your party nights.",
    "shoes": "Because your steps should speak too.",
    "bag": "Add a sparkle to your outfit.",
    "blazer": "Sleek power in every stitch.",
    "pants": "Tailored comfort for real moves.",
    "hoodie": "Chic + cozy = unstoppable.",
    "tshirt": "Simple. Smart. Effortless.",
    "jacket": "Layer up with edge.",
    "accessory": "Details that do the talking.",
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/recommendations', methods=['POST'])
def get_recommendations():
    data = request.get_json()
    gender = data.get('gender')
    occasion = data.get('occasion')
    selected_item = data.get('selected_item')
    
    # Filter products
    filtered = [p for p in PRODUCTS if p['gender'] == gender and p['occasion'] == occasion]
    
    if not filtered:
        return jsonify({'error': 'No matching products found'})
    
    # Process and get recommendations
    df = preprocess_products(filtered)
    vectors, _ = vectorize(df)
    
    # Find selected item index
    item_df = df[df['name'] == selected_item]
    if item_df.empty:
        return jsonify({'error': 'Selected item not found'})
    
    index = item_df.index[0]
    recs = recommend(df.reset_index(), vectors, index)
    
    # Format recommendations
    recommendations = []
    for _, row in recs.iterrows():
        desc = DESCRIPTIONS.get(row['category'], "Timeless and versatile.")
        recommendations.append({
            'name': row['name'],
            'category': row['category'],
            'description': desc
        })
    
    return jsonify({'recommendations': recommendations})

@app.route('/api/products', methods=['GET'])
def get_products():
    gender = request.args.get('gender')
    occasion = request.args.get('occasion')
    
    if gender and occasion:
        filtered = [p for p in PRODUCTS if p['gender'] == gender and p['occasion'] == occasion]
    else:
        filtered = PRODUCTS
    
    return jsonify({'products': filtered})

if __name__ == '__main__':
    app.run(debug=True) 
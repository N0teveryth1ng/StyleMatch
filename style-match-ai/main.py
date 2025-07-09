# from src.data_fetcher import fetch_hm_products
from src.preprocess import preprocess_products, vectorize
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def recommend(df, vectors, item_index, top_n=5):
    similarities = cosine_similarity(vectors[item_index], vectors).flatten()
    similar_indices = np.argsort(similarities)[::-1][1:top_n + 1]
    return df.iloc[similar_indices]

if __name__ == "__main__":
    print("📦 Loading product data...\n")

    data = [
    # 🔵 Male - Business
    {"name": "Slim Fit Shirt", "category": "shirt", "gender": "male", "occasion": "business"},
    {"name": "Formal Blazer", "category": "blazer", "gender": "male", "occasion": "business"},
    {"name": "Oxford Shirt", "category": "shirt", "gender": "male", "occasion": "business"},
    {"name": "Business Pants", "category": "pants", "gender": "male", "occasion": "business"},
    {"name": "Dress Shoes", "category": "shoes", "gender": "male", "occasion": "business"},

    # 🔵 Male - Party
    {"name": "Sequin Blazer", "category": "blazer", "gender": "male", "occasion": "party"},
    {"name": "Velvet Turtleneck", "category": "top", "gender": "male", "occasion": "party"},
    {"name": "Leather Pants", "category": "pants", "gender": "male", "occasion": "party"},
    {"name": "Party Loafers", "category": "shoes", "gender": "male", "occasion": "party"},
    {"name": "Silk Shirt", "category": "shirt", "gender": "male", "occasion": "party"},

    # 🔵 Male - Work
    {"name": "Casual Denim Shirt", "category": "shirt", "gender": "male", "occasion": "work"},
    {"name": "Tech Jacket", "category": "jacket", "gender": "male", "occasion": "work"},
    {"name": "Commuter Backpack", "category": "bag", "gender": "male", "occasion": "work"},
    {"name": "Slim Chinos", "category": "pants", "gender": "male", "occasion": "work"},
    {"name": "Work Sneakers", "category": "shoes", "gender": "male", "occasion": "work"},

    # 🔵 Male - Casual
    {"name": "Graphic Tee", "category": "tshirt", "gender": "male", "occasion": "casual"},
    {"name": "Relaxed Hoodie", "category": "hoodie", "gender": "male", "occasion": "casual"},
    {"name": "Joggers", "category": "pants", "gender": "male", "occasion": "casual"},
    {"name": "Cap", "category": "accessory", "gender": "male", "occasion": "casual"},
    {"name": "Slip-On Sneakers", "category": "shoes", "gender": "male", "occasion": "casual"},

    # 🔴 Female - Business
    {"name": "Formal Blazer", "category": "blazer", "gender": "female", "occasion": "business"},
    {"name": "Silk Blouse", "category": "top", "gender": "female", "occasion": "business"},
    {"name": "Tailored Pants", "category": "pants", "gender": "female", "occasion": "business"},
    {"name": "Business Heels", "category": "shoes", "gender": "female", "occasion": "business"},
    {"name": "Work Tote Bag", "category": "bag", "gender": "female", "occasion": "business"},

    # 🔴 Female - Party
    {"name": "Sequin Dress", "category": "dress", "gender": "female", "occasion": "party"},
    {"name": "Off-shoulder Top", "category": "top", "gender": "female", "occasion": "party"},
    {"name": "Mini Skirt", "category": "skirt", "gender": "female", "occasion": "party"},
    {"name": "Party Heels", "category": "shoes", "gender": "female", "occasion": "party"},
    {"name": "Shimmer Bag", "category": "bag", "gender": "female", "occasion": "party"},

    # 🔴 Female - Work
    {"name": "Smart Shirt", "category": "shirt", "gender": "female", "occasion": "work"},
    {"name": "Midi Skirt", "category": "skirt", "gender": "female", "occasion": "work"},
    {"name": "Work Pumps", "category": "shoes", "gender": "female", "occasion": "work"},
    {"name": "Structured Blazer", "category": "blazer", "gender": "female", "occasion": "work"},
    {"name": "Laptop Bag", "category": "bag", "gender": "female", "occasion": "work"},

    # 🔴 Female - Casual
    {"name": "Relaxed T-shirt", "category": "tshirt", "gender": "female", "occasion": "casual"},
    {"name": "Boyfriend Jeans", "category": "pants", "gender": "female", "occasion": "casual"},
    {"name": "Sneakers", "category": "shoes", "gender": "female", "occasion": "casual"},
    {"name": "Crossbody Bag", "category": "bag", "gender": "female", "occasion": "casual"},
    {"name": "Oversized Hoodie", "category": "hoodie", "gender": "female", "occasion": "casual"},
]


    df = preprocess_products(data)

    # 🔍 Ask user preference
    user_gender = input("Enter your gender (male/female): ").strip().lower()
    user_occasion = input("Enter the occasion (party/business/work/casual): ").strip().lower()

    # 🎯 Filter products
    filtered_df = df[
        (df['gender'] == user_gender) &
        (df['occasion'] == user_occasion)
    ]

    if filtered_df.empty:
        print("\n❌ No products found for your selected gender and occasion.")
        exit()

    print("\n🧾 Matching Products:")
    for i, row in filtered_df.reset_index().iterrows():
        print(f"{i}: {row['name']} ({row['category']})")

    try:
        index = int(input(f"\nEnter the number of a product you like (0 to {len(filtered_df)-1}): "))
        if index < 0 or index >= len(filtered_df):
            raise IndexError
    except:
        print("❌ Invalid input. Please enter a valid number.")
        exit()

    vectors, _ = vectorize(filtered_df)
    recs = recommend(filtered_df.reset_index(), vectors, index)

    print(f"\n✅ Recommendations similar to: {filtered_df.iloc[index]['name']}\n")
    for _, row in recs.iterrows():
        print(f"- {row['name']} | Category: {row['category']}")

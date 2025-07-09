from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd

def preprocess_products(products):
    df = pd.DataFrame(products)

    # Combine product name and category
    df['combined'] = (
    df['name'].fillna('') + " " +
    df['category'].fillna('') + " " +
    df['gender'].fillna('') + " " +
    df['occasion'].fillna('')
)


    return df

def vectorize(df):
    vectorizer = CountVectorizer(stop_words='english')
    vectors = vectorizer.fit_transform(df['combined'])
    return vectors, vectorizer


if __name__ == "__main__":
    from data_fetcher import fetch_hm_products

    data = fetch_hm_products(pages=1)
    df = preprocess_products(data)
    vectors, vectorizer = vectorize(df)

    print("✅ Preprocessing complete")
    print("Sample features:", vectorizer.get_feature_names_out()[:10])
    print("Vector shape:", vectors.shape)

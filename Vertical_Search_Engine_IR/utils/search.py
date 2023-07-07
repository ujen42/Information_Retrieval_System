
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from utils.wordprocess import WordProcess

from config.dbconfig import db
from models.models import Paper

class Search():
    
    def __init__(self, query):
        self.query = query

    def search(self):
        wp = WordProcess()
        vectorizer = TfidfVectorizer()
        df = wp.preprocess_df()
        tfidf_matrix = vectorizer.fit_transform(df['title'].to_numpy())
        preprocessed_query = wp.preprocess_text(self.query)
        query_tfidf = vectorizer.transform([preprocessed_query])
        similarities = cosine_similarity(query_tfidf, tfidf_matrix, dense_output=True).flatten()
        indices = similarities.argsort()[::-1]
        results = df.loc[indices]
        data_list = []
        for idx, (_, row) in enumerate(results.iterrows()):
            if(similarities[indices[idx]] > 0):
                paper = Paper.query.filter(Paper.id == row['id']).first()
                data_dict = {
                    'id': row['id'], 
                    'title': paper.title, 
                    'link':paper.link, 
                    'published_date':paper.published_date, 
                    'score': similarities[indices[idx]],
                    'authors': paper.authors
                }
                data_list.append(data_dict)
        return data_list





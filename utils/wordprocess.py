
import string
import nltk
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('punkt')
from nltk import pos_tag
from nltk.corpus import wordnet
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import pandas as pd
from models.models import Paper

class WordProcess():

    def __init__(self):
        self.sw = stopwords.words("english")
        self.lemmatizer = WordNetLemmatizer()
    
    def get_raw_df(self):
        '''
            fetch all publications from database
            and returns dataframe
        '''
        result = Paper.query.all()
        columns = result[0].__table__.columns.keys()
        data = [r.__dict__ for r in result]
        df = pd.DataFrame.from_records(data, columns=columns)
        return df
    
    def get_wordnet_pos(self, word):
        """
            Map POS tag from NLTK to WordNet POS tag.
            Args:
            - word (str): The word for which the POS tag needs to be determined.
            Returns:
            - wordnet_pos (str): The WordNet POS tag corresponding to the input word.
        """
        pos_tagged = pos_tag([word])[0]
        tag = pos_tagged[1][0].upper()
        tag_mapping = {"V": wordnet.VERB, "R": wordnet.ADV, "N": wordnet.NOUN, "J": wordnet.ADJ}
        return tag_mapping.get(tag, wordnet.NOUN)
    
    def lemmatize_text(self, text):
        """
            Lemmatize the input text by removing stopwords and performing lemmatization.
            Args:
            - text (str): The text to be lemmatized.
            Returns:
            - lemmatized_text (str): The lemmatized version of the input text.
        """
        word_tokens = nltk.word_tokenize(text)
        stop_words = set(stopwords.words("english"))
        lemmatizer = WordNetLemmatizer()
        
        lemmatized_text = ""
        for word in word_tokens:
            if word not in stop_words:
                pos_tag = self.get_wordnet_pos(word)
                lemmatized_word = lemmatizer.lemmatize(word, pos_tag)
                lemmatized_text += lemmatized_word + " "
        
        return lemmatized_text
    
    def preprocess_text(self, text):
        """
            Preprocess the input text by converting to lowercase, removing punctuation, and lemmatizing.
            Args:
            - text (str): The text to be preprocessed.
            Returns:
            - preprocessed_text (str): The preprocessed version of the input text.
        """
        text = text.lower()   # Convert to lowercase
        text = text.translate(str.maketrans('', '', string.punctuation))   # Remove punctuation marks
        preprocessed_text = self.lemmatize_text(text)
        return preprocessed_text
    
    def preprocess_df(self):
        """
            Preprocesses the raw DataFrame by applying text preprocessing and dropping unnecessary columns.
            Returns:
            - preprocessed_df (pandas.DataFrame): The preprocessed DataFrame with the 'title' column modified and specified columns dropped.
        """
        df = self.get_raw_df()
        df['title'] = df['title'].apply(self.preprocess_text)
        df = df.drop(['link', 'published_date'], axis=1)
        return df
    

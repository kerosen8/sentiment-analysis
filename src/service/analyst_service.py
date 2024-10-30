import os
import nltk
import joblib
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from scipy.special import softmax
from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification

# Download necessary NLTK datasets and load sentiment analysis and text classification models

nltk.download('wordnet')
nltk.download('punkt_tab')
nltk.download('stopwords')

SENTIMENT_MODEL_REFERENCE = f"cardiffnlp/twitter-roberta-base-sentiment"
sentiment_tokenizer = AutoTokenizer.from_pretrained(SENTIMENT_MODEL_REFERENCE)
sentiment_model = AutoModelForSequenceClassification.from_pretrained(SENTIMENT_MODEL_REFERENCE)

unexpected_text_classifier_model = joblib.load(os.path.join(os.path.dirname(__file__), '..', 'models', 'text_classifiers','unexpected_classifier_model.pkl'))
unexpected_text__classifier_vectorizer = joblib.load(os.path.join(os.path.dirname(__file__), '..', 'models', 'text_classifiers', 'unexpected_classifier_vectorizer.pkl'))

text_classifier_model = joblib.load(os.path.join(os.path.dirname(__file__), '..', 'models', 'text_classifiers', 'text_classifier_model.pkl'))
text_classifier_vectorizer =  joblib.load(os.path.join(os.path.dirname(__file__), '..', 'models', 'text_classifiers', 'text_classifier_vectorizer.pkl'))

class AnalystService():
        
    def __tokenize(self, text):
        """
        This method converts monolithic text into tokens for further processing
        return: string array
        """
        word_tokens = word_tokenize(text)
        return word_tokens
    
    def __token_filter(self, tokens):
        """
        This method uses nltk.stopwords to filter out noise in the data 
        returns: string
        """
        excluded_stop_words = ['not']
        stop_words = set(stopwords.words('english'))
        filtered_tokens = ' '.join([word for word in tokens if not word in stop_words or word in excluded_stop_words])
        return filtered_tokens
    
    def __lemmatize(self, text):
        """
        This method lemmatizes the input text, converting words to their base form 
        returns: string
        """
        lemmatizer = WordNetLemmatizer()
        lemmatized_text = ''.join([lemmatizer.lemmatize(word) for word in text])
        print(lemmatized_text)
        return lemmatized_text
    
    def __prepare_text(self, text):
        """
        Prepares the input text by tokenizing, filtering, and lemmatizing it
        returns: string
        """
        tokenized_text = self.__tokenize(text)
        filtered_text = self.__token_filter(tokenized_text)
        lemmatized_text = self.__lemmatize(filtered_text)
        return lemmatized_text
    
    def sentiment(self, text):
        """    
        Analyzes the sentiment of the input text and classifies it as negative, neutral, or positive
        returns: 'neutral' | 'negative' | 'positive'
        """
        encoded_text = sentiment_tokenizer(self.__prepare_text(text), return_tensors='pt')
        output = sentiment_model(**encoded_text)

        scores = output[0][0].detach().numpy()
        scores = softmax(scores)
                
        if scores[1] > 0.33:
            return 'neutral'
        if scores[0] == max(scores):
            return 'negative'
        if scores[1] == max(scores):
            return 'neutral'
        if scores[2] == max(scores):
            return 'positive'

    def unexpected_text_classifier(self, text):
        """
        Classifies the input text as unexpected or not using a pre-trained model
        returns: 'expected' | 'unexpected'
        """
        vectorizer = unexpected_text__classifier_vectorizer.transform([text])
        prediction = unexpected_text_classifier_model.predict(vectorizer)
        return prediction[0]
    
    def message_classifier(self, text):
        """
        Classifies the input text using a pre-trained text classification model.
        returns: 'greetings' | 'farewell' | 'question'
        """
        vectorizer = text_classifier_vectorizer.transform([text])
        prediction = text_classifier_model.predict(vectorizer)
        return prediction[0]
    
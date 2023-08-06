from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import string
import joblib
import pathlib
import nltk

nltk.download('omw-1.4')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

_stopwords = set(stopwords.words('english'))
_lemmatizer =  WordNetLemmatizer()


def tokenize(doc:str):
    return [_lemmatizer.lemmatize(tkn) for tkn in \
            word_tokenize(doc.translate(str.maketrans(' ', ' ', string.punctuation)).lower())\
            if not (tkn in _stopwords or is_link_or_at(tkn))] 

def is_link_or_at(token:str):
    return token[0] == '@' or token[:7] == 'https:/'

class Filter:
    error_message= "This method must be overwritten"
    def __init__(self,model_name) -> None:
        self.model_name= model_name
        self.accuracy = None 
        folder= str(pathlib.Path(__file__).parent.resolve())
        self.vectorizer = joblib.load(folder+"/models/vectorizer_%s.sav"%self.model_name)
        self.model= joblib.load(folder+"/models/%s.sav"%self.model_name)

    def __call__(self, *messages):
        vectors = self.vectorizer.transform(messages)
        prediction = self.model.predict(vectors)
        return dict(zip(messages, map(bool, prediction)))

     
class Vectorizer:
    def __init__(self) -> None:
        self.tfidf = TfidfVectorizer(tokenizer=tokenize)
        self.svd = TruncatedSVD(n_components= 10)    

    def fit_transform(self, docs):
        X = self.tfidf.fit_transform(docs)
        vals = self.svd.fit_transform(X)
        return vals

    def transform(self, docs):
        X = self.tfidf.transform(docs)
        vals = self.svd.transform(X)
        return vals


class BayesianFilter(Filter):
    def __init__(self, model_name) -> None:
        super().__init__("bayesian_"+model_name)

class RandomForestFilter(Filter):
    def __init__(self, model_name) -> None:
        super().__init__("decision_"+model_name,)              

class BayesianSexualContentFilter(BayesianFilter):
    def __init__(self) -> None:
        super().__init__(model_name="sexual_content_filter")

class SexualContentFilter(RandomForestFilter):
    def __init__(self) -> None:
        super().__init__(model_name="sexual_content_filter")

class BayesianRacismFilter(BayesianFilter):
    def __init__(self) -> None:
        super().__init__("racism_filter")

class RacismFilter(RandomForestFilter):
    def __init__(self) -> None:
        super().__init__("racism_filter")

class BayesianSexismFilter(BayesianFilter):
    def __init__(self) -> None:
        super().__init__("sexism_filter")

class SexismFilter(RandomForestFilter):
    def __init__(self) -> None:
        super().__init__("sexism_filter")
    
class BayesianCyberBullyingFilter(BayesianFilter):
    def __init__(self) -> None:
        super().__init__("cyberbullying_filter")

class CyberBullyingFilter(RandomForestFilter):
    def __init__(self) -> None:
        super().__init__("cyberbullying_filter")


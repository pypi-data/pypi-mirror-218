import re
from sklearn.feature_extraction.text import TfidfVectorizer 
import pickle

# load the vectorizer and the model
vectorizer = pickle.load(open("models/vectorizer.pkl", "rb"))
model = pickle.load(open("models/svm_model.pkl", "rb"))

def clean_txt(input_str):
    try:
        if input_str: # if the input string is not empty do the following
            # Remove some of special chars
            input_str = re.sub('[?؟!@#$%&*+~\/=><]+^' , '' , input_str) 
            # Remove all non-Arabic and non-digit chars
            input_str = re.sub(r'[^0-9\u0600-\u06ff\u0750-\u077f\ufb50-\ufbc1\ufbd3-\ufd3f\ufd50-\ufd8f\ufd50-\ufd8f\ufe70-\ufefc\uFDF0-\uFDFD]+', ' ', input_str)
            # Remove all spaces
            input_str = re.sub('[\\s]+'," ",input_str) 
            # Remove underscore and Arabic tatwelah
            input_str = input_str.replace("_" , ' ').replace("ـ" , '') 
            # Remove punctuation marks
            input_str = input_str.translate(str.maketrans('', '', '"\'.,:'))
            # Remove text between parentheses
            input_str = re.sub(r" ?\([^)]+\)", "", str(input_str))  
            # Strip diacritics and whitespace
            input_str = strip_diacritics(input_str).strip() 
    except:
        return input_str
    return input_str

def check_text(text: str) -> None:
    # transform the text into features using the vectorizer
    features = vectorizer.transform([clean_txt(text)])
    
    # predict the label using the model
    label = model.predict(features)[0]
    
    # if the label is 1 (bad), censor the text and print it
    return label

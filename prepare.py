import re
import unicodedata
import nltk
from nltk.tokenize import ToktokTokenizer
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords


def basic_clean(text):
    """
    Apply basic text cleaning to the input string.
    
    This function performs the following steps:
    - Lowercase the text.
    - Normalize unicode characters.
    - Replace characters that are not letters, numbers, whitespace, or single quotes.
    
    Parameters:
    - text: The input text to be cleaned.
    
    Returns:
    Cleaned text after applying the basic cleaning operations.
    """
    # Lowercase the text
    text = text.lower()
    
    # Normalize unicode characters
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    
    #Replace any characters that are not letters, numbers, spaces, or single quotes.

    text = re.sub(r"[^a-z0-9'\s]", '', text)
    return text

def tokenize(text):
    """
    Tokenize words in the input string.
    
    This function tokenizes the input text into individual words.
    
    Parameters:
    - text: The input text to be tokenized.
    
    Returns:
    A list of tokenized words.
    """
    tokenizer = ToktokTokenizer()
    tokens = tokenizer.tokenize(text)
    return tokens

def stem(text):
    """
    Apply stemming to words in the input text.
    
    This function applies stemming to each word in the input text using the Porter Stemmer algorithm.
    
    Parameters:
    - text: The input text to apply stemming to.
    
    Returns:
    Text with words after stemming.
    """
    stemmer = PorterStemmer()
    stemmed_words = [stemmer.stem(word) for word in nltk.word_tokenize(text)]
    stemmed_text = ' '.join(stemmed_words)
    return stemmed_text

def lemmatize(text):
    """
    Apply lemmatization to words in the input text.
    
    This function applies lemmatization to each word in the input text using the WordNet Lemmatizer.
    
    Parameters:
    - text: The input text to apply lemmatization to.
    
    Returns:
    Text with words after lemmatization.
    """
    lemmatizer = nltk.stem.WordNetLemmatizer()
    lemmatized_words = [lemmatizer.lemmatize(word) for word in nltk.word_tokenize(text)]
    lemmatized_text = ' '.join(lemmatized_words)
    return lemmatized_text


def remove_stopwords(text, extra_words=None, exclude_words=None):
    """
    Remove stopwords from the input text.
    
    Parameters:
    - text (str): The input text to remove stopwords from.
    - extra_words (list): List of additional words to include as stopwords.
    - exclude_words (list): List of words not to be removed.
    
    Returns:
    str: Text with stopwords removed.
    """
    # Load the stopwords list from the NLTK library
    stopword_list = set(stopwords.words('english'))
    
    # Add extra words to the stopwords list if provided
    if extra_words:
        stopword_list.update(extra_words)
        
    # Remove excluded words from the stopwords list if provided
    if exclude_words:
        stopword_list.difference_update(exclude_words)
        
    # Tokenize the input text into individual words
    words = nltk.word_tokenize(text)
    
    # Filter out words that are in the stopwords list
    filtered_words = [word for word in words if word.lower() not in stopword_list]
    
    # Reconstruct the filtered words into a text string
    filtered_text = ' '.join(filtered_words)
    
    return filtered_text

# def add_cleaned_columns(df, column):
#     """Add cleaned and processed columns to the input DataFrame.
    
#     This function adds cleaned and processed columns to the input DataFrame.
    
#     Parameters:
#     - df: DataFrame containing the text data.
#     - column: Name of the column containing the text to be processed.
    
#     Returns:
#     DataFrame with added 'clean', 'stemmed', and 'lemmatized' columns.
#     """
#     df['clean'] = df[column].apply(lambda x: remove_stopwords(stem(basic_clean(' '.join(tokenize(x))))))
#     df['stemmed'] = df['clean'].apply(stem)
#     df['lemmatized'] = df['clean'].apply(lemmatize)
#     return df

def add_cleaned_columns(df, column):
    """
    Add cleaned and processed columns to the input DataFrame.
    
    This function adds 'clean', 'stemmed', and 'lemmatized' columns to the input DataFrame.
    
    Parameters:
    - df: DataFrame containing the text data.
    - column: Name of the column containing the text to be processed.
    
    Returns:
    DataFrame with added columns for cleaned, stemmed, and lemmatized text.
    """
    df['clean'] = df[column].apply(lambda x: lemmatize(stem(remove_stopwords(basic_clean(' '.join(tokenize(x)))))))
    return df

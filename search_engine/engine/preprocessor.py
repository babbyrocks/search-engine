import string



# Stopwords - common words that add no value to the search

STOPWORDS = {
    "a", "an", "the", "is", "it", "in", "on", "at", "to", "of", "and", "or", "but", "not", "with", "this", "that", "was", "are", "be", "as", "by", "from", "has", "had", "have", "will", "do", "did", "its", "we", "he", "she", "they", "you", "i", "them"
}


def preprocess(text: str) -> list[str]:
    #cleans and tokenizes a string into a list of useful words

    text = text.lower()

    #remove punctuation using string.translate, deletes punctuatons, O(n) on the text length
    text = ''.join(char for char in text if char.isalnum() or char.isspace)

    #split string into individual words by tokenizng it
    tokens = text.split()

    #filtering out stopwords
    tokens = [word for word in tokens if word not in STOPWORDS]

    return tokens



if __name__ == "__main__":

    sample = "The quick brown fox jumps over the lazy dog!"
    print(preprocess(sample))
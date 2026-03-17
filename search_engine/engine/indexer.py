from engine.preprocessor import preprocess
from engine.ranker import rank_results

def build_index(documents: dict) -> dict:
    #building inverted index from documents
    # Input:
    #     docments = {
    #         "doc1.txt": ["python", "great", "programming"],
    #         "doc2.txt": ["python", "great", "programming"],
    #     }

    # Output:
    #     index = {
    #         "python": {"doc1.txt": 1, "doc2.txt": 1},
    #         "great": {"doc1.txt": 1},
    #     }

        #dictionary
        index = {}

        for doc_name, words in documents.items():
            for word in words:
                if word not in index:
                    index[word] = {} #new word, empty dict
                if doc_name not in index[word]:
                    index[word][doc_name] = 0
                index[word][doc_name] += 1
        return index


def search(index: dict, query:str) -> dict:
    query = query.lower()
    if query not in index:
        return {}
    results = index[query]
    ranked = dict(sorted(results.items(), key=lambda x: x[1], reverse=True))
    return ranked


def search_query(index: dict, query:str) -> dict:
    words = preprocess(query)
    scores = {}
    for word in words:
        if word in index:
            for doc, freq in index[word].items():
                if doc not in scores:
                    scores[doc] = 0
                scores[doc] += freq
    
    return rank_results(scores)




#test

documents = {
    "doc1.txt": preprocess("Python is a great programming language. Python is easy."),
    "doc2.txt": preprocess("Search engines use Python to index documents."),
    "doc3.txt": preprocess("Data structures like dictionaries help build search engines.")
}

index = build_index(documents)

print("Search 'python':", search(index, "python"))
print("Search 'search':", search(index, "search"))
print("Search 'java':",   search(index, "java"))




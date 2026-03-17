
# ✨ DocSearch
### A Python-based Document Search Engine
> Data Structures & Algorithms Project — KNUST

---

## 📖 Overview

**DocSearch** is a text-based search engine built entirely in Python. It indexes multiple documents (`.txt`, `.md`, `.pdf`) and lets users search through them using keywords, with results ranked by frequency of occurrence.

The engine is powered by core DSA concepts:
- **Dictionary** — inverted index for O(1) keyword lookups
- **Set** — stopword filtering in O(1)
- **List** — token storage and ranked results

The UI is built with **Streamlit**, styled with custom HTML/CSS for a clean, modern look with automatic dark/light mode.

---

## ✅ Features

- 📂 Load and index `.txt`, `.md`, and `.pdf` files
- ⚡ O(1) average keyword lookup via inverted index
- 🔍 Multi-word query support with combined frequency scoring
- 📊 Results ranked by relevance (frequency count)
- 🖊️ Keyword highlighting in result snippets
- 🌙 Automatic dark/light mode detection
- 🎨 Smooth animations — card fade-in, hover effects, search bar glow

---

## 📁 Project Structure

```
search_engine/
│
├── app.py                  # Streamlit UI
├── engine/
│   ├── preprocessor.py     # Text cleaning & tokenization
│   ├── indexer.py          # Inverted index + search
│   ├── ranker.py           # Result sorting
│   └── loader.py           # Document loading
└── documents/              # Your .txt / .pdf files
```

---

## 🗂 Data Structures

| Data Structure | How it's used |
|---|---|
| `Dictionary` | Inverted index — maps each word to the documents it appears in and its frequency. O(1) average lookup. |
| `Set` | Stopwords storage — O(1) membership check when filtering common words like "the", "is", "a". |
| `List` | Token storage after preprocessing, and ranked results returned as a sorted list of tuples. |

---

## ⚙️ Algorithms

| Algorithm | Details |
|---|---|
| String Matching | Keyword lookup in the inverted index using exact token matching after preprocessing. |
| Searching | Hash table lookup — O(1) average time complexity. |
| Basic Ranking | Results sorted by total frequency count using Python's Timsort — O(n log n). |

---

## 🚀 Installation & Setup

**1. Clone the repository**
```bash
git clone https://github.com/yourusername/search_engine.git
cd search_engine
```

**2. Install dependencies**
```bash
pip install streamlit pymupdf
```

**3. Add your documents**

Place your `.txt`, `.md`, or `.pdf` files in the `documents/` folder.

**4. Run the app**
```bash
python -m streamlit run app.py
```

The app will open automatically at `http://localhost:8501`

---

## 🔍 How It Works

```
Load documents → Preprocess text → Build inverted index → Search → Rank results
```

1. **Load** — `loader.py` reads all supported files from the `documents/` folder
2. **Preprocess** — `preprocessor.py` lowercases text, removes punctuation, and filters stopwords
3. **Index** — `indexer.py` builds an inverted index mapping words to documents and frequencies
4. **Search** — the user query is preprocessed then looked up in the index
5. **Rank** — `ranker.py` sorts results by combined frequency score, highest first

---

## 📦 Dependencies

- Python 3.12+
- `streamlit` — UI framework
- `pymupdf` — PDF text extraction

---

## 👤 Author

**Kwasi Asare-Boateng**
Kwame Nkrumah University of Science and Technology (KNUST)
Data Structures and Algorithms

---

> ✨ *Built with Python, DSA, and a lot of debugging.*

# 📘 Document Preprocessing using File Handling, Text Normalization, TextBlob, Lemmatization, and Recursive Chunking

This guide explains a complete preprocessing pipeline for preparing textual documents before using them in Natural Language Processing (NLP) applications such as Retrieval-Augmented Generation (RAG), Semantic Search, Question Answering, Sentiment Analysis, and Large Language Models (LLMs).

The pipeline begins with **file handling** to read the document, followed by **text normalization**, **spelling correction**, **lemmatization**, and **recursive chunking**.

---

# Workflow

```text
Load Documents (File Handling)
            ↓
Read File Content
            ↓
Convert to Lowercase
            ↓
Handle Emojis
            ↓
Expand Contractions
            ↓
Remove Punctuation
            ↓
Remove Special Characters
            ↓
Remove Extra Spaces
            ↓
Correct Spelling (TextBlob)
            ↓
Tokenization
            ↓
Combine Tokens
            ↓
Lemmatization (SpaCy)
            ↓
Recursive Chunking
            ↓
Print List of Chunks
```

---

# Step 1: File Handling

## Explanation

File handling is the process of reading and writing files. In NLP, documents are commonly stored as TXT, PDF, DOCX, CSV, or database records.

Use UTF-8 encoding to correctly read Unicode characters such as emojis.

## Syntax

```python
open(file_name, mode, encoding)
```

## Common File Modes

| Mode | Purpose |
|------|---------|
| `r` | Read |
| `w` | Write (overwrite/create) |
| `a` | Append |
| `r+` | Read and Write |
| `rb` | Read Binary |
| `wb` | Write Binary |

## Code

```python
with open("sample.txt", "r", encoding="utf-8") as file:
    text = file.read()

print(text)
```

---

# Step 2: Text Normalization

Text normalization converts raw text into a clean and consistent format.

Typical operations include:

- Lowercase conversion
- Emoji handling
- Contraction expansion
- Removing punctuation
- Removing special characters
- Removing extra spaces
- Spelling correction
- Tokenization

---

## Step 2.1 Convert to Lowercase

```python
text = text.lower()
```

---

## Step 2.2 Handle Emojis

Emoji preprocessing depends on the NLP task.

### Option 1: General NLP Tasks (Recommended)

For RAG, embeddings, semantic search, chunking, document retrieval, and question answering, emojis generally do not contribute meaningful information. Remove them using:

```python
import emoji

text = emoji.replace_emoji(text, replace="")
```

Example

```
I love Python 😊🚀
```

becomes

```
I love Python
```

### Option 2: Sentiment Analysis

For sentiment analysis, emojis contain emotional information and should be preserved by converting them into descriptive text.

```python
import emoji

text = emoji.demojize(text)
```

Example

```
😊
```

becomes

```
:smiling_face_with_smiling_eyes:
```

---

## Step 2.3 Expand Contractions

```python
import contractions

text = contractions.fix(text)
```

Example:

```
can't → cannot
I'm → I am
it's → it is
```

---

## Step 2.4 Remove Punctuation

```python
import string

text = "".join(char for char in text if char not in string.punctuation)
```

---

## Step 2.5 Remove Special Characters

```python
text = "".join(
    char if char.isalnum() or char.isspace() else " "
    for char in text
)
```

---

## Step 2.6 Remove Extra Spaces

```python
text = " ".join(text.split())
```

---

## Step 2.7 Correct Spelling using TextBlob

### Explanation

Real-world documents often contain spelling mistakes. TextBlob can automatically correct many common spelling errors before tokenization.

Install:

```python
pip install textblob
```

Download corpora:

```python
python -m textblob.download_corpora
```

Code:

```python
from textblob import TextBlob

text = str(TextBlob(text).correct())
```

Example

```
machne learnng is amazng
```

becomes

```
machine learning is amazing
```

---

## Step 2.8 Tokenization

```python
from nltk.tokenize import word_tokenize

tokens = word_tokenize(text)
```

Combine tokens back into a paragraph:

```python
normalized_text = " ".join(tokens)
```

---

# Step 3: Lemmatization using SpaCy

Install:

```python
pip install spacy
python -m spacy download en_core_web_sm
```

Code:

```python
import spacy

nlp = spacy.load("en_core_web_sm")

doc = nlp(normalized_text)

lemmatized_text = " ".join(token.lemma_ for token in doc)
```

---

# Step 4: Recursive Chunking

Install:

```python
pip install langchain
```

Code:

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

chunks = splitter.split_text(lemmatized_text)
```

The splitter recursively uses:

1. Paragraph (`\n\n`)
2. Line (`\n`)
3. Space (` `)
4. Character (`""`)

---

# Step 5: Print Chunks

```python
for i, chunk in enumerate(chunks, start=1):
    print(f"Chunk {i}")
    print(chunk)
    print("-"*80)
```

---

# Complete Pipeline

```python
import string
import emoji
import contractions
import spacy

from textblob import TextBlob
from nltk.tokenize import word_tokenize
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Read file
with open("sample.txt", "r", encoding="utf-8") as file:
    text = file.read()

# Lowercase
text = text.lower()

# Emoji handling
# General NLP
text = emoji.replace_emoji(text, replace="")

# For sentiment analysis instead use:
# text = emoji.demojize(text)

# Expand contractions
text = contractions.fix(text)

# Remove punctuation
text = "".join(c for c in text if c not in string.punctuation)

# Remove special characters
text = "".join(c if c.isalnum() or c.isspace() else " " for c in text)

# Remove extra spaces
text = " ".join(text.split())

# Correct spelling
text = str(TextBlob(text).correct())

# Tokenization
tokens = word_tokenize(text)
normalized_text = " ".join(tokens)

# Lemmatization
nlp = spacy.load("en_core_web_sm")
doc = nlp(normalized_text)
lemmatized_text = " ".join(token.lemma_ for token in doc)

# Recursive chunking
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

chunks = splitter.split_text(lemmatized_text)

# Print chunks
for i, chunk in enumerate(chunks, start=1):
    print(f"Chunk {i}")
    print(chunk)
    print("-"*80)
```

---

# Summary

| Step | Purpose |
|------|---------|
| File Handling | Read the document |
| Lowercase | Standardize case |
| Emoji Handling | Remove emojis for general NLP or convert to text for sentiment analysis |
| Expand Contractions | Replace contractions with full forms |
| Remove Punctuation | Remove punctuation symbols |
| Remove Special Characters | Keep only letters, digits, and spaces |
| Remove Extra Spaces | Normalize whitespace |
| TextBlob | Correct spelling mistakes |
| Tokenization | Split text into words |
| Combine Tokens | Create normalized paragraph |
| Lemmatization | Convert words to dictionary form |
| Recursive Chunking | Split text into overlapping chunks |
| Print Chunks | Display generated chunks |

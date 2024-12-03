# PDF Search Engine 📄🔍

A Python-based console application for searching content in PDF files. The search engine implements advanced algorithms and data structures, enabling efficient and accurate text retrieval. It supports keyword search, phrase search, and logical queries with proper evaluation using Reverse Polish Notation (RPN).

---

## 🌟 Features

- **Single/Multi-word Search**: Enter one or more keywords to retrieve relevant results.
- **Phrase Search**: Use quotation marks (`"`) for exact phrase searches.
- **Logical Operators**: Combine queries with `AND`, `OR`, and `NOT`, resolved using **Reverse Polish Notation (RPN)**.
- **Results Pagination**: Displays 10 results per page.
- **Highlighting Matches**: Marks up to 3 sections of relevant text per page for each result.
- **Efficiency**:
  - **PageRank**: Ranks results based on relevance.
  - **Caching**: Speeds up repeated queries.
  - **KMP Algorithm**: Ensures fast pattern matching.
  - **QuickSort**: Efficient sorting of results.
  - **Reverse Trie**: Optimized indexing for quick lookups.

---

## 🚀 Getting Started

### Prerequisites

- **Python**: Version 3.8 or later.
- Libraries:
  - `PyPDF2`: For PDF file processing.
  - `numpy` (optional): For additional performance optimization.

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/kize1509/PDF-Search-Engine.git

    Navigate to the project directory:

cd projeakt2



🔧 Usage
Adding PDFs

    Place your PDF files in the data/ folder. The engine will index these files when the program is started.

Running the Application

    Launch the search engine:

    python search_engine.py

Performing Searches

    Single Word:

search> basketball

Phrase (using quotes):

search> "Olympic basketball tournament"

Logical Query:

    search> basketball AND tournament NOT 2023

    The query is processed using Reverse Polish Notation for correct precedence.

    Indexing:
        PDFs are parsed using PyPDF2, and their content is tokenized and indexed.
        A Reverse Trie is built for fast search lookups.

    Search:
        Queries are parsed and normalized.
        Logical queries are converted to RPN to resolve precedence.
        KMP Algorithm is used for efficient pattern matching in indexed text.

    Ranking:
        Results are ranked using a custom PageRank implementation.
        Results are sorted using QuickSort for efficient display.

    Results Display:
        Results are paginated with 10 entries per page.
        Up to 3 matching text snippets are highlighted per document.

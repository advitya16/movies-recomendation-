 🎬 Watchlist - Movie Recommendation System

A simple, dark-themed movie recommendation web app built with Python and Streamlit using the MovieLens dataset.



##  Requirements & Tools
- Python 3.8+
- Pandas
- Scikit-learn
- Streamlit


### 1. Clone or Download the Project
Make sure your project folder looks like this:
├── ml-latest-small/
│   ├── movies.csv
│   └── tags.csv
├── model_builder.py
├── index.py
└── README.md


2. Create and Activate Virtual Environment
Bash
python -m venv venv
Windows (PowerShell): .\venv\Scripts\Activate.ps1

3. Install Dependencies
Bash
pip install pandas scikit-learn streamlit

4. Build Model Files
Run this once to clean the data and generate similarity pickle files (movies_list.pkl and similarity.pkl):
Bash
python model_builder.py

5. Run the Application
Bash
python -m streamlit run index.py


## How It Works


Combines movie genres and user tags into feature text.

Uses CountVectorizer to convert text into numbers.

Computes Cosine Similarity between movies.

Displays the top matching movies in a modern cinematic UI.
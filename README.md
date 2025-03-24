# AI-Powered Resume Parser

This resume parser is designed to automate the recruitment process by evaluating and ranking job applicants based on their relevant skills and experience. This model leverages machine learning and natural language processing (NLP) to understand the context of a candidate's resume and assign a weighted score (0-10) based on job relevance.

The system connects to a PostgreSQL database, processes job listings and resumes, and computes the similarity between them using TF-IDF Vectorization and Cosine Similarity. The highest-ranked resume per job category is stored in the database for recruiter reference.

# Key Features
- Context-aware NLP processing to filter out keyword-stuffing
- TF-IDF Vectorization and Cosine Similarity for job-to-resume matching
- Automated resume scoring (0 to 10) based on relevance
- Database integration with PostgreSQL for structured storage
- Efficient recruitment pipeline to streamline candidate shortlisting

# How it Works
1. Extracts job listings and resumes from a PostgreSQL database
2. Cleans & tokenizes the text using NLTK, removing stopwords and punctuation.
3. Tags words with Part-of-Speech (POS) labels for context-based similarity matching.
4. Vectorizes text using TF-IDF to transform resumes and job descriptions into numerical form.
5. Computes Cosine Similarity between resumes and job descriptions to determine how well a candidate matches a given job.
6. Assigns a weighted score (0-10) to each resume based on relevance.
7. Stores the highest-scoring resume per job category back into the database.

# Tech Stack
1. Programming Langauge & Frameworks:
   - Python: Core language for building the resume parser
   - PostgreSQL: Database used to store job listings and resumes
2. Machine Learning & NLP Libraries:
   - NLTK: Used for tokenization, stopword removal, and POS tagging
   - Scikit-learn: Used for TF-IDF vectorization and Cosine Similarity calculations
   - Unidecode: Converts special characters to plain ASCII for text normalization
3. Database & Connectivity:
   - Psycopg2: Python PostgreSQL adapter to interact with the database

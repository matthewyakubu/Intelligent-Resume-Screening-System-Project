import re
import os
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.corpus import stopwords
from unidecode import unidecode
import psycopg2
import string
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

#initialize TF-IDF Vectorizer
vectorizer = TfidfVectorizer(stop_words='english')

#-------------------------
# Function: clean_text(string)
# Purpose is to convert text with special characters to plain ASCII.
# Conversion is accomplished using the 'unicode' lib, and non-alphanumeric characters are removed using the 're' lib.
#-------------------------
def clean_text(text):
    uncleaned_text = unidecode(text) #converts text with special characters to plain ASCII.
    return re.sub(r'[^a-zA-Z0-9\s]', '', uncleaned_text)  # Removes all non-alphanumeric characters, then
    # the 'filtered' string is returned.

#-------------------------
# Function: extract_keywords(string)
# Purpose is to tokenize parsed text and remove stopwords and punctuation from any data acquired from the PostgreSQL
# database using psycopg2.
#-------------------------
def extract_keywords(text):
    if not isinstance(text, str):  # Ensure text is a string
        raise ValueError("Input to extract_keywords must be a string")

    tokens = word_tokenize(text) # Tokenize the text passed into the function.

    stop_words = set(stopwords.words('english'))  # creates a set containing a list of common english stopwords
    punctuation = set(string.punctuation) # creates a set containing a list of punctuation characters

    keywords = [word.lower() for word in tokens if word.lower() not in stop_words and word not in punctuation]
    # any words that do not exist in either set will be made lower case and appended to the 'keywords' array
    # the remaining words after this 'filter process' are the tokenized keywords that will be returned.
    return keywords

# Accessing the databases made using psycopg2 *Syntax below*
try:
    # Establish a connection to the database we want to access on Postgres (port declaration is optional, 5432 is
    # the default port)
    password = os.getenv("SECRET_PASSWORD") # for privacy

    conn = psycopg2.connect(
        dbname = 'postgres',
        user = 'matthewyakubu',
        password= password,
        host='localhost',
        port='5432'
    )

    # To communicate with the database, we initialize a cursor
    cur = conn.cursor()

    # the execute instruction is used to run queries in PostgreSQL through Python.
    # the fetch command is what will store the values gathered from the database(s), and will then be assigned to a
    # variable.
    cur.execute('SET search_path TO schema_resume')
    cur.execute('SELECT industry, description FROM job_listings')
    job_listings = cur.fetchall()

    # -------------------------
    # "industry_job_dict" DICTIONARY:
    # A dictionary defined to separate the two values within each row (tuple) fetched from the database,
    # making the key value pair, "industry:description," for future vectorization.
    #
    # The two pieces of data are parsed separately while iterating through the fetchall command,
    # and the first value is set as the key, while the second is the value tied to it.
    #--------------------------

    industry_job_dict = {industry: description for industry, description in job_listings}

    cur.execute('SELECT industry, job_name FROM job_listings')
    job_names = cur.fetchall()

    job_name_dict = {industry: job_name for industry, job_name, in job_names}

    cur.execute('SELECT category, resume, id FROM resumes')
    rows = cur.fetchall()

    for resume_data in rows:
        clean_resume_data = re.sub(r'\\n+', '', resume_data[1])
        # resume job description entries tend to have '\\n' which are characters attached to the valuable text that are
        # not ignored otherwise in the tokenization process.

        # the above instruction removes those character per iterated row from the 'resumes' table

        #------------------------
        # We call the extract_keywords function to TOKENIZE the JOB DESCRIPTION and remove stopwords
        # and punctuation characters when returning the list of keywords. Then we find the POS tags tied to the tokens,
        # and pair them before reconverting the list into a string for vectorization.
        #------------------------
        keyword_description = extract_keywords(industry_job_dict[resume_data[0]])  # pass the job description into the extract_keywords function
        description_pos = pos_tag(keyword_description) # POS tagging the tokenized job description
        description_merged_pos = ' '.join([f"{token}/{pos}" for token, pos in description_pos]) # converting the list of
        # tokens/POS tag pairs into a string

        # ------------------------
        # the POS tags list is reconverted into a string for vectorization. THe TfId Vectorizer expects a string or a
        # list of strings, and data parsed using psycopg2 come in a list of tuples, so we join the data in order to
        # convert it into a vector.
        # ------------------------

        keyword_resume_data = extract_keywords(clean_resume_data)
        db_pos = pos_tag(keyword_resume_data)
        resume_merged_pos = ' '.join([f"{token}/{pos}" for token, pos in db_pos])

        vectorizer.fit([description_merged_pos, resume_merged_pos]) # fit the vectors together before transformation,
        # to ensure the vector dimensions are consistent in order to calculate cosine similarity.

        description_vector = vectorizer.transform([description_merged_pos]) # transform the job description and
        # resume Token/POS tag pairs.
        resume_vector = vectorizer.transform([resume_merged_pos])

        cosine_sim = cosine_similarity(description_vector, resume_vector)  # calculate cosine similarity of the job
        # description and resume text vectors.

        resume_score = round(cosine_sim[0][0]*10, 2)  # we represent the cosine similarity as a weighted score out of
        # 10 according to the project requirements

        cur.execute('UPDATE resumes SET resume_score = %s WHERE id = %s', (float(resume_score), resume_data[2]))
        # the resume scores are then entered into the resume database in the resume_score column which is identified
        # using the Primary Key (resume id) for the resumes table.

    # a list containing all the different job categories:
    cur.execute('SELECT industry FROM job_listings')
    category = cur.fetchall()
    industry_list = []
    for cat in category: # iterate through the job categories
        if cat not in industry_list:
            industry_list.append("".join(cat)) # convert elements of the list from tuples to strings


    # we iterate through the list to assign the max resume paired with its score to enter into the job_listings table
    for ind in industry_list:
        cur.execute("SELECT resume FROM resumes WHERE category = %s ORDER BY resume_score DESC LIMIT 1", (ind,))
        max_resume = cur.fetchone()
        if max_resume:
            max_resume = ''.join(max_resume)

            cur.execute(f"SELECT resume_score FROM resumes WHERE resume = %s", (max_resume,))
            max_resume_score = cur.fetchone()

            if max_resume_score:
                max_resume_score = max_resume_score[0]
                cur.execute(f"UPDATE job_listings SET max_resume = %s WHERE industry = %s", (max_resume, ind))
                cur.execute(f"UPDATE job_listings SET max_resume_score = %s WHERE industry = %s", (max_resume_score, ind))

    conn.commit() # save changes
    cur.close() # disconnect the cursor and connection to the database
    conn.close()

except Exception as e:
    print("Error:", e)

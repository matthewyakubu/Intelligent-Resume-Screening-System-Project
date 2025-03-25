This project contains two primary databases that store job listings and candidate resumes for the AI-powered resume parser. Below is a description of the contents of each database:

# 1. job_listings Table
This table stores information about job categories and the highest-scoring resumes associated with each category. It includes:
- **industry** – The category or field of the job (e.g., "Software Engineering", "Data Science").
- **description** – A detailed job description outlining requirements, responsibilities, and expectations.
- **job_name** – The specific job title within the industry (e.g., "Automation Test Engineer", "Data Analyst").
- **max_resume_score** – The highest resume score computed for a candidate in this job category (scale of 0–10).
- **max_resume** – The content of the best-matching resume for the job category.

# 2. resumes Table
This table contains all candidate resumes, each linked to a job category from the job_listings table.
- **category** - The job category this resume belongs to (Foreign Key referencing *job_listings.industry*).
- **resume** - The full text of the candidate's resume.
- **resume_score** - The computed similarity score (0-10) indicating how well the resume matches the job category.

# Database Relationships
- The **category** column in **resumes** serves as a **foreign key** referencing the **industry** column in **job_listings**, ensuring that each resume is categorized under a relevant job listing.

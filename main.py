import pandas as pd

from Task_1.resume_data_processor import ResumeDatasetProcessor
from Task_2.get_job_descriptions_processor import JobDescriptionProcessor

from matcher import Matcher

DATASET_PATH = "Task_1/Resume.csv"
NUM_JOB_DESCRIPTION = 10

resume_dataset_processor = ResumeDatasetProcessor(DATASET_PATH)
dataset_df = resume_dataset_processor.process_dataset()

job_descriptions = JobDescriptionProcessor().fetch_job_descriptions(
    num_descriptions=NUM_JOB_DESCRIPTION
)
cv_skills = dataset_df["Skills"]
cv_education = dataset_df["Education"]

matcher = Matcher(cv_skills, cv_education, job_descriptions)
results = matcher.match_candidates_to_job_descriptions()
df = pd.DataFrame(results)
df.to_csv("matching_results.csv", index=False)
df.to_excel("matching_results.xlsx", index=False)
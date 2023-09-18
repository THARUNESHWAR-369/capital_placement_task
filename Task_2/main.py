from get_job_descriptions_processor import JobDescriptionProcessor

OUTPUT_CSV = "Task_2/job_descriptions.csv"
OUTPUT_XLSX = "TasK_2/job_descriptions.xlsx"

NUM_DESCRIPTIONS = 15

# Create an instance of the JobDescriptionProcessor
processor = JobDescriptionProcessor(OUTPUT_CSV, OUTPUT_XLSX)

# Fetch job descriptions
JOB_DESC = processor.fetch_job_descriptions(num_descriptions=NUM_DESCRIPTIONS)

# Save job descriptions to CSV and XLSX
processor.save_to_csv_and_xlsx(JOB_DESC)
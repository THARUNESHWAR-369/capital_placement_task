from datasets import load_dataset
import pandas as pd

class JobDescriptionProcessor:
    def __init__(self, output_csv : str = 'output.csv', output_xlsx : str= 'output.xlsx') -> None:
        self.output_csv = output_csv
        self.output_xlsx = output_xlsx

    def fetch_job_descriptions(self, num_descriptions : int = 10) -> list:
        # Load the Hugging Face dataset
        dataset = load_dataset("jacob-hugging-face/job-descriptions")

        # Extract job descriptions
        job_descriptions = dataset["train"]["job_description"][:num_descriptions]

        return job_descriptions

    def save_to_csv_and_xlsx(self, job_descriptions : str) -> None:
        # Create a DataFrame from job descriptions
        df = pd.DataFrame({"Job Description": job_descriptions})

        # Save to CSV
        df.to_csv(self.output_csv, index=False)

        # Save to XLSX
        df.to_excel(self.output_xlsx, index=False)

        print(f"Job descriptions saved to {self.output_csv} and {self.output_xlsx}")
    

if __name__ == "__main__":
    # Output file paths
    OUTPUT_CSV = "Task 2/job_descriptions.csv"
    OUTPUT_XLSX = "TasK 2/job_descriptions.xlsx"
    
    NUM_DESCRIPTIONS = 15

    # Create an instance of the JobDescriptionProcessor
    processor = JobDescriptionProcessor(OUTPUT_CSV, OUTPUT_XLSX)

    # Fetch job descriptions
    JOB_DESC = processor.fetch_job_descriptions(num_descriptions=NUM_DESCRIPTIONS)

    # Save job descriptions to CSV and XLSX
    processor.save_to_csv_and_xlsx(JOB_DESC)

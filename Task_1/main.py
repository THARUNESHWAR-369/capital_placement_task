from resume_data_processor import ResumeDatasetProcessor

DATASET_PATH = "Task_1/Resume.csv"
OUTPUT_CSV_PATH = "Task_1/extracted_data.csv"
OUTPUT_EXCEL_PATH = "Task_1/extracted_data.xlsx"

dataset_processor = ResumeDatasetProcessor(DATASET_PATH)
dataset_processor.process_dataset(
    output_csv=OUTPUT_CSV_PATH, output_excel=OUTPUT_EXCEL_PATH, save_file=True
)

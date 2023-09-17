"""

This script uses the PDFDataExtractor class to process a dataset of resumes in PDF format.
It extracts key details including Category, Skills, and Education from each resume.

"""

from pdf_data_extraction import PDFDataExtractor
import pandas as pd
from tqdm import tqdm


class ResumeDatasetProcessor:
    """
    A class for processing a dataset of resumes and extracting key details.

    Methods:
    - process_dataset(): Processes the entire dataset and prints extracted details.
    """

    def __init__(self, dataset_path: str) -> None:
        """
        Initializes a ResumeDatasetProcessor instance.

        Args:
            dataset_path (str): The path to the dataset CSV file.
        """
        self.dataset_path = dataset_path
        self.pdf_extractor = PDFDataExtractor()

    def process_dataset(
        self,
        output_csv: str,
        output_excel: str,
        drop_duplicates: bool = True,
        drop_nan: bool = True,
    ) -> None:
        """
        Processes the entire dataset, extracts key details from each CV, and saves the results to a CSV file.

        Args:
            output_csv (str): The path to the output CSV file.
        """
        df = pd.read_csv(self.dataset_path)
        extracted_data = []

        for _, row in tqdm(df.iterrows(), total=df.shape[0]):
            details = self.pdf_extractor.process_cv(row)
            if len(details) > 0 : extracted_data.append(details)

            # Create a DataFrame from the extracted_data list
        result_df = pd.DataFrame(extracted_data)
        result_df.drop_duplicates(inplace=drop_duplicates)
        result_df.dropna(inplace=drop_nan)

        # Save the DataFrame to a CSV file
        result_df.to_csv(output_csv, index=False)
        result_df.to_excel(output_excel, index=False, engine="xlsxwriter")

        print(f"Extracted details saved to {output_csv}")


if __name__ == "__main__":
    DATASET_PATH = "Task 1/Resume.csv"
    OUTPUT_CSV_PATH = "Task 1/extracted_data.csv"
    OUTPUT_EXCEL_PATH = "Task 1/extracted_data.xlsx"

    dataset_processor = ResumeDatasetProcessor(DATASET_PATH)
    dataset_processor.process_dataset(
        output_csv=OUTPUT_CSV_PATH, output_excel=OUTPUT_EXCEL_PATH
    )

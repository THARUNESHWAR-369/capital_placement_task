"""

This script uses the PDFDataExtractor class to process a dataset of resumes in PDF format.
It extracts key details including Category, Skills, and Education from each resume.

"""


from Task_1.pdf_data_extraction import PDFDataExtractor
import pandas as pd
from tqdm import tqdm
#from utils import save

class ResumeDatasetProcessor:
    """
    A class for processing a dataset of resumes and extrawcting key details.

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
        output_csv: str = "output.csv",
        output_excel: str = 'output.xlsx',
        drop_duplicates: bool = True,
        drop_nan: bool = True,
        save_file: bool = False,
    ) -> pd.DataFrame:
        """
        Processes the entire dataset, extracts key details from each CV, and saves the results to a CSV file.

        Args:
            output_csv (str): The path to the output CSV file.
        """
        df = pd.read_csv(self.dataset_path)
        extracted_data = []

        for _, row in tqdm(df.iterrows(), total=df.shape[0], desc="Reading PDF: "):
            details = self.pdf_extractor.process_cv(row)
            if len(details) > 0:
                extracted_data.append(details)

        result_df = pd.DataFrame(extracted_data)
        result_df.drop_duplicates(inplace=drop_duplicates)
        result_df.dropna(inplace=drop_nan)
        
        if save_file:
            #save(to_csv=True, to_excel = True, dataframe=result_df)
            result_df.to_csv(output_csv, index=False)
            result_df.to_excel(output_excel, index=False, engine="xlsxwriter")

            print(f"Extracted details saved to {output_csv}")
            
        return result_df

"""
PDF Resume Data Extraction Script

This script extracts key details (Category, Skills, Education) from PDF resumes in a dataset.

"""

import PyPDF2
from bs4 import BeautifulSoup
import re


class PDFDataExtractor:
    """
    A class for extracting key details (Category, Skills, Education) from PDF resumes.

    Methods:
    - extract_text_from_pdf(pdf_file): Extracts text from a PDF file.
    - extract_details(text): Extracts key details (Category, Skills, Education) from text.
    - process_cv(cv_text): Processes a CV's text and returns extracted details.
    """

    def __init__(self) -> None:
        self.skills_div_regx_pattern = r"SECTION_SKLL\d+"
        self.skills_inner_div_regx_pattern = r"\d+FRFM1"

        self.category_regx_pattern = r"\d+LNAM1"

        self.edu_div_regx_pattern = r"SECTION_EDUC\d+"

    def __get_skills(self, soup) -> str:
        skills_div_regx = re.compile(self.skills_div_regx_pattern)
        skills_inner_div_regx = re.compile(self.skills_inner_div_regx_pattern)

        skills = soup.findAll("div", {"id": skills_div_regx})

        if len(skills) < 1:
            return ""
        skills_text = skills[0].find("div", {"id": skills_inner_div_regx})
        skills_text = skills_text.get_text(strip=True) if skills_text != None else None

        return skills_text if skills_text != None else ""

    def __get_category(self, soup) -> str:
        category_regx = re.compile(self.category_regx_pattern)

        categories = soup.find("span", {"id": category_regx})

        categories_text = categories
        categories_text = (
            categories_text.get_text(strip=True).replace("/", " | ")
            if categories_text != None
            else None
        )
        try:
            categories_text = categories_text.split("\n")[0]
        except:
            pass

        return categories_text if categories_text != None else None

    def __get_education(self, soup) -> list:
        education = []
        education_div_regx = re.compile(self.edu_div_regx_pattern)

        education_div = soup.find("div", {"id": education_div_regx})

        if education_div != None:
            single_column = education_div.find_all("div", {"class": "singlecolumn"})

            for sc in single_column:
                if sc != None:
                    institution_name = sc.find("span", {"class": "companyname_educ"})
                    institution_name = (
                        institution_name.get_text(strip=True)
                        if institution_name != None
                        else None
                    )
                    if (
                        institution_name != "N/A"
                        or institution_name != None
                        or institution_name != ""
                    ):
                        degree_name = sc.find("span", {"class": "degree"})
                        degree_name = (
                            degree_name.get_text(strip=True)
                            if degree_name != None
                            else None
                        )
                        if (
                            degree_name == "N/A"
                            or degree_name == None
                            or degree_name == ""
                        ):
                            continue

                        education.append(f"{degree_name} - {institution_name}")

        return education

    def extract_text_from_pdf(self, pdf_file) -> str:
        """
        Extracts text content from a PDF file.

        Args:
            pdf_file (str): The path to the PDF file.

        Returns:
            str: Extracted text content.
        """
        text = ""
        try:
            with open(pdf_file, "rb") as pdf_file:
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                for page_num in range(len(pdf_reader.pages)):
                    text += pdf_reader.pages[page_num].extract_text()
        except FileNotFoundError:
            print(f"[-] File not found {pdf_file}")
        return text
    
    def extract_details_from_pdf_text(self, pdf_text: str) -> dict:
        """
        Extracts education, skills, and category information from PDF text.

        Args:
            pdf_text (str): Text extracted from a PDF.

        Returns:
            dict: Extracted details including 'Category', 'Skills', and 'Education'.
        """
        data = {}
        
        # Extract Category (assuming it's the first line)
        lines = pdf_text.split('\n')
        data['Category'] = lines[0].strip()

        # Extract Skills
        skills_match = re.search(r'SKILLS\s*([\s\S]*?)CERTIFICATIONS', pdf_text, re.IGNORECASE)
        print(skills_match)
        if skills_match:
            skills_text = skills_match.group(1).strip()
            skills = [line.strip() for line in skills_text.split('\n') if line.strip()]
            data['Skills'] = skills

        # Extract Education
        education_match = re.search(r'EDUCATION(.*?)SKILLS', pdf_text, re.DOTALL)
        if education_match:
            education_text = education_match.group(1).strip()
            education = [line.strip() for line in education_text.split('\n') if line.strip()]
            data['Education'] = education

        return data

    def extract_details(self, text) -> dict:
        """
        Extracts key details (Category, Skills, Education) from text.

        Args:
            text (str): Text content from a CV.

        Returns:
            dict: Extracted details including 'Category', 'Skills', and 'Education'.
        """

        data = {}

        soup = BeautifulSoup(text["Resume_html"], "html.parser")

        data["Category"] = self.__get_category(soup)
        if data["Category"] != None:
            
            data["Skills"] = self.__get_skills(soup)
            data["Education"] = self.__get_education(soup)
            
            if len(data["Education"]) > 0:
                data["Education"] = ", ".join([i for i in data['Education']])
            else:
                data['Education'] = ''

        return data


    def process_cv(self, cv_text) -> dict:
        """
        Processes a CV's text and returns extracted details.

        Args:
            cv_text (str): Text content from a CV.

        Returns:
            dict: Extracted details including 'Category', 'Skills', and 'Education'.
        """
        return self.extract_details(cv_text)

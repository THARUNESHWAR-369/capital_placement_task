# capital_placement_task

## **Task: Matching Extracted CV Details to Job Descriptions**

### **Approach:**

1. **Data Extraction from PDFs:**
    - We used the PyPDF2 library to extract text content from PDF resumes. This was done using the `PDFDataExtractor` class, which utilized regular expressions to extract key details like skills, education, and category.

2. **Preprocessing Extracted Data:**
    - Extracted data was then processed using the `PDFDataExtractor` class to obtain structured information including Category, Skills, and Education.

3. **Job Description Fetching:**
    - We fetched job descriptions using the Hugging Face dataset library. This provided us with a set of job descriptions to match against the extracted CV details.

4. **Matching Candidates to Job Descriptions:**
    - For each job description, we calculated the cosine similarity between the job description's embedding and the embeddings of the CVs based on skills and education.
    - We ranked CVs based on similarity scores and selected the top 5 candidates for each job description based on both skills and education similarities.
    - Results were stored in a structured format.

5. **Data Saving:**
    - Finally, we saved the matching results to CSV and Excel files for further analysis.

### **Challenges Faced and Solutions:**

1. **PDF Data Extraction:**
    - The challenge was extracting structured data from PDFs, as the format of PDFs can vary significantly. We solved this by using regular expressions to identify and extract specific sections (skills, education, etc.).

2. **Embedding Size Mismatch:**
    - We encountered issues with embeddings having a shape mismatch. To address this, we modified the `tokenize_and_embed` function to ensure that embeddings are of the correct shape (768 dimensions) by truncating or padding as needed.

3. **Efficiency and Scalability:**
    - Scaling up to process a large number of CVs and job descriptions efficiently could be a challenge. We addressed this by using batch processing and optimizing code for performance.

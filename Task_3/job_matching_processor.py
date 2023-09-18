import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from transformers import DistilBertTokenizer, DistilBertModel
import pandas as pd

from Task_1.resume_data_processor import ResumeDatasetProcessor
from Task_2.get_job_descriptions_processor import JobDescriptionProcessor

class ResumeMatcherProcessor:
    
    def __init__(self, tokenizer_model : str = "distilbert-base-uncased", bert_model : str = "distilbert-base-uncased") -> None:
        
        self.tokenizer_model = tokenizer_model
        self.bert_model = bert_model
    
        self.__init_models__()
        
    def __init_models__(self) -> None:
        self.tokenizer = DistilBertTokenizer.from_pretrained(self.tokenizer_model)
        self.model = DistilBertModel.from_pretrained(self.bert_model)
               
    def tokenize_and_embed(self, text_list : list) -> list:
        embeddings = []
        for text in text_list:
            # Tokenize text
            tokens = self.tokenizer(text, return_tensors='pt', padding=True, truncation=True)
            with np.errstate(divide='ignore'):
                embedding = self.model(**tokens).last_hidden_state.mean(dim=1).detach().numpy()
            embeddings.append(embedding.reshape(768))  # Reshape to 1D array
        return embeddings

        
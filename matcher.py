import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

from Task_3.job_matching_processor import ResumeMatcherProcessor

class Matcher:
    def __init__(
        self,
        cv_skills: list,
        cv_education: list,
        job_descriptions: list,
        resume_matching_processor: ResumeMatcherProcessor = ResumeMatcherProcessor(),
    ):
        self.cv_skills = cv_skills
        self.cv_education = cv_education
        self.job_descriptions = job_descriptions

        self.resume_matching_processor = resume_matching_processor

    def match_candidates_to_job_descriptions(self) -> list:
        num_top_candidates = 5
        cv_skills_embeddings = self.resume_matching_processor.tokenize_and_embed(
            self.cv_skills
        )
        cv_education_embeddings = self.resume_matching_processor.tokenize_and_embed(
            self.cv_education
        )
        job_description_embeddings = self.resume_matching_processor.tokenize_and_embed(
            self.job_descriptions
        )

        similarity_scores_skills = cosine_similarity(
            job_description_embeddings, cv_skills_embeddings
        )
        similarity_scores_education = cosine_similarity(
            job_description_embeddings, cv_education_embeddings
        )

        results = []

        for i, description in enumerate(self.job_descriptions):
            ranked_candidates = np.argsort(similarity_scores_skills[i])[::-1][
                :num_top_candidates
            ]

            top_candidates = []
            for rank, candidate_idx in enumerate(ranked_candidates, start=1):
                top_candidates.append(
                    {
                        "Rank": rank,
                        "Candidate": f"Candidate {candidate_idx + 1}",
                        "Similarity Score (Skills)": similarity_scores_skills[i][
                            candidate_idx
                        ],
                    }
                )

            ranked_candidates_education = np.argsort(similarity_scores_education[i])[
                ::-1
            ][:num_top_candidates]
            top_candidates_education = []
            for rank, candidate_idx in enumerate(ranked_candidates_education, start=1):
                top_candidates_education.append(
                    {
                        "Rank": rank,
                        "Candidate": f"Candidate {candidate_idx + 1}",
                        "Similarity Score (Education)": similarity_scores_education[i][
                            candidate_idx
                        ],
                    }
                )

            results.append(
                {
                    "Job Description": description,
                    "Top Candidates (Skills)": top_candidates,
                    "Top Candidates (Education)": top_candidates_education,
                }
            )

        return results


import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

from Task_1.resume_data_processor import ResumeDatasetProcessor
from Task_2.get_job_descriptions_processor import JobDescriptionProcessor
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

            # Now, let's also include the top candidates based on education similarity
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


if __name__ == "__main__":
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

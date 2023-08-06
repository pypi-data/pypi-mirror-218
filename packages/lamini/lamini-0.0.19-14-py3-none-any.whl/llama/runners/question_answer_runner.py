from typing import List
from llama import Type, Context, LLMEngine
import jsonlines
import pandas as pd


# Input
class Question(Type):
    question: str = Context("a question")


# Output
class Answer(Type):
    answer: str = Context("the response to the question")


# Document
class Document(Type):
    document: str = Context("a document")


class QuestionAnswerModel:
    """A class for running and training a question answering model"""

    def __init__(self, model_name: str = "EleutherAI/pythia-410m-deduped"):
        self.model_name = model_name
        self.llm = LLMEngine("question_answer_runner", model_name=model_name)
        self.question_answer = []
        self.documents = []
        self.job_id = None

    def get_answer(self, question: str) -> str:
        """Get answer to a single question"""
        question_object = Question(question=question)
        answer_object = self.llm(
            input=question_object,
            output_type=Answer,
            model_name=self.model_name,
            task="question_answer",
        )
        return answer_object.answer

    def get_answers(self, questions: List[str]) -> List[str]:
        """Get answers to a batch of questions"""
        print("Asking %d questions" % len(questions))
        question_objects = [Question(question=q) for q in questions]
        answer_objects = self.llm(
            input=question_objects,
            output_type=Answer,
            model_name=self.model_name,
            task="question_answer",
        )
        answers = [a.answer for a in answer_objects]
        return [{"question": q, "answer": a} for q, a in zip(questions, answers)]

    def load_documents(self, documents: List[str]):
        """Load a list of document strings into the LLM"""
        document_objects = [Document(document=d) for d in documents]
        self.documents.extend(document_objects)

    def load_documents_from_jsonlines(self, file_path: str):
        """
        Load a jsonlines file with documents into the LLM.
        Each line must be a json object with 'document' as a key.
        """
        documents = []
        try:
            with open(file_path) as dataset_file:
                reader = jsonlines.Reader(dataset_file)
                documents = list(reader)
                documents = [d["document"] for d in documents]
        except KeyError:
            raise ValueError("Each json object in file must have 'document' as a key")
        self.load_documents(documents)

    def load_question_answer(self, data):
        """
        Load a list of json objects with question answer keys into the LLM
        Each object must have 'question' and 'answer' as keys.
        """
        try:
            question_answer_objects = [
                [Question(question=d["question"]), Answer(answer=d["answer"])]
                for d in data
            ]
        except KeyError:
            raise ValueError("Each object must have 'question' and 'answer' as keys")
        self.question_answer.extend(question_answer_objects)

    def load_question_answer_from_jsonlines(self, file_path: str):
        """
        Load a jsonlines file with question answer keys into the LLM.
        Each line must be a json object with 'question' and 'answer' as keys.
        """
        data = []
        with open(file_path) as dataset_file:
            reader = jsonlines.Reader(dataset_file)
            data = list(reader)
        self.load_question_answer(data)

    def load_question_from_dataframe(self, df: pd.DataFrame):
        """
        Load a pandas dataframe with question answer keys into the LLM.
        Each row must have 'question' as a key.
        """
        for _, row in df.iterrows():
            self.question_answer.append(
                [Question(question=row["question"]), Answer(answer=row["answer"])]
            )

    def load_question_answer_from_csv(self, file_path: str):
        """
        Load a csv file with question answer keys into the LLM.
        Each row must have 'question' and 'answer' as keys.
        """
        df = pd.read_csv(file_path)
        self.load_question_from_dataframe(df)

    def clear_data(self):
        """Clear the data from the LLM"""
        self.llm.clear_data()
        self.question_answer = []
        self.documents = []

    def train(
        self,
        verbose: bool = False,
    ):
        """
        Train the LLM on added data. This function blocks until training is complete.
        """
        if len(self.question_answer) > 500:
            qa_pairs = self.question_answer[:500]
        else:
            qa_pairs = self.question_answer
        self.llm.save_data(qa_pairs)
        if len(self.documents) > 100:
            documents = self.documents[:100]
        else:
            documents = self.documents
        self.llm.save_data(documents)
        final_status = self.llm.train(task="question_answer", verbose=verbose)
        self.model_name = final_status["model_name"]
        self.job_id = final_status["job_id"]
        self.llm = LLMEngine("question_answer_runner", model_name=self.model_name)
        self.llm.clear_data()

    def get_eval_results(self) -> List:
        """Get evaluation results"""
        if self.job_id is None:
            raise Exception("Must train before getting results")
        return self.llm.eval(self.job_id)

import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from recruiter_questions import RECRUITER_QUESTIONS
from rag.retriever import retrieve_knowledge

print("\n======================================")
print("   MALAMIN RECRUITER RAG TEST")
print("======================================\n")


for number, question in enumerate(
    RECRUITER_QUESTIONS,
    start=1
):

    print("--------------------------------------")

    print(f"TEST {number}")
    print(f"QUESTION: {question}")

    result = retrieve_knowledge(question)

    print("\nRETRIEVED KNOWLEDGE:")
    print(result)

    print("--------------------------------------\n")
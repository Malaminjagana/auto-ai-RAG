import os


KNOWLEDGE_FILE = os.path.join(
    "knowledge",
    "institute.txt"
)


def load_knowledge():

    with open(
        KNOWLEDGE_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return file.read()


def retrieve_knowledge(user_message):

    knowledge = load_knowledge()

    return knowledge
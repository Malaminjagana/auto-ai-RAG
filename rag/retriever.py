import chromadb


client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_or_create_collection(
    name="institute_knowledge"
)


def retrieve_knowledge(
    query: str,
    n_results: int = 4
):

    
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )

    documents = results.get("documents", [[]])[0]

    return "\n\n".join(documents)

if __name__ == "__main__":

    result = retrieve_knowledge(
        "What programs does the institute offer?"
    )

    print(result)
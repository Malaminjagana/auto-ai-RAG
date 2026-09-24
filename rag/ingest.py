import os
import chromadb
from pypdf import PdfReader
from docx import Document


# =========================================================
# CHROMADB
# =========================================================

client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_or_create_collection(
    name="institute_knowledge"
)


# =========================================================
# CHUNK TEXT
# =========================================================

def chunk_text(
    text: str,
    chunk_size: int = 500,
    overlap: int = 50
):

    words = text.split()

    chunks = []

    start = 0

    while start < len(words):

        end = start + chunk_size

        chunk = " ".join(
            words[start:end]
        )

        if chunk.strip():
            chunks.append(chunk)

        start = end - overlap

    return chunks


# =========================================================
# LOAD TXT
# =========================================================

def load_txt(filepath):

    with open(
        filepath,
        "r",
        encoding="utf-8"
    ) as file:

        text = file.read()

    return [
        {
            "text": text
        }
    ]


# =========================================================
# LOAD PDF
# =========================================================

def load_pdf(filepath):

    reader = PdfReader(filepath)

    pages = []

    for page_number, page in enumerate(
        reader.pages,
        start=1
    ):

        text = page.extract_text() or ""

        if text.strip():

            pages.append({
                "text": text,
                "page": page_number
            })

    return pages


# =========================================================
# LOAD DOCX
# =========================================================

def load_docx(filepath):

    document = Document(filepath)

    paragraphs = []

    for paragraph_number, paragraph in enumerate(
        document.paragraphs,
        start=1
    ):

        text = paragraph.text.strip()

        if text:

            paragraphs.append({
                "text": text,
                "paragraph": paragraph_number
            })

    return paragraphs


# =========================================================
# LOAD DOCUMENTS
# =========================================================

def load_documents():

    all_chunks = []
    all_ids = []
    all_metadata = []

    knowledge_folder = "knowledge"


    # -----------------------------------------------------
    # Check knowledge folder
    # -----------------------------------------------------

    if not os.path.exists(knowledge_folder):

        print(
            "Knowledge folder not found."
        )

        return (
            all_chunks,
            all_ids,
            all_metadata
        )


    # -----------------------------------------------------
    # Loop through files
    # -----------------------------------------------------

    for filename in os.listdir(
        knowledge_folder
    ):

        filepath = os.path.join(
            knowledge_folder,
            filename
        )


        # -------------------------------------------------
        # Ignore directories
        # -------------------------------------------------

        if not os.path.isfile(filepath):
            continue


        # -------------------------------------------------
        # Get file extension
        # -------------------------------------------------

        extension = os.path.splitext(
            filename
        )[1].lower()


        # -------------------------------------------------
        # Load TXT
        # -------------------------------------------------

        if extension == ".txt":

            documents = load_txt(filepath)


        # -------------------------------------------------
        # Load PDF
        # -------------------------------------------------

        elif extension == ".pdf":

            documents = load_pdf(filepath)


        # -------------------------------------------------
        # Load DOCX
        # -------------------------------------------------

        elif extension == ".docx":

            documents = load_docx(filepath)


        # -------------------------------------------------
        # Ignore unsupported files
        # -------------------------------------------------

        else:

            print(
                f"Skipping unsupported file: {filename}"
            )

            continue


        # -------------------------------------------------
        # Process each document section
        # -------------------------------------------------

        for document_index, document in enumerate(
            documents
        ):

            text = document["text"]

            chunks = chunk_text(text)


            # -------------------------------------------------
            # Create chunks
            # -------------------------------------------------

            for chunk_index, chunk in enumerate(
                chunks
            ):


                # ---------------------------------------------
                # Create a UNIQUE ID
                # ---------------------------------------------

                chunk_id = (
                    f"{filename}-"
                    f"section{document_index}-"
                    f"chunk{chunk_index}"
                )


                # ---------------------------------------------
                # Base metadata
                # ---------------------------------------------

                metadata = {
                    "source": filename,
                    "file_type": extension.replace(
                        ".",
                        ""
                    ),
                    "section": document_index,
                    "chunk": chunk_index
                }


                # ---------------------------------------------
                # Add PDF page
                # ---------------------------------------------

                if "page" in document:

                    metadata["page"] = document["page"]


                # ---------------------------------------------
                # Add DOCX paragraph
                # ---------------------------------------------

                if "paragraph" in document:

                    metadata["paragraph"] = (
                        document["paragraph"]
                    )


                # ---------------------------------------------
                # Save data
                # ---------------------------------------------

                all_chunks.append(chunk)

                all_ids.append(chunk_id)

                all_metadata.append(metadata)


    return (
        all_chunks,
        all_ids,
        all_metadata
    )


# =========================================================
# INGEST DOCUMENTS INTO CHROMADB
# =========================================================

def ingest_documents():

    global collection


    # -----------------------------------------------------
    # LOAD DOCUMENTS
    # -----------------------------------------------------

    (
        chunks,
        ids,
        metadata
    ) = load_documents()


    # -----------------------------------------------------
    # NO DOCUMENTS
    # -----------------------------------------------------

    if not chunks:

        print(
            "No documents found."
        )

        return


    # -----------------------------------------------------
    # CHECK FOR DUPLICATE IDS
    # -----------------------------------------------------

    if len(ids) != len(set(ids)):

        print(
            "ERROR: Duplicate IDs were detected."
        )

        return


    # -----------------------------------------------------
    # DELETE OLD KNOWLEDGE COLLECTION
    # -----------------------------------------------------

    print(
        "Deleting old knowledge collection..."
    )

    try:

        client.delete_collection(
            name="institute_knowledge"
        )

        print(
            "Old knowledge collection deleted."
        )

    except Exception:

        print(
            "No existing collection found."
        )


    # -----------------------------------------------------
    # CREATE CLEAN COLLECTION
    # -----------------------------------------------------

    collection = client.create_collection(
        name="institute_knowledge"
    )


    # -----------------------------------------------------
    # ADD NEW DOCUMENTS
    # -----------------------------------------------------

    collection.add(

        documents=chunks,

        ids=ids,

        metadatas=metadata

    )


    # -----------------------------------------------------
    # SUCCESS
    # -----------------------------------------------------

    print(
        f"Added {len(chunks)} chunks "
        "to the knowledge base."
    )


# =========================================================
# RUN INGESTION
# =========================================================

if __name__ == "__main__":

    ingest_documents()
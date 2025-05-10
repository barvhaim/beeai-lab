"""
RAG (Retrieval-Augmented Generation) example with security focus using a local vector database.
This lab demonstrates how to create a simple RAG system that can answer questions about
cyber threats based on a local knowledge base of security reports.
"""

import os
from typing import List, Optional

from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from termcolor import colored
from llm_provider import get_llm_client
from llm_provider.embeddings_model import get_embeddings_model


def _load_documents(file_path: str) -> List[Document]:
    """
    Load documents from a text file and split them into chunks.
    """
    from langchain_text_splitters import RecursiveCharacterTextSplitter

    loader = TextLoader(file_path)
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=40)

    return text_splitter.split_documents(documents)


def _create_vector_db(documents: List[Document], persist_directory: str) -> Chroma:
    """
    Create a vector database from documents and persist it to disk.
    """
    embeddings = get_embeddings_model()
    vectordb = Chroma.from_documents(
        documents=documents, embedding=embeddings, persist_directory=persist_directory
    )
    vectordb.persist()
    return vectordb


def _load_vector_db(persist_directory: str) -> Optional[Chroma]:
    """
    Load a vector database from disk if it exists.
    """
    if not os.path.exists(persist_directory):
        return None

    embeddings = get_embeddings_model()
    return Chroma(persist_directory=persist_directory, embedding_function=embeddings)


def _format_docs(docs: List[Document]) -> str:
    """
    Format documents for inclusion in the prompt.
    """
    return "\n\n".join([doc.page_content for doc in docs])


def lab_4():
    """
    RAG example with CTI reports using a local vector database.
    """

    llm_parameters = {
        "decoding_method": "sample",
        "max_new_tokens": 256,
        "min_new_tokens": 1,
        "temperature": 0.05,
        "top_k": 10,
        "stop_sequences": ["\nQuestion:"],
    }

    # model_name = "meta-llama/llama-3-3-70b-instruct"
    model_name = "phi3"

    llm = get_llm_client(
        model_name=model_name,
        model_parameters=llm_parameters,
    )

    data_path = os.path.join(
        os.path.dirname(__file__), "data", "example_cti_report.txt"
    )
    db_path = os.path.join(os.path.dirname(__file__), "data", "vector_db")

    vectordb = _load_vector_db(db_path)
    if vectordb is None:
        print(colored("Creating new vector database...", "yellow"))
        documents = _load_documents(data_path)
        vectordb = _create_vector_db(documents, db_path)
        print(colored(f"Vector database created with {len(documents)} chunks", "green"))
    else:
        print(colored("Loaded existing vector database", "green"))

    retriever = vectordb.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 3},  # Retrieve top 3 most relevant chunks
    )

    template = """You are a cybersecurity analyst assistant. Use the following pieces of context to answer the question at the end.
If you don't know the answer, just say that you don't know, don't try to make up an answer.
Keep your answers concise and focused on the security information provided.

Context:
{context}

Question: {question}

Answer:"""

    prompt = PromptTemplate.from_template(template)

    rag_chain = (
        {"context": retriever | _format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    security_questions = [
        "What techniques did APT29 use to bypass MFA?",
        "How did the hackers maintain persistence on compromised systems?",
        "What malware was used in the StellarParticle campaign?",
        "How long were the attackers able to stay undetected?",
    ]

    print(colored("=== RAG Demo ===", "blue", attrs=["bold"]))
    for i, question in enumerate(security_questions, 1):
        print(colored(f"Question {i}: {question}", "cyan"))
        answer = rag_chain.invoke(question)
        print(colored(f"Answer: {answer}\n", "green"))


if __name__ == "__main__":
    lab_4()

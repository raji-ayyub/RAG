from pathlib import Path
from typing import List, Dict, Any
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
import os
from dotenv import load_dotenv

load_dotenv()


class VectorStoreManager:
    def __init__(self, pdf_path: str, api_key: str):
        self.pdf_path = pdf_path
        self.api_key = api_key

        self.embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small",
            openai_api_key = self.api_key,
        )

        self.vectorstore = self._build_vectorstore()

    def _build_vectorstore(self):
        loader = PyPDFLoader(self.pdf_path)
        pages = loader.load()

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=600,
            chunk_overlap=100
        )

        documents = splitter.split_documents(pages)

        return FAISS.from_documents(documents, self.embeddings)

    def get_retriever(self, k: int=3):
        return self.vectorstore.as_retriever(
            search_kwargs={"k":k}
        )


class PromptBuilder:
    def __init__(self):
        self.prompt = ChatPromptTemplate.from_messages([
            (
                "system", 
                 """
You are a retrieval-augmented assistant for Raji Ayyub.

Rules you MUST follow:
1. Use ONLY the information in the provided context.
2. If the answer is not present in the context, answer with something related but from the context.
"""
            ),
            (
                "human",
                "Question: {question}\n\nContext:\n{context}"
            ),
        ])

    def get_prompt(self):
        return self.prompt
    

class LLMClient:
    def __init__(self, api_key: str):
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0,
            openai_api_key=api_key
        )
    
    def get_llm(self):
        return self.llm
        


class RAGPipeline:
    def __init__(self, retriever, prompt, llm):
        self.retriever = retriever
        self.prompt = prompt
        self.llm = llm

        self.chain = self._build_chain()

    def _format_docs(self, docs):
        return "\n\n".join(doc.page_content for doc in docs)
    
    def _build_chain(self):
        return (
            {
                "context": self.retriever | self._format_docs,
                "question": RunnablePassthrough(),
            }

            | self.prompt
            | self.llm
        )
    
    def ask(self, question: str) -> str:
        response = self.chain.invoke(question)
        return response.content
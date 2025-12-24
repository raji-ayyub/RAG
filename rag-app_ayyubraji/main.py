import os
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

from .rag import (
    VectorStoreManager,
    PromptBuilder,
    LLMClient,
    RAGPipeline
)


load_dotenv()


API_KEY = os.getenv("gen_api_key")
PDF_PATH = "rag-app_ayyubraji/ayyub_cv.pdf"

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


vector_manager = VectorStoreManager(
    pdf_path=PDF_PATH,
    api_key=API_KEY
)

retriever = vector_manager.get_retriever()

prompt_builder = PromptBuilder()

llm_client = LLMClient(api_key=API_KEY)

rag_pipeline = RAGPipeline(
    retriever = retriever,
    prompt= prompt_builder.get_prompt(),
    llm = llm_client.get_llm()
)












class QuestionRequest(BaseModel):
    question: str

@app.post("/chat")
def chat(request: QuestionRequest):
    answer = rag_pipeline.ask(request.question)
    return {"response": answer}

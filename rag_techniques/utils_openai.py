# import os
# from dotenv import load_dotenv
# import openai

# import pandas as pd


# load_dotenv()




# def set_openai_api_key():
#     api_key = os.getenv("gen_api_key")
#     if not api_key:
#         return {"message": "api key not found, ensure it exists in .env and is properly named"}

#     openai.api_key = api_key
#     return api_key


# def load_msme_data(filepath: str = "msme_data.csv"):
#     """
    
#     """

#     filepath = "msme_sample.json"

#     try:
#         if filepath.endswith(".csv"):
#             df = pd.read_csv(filepath)
#         elif filepath.endswith(".json"):
#             df = pd.read_json(filepath)
#         else:
#             raise ValueError("Unsurported file format")
        
#         return df

#     except FileNotFoundError:
#         print("file not found")
    

# def create_embeddings(texts: Lists[str], model: str="text-embedding-ada-002") -> List[List[float]]:
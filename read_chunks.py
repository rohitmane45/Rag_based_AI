import requests
import os
import json
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import joblib

OLLAMA_EMBED_URL = "http://localhost:11434/api/embed"
EMBED_MODEL = "bge-m3"

def create_embedding(text_list):
    def request_embedding(text, idx):
        try:
            r = requests.post(
                OLLAMA_EMBED_URL,
                json={"model": EMBED_MODEL, "input": [str(text).strip()]},
                timeout=60,
            )
        except requests.exceptions.RequestException as e:
            raise RuntimeError(
                "Cannot reach Ollama at http://localhost:11434. "
                "Start Ollama with 'ollama serve'."
            ) from e

        try:
            payload = r.json()
        except ValueError as e:
            raise RuntimeError(f"Non-JSON response from Ollama: {r.text[:200]}") from e

        if not r.ok:
            msg = payload.get("error", r.text)
            raise RuntimeError(f"Embedding request failed at chunk {idx}: {msg}")

        if "embeddings" not in payload or not payload["embeddings"]:
            msg = payload.get("error", f"Unexpected response keys: {list(payload.keys())}")
            raise RuntimeError(f"Missing embeddings at chunk {idx}: {msg}")

        return payload["embeddings"][0]

    def embed_with_fallback(text, idx):
        try:
            return request_embedding(text, idx)
        except RuntimeError:
            words = str(text).split()
            if len(words) <= 1:
                raise
            middle = len(words) // 2
            left = embed_with_fallback(" ".join(words[:middle]), idx)
            right = embed_with_fallback(" ".join(words[middle:]), idx)
            return [(l + r) / 2 for l, r in zip(left, right)]

    embeddings = []
    for idx, text in enumerate(text_list):
        embeddings.append(embed_with_fallback(text, idx))

    return embeddings


jsons = os.listdir("json")  # List all the jsons 
my_dicts = []
chunk_id = 0

for json_file in jsons:
    with open(f"json/{json_file}") as f:
        content = json.load(f)
    print(f"Creating Embeddings for {json_file}")
    embeddings = create_embedding([c['text'] for c in content['chunks']])
       
    for i, chunk in enumerate(content['chunks']):
        chunk['chunk_id'] = chunk_id
        chunk['embedding'] = embeddings[i]
        chunk_id += 1
        my_dicts.append(chunk) 
# print(my_dicts)

df = pd.DataFrame.from_records(my_dicts)
# print(df)
joblib.dump(df,"embeddings.joblib")




# a = create_embedding(["Cat sat on the mat", "Harry dances on a mat"])
# print(a)






# import requests
# import requests.exceptions
# import os
# import json
# import pandas as pd

# def create_embedding(text_list):
#     def embed_text(text):
#         try:
#             r = requests.post(
#                 "http://localhost:11434/api/embed",
#                 json={"model": "bge-m3", "input": [text.strip()]},
#                 timeout=10,
#             )
#         except requests.exceptions.ConnectionError as e:
#             raise RuntimeError(
#                 "Could not connect to embedding server at http://localhost:11434. "
#                 "Start the local embedding server or change the endpoint in read_chunks.py."
#             ) from e
#         except requests.exceptions.RequestException as e:
#             raise RuntimeError(f"Request to embedding server failed: {e}") from e

#         if r.ok:
#             return r.json()["embeddings"][0]

#         words = text.split()
#         if len(words) > 1:
#             middle = len(words) // 2
#             left_embedding = embed_text(" ".join(words[:middle]))
#             right_embedding = embed_text(" ".join(words[middle:]))
#             return [(left + right) / 2 for left, right in zip(left_embedding, right_embedding)]

#         raise RuntimeError(r.text)

#     return [embed_text(text) for text in text_list]
    

# # embedding = create_embedding("roo is my name and i am a software engineer")
# # print(embedding[0:6])

# jsons = os.listdir("json")
# my_dicts=[]
# chunk_id =0

# for json_file in jsons:
#     with open(f"json/{json_file}") as f:
#         content = json.load(f)
#         print(f"Creating embedding for {json_file}")
#         embeddings = create_embedding([c["text"]for c in content["chunks"]])


#         for i,chunk in enumerate(content["chunks"]):
#             chunk["chunk_id"] = chunk_id
#             chunk["embedding"] = embeddings[i]
#             chunk_id+=1
#             my_dicts.append(chunk)

# df = pd.DataFrame.from_records(my_dicts)
# print(df)
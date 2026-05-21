import requests
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np
import joblib
from typer import prompt

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

def inference(prompt):
    r = requests.post("http://localhost:11434/api/generate", json={
        # "model": "deepseek-r1",
        "model": "llama3.2",
        "prompt": prompt,
        "stream": False
    })

    response = r.json()
    print(response)
    return response

df = joblib.load("embeddings.joblib")  # Load the dataframe with embeddings

incoming_queries = input("Ask  your query: ")
query_embedding = create_embedding([incoming_queries])[0]
# print(query_embedding)
# print(np.vstack(df['embedding'].values))
# print(np.vstack(df['embedding'].values).shape)

similarities = cosine_similarity(np.vstack(df['embedding']),[query_embedding]).flatten()
# print(similarities)
top_results = 5
max_indx = similarities.argsort()[::-1][0:top_results]
new_df = df.iloc[max_indx]
# print(new_df[['title','number','text']])

for index,item in new_df.iterrows():
    print(index,item['title'],item['number'],item['text'],item['start'],item['end'])

prompt = f'''I am teaching AI using YT 2MIN VIDEOS come. Here are video subtitle chunks containing video title, video, number, start time in se, end time in seconds, the text at that time:

{new_df[['title','number','start','end','text']].to_json(orient="records")}

{incoming_queries}

User asked question related to the video chunks, you have to answer where and how much content is taught in winch video (in which video and at what timestamp) and guide the user to go to that particular video. If user asks unrelated question, tell him that you can only answer questions related to the course
'''


with open("prompt.txt","w") as f:
    f.write(prompt)


response = inference(prompt)["response"]
print(response)

with open("response.txt", "w") as f:
    f.write(response)   
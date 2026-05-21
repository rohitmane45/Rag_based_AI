# 🚀 Rag Based AI

> Ask questions about course videos and get the most relevant answer, chunk, and timestamp.

## ✨ What this project does

This project turns long course videos into something searchable.
Instead of rewatching everything, you can ask questions like:

- 📌 What is this course about?
- 🎯 Where is this topic explained?
- ⏱️ Which video covers this idea?

The system finds the most relevant transcript chunks and uses a local Ollama model to generate an answer.

## 🧠 How it works

1. 🎥 Video is converted to audio
2. 🎙️ Audio is transcribed into text chunks
3. 🔎 Chunks are converted into embeddings
4. 💬 Your question is matched with the closest chunks
5. 🤖 Ollama creates the final response

## 🛠️ Main scripts

- `video_file_to_mp3.py` - converts videos in `video/` into MP3 files in `audio/`
- `mp3_to_json.py` - transcribes audio with Whisper and saves chunk data
- `read_chunks.py` - creates embeddings for each chunk and stores them in `embeddings.joblib`
- `process_chuunks.py` - asks a question, finds the best chunks, and generates the answer

## 📁 Project structure

- `video/` - input video files
- `audio/` - extracted audio files
- `json/` - transcript chunk files
- `embeddings.joblib` - saved embeddings and metadata
- `prompt.txt` - prompt sent to the local model
- `response.txt` - final answer saved from the model
- `whisper/` - local Whisper source used by the project

## ✅ What is already done

- Video files are converted into audio
- Audio is split into transcript chunks
- Chunks are saved in JSON format
- Embeddings are generated for every chunk
- User questions are matched with the most relevant chunks
- A local model generates the final answer

## 📦 Requirements

You need:

- Python
- FFmpeg
- Ollama

Python packages used by the project:

- `requests`
- `pandas`
- `numpy`
- `scikit-learn`
- `joblib`
- `whisper`
- `typer`

## ⚙️ Setup

1. Create and activate a virtual environment.
2. Install the required Python packages.
3. Make sure FFmpeg is available in your system path.
4. Start Ollama locally.

```bash
ollama serve
```

## ▶️ How to use

### 1) Put videos in the `video/` folder

Add your course videos to the `video/` folder.

### 2) Convert video to audio

```bash
python video_file_to_mp3.py
```

### 3) Transcribe audio

```bash
python mp3_to_json.py
```

### 4) Create embeddings

```bash
python read_chunks.py
```

### 5) Ask a question

```bash
python process_chuunks.py
```

Then enter your query when prompted:

```text
Ask your query:
```

## ⚠️ Important notes

- Ollama is expected to run on `http://localhost:11434`
- The embedding model used in the code is `bge-m3`
- The answer generation model used in the code is `llama3.2`
- Generated files such as `embeddings.joblib`, `output.json`, `response.txt`, `audio/`, `video/`, and `json/` should not be committed

## 🌱 Future improvements

- Better chunk cleaning
- Better prompt formatting
- A proper web interface
- Source links and timestamps in the answer
- A one-command pipeline for the full workflow

## 📄 License

This repository includes a `LICENSE` file. Check it for usage terms.
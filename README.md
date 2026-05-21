# Rag Based AI

This project is a simple question-answering system for course videos.
It helps you ask questions about the video content and find the part of the course where the topic is taught.

The project uses three main ideas:

1. Convert video to audio
2. Transcribe audio into text chunks
3. Search the chunks with embeddings and return the most relevant answer

## What this project does

The goal of this project is to make long course videos easier to search.
Instead of watching the whole video again, you can ask a question like:

- What is this course about?
- Where is this topic explained?
- Which video covers this idea?

The system finds the most relevant subtitle chunks and then uses a local Ollama model to generate a response.

## How it works

### 1. Video to audio

The script `video_file_to_mp3.py` converts videos inside the `video/` folder into MP3 files inside the `audio/` folder.

### 2. Audio to text chunks

The script `mp3_to_json.py` uses Whisper to transcribe the audio.
It saves the result as chunk data in the `json/` folder and also creates `output.json`.

### 3. Create embeddings

The script `read_chunks.py` reads the JSON chunk files, sends each chunk to Ollama embedding API, and stores the vectors in `embeddings.joblib`.

### 4. Ask a question

The script `process_chuunks.py`:

- asks the user for a query
- creates an embedding for the query
- compares it with stored chunk embeddings
- picks the best matching chunks
- sends the selected chunks to Ollama for the final answer

## Project files

### Main scripts

- `video_file_to_mp3.py` - converts video files to audio
- `mp3_to_json.py` - transcribes audio and creates chunk JSON
- `read_chunks.py` - creates embeddings for the chunks
- `process_chuunks.py` - answers user questions using similarity search

### Data folders

- `video/` - source video files
- `audio/` - extracted MP3 files
- `json/` - transcript chunks in JSON format
- `embeddings.joblib` - saved chunk embeddings and metadata

### Other files

- `prompt.txt` - prompt sent to the local model
- `response.txt` - saved final model response
- `whisper/` - local Whisper package source used by the project

## Requirements

You need these tools installed on your machine:

- Python
- FFmpeg
- Ollama

You also need Python packages such as:

- requests
- pandas
- numpy
- scikit-learn
- joblib
- whisper
- typer

## Setup

1. Create and activate a virtual environment.
2. Install the required Python packages.
3. Make sure FFmpeg is available in your system path.
4. Start Ollama locally with the embedding and chat models you want to use.

Example:

```bash
ollama serve
```

## How to use

### Step 1: Put videos in the video folder

Add your course videos to the `video/` folder.

### Step 2: Convert video to audio

Run the video conversion script:

```bash
python video_file_to_mp3.py
```

### Step 3: Transcribe audio

Run the transcription script:

```bash
python mp3_to_json.py
```

### Step 4: Create embeddings

Run the embedding script:

```bash
python read_chunks.py
```

### Step 5: Ask a question

Run the question-answering script:

```bash
python process_chuunks.py
```

Then type your question when the script asks:

```text
Ask your query:
```

## Important notes

- The project expects Ollama to run on `http://localhost:11434`.
- The embedding model used in the code is `bge-m3`.
- The answer generation model used in the code is `llama3.2`.
- Some generated files should not be committed to git, such as `embeddings.joblib`, `output.json`, `response.txt`, `audio/`, `video/`, and `json/`.

## Current status of the project

These are the main things already done in this project:

- video files are converted into audio
- audio is transcribed into subtitle chunks
- chunks are saved into JSON form
- embeddings are created for every chunk
- user questions are matched with the most relevant chunks
- a local model generates the final answer

## Future improvements

You can improve this project by adding:

- better chunk cleaning
- a proper web interface
- better prompt formatting
- source links and timestamps in the answer
- a single command pipeline for all steps

## License

This repository includes a `LICENSE` file. Check it for usage terms.
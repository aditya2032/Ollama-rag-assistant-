# Local RAG Assistant with Ollama

This is a simple question-answering application that runs completely on your own computer. It uses a local AI model through **Ollama** and a clean web interface built with **Streamlit**.

You can ask questions about the information saved in the knowledge-base file. The application finds the most relevant information first, then uses the local AI model to write an answer.

No OpenAI key, cloud account, or paid API is required.

## What this application does

1. Reads information from `data/knowledge_base.txt`.
2. Finds the most relevant lines for your question.
3. Gives those lines to a local AI model.
4. Shows an answer and lets you inspect the retrieved context.

## Before you start

You need a Windows computer with an internet connection for the first-time downloads. You also need about 4 GB of free disk space for the local AI models.

## Step 1: Download this project

If you received this project as a ZIP file:

1. Right-click the ZIP file.
2. Choose **Extract All**.
3. Open the extracted `ollama-rag-assistant` folder.

Keep this folder somewhere easy to find, such as `Documents` or `Desktop`.

## Step 2: Install Ollama

Ollama runs the AI models locally on your computer.

1. Open [Ollama Download](https://ollama.com/download).
2. Download the **Windows** installer.
3. Run the downloaded installer and follow the on-screen instructions.
4. After it finishes, open a new **PowerShell** window.
5. Check that Ollama works:

```powershell
ollama --version
```

If you see a version number, Ollama is installed correctly.

## Step 3: Install uv

This project uses **uv** to install and run Python packages.

1. Open **PowerShell**.
2. Copy and run this command:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

3. Close PowerShell completely.
4. Open a new PowerShell window.
5. Confirm the installation:

```powershell
uv --version
```

If you see a version number, uv is ready.

## Step 4: Download the AI models

Open PowerShell and run these two commands. They download the models only once.

```powershell
ollama pull hf.co/CompendiumLabs/bge-base-en-v1.5-gguf
ollama pull hf.co/bartowski/Llama-3.2-1B-Instruct-GGUF
```

The first model helps the app find relevant information. The second model writes the final answer.

## Step 5: Open the project folder in PowerShell

In File Explorer, open the extracted `ollama-rag-assistant` folder.

Click the address bar, type `powershell`, and press **Enter**. A PowerShell window will open directly inside the project folder.

Alternatively, use `cd` with the location of your folder. For example:

```powershell
cd "C:\Users\YourName\Documents\ollama-rag-assistant"
```

## Step 6: Install the app dependencies

Run:

```powershell
uv sync
```

Wait for this command to finish. It creates the project environment and installs Streamlit and the Ollama Python library.

## Step 7: Start the application

Run:

```powershell
uv run streamlit run app.py
```

After a few seconds, PowerShell will display a link similar to this:

```text
http://localhost:8501
```

Open that link in your browser. The Local RAG Assistant is now ready to use.

To stop the app later, return to PowerShell and press `Ctrl + C`.

## How to use the app

1. Type a question in the chat box, such as: `How long do cats sleep?`
2. Press Enter.
3. Wait for the local AI response.
4. Open **Retrieved context** to see the knowledge-base lines used for the answer.
5. Use the **Context chunks** slider in the sidebar to choose how many relevant lines are sent to the AI.

## Add your own information

Open this file in a text editor:

```text
data/knowledge_base.txt
```

Add one complete fact or short paragraph on each new line. For example:

```text
Our library opens from 9 AM to 5 PM on weekdays.
Students can borrow up to four books at one time.
The computer lab is located on the second floor.
```

Save the file, stop the app with `Ctrl + C`, and start it again:

```powershell
uv run streamlit run app.py
```

The application will include your new information when answering questions.

## Project files

```text
ollama-rag-assistant/
├── app.py                     Main application file to run
├── data/
│   └── knowledge_base.txt     Your questions are answered from this file
├── src/                       Application logic
├── pyproject.toml             uv dependency configuration
├── requirements.txt           Dependency list for reference
└── README.md                  This guide
```

## Troubleshooting

### `uv` is not recognized

Close PowerShell, open it again, then run `uv --version`. If it still fails, repeat the uv installation step above.

### `ollama` is not recognized

Install Ollama from [ollama.com/download](https://ollama.com/download), then close and reopen PowerShell.

### The application says Ollama is unavailable

Open the Ollama application from the Windows Start menu. Wait a few seconds and refresh the Streamlit page. You can also check it with:

```powershell
ollama list
```

### A model cannot be found

Run the two `ollama pull` commands from Step 4 again.

### Port 8501 is already in use

Run the app on another port:

```powershell
uv run streamlit run app.py --server.port 8502
```

Then open `http://localhost:8502`.

## Technology used

- Python
- Streamlit for the user interface
- Ollama for locally running embedding and language models
- Cosine similarity for finding relevant knowledge-base chunks
- uv for dependency management
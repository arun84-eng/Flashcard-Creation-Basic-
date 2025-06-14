# Flashcard-Creation-Basic-
Turn educational content into structured flashcards using either a remote Hugging Face API or a local language model like google/flan-t5-small.

🚀 Features
Generate Q&A flashcards from text or uploaded files.

Choose from preconfigured LLMs (e.g., flan-t5-small, flan-t5-xxl).

Supports both API-based inference and local model inference.

Adjustable number of flashcards per request.

Flashcards include:

Question

Answer

Difficulty

Topic

🖥️ Local Setup
1. Clone the Repository
bash
Copy
Edit
git clone https://github.com/your-username/flashcard-generator.git
cd flashcard-generator
2. Create Virtual Environment
bash
Copy
Edit
python -m venv .venv
source .venv/Scripts/activate  # or source .venv/bin/activate (Linux/Mac)
3. Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
Make sure you have transformers, torch, streamlit, and huggingface_hub installed.

⚙️ Configuration
You can run the app in two modes:

🔑 API Mode
Get your API key from HuggingFace:

https://huggingface.co/settings/tokens

In the Streamlit sidebar, paste the API key.

Select a model like google/flan-t5-xxl.

🖥️ Local Model Mode
Check "Use Local Model" in the Streamlit sidebar.

No API key required.

The app will load flan-t5-small locally using Transformers.

▶️ Running the App
bash
Copy
Edit
streamlit run app.py
Paste educational content or upload a .txt/.pdf file.

Select the model and number of flashcards.

Click Generate.

Flashcards will be displayed below.

📁 Project Structure
graphql
Copy
Edit
flashcard-generator/
│
├── app.py                 # Streamlit main UI
├── local_generate.py      # Local model inference logic
├── api_generate.py        # Hugging Face API inference logic
├── utils.py               # Utility functions
├── requirements.txt
└── README.md

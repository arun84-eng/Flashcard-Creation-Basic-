import streamlit as st
import json
import os
from dotenv import load_dotenv
from utils.file_processor import FileProcessor
from utils.llm_client import LLMClient
from utils.flashcard_generator import FlashcardGenerator
from utils.export_utils import ExportUtils

# Page configuration
st.set_page_config(
    page_title="LLM-Powered Flashcard Generator",
    page_icon="🧠",
    layout="wide"
)

# Initialize session state
if 'flashcards' not in st.session_state:
    st.session_state.flashcards = []
if 'generated' not in st.session_state:
    st.session_state.generated = False

def generate_demo_flashcards(content: str, subject: str, num_cards: int):
    import re
    words = re.findall(r'\b[A-Z][a-z]+\b|\b[a-z]{4,}\b', content)
    key_terms = list(set([word for word in words if len(word) > 3]))[:num_cards]

    demo_cards = []
    for i, term in enumerate(key_terms[:num_cards]):
        demo_cards.append({
            'id': i + 1,
            'question': f"What is {term}?",
            'answer': f"{term} is an important concept in {subject}. (Demo mode - for full AI-generated content, configure API key)",
            'subject': subject,
            'difficulty': 'Medium',
            'topic': term.capitalize()
        })

    while len(demo_cards) < num_cards:
        demo_cards.append({
            'id': len(demo_cards) + 1,
            'question': f"What is a key concept in {subject}?",
            'answer': f"This is a demo flashcard for {subject}. Configure API key for AI-generated content.",
            'subject': subject,
            'difficulty': 'Easy',
            'topic': 'General'
        })

    return demo_cards

def main():
    load_dotenv()
    default_model = os.getenv("MODEL_NAME", "google/flan-t5-small")

    st.title("🧠 LLM-Powered Flashcard Generator")
    st.markdown("Transform your educational content into effective Q&A flashcards using AI")

    # Sidebar
    with st.sidebar:
        st.header("Configuration")

        use_local = st.checkbox("✅ Use Local Model", value=True)

        if not use_local:
            api_key = st.text_input("🔑 Enter Hugging Face API Key", type="password")
        else:
            api_key = None

        subject = st.selectbox(
            "Subject Type",
            ["General", "Biology", "History", "Computer Science", "Mathematics", 
             "Physics", "Chemistry", "Literature", "Psychology", "Economics"],
            help="Select the subject to optimize flashcard generation"
        )

        # Model selection with default from .env
        model_options = [
            "google/flan-t5-small",
            "google/flan-t5-base",
            "google/flan-t5-large",
            "google/flan-t5-xxl"
        ]
        model = st.selectbox(
            "LLM Model",
            model_options,
            index=model_options.index(default_model) if default_model in model_options else 0,
            help="Choose the language model for flashcard generation"
        )

        num_cards = st.slider(
            "Number of Flashcards",
            min_value=5,
            max_value=25,
            value=15,
            help="Number of flashcards to generate"
        )

    col1, col2 = st.columns([1, 1])
    content = ""

    with col1:
        st.header("📝 Input Content")
        input_method = st.radio("Choose input method:", ["Direct Text Input", "File Upload"])

        if input_method == "Direct Text Input":
            content = st.text_area(
                "Paste your educational content here:",
                height=300,
                placeholder="Enter textbook excerpts, lecture notes, or any educational material..."
            )
        else:
            uploaded_file = st.file_uploader(
                "Upload your educational content:",
                type=['txt', 'pdf'],
                help="Supported formats: .txt, .pdf"
            )
            if uploaded_file:
                try:
                    file_processor = FileProcessor()
                    content = file_processor.process_file(uploaded_file)
                    st.success(f"Successfully processed {uploaded_file.name}")
                    with st.expander("Preview extracted content"):
                        st.text_area("Extracted text:", content[:1000] + "..." if len(content) > 1000 else content, height=150)
                except Exception as e:
                    st.error(f"Error processing file: {str(e)}")

        if st.button("🚀 Generate Flashcards", type="primary", disabled=not content):
            if not content.strip():
                st.error("Please provide some educational content to process.")
            elif use_local:
                with st.spinner("Generating flashcards locally..."):
                    try:
                        llm_client = LLMClient(api_key, model, use_local=True)
                        flashcard_gen = FlashcardGenerator(llm_client)
                        flashcards = flashcard_gen.generate_flashcards(content, subject, num_cards)
                        if flashcards:
                            st.session_state.flashcards = flashcards
                            st.session_state.generated = True
                            st.success(f"Successfully generated {len(flashcards)} flashcards using local model!")
                        else:
                            st.error("No flashcards were generated. Please check your content and try again.")
                    except Exception as e:
                        st.error(f"Error generating flashcards: {str(e)}")
            else:
                with st.spinner("Generating flashcards using API..."):
                    try:
                        llm_client = LLMClient(api_key, model)
                        st.info("Testing API connection...")
                        if not llm_client.test_connection():
                            st.error("Failed to connect to the API. Please check your API key and model selection.")
                            st.stop()

                        st.info("API connection successful. Generating flashcards...")
                        flashcard_gen = FlashcardGenerator(llm_client)
                        flashcards = flashcard_gen.generate_flashcards(content, subject, num_cards)

                        if flashcards:
                            st.session_state.flashcards = flashcards
                            st.session_state.generated = True
                            st.success(f"Successfully generated {len(flashcards)} flashcards!")
                        else:
                            st.error("No flashcards were generated. Please check your content and try again.")

                    except Exception as e:
                        st.error(f"Error generating flashcards: {str(e)}")

    with col2:
        st.header("🎴 Generated Flashcards")
        if st.session_state.generated and st.session_state.flashcards:
            for i, card in enumerate(st.session_state.flashcards):
                with st.expander(f"Flashcard {i+1}: {card['question'][:50]}..."):
                    st.markdown(f"**Question:** {card['question']}")
                    st.markdown(f"**Answer:** {card['answer']}")
                    if 'difficulty' in card:
                        st.markdown(f"**Difficulty:** {card['difficulty']}")
                    if 'topic' in card:
                        st.markdown(f"**Topic:** {card['topic']}")

            st.header("📤 Export Flashcards")
            export_utils = ExportUtils()

            col_csv, col_json = st.columns(2)

            with col_csv:
                csv_data = export_utils.to_csv(st.session_state.flashcards)
                st.download_button("Download CSV", csv_data, "flashcards.csv", "text/csv")

            with col_json:
                json_data = export_utils.to_json(st.session_state.flashcards)
                st.download_button("Download JSON", json_data, "flashcards.json", "application/json")

            if st.button("🗑️ Clear Flashcards"):
                st.session_state.flashcards = []
                st.session_state.generated = False
                st.rerun()
        else:
            st.info("Generate flashcards from your educational content to see them here.")

if __name__ == "__main__":
    main()

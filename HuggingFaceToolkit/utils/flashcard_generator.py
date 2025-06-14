class FlashcardGenerator:
    def __init__(self, llm_client):
        self.llm_client = llm_client

    def generate_flashcards(self, content, subject, num_cards):
        # Split into chunks or keywords
        # Example basic logic for flashcards
        questions = self.extract_keywords(content)[:num_cards]
        flashcards = []
        for i, keyword in enumerate(questions):
            prompt = f"Generate a flashcard question and answer about: {keyword} in the context of {subject}."
            answer = self.llm_client.generate(prompt)
            flashcards.append({
                'id': i + 1,
                'question': f"What is {keyword}?",
                'answer': answer,
                'subject': subject,
                'difficulty': 'Medium',
                'topic': keyword
            })
        return flashcards

    def extract_keywords(self, content):
        import re
        words = re.findall(r'\b[a-zA-Z]{4,}\b', content)
        return list(set(words))[:25]

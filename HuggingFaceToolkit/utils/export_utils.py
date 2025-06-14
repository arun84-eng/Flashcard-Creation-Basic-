import json
import csv
import io
from typing import List, Dict, Any

class ExportUtils:
    """Utilities for exporting flashcards in different formats"""
    
    def to_csv(self, flashcards: List[Dict[str, Any]]) -> str:
        """
        Export flashcards to CSV format
        
        Args:
            flashcards: List of flashcard dictionaries
            
        Returns:
            str: CSV formatted string
        """
        if not flashcards:
            return ""
        
        output = io.StringIO()
        fieldnames = ['id', 'question', 'answer', 'subject', 'difficulty', 'topic']
        
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        
        for card in flashcards:
            # Ensure all required fields exist
            row = {
                'id': card.get('id', ''),
                'question': card.get('question', ''),
                'answer': card.get('answer', ''),
                'subject': card.get('subject', ''),
                'difficulty': card.get('difficulty', ''),
                'topic': card.get('topic', '')
            }
            writer.writerow(row)
        
        return output.getvalue()
    
    def to_json(self, flashcards: List[Dict[str, Any]]) -> str:
        """
        Export flashcards to JSON format
        
        Args:
            flashcards: List of flashcard dictionaries
            
        Returns:
            str: JSON formatted string
        """
        if not flashcards:
            return "[]"
        
        export_data = {
            "flashcards": flashcards,
            "metadata": {
                "total_cards": len(flashcards),
                "subjects": list(set(card.get('subject', '') for card in flashcards)),
                "difficulties": list(set(card.get('difficulty', '') for card in flashcards)),
                "export_format": "LLM Flashcard Generator v1.0"
            }
        }
        
        return json.dumps(export_data, indent=2, ensure_ascii=False)
    
    def to_anki_format(self, flashcards: List[Dict[str, Any]]) -> str:
        """
        Export flashcards in Anki-compatible format
        
        Args:
            flashcards: List of flashcard dictionaries
            
        Returns:
            str: Anki formatted string (tab-separated)
        """
        if not flashcards:
            return ""
        
        output = io.StringIO()
        
        for card in flashcards:
            question = card.get('question', '').replace('\t', ' ').replace('\n', '<br>')
            answer = card.get('answer', '').replace('\t', ' ').replace('\n', '<br>')
            
            # Anki format: Front\tBack\tTags
            tags = f"{card.get('subject', '')} {card.get('difficulty', '')} {card.get('topic', '')}"
            tags = tags.strip().replace(' ', '_')
            
            output.write(f"{question}\t{answer}\t{tags}\n")
        
        return output.getvalue()
    
    def to_quizlet_format(self, flashcards: List[Dict[str, Any]]) -> str:
        """
        Export flashcards in Quizlet-compatible format
        
        Args:
            flashcards: List of flashcard dictionaries
            
        Returns:
            str: Quizlet formatted string (tab-separated)
        """
        if not flashcards:
            return ""
        
        output = io.StringIO()
        
        for card in flashcards:
            question = card.get('question', '').replace('\t', ' ')
            answer = card.get('answer', '').replace('\t', ' ')
            
            # Quizlet format: Term\tDefinition
            output.write(f"{question}\t{answer}\n")
        
        return output.getvalue()

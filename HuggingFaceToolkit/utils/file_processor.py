import streamlit as st
import PyPDF2
import io
from typing import Optional

class FileProcessor:
    """Handle file processing for different formats"""
    
    def process_file(self, uploaded_file) -> str:
        """
        Process uploaded file and extract text content
        
        Args:
            uploaded_file: Streamlit uploaded file object
            
        Returns:
            str: Extracted text content
        """
        if uploaded_file is None:
            return ""
        
        file_extension = uploaded_file.name.split('.')[-1].lower()
        
        if file_extension == 'txt':
            return self._process_txt_file(uploaded_file)
        elif file_extension == 'pdf':
            return self._process_pdf_file(uploaded_file)
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")
    
    def _process_txt_file(self, uploaded_file) -> str:
        """Process text file"""
        try:
            # Read the file content
            content = uploaded_file.read()
            
            # Try to decode as UTF-8, fallback to other encodings if needed
            try:
                text = content.decode('utf-8')
            except UnicodeDecodeError:
                try:
                    text = content.decode('latin-1')
                except UnicodeDecodeError:
                    text = content.decode('cp1252')
            
            return text.strip()
            
        except Exception as e:
            raise Exception(f"Error processing text file: {str(e)}")
    
    def _process_pdf_file(self, uploaded_file) -> str:
        """Process PDF file and extract text"""
        try:
            # Create a PDF reader object
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))
            
            text = ""
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text() + "\n"
            
            if not text.strip():
                raise Exception("No text could be extracted from the PDF. The PDF might contain only images or be password protected.")
            
            return text.strip()
            
        except Exception as e:
            raise Exception(f"Error processing PDF file: {str(e)}")
    
    def preprocess_content(self, content: str) -> str:
        """
        Preprocess extracted content for better LLM processing
        
        Args:
            content: Raw extracted text content
            
        Returns:
            str: Preprocessed content
        """
        if not content:
            return ""
        
        # Remove excessive whitespace
        lines = [line.strip() for line in content.split('\n')]
        lines = [line for line in lines if line]  # Remove empty lines
        
        # Join lines with single newlines
        processed_content = '\n'.join(lines)
        
        # Limit content length to prevent API issues
        max_length = 8000  # Adjust based on model limits
        if len(processed_content) > max_length:
            processed_content = processed_content[:max_length] + "..."
        
        return processed_content

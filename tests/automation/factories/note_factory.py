"""
Note factory for generating test note data.
"""

from typing import Dict

from faker import Faker

fake = Faker()


class NoteFactory:
    """Factory for creating test note objects."""
    
    @staticmethod
    def create(
        title: str = None,
        content: str = None,
        **kwargs
    ) -> Dict[str, str]:
        """
        Create a test note object.
        
        Args:
            title: Note title (default: random generated)
            content: Note content (default: random paragraph)
            **kwargs: Additional fields to include
            
        Returns:
            Dictionary with note data
        """
        note_data = {
            "title": title or f"Test Note - {fake.word()}",
            "content": content or fake.paragraph(nb_sentences=5),
        }
        
        note_data.update(kwargs)
        return note_data
    
    @staticmethod
    def create_minimal() -> Dict[str, str]:
        """Create minimal note with only required fields."""
        return NoteFactory.create()
    
    @staticmethod
    def create_long_content() -> Dict[str, str]:
        """Create note with extensive content."""
        return NoteFactory.create(
            content=fake.paragraph(nb_sentences=50)
        )
    
    @staticmethod
    def create_batch(count: int = 3) -> list[Dict[str, str]]:
        """Create multiple note objects."""
        return [NoteFactory.create() for _ in range(count)]

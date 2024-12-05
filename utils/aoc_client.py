import os
import requests
from pathlib import Path
from datetime import datetime
from bs4 import BeautifulSoup

class AocClient:
    def __init__(self, session_token=None):
        self.session_token = session_token or os.getenv('AOC_SESSION')
        if not self.session_token:
            raise ValueError("Session token required. Set AOC_SESSION environment variable or pass token directly.")

        self.base_url = "https://adventofcode.com"
        self.year = datetime.now().year
        self.session = requests.Session()
        self.session.cookies.set('session', self.session_token)

    def get_input(self, day: int) -> str:
        """Fetch the input for a specific day and cache it locally."""
        cache_dir = Path(f"inputs/{self.year}")
        cache_dir.mkdir(parents=True, exist_ok=True)

        cache_file = cache_dir / f"day_{day:02d}.txt"
        if cache_file.exists():
            return cache_file.read_text()

        response = self.session.get(f"{self.base_url}/{self.year}/day/{day}/input")
        response.raise_for_status()

        input_text = response.text.rstrip('\n')  # Remove trailing newlines
        cache_file.write_text(input_text)
        return input_text

    def get_puzzle_text(self, day: int) -> str:
        """Fetch the puzzle description."""
        response = self.session.get(f"{self.base_url}/{self.year}/day/{day}")
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        article = soup.find('article', class_='day-desc')
        return article.get_text() if article else "Could not fetch puzzle text"

    def submit_answer(self, day: int, part: int, answer: str) -> str:
        """Submit an answer and return the response message."""
        if part not in (1, 2):
            raise ValueError("Part must be 1 or 2")

        response = self.session.post(
            f"{self.base_url}/{self.year}/day/{day}/answer",
            data={'level': str(part), 'answer': str(answer)}
        )
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        message = soup.find('article').get_text()
        return message.strip() 

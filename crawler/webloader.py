import requests
from bs4 import BeautifulSoup
# from langchain_core.documents import Document
from readability import Document
from urllib.parse import urlparse 

from utils.logger import setup_logger

logger = setup_logger("crawler")


class WebsiteLoader:
    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.headers = {
            "User-Agent": "Mozilla/5.0"
        }

    def validate_url(self, url: str):
        ''' Function to validate the url '''


        parsed = urlparse(url)
        return parsed.scheme in ["http", "https"]

    def load(self, url: str):

        ''' Function to load the content of the website '''

        
        if not self.validate_url(url):
            raise ValueError("Invalid URL format")

        try:
            logger.info(f"Starting website extraction: {url}")
            response = requests.get(
                url,
                headers=self.headers,
                timeout=self.timeout
            )
        
            if response.status_code != 200:
                raise ValueError("Unable to reach the website")

            content_type = response.headers.get("Content-Type", "")
            if "text/html" not in content_type:
                raise ValueError("Unsupported content type")

            soup = BeautifulSoup(response.text, 'html.parser')

            # Remove script and style elements
            for unwanted_tag in soup(["script", "style"]):
                unwanted_tag.decompose()

            text = soup.get_text(separator=" ", strip=True)

            final_text="\n".join(text) 

            logger.info(f"Text extraction completed : {len(text)}")
            return {
                "text": text,
                "metadata": {
                    "source_url": url,
                    "title": soup.title.string if soup.title else ""
                }
            }
            

        except requests.exceptions.RequestException as e:
            return f"Error fetching the URL: {e}"

        
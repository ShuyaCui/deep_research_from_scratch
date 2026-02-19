import time
from functools import cached_property
from azure.identity import ChainedTokenCredential, DefaultAzureCredential
import json
from dotenv import load_dotenv as _load_dotenv

_load_dotenv()
# Create a token manager that will be reused
class GenAIToken:
    """Module provides a class, GenAIToken, that represents a token for the GenAI service."""

    _token: str
    _expires_on: int

    def __init__(
        self,
        refresh_threshold: int = 1 * 60,
        cognitive_services: str = "https://cognitiveservices.azure.com/.default",
    ):
        """Initialize the GenAIToken object.

        Args:
            refresh_threshold (int): The threshold in seconds for refreshing the token.
                                    Default is 3600 seconds (1 hour).
            cognitive_services (str): The URL of the cognitive services endpoint.
                                    Default is "https://cognitiveservices.azure.com/.default".
        """
        self._refresh_threshold = refresh_threshold
        self._cognitive_services = cognitive_services
        self._token, self._expires_on = self._get_token()

    @cached_property
    def _credentials(self) -> ChainedTokenCredential:
        """Return the credentials for accessing the Azure services.

        Returns:
            ChainedTokenCredential: The credentials object.
        """
        return DefaultAzureCredential(exclude_interactive_browser_credential=False)

    def _get_token(self) -> tuple[str, int]:
        """Get the token and its expiration time.

        Returns:
            tuple[str, int]: The token and its expiration time.
        """
        token = self._credentials.get_token(self._cognitive_services)
        return token.token, token.expires_on

    def token(self) -> str:
        """Return the token.

        If the token is expired or about to expire, it will be refreshed.

        Returns:
            str: The token.
        """
        if self._expires_on < time.time() + self._refresh_threshold:
            self._token, self._expires_on = self._get_token()
        return self._token

def determine_mime_type(filename: str) -> str:
    """Determine the MIME type of a file based on its extension."""
    mime_types = {
        'pdf': 'application/pdf',
        'mp3': 'audio/mpeg',
        'mpeg': 'audio/mpeg',
        'wav': 'audio/wav',
        'png': 'image/png',
        'jpeg': 'image/jpeg',
        'jpg': 'image/jpeg',
        'webp': 'image/webp',
        'txt': 'text/plain',
        'csv': 'text/plain',
        'mov': 'video/mov',
        'mp4': 'video/mp4',
        'mpg': 'video/mpg',
        'avi': 'video/avi',
        'wmv': 'video/wmv',
        'mpegps': 'video/mpegps',
        'flv': 'video/flv'
    }

    file_extension = filename.split('.')[-1].lower()
    mime_type = mime_types.get(file_extension)

    if mime_type is None:
        raise ValueError(f"Unknown file extension: {file_extension}")

    return mime_type
    """Load cached results from a JSON file"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            cached_results = json.load(f)
        print(f"Cached results loaded from {filename}")
        return cached_results
    except FileNotFoundError:
        print(f"File {filename} not found. Starting with empty cache.")
        return {}

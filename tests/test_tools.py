import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Mock Streamlit secrets before importing app modules that use them
with patch("streamlit.secrets", {"OPENAI_API_KEY": "sk-fake-key", "REDDIT_CLIENT_ID": "fake", "REDDIT_CLIENT_SECRET": "fake", "NEWS_API_KEY": "fake", "TWITTER_BEARER_TOKEN": "fake"}):
    from app.chat_engine import get_chat_engine
    from app.retriever import fetch_reddit_posts

class TestFinFriend(unittest.TestCase):
    
    @patch("app.retriever.requests.post")
    @patch("app.retriever.requests.get")
    def test_reddit_fetch(self, mock_get, mock_post):
        # Mock Reddit Auth
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"access_token": "fake-token"}
        
        # Mock Reddit Post Fetch
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "data": {
                "children": [
                    {"data": {"title": "Test Post", "selftext": "Content"}}
                ]
            }
        }

        posts = fetch_reddit_posts()
        self.assertTrue(len(posts) > 0)
        self.assertIn("[Reddit]", posts[0])

    @patch("app.chat_engine.ChatOpenAI")
    def test_agent_initialization(self, mock_llm):
        # Just test if we can get the agent without crashing
        agent = get_chat_engine()
        self.assertIsNotNone(agent)

if __name__ == "__main__":
    unittest.main()

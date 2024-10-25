import pytest
from backend.services.flask_client_binding import FlaskClientBinding

client = FlaskClientBinding(base_url="http://localhost:5000")

def test_start_conversation():
    """Test starting a new conversation."""
    conversation = client.start_conversation()
    print('TEST 1, Testing conversion: '+conversation)
    assert 'conversation_id' in conversation

def test_send_message():
    """Test sending a message in a conversation."""
    conversation = client.start_conversation()
    conversation_id = conversation['conversation_id']
    message_response = client.send_message(conversation_id, "Test message")
    print(message_response)
    assert message_response['assistant_reply'] is not None

def test_get_conversation_messages():
    """Test retrieving messages in a conversation."""
    conversation = client.start_conversation()
    conversation_id = conversation['conversation_id']
    client.send_message(conversation_id, "Test message")
    messages = client.get_conversation_messages(conversation_id)
    assert len(messages) > 0

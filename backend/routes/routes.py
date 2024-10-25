# backend/routes/routes.py
import json
from flask import Blueprint, request, jsonify
from ..models import Conversation, Message
from ..db import db
from ..client.openai_client import OpenAIClient

chat_bp = Blueprint('chat_bp', __name__)

# Initialize the OpenAI client
openai_client = OpenAIClient()

@chat_bp.route('/conversations', methods=['POST'])
def start_conversation():
    """Start a new conversation."""
    new_conversation = Conversation()
    db.session.add(new_conversation)
    db.session.commit()
    return jsonify({
        'message': 'Conversation started',
        'conversation_id': new_conversation.id
    }), 201

@chat_bp.route('/conversations/<int:conversation_id>/messages', methods=['POST'])
def send_message(conversation_id):
    """Send a message in a conversation and get a response from the assistant."""

    content = request.json.get('content')
    if not content:
        return jsonify({'error': 'Message content is required'}), 400
        

    conversation = Conversation.query.get_or_404(conversation_id)

    #You can extend query param functionality here
    #model_version = request.args.get('model_version', default='gpt-3.5-turbo')

    user_message = Message(
        conversation_id=conversation.id,
        content=content,
        role='user'
    )
    db.session.add(user_message)
    db.session.commit()

    # retrieves all previous messages in the conversation to maintain context.
    previous_messages = Message.query.filter_by(
        conversation_id=conversation.id
    ).order_by(Message.timestamp).all()

    # prepares the messages for the OpenAI API and sends a request to get a response.
    messages = [{'role': msg.role, 'content': msg.content} for msg in previous_messages]

    # Get response from OpenAI
    assistant_response = openai_client.get_response(messages)
    assistant_response_dict = json.loads(assistant_response)

    # Print the entire dictionary to see the structure
    # print(assistant_response_dict)

    # Get the assistant's message content...the first one
    message_content = assistant_response_dict.get('choices', [{}])[0].get('message', {}).get('content', '')

    if assistant_response is None:
        return jsonify({'error': 'Failed to get response from OpenAI API'}), 500

    # Save assistant's message to the database
    assistant_message = Message(
        conversation_id=conversation.id,
        content=assistant_response,
        role='assistant'
    )
    db.session.add(assistant_message)
    db.session.commit()

    return jsonify({
        'message': 'Assistant response received',
        'conversation_id': conversation.id,
        'assistant_reply': message_content
    }), 201

@chat_bp.route('/conversations/<int:conversation_id>/messages', methods=['GET'])
def get_conversation_messages(conversation_id):
    """Retrieve all messages in a conversation."""
    conversation = Conversation.query.get_or_404(conversation_id)
    messages = Message.query.filter_by(
        conversation_id=conversation.id
    ).order_by(Message.timestamp).all()

    return jsonify([
        {
            'id': msg.id,
            'role': msg.role,
            'content': msg.content,
            'timestamp': msg.timestamp.isoformat()
        } for msg in messages
    ]), 200

@chat_bp.route('/conversations/messages', methods=['GET'])
def get_all_messages():
    """Retrieve all messages across all conversations."""
    messages = Message.query.order_by(Message.timestamp).all()

    return jsonify([
        {
            'id': msg.id,
            'conversation_id': msg.conversation_id,
            'role': msg.role,
            'content': msg.content,
            'timestamp': msg.timestamp.isoformat()
        } for msg in messages
    ]), 200

@chat_bp.route('/conversations/<int:conversation_id>/messages', methods=['DELETE'])
def clear_conversation(conversation_id):
    """Delete all messages from a specific conversation."""
    conversation = Conversation.query.get_or_404(conversation_id)
    Message.query.filter_by(conversation_id=conversation.id).delete()
    db.session.commit()

    return jsonify({
        'message': f'All messages from conversation {conversation_id} have been cleared'
    }), 200

@chat_bp.route('/conversations/<int:conversation_id>', methods=['DELETE'])
def delete_conversation(conversation_id):
    """Delete a conversation and all associated messages."""
    conversation = Conversation.query.get_or_404(conversation_id)
    Message.query.filter_by(conversation_id=conversation.id).delete()
    db.session.delete(conversation)
    db.session.commit()

    return jsonify({
        'message': f'Conversation {conversation_id} has been deleted'
    }), 200


@chat_bp.route('/customer-support/<int:conversation_id>/messages', methods=['POST'])
def send_customer_support_message(conversation_id):
    """Send a customer support message in an existing conversation and get the assistant's response."""
    content = request.json.get('content')
    if not content:
        return jsonify({'error': 'Message content is required'}), 400

    conversation = Conversation.query.get_or_404(conversation_id)

    user_message = Message(
        conversation_id=conversation.id,
        content=content,
        role='user'
    )
    db.session.add(user_message)
    db.session.commit()

    previous_messages = Message.query.filter_by(
        conversation_id=conversation.id
    ).order_by(Message.timestamp).all()

    context = [{'role': msg.role, 'content': msg.content} for msg in previous_messages]

    assistant_response = openai_client.get_customer_support_response(content, context)
    if assistant_response is None:
        return jsonify({'error': 'Failed to get response from OpenAI API'}), 500

    assistant_message = Message(
        conversation_id=conversation.id,
        content=assistant_response,
        role='assistant'
    )
    db.session.add(assistant_message)
    db.session.commit()

    return jsonify({
        'message': 'Assistant response received',
        'conversation_id': conversation.id,
        'assistant_reply': assistant_message.content
    }), 201

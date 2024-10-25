import requests
import json

class FlaskClientBinding:
    def __init__(self, base_url):
        self.base_url = base_url

    def start_conversation(self):
        """Start a new conversation."""
        url = f"{self.base_url}/conversations"
        response = requests.post(url)
        if response.status_code == 201:
            return response.json()
        else:
            raise Exception(f"Failed to start conversation: {response.status_code} - {response.text}")

    def send_message(self, conversation_id, content):
        """Send a message in an existing conversation and get the assistant's response."""
        url = f"{self.base_url}/conversations/{conversation_id}/messages"
        payload = {'content': content}
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, data=json.dumps(payload), headers=headers)

        if response.status_code == 201:
            return response.json()
        else:
            raise Exception(f"Failed to send message: {response.status_code} - {response.text}")

    def get_conversation_messages(self, conversation_id):
        """Retrieve all messages in a specific conversation."""
        url = f"{self.base_url}/conversations/{conversation_id}/messages"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to retrieve messages: {response.status_code} - {response.text}")

    def get_all_messages(self):
        """Retrieve all messages across all conversations."""
        url = f"{self.base_url}/conversations/messages"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to retrieve all messages: {response.status_code} - {response.text}")

    def clear_conversation(self, conversation_id):
        """Delete all messages in a conversation."""
        url = f"{self.base_url}/conversations/{conversation_id}/messages"
        response = requests.delete(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to clear conversation: {response.status_code} - {response.text}")

    def delete_conversation(self, conversation_id):
        """Delete a conversation and all associated messages."""
        url = f"{self.base_url}/conversations/{conversation_id}"
        response = requests.delete(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to delete conversation: {response.status_code} - {response.text}")


class CustomerSupportClient(FlaskClientBinding):
    def __init__(self, base_url):
        super().__init__(base_url)
        self.servicenow_client = ServiceNowClient()  # Initialize ServiceNow client

    def send_customer_support_message(self, conversation_id, content):
        """Send a customer support message in an existing conversation and get the assistant's response."""
        url = f"{self.base_url}/customer-support/{conversation_id}/messages"
        payload = {'content': content}
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, data=json.dumps(payload), headers=headers)

        if response.status_code == 201:
            return response.json()
        else:
            # If the message fails, escalate by creating a ServiceNow ticket
            self.escalate_to_servicenow(conversation_id, content)
            raise Exception(f"Failed to send customer support message: {response.status_code} - {response.text}")

    def escalate_to_servicenow(self, conversation_id, content):
        """Escalate the issue by creating a ticket in ServiceNow."""
        ticket_created = self.servicenow_client.create_ticket(conversation_id, content)
        if ticket_created:
            print(f"Ticket successfully created in ServiceNow for conversation {conversation_id}.")
        else:
            raise Exception("Failed to create a ticket in ServiceNow.")
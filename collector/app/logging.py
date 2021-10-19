import json
from pprint import pprint


def print_payload(str_payload):
    '''Print payload and content of first message to stdout'''
    MESSAGES = 'messages'
    CONTENT = 'content'
    payload = json.loads(str_payload)
    payload_without_data = {}
    first_message = None
    for payload_key in payload:
        if payload_key != MESSAGES:
            payload_without_data[payload_key] = payload[payload_key]
        else:
            messages_without_data = []
            for message in payload[MESSAGES][:2]:  # First 2 messages only for display
                message_without_data = {}
                for message_key in message:
                    if message_key != CONTENT:
                        message_without_data[message_key] = message[message_key]
                    else:
                        message_without_data[CONTENT] = '<spark-event-json-as-a-string>'
                        if first_message is None:
                            if message['message_type'] == 'heartbeat':
                                first_message = 'No content, this was a heartbeat.'
                            else:
                                first_message = json.loads(message[CONTENT])
                messages_without_data.append(message_without_data)
            messages_without_data.append('...')
            payload_without_data[MESSAGES] = messages_without_data
    print('---------------------- Payload without messages content ----------------------')
    pprint(payload_without_data)
    print('---------------------- Content of first message ----------------------')
    pprint(first_message)

import json
import os
from slack import WebClient
from slack.errors import SlackApiError
from time import sleep

"""Sample pure Lambda function

Parameters
----------
event: dict, required
    API Gateway Lambda Proxy Input Format

    Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

context: object, required
    Lambda Context runtime methods and attributes

    Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

Returns
------
API Gateway Lambda Proxy Output Format: dict

    Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
"""
def lambda_handler(event, context):

    print(os.environ)
    client = WebClient(token=os.environ['BOT_USER_TOKEN'])
    
    """Print payload sent from Pinpoint. 

    Custom Channels doc: https://docs.aws.amazon.com/pinpoint/latest/developerguide/channels-custom.html
    """
    print(event)

    # A valid invocation of this channel by the Pinpoint Service will include Endpoints in the event payload.
    if 'Endpoints' not in event:
        return response_obj(500, f'Payload does not contain endpoints. Event: {event}')

    endpoints = event['Endpoints']

    for endpoint_id in endpoints:

        """The endpoint profile contains the entire endpoint definition.

        Attributes and UserAttributes can be interpolated into your message for personalization.
        """
        endpoint_profile = endpoints[endpoint_id]

        """Channel, private group, or IM channel to send message to. Can be an encoded ID, or a name.

        Slack Channels doc: https://api.slack.com/methods/chat.postMessage#channels
        """
        address = endpoint_profile['Address']

        """Construct your message here.  You have access to the endpoint profile to personalize the message with Attributes.
        
        `message = "Hello {name}!".format(name=endpoint_profile["Attributes"]["FirstName"])`
        """
        message = 'Hello World! - Pinpoint Slack Channel'

        try:
            """Slack Chat PostMessage doc: https://api.slack.com/methods/chat.postMessage

            Note: In order for a channel or user to receive a message, the app must have relevant permissions and join the conversation first.
            Slack Conversation Join doc: https://api.slack.com/methods/conversations.join
            """
            response = client.chat_postMessage(
                channel=address,
                text=message)
            assert response['message']['text'] == message
            print(response_obj(200, response['message']))
        except SlackApiError as e:
            # You will get a SlackApiError if "ok" is False
            assert e.response['ok'] is False
            assert e.response['error']  # str like 'invalid_auth', 'channel_not_found'
            print(response_obj(500, f"{e.response['error']}"))

        """Required to avoid hitting rate limit.

        Slack rate limits doc: https://api.slack.com/docs/rate-limits#tier_t5
        """
        sleep(1)

    return(response_obj(200, "Complete"))


def response_obj(statusCode, message):
    return {
        'statusCode': statusCode,
        'body': json.dumps({
            'message': message,
        }),
    }
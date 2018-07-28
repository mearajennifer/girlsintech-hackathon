# functions that interact with Twilio
# import this into server.py

from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import os

account_sid = os.environ['ACCOUNT_SID']
auth_token = os.environ['AUTH_TOKEN']
client = Client(account_sid, auth_token)


def sms_volunteer_request(message, phone_nums):
    """Connects organizations on our app to the Twilio functionality.

    Org message is passed in (request is created by info that orgs supply
    on webpage, and is put together as a string before this function is called.)
    Phone numbers of interested volunteers are passed in as a list from
    the database.
    """

    # can add media url below body if needed
    # media_url="https://climacons.herokuapp.com/clear.png"

    for num in phone_nums:
        call = client.messages.create(
            to=num,
            from_='+15109441564',
            body=message,
        )

    print(call.sid)


@app.route("/sms", methods=['GET', 'POST'])
def sms_ahoy_reply():
    """Respond to incoming messages with a friendly SMS."""
    # Start our response
    resp = MessagingResponse()

    # Add a message
    resp.message("Ahoy! Thanks so much for your message.")

    return str(resp)





# sample data to call functions
message = 'Hackbright needs 30 volunteers today from 2pm to 7pm. Can you make it?'
numbers = os.environ['numbers_list']

# functions
send_sms_volunteer_request(message, numbers)









































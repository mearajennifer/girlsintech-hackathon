# functions that interact with Twilio
# import this into server.py

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import os

account_sid = os.environ['ACCOUNT_SID']
auth_token = os.environ['AUTH_TOKEN']
client = Client(account_sid, auth_token)

app = Flask(__name__)
app.secret_key = 'abc'

@app.route("/")
def landing():
    return """
    Hello world<br>
    <a href="/sms">Send text</a>
    """


@app.route("/sms")
def sms_volunteer_request():
    """Connects organizations on our app to the Twilio functionality.

    Org message is passed in (request is created by info that orgs supply
    on webpage, and is put together as a string before this function is called.)
    Phone numbers of interested volunteers are passed in as a list from
    the database.
    """

    # org_id = session['organization_id']
    # org = Organization.query.filter(Organization.organization_id == org_id).first()
    # 

    # sample data to call functions
    message = 'Hackbright needs 30 volunteers today from 2pm to 7pm. Can you make it? Reply YES.'
    numbers = ["+12163921002"]

    for num in numbers:
        call = client.messages.create(
            to=num,
            from_='+15109441564',
            body=message,
        )

    print(call.sid)

    flash("Your request for volunteers was sent!")
    return redirect("/")


@app.route("/sms", methods=['GET', 'POST'])
def sms_reply_attending_():
    """Respond to incoming messages that way the volunteer will attend
    with an SMS containing more data."""

    # Start our response
    resp = MessagingResponse()

    # Add a message
    resp.message("Can't wait to see you! Find more info at hackbright.com.")

    return str(resp)


if __name__ == '__main__':
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True

    # make sure templates, etc. are not cached in debug mode
    # app.jinja_env.auto_reload = app.debug

    # connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')




































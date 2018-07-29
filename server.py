""" Volunteer app server. """

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import Volunteer, Organization, Category, OrganizationVolunteer, connect_to_db, db

from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import os

# set up twilio client
account_sid = os.environ['ACCOUNT_SID']
auth_token = os.environ['AUTH_TOKEN']
client = Client(account_sid, auth_token)

# set up flask app
app = Flask(__name__)
app.secret_key = 'abc'

# Make sure Jinja raises errors
app.jinja_env.undefined = StrictUndefined


###################### LANDING AND GENERAL LOGIN ######################
@app.route("/")
def show_landing():
    """Landing page"""
    return render_template('landing.html')


@app.route("/login")
def show_login():
    """Login option for volunteers or organizations"""
    return render_template('login.html')


###################### REGISTER / LOGIN FOR VOLUNTEERS #####################
@app.route('/register/volunteer', methods=['GET'])
def show_volunteer_register_form():
    """Shows registration form to volunteer"""
    return render_template('register-volunteer.html')


@app.route('/register/volunteer', methods=['POST'])
def process_volunteer_register_form():
    """ Process data given by user in form and add to database."""

    name = request.form.get('name')
    email = request.form.get('email')
    phone_number = request.form.get('phone_number')
    password = request.form.get('password')

    volunteer = Volunteer(name=name, email=email, phone_number=phone_number, password=password)
    db.session.add(volunteer)
    db.session.commit()

    flash('Thanks for registering. Please login.')
    return redirect('/login/volunteer')


@app.route('/login/volunteer', methods=['GET'])
def show_volunteer_login():
    """Shows form for volunteer to sign in."""
    return render_template('login-volunteer.html')


@app.route('/login/volunteer', methods=['POST'])
def verify_volunteer_login():
    """Verifies volunteeremail is in database and password matches"""

    # gets email and password from form and verifies user in db
    email = request.form.get('email')
    password = request.form.get('password')
    volunteer = Volunteer.query.filter(Volunteer.email == email).first()

    # if user doesn't exist, redirect
    if not volunteer:
        flash('No user exists with that email address.')
        return redirect('/login/volunteer')

    # if user exists but passwords don't match
    if volunteer.password != password:
        flash('Incorrect password for the email address entered.')
        return redirect('/login/volunteer')

    # add user_id to session
    session['user_id'] = user.user_id
    session['type'] = 'volunteer'

    # redirect to home page
    flash('You are now logged in.')
    return redirect('/home')


###################### REGISTER / LOGIN FOR ORGANIZATIONS #####################
@app.route('/register/organization', methods=['GET'])
def show_registration_form():
    """Shows registration form to user"""

    return render_template('register-org.html')


@app.route('/register/organization', methods=['POST'])
def show_org_registration_form():
    """Shows registration form to organization"""

    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    address = request.form.get('address')
    category = request.form.get('category')
    description = request.form.get('description')
    website = request.form.get('website')
    
    organization = Organization(name=name, email=email, password=password,
                                    address=address, category=category,
                                    description=description, website)

    db.session.add(organization)
    db.session.commit()

    flash('Thanks for registering. Please login.')
    return redirect('/login/organization')


@app.route('/login/organization', methods=['GET'])
def show_organization_login():
    """Shows form for organization to sign in."""
    return render_template('login-org.html')


@app.route('/login/organization', methods=['POST'])
def verify_organization_login():
    """Verifies org email is in database and password matches"""

    # gets email and password from form and verifies user in db
    email = request.form.get('email')
    password = request.form.get('password')
    organization = Organization.query.filter(Organization.email == email).first()

    # if user doesn't exist, redirect
    if not organization:
        flash('No organization exists with that email address.')
        return redirect('/login/organization')

    # if user exists but passwords don't match
    if organization.password != password:
        flash('Incorrect password for the email address entered.')
        return redirect('/login/organization')

    # add user_id to session
    session['user_id'] = organization.organization_id
    session['type'] = 'organization'

    # redirect to home page
    flash('You are now logged in.')
    return redirect('/home')


##################### GENERAL PAGES ######################
@app.route("/logout")
def logout():
    """Logs the current user out"""

    # remove session from browser to log out
    del session['user_id']
    del session['type']
    flash('Logged out.')
    return redirect("/")


########## TWILIO SMS ROUTES ##########
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




































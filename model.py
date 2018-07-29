"""Models and database functions for Connector project."""

from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from jinja2 import StrictUndefined
from os import environ


# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do m st of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Volunteer definition

class Volunteer(db.Model):
    """Volunteer of Connector website."""

    __tablename__ = "volunteers"

    volunteer_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Volunteer name={}, phone={}>".format(self.name, self.phone_number)


    def retrieve_organizations_volunteer_is_in(self):
        """"""

        return Organization.query.join(OrganizationVolunteer).join(Volunteer).filter(
            OrganizationVolunteer.volunteer_id == self.volunteer_id).all()


##############################################################################
# Organization definition

class Organization(db.Model):
    """Organization of Connector website."""

    __tablename__ = "organizations"

    organization_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    address = db.Column(db.String(64), nullable=False)
    category_code = db.Column(db.Integer, db.ForeignKey('categories.category_code'),nullable=False)
    description = db.Column(db.String(256))
    website = db.Column(db.String(64))
    # TODO Implement hours in a non stupid way


    category = db.relationship("Category", backref=db.backref("categories", order_by=category_code))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Organization name={}, category_code={}>".format(self.name, self.category_code)

    def retrieve_volunteers(self):
        """"""
        return Volunteer.query.join(OrganizationVolunteer).join(Organization).filter(
            OrganizationVolunteer.organization_id == self.organization_id).all()


##############################################################################
# Category definition

class Category(db.Model):
    """Categories of Connector website."""

    __tablename__ = "categories"

    category_code = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Organization category_code={}, name={}>".format(self.category_code, self.name)


##############################################################################
# OrganizationVolunteers definition

class OrganizationVolunteer(db.Model):
    """OrganizationVolunteers of Connector website."""

    __tablename__ = "organization_volunteers"

    orgvol_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    volunteer_id = db.Column(db.Integer, db.ForeignKey('volunteers.volunteer_id'), nullable=False)
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.organization_id'), nullable=False)

    organizations = db.relationship("Organization", backref=db.backref("organizations", order_by=organization_id))
    volunteers = db.relationship("Volunteer", backref=db.backref("volunteers", order_by=volunteer_id))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<OrganizationVolunteer volunteer_id={}, organization_id={}>".format(self.volunteer_id,
                                                                                    self.organization_id)

    def remove_organization_volunteer(self):
        db.session.delete(self)


##############################################################################
# Test functions

def create_dummy_volunteers():
    """Create dummy volunteers for testing purposes"""

    kami = Volunteer(name="Kami",
                     email="kami@kami.com",
                     password=environ['kami_pass'],
                     phone_number=environ['kami_num'])
    jennifer = Volunteer(name="Jennifer",
                         email="jen@jennifer.com",
                         password=environ['jen_pass'],
                         phone_number=environ['jen_num'])
    ione = Volunteer(name="Ione",
                         email="ione@ione.com",
                         password=environ['ione_pass'],
                         phone_number=environ['ione_num'])

    db.session.add_all([kami, jennifer, ione])
    db.session.commit()
    return [kami, jennifer, ione]


def create_dummy_category():

    food_aid = Category(name="food aid")
    db.session.add(food_aid)
    return food_aid



def create_dummy_organization():
    """"""
    hackoak = Organization(name="HackOak",
                           email="hackoak@hackoak.com",
                           password=environ['oak_pass'],
                           address="221 Main St, San Francisco, CA",
                           category_code=1,
                           description="Dedicated to helping out our peeps",
                           )

    brightland = Organization(name="BrightLand",
                           email="brightland@brightland.com",
                           password=environ['bright_pass'],
                           address="221 Main St, San Francisco, CA",
                           category_code=1,
                           description="Dedicated to helping out our friends",
                           )

    db.session.add_all([hackoak, brightland])
    db.session.commit()

    return hackoak

def create_dummy_orgvol(volunteers, organization):
    organization_volunteers = []

    for volunteer in volunteers:
        organization_volunteer = OrganizationVolunteer(volunteer_id=volunteer.volunteer_id,
                                                       organization_id=organization.organization_id)
        organization_volunteers.append(organization_volunteer)

    organization_volunteers.append(OrganizationVolunteer(volunteer_id=1, organization_id=2))

    db.session.add_all(organization_volunteers)

    db.session.commit()

    return organization_volunteers


##############################################################################
# Test functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///volunteer'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    app = Flask(__name__)

    # Required to use Flask sessions and the debug toolbar
    app.secret_key = "ABC"

    # Normally, if you use an undefined variable in Jinja2, it fails
    # silently. This is horrible. Fix this so that, instead, it raises an
    # error.
    app.jinja_env.undefined = StrictUndefined

    # Connect database to flask
    connect_to_db(app)

    # Drop old tables before adding dummy info
    db.drop_all()
    db.create_all()
    dummies = create_dummy_volunteers()
    category = create_dummy_category()
    organization = create_dummy_organization()
    volunteerList = create_dummy_orgvol(dummies, organization)
    for volunteer in dummies:
        print(volunteer.retrieve_organizations_volunteer_is_in())

    print(organization.retrieve_volunteers())
    bright = Organization.query.get(2).retrieve_volunteers()
    print(bright)


    print("Connected to DB.")


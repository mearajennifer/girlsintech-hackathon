"""Models and database functions for Connector project."""

from flask_sqlalchemy import SQLAlchemy

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




##############################################################################
# Organization definition

class Organization(db.Model):
    """Organization of Connector website."""

    __tablename__ = "organizations"

    organization_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    address = db.Column(db.String(64), nullable=False)
    category_code = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(256))
    website = db.Column(db.String(64))
    # TODO Implement hours in a non stupid way


    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Organization name={}, category_code={}>".format(self.name, self.category_code)



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

    volunteer_id = db.Column(db.Integer, nullable=False)
    organization_id = db.Column(db.Integer, nullable=False)


    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<OrganizationVolunteer volunteer_id={}, organization_id={}>".format(self.volunteer_id,
                                                                                    self.organization_id)

# class Movie(db.Model):
#     """Movie of ratings website."""
#
#     __tablename__ = "movies"
#
#     movie_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     title = db.Column(db.String(100), nullable=True)
#     released_at = db.Column(db.DateTime, nullable=True)
#     imdb_url = db.Column(db.String, nullable=True)
#
#     def __repr__(self):
#         """Provide helpful representation when printed."""
#
#         return f"""<Movie movie_id={self.movie_id}
#                    title={self.title}
#                    released_at={self.released_at}
#                    imdb_url={self.imdb_url}>"""

#
# class Rating(db.Model):
#     """Rating of ratings website."""
#
#     __tablename__ = "ratings"
#
#     rating_id = db.Column(db.Integer,
#                           autoincrement=True,
#                           primary_key=True)
#     movie_id = db.Column(db.Integer,
#                          db.ForeignKey('movies.movie_id'))
#     user_id = db.Column(db.Integer,
#                         db.ForeignKey('users.user_id'))
#     score = db.Column(db.Integer)
#
#     user = db.relationship("User",
#                            backref=db.backref("ratings", order_by=rating_id))
#
#     movie = db.relationship("Movie",
#                             backref=db.backref("ratings", order_by=rating_id))
#
#     def __repr__(self):
#         """Provide helpful representation when printed."""
#
#         return f"""<Rating rating_id={self.rating_id}
#                    movie_id={self.movie_id}
#                    user_id={self.user_id}
#                    score={self.score}>"""

##############################################################################
# Helper functions


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

    from server import app
    connect_to_db(app)
    print("Connected to DB.")


from app import db


class Users(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), index=True)
    last_name = db.Column(db.String(30), index=True, unique=True)
    password = db.Column(db.String(20), index=True, unique=True)
    profession = db.Column(db.String(50))
    mail = db.Column(db.String(50), index=True, unique=True)
    birth_date = db.Column(db.Date())
    phone = db.Column(db.String(), unique=True)
    height = db.Column(db.Float())
    weight = db.Column(db.Float())
    blood_group = db.Column(db.String(2))
    allergies = db.Column(db.String(100))
    medical_background = db.Column(db.Text())
    medicines = db.Column(db.String(100))
    illness = db.relationship('SickRequest', backref='user', lazy='dynamic')
    address = db.relationship('Address', backref='user', lazy='dynamic')
    authenticated = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Username: {self.first_name}>'

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
            """Return the email address to satisfy Flask-Login's requirements."""
            return self.user_id

    def is_authenticated(self):
            """Return True if the user is authenticated."""
            return self.authenticated

    def is_anonymous(self):
            """False, as anonymous users aren't supported."""
            return False


class SickRequest(db.Model):
    ill_id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text())
    pub_date = db.Column(db.DateTime())
    category = db.Column(db.String(50))
    answer = db.Column(db.Text())
    image_file = db.Column(db.String())
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    doc_id = db.Column(db.Integer, db.ForeignKey('doctor.doc_id'))

    def __repr__(self):
        return f'<Post: {self.content}>'


class Doctor(db.Model):
    doc_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True)
    doc_mail = db.Column(db.String(30))
    doc_pass = db.Column(db.String(30))
    category = db.Column(db.String(100), index=True, unique=True)
    image_profile = db.Column(db.String(50))
    illness = db.relationship('SickRequest', backref='doctor', lazy='joined')
    address = db.relationship('Address', backref='doctor', lazy='dynamic')
    authenticated = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Username: {self.name}>'

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
            """Return the email address to satisfy Flask-Login's requirements."""
            return self.doc_id

    def is_authenticated(self):
            """Return True if the user is authenticated."""
            return self.authenticated

    def is_anonymous(self):
            """False, as anonymous users aren't supported."""
            return False


class Address(db.Model):
    address_id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(100))
    city = db.Column(db.String(100))
    address = db.Column(db.String(100))
    birth_place = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    doc_id = db.Column(db.Integer, db.ForeignKey('doctor.doc_id'))

    def __repr__(self):
        return f'<Username: {self.city}>'


"""
hide and generate hashed password
import generate_password_hash from werkzeug.utils
hashed_passsword = generate_password_hash(password, method='sha256'
To check: if check_password_hash(hashed password, login password)
"""
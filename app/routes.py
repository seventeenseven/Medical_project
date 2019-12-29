from flask import render_template, redirect, url_for, request, flash
from app import app, db
from app.forms import LoginForm, RegisterForm, AnswerForm, IllnessForm
from app.models import *
from flask_login import login_user, login_required, LoginManager, current_user, logout_user
from datetime import datetime
from werkzeug.utils import secure_filename
import os

login_manager = LoginManager()
login_manager.init_app(app=app)
login_manager.login_message = u"You're log in successfully."
login_manager.login_message_category = "info"


@login_manager.unauthorized_handler
def unauthorized():
    # do stuff
    return redirect(url_for('login'))


@login_manager.user_loader
def user_loader(user_id):
    return Users.query.get(user_id)


"""@login_manager.user_loader
def user_loader(doc_id):
    return Doctor.query.get(doc_id)"""


@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        print("first")
        email = form.email.data
        passw = form.password.data
        role = form.role.data
        if role == 'doctor':
            doc = Doctor.query.filter_by(doc_pass=passw).first()

            if doc:
                doc.authenticated = True
                db.session.add(doc)
                db.session.commit()
                login_user(doc, remember=True)
                flash(u'You were successfully logged in', 'success')
                return redirect(url_for('doctor', category=current_user.category, d_id=current_user.doc_id))
            else:
                flash(u"Wrong credentials, are you a doctor ?", "danger")

        elif role == 'patient':
            print("second")
            user = Users.query.filter_by(password=passw).first()

            if user:
                user.authenticated = True
                db.session.add(user)
                db.session.commit()
                login_user(user, remember=True)
                print("third")
                flash(u'You were successfully logged in', 'info')
                return redirect(url_for('home'))
            else:
                flash(u'Wrong credentials, are you registered ?', 'danger')
    return render_template('login1.html', form=form)


@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    form = IllnessForm()

    if form.validate_on_submit():
        category = form.category.data
        content = form.content.data
        f = form.document.data
        if f:
            filename = secure_filename(f.filename)
            f.save(os.path.join(app.static_folder, filename))

            new_sick = SickRequest(category=category, content=content, pub_date=datetime.now(), user=current_user, image_file=filename)
        else:
            new_sick = SickRequest(category=category, content=content, pub_date=datetime.now(), user=current_user)

        db.session.add(new_sick)
        db.session.commit()
        flash(u"Request sent successfully", "success")
        return redirect(url_for('home'))
    return render_template('index.html', form=form, doctors=Doctor.query.all(), userId=current_user.user_id)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    print('before register')
    if form.validate_on_submit():
        print('in register form data')
        firstname = form.first_name.data
        lastname =form.last_name.data
        birthd = form.birth_date.data
        mail = form.email.data
        psw = form.password.data
        job = form.profession.data
        phone = form.phone.data
        address = form.address.data
        city = form.city.data
        country = form.country.data
        height = form.height.data
        weight = form.weight.data
        bloodg = form.blood_group.data
        allergy = form.allergies.data
        drug = form.medicines.data
        medback = form.medical_background.data

        new_user = Users(first_name=firstname, last_name=lastname, birth_date=birthd, password=psw,
                         profession=job, mail=mail, phone=phone, height=height, weight=weight,
                         blood_group=bloodg, allergies=allergy, medicines=drug, medical_background=medback)
        addressed = Address(country=country, city=city, address=address, user=new_user)
        db.session.add(new_user)
        db.session.add(addressed)
        db.session.commit()

        return redirect(url_for('login'))
    else:
        flash(u"Oops something went wrong, try again !", "info")
    return render_template('register.html', form=form)


@app.route('/profil/<int:id>')
def profil(id):
    #id=current_user.user_id
    return render_template('profile_page.html', user=Users.query.filter_by(user_id=id).first(),
                           addressed=Address.query.filter_by(user_id=id).first(),
                           userId=current_user.user_id)


@app.route('/profil/<int:id>/request')
@login_required
def patient_request(id):
   if current_user.user_id:
        return render_template('patient_request.html', user=Users.query.filter_by(user_id=id).first(),
                           p_request=SickRequest.query.filter_by(user_id=id).all(),
                           userId=current_user.user_id)
   else:
       flash("You're not authorized to be there", "danger")


@app.route('/profil/<int:id>/modif', methods=['GET', 'POST'])
@login_required
def modify(id):
    if current_user.user_id:
        modif_form=RegisterForm()

        if modif_form.validate_on_submit():
            print('in register form data')
            firstname = modif_form.first_name.data
            lastname = modif_form.last_name.data
            birthd = modif_form.birth_date.data
            mail = modif_form.email.data
            psw = modif_form.password.data
            job = modif_form.profession.data
            phone = modif_form.phone.data
            address = modif_form.address.data
            city = modif_form.city.data
            country = modif_form.country.data
            height = modif_form.height.data
            weight = modif_form.weight.data
            bloodg = modif_form.blood_group.data
            allergy = modif_form.allergies.data
            drug = modif_form.medicines.data
            medback = modif_form.medical_background.data

            if firstname:
                Users.query.filter_by(user_id=id).first().first_name=firstname
            if lastname:
                Users.query.filter_by(user_id=id).first().last_name=lastname
            if birthd:
                Users.query.filter_by(user_id=id).first().birth_date=birthd
            if mail:
                Users.query.filter_by(user_id=id).first().mail = mail
            if psw:
                Users.query.filter_by(user_id=id).first().password = psw
            if job:
                Users.query.filter_by(user_id=id).first().profession = job
            if phone:
                Users.query.filter_by(user_id=id).first().phone = phone
            if address:
                Address.query.filter_by(user_id=id).first().address =address
            if city:
                Address.query.filter_by(user_id=id).first().city=city
            if country:
                Address.query.filter_by(user_id=id).first().country=country
            if height:
                Users.query.filter_by(user_id=id).first().height=height
            if weight:
                Users.query.filter_by(user_id=id).first().weight=weight
            if bloodg:
                Users.query.filter_by(user_id=id).first().blood_group=bloodg
            if allergy:
                Users.query.filter_by(user_id=id).first().allergies=allergy
            if drug:
                print(drug)
                Users.query.filter_by(user_id=id).first().medicines=drug
            if medback:
                print(medback)
                Users.query.filter_by(user_id=id).first().medical_background=medback
            else:
                flash("Oops something went wrong, try again !", "info")

            db.session.commit()

            return redirect(url_for('profil', id=id))


        return render_template('profile_modify.html', form=modif_form,
                               user=Users.query.filter_by(user_id=id).first(), userId=current_user.user_id)
    else:
        flash("You're not authorized to be there", "danger")


@app.route('/doctor/<string:category>/<int:d_id>', methods=['POST', 'GET'])
def doctor(category, d_id):
    form = AnswerForm()
    sick_requests = SickRequest.query.filter_by(category=category).all()
    counter = SickRequest.query.filter_by(category= category).count()
    return render_template('page_doctor.html', requests=sick_requests, category=category, counter=counter, form=form, d_id=d_id,
                           doctor=Doctor.query.filter_by(doc_id=d_id).first())


@app.route('/doctor/<string:category>/<int:d_id>/<int:id>', methods=['POST', 'GET'])
def answer(id, category, d_id):
    form = AnswerForm()
    answer = form.answer.data
    print(answer)
    requested = SickRequest.query.filter_by(ill_id=id).first()
    requested.doc_id = d_id
    requested.answer = answer
    db.session.commit()
    return redirect(url_for('doctor', category=category, d_id=d_id))


@app.route('/doctor/<string:category>/<int:d_id>/answered', methods=['POST', 'GET'])
def doctor_answer(category, d_id):
    sick_requests = SickRequest.query.filter_by(category=category).all()
    counter = SickRequest.query.filter_by(category= category).count()
    return render_template('doctor_answers.html', requests=sick_requests, category=category, counter=counter, d_id=d_id,
                           doctor=Doctor.query.filter_by(doc_id=d_id).first())


@app.route("/logout", methods=["GET"])
@login_required
def logout():
    """Logout the current user."""
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    return redirect(url_for('login'))
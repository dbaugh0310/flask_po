from flask import render_template, flash, redirect, url_for, request, abort
from werkzeug.utils import secure_filename
from flask_login import current_user, login_user, logout_user, login_required
from po_app import app, db
from po_app.forms import UploadPhoto, LoginForm
from po_app.models import PO, User
import os
import sqlalchemy as sa

@app.route('/')
@app.route('/index')
def index():
    po_list = PO.get_random_post_offices()   
    return render_template('index.html', title='Home', po=po_list)

@login_required
@app.route('/submit', methods=['GET', 'POST'])
def submit():
    form = UploadPhoto()
    if form.validate_on_submit():
        uploaded_file = request.files['file']
        filename = secure_filename(uploaded_file.filename)
        file_ext = os.path.splitext(filename)[1]
        if file_ext != '.jpg':
            abort(400)
        po = db.first_or_404(sa.select(PO).where(PO.zip == form.zip.data))
        file_name = po.po_pic
        uploaded_file.save(os.path.join(app.root_path, 'static', file_name))
        PO.update_po(form.zip.data)
        flash('Picture for {}, NC submitted!'.format(po.city.title()))
        return redirect(url_for('zip', zip = form.zip.data))
    return render_template('submit.html', title='A new visit!', form=form)

@app.route('/<zip>')
def zip(zip):
    po = db.first_or_404(sa.select(PO).where(PO.zip == zip))
    pic = os.path.isfile(os.path.join(app.root_path, 'static', po.po_pic))
    if pic:
        return render_template('po.html', po=po, pic=pic )
    else:
        return render_template('po.html', po=po )

@app.route('/list')
def list():
    po = db.session.scalars(sa.select(PO).order_by(PO.city))
    return render_template('list.html', po=po )

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
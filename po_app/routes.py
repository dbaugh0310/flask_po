from flask import render_template, flash, redirect, url_for
from po_app import app, db
import sqlalchemy as sa
from po_app.forms import POForm
from po_app.models import PO

@app.route('/')
@app.route('/index')
def index():
    po_list = PO.get_random_post_offices()   
    return render_template('index.html', title='Home', po=po_list)

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    form = POForm()
    if form.validate_on_submit():
        flash('Post office {} in {} submitted!'.format(form.zip.data, form.city.data))
        return redirect(url_for('index'))
    return render_template('submit.html', title='A new visit!', form=form)

@app.route('/<zip>')
def zip(zip):
    po = db.first_or_404(sa.select(PO).where(PO.zip == zip))
    pic = po.po_pic
    return render_template('po.html', po=po, pic=pic )

@app.route('/list')
def list():
    po = db.session.scalars(sa.select(PO))
    return render_template('list.html', po=po )
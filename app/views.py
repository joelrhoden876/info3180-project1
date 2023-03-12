"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file contains the routes for your application.
"""

import os 
from app import app, db
from flask import render_template, request, redirect, url_for, flash, send_from_directory
from werkzeug.utils import secure_filename
from app.forms import PropertyForm
from app.models import Property


###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Joel Rhoden")

@app.route('/properties/create', methods=['GET', 'POST']) #3.3
def create_property():
    form = PropertyForm()
    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        rooms = form.rooms.data
        bathrooms = form.bathrooms.data
        price = form.price.data
        type = form.type.data
        location = form.location.data
        photo = request.files['photo']
        filename = secure_filename(photo.filename)
        photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        property = Property(title=title, description=description, rooms=rooms, bathrooms=bathrooms, price=price, location=location, type=type, photo=filename )
        db.session.add(property)
        db.session.commit()
        
        property_listing = Property.query.all()
        flash('Property Successfully Added!')
        return redirect(url_for('properties', properties = property_listing))
        # return render_template('newproperty.html', form = form)
    flash_errors(form)
    """Render the website's contact form."""
    return render_template('newproperty.html', form = form)

@app.route('/properties', methods=['POST', 'GET'])
def properties():
    property_listing = Property.query.all()
    filename = get_uploaded_images()
    return render_template('properties.html', properties = property_listing) 

@app.route('/property/<propertyid>')
def propertyid(propertyid):
    property= Property.query.filter_by(id=propertyid).first()
    return render_template('property.html', property=property)

@app.route("/image/<filename>")
def get_image(filename):
    return send_from_directory(os.path.join(os.getcwd(), app.config['UPLOAD_FOLDER']), filename)

###
# The functions below should be applicable to all Flask apps.
###

def get_uploaded_images():
    root_dir = os.getcwd()
    temp=[]
    for subdir, dirs, files in os.walk(root_dir + '/uploads'): 
        for file in files:
            filename = file 
            temp.append(filename)
    return temp

def get_image(filename):
    return send_from_directory(os.path.join(os.getcwd(), app.config['UPLOAD_FOLDER']), filename)

# Display Flask WTF errors as Flash messages
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404

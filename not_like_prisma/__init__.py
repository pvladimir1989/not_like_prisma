import os

import cv2

from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from flask import send_from_directory

from not_like_prisma.filters import ImageFilters

#
from not_like_prisma.settings import UPLOAD_FOLDER, ALLOWED_EXTENSIONS


# from not_like_prisma.utils import filter_user_image


def create_app():
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    # @app.route('/', methods=['GET', 'POST'])
    # def what_filter():
    # if request.method == 'POST':
    #     if 'file' not in request.files:
    #         flash('No file part')
    #         return redirect(request.url)
    #     file = request.files['file']
    #     # if user does not select file, browser also
    #     # submit an empty part without filename
    #     if file.filename == '':
    #         flash('No selected file')
    #         return redirect(request.url)
    #     if file and allowed_file(file.filename):
    #         filename = secure_filename(file.filename)
    #         file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    #         image = cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    #         filter = ImageFilters(image).gray_filter()
    #         cv2.imwrite(os.path.join(app.config['UPLOAD_FOLDER'], filename), filter)
    #         print(redirect(url_for('uploaded_file', filename=filename)))
    #         return redirect(url_for('uploaded_file', filename=filename))

    # return render_template('index.html')

    @app.route('/', methods=['GET', 'POST'])
    def upload_file():
        if request.method == 'POST':
            # check if the post request has the file part
            if request.form['increase_brightness'] == 'increase_brightness':
                # what_filter()
                if 'file' not in request.files:
                    flash('No file part')
                    return redirect(request.url)
                file = request.files['file']
                if file.filename == '':
                    flash('No selected file')
                    return redirect(request.url)
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    image = cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    filter = ImageFilters(image).increase_brightness()
                    cv2.imwrite(os.path.join(app.config['UPLOAD_FOLDER'], filename), filter)
                    return redirect(url_for('uploaded_file', filename=filename))

            elif request.form['gray'] == 'gray':
                if 'file' not in request.files:
                    flash('No file part')
                    return redirect(request.url)
                file = request.files['file']
                if file.filename == '':
                    flash('No selected file')
                    return redirect(request.url)
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    image = cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    filter = ImageFilters(image).gray_filter()
                    cv2.imwrite(os.path.join(app.config['UPLOAD_FOLDER'], filename), filter)
                    return redirect(url_for('uploaded_file', filename=filename))

        return render_template('index.html')

    @app.route('/uploads/<filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    #
    # @app.route('/', methods=['GET', 'POST'])
    # def contact():
    #     if request.method == 'POST':
    #         if request.form['gray'] == 'gray':
    #             print("ok") # do something
    #             render_template('index.html')
    #         elif request.form['submit_button'] == 'Do Something Else':
    #             pass  # do something else
    #         else:
    #             pass  # unknown
    #     elif request.method == 'GET':
    #         return render_template('index.html')

    from werkzeug.middleware.shared_data import SharedDataMiddleware
    app.add_url_rule('/uploads/<filename>', 'uploaded_file', build_only=True)
    app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {'/uploads': app.config['UPLOAD_FOLDER']})
    return app

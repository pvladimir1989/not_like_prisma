import os

import cv2

from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from flask import send_from_directory

from not_like_prisma.filters import ImageFilters

from not_like_prisma.settings import UPLOAD_FOLDER, ALLOWED_EXTENSIONS


def create_app():
    app = Flask(__name__)

    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    def what_filter(filename):
        image = cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        filter = ImageFilters(image).increase_brightness()
        cv2.imwrite(os.path.join(app.config['UPLOAD_FOLDER'], filename), filter)
        return redirect(url_for('uploaded_file', filename=filename))

    @app.route('/', methods=['GET', 'POST'])
    def upload_file():
        if request.method == 'POST':
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
                if request.form.get('gray') == 'gray':
                    image = cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    filter = ImageFilters(image).gray_filter()
                    cv2.imwrite(os.path.join(app.config['UPLOAD_FOLDER'], filename), filter)
                    return redirect(url_for('uploaded_file', filename=filename))
                elif request.form.get('increase_brightness') == 'increase_brightness':
                    # filename = secure_filename(file.filename)
                    # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    image = cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    filter = ImageFilters(image).increase_brightness()
                    cv2.imwrite(os.path.join(app.config['UPLOAD_FOLDER'], filename), filter)
                    return redirect(url_for('uploaded_file', filename=filename))
                elif request.form.get('threshold_filter') == 'threshold_filter':
                    # filename = secure_filename(file.filename)
                    # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    image = cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    filter = ImageFilters(image).threshold_filter()
                    cv2.imwrite(os.path.join(app.config['UPLOAD_FOLDER'], filename), filter)
                    return redirect(url_for('uploaded_file', filename=filename))
                elif request.form.get('blur_filter') == 'blur_filter':
                    # filename = secure_filename(file.filename)
                    # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    image = cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    filter = ImageFilters(image).blur_filter()
                    cv2.imwrite(os.path.join(app.config['UPLOAD_FOLDER'], filename), filter)
                    return redirect(url_for('uploaded_file', filename=filename))
                elif request.form.get('sobel_filter') == 'sobel_filter':
                    # filename = secure_filename(file.filename)
                    # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    image = cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    filter = ImageFilters(image).sobel_filter()
                    cv2.imwrite(os.path.join(app.config['UPLOAD_FOLDER'], filename), filter)
                    return redirect(url_for('uploaded_file', filename=filename))
                elif request.form.get('sepia') == 'sepia':
                    # filename = secure_filename(file.filename)
                    # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    image = cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    filter = ImageFilters(image).sepia()
                    cv2.imwrite(os.path.join(app.config['UPLOAD_FOLDER'], filename), filter)
                    return redirect(url_for('uploaded_file', filename=filename))
                elif request.form.get('cartoon') == 'cartoon':
                    # filename = secure_filename(file.filename)
                    # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    image = cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    filter = ImageFilters(image).cartoon()
                    cv2.imwrite(os.path.join(app.config['UPLOAD_FOLDER'], filename), filter)
                    return redirect(url_for('uploaded_file', filename=filename))
                elif request.form.get('pencil_scatch') == 'pencil_scatch':
                    # filename = secure_filename(file.filename)
                    # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    image = cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    filter = ImageFilters(image).pencil_scatch()
                    cv2.imwrite(os.path.join(app.config['UPLOAD_FOLDER'], filename), filter)
                    return redirect(url_for('uploaded_file', filename=filename))
                elif request.form.get('pointillism') == 'pointillism':
                    # filename = secure_filename(file.filename)
                    # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    image = cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    filter = ImageFilters(image).pointillism()
                    cv2.imwrite(os.path.join(app.config['UPLOAD_FOLDER'], filename), filter)
                    return redirect(url_for('uploaded_file', filename=filename))

        return render_template('index.html')

    @app.route('/uploads/<filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    from werkzeug.middleware.shared_data import SharedDataMiddleware
    app.add_url_rule('/uploads/<filename>', 'uploaded_file', build_only=True)
    app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {'/uploads': app.config['UPLOAD_FOLDER']})
    return app

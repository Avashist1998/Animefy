import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from test_module import imageConverter

UPLOAD_FOLDER = 'static/Input_img'
OUTPUT_FOLDER = 'static/Output_img'
# in the future  'jpeg' and gif should be added
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return render_template('index.html', message='No selected file')
        if file and not allowed_file(file.filename):
            return render_template('index.html', message='The file does not have proper extension. The file must be .jpg or .png')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            input_file_path = os.path.join(
                app.config['UPLOAD_FOLDER'], filename)
            file.save(input_file_path)
            #redirect(url_for('upload_file', filename=filename))
            # TODO: add option for the user to choose their styles
            # & add a bio section on the html page
            Hosoda_output_file = imageConverter(
                input_file=filename, input_dir=app.config['UPLOAD_FOLDER'], output_dir=app.config['OUTPUT_FOLDER'], load_size=-1, style='Hosoda')
            Paprika_output_file = imageConverter(
                input_file=filename, input_dir=app.config['UPLOAD_FOLDER'], output_dir=app.config['OUTPUT_FOLDER'], load_size=-1, style='Paprika')
            Shinkai_output_file = imageConverter(
                input_file=filename, input_dir=app.config['UPLOAD_FOLDER'], output_dir=app.config['OUTPUT_FOLDER'], load_size=-1, style='Shinkai')
            Hayao_output_file = imageConverter(
                input_file=filename, input_dir=app.config['UPLOAD_FOLDER'], output_dir=app.config['OUTPUT_FOLDER'], load_size=-1, style='Hayao')
            input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            data = {'Hosoda_output_file': Hosoda_output_file, 'Paprika_output_file': Paprika_output_file,
                    'Shinkai_output_file': Shinkai_output_file, 'Hayao_output_file': Hayao_output_file}
            return render_template("final.html", data=data)
    return render_template("index.html")


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')

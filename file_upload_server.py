import os
import glob
import json
import zipfile
from tempfile import TemporaryDirectory

from flask import Flask, request, render_template, make_response, send_file

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'
directories = glob.glob(os.path.join(app.config['UPLOAD_FOLDER'], '*'))

if directories:
    app.config['COUNTER'] = max(int(os.path.basename(d)) for d in directories)
else:
    app.config['COUNTER'] = 0


@app.route('/', methods=['POST'])
def upload_file():
    submission_id = request.cookies.get('submission_id')
    if submission_id:
        # Delete old file if new is uploaded
        path = os.path.join(app.config['UPLOAD_FOLDER'], submission_id)
        file = request.files.get('file')
        if file:
            files = glob.glob(f'{path}/*')
            for f in files:
                os.remove(f)
    else:
        # New submission
        app.config['COUNTER'] += 1
        path = os.path.join(
            app.config['UPLOAD_FOLDER'], str(app.config['COUNTER']))
        os.makedirs(path)

    file = request.files.get('file')
    artwork_name = request.form.get('artwork_name')
    author = request.form.get('author')
    description = request.form.get('description')
    platform = request.form.get('platform')

    if file or not submission_id:
        file.save(os.path.join(path, file.filename))

    info = {
        "title": artwork_name,
        "author": author,
        "description": description,
        "platform": platform
    }

    with open(os.path.join(path, "info.json"), "w") as outfile:
        json.dump(info, outfile, indent=4)

    resp = make_response(render_template(
        'upload.html', form_initial=info, file_uploaded=True))
    resp.set_cookie('submission_id', str(app.config['COUNTER']))
    return resp


@app.route('/', methods=['GET'])
def get_form():
    submission_id = request.cookies.get('submission_id')
    form_initial = {}
    if submission_id:
        path = os.path.join(app.config['UPLOAD_FOLDER'], submission_id)
        with open(os.path.join(path, "info.json"), "r") as json_file:
            info = json.load(json_file)
            form_initial = info
    return render_template('upload.html', form_initial=form_initial)


@app.route('/download', methods=['GET'])
def download_files():
    # Create a temporary directory using tempfile
    with TemporaryDirectory() as tempdir:
        zipfile_path = os.path.join(tempdir, 'uploads.zip')
        # Create a new ZipFile object
        zip_file = zipfile.ZipFile(zipfile_path, 'w', zipfile.ZIP_DEFLATED)

        # Iterate over each file in the directory
        # os.walk is recursive, so subfolders can be ignored
        for folder_name, subfolders, file_names in os.walk(app.config['UPLOAD_FOLDER']):
            for file_name in file_names:
                # Create a complete filepath
                file_path = os.path.join(folder_name, file_name)

                # Add file to the zip
                zip_file.write(file_path)

        # Close the Zip File
        zip_file.close()

        response = send_file(zipfile_path, as_attachment=True)
        os.remove(zipfile_path)
        return response


if __name__ == '__main__':
    app.run(debug=False)

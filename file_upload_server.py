from flask import Flask, request, render_template, make_response
import os
import glob
import json

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'
directories = glob.glob(os.path.join(app.config['UPLOAD_FOLDER'], '*'))

if directories:
    app.config['COUNTER'] = max(int(os.path.basename(d)) for d in directories)
else:
    app.config['COUNTER'] = 0


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
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
            path = os.path.join(app.config['UPLOAD_FOLDER'], str(app.config['COUNTER']))
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

        resp = make_response(render_template('result.html'))
        resp.set_cookie('submission_id', str(app.config['COUNTER']))
        return resp
    return render_template('upload.html')


if __name__ == '__main__':
    app.run(debug=False)

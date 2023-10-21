from flask import Flask, request, render_template
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'
app.config['COUNTER'] = 0 # initial counter
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        app.config['COUNTER'] += 1
        path = os.path.join(app.config['UPLOAD_FOLDER'], str(app.config['COUNTER']))
        if not os.path.exists(path):
            os.makedirs(path)

        file = request.files['file']
        name = request.form.get('name')
        author = request.form.get('author')
        description = request.form.get('description')

        file.save(os.path.join(path, file.filename))

        with open(os.path.join(path, "info.txt"), "w") as info:
            info.write(f"Name: {name}\nAuthor: {author}\nDescription: {description}")

        return 'File upload successfully!'
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=False)

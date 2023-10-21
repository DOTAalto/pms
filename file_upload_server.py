from flask import Flask, request, render_template
import os
import glob

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'
directories = glob.glob(os.path.join(app.config['UPLOAD_FOLDER'], '*'))
app.config['COUNTER'] = max(int(os.path.basename(d)) for d in directories)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        app.config['COUNTER'] += 1
        path = os.path.join(app.config['UPLOAD_FOLDER'], str(app.config['COUNTER']))
        if not os.path.exists(path):
            os.makedirs(path)

        file = request.files['file']
        artwork_name = request.form.get('artwork_name')
        author = request.form.get('author')
        description = request.form.get('description')

        file.save(os.path.join(path, file.filename))

        with open(os.path.join(path, "info.txt"), "w") as info:
            info.write(f"Artwork Name: {artwork_name}\nAuthor: {author}\nDescription: {description}")

        return render_template('result.html')
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=False)

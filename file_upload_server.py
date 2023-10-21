from flask import Flask, request, render_template
import os
import uuid

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        unique_id = uuid.uuid4().hex
        path = os.path.join(app.config['UPLOAD_FOLDER'], unique_id)
        if not os.path.exists(path):
            os.makedirs(path)
        
        file = request.files['file']
        author = request.form.get('author')
        description = request.form.get('description')
        
        file.save(os.path.join(path, file.filename))
        
        with open(os.path.join(path, "info.txt"), "w") as info:
            info.write(f"Author: {author}\nDescription: {description}")
            
        return 'File upload successfully!'
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=False)

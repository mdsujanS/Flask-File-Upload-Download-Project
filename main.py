from flask import Flask, request, render_template, url_for, flash, redirect, send_file 
from io import BytesIO 
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///File.db'
app.config['SQLALCHEMY_TRACK_MODIFICTIONS'] = False

db = SQLAlchemy(app)

# Models to upload file
class FileUpload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(50), nullable=False)
    file = db.Column(db.LargeBinary, nullable=False)
    
    def __repr__(self):
        return f'{self.filename}'

# Create database  
with app.app_context():
    db.create_all()
    
    

# Show all image in Frontend 
@app.route('/')
def show_all_image():
    all_image = FileUpload.query.all()
    return render_template('all_images.html', images=all_image)
    

    
# Upload File  
@app.route('/upload', methods=['POST'])
def Upload_file():
    if request.method =='POST':
        upload_file = request.files['file']
        
        if upload_file and Allowed_file(upload_file.filename):
            
            upload = FileUpload(filename = upload_file.filename, file = upload_file.read())
            db.session.add(upload)
            db.session.commit()
            
            return redirect(url_for('show_all_image'))
        
    return render_template('upload.html')

# Allowed File Extension                      
def Allowed_file(filename):
    ALLOWED_EXTENSION = [ 'png', 'jpg', 'jpeg']
    return "." in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSION

#Download File by id 
@app.route('/download/<int:id>')
def Download_file(id):
    file_data = FileUpload.query.get(id)
    return send_file(BytesIO(file_data.file), download_name = file_data.filename, as_attachment=True)


    
if __name__=='__main__':
    app.run(debug=True)
    
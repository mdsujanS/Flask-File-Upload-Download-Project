from flask import Flask, request, render_template, url_for, flash, redirect, send_file 
from io import BytesIO 
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///File.db'
app.config['SQLALCHEMY_TRACK_MODIFICTIONS'] = False

db = SQLAlchemy(app)

# Models 
class FileUpload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(50), nullable=False)
    file = db.Column(db.LargeBinary, nullable=False)
    
    def __repr__(self):
        return f'{self.filename}'

# Create database  
with app.app_context():
    db.create_all()
    
# Upload File    
@app.route('/', methods=['POST', 'GET'])
def Upload_file():
    if request.method =='POST':
        upload_file = request.files['file']
        
        if upload_file and Allowed_file(upload_file.filename):
            
            upload = FileUpload(filename = upload_file.filename, file = upload_file.read())
            db.session.add(upload)
            db.session.commit()
            
            flash('File Upload Successfully')
            return redirect(url_for('Upload_file'))
        
    return render_template('home.html')

# Allowed File Extension                      
def Allowed_file(filename):
    ALLOWED_EXTENSION = ['pdf', 'png', 'jpg', 'jpeg', 'text']
    return "." in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSION

#Download File
@app.route('/download/<int:id>')
def Download_file(id):
    file_data = FileUpload.query.get(id)
    return send_file(BytesIO(file_data.file), download_name = file_data.filename, as_attachment=True)

    
if __name__=='__main__':
    app.run(debug=True)
    
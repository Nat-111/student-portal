import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

app = Flask(__name__)

# DB Config
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'students.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Upload Config
UPLOAD_FOLDER = os.path.join(basedir, 'static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_path = db.Column(db.String(255))
    fname = db.Column(db.String(100), nullable=False)
    lname = db.Column(db.String(100), nullable=False)
    mname = db.Column(db.String(100))
    dob = db.Column(db.String(20))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    state_of_origin = db.Column(db.String(100))
    local_depaerment = db.Column(db.String(100))
    next_of_kin = db.Column(db.String(150))
    sex = db.Column(db.String(20))
    address = db.Column(db.Text)
    score = db.Column(db.String(10))
    admission_status = db.Column(db.String(50), default='undecided')

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        mname = request.form.get('mname')
        dob = request.form.get('DOB')
        phone = request.form.get('phone')
        email = request.form.get('email')
        state_of_origin = request.form.get('state_of_origin')
        local_depaerment = request.form.get('local_depaerment')
        next_of_kin = request.form.get('next_of_kin')
        sex = request.form.get('sex')
        address = request.form.get('address')
        score = request.form.get('Score')

        # handle file
        image_path = None
        if 'image' in request.files:
            file = request.files['image']
            if file.filename != '':
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                image_path = 'uploads/' + filename
        
        student = Student(
            image_path=image_path,
            fname=fname,
            lname=lname,
            mname=mname,
            dob=dob,
            phone=phone,
            email=email,
            state_of_origin=state_of_origin,
            local_depaerment=local_depaerment,
            next_of_kin=next_of_kin,
            sex=sex,
            address=address,
            score=score
        )
        db.session.add(student)
        db.session.commit()
        return redirect(url_for('students'))

    return render_template('form.html')

@app.route('/students')
def students():
    all_students = Student.query.all()
    return render_template('students.html', students=all_students)

@app.route('/students/<int:id>')
def student_details(id):
    student = Student.query.get_or_404(id)
    return render_template('student_details.html', student=student)

@app.route('/api/students/<int:id>/status', methods=['POST'])
def update_status(id):
    student = Student.query.get_or_404(id)
    data = request.get_json()
    new_status = data.get('status')
    if new_status:
        student.admission_status = new_status
        db.session.commit()
        return jsonify({'success': True, 'status': new_status})
    return jsonify({'success': False, 'message': 'No status provided'}), 400

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for, session
import os
import csv


from werkzeug.utils import secure_filename
app = Flask(__name__)
app.secret_key = 'Ganesh@2005'

# Set up upload folder globally
UPLOAD_FOLDER = os.path.join('static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/placements', methods=['GET', 'POST'])
def placements():
    UPLOAD_FOLDER = os.path.join('static', 'uploads')
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    return render_template('placements.html')
@app.route('/admission', methods=['GET', 'POST'])
def admission():
    if request.method == 'POST':
        name = request.form.get('name')
        msslc = request.form.get('msslc')
        mpuc = request.form.get('mpuc')
        branch = request.form.get('branch')
        mpucp =  request.form.get('mpucp')
        date = request.form.get('date')
        rno = request.form.get('Rno')
        document_type = request.form.get('document_type')
        pno = request.form.get('pno')
        address = request.form.get('address')
        # Validate msslc and mpuc
        try:
            if int(msslc) > 625:
                return render_template('admission.html', message='Marks in SSLC must be less than 626.'), 400
            elif int(mpuc) >= 600:
                return render_template('admission.html', message='Marks in puc must be less than 626.'), 400
        except (ValueError, TypeError):
            return render_template('admission.html', message='Marks in SSLC and PUC must be valid numbers.'), 400

        # Handle file uploads
        mpucp_file = request.files.get('mpucp')
        document_img_file = request.files.get('document_img')
        mpucp_filename = ''
        document_img_filename = ''
        if mpucp_file and mpucp_file.filename:
            mpucp_filename = secure_filename(mpucp_file.filename)
            mpucp_file.save(os.path.join(app.config['UPLOAD_FOLDER'], mpucp_filename))
        if document_img_file and document_img_file.filename:
            document_img_filename = secure_filename(document_img_file.filename)
            document_img_file.save(os.path.join(app.config['UPLOAD_FOLDER'], document_img_filename))

        # Validate Rno: must be 6 digits
        if not (rno and rno.isdigit() and len(rno) == 6):
            return render_template('admission.html', message='Registration No. (Rno) must be exactly 6 digits.'), 400

        # Check for duplicate Rno in the branch file
        branch_map = {'ME': 'admissions_me.csv', 'CS': 'admissions_cs.csv', 'CV': 'admissions_cv.csv'}
        csv_filename = branch_map.get(branch, 'admissions_other.csv')
        file_exists = os.path.isfile(csv_filename)
        if file_exists:
            with open(csv_filename, 'r', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if row.get('Registration No') == rno:
                        return render_template('exist.html',message=f' Registration number already exist '), 400

        # Determine the next serial number for this branch
        serial_number = 1
        if file_exists:
            with open(csv_filename, 'r', newline='') as csvfile:
                reader = csv.reader(csvfile)
                rows = list(reader)
                if len(rows) > 1:
                    serial_number = len(rows)

        # Write the registration row
        with open(csv_filename, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            if not file_exists:
                writer.writerow(['Serial No', 'Name', 'Date of Birth', 'ph no', 'address', 'Registration No', 'Marks SSLC', 'Marks PUC', 'Branch', 'PUC Marks Image', 'Document Type', 'Document Image'])
            writer.writerow([serial_number, name, date, pno, address, rno, msslc, mpuc, branch, mpucp_filename, document_type, document_img_filename])
        return render_template('rsuccess.html', message=f' Your registration number is {serial_number}.')
    return render_template('admission.html')
@app.route('/gallery')
def gallery():
     
    return render_template('gallery.html')
@app.route('/ERP_login', methods=['GET', 'POST'])
def ERP_login():
    message = ''
    if request.method == 'POST':
        login_type = request.form.get('login_type')
        username = request.form.get('username')
        password = request.form.get('password')
        # For demonstration, use a simple user store. Replace with DB in production.
        users = {
            'student': {'student1': 'pass123'},
            'teacher': {'teacher1': 'teach123'},
            'admin': {'admin': 'admin123'}
        }
        user_dict = users.get(login_type.lower(), {})
        if username in user_dict and user_dict[username] == password:
            message = f'Login successful as {login_type}!'
        else:
            message = 'Invalid username or password.'
        return render_template('ERP_login.html', message=message)
    return render_template('ERP_login.html', message=message)

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method=='POST':
        code=request.form.get('code')
        if code != 'dsce@1979':
            message = 'Invalid code. Please enter the correct code to create an account.'
            return render_template('create_account.html', message=message)
        name=request.form.get('name')
        username=request.form.get('username')
        password=request.form.get('password')
        DOB=request.form.get('DOB')
        role=request.form.get('role')
        if role=="student":
            branch=request.form.get('branch')
            Type_of_Admission=request.form.get('Type_of_Admission')
            csv_filename = 'students.csv'
            file_exists = os.path.isfile(csv_filename)
            if file_exists:
                with open(csv_filename, 'r', newline='') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        if row.get('username') == username:
                            return render_template('exist.html', message=f'User name already exist'), 400

            # Determine the next serial number for this branch
            serial_number = 1
            if file_exists:
                with open(csv_filename, 'r', newline='') as csvfile:
                    reader = csv.reader(csvfile)
                    rows = list(reader)
                    if len(rows) > 1:
                        serial_number = len(rows)

            # Write the registration row
            with open(csv_filename, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                if not file_exists:
                    writer.writerow(['Serial No', 'Name', 'username','password','Date of Birth', 'Type_of_Admission' ])
                writer.writerow([serial_number, name, username,password, DOB, branch, Type_of_Admission])
            return render_template('rsuccess.html', message=f' Your account created successfully.')
    return render_template('create_account.html')


if __name__ == '__main__':
    app.run(debug=True)

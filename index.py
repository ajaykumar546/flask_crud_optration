from flask import Flask, render_template,request,redirect
from model import db,StudentModel

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
db.init_app(app)

@app.before_request
def create_table():
    db.create_all()

@app.route('/create' , methods = ['GET','POST'])
def create():
    if request.method == "GET":
        return render_template('create.html')

    #Try to insert data call method
    if request.method == "POST":
        hobby = request.form.getlist('hobbies')
        hobbies = ",".join(map(str, hobby))
        genders = request.form.getlist('genders')
        gender =",".join(map(str, genders))
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        gender = request.form['gender']
        hobbies = hobbies
        country = request.form['country']

        students = StudentModel(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            gender=gender,
            hobbies=hobbies,
            country=country
        )
        db.session.add(students)
        db.session.commit()
        return redirect('/')

#display student list
@app.route('/' , methods = ['GET'])
def RetrieveList():
    students = StudentModel.query.all()
    return render_template('index.html', students=students)

#Edit function
@app.route('/<int:id>/edit' , methods = ['GET','POST'])
def update(id):
    student = StudentModel.query.filter_by(id=id).first()
    if request.method == "POST":
        if student:
            db.session.delete(student)
            db.session.commit()
            hobby = request.form.getlist('hobbies')
            hobbies = ",".join(map(str, hobby))
            genders = request.form.getlist('genders')
            gender =",".join(map(str, genders))
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            email = request.form['email']
            password = request.form['password']
            gender = request.form['gender']
            hobbies = hobbies
            country = request.form['country']

            student = StudentModel(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
                gender=gender,
                hobbies=hobbies,
                country=country
            )
            db.session.add(student)
            db.session.commit()
            return redirect('/')
        return f"Student with id {id} Dose not exist"

    return render_template('update.html', student=student)


#delet function
@app.route('/<int:id>/delete' , methods = ['GET', 'POST'])
def Delete(id):
    students = StudentModel.query.filter_by(id=id).first()
    if request.method == 'POST':
        if students:
           db.session.delete(students)
           db.session.commit()
           return redirect('/')
        abort(404)
    #return redirect('/')
    return render_template('delete.html')


app.run(host='localhost',port=5000)

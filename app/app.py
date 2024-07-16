from flask import Flask, render_template, request, redirect, session
from models import db, User, Donation, Message

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///conecta_hemosc.db'
db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    if 'user_id' in session:
        donations = Donation.query.filter_by(user_id=session['user_id']).all()
        return render_template('index.html', donations=donations)
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and user.check_password(request.form['password']):
            session['user_id'] = user.id
            return redirect('/')
        return 'Invalid credentials'
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        new_user = User(
            username=request.form['username'],
            password=request.form['password'],
            email=request.form['email'],
            role=request.form['role']
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect('/login')
    return render_template('register.html')

@app.route('/schedule_donation', methods=['GET', 'POST'])
def schedule_donation():
    if request.method == 'POST':
        new_donation = Donation(
            user_id=session['user_id'],
            date=request.form['date'],
            blood_type=request.form['blood_type'],
            quantity=request.form['quantity']
        )
        db.session.add(new_donation)
        db.session.commit()
        return redirect('/')
    return render_template('schedule_donation.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'GET':
        query = request.args.get('query')
        users = User.query.filter(User.username.contains(query)).all()
        return render_template('search.html', users=users)
    return render_template('search.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        new_message = Message(
            user_id=session['user_id'],
            subject=request.form['subject'],
            message=request.form['message']
        )
        db.session.add(new_message)
        db.session.commit()
        return 'Mensagem enviada com sucesso'
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)

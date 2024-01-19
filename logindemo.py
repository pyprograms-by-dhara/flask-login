from flask import Flask,render_template,request,redirect,url_for
from flask_login import LoginManager,UserMixin,login_user,current_user,login_required,logout_user
import pymysql

app=Flask(__name__)
app.secret_key="adbcdefg"
login_manage =LoginManager()
login_manage.init_app(app)

con=pymysql.connect(host="localhost",
                    user="root",
                    password="",
                    db="logindemo1")

#user loader function
@login_manage.user_loader
def load_user(user_id):
    return User.get(user_id)

class User(UserMixin):
    def __init__(self,user_id,name,email):
        self.id=user_id
        self.name=name
        self.email=email
    @staticmethod
    def get(user_id):
        cur=con.cursor()
        cur.execute("select name,email from users where id=%s",(user_id,))
        result=cur.fetchone()
        cur.close()
        if result:
            return User(user_id,result[0],result[1])

@app.route("/")
def index():
    return render_template("login.html")

@app.route("/login",methods=['GET','POST'])
def login():
    if request.method=="POST":
        email=request.form.get('email')
        password=request.form.get('password')

        cur=con.cursor()
        cur.execute("select id,name,email,password from users where email=%s",(email,))
        user_data=cur.fetchone()
        if user_data:
            user= User (user_data[0],user_data[1],user_data[2])
        login_user(user)
        return redirect(url_for('dashboard'))

        
    return render_template("login.html")

@app.route("/register",methods=['GET','POST'])
def register():
    if request.method=="POST":
        name=request.form['name']
        email=request.form['email']
        password=request.form['password']

        cur=con.cursor()
        cur.execute("insert into users(name,email,password)values(%s,%s,%s)",(name,email,password))
        con.commit()
        cur.close()
        return redirect(url_for('login'))

    return render_template("register.html")

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return render_template("login.html")

if __name__=="__main__":
    app.run(debug=True)
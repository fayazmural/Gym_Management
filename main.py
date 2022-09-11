from logging import warning
from flask import Flask, json,redirect,render_template,flash,request
from flask.globals import request, session
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_required,logout_user,login_user,login_manager,LoginManager,current_user
from flask_mail import Mail
import json

# mydatabase connection
local_server=True
app=Flask(__name__)
app.secret_key="fayaz"


with open('config.json','r') as c:
    params=json.load(c)["params"]


app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT='465',
    MAIL_USE_SSL=True,
    MAIL_USERNAME=params['gmail-user'],
    MAIL_PASSWORD=params['gmail-password']
)
mail = Mail(app)




# this is for getting the unique user access
login_manager=LoginManager(app)
login_manager.login_view='login'

# app.config['SQLALCHEMY_DATABASE_URI']='mysql://username:password@localhost/databsename'
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:@localhost/dbmsgym'
db=SQLAlchemy(app)



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id)) or Trainer.query.get(int(user_id))


class Test(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50))


class User(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=True)
    aadharid=db.Column(db.String(20),unique=True)
    email=db.Column(db.String(50))
    dob=db.Column(db.String(1000))


class Trainer(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=True)
    tcode=db.Column(db.String(20))
    email=db.Column(db.String(50))
    password=db.Column(db.String(1000))




class Trainerdata(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    tcode=db.Column(db.String(20),unique=True)
    tname=db.Column(db.String(100))
    normal=db.Column(db.Integer)
    premium=db.Column(db.Integer)
    diamond=db.Column(db.Integer)
    exclusive=db.Column(db.Integer)

class Trig(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    tcode=db.Column(db.String(20))
    normal=db.Column(db.Integer)
    premium=db.Column(db.Integer)
    diamond=db.Column(db.Integer)
    exclusive=db.Column(db.Integer)
    querys=db.Column(db.String(50))
    date=db.Column(db.String(50))

class Trainee(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    aadharid=db.Column(db.String(20),unique=True)
    trainingtype=db.Column(db.String(100))
    tcode=db.Column(db.String(20))
    weight=db.Column(db.Integer)
    tname=db.Column(db.String(100))
    tphone=db.Column(db.String(100))
    taddress=db.Column(db.String(100))


@app.route("/")
def home():
   
    return render_template("index.html")

@app.route("/trigers")
def trigers():
    query=Trig.query.all() 
    return render_template("trigers.html",query=query)

@app.route("/aboutus")
def about():
    return render_template("aboutus.html")


@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method=="POST":
        aadharid=request.form.get('aadhar')
        email=request.form.get('email')
        dob=request.form.get('dob')
        # print(srfid,email,dob)
        if len(aadharid)==12:
            encpassword=generate_password_hash(dob)
            user=User.query.filter_by(aadharid=aadharid).first()
            emailUser=User.query.filter_by(email=email).first()
            if user or emailUser:
                flash("Email or aadhar is already taken","warning")
                return render_template("usersignup.html")
            new_user=db.engine.execute(f"INSERT INTO `user` (`aadharid`,`email`,`dob`) VALUES ('{aadharid}','{email}','{encpassword}') ")
                
            flash("SignUp Success Please Login","success")
            return render_template("userlogin.html")
        else:
            flash("Enter Valid id","warning")

    return render_template("usersignup.html")


@app.route('/login',methods=['POST','GET'])
def login():
    if request.method=="POST":
        aadharid=request.form.get('aadhar')
        dob=request.form.get('dob')
        user=User.query.filter_by(aadharid=aadharid).first()
        if user and check_password_hash(user.dob,dob):
            login_user(user)
            flash("Login Success","info")
            return render_template("index.html")
        else:
            flash("Invalid Credentials","danger")
            return render_template("userlogin.html")


    return render_template("userlogin.html")

@app.route('/trainerlogin',methods=['POST','GET'])
def trainerlogin():
    if request.method=="POST":
        email=request.form.get('email')
        password=request.form.get('password')
        user=Trainer.query.filter_by(email=email).first()
        if user and check_password_hash(user.password,password):
            login_user(user)
            flash("Login Success","info")
            return render_template("index.html")
        else:
            flash("Invalid Credentials","danger")
            return render_template("trainerlogin.html")


    return render_template("trainerlogin.html")

@app.route('/admin',methods=['POST','GET'])
def admin():
 
    if request.method=="POST":
        username=request.form.get('username')
        password=request.form.get('password')
        if(username==params['user'] and password==params['password']):
            session['user']=username
            flash("login success","info")
            return render_template("addTrainer.html")
        else:
            flash("Invalid Credentials","danger")

    return render_template("admin.html")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logout SuccessFul","warning")
    return redirect(url_for('login'))



@app.route('/addTrainer',methods=['POST','GET'])
def addTrainer():
   
    if('user' in session and session['user']==params['user']):
      
        if request.method=="POST":
            tcode=request.form.get('tcode')
            email=request.form.get('email')
            password=request.form.get('password')        
            encpassword=generate_password_hash(password)  
            tcode=tcode.upper()      
            emailUser=Trainer.query.filter_by(email=email).first()
            if  emailUser:
                flash("Email or aadhar is already taken","warning")
         
            db.engine.execute(f"INSERT INTO `trainer` (`tcode`,`email`,`password`) VALUES ('{tcode}','{email}','{encpassword}') ")
            #try:
            mail.send_message('HI-FI GYM',sender=params['gmail-user'],recipients=[email],body=f"Welcome thanks for choosing us\nYour Login Credentials Are:\n Email Address: {email}\nPassword: {password}\nTrainer Code {tcode}\n\n Do not share your password\n\n\nThank You..." )
            #except :
                #flash(" Server Bussy.Please try Later","warning")



            #flash("Welcome thanks for choosing us\nYour Login Credentials Are:\n Email Address: {email}\nPassword: {password}\n\nTrainer Code {tcode}\n\n Do not share your password\n\n\nThank You..." )
            flash("Data Sent and Inserted Successfully",)
            return render_template("addTrainer.html")
    else:
        flash("Login and try Again","warning")
        return render_template("addTrainer.html")
    


# testing wheather db is connected or not  
@app.route("/test")
def test():
    try:
        a=Test.query.all()
        print(a)
        return f'MY DATABASE IS CONNECTED'
    except Exception as e:
        print(e)
        return f'MY DATABASE IS NOT CONNECTED {e}'

@app.route("/logoutadmin")
def logoutadmin():
    session.pop('user')
    flash("You are logout admin", "primary")

    return redirect('/admin')


@app.route("/addtrainerinfo",methods=['POST','GET'])
def addtrainerinfo():
    email=current_user.email
    posts=Trainer.query.filter_by(email=email).first()
    code=posts.tcode
    print(code)
    postsdata=Trainerdata.query.filter_by(tcode=code).first()

    if request.method=="POST":
        tcode=request.form.get('tcode')
        tname=request.form.get('tname')
        n=request.form.get('normal')
        h=request.form.get('premium')
        i=request.form.get('diamond')
        v=request.form.get('exclusive')
        tcode=tcode.upper()
        tuser=Trainer.query.filter_by(tcode=tcode).first()
        tduser=Trainerdata.query.filter_by(tcode=tcode).first()
        if tduser:
            flash("Data is already Present you can update it..","primary")
            return render_template("trainerdata.html")
        if tuser:            
            db.engine.execute(f"INSERT INTO `trainerdata` (`tcode`,`tname`,`normal`,`premium`,`diamond`,`exclusive`) VALUES ('{tcode}','{tname}','{n}','{h}','{i}','{v}')")
            flash("Data Is Added","primary")
        else:
            flash("Trainer not Exist","warning")




    return render_template("trainerdata.html",postsdata=postsdata)


@app.route("/tedit/<string:id>",methods=['POST','GET'])
@login_required
def tedit(id):
    posts=Trainerdata.query.filter_by(id=id).first()
  
    if request.method=="POST":
        tcode=request.form.get('tcode')
        tname=request.form.get('tname')
        n=request.form.get('normal')
        h=request.form.get('premium')
        i=request.form.get('diamond')
        v=request.form.get('exclusive')
        hcode=tcode.upper()
        db.engine.execute(f"UPDATE `trainerdata` SET `tcode` ='{tcode}',`tname`='{tname}',`normal`='{n}',`premium`='{h}',`diamond`='{i}',`exclusive`='{v}' WHERE `trainerdata`.`id`={id}")
        flash("Slot Updated","info")
        return redirect("/addtrainerinfo")

    # posts=Trainerdata.query.filter_by(id=id).first()
    return render_template("tedit.html",posts=posts)


@app.route("/hdelete/<string:id>",methods=['POST','GET'])
@login_required
def hdelete(id):
    db.engine.execute(f"DELETE FROM `trainerdata` WHERE `trainerdata`.`id`={id}")
    flash("Date Deleted","danger")
    return redirect("/addtrainerinfo")


@app.route("/tdetails",methods=['GET'])
@login_required
def tdetails():
    code=current_user.aadharid
    print(code)
    data=Trainee.query.filter_by(aadharid=code).first()
   
    
    return render_template("detials.html",data=data)


@app.route("/slotbooking",methods=['POST','GET'])
@login_required
def slotbooking():
    query=db.engine.execute(f"SELECT * FROM `trainerdata` ")
    if request.method=="POST":
        aadharid=request.form.get('aadharid')
        trainingtype=request.form.get('trainingtype')
        tcode=request.form.get('tcode')
        weight=request.form.get('weight')
        tname=request.form.get('tname')
        tphone=request.form.get('tphone')
        taddress=request.form.get('taddress')  
        check2=Trainerdata.query.filter_by(tcode=tcode).first()
        if not check2:
            seat=0
            flash("Trainer not exist","warning")

        code=tcode
        dbb=db.engine.execute(f"SELECT * FROM `trainerdata` WHERE `trainerdata`.`tcode`='{code}' ")        
        trainingtype=trainingtype
        if trainingtype=="Normal Type":       
            for d in dbb:
                seat=d.normal
                print(seat)
                ar=Trainerdata.query.filter_by(tcode=code).first()
                ar.normal=seat-1
                db.session.commit()
                
            
        elif trainingtype=="Premium Type":      
            for d in dbb:
                seat=d.premium
                print(seat)
                ar=Trainerdata.query.filter_by(tcode=code).first()
                ar.premium=seat-1
                db.session.commit()

        elif trainingtype=="Diamond Type":     
            for d in dbb:
                seat=d.diamond
                print(seat)
                ar=Trainerdata.query.filter_by(tcode=code).first()
                ar.diamond=seat-1
                db.session.commit()

        elif trainingtype=="Exclusive Type": 
            for d in dbb:
                seat=d.exclusive
                ar=Trainerdata.query.filter_by(tcode=code).first()
                ar.exclusive=seat-1
                db.session.commit()
        else:
            pass

        check=Trainerdata.query.filter_by(tcode=tcode).first()
        if(seat>0 and check):
            res=Trainee(aadharid=aadharid,trainingtype=trainingtype,tcode=tcode,weight=weight,tname=tname,tphone=tphone,taddress=taddress)
            db.session.add(res)
            db.session.commit()
            flash("Slot is Booked kindly Visit Center for Further Procedure","success")
        else:
            flash("Something Went Wrong","danger")
    
    return render_template("booking.html",query=query)




app.run(debug=True)
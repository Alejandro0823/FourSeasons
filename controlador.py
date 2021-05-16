# import pymongo
from flask_mongoengine import MongoEngine
from mongoengine.queryset.visitor import Q
from bson.objectid import ObjectId
from flask import Flask, render_template, request, redirect, url_for, json, jsonify,session

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'super secret key'


# #Conexion Mongo
# connection = pymongo.MongoClient("mongodb://localhost:27017")
# db = connection["fourseasons"]
# apartments = db["apartments"]
# users = db["users"]

app.config['MONGODB_SETTINGS'] = {
    'db': 'fourseasons',
    'host': 'localhost',
    'port': 27017,
}

db = MongoEngine()
db.init_app(app)

class Apartments(db.Document):
    City = db.StringField()
    Country = db.StringField()
    Direction = db.StringField()
    Location = db.StringField()
    NumRooms = db.StringField()
    imgFile = db.StringField()
    imgsFiles = db.StringField()
    priceNight = db.StringField()
    review = db.StringField()

class Users(db.Document):
    full_name = db.StringField()
    email = db.StringField()
    country = db.StringField()
    city = db.StringField()
    password = db.StringField()
    rol = db.IntField()



##Formulario Index
@app.route('/')
def Index():
    apartments = Apartments.objects.all()
    return render_template('/Index/Index.html',apartments=apartments)


#Rutas Login y registro
@app.route('/login')
def Login():
    return render_template('LoginAndRegister/Login.html')

@app.route('/register')
def Register():
    return render_template('LoginAndRegister/Register.html')

<<<<<<< HEAD
@app.route('/User/SearchApart/<string:id_apatartment>/', methods=['POST','GET'])
def SearchApart(id_apatartment):
    apartments = Apartments.objects(id=id_apatartment).first()
    return render_template('User/SearchApart.html', data=apartments);

##Formulario registro Apartamento Interfaz Admin
=======
##Formulario registro Apartamento Interfaz Admin

>>>>>>> 738fe5f1f85b9743f0b82d7f6efa1641c61aaa3f
@app.route('/admin')
def Admin():
    apartments = Apartments.objects.all()
    return render_template('/Admin/Index.html',apartments=apartments)


@app.route('/registerApart', methods=["POST"])
def RegisterApart():
    if request.method == 'POST':
        City       =   request.form['City']
        Country    =   request.form['Country']
        Direction  =   request.form['Direction']
        Location   =   request.form['Location']
        NumRooms   =   request.form['NumRooms']
        imgFile    =   request.form['imgFile']
        imgsFiles  =   request.form['imgsFiles']
        priceNight =   request.form['priceNight']
        review     =   request.form['review']

        apartmentsave = Apartments(
            City = City,
            Country=Country,
            Direction=Direction,
            Location=Location,
            NumRooms=NumRooms,
            imgFile=imgFile,
            imgsFiles=imgsFiles,
            priceNight=priceNight,
            review=review
            )
        apartmentsave.save()
        return redirect(url_for('Admin'))   
    else:
        return "Error bad request"

##Actualizar Apartamento

@app.route('/updateapartment', methods=['POST'])
def updateapartment():
    pk = request.form['pk']
    namepost = request.form['name']
    value = request.form['value']
    apartments = Apartments.objects(id=pk).first()
    if not apartments:
        return json.dumps({'error':'data not found'})
    else:
        if namepost == 'City':
            apartments.update(City=value)
        elif namepost == 'Country':
            apartments.update(Country=value)
        elif namepost == 'NumRooms':
            apartments.update(NumRooms=value)
        elif namepost == 'priceNight':
            apartments.update(priceNight=value)
        elif namepost == 'review':
            apartments.update(review=value)   

    return json.dumps({'status':'OK'})        

##Eliminar apartamentos
@app.route('/delete/<string:getid>', methods = ['POST','GET'])
def delete(getid):
    print(getid)
    apartments = Apartments.objects(id=getid).first()
    if not apartments:
        return jsonify({'error': 'data not found'})
    else:
        apartments.delete() 
    return redirect('/admin')

##buscar apartamento desde index
@app.route('/SearchApart/<string:getid>', methods = ['POST','GET'])
def SearchApart(getid):
    
    apartments = Apartments.objects(id=getid).first() #consultar apartamento por ID en Mongo DB
    data = json.dumps(apartments) #se convierte el objeto del documento a JSON
    info = json.loads(data) #se parsea el JSON para poder utilizar los campos en la vista 
    print(info)
    


    if not apartments:
        return jsonify({'error': 'data not found'})
    else:
        
        print(getid)
       
    return render_template('/Index/Apartment.html', info=info)   



##Obtener todos los datos DB
@app.route('/ReadAllData')
def ReadAllData():
    result = Apartments.objects.all()
    return render_template('/Admin/Index.html', result=result)

##Ruta Usuario
@app.route('/user')
def User():
    apartments = Apartments.objects.all()
    return render_template('/Index/Index.html',apartments=apartments)



##Formulario registro usuario Interfaz Admin

@app.route('/create_user', methods=["POST"])
def create_user():
    full_name = request.form['full_name']
    email = request.form['email']
    country = request.form['country']
    city = request.form['city']
    userType = request.form['userType']
    password = request.form['password']
    validate_password = request.form['validate_password']

    if userType!="none":
        newUser = Users(
            full_name=full_name,
            email=email,
            country = country,
            city = city,
            password = password,
            rol = int(userType))
        newUser.save()
        return redirect(url_for('Admin'))
    return redirect(url_for('Admin'))

##Formulario registro usuario Interfaz index
@app.route('/create_user_Index', methods=["POST"])
def create_user_Index():
    full_name = request.form['full_name']
    email = request.form['email']
    country = request.form['country']
    city = request.form['city']
    userType = 1
    password = request.form['password']
    validate_password = request.form['validate_password']

    if userType!="none":
        newUser = Users(
            full_name=full_name,
            email=email,
            country = country,
            city = city,
            password = password,
            rol = int(userType))
        newUser.save()
        return redirect(url_for('Index'))
    return redirect(url_for('Index'))

#Validar Usuario
@app.route('/validate_user', methods=["POST"])
def validate_user():
    email = request.form['email']
    password = request.form['password']
    try:
        exist = Users.objects.get(Q(email=email) & Q(password=password))
        
        if exist == None:
            # return redirect(url_for('Login'))
            return 'login'
        else:
            if exist['rol'] == 0:
                # session['Correo'] = email
                # UserData = Users.objects(email=email).first()
                # json = UserData.to_json()
                
                Name = []
                Email = []
                for user in Users.objects(email=email):
                    Name.append(user.full_name)
                    Email.append(user.email)  
                  
                    # users.append(user.to_json())
                print(Name[0])
                print(Email[0])

                session['Name'] = Name[0]
                session['Email'] = Email[0]
            
                
                
                return redirect(url_for('Admin'))
            else:
                session['Correo'] = email
                return redirect(url_for('User'))
    except Exception as e:
        if str(e) == 'Users matching query does not exist.':
            return redirect(url_for('Login'))
            print('usuario no valido')
        else:
            return redirect(url_for('Login'))
            print('error inesperado')


            

        

if __name__ == '__main__':
    app.run(debug=True)
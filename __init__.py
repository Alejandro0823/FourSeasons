# import pymongo
from flask_mongoengine import MongoEngine
from mongoengine.queryset.visitor import Q
from bson.objectid import ObjectId
from flask import Flask, render_template, request, redirect, url_for, json, jsonify, session

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
    'host': 'mongodb://admin:nbz0813@3.220.229.142:27017/fourseasons',
    # 'port': 27017,
    # 'username':'admin',
    # 'password':'nbz013'
    # 'admin': 'nbz013'
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
    Estado = db.IntField()


class Users(db.Document):
    full_name = db.StringField()
    email = db.StringField()
    imgPerfil = db.StringField()
    country = db.StringField()
    city = db.StringField()
    password = db.StringField()
    rol = db.IntField()

class Reservas(db.Document):
    IdUsuario = db.StringField()
    IdApartamento = db.StringField()
    NombreCompleto = db.StringField()
    Nidentificacion = db.StringField()
    FechaInicio = db.StringField()
    FechaFin = db.StringField()
    Correo = db.StringField()
    Telefono= db.StringField()
    Npersonas= db.StringField()
    PrecioNoche = db.StringField()
    
 


# Formulario Index
@app.route('/')
def Index():
    apartments = Apartments.objects.all()
    return render_template('/Index/Index.html', apartments=apartments)


# Rutas Login y registro
@app.route('/login')
def Login():
    return render_template('LoginAndRegister/Login.html')

# Cerrar session
@app.route('/logout', methods=['POST','GET'])
def Logout():
    session['IdUser'] = ""
    session['IdApartment'] = ""
    session['ImgPerfil'] = ""
    session['Name'] = ""
    session['Email'] = ""
    

    return redirect(url_for('Index'))

@app.route('/register')
def Register():
    return render_template('LoginAndRegister/Register.html')

# Formulario registro Apartamento Interfaz Admin
@app.route('/admin')
def Admin():
    apartments = Apartments.objects.all()
    return render_template('/Admin/Index.html', apartments=apartments)

# Ruta Usuario
@app.route('/user')
def User():
    apartments = Apartments.objects.all()
    if session['IdUser'] == "":
        return redirect(url_for('Index'))
    else:
        return render_template('/User/Index.html', apartments=apartments)  


#Ruta reservas generadas por usuarios
@app.route('/reservasUsuarios')
def ReservasUsuarios():
    
    getid = session['IdUser']
    reservas = Reservas.objects(IdUsuario=getid)
    data = json.dumps(reservas)
    info = json.loads(data)

    return render_template('/User/VerReservas.html', info=info)        

#Cancelar reservas por usuario
@app.route('/cancelar/<string:getid>', methods=['POST', 'GET'])
def cancelar(getid):
    
    reservas = Reservas.objects(IdApartamento=getid).first()
    data = json.dumps(reservas)
    info = json.loads(data)
    if not reservas:
        return jsonify({'error': 'data not found'})
    else:
        reservas.delete()
        pk = info['IdApartamento']
        value = "0"
        apartments = Apartments.objects(id=pk).first()
        apartments.update(Estado=value)
    return redirect(url_for('ReservasUsuarios'))


@app.route('/registerApart', methods=["POST"])
def RegisterApart():
    if request.method == 'POST':
        City = request.form['City']
        Country = request.form['Country']
        Direction = request.form['Direction']
        Location = request.form['Location']
        NumRooms = request.form['NumRooms']
        imgFile = request.form['imgFile']
        imgsFiles = request.form['imgsFiles']
        priceNight = request.form['priceNight']
        review = request.form['review']

        apartmentsave = Apartments(
            City=City,
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


#Buscar apartamentos desde usuarios
@app.route('/BuscarApartUsuario')
def BuscarApartUsuario():
    apartments = Apartments.objects.all()
    data = json.dumps(apartments)
    info = json.loads(data)
    print(info)
    return render_template('/User/BuscarApartamentos.html', info=info) 


# Actualizar Apartamento
@app.route('/updateapartment', methods=['POST'])
def updateapartment():
    pk = request.form['pk']
    namepost = request.form['name']
    value = request.form['value']
    apartments = Apartments.objects(id=pk).first()
    if not apartments:
        return json.dumps({'error': 'data not found'})
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

    return json.dumps({'status': 'OK'})

# Eliminar apartamentos
@app.route('/delete/<string:getid>', methods=['POST', 'GET'])
def delete(getid):
    print(getid)
    apartments = Apartments.objects(id=getid).first()
    if not apartments:
        return jsonify({'error': 'data not found'})
    else:
        apartments.delete()
    return redirect('/admin')


#GENERAR RESERVAS
@app.route('/generarReserva', methods=["POST"])
def GenerarReserva():
    if request.method == 'POST':

        IdUsuario = session['IdUser']
        IdApartamento = session['IdApartment'] 
        NombreCompleto = request.form['NombreCompleto']
        Nidentificacion = request.form['Nidentificacion']
        FechaInicio = request.form['FechaInicio']
        FechaFin = request.form['FechaFin']
        Correo = request.form['Correo']
        Telefono = request.form['Telefono']
        Npersonas = request.form['Npersonas']
        PrecioNoche = session['PrecioNoche']
        
        reservasave = Reservas(
            IdUsuario=IdUsuario,
            IdApartamento=IdApartamento,
            NombreCompleto=NombreCompleto,
            Nidentificacion=Nidentificacion,
            FechaInicio=FechaInicio,
            FechaFin=FechaFin,
            Correo=Correo,
            Telefono=Telefono,
            Npersonas=Npersonas,
            PrecioNoche = PrecioNoche
        )
        reservasave.save()

        #cambiar estado en apartamentos
        pk = session['IdApartment']
        value = "1"
        apartments = Apartments.objects(id=pk).first()
        apartments.update(Estado=value)
        
        return redirect(url_for('User'))
    else:
        return "Error bad request"



# buscar apartamento desde index
@app.route('/SearchApartIndex/<string:getid>', methods=['POST', 'GET'])
def SearchApartIndex(getid):

    # consultar apartamento por ID en Mongo DB
    apartments = Apartments.objects(id=getid).first()
    # se convierte el objeto del documento a JSON
    data = json.dumps(apartments)
    # se parsea el JSON para poder utilizar los campos en la vista
    info = json.loads(data)
    

    if not apartments:
        return jsonify({'error': 'data not found'})
    else:
        return render_template('/Index/Apartment.html', info=info)

        

    

##Buscar apartamentos desde usuarios
@app.route('/SearchApartUsers/<string:getid>', methods=['POST', 'GET'])
def SearchApartUsers(getid):

    # consultar apartamento por ID en Mongo DB
    apartments = Apartments.objects(id=getid).first()
    # se convierte el objeto del documento a JSON
    data = json.dumps(apartments)
    # se parsea el JSON para poder utilizar los campos en la vista
    info = json.loads(data)
    session['PrecioNoche'] = info['priceNight']
    print (session['PrecioNoche'])

    if not apartments:
        return jsonify({'error': 'data not found'})
    else:
        # capturar id del apartamento para generar reserva    
        session['IdApartment'] = getid
        return render_template('/User/Apartment.html', info=info)
        
    



# Obtener todos los datos DB
@app.route('/ReadAllData')
def ReadAllData():
    result = Apartments.objects.all()
    return render_template('/Admin/Index.html', result=result)



# Formulario registro usuario Interfaz Admin

@app.route('/create_user', methods=["POST"])
def create_user():
    full_name = request.form['full_name']
    email = request.form['email']
    country = request.form['country']
    city = request.form['city']
    userType = request.form['userType']
    password = request.form['password']
    validate_password = request.form['validate_password']

    if userType != "none":
        newUser = Users(
            full_name=full_name,
            email=email,
            country=country,
            city=city,
            password=password,
            rol=int(userType))
        newUser.save()
        return redirect(url_for('Admin'))
    return redirect(url_for('Admin'))

# Formulario registro usuario Interfaz index


@app.route('/create_user_Index', methods=["POST"])
def create_user_Index():
    full_name = request.form['full_name']
    email = request.form['email']
    imgPerfil = request.form['imgPerfil']
    country = request.form['country']
    city = request.form['city']
    userType = 1
    password = request.form['password']
    validate_password = request.form['validate_password']

    if userType != "none":
        newUser = Users(
            full_name=full_name,
            email=email,
            imgPerfil=imgPerfil,
            country=country,
            city=city,
            password=password,
            rol=int(userType))
        newUser.save()
        return redirect(url_for('Index'))
    return redirect(url_for('Index'))

# Validar Usuario


@app.route('/validate_user', methods=["POST"])
def validate_user():
    email = request.form['email']
    password = request.form['password']
    
    try:
        UserData = Users.objects.get(Q(email=email) & Q(password=password))
        data = json.dumps(UserData)
        info = json.loads(data)

        if info == None:
            return redirect(url_for('Index'))
        else:
            if info['rol'] == 0:
                session['ImgPerfil'] = info['imgPerfil']
                session['Name'] = info['full_name']
                session['Email'] = info['email']
                return redirect(url_for('Admin'))
            else:
                p1 = info['_id']
                p2 = p1['$oid']
                session['IdUser'] = p2
                session['ImgPerfil'] = info['imgPerfil']
                session['Name'] = info['full_name']
                session['Email'] = info['email']
                return redirect(url_for('User'))
                
    except Exception as e:
        if str(e) == 'Users matching query does not exist.':
            print('usuario no valido')
            return redirect(url_for('Index'))
        else:
            print('error inesperado')
            return redirect(url_for('Index'))

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask,render_template, request, flash, url_for, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import select
from sqlalchemy import func
import json

app = Flask (__name__)
app.secret_key = 'flask message'
#------------------------------------ Connection avec la base de données -------------------------
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:gningue1991@localhost/GestionFormulaireSA'
db = SQLAlchemy(app)
#------------------------------------ Création des tables ou classes ------------------------
class Etudiant(db.Model):
    __tablename__='Etudiant'
    id_etudiant = db.Column(db.Integer, primary_key=True)
    matricule_etudiant = db.Column(db.String(255))
    nom_etudiant = db.Column(db.String(255))
    prenom_etudiant = db.Column(db.String(255))
    date_naissance = db.Column(db.Date)

    def __init__(self, matricule_etudiant, nom_etudiant, prenom_etudiant, date_naissance):
        self.matricule_etudiant = matricule_etudiant
        self.nom_etudiant = nom_etudiant
        self.prenom_etudiant = prenom_etudiant
        self.date_naissance = date_naissance
    
    def __repr__(self):
        return '<Etudiant %r>' % self.matricule_etudiant

class Classe(db.Model):
    __tablename__='Classe'
    id_classe = db.Column(db.Integer, primary_key=True)
    libelle_classe = db.Column(db.String(255))
    montant_ins = db.Column(db.String(255))
    mensualite = db.Column(db.String(255))
    id_filiere = db.Column(db.Integer, db.ForeignKey ('Filiere.id_filiere'))

    def __init__(self, libelle_classe, montant_ins, mensualite, id_filiere):
        self.libelle_classe = libelle_classe
        self.montant_ins = montant_ins
        self.mensualite = mensualite
        self.id_filiere = id_filiere
    
    def __repr__(self):
        return '<Classe %r>' % self.libelle_classe

class Inscription(db.Model):
    __tablename__='Inscription'
    id_ins = db.Column(db.Integer, primary_key=True)
    date_ins = db.Column(db.Date)
    annee_acad = db.Column(db.String(255))
    id_etudiant = db.Column(db.Integer, db.ForeignKey ('Etudiant.id_etudiant'))
    id_classe = db.Column(db.Integer, db.ForeignKey ('Classe.id_classe'))


    def __init__(self, date_ins, annee_acad, id_etudiant, id_classe):
        self.date_ins = date_ins
        self.annee_acad = annee_acad
        self.id_etudiant = id_etudiant
        self.id_classe = id_classe
    
    def __repr__(self):
        return '<Inscription %r>' % self.date_ins

class Filiere(db.Model):
    __tablename__='Filiere'
    id_filiere = db.Column(db.Integer, primary_key=True)
    libelle_filiere = db.Column(db.String(255))

    def __init__(self, libelle_filiere):
        self.libelle_filiere = libelle_filiere

    def __repr__(self):
        return '<Filiere %r>' % self.libelle_filiere


@app.route('/')
def index():

    etudiant=Etudiant.query.all()
    db.session.commit()

    filiere=Filiere.query.all()
    db.session.commit()

    classe=Classe.query.all()
    db.session.commit()
     #------------------------------- Gérer matricule -------------------------------------------
    matricule=db.session.query(func.max(Etudiant.id_etudiant)).one()
    
    if matricule[0] == None:
        num=1
        val='-'+str(num)+'-'
        sa = "SA"+val+"Code"
    else:
        num=matricule[0]+1
        val='-'+str(num)+'-'
        sa="SA"+val+"Code"

    return render_template('pages/index.html',classe=classe,etudiant=etudiant,sa=sa,filiere=filiere)
#--------------------------------------- Insertion des données dans la base de données ------------------
@app.route('/add', methods = ['GET', 'POST'])
def add():
   if request.method == 'POST':
        if not request.form['matricule'] or not request.form['nom'] or not request.form['prenom'] or not request.form['naissance'] :
         flash('Please enter all the fields', 'error')
        else:
         etudiant = Etudiant(request.form['matricule'], request.form['nom'],
            request.form['prenom'], request.form['naissance'])
         
         db.session.add(etudiant)
         db.session.commit()
         flash('Record was successfully added')
         return redirect(url_for('index'))
   return render_template('index.html', etudiant = Etudiant.query.all())

#---------------------------------- Ajax Jquery --------------------------------------------
@app.route('/process',methods= ['POST'])    
def process():
    matricule = request.form['matricule']
    nom = request.form['nom']
    prenom = request.form['prenom']
    naissance = request.form['naissance']
    output = matricule + nom + prenom + naissance
    db.session.add(Etudiant(matricule, nom, prenom, naissance))
    db.session.commit() 
    if matricule and nom and prenom and naissance:
        return jsonify({'output':'Full Name: ' + output})
    return jsonify({'error' : 'Missing data!'})
    
if (__name__) == '__main__':
    app.run(debug=True, port=3000) 

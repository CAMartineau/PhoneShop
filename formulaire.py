from wtforms import Form, StringField, IntegerField, TextAreaField, PasswordField, validators

# Formulaire pour la recherche de produit
class searchForm(Form):
    model = StringField('Nom du model',[validators.Length(min=1, max=50)])
    prixMin = IntegerField('Prix min')
    prixMax = IntegerField('Prix max')

# Formulaire pour l'inscription d'un utilisateur a la base de donnée
class InscriptionForm(Form):
    name = StringField('Prénom', [validators.Length(min=2, max=50)])
    lastname = StringField('Nom', [validators.Length(min=2, max=25)])
    email = StringField('Adresse courriel', [validators.Email(message="Cette adresse email est invalide"),
                                             validators.Length(max=100, message="Cette adresse email est trop longue")])

    password = PasswordField('Mot de passe',
                             [validators.Required(),validators.EqualTo('passwordConfirm', message='Passwords must match')])
    
    passwordConfirm = PasswordField('Confirmer le mot de passe')

# Formulaire pour l'inscription d'un utilisateur a la base de donn
class ConnectionForm(Form):
    # les 2 champs sont obligatoires
    email = StringField('Adresse courriel', [validators.data_required(message='Ce champ doit etre remplis')])
    password = PasswordField('Mot de passe', [validators.data_required(message='Ce champ doit etre remplis')])

from wtforms import Form, StringField, TextAreaField, PasswordField, validators

class searchForm(Form):
    model = StringField([validators.Length(min=1, max=50)])
	
class InscriptionForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    lastname = StringField('Lastname', [validators.Length(min=4, max=25)])
    email = StringField('Adresse courriel', [validators.Email(message="Cette adresse email est invalide"),
                                             validators.Length(max=100, message="Cette adresse email est trop longue")])

    password = PasswordField('Mot de passe',
                             [validators.Required(),validators.EqualTo('passwordConfirm', message='Passwords must match')])
    
    passwordConfirm = PasswordField('Confirmer le mot de passe')

class ConnectionForm(Form):
    # les 2 champs sont obligatoires
    email = StringField('Adresse courriel', [validators.data_required(message='Ce champ doit etre remplis')])
    password = PasswordField('Mot de passe', [validators.data_required(message='Ce champ doit etre remplis')])

from wtforms import Form, StringField, validators, SubmitField
from flask_wtf import FlaskForm


class ArticlesForm(FlaskForm):
    article1 = StringField('Article 1', [validators.Length(min=0, max=25)])
    article2 = StringField('Article 2', [validators.Length(min=0, max=25)])
    article3 = StringField('Article 3', [validators.Length(min=0, max=25)])
    article4 = StringField('Article 4', [validators.Length(min=0, max=25)])
    article5 = StringField('Article 5', [validators.Length(min=0, max=25)])
    article6 = StringField('Article 6', [validators.Length(min=0, max=25)])
    submit = SubmitField('Submit')

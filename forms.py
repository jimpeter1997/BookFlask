from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired

class SearchForm(FlaskForm):
    keyword=StringField('keyword',validators=[DataRequired()])
    submit=SubmitField('开始搜索')

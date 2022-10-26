from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, TextAreaField, SubmitField, validators, ValidationError

class ContactForm(FlaskForm):
  name = StringField("Username",  [validators.DataRequired("Please enter your name.")])
  email = StringField("Email",  [validators.DataRequired("Please enter your email address."), validators.Email("Please enter your email address.")])
  subject = "Ore Miner - Contact Form"
  message = TextAreaField("Message",  [validators.DataRequired("Please enter a message.")])
  submit = SubmitField("Send")

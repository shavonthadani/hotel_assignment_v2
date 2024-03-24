from flask_wtf import FlaskForm
from wtforms import FieldList, FormField, StringField, SelectField, IntegerField, SubmitField, DateField, ValidationError, validators
from wtforms.validators import DataRequired, Optional
from . import db
from .models import Customer

class PhoneNumberForm(FlaskForm):
    phone_number = StringField('Phone Number', validators=[validators.DataRequired()])

class EmailForm(FlaskForm):
    email = StringField('Email', validators=[validators.DataRequired(), validators.Email()])
class SearchRoomsForm(FlaskForm):
    start_date = DateField('Start Date', validators=[DataRequired()])
    end_date = DateField('End Date', validators=[DataRequired()])
    capacity = IntegerField('Capacity', validators=[DataRequired()])
    area = StringField('Area', validators=[Optional()])
    hotel_chain = SelectField('Hotel Chain', choices=[
        ('Luxury Resorts', 'Luxury Resorts'),
        ('Business Inn', 'Business Inn'),
        ('Budget Stays', 'Budget Stays'),
        ('Travellers Joy', 'Travellers Joy'),
        ('Comfortable Retreat', 'Comfortable Retreat')], validators=[Optional()])
    category = SelectField('Category', choices=[('1', '1 Star'), ('2', '2 Star'), ('3', '3 Star'), ('4', '4 Star'), ('5', '5 Star')])
    min_rooms = IntegerField('Minimum Number of Rooms', validators=[Optional()])
    price = IntegerField('Price Limit', validators=[Optional()])
    submit = SubmitField('Search')

class NewBookingForm(FlaskForm):
    new_customer_id = StringField('Enter a Customer ID (SIN or driver\'s license)', validators=[Optional()])
    street_number = IntegerField('Street Number', validators=[DataRequired()])
    street_name = StringField('Street Name', validators=[DataRequired()])
    apt_number = StringField('Apartment Number', validators=[Optional()])
    city = StringField('City', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    zip_code = StringField('ZIP Code', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    middle_name = StringField('Middle Name', validators=[Optional()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    phone_numbers = StringField('Phone number(s) (Seperate multiple phone numbers by commas)', validators=[DataRequired()])
    emails = StringField('Email(s) (Seperate multiple emails by commas)', validators=[DataRequired()])
    submit = SubmitField('Enter')


class ExistingBookingForm(FlaskForm):
    existing_customer_id = StringField('Enter a Customer ID (SIN or driver\'s license)', validators=[DataRequired()])
    submit = SubmitField('Confirm Booking')


class DirectRentingForm(FlaskForm):
    customerID = StringField('Enter Customer\'s ID', validators=[DataRequired()])
    employee_ssn = StringField('Enter your SSN', validators=[DataRequired()])
    hotel_id = IntegerField('Enter your hotel\'s id', validators=[DataRequired()])
    room_number = StringField('Enter room number', validators=[DataRequired()])
    start_date = DateField('Start Date', validators=[DataRequired()])
    end_date = DateField('End Date', validators=[DataRequired()])
    credit_card_number = StringField('Enter customer\'s credit card number', validators=[DataRequired()])
    cvv = StringField('Enter customer\'s cvv', validators=[DataRequired()])
    credit_card_expiry = DateField('Enter customer\'s credit card expiry', validators=[DataRequired()])
    billing_address = StringField('Enter customer\'s billing address', validators=[DataRequired()])
    submit = SubmitField('Register Customer')
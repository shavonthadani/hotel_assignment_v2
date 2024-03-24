from flask import render_template, request, redirect, url_for, flash
from wtforms import ValidationError
from . import db
from sqlalchemy import text
from .models import Customer
from .forms import SearchRoomsForm, NewBookingForm, ExistingBookingForm, DirectRentingForm
from flask import current_app as app 


start_date = None
end_date = None

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/view1')
def view1():
    # SQL query to get the number of available rooms by area
    sql_query = """
    SELECT * FROM available_rooms_per_area;
    """
    areas_tuples = db.engine.execute(sql_query).fetchall()
    # Convert each tuple to a dictionary
    areas = [{'area': row[0], 'available_rooms': row[1]} for row in areas_tuples]
    return render_template('view1.html', areas=areas)

@app.route('/view2')
def view2():
    # SQL query to get the aggregated capacity of rooms per hotel, including hotel chain name and hotel city
    sql_query = """
    SELECT h.hotelID, hc.name AS hotel_chain_name, h.city, SUM(r.capacity) AS total_capacity
    FROM room r
    JOIN hotel h ON r.hotelID = h.hotelID
    JOIN hotel_chain hc ON h.hotel_chainID = hc.hotel_chainID
    GROUP BY h.hotelID, hc.name, h.city;
    """
    hotel_info_tuples = db.engine.execute(sql_query).fetchall()
    # Convert each tuple to a dictionary for easier access in the template
    hotels = [{'hotelID': row[0], 'hotel_chain_name': row[1], 'city': row[2], 'total_capacity': row[3]} for row in hotel_info_tuples]
    return render_template('view2.html', hotels=hotels)


@app.route('/bookings')
def show_bookings():
    # SQL query to get all bookings with status 'booking', including hotel chain name, city, and room capacity
    sql_query = """
    SELECT br.bookingID, br.customerID, br.hotelID, br.room_number, br.check_in_date, br.check_out_date,
           hc.name AS hotel_chain_name, h.city, r.capacity
    FROM booking_renting br
    JOIN hotel h ON br.hotelID = h.hotelID
    JOIN hotel_chain hc ON h.hotel_chainID = hc.hotel_chainID
    JOIN room r ON br.hotelID = r.hotelID AND br.room_number = r.room_number
    WHERE br.status = 'booking';
    """
    booking_tuples = db.engine.execute(sql_query).fetchall()
    # Convert each tuple to a dictionary
    bookings = [dict(bookingID=row[0], customerID=row[1], hotelID=row[2], room_number=row[3], 
                     check_in_date=row[4], check_out_date=row[5], hotel_chain_name=row[6], 
                     city=row[7], capacity=row[8]) for row in booking_tuples]
    return render_template('booking_to_renting.html', bookings=bookings)

@app.route('/convert/<int:booking_id>', methods=['GET', 'POST'])
def convert_to_rental(booking_id):
    if request.method == 'POST':
        employee_ssn = request.form['employee_ssn']
        credit_card_number = request.form['credit_card_number']
        cvv = request.form['cvv']
        credit_card_expiry = request.form['credit_card_expiry']
        billing_address = request.form['billing_address']
        # Check if SSN exists
        ssn_query = "SELECT EXISTS (SELECT 1 FROM employee WHERE ssn = :ssn);"
        ssn_exists = db.engine.execute(text(ssn_query), {'ssn': employee_ssn}).fetchone()

        if ssn_exists[0]:
            # Update the booking status to 'rental' along with credit card details
            update_query = """
            UPDATE booking_renting
            SET status = 'renting', ssn = :ssn, credit_card_number = :credit_card_number, cvv = :cvv, credit_card_expiry = :credit_card_expiry, billing_address =:billing_address
            WHERE bookingID = :booking_id;
            """
            db.engine.execute(text(update_query), {'ssn': employee_ssn, 'booking_id': booking_id,'credit_card_number': credit_card_number, 'cvv': cvv, 'credit_card_expiry': credit_card_expiry, 'billing_address': billing_address})
            # Archive the rental
            db.engine.execute(text("""
                INSERT INTO archives (bookingID, customerID, check_in_date, check_out_date, date_booked, status, room_number)
                SELECT bookingID, customerID, check_in_date, check_out_date, date_booked, 'renting' AS status, room_number
                FROM booking_renting
                WHERE bookingID = :booking_id
            """), {'booking_id': booking_id})

            return redirect(url_for('success_renting'))
        else:
            flash("Employee SSN not recognized.", "error")

    # If GET request or form not submitted, show the form
    return render_template('convert_to_rental.html', booking_id=booking_id)



@app.route('/direct_renting',  methods=['GET', 'POST'])
def direct_renting():
    form = DirectRentingForm()
    if form.is_submitted():
        customer_id = form.customerID.data
        employee_ssn = form.employee_ssn.data
        hotel_id = form.hotel_id.data
        room_number = form.room_number.data
        start_date = form.start_date.data
        end_date = form.end_date.data 
        credit_card_number = form.credit_card_number.data
        cvv = form.cvv.data
        credit_card_expiry = form.credit_card_expiry.data
        billing_address = form.billing_address.data
    
        #check if customer_id exists:
        check_id_sql_query = """
        SELECT EXISTS (
            SELECT 1 FROM customer 
            WHERE customerID = :customerID
        );
        """
        #check if ssn exists:
        check_ssn_sql_query = """
        SELECT EXISTS (
            SELECT 1 FROM employee 
            WHERE ssn = :employee_ssn
        );
        """
        # SQL query to check if the specific room in the specified hotel exists
        check_room_sql_query = """
        SELECT EXISTS (
            SELECT 1 FROM room 
            WHERE hotelID = :hotel_id AND room_number = :room_number
        );
        """
        # check if 
        check_availability_sql_query = """
        SELECT NOT EXISTS (
            SELECT 1 
            FROM booking_renting
            WHERE hotelID = :hotel_id 
            AND room_number = :room_number
            AND (
                (check_in_date BETWEEN :start_date AND :end_date)
                OR 
                (check_out_date BETWEEN :start_date AND :end_date)
                OR 
                (check_in_date <= :start_date AND check_out_date >= :end_date)
            )
        ) AS available;
        """

        # Check if customer exists
        query = text(check_id_sql_query)
        result = db.engine.execute(query, {'customerID': customer_id}).fetchone()
        if not result[0]:  # If customer is found, redirect to other booking page
            flash("Customer has not been registered. Please register customer using above button first","error")
        else:
            # Check if employee exists
            query = text(check_ssn_sql_query)
            result = db.engine.execute(query, {'employee_ssn': employee_ssn}).fetchone()
            if not result[0]:  # If customer is found, redirect to other booking page
                flash("Employee SSN not recognized", "error")
            else:
                # Check if the room exists
                room_query = text(check_room_sql_query)
                room_exists_result = db.engine.execute(room_query, {'hotel_id': hotel_id, 'room_number': room_number}).fetchone()
                if not room_exists_result[0]:  # If the room is not found
                    flash("The specified room or the hotel does not exist", "error")
                else:
                    # Check if dates are available
                    availability_query = text(check_availability_sql_query)
                    availability_result = db.engine.execute(availability_query, {
                        'hotel_id': hotel_id,
                        'room_number': room_number,
                        'start_date': start_date,
                        'end_date': end_date
                    }).fetchone()
                    if not availability_result['available']:
                         flash("Room is not available for the selected dates. Please choose different dates.", "error")
                    else:
                        # Making the booking
                        status = "renting"
                        params_renting = {
                            'customerID': customer_id,
                            'ssn': employee_ssn,
                            'hotelID': hotel_id,
                            'room_number': room_number,
                            'status': status,
                            'check_in_date': start_date,
                            'check_out_date': end_date,
                            'credit_card_number': credit_card_number,
                            'cvv': cvv,
                            'credit_card_expiry': credit_card_expiry,
                            'billing_address': billing_address
                        }

                        sql_query_booking = """
                        INSERT INTO booking_renting (
                            customerID,
                            ssn,
                            hotelID,
                            date_booked,
                            room_number,
                            status,
                            check_in_date,
                            check_out_date,
                            credit_card_number,
                            cvv,
                            credit_card_expiry,
                            billing_address

                        ) VALUES (
                            :customerID,
                            :ssn,
                            :hotelID,
                            CURRENT_DATE,
                            :room_number,
                            :status,
                            :check_in_date,
                            :check_out_date,
                            :credit_card_number,
                            :cvv,
                            :credit_card_expiry,
                            :billing_address
                        );
                        """

                        # Execute the booking insert query
                        db.engine.execute(text(sql_query_booking), params_renting)
                        archive_query = """
                        INSERT INTO archives (
                            bookingID, customerID, check_in_date, check_out_date, date_booked, status, room_number
                        ) VALUES (
                            (SELECT MAX(bookingID) FROM booking_renting),  -- Assuming bookingID is auto-incremented and you want to fetch the latest
                            :customerID,
                            :check_in_date,
                            :check_out_date,
                            CURRENT_DATE,
                            'renting',  -- Assuming status is 'renting' for direct renting entries
                            :room_number
                        );
                        """
                        db.engine.execute(text(archive_query), params_renting)
                        return redirect(url_for('success_renting'))    
    return render_template('direct_renting.html', form=form)

@app.route('/register_customer_inperson',  methods=['GET', 'POST'])
def register_customer():
    form = NewBookingForm()
    if form.is_submitted():
        new_customer_id = form.new_customer_id.data
        street_number = form.street_number.data
        street_name = form.street_name.data
        apt_number = form.apt_number.data
        city = form.city.data
        state = form.state.data 
        zip_code = form.zip_code.data
        first_name = form.first_name.data
        middle_name = form.middle_name.data
        last_name = form.last_name.data
        phone_numbers = form.phone_numbers.data
        emails = form.emails.data

        check_id_sql_query = """
        SELECT EXISTS (
            SELECT 1 FROM customer 
            WHERE customerID = :customerID
        );
        """
        # Execute the query with the provided customerID
        query = text(check_id_sql_query)
        result = db.engine.execute(query, {'customerID': new_customer_id}).fetchone()
        if result[0]:  # If customer is found, redirect to other booking page
            flash("Your id has already been registered")
        else:
            params_customer = {
                'customerID': new_customer_id,
                'street_number': street_number,
                'street_name': street_name,
                'apt_number': apt_number,
                'city': city,
                'state': state,
                'zip_code': zip_code,
                'first_name': first_name,
                'middle_name': middle_name,
                'last_name': last_name
            }

            sql_query_customer = """
            INSERT INTO customer (
                customerID,
                date_of_registration,
                street_number,
                street_name,
                apt_number,
                city,
                state,
                zip_code,
                first_name,
                middle_name,
                last_name
            ) VALUES (
                :customerID,
                CURRENT_DATE,
                :street_number,
                :street_name,
                :apt_number,
                :city,
                :state,
                :zip_code,
                :first_name,
                :middle_name,
                :last_name
            );
            """

            # Execute the query to insert the new customer
            db.engine.execute(text(sql_query_customer), params_customer)
            # Insert a phone number
            phone_num_array = phone_numbers.split(",")
            for num in phone_num_array:
                params_phone = {'customerID': new_customer_id, 'phone_number': num.strip()}
                sql_query_phone = """
                INSERT INTO customer_phone_numbers (customerID, phone_number) VALUES (:customerID, :phone_number);
                """
                db.engine.execute(text(sql_query_phone), params_phone)

            # Insert an email
            email_array = emails.split(",")
            for email in email_array:
                params_email = {'customerID': new_customer_id, 'email': email.strip()}
                sql_query_email = """
                INSERT INTO customer_emails (customerID, email) VALUES (:customerID, :email);
                """
                db.engine.execute(text(sql_query_email), params_email)
            return redirect(url_for('direct_renting'))
    return render_template("register_customer.html", form=form)


@app.route('/new_book_room/<int:hotel_id>/<room_number>', methods=['GET', 'POST'])
def new_book_room(hotel_id, room_number):
    form = NewBookingForm()
    if form.is_submitted():
        new_customer_id = form.new_customer_id.data
        street_number = form.street_number.data
        street_name = form.street_name.data
        apt_number = form.apt_number.data
        city = form.city.data
        state = form.state.data 
        zip_code = form.zip_code.data
        first_name = form.first_name.data
        middle_name = form.middle_name.data
        last_name = form.last_name.data
        phone_numbers = form.phone_numbers.data
        emails = form.emails.data

        check_id_sql_query = """
        SELECT EXISTS (
            SELECT 1 FROM customer 
            WHERE customerID = :customerID
        );
        """
        # Execute the query with the provided customerID
        query = text(check_id_sql_query)
        result = db.engine.execute(query, {'customerID': new_customer_id}).fetchone()
        if result[0]:  # If customer is found, redirect to other booking page
            flash("Your id is already registered. Go back and book as an existing customer")
        else:
            params_customer = {
                'customerID': new_customer_id,
                'street_number': street_number,
                'street_name': street_name,
                'apt_number': apt_number,
                'city': city,
                'state': state,
                'zip_code': zip_code,
                'first_name': first_name,
                'middle_name': middle_name,
                'last_name': last_name
            }

            sql_query_customer = """
            INSERT INTO customer (
                customerID,
                date_of_registration,
                street_number,
                street_name,
                apt_number,
                city,
                state,
                zip_code,
                first_name,
                middle_name,
                last_name
            ) VALUES (
                :customerID,
                CURRENT_DATE,
                :street_number,
                :street_name,
                :apt_number,
                :city,
                :state,
                :zip_code,
                :first_name,
                :middle_name,
                :last_name
            );
            """

            # Execute the query to insert the new customer
            db.engine.execute(text(sql_query_customer), params_customer)
            # Insert a phone number
            phone_num_array = phone_numbers.split(",")
            for num in phone_num_array:
                params_phone = {'customerID': new_customer_id, 'phone_number': num.strip()}
                sql_query_phone = """
                INSERT INTO customer_phone_numbers (customerID, phone_number) VALUES (:customerID, :phone_number);
                """
                db.engine.execute(text(sql_query_phone), params_phone)

            # Insert an email
            email_array = emails.split(",")
            for email in email_array:
                params_email = {'customerID': new_customer_id, 'email': email.strip()}
                sql_query_email = """
                INSERT INTO customer_emails (customerID, email) VALUES (:customerID, :email);
                """
                db.engine.execute(text(sql_query_email), params_email)  

            
            # Making the booking
            status = "booking"

            params_booking = {
                'customerID': new_customer_id,
                'hotelID': hotel_id,
                'room_number': room_number,
                'status': status,
                'check_in_date': start_date,
                'check_out_date': end_date
            }

            sql_query_booking = """
            INSERT INTO booking_renting (
                customerID,
                hotelID,
                date_booked,
                room_number,
                status,
                check_in_date,
                check_out_date
            ) VALUES (
                :customerID,
                :hotelID,
                CURRENT_DATE,
                :room_number,
                :status,
                :check_in_date,
                :check_out_date
            );
            """

            # Execute the booking insert query
            db.engine.execute(text(sql_query_booking), params_booking)

            # Archive the booking
            db.engine.execute(text("""
                INSERT INTO archives (bookingID, customerID, check_in_date, check_out_date, date_booked, status, room_number)
                SELECT bookingID, customerID, check_in_date, check_out_date, date_booked, status, room_number
                FROM booking_renting
                WHERE customerID = :customerID AND hotelID = :hotelID AND room_number = :room_number
            """), params_booking)
            return redirect(url_for('success'))     
        
    
    # If GET request or form not valid, render the booking form template
    return render_template('booking.html', form=form)

@app.route('/existing_book_room/<int:hotel_id>/<room_number>', methods=['GET', 'POST'])
def existing_book_room(hotel_id, room_number):
    form = ExistingBookingForm()
    if form.is_submitted():
        customer_id = form.existing_customer_id.data
        params = {'customerID': customer_id}
        sql_query = """
        SELECT EXISTS (
            SELECT 1 FROM customer 
            WHERE customerID = :customerID
        );
        """
        # Execute the query with the provided customerID
        query = text(sql_query)
        result = db.engine.execute(query, params).fetchone()
        if not result[0]:  # If no customer is found with the provided ID, raise a validation error
             flash('Customer ID does not exist in the database.', 'error')
        else:
            # Making the booking
            status = "booking"

            params_booking = {
                'customerID': customer_id,
                'hotelID': hotel_id,
                'room_number': room_number,
                'status': status,
                'check_in_date': start_date,
                'check_out_date': end_date
            }

            sql_query_booking = """
            INSERT INTO booking_renting (
                customerID,
                hotelID,
                date_booked,
                room_number,
                status,
                check_in_date,
                check_out_date
            ) VALUES (
                :customerID,
                :hotelID,
                CURRENT_DATE,
                :room_number,
                :status,
                :check_in_date,
                :check_out_date
            );
            """

            # Execute the booking insert query
            db.engine.execute(text(sql_query_booking), params_booking)
            # Archive the booking
            db.engine.execute(text("""
                INSERT INTO archives (bookingID, customerID, check_in_date, check_out_date, date_booked, status, room_number)
                SELECT bookingID, customerID, check_in_date, check_out_date, date_booked, status, room_number
                FROM booking_renting
                WHERE customerID = :customerID AND hotelID = :hotelID AND room_number = :room_number
            """), params_booking)

            return redirect(url_for('success'))
        
    # If GET request or form not valid, render the booking form template
    return render_template('existing_booking.html', form=form)

@app.route('/booked', methods=['GET'])
def success():
    return render_template('booking_success.html')
@app.route('/rented', methods=['GET'])
def success_renting():
    return render_template('renting_success.html')
@app.route('/search', methods=['GET', 'POST'])
def search_rooms():
    form = SearchRoomsForm()
    if form.validate_on_submit():
        # Retrieve form data
        global start_date
        global end_date
        start_date = form.start_date.data
        end_date = form.end_date.data
        capacity = form.capacity.data
        category = form.category.data
        
        # Optional fields
        area = form.area.data
        hotel_chain = form.hotel_chain.data
        price = form.price.data
        min_rooms = form.min_rooms.data if form.min_rooms.data else 0
        # Base SQL query incorporating mandatory fields and excluding booked rooms
        sql_query = """
            SELECT room.*, hotel_chain.name AS chain_name, hotel.city,
                   (SELECT string_agg(ra.amenities, ', ') 
                    FROM room_amenities ra 
                    WHERE ra.room_number = room.room_number AND ra.hotelID = room.hotelID) AS amenities,
                   (SELECT string_agg(rp.problem, ', ') 
                    FROM room_problems rp 
                    WHERE rp.room_number = room.room_number AND rp.hotelID = room.hotelID) AS problems
            FROM room
            JOIN hotel ON room.hotelID = hotel.hotelID
            JOIN hotel_chain ON hotel.hotel_chainID = hotel_chain.hotel_chainID
            WHERE room.capacity >= :capacity
              AND hotel.star_rating = :category
              AND NOT EXISTS (
                SELECT 1 
                FROM booking_renting br
                WHERE br.hotelID = room.hotelID
                  AND br.room_number = room.room_number
                  AND (br.check_in_date <= :end_date AND br.check_out_date >= :start_date)
              )
              -- Additional conditions based on optional fields
        """

        # Parameters dictionary
        params = {'capacity': capacity, 'category': category, 'start_date': start_date, 'end_date': end_date, 'min_rooms': min_rooms}

        # Append conditions for optional fields
        if area:
            sql_query += " AND hotel.city ILIKE :area"
            params['area'] = f"%{area}%"
        
        if hotel_chain:
            sql_query += " AND hotel.hotel_chainID IN (SELECT hotel_chainID FROM hotel_chain WHERE name = :hotel_chain)"
            params['hotel_chain'] = hotel_chain
        
        if price is not None:  # Check if price is provided (it could be 0)
            sql_query += " AND room.price <= :price"
            params['price'] = price

        # Execute the constructed query
        query = text(sql_query)
        available_rooms = db.engine.execute(query, **params).fetchall()

        # Render the template with available rooms
        return render_template('search_results.html', rooms=available_rooms)
    return render_template('search.html', form=form)
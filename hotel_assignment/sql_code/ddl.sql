-- Hotel Chain
CREATE TABLE hotel_chain (
    hotel_chainID SERIAL PRIMARY KEY,
    name VARCHAR(255),
    street_number INT,
    street_name VARCHAR(255),
    apt_number VARCHAR(255),
    city VARCHAR(255),
    state VARCHAR(255),
    zip VARCHAR(20)
);

-- Hotel
CREATE TABLE hotel (
    hotelID SERIAL PRIMARY KEY,
    hotel_chainID INT,
    star_rating INT,
    street_number INT,
    street_name VARCHAR(255),
    apt_number VARCHAR(255),
    city VARCHAR(255),
    state VARCHAR(255),
    zip VARCHAR(20),
    FOREIGN KEY (hotel_chainID) REFERENCES hotel_chain (hotel_chainID)
);

-- Customer
CREATE TABLE customer (
    customerID VARCHAR(255) PRIMARY KEY,
    date_of_registration DATE,
    street_number INT,
    street_name VARCHAR(255),
    apt_number VARCHAR(255),
    city VARCHAR(255),
    state VARCHAR(255),
    zip VARCHAR(20),
    first_name VARCHAR(255),
    middle_name VARCHAR(255),
    last_name VARCHAR(255)
);

-- Room
CREATE TABLE room (
    hotelID INT,
    room_number INT,
    price DECIMAL(10, 2),
    view_type VARCHAR(255),
    is_extended BOOLEAN,
    capacity INT,
    PRIMARY KEY (hotelID, room_number),
    FOREIGN KEY (hotelID) REFERENCES hotel (hotelID)
);

-- Employee
CREATE TABLE employee (
    SSN VARCHAR(11) PRIMARY KEY,
    hotelID INT,
    street_number INT,
    street_name VARCHAR(255),
    apt_number VARCHAR(255),
    city VARCHAR(255),
    state VARCHAR(255),
    zip VARCHAR(20),
    first_name VARCHAR(255),
    middle_name VARCHAR(255),
    last_name VARCHAR(255),
    FOREIGN KEY (hotelID) REFERENCES hotel (hotelID)
);

-- Booking/Renting
CREATE TABLE booking_renting (
    bookingID SERIAL PRIMARY KEY,
    customerID VARCHAR(255),
    SSN VARCHAR(11),
    hotelID INT,
    room_number INT,
    check_in_date DATE,
    check_out_date DATE,
    date_booked DATE,
    status VARCHAR(255),
    credit_card_number VARCHAR(19),
    cvv VARCHAR(5),
    credit_card_expiry DATE,
    billing_address VARCHAR(255),
    FOREIGN KEY (customerID) REFERENCES customer (customerID),
    FOREIGN KEY (SSN) REFERENCES employee (SSN),
    FOREIGN KEY (hotelID, room_number) REFERENCES room (hotelID, room_number)
);

-- Archives
CREATE TABLE archives (
    archiveID SERIAL PRIMARY KEY,
    bookingID INT,
    customerID VARCHAR(255),
    check_in_date DATE,
    check_out_date DATE,
    date_booked DATE,
    status VARCHAR(255),
    room_number INT
);

-- Hotel Chain Phone Numbers
CREATE TABLE hotel_chain_phone_numbers (
    hotel_chainID INT,
    phone_number VARCHAR(20),
    PRIMARY KEY (hotel_chainID, phone_number),
    FOREIGN KEY (hotel_chainID) REFERENCES hotel_chain (hotel_chainID)
);

-- Hotel Phone Numbers
CREATE TABLE hotel_phone_numbers (
    hotelID INT,
    phone_number VARCHAR(20),
    PRIMARY KEY (hotelID, phone_number),
    FOREIGN KEY (hotelID) REFERENCES hotel (hotelID)
);

-- Customer Phone Numbers
CREATE TABLE customer_phone_numbers (
    customerID VARCHAR(255),
    phone_number VARCHAR(20),
    PRIMARY KEY (customerID, phone_number),
    FOREIGN KEY (customerID) REFERENCES customer (customerID)
);

-- Employee Phone Numbers
CREATE TABLE employee_phone_numbers (
    SSN VARCHAR(11),
    phone_number VARCHAR(20),
    PRIMARY KEY (SSN, phone_number),
    FOREIGN KEY (SSN) REFERENCES employee (SSN)
);

-- Hotel Chain Emails
CREATE TABLE hotel_chain_emails (
    hotel_chainID INT,
    email VARCHAR(255),
    PRIMARY KEY (hotel_chainID, email),
    FOREIGN KEY (hotel_chainID) REFERENCES hotel_chain (hotel_chainID)
);

-- Hotel Emails
CREATE TABLE hotel_emails (
    hotelID INT,
    email VARCHAR(255),
    PRIMARY KEY (hotelID, email),
    FOREIGN KEY (hotelID) REFERENCES hotel (hotelID)
);

-- Customer Emails
CREATE TABLE customer_emails (
    customerID VARCHAR(255),
    email VARCHAR(255),
    PRIMARY KEY (customerID, email),
    FOREIGN KEY (customerID) REFERENCES customer (customerID)
);

c

-- Room Amenities
CREATE TABLE room_amenities (
    hotelID INT,
    room_number INT,
    amenities VARCHAR(255),
    PRIMARY KEY (hotelID, room_number, amenities),
    FOREIGN KEY (hotelID, room_number) REFERENCES room (hotelID, room_number)
);

-- Room Problems
CREATE TABLE room_problems (
    hotelID INT,
    room_number INT,
    problem VARCHAR(255),
    PRIMARY KEY (hotelID, room_number, problem),
    FOREIGN KEY (hotelID, room_number) REFERENCES room (hotelID, room_number)
);


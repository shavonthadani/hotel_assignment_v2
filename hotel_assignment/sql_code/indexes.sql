-- Very common operation is to find rooms that belong to a hotel. 
-- Doing this will queries involving things like Select * FROM rooom where hotelID = x
CREATE INDEX idx_room_hotelID ON room (hotelID);

-- Common operation to get rooms that are booked between certain dates
-- Useful for employees to quickly find roooms that are under a certain status such as booked or rented
CREATE INDEX idx_booking_date_status ON booking_renting (date_booked, status);

-- Looking up all bookings that belong to a customer could be a very common operation as well
-- This will speed up selecting rows for bookings that belong to a specifc customer
CREATE INDEX idx_booking_customerID ON booking_renting (customerID);



-- Count number of rooms per hotel
SELECT hotelID, COUNT(*) AS total_rooms
FROM room
GROUP BY hotelID
HAVING COUNT(*) > 50; -- Change 50 to your threshold of interest

-- List all rooms booked between a certain time interval
SELECT r.hotelID, r.room_number
FROM room r
WHERE EXISTS (
    SELECT 1
    FROM booking_renting br
    WHERE br.hotelID = r.hotelID AND br.room_number = r.room_number
    AND (br.check_in_date BETWEEN '2024-03-01' AND '2024-08-31' OR 
         br.check_out_date BETWEEN '2024-03-01' AND '2024-08-31')
);

-- Average price of room for hotel
SELECT hotelID, AVG(price) AS average_price
FROM room
GROUP BY hotelID;

-- Identify customers that have booked x many times between certain dates
SELECT br.customerID, c.first_name, c.last_name, COUNT(br.bookingID) AS number_of_bookings
FROM booking_renting br
JOIN customer c ON br.customerID = c.customerID
WHERE br.date_booked BETWEEN '2024-01-01' AND '2025-12-31' -- Adjust the date range as needed
GROUP BY br.customerID, c.first_name, c.last_name
HAVING COUNT(br.bookingID) > 3 -- Customers with more than 3 bookings in the specified period
ORDER BY number_of_bookings DESC;
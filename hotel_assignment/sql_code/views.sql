-- View 1 to see available rooms per area (Assuming availability means no current booking)
CREATE VIEW available_rooms_per_area AS
SELECT h.city AS area, COUNT(*) AS available_rooms
FROM room r
JOIN hotel h ON r.hotelID = h.hotelID
LEFT JOIN booking_renting br ON r.hotelID = br.hotelID AND r.room_number = br.room_number
    AND (br.check_out_date < CURRENT_DATE OR br.check_in_date > CURRENT_DATE)
GROUP BY h.city;


-- Count capacity of each hotel
CREATE VIEW total_capacity_per_hotel AS
SELECT hotelID, SUM(capacity) AS total_capacity
FROM room
GROUP BY hotelID;

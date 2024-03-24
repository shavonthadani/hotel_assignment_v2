-- Check star rating is a number between 1 - 5
CREATE OR REPLACE FUNCTION check_star_rating()
RETURNS TRIGGER AS $$
BEGIN
    -- Check if star_rating is between 1 and 5
    IF NEW.star_rating < 1 OR NEW.star_rating > 5 THEN
        RAISE EXCEPTION 'Star rating must be between 1 and 5. Given value: %', NEW.star_rating;
    END IF;
    RETURN NEW; -- Return the row to be inserted or updated
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER validate_star_rating
BEFORE INSERT OR UPDATE ON hotel
FOR EACH ROW EXECUTE FUNCTION check_star_rating();



-- Checks if capacity value for a room is positive
CREATE OR REPLACE FUNCTION check_room_capacity()
RETURNS TRIGGER AS $$
BEGIN
    -- Check if capacity is positive
    IF NEW.capacity <= 0 THEN
        RAISE EXCEPTION 'Room capacity must be positive. Given value: %', NEW.capacity;
    END IF;
    RETURN NEW; -- Return the row to be inserted or updated
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER validate_room_capacity
BEFORE INSERT OR UPDATE ON room
FOR EACH ROW EXECUTE FUNCTION check_room_capacity();


-- Testing invalid values
INSERT INTO hotel (star_rating) VALUES (6);
INSERT INTO room (hotelID, room_number, capacity) VALUES (1, 102, 0);
INSERT INTO hotel_chain (name, street_number, street_name, apt_number, city, state, zip) VALUES
('Luxury Resorts', 100, 'Ocean View', 'Suite 20', 'Miami', 'FL', '33101'),
('Business Inn', 200, 'Market Street', 'Suite 10', 'New York', 'NY', '10001'),
('Budget Stays', 300, 'Main Street', '', 'Dallas', 'TX', '75001'),
('Travellers Joy', 400, 'Adventurers Road', '', 'San Francisco', 'CA', '94016'),
('Comfortable Retreat', 500, 'Tranquil Street', 'Apt 5A', 'Seattle', 'WA', '98101');

-- Inserting 8 hotels for hotel_chainID = 1
INSERT INTO hotel (hotel_chainID, star_rating, street_number, street_name, city, state, zip) VALUES
-- Two hotels in San Francisco
(1, 5, 100, 'Bay Street', 'San Francisco', 'CA', '94111'),
(1, 4, 200, 'Marina Blvd', 'San Francisco', 'CA', '94123'),

-- Other hotels in different cities
(1, 3, 300, 'Ocean Drive', 'Miami', 'FL', '33101'),
(1, 2, 400, 'Duval Street', 'Key West', 'FL', '33040'),
(1, 5, 500, 'Las Vegas Boulevard', 'Las Vegas', 'NV', '89109'),
(1, 4, 600, 'Fremont Street', 'Las Vegas', 'NV', '89101'),
(1, 3, 700, 'Broadway', 'New York', 'NY', '10006'),
(1, 2, 800, 'Fifth Avenue', 'New York', 'NY', '10118');

-- Inserting 8 hotels for hotel_chainID = 2
INSERT INTO hotel (hotel_chainID, star_rating, street_number, street_name, city, state, zip) VALUES
-- Two hotels in Miami
(2, 5, 150, 'Collins Avenue', 'Miami', 'FL', '33139'),
(2, 4, 250, 'Washington Avenue', 'Miami', 'FL', '33139'),

-- Other hotels in different cities
(2, 3, 100, 'Royal Palm Way', 'Palm Beach', 'FL', '33480'),
(2, 2, 200, 'Beachfront Avenue', 'Daytona Beach', 'FL', '32118'),
(2, 5, 50, 'The Strip', 'Las Vegas', 'NV', '89109'),
(2, 4, 150, 'Sunset Boulevard', 'Los Angeles', 'CA', '90046'),
(2, 3, 250, 'Magnificent Mile', 'Chicago', 'IL', '60611'),
(2, 2, 350, 'Union Square', 'San Francisco', 'CA', '94108');

-- Inserting 8 hotels for hotel_chainID = 3
INSERT INTO hotel (hotel_chainID, star_rating, street_number, street_name, city, state, zip) VALUES
-- Two hotels in Chicago
(3, 5, 900, 'Michigan Avenue', 'Chicago', 'IL', '60611'),
(3, 4, 950, 'Wacker Drive', 'Chicago', 'IL', '60601'),

-- Other hotels in different cities
(3, 3, 100, 'Peachtree Street', 'Atlanta', 'GA', '30303'),
(3, 2, 200, 'Ocean Drive', 'Savannah', 'GA', '31401'),
(3, 5, 300, 'Pennsylvania Avenue', 'Washington', 'DC', '20004'),
(3, 4, 400, 'Charles Street', 'Baltimore', 'MD', '21201'),
(3, 3, 500, 'Royal Street', 'New Orleans', 'LA', '70130'),
(3, 2, 600, 'Beale Street', 'Memphis', 'TN', '38103');

-- Inserting 8 hotels for hotel_chainID = 4
INSERT INTO hotel (hotel_chainID, star_rating, street_number, street_name, city, state, zip) VALUES
-- Two hotels in New York City
(4, 5, 100, 'Fifth Avenue', 'New York', 'NY', '10010'),
(4, 4, 150, 'Madison Avenue', 'New York', 'NY', '10016'),

-- Other hotels in different cities
(4, 3, 200, 'Boardwalk', 'Atlantic City', 'NJ', '08401'),
(4, 2, 250, 'Ocean Avenue', 'Jersey City', 'NJ', '07305'),
(4, 5, 300, 'Rodeo Drive', 'Beverly Hills', 'CA', '90210'),
(4, 4, 350, 'Sunset Strip', 'West Hollywood', 'CA', '90069'),
(4, 3, 400, 'Capitol Hill', 'Denver', 'CO', '80203'),
(4, 2, 450, 'Alameda Avenue', 'El Paso', 'TX', '79901');

-- Inserting 8 hotels for hotel_chainID = 5
INSERT INTO hotel (hotel_chainID, star_rating, street_number, street_name, city, state, zip) VALUES
-- Two hotels in Los Angeles
(5, 5, 200, 'Hollywood Boulevard', 'Los Angeles', 'CA', '90028'),
(5, 4, 250, 'Sunset Boulevard', 'Los Angeles', 'CA', '90026'),

-- Other hotels in different cities
(5, 3, 100, 'Market Street', 'San Francisco', 'CA', '94102'),
(5, 2, 150, 'Las Vegas Boulevard', 'Las Vegas', 'NV', '89109'),
(5, 5, 300, 'Michigan Avenue', 'Chicago', 'IL', '60601'),
(5, 4, 350, 'Ocean Drive', 'Miami', 'FL', '33139'),
(5, 3, 400, 'Canal Street', 'New Orleans', 'LA', '70130'),
(5, 2, 450, 'Sixth Avenue', 'Seattle', 'WA', '98101');



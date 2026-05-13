


-- Production & Performance
CREATE TABLE Production (
    production_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    start_date DATE,
    end_date DATE
);


CREATE TABLE Performance (
    performance_id SERIAL PRIMARY KEY,
    production_id INTEGER NOT NULL,
    start_time TIME,
    end_time TIME,
    date DATE,
    total_seats INTEGER,
    FOREIGN KEY (production_id) REFERENCES Production(production_id)
);

-- Seating
CREATE TABLE Seat (
    seat_id SERIAL PRIMARY KEY,
    seat_view VARCHAR(100),
    seat_number VARCHAR(20)
);

CREATE TABLE Performance_Seat (
    performance_seat_id SERIAL PRIMARY KEY,
    seat_id INTEGER NOT NULL,
    price DOUBLE PRECISION,
    is_available BOOLEAN,
	performance_id INTEGER NOT NULL,
    FOREIGN KEY (seat_id) REFERENCES Seat(seat_id),
    FOREIGN KEY (performance_id) REFERENCES Performance(performance_id)
);

-- Customers & Tickets
CREATE TABLE Customer (
    customer_id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255),
    mobile_number VARCHAR(50)
);

CREATE TABLE Ticket (
    performance_seat_id INTEGER NOT NULL,
    ticket_id SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    status VARCHAR(50),
    ticket_number VARCHAR(100),
    sale_date DATE,
    FOREIGN KEY (performance_seat_id) REFERENCES Performance_Seat(performance_seat_id),
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id)
);

-- Staff & Departments
CREATE TABLE Department (
    department_id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    manager_id INTEGER
);

CREATE TABLE Staff (
    staff_id SERIAL PRIMARY KEY,
    department_id INTEGER,
    name VARCHAR(255),
    type VARCHAR(50),
    FOREIGN KEY (department_id) REFERENCES Department(department_id)
);


CREATE TABLE Log_In (
    log_in_id SERIAL PRIMARY KEY,
    staff_id INTEGER,
    password VARCHAR(255),
    FOREIGN KEY (staff_id) REFERENCES Staff(staff_id)
);


-- Staff subtypes
CREATE TABLE Full_Time (
    staff_id INTEGER PRIMARY KEY,
    monthly_salary DOUBLE PRECISION,
    FOREIGN KEY (staff_id) REFERENCES Staff(staff_id)
);

CREATE TABLE Hourly (
    staff_id INTEGER PRIMARY KEY,
    hourly_rate DOUBLE PRECISION,
    famous_level INTEGER,
    FOREIGN KEY (staff_id) REFERENCES Staff(staff_id)
);

CREATE TABLE Commissioned (
    staff_id INTEGER PRIMARY KEY,
    commission_rate FLOAT,
    FOREIGN KEY (staff_id) REFERENCES Staff(staff_id)
);

-- Work logs & Transactions
CREATE TABLE Work_Log (
    staff_id INTEGER NOT NULL,
    performance_id INTEGER NOT NULL,
    hours_worked INTEGER,
    FOREIGN KEY (staff_id) REFERENCES Staff(staff_id),
    FOREIGN KEY (performance_id) REFERENCES Performance(performance_id)
);

CREATE TABLE Transactions (
    transaction_id SERIAL PRIMARY KEY,
    ticket_id INTEGER NOT NULL,
    staff_id INTEGER,
    transaction_date DATE,
    type VARCHAR(50),
    amount DOUBLE PRECISION,
    FOREIGN KEY (ticket_id) REFERENCES Ticket(ticket_id),
    FOREIGN KEY (staff_id)  REFERENCES Staff(staff_id)
);

-- 1. PRODUCTION (30 rows)
-- Some productions overlap (max 4 at a time)
INSERT INTO Production (title, start_date, end_date) VALUES
('The Notebook: The Musical',   '2024-01-10', '2024-03-15'),
('Les Misérables',              '2024-01-20', '2024-03-30'),
('Shrek',                       '2024-02-01', '2024-04-15'),
('A Christmas Carol',           '2024-02-10', '2024-04-20'),
('Ang Huling El Bimbo',         '2024-03-01', '2024-05-10'),
('Mamma Mia!',                  '2024-03-15', '2024-05-25'),
('Miss Saigon',                 '2024-04-01', '2024-06-10'),
('Rak of Aegis',                '2024-04-10', '2024-06-20'),
('Hamilton',                    '2024-05-01', '2024-07-15'),
('Wicked',                      '2024-05-10', '2024-07-25'),
('Into the Woods',              '2024-06-01', '2024-08-10'),
('Sweeney Todd',                '2024-06-15', '2024-08-20'),
('The Phantom of the Opera',    '2024-07-01', '2024-09-10'),
('Cats',                        '2024-07-10', '2024-09-20'),
('Chicago',                     '2024-08-01', '2024-10-10'),
('Rent',                        '2024-08-10', '2024-10-20'),
('Noli Me Tangere: The Musical','2024-09-01', '2024-11-10'),
('Himala: Isang Musikal',       '2024-09-10', '2024-11-20'),
('Next to Normal',              '2024-10-01', '2024-12-10'),
('Spring Awakening',            '2024-10-10', '2024-12-20'),
('Dear Evan Hansen',            '2024-11-01', '2025-01-10'),
('Come From Away',              '2024-11-10', '2025-01-20'),
('Six: The Musical',            '2024-12-01', '2025-02-10'),
('Hadestown',                   '2024-12-10', '2025-02-20'),
('Fun Home',                    '2025-01-01', '2025-03-10'),
('The Color Purple',            '2025-01-10', '2025-03-20'),
('Kinky Boots',                 '2025-02-01', '2025-04-10'),
('Jersey Boys',                 '2025-02-10', '2025-04-20'),
('Billy Elliot',                '2025-03-01', '2025-05-10'),
('Matilda: The Musical',        '2025-03-10', '2025-05-20');

-- 2. SEAT 
INSERT INTO Seat (seat_view, seat_number) VALUES
('/images/seats/A1_view.jpg', 'A1'),
('/images/seats/A2_view.jpg', 'A2'),
('/images/seats/A3_view.jpg', 'A3'),
('/images/seats/A4_view.jpg', 'A4'),
('/images/seats/A5_view.jpg', 'A5'),
('/images/seats/A6_view.jpg', 'A6'),
('/images/seats/B1_view.jpg', 'B1'),
('/images/seats/B2_view.jpg', 'B2'),
('/images/seats/B3_view.jpg', 'B3'),
('/images/seats/B4_view.jpg', 'B4'),
('/images/seats/B5_view.jpg', 'B5'),
('/images/seats/B6_view.jpg', 'B6'),
('/images/seats/C1_view.jpg', 'C1'),
('/images/seats/C2_view.jpg', 'C2'),
('/images/seats/C3_view.jpg', 'C3'),
('/images/seats/C4_view.jpg', 'C4'),
('/images/seats/C5_view.jpg', 'C5'),
('/images/seats/C6_view.jpg', 'C6'),
('/images/seats/D1_view.jpg', 'D1'),
('/images/seats/D2_view.jpg', 'D2'),
('/images/seats/D3_view.jpg', 'D3'),
('/images/seats/D4_view.jpg', 'D4'),
('/images/seats/D5_view.jpg', 'D5'),
('/images/seats/D6_view.jpg', 'D6'),
('/images/seats/E1_view.jpg', 'E1'),
('/images/seats/E2_view.jpg', 'E2'),
('/images/seats/E3_view.jpg', 'E3'),
('/images/seats/E4_view.jpg', 'E4'),
('/images/seats/E5_view.jpg', 'E5'),
('/images/seats/E6_view.jpg', 'E6');

-- 3. DEPARTMENT
INSERT INTO Department (name, manager_id) VALUES
('Entertainment', 1),
('Sales', 2),
('Production', 3);

-- 7. STAFF (30 rows)
-- Full_Time: staff_id 1-10
-- Hourly (Actors/Actresses): staff_id 11-22
-- Commissioned (Sales Agents): staff_id 23-30
INSERT INTO Staff (department_id, name, type) VALUES
(3, 'Miguel Reyes',          'Full_Time'),
(3, 'Patricia Delos Santos', 'Full_Time'),
(3, 'Ronald Villanueva',     'Full_Time'),
(3, 'Sonia Macaraeg',        'Full_Time'),
(3, 'Benedict Ocampo',       'Full_Time'),
(3, 'Lourdes Santiago',      'Full_Time'),
(3, 'Carlo Buenaventura',    'Full_Time'),
(3, 'Therese Paglinawan',    'Full_Time'),
(3, 'Francis Ilagan',        'Full_Time'),
(3, 'Luz Quiambao',          'Full_Time'),
(1, 'Gabriel Bautista',      'Hourly'),
(1, 'Luz Garcia',            'Hourly'),
(1, 'Alma Flores',           'Hourly'),
(1, 'Rain Ramos',            'Hourly'),
(1, 'Arlene Mendoza',        'Hourly'),
(1, 'Robert Santos',         'Hourly'),
(1, 'Joseph Dela Cruz',      'Hourly'),
(1, 'Alex Pascual',          'Hourly'),
(1, 'Patty Torres',          'Hourly'),
(1, 'Dio Cruz',              'Hourly'),
(1, 'Caridad Navarro',       'Hourly'),
(1, 'Marco Lim',             'Hourly'),
(2, 'Marius Aquino',         'Commissioned'),
(2, 'Mary Castillo',         'Commissioned'),
(2, 'Carmen Reyes',          'Commissioned'),
(2, 'Paulo Gonzales',        'Commissioned'),
(2, 'Felicity Hernandez',    'Commissioned'),
(2, 'Simon Morales',         'Commissioned'),
(2, 'Natividad Dizon',       'Commissioned'),
(2, 'Jamie Soriano',         'Commissioned');

-- staff_id references staff_id in staff table 
-- staff_id: 1-miguel reyes, 2- patricia, 3- ronald villanueva
-- 4. LOG_IN
INSERT INTO Log_In (staff_id, password) VALUES
(1,  'reyes.miguel.1@mmt'),
(2,  'delossantos.patricia.2@mmt'),
(3,  'villanueva.ronald.3@mmt'),

(23, 'aquino.marius.23@mmt'),
(24, 'castillo.mary.24@mmt'),
(25, 'reyes.carmen.25@mmt'),
(26, 'gonzales.paulo.26@mmt'),
(27, 'hernandez.felicity.27@mmt'),
(28, 'morales.simon.28@mmt'),
(29, 'dizon.natividad.29@mmt'),
(30, 'soriano.jamie.30@mmt');
 
-- 5. CUSTOMER 
INSERT INTO Customer (name, email, mobile_number) VALUES
('Diana Padilla',        'diana.padilla@gmail.com',        '09173829164'),
('Dennis Fuentes',       'den.fuentes12@yahoo.com',        '09561047382'),
('Sunshine Evangelista', 'sunshine_eva@gmail.com',         '09284716053'),
('Jerome Castaneda',     'jcastaneda@outlook.com',         '09390284756'),
('Precious Tolentino',   'precious.tol@gmail.com',         '09624831907'),
('Marvin Estrada',       'est.marvin@yahoo.com',           '09451728364'),
('Lovely De Jesus',      'lovely.dj21@gmail.com',          '09783920145'),
('Noel Beltran',         'noelbeltran88@outlook.com',      '09217364850'),
('Shiela Magbanua',      'shiela.magbanua@gmail.com',      '09948271036'),
('Noah Lim',             'noah.lim@gmail.com',             '09362048175'),
('Cassandra Alcantara',  'cassandra.alcantara@gmail.com',  '09475829163'),
('Shane Ancheta',        'sancheta@yahoo.com',             '09518273640'),
('Daine Manalo',         'daine.manalo@gmail.com',         '09631827459'),
('Jarren Dela Pierre',   'jarren.dela_pierre@outlook.com', '09724816350'),
('Therese Villaluiz',    'therese.villaluiz16@gmail.com',  '09867253041'),
('Carson Villafuerte',   'carson.vf@yahoo.com',            '09152748630'),
('Summer Macapagal',     'summer.macapagal01@gmail.com',   '09348162750'),
('Rosie Ganzon',         'ganzon.rosie@outlook.com',       '09293847561'),
('Anton Benitez',        'anton.benitez12@gmail.com',      '09586274130'),
('Jane Espinosa',        'jane.espinosa@yahoo.com',        '09417362850'),
('Nicole Andalucia',     'nicole.andalucia@gmail.com',     '09638271405'),
('Phoebe Gray',          'phoebe.gray@gmail.com',          '09271836450'),
('Daniel Torres',        'daniel.torres@gmail.com',        '09754821360'),
('Gabrielle Umali',      'gabrielle_umali09@yahoo.com',    '09183726450'),
('Sophia Marcos',        'sophia.marcos@gmail.com',        '09326481750'),
('Kyle Herrero',         'kyle.herrero@outlook.com',       '09847261305'),
('Robin Agustin',        'robin.agustin@gmail.com',        '09512836470'),
('Angela Villamor',      'villamor_angela29@gmail.com',    '09673812540'),
('Earl Sevilla',         'earl_sevilla23@gmail.com',       '09248163570'),
('Yve Robles',           'yve.robles@gmail.com',           '09431728605');

-- 6. PERFORMANCE 
INSERT INTO Performance (production_id, start_time, end_time, date, total_seats) VALUES
(1,  '19:00:00', '22:00:00', '2024-01-15', 30),
(1,  '14:00:00', '17:00:00', '2024-01-20', 30),
(2,  '19:00:00', '22:00:00', '2024-01-25', 30),
(2,  '14:00:00', '17:00:00', '2024-02-01', 30),
(3,  '20:00:00', '23:00:00', '2024-02-05', 30),
(3,  '15:00:00', '18:00:00', '2024-02-10', 30),
(4,  '19:00:00', '22:00:00', '2024-02-15', 30),
(4,  '14:00:00', '17:00:00', '2024-02-20', 30),
(5,  '20:00:00', '23:00:00', '2024-03-05', 30),
(5,  '15:00:00', '18:00:00', '2024-03-10', 30),
(6,  '19:00:00', '22:00:00', '2024-03-20', 30),
(6,  '14:00:00', '17:00:00', '2024-03-25', 30),
(7,  '20:00:00', '23:00:00', '2024-04-05', 30),
(7,  '15:00:00', '18:00:00', '2024-04-10', 30),
(8,  '19:00:00', '22:00:00', '2024-04-15', 30),
(8,  '14:00:00', '17:00:00', '2024-04-20', 30),
(9,  '20:00:00', '23:00:00', '2024-05-05', 30),
(9,  '15:00:00', '18:00:00', '2024-05-10', 30),
(10, '19:00:00', '22:00:00', '2024-05-15', 30),
(10, '14:00:00', '17:00:00', '2024-05-20', 30),
(11, '20:00:00', '23:00:00', '2024-06-05', 30),
(11, '15:00:00', '18:00:00', '2024-06-10', 30),
(12, '19:00:00', '22:00:00', '2024-06-20', 30),
(12, '14:00:00', '17:00:00', '2024-06-25', 30),
(13, '20:00:00', '23:00:00', '2024-07-05', 30),
(13, '15:00:00', '18:00:00', '2024-07-10', 30),
(14, '19:00:00', '22:00:00', '2024-07-15', 30),
(14, '14:00:00', '17:00:00', '2024-07-20', 30),
(15, '20:00:00', '23:00:00', '2024-08-05', 30),
(15, '15:00:00', '18:00:00', '2024-08-10', 30);


-- 8. PERFORMANCE_SEAT 
-- Prices vary by seat row: A=SVIP, B=VIP PREMIUM, C=VIP REGULAR, D=BOX PREMIUM, E=BOX REGULAR
INSERT INTO Performance_Seat (seat_id, price, is_available, performance_id) VALUES
(1,  5000.00, FALSE, 1),
(2,  5000.00, FALSE, 1),
(3,  5000.00, TRUE,  1),
(4,  5000.00, TRUE,  1),
(5,  5000.00, FALSE, 1),
(6,  5000.00, TRUE,  1),
(7,  3500.00, FALSE, 2),
(8,  3500.00, FALSE, 2),
(9,  3500.00, TRUE,  2),
(10, 3500.00, TRUE,  2),
(11, 3500.00, FALSE, 2),
(12, 3500.00, TRUE,  2),
(13, 2500.00, FALSE, 3),
(14, 2500.00, FALSE, 3),
(15, 2500.00, TRUE,  3),
(16, 2500.00, TRUE,  3),
(17, 2500.00, FALSE, 3),
(18, 2500.00, TRUE,  3),
(19, 1800.00, FALSE, 4),
(20, 1800.00, FALSE, 4),
(21, 1800.00, TRUE,  4),
(22, 1800.00, TRUE,  4),
(23, 1800.00, FALSE, 4),
(24, 1800.00, TRUE,  4),
(25, 1200.00, FALSE, 5),
(26, 1200.00, FALSE, 5),
(27, 1200.00, TRUE,  5),
(28, 1200.00, TRUE,  5),
(29, 1200.00, FALSE, 5),
(30, 1200.00, TRUE,  5);

-- 9. FULL_TIME
INSERT INTO Full_Time (staff_id, monthly_salary) VALUES
(1,  45000.00),
(2,  42000.00),
(3,  40000.00),
(4,  38000.00),
(5,  36000.00),
(6,  35000.00),
(7,  34000.00),
(8,  33000.00),
(9,  32000.00),
(10, 30000.00);

-- 10. HOURLY 
INSERT INTO Hourly (staff_id, hourly_rate, famous_level) VALUES
(11, 150.00, 1),
(12, 150.00, 1),
(13, 150.00, 1),
(14, 300.00, 2),
(15, 300.00, 2),
(16, 300.00, 2),
(17, 500.00, 3),
(18, 500.00, 3),
(19, 700.00, 4),
(20, 700.00, 4),
(21, 1000.00, 5),
(22, 1000.00, 5);

-- 11. COMMISSIONED
INSERT INTO Commissioned (staff_id, commission_rate) VALUES
(23, 0.25),
(24, 0.25),
(25, 0.25),
(26, 0.25),
(27, 0.25),
(28, 0.25),
(29, 0.25),
(30, 0.25);

-- 12. TICKET
INSERT INTO Ticket (performance_seat_id, customer_id, status, ticket_number, sale_date) VALUES
(1,  1,  'sold',     '1cal011519', '2024-01-10'),
(2,  2,  'sold',     '1cal011519', '2024-01-10'),
(3,  3,  'reserved', '1cal011519', '2024-01-11'),
(4,  4,  'sold',     '1cal011519', '2024-01-11'),
(5,  5,  'sold',     '1cal012014', '2024-01-15'),
(6,  6,  'refunded', '1cal012014', '2024-01-15'),
(7,  7,  'sold',     '2ble012519', '2024-01-20'),
(8,  8,  'sold',     '2ble012519', '2024-01-20'),
(9,  9,  'reserved', '2ble012519', '2024-01-21'),
(10, 10, 'sold',     '2ble012519', '2024-01-21'),
(11, 11, 'sold',     '2ble020114', '2024-01-26'),
(12, 12, 'refunded', '2ble020114', '2024-01-26'),
(13, 13, 'sold',     '3rek020520', '2024-02-01'),
(14, 14, 'sold',     '3rek020520', '2024-02-01'),
(15, 15, 'reserved', '3rek020520', '2024-02-02'),
(16, 16, 'sold',     '3rek021015', '2024-02-05'),
(17, 17, 'sold',     '3rek021015', '2024-02-05'),
(18, 18, 'sold',     '3rek021015', '2024-02-06'),
(19, 19, 'sold',     '4rol021519', '2024-02-10'),
(20, 20, 'sold',     '4rol021519', '2024-02-10'),
(21, 21, 'reserved', '4rol021519', '2024-02-11'),
(22, 22, 'sold',     '4rol022014', '2024-02-15'),
(23, 23, 'sold',     '4rol022014', '2024-02-15'),
(24, 24, 'refunded', '4rol022014', '2024-02-16'),
(25, 25, 'sold',     '5mbo030520', '2024-03-01'),
(26, 26, 'sold',     '5mbo030520', '2024-03-01'),
(27, 27, 'reserved', '5mbo030520', '2024-03-02'),
(28, 28, 'sold',     '5mbo031015', '2024-03-05'),
(29, 29, 'sold',     '5mbo031015', '2024-03-05'),
(30, 30, 'sold',     '5mbo031015', '2024-03-06');
 
-- 13. WORK_LOG
INSERT INTO Work_Log (staff_id, performance_id, hours_worked) VALUES
(1,  1,  8),
(2,  1,  6),
(3,  2,  7),
(4,  2,  5),
(5,  3,  8),
(6,  3,  6),
(7,  4,  7),
(8,  4,  5),
(9,  5,  8),
(10, 5,  6),
(11, 6,  5),
(12, 6,  6),
(13, 7,  7),
(14, 7,  5),
(15, 8,  6),
(16, 8,  8),
(17, 9,  5),
(18, 9,  7),
(19, 10, 6),
(20, 10, 8),
(21, 11, 5),
(22, 11, 6),
(1,  12, 7),
(2,  12, 5),
(3,  13, 8),
(4,  13, 6),
(5,  14, 7),
(6,  14, 5),
(7,  15, 8),
(8,  15, 6);

-- 14. TRANSACTIONS 
INSERT INTO Transactions (ticket_id, staff_id, transaction_date, type, amount) VALUES
(1,  23, '2024-01-10', 'purchased', 5000.00),
(2,  23, '2024-01-10', 'purchased', 5000.00),
(3,  24, '2024-01-11', 'reserved',  5000.00),
(4,  24, '2024-01-11', 'purchased', 5000.00),
(5,  25, '2024-01-15', 'purchased', 5000.00),
(6,  25, '2024-01-15', 'refunded',  -5000.00),
(7,  26, '2024-01-20', 'purchased', 3500.00),
(8,  26, '2024-01-20', 'purchased', 3500.00),
(9,  27, '2024-01-21', 'reserved',  3500.00),
(10, 27, '2024-01-21', 'purchased', 3500.00),
(11, 28, '2024-01-26', 'purchased', 3500.00),
(12, 28, '2024-01-26', 'refunded',  -3500.00),
(13, 29, '2024-02-01', 'purchased', 2500.00),
(14, 29, '2024-02-01', 'purchased', 2500.00),
(15, 30, '2024-02-02', 'reserved',  2500.00),
(16, 23, '2024-02-05', 'purchased', 2500.00),
(17, 23, '2024-02-05', 'purchased', 2500.00),
(18, 24, '2024-02-06', 'purchased', 2500.00),
(19, 24, '2024-02-10', 'purchased', 1800.00),
(20, 25, '2024-02-10', 'purchased', 1800.00),
(21, 25, '2024-02-11', 'reserved',  1800.00),
(22, 26, '2024-02-15', 'purchased', 1800.00),
(23, 26, '2024-02-15', 'purchased', 1800.00),
(24, 27, '2024-02-16', 'refunded',  -1800.00),
(25, 27, '2024-03-01', 'purchased', 1200.00),
(26, 28, '2024-03-01', 'purchased', 1200.00),
(27, 28, '2024-03-02', 'reserved',  1200.00),
(28, 29, '2024-03-05', 'purchased', 1200.00),
(29, 29, '2024-03-05', 'purchased', 1200.00),
(30, 30, '2024-03-06', 'purchased', 1200.00);

SELECT * FROM Production;
SELECT * FROM Seat;
SELECT * FROM Department;
SELECT * FROM Log_In;
SELECT * FROM Customer;
SELECT * FROM Performance;
SELECT * FROM Staff;
SELECT * FROM Performance_Seat;
SELECT * FROM Full_Time;
SELECT * FROM Hourly;
SELECT * FROM Commissioned;
SELECT * FROM Ticket;
SELECT * FROM Work_Log;
SELECT * FROM Transactions;
# --- TABLES CREATION ---

# Table Personal_Info
CREATE TABLE Personal_Info (
    personal_id INT PRIMARY KEY,
    name VARCHAR(255),
    surname VARCHAR(255),
    birth_year INT,
    mail VARCHAR(255) UNIQUE
);

# Table Regions
CREATE TABLE Regions (
    regional_id INT PRIMARY KEY,
    name VARCHAR(255),
    population INT,
    crime_rate FLOAT,
    unemployment_rate FLOAT,
    avg_income FLOAT,
    extreme_weather_events INT
);

# Table Policies
CREATE TABLE Policies (
    policy_id INT PRIMARY KEY,
    charges FLOAT,
    start_date DATE,
    end_date DATE,
    status VARCHAR(50) CHECK (status IN ('active', 'expired'))
);

# Table Clients
CREATE TABLE Clients (
    client_id INT PRIMARY KEY,
    age INT,
    sex VARCHAR(10) CHECK (sex IN ('female', 'male')),
    bmi FLOAT,
    children INT,
    smoker VARCHAR(10) CHECK (smoker IN ('yes', 'no')),
    id_region INT,
    id_policy INT,
    id_personal INT,
    FOREIGN KEY (id_region) REFERENCES Regions(regional_id),
    FOREIGN KEY (id_policy) REFERENCES Policies(policy_id),
    FOREIGN KEY (id_personal) REFERENCES Personal_Info(personal_id)
);
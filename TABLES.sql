CREATE TABLE SPECIES(
SP_ID VARCHAR(30) NOT NULL PRIMARY KEY,
SP_NAME VARCHAR(50) NOT NULL,
SP_CLASSIFICATION VARCHAR(50));


CREATE TABLE SPECIES_PRESERVES (
    PID VARCHAR(30) NOT NULL PRIMARY KEY,
    PNAME VARCHAR(50) NOT NULL,
    PLOC VARCHAR(30),
    PECOSYSTEM VARCHAR(50),
    SP_ID VARCHAR(30),
    FOREIGN KEY (SP_ID) REFERENCES SPECIES(SP_ID)
);

CREATE INDEX PECO_INDEX ON SPECIES_PRESERVES(PECOSYSTEM);


CREATE TABLE ENVIRONMENTAL_DATA (
    D_ID VARCHAR(30) PRIMARY KEY,
    WATER_QUAL VARCHAR(30),
    WEATHER_COND VARCHAR(30),
    SOIL_COMP VARCHAR(30),
    AIR_QUAL VARCHAR(30),
    PID VARCHAR(30),
    FOREIGN KEY (PID) REFERENCES SPECIES_PRESERVES(PID)
);



CREATE TABLE OBSERVATIONS (
    OB_ID VARCHAR(30) PRIMARY KEY,
    OB_DATE DATE,
    OB_LOC VARCHAR(30),
    SP_ID VARCHAR(30),
	D_ID VARCHAR(30),
    FOREIGN KEY (SP_ID) REFERENCES SPECIES(SP_ID),
FOREIGN KEY (D_ID) REFERENCES ENVIRONMENTAL_DATA(D_ID)
);

CREATE TABLE CONSERVATION_PLAN (
    PROJ_ID VARCHAR(30) PRIMARY KEY,
    PROJ_NAME VARCHAR(70),
    STR_DATE DATE,
    END_DATE DATE,
    SP_ID VARCHAR(30),
    FOREIGN KEY (SP_ID) REFERENCES SPECIES(SP_ID)
);

CREATE TABLE PROTECTED_BY (
    CONSERVATION_STATUS VARCHAR(30),
    SP_ID VARCHAR(30),
    PROJ_ID VARCHAR(30),
    PRIMARY KEY (SP_ID, PROJ_ID),
    FOREIGN KEY (SP_ID) REFERENCES SPECIES(SP_ID) ON DELETE CASCADE,
    FOREIGN KEY (PROJ_ID) REFERENCES CONSERVATION_PLAN(PROJ_ID) ON DELETE CASCADE
);

-----did not use ------
CREATE TABLE ECOSYSTEM (
    PID VARCHAR(30),
    PECOSYSTEM VARCHAR(30),
    PRIMARY KEY (PID, PECOSYSTEM),
    FOREIGN KEY (PID) REFERENCES SPECIES_PRESERVES(PID) ON DELETE CASCADE,
    FOREIGN KEY (PECOSYSTEM) REFERENCES SPECIES_PRESERVES(PECOSYSTEM) ON DELETE CASCADE
);


CREATE INDEX PECO_INDEX ON SPECIES_PRESERVES(PECOSYSTEM);
-------------------

CREATE TABLE MANAGEMENTUSERS(
ID INT,
USERNAME VARCHAR(30),
EMAIL VARCHAR(30),
PASSWORD VARCHAR(30),
DEPARTMENT VARCHAR(30));





INSERT INTO SPECIES (SP_ID, SP_NAME, SP_CLASSIFICATION) 
VALUES 
('SP001', 'Tiger', 'Mammal'),
('SP002', 'Elephant', 'Mammal'),
('SP003', 'Lion', 'Mammal'),
('SP004', 'Leopard', 'Mammal'),
('SP005', 'Giraffe', 'Mammal');


INSERT INTO SPECIES_PRESERVES (PID, PNAME, PLOC, PECOSYSTEM, SP_ID)
VALUES 
('P001', 'Bandipur Tiger Reserve', 'Karnataka', 'Tropical Forest', 'SP001'),
('P002', 'Ranthambore National Park', 'Rajasthan', 'Dry Deciduous Forest', 'SP002'),
('P003', 'Jim Corbett National Park', 'Uttarakhand', 'Savanna and Grasslands', 'SP003'),
('P004', 'Sundarbans National Park', 'West Bengal', 'Mangrove', 'SP004'),
('P005', 'Kaziranga National Park', 'Assam', 'Tropical Wet Evergreen Forest', 'SP005');


INSERT INTO ENVIRONMENTAL_DATA (D_ID, WATER_QUAL, WEATHER_COND, SOIL_COMP, AIR_QUAL, PID)
VALUES 
('D001', 'High', 'Sunny', 'Loamy', 'Good', 'P001'),
('D002', 'Moderate', 'Rainy', 'Sandy', 'Moderate', 'P002'),
('D003', 'Low', 'Snowy', 'Clay', 'Poor', 'P003'),
('D004', 'High', 'Cloudy', 'Silty', 'Excellent', 'P004'),
('D005', 'Moderate', 'Windy', 'Rocky', 'Fair', 'P005');


INSERT INTO OBSERVATIONS (OB_ID, OB_DATE, OB_LOC, SP_ID, D_ID)
VALUES 
('OB001', '2023-01-15', 'Sundarbans Reserve Forest', 'SP001', 'D001'),
('OB002', '2023-02-20', 'Maasai Mara National Reserve', 'SP002', 'D002'),
('OB003', '2023-03-25', 'Yellowstone National Park', 'SP003', 'D003'),
('OB004', '2023-04-30', 'Great Barrier Reef Marine Park', 'SP004', 'D004'),
('OB005', '2023-05-10', 'Amazon Rainforest', 'SP005', 'D005');


INSERT INTO CONSERVATION_PLAN (PROJ_ID, PROJ_NAME, STR_DATE, END_DATE, SP_ID)
VALUES 
('CP001', 'Tiger Conservation Project', '2023-01-01', '2025-01-01', 'SP001'),
('CP002', 'Elephant Protection Initiative', '2023-02-01', '2025-02-01', 'SP002'),
('CP003', 'Lion Habitat Restoration', '2022-03-01', '2023-03-01', 'SP003'),
('CP004', 'Leopard Population Monitoring', '2023-04-01', '2025-04-01', 'SP004'),
('CP005', 'Giraffe Conservation Program', '2024-05-01', '2026-05-01', 'SP005');


INSERT INTO PROTECTED_BY (CONSERVATION_STATUS, SP_ID, PROJ_ID)
VALUES 
('Ongoing', 'SP001', 'CP001'),
('Ongoing', 'SP002', 'CP002'),
('Completed', 'SP003', 'CP003'),
('Ongoing', 'SP004', 'CP004'),
('Yet to Start', 'SP005', 'CP005');






DELIMITER //

CREATE PROCEDURE UpdateProtectedByStatus()
BEGIN
    DECLARE today_date DATE;
    DECLARE proj_status VARCHAR(30);
    
    SET today_date = CURDATE();
    
    UPDATE PROTECTED_BY pb
    INNER JOIN CONSERVATION_PLAN cp ON pb.PROJ_ID = cp.PROJ_ID
    SET pb.CONSERVATION_STATUS = 'Yet to Start'
    WHERE today_date < cp.STR_DATE;
    
  
    UPDATE PROTECTED_BY pb
    INNER JOIN CONSERVATION_PLAN cp ON pb.PROJ_ID = cp.PROJ_ID
    SET pb.CONSERVATION_STATUS = 'Ongoing'
    WHERE today_date >= cp.STR_DATE AND today_date <= cp.END_DATE;
    
 
    UPDATE PROTECTED_BY pb
    INNER JOIN CONSERVATION_PLAN cp ON pb.PROJ_ID = cp.PROJ_ID
    SET pb.CONSERVATION_STATUS = 'Completed'
    WHERE today_date > cp.END_DATE;
END//

DELIMITER ;



DELIMITER //

CREATE TRIGGER UpdateConservationStatusTrigger
AFTER INSERT ON CONSERVATION_PLAN
FOR EACH ROW
BEGIN
    DECLARE today_date DATE;
    DECLARE proj_status VARCHAR(30);
    
    SET today_date = CURDATE();
    
    IF today_date < NEW.STR_DATE THEN
        SET proj_status = 'Yet to Start';
    ELSEIF today_date >= NEW.STR_DATE AND today_date <= NEW.END_DATE THEN
        SET proj_status = 'Ongoing';
    ELSE
        SET proj_status = 'Completed';
    END IF;
    
   
    INSERT INTO PROTECTED_BY (CONSERVATION_STATUS, SP_ID, PROJ_ID)
    VALUES (proj_status, NEW.SP_ID, NEW.PROJ_ID);
    
    CALL UpdateProtectedByStatus();
END//

DELIMITER ;
--



DELIMITER //

CREATE TRIGGER UpdateConservationStatusOnEndDateUpdate
AFTER UPDATE ON CONSERVATION_PLAN
FOR EACH ROW
BEGIN
    DECLARE new_end_date DATE;
    DECLARE proj_status VARCHAR(30);
    
    IF OLD.END_DATE <> NEW.END_DATE THEN
        SET new_end_date = NEW.END_DATE;
        
        IF CURDATE() < NEW.STR_DATE THEN
            SET proj_status = 'Yet to Start';
        ELSEIF CURDATE() >= NEW.STR_DATE AND CURDATE() <= new_end_date THEN
            SET proj_status = 'Ongoing';
        ELSE
            SET proj_status = 'Completed';
        END IF;
        
     
        UPDATE PROTECTED_BY
        SET CONSERVATION_STATUS = proj_status
        WHERE PROJ_ID = NEW.PROJ_ID;
    END IF;
END//

DELIMITER ;

--



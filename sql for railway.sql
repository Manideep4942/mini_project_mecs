show databases;
use drdl;

show databases;



create database railways_db;
use railways_db;

CREATE TABLE TrainAnnouncements (
    id INT AUTO_INCREMENT PRIMARY KEY,
    Train_No VARCHAR(20),
    Train_Name VARCHAR(100),
    From_City VARCHAR(100),
    To_City VARCHAR(100),
    Via_City VARCHAR(100),
    Platform_No SMALLINT(10)
);

INSERT INTO TrainAnnouncements (Train_No, Train_Name, From_City, To_City, Via_City, Platform_No)
VALUES
('1 2 3 4 5', 'vandhey bharat', 'secendrabad', 'vizag', 'bonagiri', '1'),
('6 7 8 9 0', 'Demo Train', 'City X', 'City Y', 'City Z', '2');

drop  table TrainAnnouncements;


Create database Health_and_Fitness_Tracking_System;

use Health_and_Fitness_Tracking_System;

CREATE TABLE Users (
    UserID INT PRIMARY KEY NOT NULL, 
    Name NVARCHAR(100) NOT NULL,          
    Age INT NOT NULL,                     
    Gender NVARCHAR(10) NOT NULL,         
    Height FLOAT NOT NULL,                
    Weight FLOAT NOT NULL,                
    Goal NVARCHAR(255)                    
);

CREATE TABLE Goal (
    GoalID INT IDENTITY(1,1) PRIMARY KEY, 
    UserID INT NOT NULL,                  
    GoalType NVARCHAR(255) NOT NULL,      
    TargetValue NVARCHAR(255),            
    StartDate DATE NOT NULL,              
    EndDate DATE,                         
    AchievedDate DATE,                    
    Constraint FK FOREIGN KEY (UserID) REFERENCES Users(UserID)
);

CREATE TABLE Workout (
    WorkoutID INT IDENTITY(1,1) PRIMARY KEY, 
    UserID INT NOT NULL,                     
    WorkoutType NVARCHAR(255) NOT NULL,      
    WorkoutDate DATE NOT NULL,               
    WorkoutDuration INT NOT NULL,            
    CaloriesBurned FLOAT NOT NULL,           
    Constraint FK1 FOREIGN KEY (UserID) REFERENCES Users(UserID)
);

CREATE TABLE Nutrition (
    NutritionID INT IDENTITY(1,1) PRIMARY KEY, 
    UserID INT NOT NULL,                       
    NutritionDate DATE NOT NULL,               
    FoodItem NVARCHAR(255) NOT NULL,           
    Calories FLOAT NOT NULL,                  
    Protein FLOAT NOT NULL,                    
    Fat FLOAT NOT NULL,                        
    Carbohydrates FLOAT NOT NULL,             
    Constraint FK2 FOREIGN KEY (UserID) REFERENCES Users(UserID)
);

CREATE TABLE UserDeletionLog (
    LogID INT PRIMARY KEY IDENTITY(1,1),           
    UserID INT NOT NULL,                            
    DataType VARCHAR(50) NOT NULL,                 
    DataDetails VARCHAR(MAX),                       
    DeletionTime DATETIME DEFAULT GETDATE(),       
    DeletedBy VARCHAR(50) NOT NULL,                 
    
);

select * from Users
select * from Goal
select * from Workout
select * from Nutrition
select * from UserDeletionLog

delete from Users
delete from Goal  
delete from Workout
delete from Nutrition
delete from UserDeletionLog where LogID between 1 and 4

drop table Users

alter table Goal drop Constraint FK
alter table Workout drop Constraint FK1
alter table Nutrition drop Constraint FK2

alter table Goal add constraint FK Foreign Key(UserID) REFERENCES Users(UserID)
alter table Workout add constraint FK1 Foreign Key(UserID) REFERENCES Users(UserID)
alter table Nutrition add constraint FK2 Foreign Key(UserID) REFERENCES Users(UserID)
alter table UserDeletionLog add constraint FK3 Foreign Key(UserID) REFERENCES Users(UserID)

update Goal set GoalType = 'Weight Increase' where GoalType = 'Height Increase' and UserID = 1
update Users set Name = 'Maaz Javed' where UserID = 5
alter table UserDeletionLog drop constraint FK3 
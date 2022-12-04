# These are the queries you need to execute to your local DB

"""
CREATE TABLE `car_model_schema`.`car_model` (
  `objectId` VARCHAR(10) NOT NULL,
  `Year` INT NULL,
  `Make` VARCHAR(50) NULL,
  `Model` VARCHAR(500) NULL,
  `Category` VARCHAR(500) NULL,
  PRIMARY KEY (`objectId`));

ALTER TABLE `car_model_schema`.`car_model` 
ADD COLUMN `createdAt` VARCHAR(100) NULL AFTER `Category`,
ADD COLUMN `updatedAt` VARCHAR(100) NULL AFTER `createdAt`;

"""



    
    
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema reservation
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema reservation
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `reservation` DEFAULT CHARACTER SET utf8 ;
USE `reservation` ;

-- -----------------------------------------------------
-- Table `reservation`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `reservation`.`users` (
  `user_id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`user_id`))
ENGINE = InnoDB;

CREATE UNIQUE INDEX `user_id_UNIQUE` ON `reservation`.`users` (`user_id` ASC) VISIBLE;


-- -----------------------------------------------------
-- Table `reservation`.`panel`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `reservation`.`panel` (
  `panel_id` INT NOT NULL AUTO_INCREMENT,
  `rStatus` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`panel_id`))
ENGINE = InnoDB;

CREATE UNIQUE INDEX `user_id_UNIQUE` ON `reservation`.`panel` (`panel_id` ASC) VISIBLE;


-- -----------------------------------------------------
-- Table `reservation`.`reservation`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `reservation`.`reservation` (
  `users_user_id` INT NOT NULL,
  `panel_panel_id` INT NOT NULL,
  `rStatus` VARCHAR(45) NOT NULL,
  `rTime` VARCHAR(45) NOT NULL,
  `user_name` VARCHAR(45) NULL,
  PRIMARY KEY (`users_user_id`, `panel_panel_id`),
  CONSTRAINT `fk_users_has_panel_users`
    FOREIGN KEY (`users_user_id`)
    REFERENCES `reservation`.`users` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_users_has_panel_panel1`
    FOREIGN KEY (`panel_panel_id`)
    REFERENCES `reservation`.`panel` (`panel_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

CREATE INDEX `fk_users_has_panel_panel1_idx` ON `reservation`.`reservation` (`panel_panel_id` ASC) VISIBLE;

CREATE INDEX `fk_users_has_panel_users_idx` ON `reservation`.`reservation` (`users_user_id` ASC) VISIBLE;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
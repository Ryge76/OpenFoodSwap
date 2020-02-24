-- MySQL Script generated by MySQL Workbench
-- Tue Feb 11 11:03:48 2020
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema OFSdb
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `OFSdb` ;

-- -----------------------------------------------------
-- Schema OFSdb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `OFSdb` DEFAULT CHARACTER SET utf8 ;
USE `OFSdb` ;

-- -----------------------------------------------------
-- Table `OFSdb`.`Categories`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OFSdb`.`Categories` ;

CREATE TABLE IF NOT EXISTS `OFSdb`.`Categories` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `categ_name` VARCHAR(30) NOT NULL COMMENT 'Fruits, Legumes, Viandes, Poissons, Cereales, Plaitiers, Boissons, Pdej, Snacks',
  PRIMARY KEY (`id`))
ENGINE = InnoDB;

CREATE UNIQUE INDEX `id_UNIQUE` ON `OFSdb`.`Categories` (`id` ASC) VISIBLE;

CREATE UNIQUE INDEX `categ_name_UNIQUE` ON `OFSdb`.`Categories` (`categ_name` ASC) VISIBLE;


-- -----------------------------------------------------
-- Table `OFSdb`.`Products`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OFSdb`.`Products` ;

CREATE TABLE IF NOT EXISTS `OFSdb`.`Products` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `category_id` INT UNSIGNED NOT NULL,
  `product_name` MEDIUMTEXT NOT NULL,
  `url` MEDIUMTEXT NOT NULL,
  `image_url` MEDIUMTEXT NULL,
  `nutrition_grade_fr` CHAR(1) NOT NULL,
  `ingredients_text` LONGTEXT NOT NULL,
  `allergens` MEDIUMTEXT NULL,
  `stores` MEDIUMTEXT NOT NULL,
  `purchase_places` MEDIUMTEXT NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `fk_categ_id`
    FOREIGN KEY (`category_id`)
    REFERENCES `OFSdb`.`Categories` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

CREATE UNIQUE INDEX `id_UNIQUE` ON `OFSdb`.`Products` (`id` ASC) INVISIBLE;

CREATE FULLTEXT INDEX `idx_char_product` ON `OFSdb`.`Products` (`product_name`(10)) INVISIBLE;

CREATE INDEX `idx_char_score` ON `OFSdb`.`Products` (`nutrition_grade_fr` ASC) INVISIBLE;

CREATE FULLTEXT INDEX `idx_char_store` ON `OFSdb`.`Products` (`purchase_places`(10)) VISIBLE;

CREATE UNIQUE INDEX `product_name_UNIQUE` ON `OFSdb`.`Products` (`product_name`(20) ASC) VISIBLE;

CREATE INDEX `fk_categ_id_idx` ON `OFSdb`.`Products` (`category_id` ASC) VISIBLE;


-- -----------------------------------------------------
-- Table `OFSdb`.`Substitutes`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OFSdb`.`Substitutes` ;

CREATE TABLE IF NOT EXISTS `OFSdb`.`Substitutes` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `initial_product` INT UNSIGNED NOT NULL,
  `substitute` INT UNSIGNED NOT NULL,
  `subs_date` DATETIME NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `fk_initial_id0`
    FOREIGN KEY (`initial_product`)
    REFERENCES `OFSdb`.`Products` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_substitute_id0`
    FOREIGN KEY (`substitute`)
    REFERENCES `OFSdb`.`Products` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

CREATE UNIQUE INDEX `idsubstitutions_UNIQUE` ON `OFSdb`.`Substitutes` (`id` ASC) INVISIBLE;

CREATE INDEX `fk_initial_id_idx` ON `OFSdb`.`Substitutes` (`initial_product` ASC) VISIBLE;

CREATE INDEX `fk_substitute_id_idx` ON `OFSdb`.`Substitutes` (`substitute` ASC) VISIBLE;

CREATE INDEX `idx_date` ON `OFSdb`.`Substitutes` (`subs_date` ASC) VISIBLE;

CREATE UNIQUE INDEX `idx_ini_sub_UNIQUE` ON `OFSdb`.`Substitutes` (`initial_product` ASC, `substitute` ASC) VISIBLE;

SET SQL_MODE = '';
DROP USER IF EXISTS appuser;
SET SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';
CREATE USER 'appuser' IDENTIFIED BY 'test';

GRANT SELECT, INSERT, TRIGGER, UPDATE, DELETE ON TABLE `OFSdb`.* TO 'appuser';
SET SQL_MODE = '';
DROP USER IF EXISTS appadm;
SET SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';
CREATE USER 'appadm' IDENTIFIED BY 'testrole';

GRANT ALL ON `OFSdb`.* TO 'appadm';

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

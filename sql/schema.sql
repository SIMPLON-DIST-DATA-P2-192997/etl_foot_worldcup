-- ============================================================
-- RESET DES TABLES (ordre inverse des dépendances)
-- ============================================================

DROP TABLE IF EXISTS `match`;
DROP TABLE IF EXISTS stadium;
DROP TABLE IF EXISTS team;
DROP TABLE IF EXISTS edition;
DROP TABLE IF EXISTS city;

-- ============================================================
-- TABLE CITY
-- ============================================================

CREATE TABLE city (
    id_city      INT PRIMARY KEY AUTO_INCREMENT,
    city_name    VARCHAR(255) NOT NULL
);

-- Index utile pour les KPI
CREATE INDEX idx_city_name ON city(city_name);

-- ============================================================
-- TABLE STADIUM
-- ============================================================

CREATE TABLE stadium (
    id_stadium   INT PRIMARY KEY AUTO_INCREMENT,
    id_city      INT NULL,  -- corrigé : NULLABLE
    stadium_name VARCHAR(255) NOT NULL,

    CONSTRAINT fk_stadium_city
        FOREIGN KEY (id_city)
        REFERENCES city(id_city)
        ON UPDATE CASCADE
        ON DELETE SET NULL
);

CREATE INDEX idx_stadium_name ON stadium(stadium_name);

-- ============================================================
-- TABLE TEAM
-- ============================================================

CREATE TABLE team (
    id_team    INT PRIMARY KEY AUTO_INCREMENT,
    team_name  VARCHAR(255) NOT NULL
);

CREATE INDEX idx_team_name ON team(team_name);

-- ============================================================
-- TABLE EDITION
-- ============================================================

CREATE TABLE edition (
    id_edition    INT PRIMARY KEY AUTO_INCREMENT,
    edition_name  VARCHAR(255) NOT NULL
    -- colonne year supprimée
);

CREATE INDEX idx_edition_name ON edition(edition_name);

-- ============================================================
-- TABLE MATCH  (nom réservé → backticks obligatoires)
-- ============================================================

CREATE TABLE `match` (
    id_match      INT PRIMARY KEY AUTO_INCREMENT,

    id_home_team  INT NOT NULL,
    id_away_team  INT NOT NULL,
    id_stadium    INT NOT NULL,
    id_edition    INT NOT NULL,

    date          DATETIME NULL,
    round         VARCHAR(255) NOT NULL,
    home_result   INT NOT NULL,
    away_result   INT NOT NULL,
    result        VARCHAR(255) NOT NULL,

    CONSTRAINT fk_match_home_team
        FOREIGN KEY (id_home_team)
        REFERENCES team(id_team)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT fk_match_away_team
        FOREIGN KEY (id_away_team)
        REFERENCES team(id_team)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT fk_match_stadium
        FOREIGN KEY (id_stadium)
        REFERENCES stadium(id_stadium)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT fk_match_edition
        FOREIGN KEY (id_edition)
        REFERENCES edition(id_edition)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

-- ============================================================
-- INDEX
-- ============================================================

CREATE INDEX idx_match_home_team ON `match`(id_home_team);
CREATE INDEX idx_match_away_team ON `match`(id_away_team);
CREATE INDEX idx_match_stadium ON `match`(id_stadium);
CREATE INDEX idx_match_edition ON `match`(id_edition);
CREATE INDEX idx_match_date ON `match`(date);

-- ============================================================
-- VUE FINALE (conforme au brief)
-- ============================================================

CREATE OR REPLACE VIEW match_final AS
SELECT 
    m.id_match,
    t1.team_name AS home_team,
    t2.team_name AS away_team,
    m.home_result,
    m.away_result,
    m.result,
    m.date,
    m.round,
    c.city_name AS city,
    e.edition_name AS edition
FROM `match` m
JOIN team t1 ON m.id_home_team = t1.id_team
JOIN team t2 ON m.id_away_team = t2.id_team
JOIN edition e ON m.id_edition = e.id_edition
LEFT JOIN stadium s ON m.id_stadium = s.id_stadium
LEFT JOIN city c ON s.id_city = c.id_city;


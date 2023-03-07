CREATE TABLE telemetry (
  id INT UNSIGNED NOT NULL AUTO_INCREMENT,
  data JSON NOT NULL,
  created TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  PRIMARY KEY (id)
) CHARACTER SET = latin1 COLLATE latin1_general_cs;

ALTER TABLE telemetry
ADD INDEX device ((
    CAST(data->>"$.device_id" AS CHAR(100)) COLLATE latin1_general_cs
  )) USING BTREE;

ALTER TABLE telemetry ADD COLUMN device_id VARCHAR(100)
  GENERATED ALWAYS as (data->>"$.device_id");

SHOW CREATE TABLE telemetry\G

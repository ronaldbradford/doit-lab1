DROP USER IF EXISTS api@'%';
CREATE USER api@'%' IDENTIFIED BY 'Doit#Lab1@2023';
GRANT INSERT on lab1.telemetry TO api@'%';

-- Keep a log of any SQL queries you execute as you solve the mystery.

SELECT * FROM crime_scene_reports WHERE day=28 AND month=7 AND year=2023 AND street='Humphrey Street'; -- GOT WITNESS

-- WITNESS
SELECT * FROM interviews WHERE transcript LIKE 'bakery'; -- GOT WITNESSES

-- RUTH: SAW THIEF WITHIN TEN-MIN AT PARKING LOT
-- EUGENE: SAW THIEF BEFORE COMING TO BAKERY AT ATM ON LEGGETT STREET (GET THE TIME EUGENE ARRIVED AT BAKERY AND SEARCH ATM FOOTAGE)
-- RAYMOND: (FLIGHT TICKET NEXT-DAY, PHONE-CALL)

-- ANALYSING RUTH
SELECT * FROM bakery_security_logs WHERE day=28 AND month=7 AND year=2023 AND hour=10 AND minute BETWEEN 15 AND 25; -- GOT SOME "LICENSE_PLATES"

-- SELECT NAME, PHONE-NUMBER, PASSPORT_NUMBER FROM PEOPLE WHERE LICENSE_PLATE MATCHES TO BAKERY_LOG
SELECT name, phone_number, passport_number, license_plate FROM people WHERE license_plate IN (SELECT license_plate FROM bakery_security_logs WHERE day=28 AND month=7 AND year=2023 AND hour=10 AND minute BETWEEN 15 AND 25); -- GOT LIST OF 7 PEOPLE WITH THEIR PHONE-NUMBERS AND PASSPORT.

-- ANALYSING EUGENE(SAW AT ATM)
SELECT * FROM atm_transactions WHERE day=27 AND month=7 AND year=2023 AND atm_location='Leggett Street'; -- GOT SOME ACCOUNT NUMBERS

-- GET NAMES, WHO WITHDRAWED MONEY
SELECT name FROM people WHERE id IN (SELECT person_id FROM bank_accounts WHERE account_number IN (SELECT account_number FROM atm_transactions WHERE day=28 AND month=7 AND year=2023 AND atm_location='Leggett Street'));

-- FIND COMMON NAMES TILL NOW
SELECT name FROM people WHERE id IN (SELECT person_id FROM bank_accounts WHERE account_number IN (SELECT account_number FROM atm_transactions WHERE day=28 AND month=7 AND year=2023 AND atm_location='Leggett Street')) INTERSECT SELECT name FROM people WHERE license_plate IN (SELECT license_plate FROM bakery_security_logs WHERE day=28 AND month=7 AND year=2023 AND hour=10 AND minute BETWEEN 15 AND 25);-- BRUCE, DIANA, IMAN, LUCA

-- ANALYSING RAYMOND(PHONE CALL)
SELECT * FROM phone_calls WHERE duration<60 AND day=28 AND month=7 AND year=2023;

-- ADDING NAMES TO CALLERS
SELECT name FROM people WHERE phone_number IN (SELECT caller FROM phone_calls WHERE duration<60 AND day=28 AND month=7 AND year=2023);

-- GET COMMON NAMES FROM ALL 3 WITNESSES
SELECT name FROM people WHERE id IN (SELECT person_id FROM bank_accounts WHERE account_number IN
(SELECT account_number FROM atm_transactions WHERE day=28 AND month=7 AND year=2023 AND atm_location='Leggett Street')) INTERSECT
SELECT name FROM people WHERE license_plate IN (SELECT license_plate FROM bakery_security_logs WHERE day=28 AND month=7 AND year=2023 AND hour=10 AND minute BETWEEN 15 AND 25)
INTERSECT SELECT name FROM people WHERE phone_number IN (SELECT caller FROM phone_calls WHERE duration<60 AND day=28 AND month=7 AND year=2023); -- BRUCE AND DIANA

-- GET ID NUMBER OF AIRPORT FIFTYVILLE
SELECT * FROM airports; -- ID IS 8

-- GET THE FIRST FLIGHT ON 29/7/2023 WHERE FLIGHT ORIGIN_ID = 8
SELECT * FROM flights WHERE day=29 AND month=7 AND year=2023 AND origin_airport_is = 8; -- CONSIDERED FIRST-FLIGHT(AT 8:20), FLIGHT_ID=36 AND ALSO FOUND THEY ARE GOING TO "NEW YORK"

-- CHECK PASSENGERS IN FLIGHT WHERE ID = 36
SELECT name FROM people WHERE passport_number IN (SELECT passport_number FROM passengers WHERE flight_id=36);

-- FIND COMMON NAME FROM ALL NAMES WE HAVE
SELECT name FROM people WHERE id IN (SELECT person_id FROM bank_accounts WHERE account_number IN
(SELECT account_number FROM atm_transactions WHERE day=28 AND month=7 AND year=2023 AND atm_location='Leggett Street')) INTERSECT
SELECT name FROM people WHERE license_plate IN (SELECT license_plate FROM bakery_security_logs WHERE day=28 AND month=7 AND year=2023 AND hour=10 AND minute BETWEEN 15 AND 25)
INTERSECT SELECT name FROM people WHERE phone_number IN (SELECT caller FROM phone_calls WHERE duration<60 AND day=28 AND month=7 AND year=2023); INTERSECT
SELECT name FROM people WHERE passport_number IN (SELECT passport_number FROM passengers WHERE flight_id=36); -- FOUND "BRUCE" IS THE THEIF

-- GET THE NAME OF PERSON WITH WHOME BRUE HAD A CALL
SELECT name FROM people WHERE phone_number IN (SELECT receiver FROM phone_calls WHERE caller IN (SELECT phone_number FROM people WHERE name='Bruce' AND day=28 AND month=7 AND year=2023 AND duration<60)); -- BRUCE HAD A CALL WITH 'ROBIN'.

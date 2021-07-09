-- CREATE USER postgres WITH SUPERUSER PASSWORD 'postgres';
-- ALTER DATABASE postgres OWNER TO postgres;

CREATE TABLE client_wallet (
    id serial primary key,
    balance float default 0
);

CREATE TABLE transaction_history (
    id serial primary key,
    ts timestamp with time zone default current_timestamp,
    receiver_id integer REFERENCES client_wallet (id),
    sender_id integer REFERENCES client_wallet (id),
    amount float
);

CREATE TABLE refill_history (
    id serial primary key,
    ts timestamp with time zone default current_timestamp,
    client_id integer REFERENCES client_wallet (id),
    amount float
);

-- DROP TABLE client_wallet CASCADE;
-- DROP TABLE transaction_history;
-- DROP TABLE refill_history;

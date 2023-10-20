CREATE TABLE IF NOT EXISTS manzi_mfa.user_events
(
    event_id SERIAL PRIMARY KEY,
    action varchar(255),
    created_at timestamp,
    customer_email varchar(255), -- Add the customer_email column
    customer_name varchar(255),  -- Add the customer_name column
    service_name varchar(255),   -- Add the service_name column
    provider_name varchar(255),  -- Add the provider_name column
    provider_email varchar(255), -- Add the provider_email column
    start_date timestamp,        -- Add the start_date column,
    end_date timestamp,
    event json
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS manzi_mfa.user_events
    OWNER to postgres;
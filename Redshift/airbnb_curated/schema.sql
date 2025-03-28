CREATE TABLE fact_bookings (
    booking_id BIGINT ENCODE az64,
    user_id BIGINT ENCODE az64,
    apartment_id BIGINT ENCODE az64,
    booking_date VARCHAR(65535) ENCODE lzo,
    checkin_date DATE ENCODE az64,
    checkout_date DATE ENCODE az64,
    booking_duration INTEGER ENCODE az64,
    total_price DOUBLE PRECISION ENCODE none,
    currency VARCHAR(65535) ENCODE lzo
);

CREATE TABLE dim_apartments (
    id BIGINT ENCODE az64,
    title VARCHAR(65535) ENCODE lzo,
    source VARCHAR(65535) ENCODE lzo,
    price DOUBLE PRECISION ENCODE none,
    currency VARCHAR(65535) ENCODE lzo,
    listing_created_on DATE ENCODE az64,
    is_active BOOLEAN ENCODE none,
    last_modified_timestamp VARCHAR(65535) ENCODE lzo
);


CREATE TABLE dim_users (
    user_id BIGINT ENCODE az64,
    apartment_id BIGINT ENCODE az64,
    viewed_at VARCHAR(65535) ENCODE lzo,
    is_wishlisted BOOLEAN ENCODE none,
    call_to_action VARCHAR(65535) ENCODE lzo
);



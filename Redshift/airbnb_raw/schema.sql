CREATE TABLE raw_apartment_attr (
    id BIGINT ENCODE az64,
    category VARCHAR(65535) ENCODE lzo,
    body VARCHAR(65535) ENCODE lzo,
    amenities VARCHAR(65535) ENCODE lzo,
    bathrooms BIGINT ENCODE az64,
    bedrooms BIGINT ENCODE az64,
    fee DOUBLE PRECISION ENCODE none,
    has_photo BOOLEAN ENCODE none
);

CREATE TABLE raw_apartments (
    id BIGINT ENCODE az64,
    title VARCHAR(65535) ENCODE lzo,
    source VARCHAR(65535) ENCODE lzo,
    price DOUBLE PRECISION ENCODE none,
    currency VARCHAR(65535) ENCODE lzo,
    listing_created_on VARCHAR(65535) ENCODE lzo,
    is_active BOOLEAN ENCODE none,
    last_modified_timestamp VARCHAR(65535) ENCODE lzo
);

CREATE TABLE raw_bookings (
    booking_id BIGINT ENCODE az64,
    user_id BIGINT ENCODE az64,
    apartment_id BIGINT ENCODE az64,
    booking_date VARCHAR(65535) ENCODE lzo,
    checkin_date VARCHAR(65535) ENCODE lzo,
    checkout_date VARCHAR(65535) ENCODE lzo,
    total_price DOUBLE PRECISION ENCODE none,
    currency VARCHAR(65535) ENCODE lzo,
    booking_status VARCHAR(65535) ENCODE lzo
);


CREATE TABLE raw_user_viewing (
    user_id BIGINT ENCODE az64,
    apartment_id BIGINT ENCODE az64,
    viewed_at VARCHAR(65535) ENCODE lzo,
    is_wishlisted BOOLEAN ENCODE none,
    call_to_action VARCHAR(65535) ENCODE lzo
);

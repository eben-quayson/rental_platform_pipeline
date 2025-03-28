CREATE TABLE user_viewing (
    user_id BIGINT NOT NULL,
    apartment_id BIGINT NOT NULL,
    viewed_at TIMESTAMP NOT NULL,
    is_wishlisted BOOLEAN DEFAULT FALSE,
    call_to_action VARCHAR(255),
    PRIMARY KEY (user_id, apartment_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (apartment_id) REFERENCES apartment(apartment_id) ON DELETE CASCADE
);

CREATE TABLE apartment (
    apartment_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    source VARCHAR(255),
    price DECIMAL(10,2) NOT NULL,
    currency VARCHAR(10),
    listing_created_on DATE NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE apartment_attributes (
    apartment_id BIGINT NOT NULL,
    attribute_key VARCHAR(255) NOT NULL,
    attribute_value VARCHAR(255) NOT NULL,
    PRIMARY KEY (apartment_id, attribute_key),
    FOREIGN KEY (apartment_id) REFERENCES apartment(apartment_id) ON DELETE CASCADE
);

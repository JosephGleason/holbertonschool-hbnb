-- Admin User Insert
INSERT INTO users (
    id, first_name, last_name, email, password, is_admin
) VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2b$12$W35l/5e8MZ8jX25IMHcHVeOt/anGD01ZjfqtnRki92r/x8iFiklM6',
    TRUE
);

-- Initial Amenities Inserts
INSERT INTO amenities (id, name) VALUES
    ('0e34f0c6-6ef1-4b37-8947-94622137d9ef', 'WiFi'),
    ('8c0e2d87-75d7-4605-a82f-c71f65f4e213', 'Swimming Pool'),
    ('63bfa6e1-1d92-404b-a00d-4f5a72ac5a42', 'Air Conditioning');

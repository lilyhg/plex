ALTER TABLE users
ADD COLUMN subscription_status VARCHAR(255),
ADD COLUMN subscription_id VARCHAR(255) UNIQUE;
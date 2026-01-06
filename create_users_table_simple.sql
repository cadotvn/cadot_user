-- Create users table for Cadot User Management API
-- Based on the User model in app/models/user.py
-- Simple version without schema specification

-- Create the users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    username VARCHAR(255) NOT NULL UNIQUE,
    full_name VARCHAR(255),
    phone_number VARCHAR(20),
    avatar_url TEXT,
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    is_superuser BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_users_is_active ON users(is_active);
CREATE INDEX IF NOT EXISTS idx_users_created_at ON users(created_at);

-- Create a trigger to automatically update the updated_at column
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_users_updated_at 
    BEFORE UPDATE ON users 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- Insert 10 sample users
-- Note: All passwords are hashed using bcrypt. Default password is "password123" unless specified otherwise.
INSERT INTO users (email, username, full_name, phone_number, avatar_url, hashed_password, is_active, is_superuser) VALUES
('admin@example.com', 'admin', 'Administrator User', '+1-555-0100', 'https://i.pravatar.cc/150?img=1', '$2b$12$c6FmldQa4Jg0hR3p/nNL7OiMOKoeJ/FJKxn5dVHTybU2ETcxpxrdS', TRUE, TRUE),
('john.doe@example.com', 'johndoe', 'John Doe', '+1-555-0101', 'https://i.pravatar.cc/150?img=2', '$2b$12$c6FmldQa4Jg0hR3p/nNL7OiMOKoeJ/FJKxn5dVHTybU2ETcxpxrdS', TRUE, FALSE),
('jane.smith@example.com', 'janesmith', 'Jane Smith', '+1-555-0102', 'https://i.pravatar.cc/150?img=3', '$2b$12$c6FmldQa4Jg0hR3p/nNL7OiMOKoeJ/FJKxn5dVHTybU2ETcxpxrdS', TRUE, FALSE),
('bob.wilson@example.com', 'bobwilson', 'Bob Wilson', '+1-555-0103', 'https://i.pravatar.cc/150?img=4', '$2b$12$c6FmldQa4Jg0hR3p/nNL7OiMOKoeJ/FJKxn5dVHTybU2ETcxpxrdS', TRUE, FALSE),
('alice.brown@example.com', 'alicebrown', 'Alice Brown', '+1-555-0104', 'https://i.pravatar.cc/150?img=5', '$2b$12$c6FmldQa4Jg0hR3p/nNL7OiMOKoeJ/FJKxn5dVHTybU2ETcxpxrdS', TRUE, FALSE),
('charlie.davis@example.com', 'charliedavis', 'Charlie Davis', '+1-555-0105', 'https://i.pravatar.cc/150?img=6', '$2b$12$c6FmldQa4Jg0hR3p/nNL7OiMOKoeJ/FJKxn5dVHTybU2ETcxpxrdS', FALSE, FALSE),
('diana.miller@example.com', 'dianamiller', 'Diana Miller', '+1-555-0106', 'https://i.pravatar.cc/150?img=7', '$2b$12$c6FmldQa4Jg0hR3p/nNL7OiMOKoeJ/FJKxn5dVHTybU2ETcxpxrdS', TRUE, FALSE),
('edward.garcia@example.com', 'edwardgarcia', 'Edward Garcia', '+1-555-0107', NULL, '$2b$12$c6FmldQa4Jg0hR3p/nNL7OiMOKoeJ/FJKxn5dVHTybU2ETcxpxrdS', TRUE, FALSE),
('fiona.martinez@example.com', 'fionamartinez', 'Fiona Martinez', '+1-555-0108', 'https://i.pravatar.cc/150?img=9', '$2b$12$c6FmldQa4Jg0hR3p/nNL7OiMOKoeJ/FJKxn5dVHTybU2ETcxpxrdS', TRUE, FALSE),
('george.anderson@example.com', 'georgeanderson', 'George Anderson', NULL, 'https://i.pravatar.cc/150?img=10', '$2b$12$c6FmldQa4Jg0hR3p/nNL7OiMOKoeJ/FJKxn5dVHTybU2ETcxpxrdS', TRUE, FALSE);

-- Note: Default password for all users is "password123"
-- Admin user (admin@example.com) has superuser privileges
-- User charlie.davis@example.com is inactive (is_active = FALSE)

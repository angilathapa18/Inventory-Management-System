-- Inventory & Asset Management System
-- Run in Supabase Dashboard → SQL Editor

CREATE TABLE IF NOT EXISTS roles (
    role_id SERIAL PRIMARY KEY,
    role_name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT
);

CREATE TABLE IF NOT EXISTS categories (
    category_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT
);

CREATE TABLE IF NOT EXISTS locations (
    location_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    address TEXT,
    is_active BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS suppliers (
    supplier_id SERIAL PRIMARY KEY,
    company_name VARCHAR(150) NOT NULL,
    contact_name VARCHAR(100),
    email VARCHAR(255),
    phone VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS users (
    user_id SERIAL PRIMARY KEY,
    role_id INT REFERENCES roles(role_id) ON DELETE SET NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    full_name VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    last_login TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS items (
    item_id SERIAL PRIMARY KEY,
    category_id INT REFERENCES categories(category_id) ON DELETE SET NULL,
    name VARCHAR(200) NOT NULL,
    sku VARCHAR(50) UNIQUE NOT NULL,
    reorder_level INT DEFAULT 10,
    unit_price DECIMAL(10, 2) DEFAULT 0.00
);

CREATE TABLE IF NOT EXISTS inventory (
    inventory_id SERIAL PRIMARY KEY,
    item_id INT REFERENCES items(item_id) ON DELETE CASCADE,
    location_id INT REFERENCES locations(location_id) ON DELETE CASCADE,
    quantity_on_hand INT NOT NULL DEFAULT 0,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS assets (
    asset_id SERIAL PRIMARY KEY,
    item_id INT REFERENCES items(item_id) ON DELETE CASCADE,
    serial_number VARCHAR(100) UNIQUE,
    location_id INT REFERENCES locations(location_id) ON DELETE SET NULL,
    supplier_id INT REFERENCES suppliers(supplier_id) ON DELETE SET NULL,
    status VARCHAR(50) DEFAULT 'In Stock',
    purchase_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS transactions (
    transaction_id SERIAL PRIMARY KEY,
    item_id INT REFERENCES items(item_id) ON DELETE SET NULL,
    location_id INT REFERENCES locations(location_id) ON DELETE SET NULL,
    user_id INT REFERENCES users(user_id) ON DELETE SET NULL,
    transaction_type VARCHAR(20) NOT NULL,
    quantity INT NOT NULL,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO roles (role_name, description) VALUES
    ('ADMIN', 'Full system access and user management'),
    ('MANAGER', 'Can edit inventory and view reports'),
    ('STAFF', 'Can perform check-ins and check-outs')
ON CONFLICT (role_name) DO NOTHING;

INSERT INTO locations (name, address)
SELECT 'Main Warehouse', '123 Supply Chain Road'
WHERE NOT EXISTS (SELECT 1 FROM locations WHERE name = 'Main Warehouse');

INSERT INTO locations (name, address)
SELECT 'Tech Lab', '456 Innovation Drive'
WHERE NOT EXISTS (SELECT 1 FROM locations WHERE name = 'Tech Lab');

INSERT INTO categories (name, description)
SELECT 'Laptops', 'Company issued computers'
WHERE NOT EXISTS (SELECT 1 FROM categories WHERE name = 'Laptops');

INSERT INTO categories (name, description)
SELECT 'Peripherals', 'Mice, Keyboards, Monitors'
WHERE NOT EXISTS (SELECT 1 FROM categories WHERE name = 'Peripherals');

INSERT INTO categories (name, description)
SELECT 'Stationery', 'Bulk office supplies'
WHERE NOT EXISTS (SELECT 1 FROM categories WHERE name = 'Stationery');

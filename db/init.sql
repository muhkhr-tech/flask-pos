CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role ENUM('admin', 'cashier') NOT NULL,
    is_active BOOLEAN,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO users (user_id, username, password, role, is_active)
VALUES (1, 'admin', '$2b$12$G5xSJ8mTrYK/RH6LDJg7RujxBPVEIfEokbFrQKfwAP7ZjhT.B0eOG', 'admin', TRUE);

CREATE TABLE categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(5) NOT NULL UNIQUE,
    name VARCHAR(50) NOT NULL,
    description TEXT,
    is_active BOOLEAN,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(10) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    category_id INT,
    price DECIMAL(10, 2) NOT NULL,
    stock INT DEFAULT 0,
    is_active BOOLEAN,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
);

CREATE TABLE sales (
    sale_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    payment_method ENUM('cash', 'credit_card', 'e-wallet') NOT NULL,
    sale_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    status ENUM('process', 'success', 'fail', 'cancel'),
    canceled_by INT,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE sale_details (
    sale_detail_id INT AUTO_INCREMENT PRIMARY KEY,
    sale_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    subtotal DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (sale_id) REFERENCES sales(sale_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

CREATE TABLE inventory_logs (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    change_type ENUM('restock', 'sale', 'adjustment') NOT NULL,
    quantity INT NOT NULL,
    log_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    note TEXT,
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

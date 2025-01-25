-- CREATE TABLE users
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role TEXT CHECK (role IN ('admin', 'cashier')) NOT NULL,
    is_active BOOLEAN,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- INSERT INTO users
INSERT INTO users (username, password, role, is_active)
VALUES ('admin', '$2b$12$G5xSJ8mTrYK/RH6LDJg7RujxBPVEIfEokbFrQKfwAP7ZjhT.B0eOG', 'admin', TRUE);

-- CREATE TABLE categories
CREATE TABLE categories (
    category_id SERIAL PRIMARY KEY,
    code VARCHAR(5) NOT NULL UNIQUE,
    name VARCHAR(50) NOT NULL,
    description TEXT,
    is_active BOOLEAN,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- CREATE TABLE products
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    code VARCHAR(10) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    category_id INT REFERENCES categories(category_id) ON DELETE SET NULL,
    price NUMERIC(10, 2) NOT NULL,
    stock INT DEFAULT 0,
    is_active BOOLEAN,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- CREATE TABLE sales
CREATE TABLE sales (
    sale_id SERIAL PRIMARY KEY,
    code VARCHAR(15) NOT NULL UNIQUE,
    user_id INT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    total_amount BIGINT NOT NULL,
    amount_paid BIGINT NOT NULL DEFAULT 0,
    amount_change BIGINT NOT NULL DEFAULT 0,
    payment_method TEXT CHECK (payment_method IN ('cash', 'transfer-bank', 'e-wallet', 'qris')),
    sale_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    status TEXT CHECK (status IN ('proses', 'sukses', 'gagal', 'batal')) NOT NULL,
    canceled_by INT REFERENCES users(user_id) ON DELETE SET NULL
);

-- CREATE TABLE sale_details
CREATE TABLE sale_details (
    sale_detail_id SERIAL PRIMARY KEY,
    sale_id INT NOT NULL REFERENCES sales(sale_id) ON DELETE CASCADE,
    product_id INT NOT NULL REFERENCES products(product_id) ON DELETE CASCADE,
    quantity INT NOT NULL,
    price BIGINT NOT NULL,
    subtotal BIGINT NOT NULL,
    UNIQUE (sale_id, product_id)
);

-- CREATE TABLE inventory_logs
CREATE TABLE inventory_logs (
    log_id SERIAL PRIMARY KEY,
    product_id INT NOT NULL REFERENCES products(product_id) ON DELETE CASCADE,
    change_type TEXT CHECK (change_type IN ('restock', 'sale', 'adjustment')) NOT NULL,
    quantity INT NOT NULL,
    log_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    note TEXT
);

--table view untuk ambil struct dengan status 'proses'
CREATE OR REPLACE VIEW public.v_get_struct
AS SELECT s.sale_id,
    s.code,
    s.user_id,
    s.total_amount,
    s.payment_method,
    to_char(s.sale_date, 'FMDay, DD FMMonth YYYY HH24:MI TZ'::text) AS sale_date,
    s.status,
    u.username AS cashier,
    jsonb_agg(jsonb_build_object('product_id', p.product_id, 'product_code', p.code, 'product_name', p.name, 'quantity', sd.quantity, 'price', sd.price, 'amount', sd.quantity * sd.price)) AS products,
    s.amount_paid,
    s.amount_change
   FROM sales s
     JOIN sale_details sd ON s.sale_id = sd.sale_id
     JOIN products p ON sd.product_id = p.product_id
     JOIN users u ON u.user_id = s.user_id
  GROUP BY s.sale_id, u.username;

--fungsi untuk kurang/hapus sales
CREATE OR REPLACE FUNCTION public.update_sale_details_and_sales(p_sale_id integer, p_product_id integer, p_user_id integer)
 RETURNS void
 LANGUAGE plpgsql
AS $function$
begin
    -- Kurangi quantity jika lebih dari 1
    UPDATE sale_details
    SET quantity = quantity - 1,
        subtotal = subtotal - price
    WHERE sale_id = p_sale_id
      AND product_id = p_product_id
      AND quantity > 0;

    -- Hapus baris jika quantity menjadi 0
    DELETE FROM sale_details
    WHERE sale_id = p_sale_id
      AND product_id = p_product_id
      AND quantity = 0;

    -- Perbarui total_amount di tabel sales
    UPDATE sales
    SET total_amount = (
        SELECT COALESCE(SUM(subtotal), 0)
        FROM sale_details
        WHERE sale_id = p_sale_id
    ),
    user_id = p_user_id
    WHERE sale_id = p_sale_id;

   DELETE FROM sales
    WHERE sale_id = p_sale_id
      AND total_amount = 0;

    update products
	set stock=stock+1
    WHERE product_id = p_product_id;
END;
$function$
;

--fungsi untuk buat sale
CREATE OR REPLACE FUNCTION public.insert_sales(p_product_id integer, p_user_id integer, p_code character varying)
 RETURNS void
 LANGUAGE plpgsql
AS $function$
declare
new_sale_id INT;
    product_price bigint;
begin
	SELECT price INTO product_price
    FROM products
    WHERE product_id = p_product_id and stock > 0;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Stok kurang';
    END IF;

    INSERT INTO sales (code, total_amount, status, user_id)
    values (
    	p_code,
        product_price,
--        'cash',
        'proses',
        p_user_id)
    returning sale_id into new_sale_id;

   insert into sale_details (quantity, subtotal, product_id, sale_id, price)
   values(1, product_price, p_product_id, new_sale_id, product_price);

  	update products
	set stock=stock-1
    WHERE product_id = p_product_id;
END;
$function$
;

--fungsi untuk update/tambah produk ke struk
CREATE OR REPLACE FUNCTION public.update_sale_details_and_sales(p_sale_id integer, p_product_id integer, p_user_id integer)
 RETURNS void
 LANGUAGE plpgsql
AS $function$
BEGIN
    -- Kurangi quantity jika lebih dari 1
    UPDATE sale_details
    SET quantity = quantity - 1,
        subtotal = subtotal - price
    WHERE sale_id = p_sale_id
      AND product_id = p_product_id
      AND quantity > 0;

    -- Hapus baris jika quantity menjadi 0
    DELETE FROM sale_details
    WHERE sale_id = p_sale_id
      AND product_id = p_product_id
      AND quantity = 0;

    -- Perbarui total_amount di tabel sales
    UPDATE sales
    SET total_amount = (
        SELECT COALESCE(SUM(subtotal), 0)
        FROM sale_details
        WHERE sale_id = p_sale_id
    ),
    user_id = p_user_id
    WHERE sale_id = p_sale_id;

   DELETE FROM sales
    WHERE sale_id = p_sale_id
      AND total_amount = 0;
END;
$function$
;

--fungsi untuk tambah produk ke cart
CREATE OR REPLACE FUNCTION public.update_cart(p_sale_id integer, p_product_id integer, p_user_id integer)
 RETURNS void
 LANGUAGE plpgsql
AS $function$
declare
    product_price bigint;
   	new_subtotal bigint;
begin
	SELECT price into product_price
    FROM products
    WHERE product_id = p_product_id and stock > 0;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Stok kurang';
    END IF;

   insert into sale_details (quantity, subtotal, product_id, sale_id, price)
   values(1, product_price, p_product_id, p_sale_id, product_price)
   on conflict (sale_id, product_id) do update
   set quantity=sale_details.quantity+1, subtotal=sale_details.subtotal+product_price
   returning subtotal into new_subtotal;

  	update sales
  	set user_id=p_user_id, total_amount=(select sum(subtotal) from sale_details where sale_id = p_sale_id)
  	where sale_id=p_sale_id;

  	update products
	set stock=stock-1
    WHERE product_id = p_product_id;
END;
$function$
;

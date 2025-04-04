-- create payments table
CREATE TYPE payment_status AS ENUM ('pending', 'paid', 'refused', 'refunded', 'cancelled');
CREATE TYPE payment_methods AS ENUM ('credit_card', 'debit_card', 'paypal', 'pix', 'boleto', 'cash', 'gift_card');

CREATE TABLE IF NOT EXISTS payments (
    payment_id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES orders(order_id),
    amount DECIMAL(10, 2) NOT NULL,
    payment_method payment_methods NOT NULL,
    status payment_status NOT NULL DEFAULT 'pending',
    payment_details JSONB,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NULL,
    deleted_at TIMESTAMP WITH TIME ZONE NULL
);

COMMENT ON TABLE payments IS 'Stores payment information.';

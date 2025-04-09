-- create transactions table
-- CREATE TYPE transaction_status AS ENUM ('pending', 'paid', 'refused', 'refunded', 'cancelled', 'failed', 'disputed', 'chargeback', 'reversed', 'completed', 'processing', 'on_hold', 'partially_refunded', 'partially_paid', 'voided');
-- CREATE TYPE transaction_type AS ENUM ('credit', 'debit');
-- CREATE TYPE transaction_method AS ENUM ('credit_card', 'debit_card', 'paypal', 'pix', 'boleto', 'cash', 'gift_card', 'bank_transfer', 'crypto');

CREATE TABLE IF NOT EXISTS transactions (
    transaction_id SERIAL PRIMARY KEY,
    wallet_id INTEGER NOT NULL REFERENCES wallets(wallet_id), 
    amount DECIMAL(10, 2) NOT NULL,
    status transaction_status NOT NULL DEFAULT 'pending',
    type transaction_type NOT NULL DEFAULT 'credit',
    method transaction_method NOT NULL DEFAULT 'cash',
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NULL,
    deleted_at TIMESTAMP WITH TIME ZONE NULL,
    additional_info JSONB NULL
);

COMMENT ON TABLE transactions IS 'Stores transaction information.';
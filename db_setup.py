import sqlite3
import os
from typing import List, Dict, Any

DB_PATH = "fintech_ledger.db"

SCHEMA_DDL = """
CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY,
    full_name TEXT NOT NULL,
    city TEXT NOT NULL,
    risk_tier TEXT CHECK(risk_tier IN ('Low', 'Medium', 'High')),
    kyc_verified INTEGER DEFAULT 1,
    signup_date DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS accounts (
    account_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    account_type TEXT CHECK(account_type IN ('Checking', 'Savings', 'Corporate')),
    balance_pkr REAL NOT NULL,
    status TEXT CHECK(status IN ('Active', 'Frozen', 'Closed')),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE IF NOT EXISTS merchants (
    merchant_id INTEGER PRIMARY KEY,
    merchant_name TEXT NOT NULL,
    category TEXT NOT NULL,
    city TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS transactions (
    txn_id INTEGER PRIMARY KEY,
    account_id INTEGER NOT NULL,
    merchant_id INTEGER NOT NULL,
    amount_pkr REAL NOT NULL,
    txn_type TEXT CHECK(txn_type IN ('Debit', 'Credit')),
    is_flagged_fraud INTEGER DEFAULT 0,
    txn_timestamp DATETIME NOT NULL,
    FOREIGN KEY (account_id) REFERENCES accounts(account_id),
    FOREIGN KEY (merchant_id) REFERENCES merchants(merchant_id)
);

CREATE TABLE IF NOT EXISTS loans (
    loan_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    principal_pkr REAL NOT NULL,
    interest_rate REAL NOT NULL,
    loan_status TEXT CHECK(loan_status IN ('Current', 'Defaulted', 'Paid')),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);
"""

def init_database(db_path: str = DB_PATH) -> None:
    if os.path.exists(db_path):
        os.remove(db_path)

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.executescript(SCHEMA_DDL)

    customers = [
        (1, "Zainab Tariq", "Lahore", "Low", 1, "2024-01-15"),
        (2, "Bilal Mahmood", "Karachi", "High", 1, "2024-03-22"),
        (3, "Hamza Siddiqui", "Islamabad", "Medium", 1, "2024-05-10"),
        (4, "Ayesha Khan", "Lahore", "Low", 1, "2024-07-01"),
        (5, "Usman Farooq", "Lahore", "High", 0, "2024-08-19"),
        (6, "Sara Raza", "Karachi", "Low", 1, "2024-09-12"),
        (7, "Omar Sheikh", "Islamabad", "Medium", 1, "2024-11-05"),
        (8, "Fatima Noor", "Lahore", "High", 0, "2025-01-20"),
    ]
    cur.executemany("INSERT INTO customers VALUES (?, ?, ?, ?, ?, ?);", customers)

    accounts = [
        (101, 1, "Savings", 1450000.0, "Active"),
        (102, 1, "Checking", 320000.0, "Active"),
        (103, 2, "Corporate", 4800000.0, "Frozen"),
        (104, 3, "Checking", 215000.0, "Active"),
        (105, 4, "Savings", 980000.0, "Active"),
        (106, 5, "Checking", 65000.0, "Frozen"),
        (107, 6, "Corporate", 3100000.0, "Active"),
        (108, 7, "Savings", 540000.0, "Active"),
        (109, 8, "Checking", 110000.0, "Active"),
    ]
    cur.executemany("INSERT INTO accounts VALUES (?, ?, ?, ?, ?);", accounts)

    merchants = [
        (1, "Johnny & Jugnu", "Food & Dining", "Lahore"),
        (2, "CloudHost PK", "Technology", "Karachi"),
        (3, "Packages Mall Retail", "Shopping", "Lahore"),
        (4, "AirBlue Ticketing", "Travel", "Islamabad"),
        (5, "CryptoSwap Exchange", "Financial Services", "Karachi"),
    ]
    cur.executemany("INSERT INTO merchants VALUES (?, ?, ?, ?);", merchants)

    transactions = [
        (1001, 102, 1, 4500.0, "Debit", 0, "2026-02-01 13:20:00"),
        (1002, 102, 3, 28000.0, "Debit", 0, "2026-02-02 18:10:00"),
        (1003, 103, 5, 950000.0, "Debit", 1, "2026-02-03 02:15:00"),
        (1004, 104, 4, 64000.0, "Debit", 0, "2026-02-04 09:45:00"),
        (1005, 105, 1, 3200.0, "Debit", 0, "2026-02-05 20:00:00"),
        (1006, 106, 5, 180000.0, "Debit", 1, "2026-02-06 03:40:00"),
        (1007, 107, 2, 420000.0, "Debit", 0, "2026-02-07 11:30:00"),
        (1008, 108, 4, 85000.0, "Debit", 0, "2026-02-08 15:10:00"),
        (1009, 109, 5, 290000.0, "Debit", 1, "2026-02-09 01:05:00"),
        (1010, 101, 2, 55000.0, "Credit", 0, "2026-02-10 10:00:00"),
        (1011, 103, 2, 310000.0, "Debit", 1, "2026-02-11 04:12:00"),
        (1012, 105, 3, 42000.0, "Debit", 0, "2026-02-12 17:25:00"),
    ]
    cur.executemany("INSERT INTO transactions VALUES (?, ?, ?, ?, ?, ?, ?);", transactions)

    loans = [
        (501, 1, 1200000.0, 14.5, "Current"),
        (502, 2, 3500000.0, 19.0, "Defaulted"),
        (503, 3, 800000.0, 15.0, "Paid"),
        (504, 5, 1500000.0, 21.0, "Defaulted"),
        (505, 6, 2000000.0, 13.5, "Current"),
        (506, 8, 950000.0, 18.5, "Defaulted"),
    ]
    cur.executemany("INSERT INTO loans VALUES (?, ?, ?, ?, ?);", loans)

    conn.commit()
    conn.close()


BENCHMARK_TEST_SUITE: List[Dict[str, Any]] = [
    {
        "id": 1,
        "difficulty": "Easy",
        "question": "List all customers from Lahore along with their risk tier.",
        "gold_sql": "SELECT full_name, risk_tier FROM customers WHERE city = 'Lahore';",
        "base_pred_sql": "SELECT full_name, risk_tier FROM customers WHERE city = 'Lahore';",
        "qlora_pred_sql": "SELECT full_name, risk_tier FROM customers WHERE city = 'Lahore';",
    },
    {
        "id": 2,
        "difficulty": "Easy",
        "question": "What is the total balance across all active accounts?",
        "gold_sql": "SELECT SUM(balance_pkr) AS total_active_balance FROM accounts WHERE status = 'Active';",
        "base_pred_sql": "SELECT SUM(balance) FROM accounts WHERE status = 'Active';",
        "qlora_pred_sql": "SELECT SUM(balance_pkr) AS total_active_balance FROM accounts WHERE status = 'Active';",
    },
    {
        "id": 3,
        "difficulty": "Easy",
        "question": "Show all transactions that were flagged as fraud ordered by amount descending.",
        "gold_sql": "SELECT txn_id, account_id, amount_pkr, txn_timestamp FROM transactions WHERE is_flagged_fraud = 1 ORDER BY amount_pkr DESC;",
        "base_pred_sql": "SELECT txn_id, account_id, amount_pkr, txn_timestamp FROM transactions WHERE is_flagged_fraud = 1 ORDER BY amount_pkr DESC;",
        "qlora_pred_sql": "SELECT txn_id, account_id, amount_pkr, txn_timestamp FROM transactions WHERE is_flagged_fraud = 1 ORDER BY amount_pkr DESC;",
    },
    {
        "id": 4,
        "difficulty": "Medium",
        "question": "Count the number of accounts and average balance for each account type.",
        "gold_sql": "SELECT account_type, COUNT(account_id) AS account_count, AVG(balance_pkr) AS avg_balance FROM accounts GROUP BY account_type;",
        "base_pred_sql": "SELECT account_type, COUNT(account_id), AVG(balance) FROM accounts;",
        "qlora_pred_sql": "SELECT account_type, COUNT(account_id) AS account_count, AVG(balance_pkr) AS avg_balance FROM accounts GROUP BY account_type;",
    },
    {
        "id": 5,
        "difficulty": "Medium",
        "question": "Show each customer's full name, city, and their total account balance across all accounts.",
        "gold_sql": "SELECT c.full_name, c.city, SUM(a.balance_pkr) AS total_balance FROM customers c JOIN accounts a ON c.customer_id = a.customer_id GROUP BY c.customer_id, c.full_name, c.city;",
        "base_pred_sql": "SELECT full_name, city, SUM(balance_pkr) FROM customers JOIN accounts ON customer_id = customer_id GROUP BY full_name;",
        "qlora_pred_sql": "SELECT c.full_name, c.city, SUM(a.balance_pkr) AS total_balance FROM customers c JOIN accounts a ON c.customer_id = a.customer_id GROUP BY c.customer_id, c.full_name, c.city;",
    },
    {
        "id": 6,
        "difficulty": "Medium",
        "question": "Calculate the total transaction volume per merchant category.",
        "gold_sql": "SELECT m.category, SUM(t.amount_pkr) AS total_volume, COUNT(t.txn_id) AS txn_count FROM merchants m JOIN transactions t ON m.merchant_id = t.merchant_id GROUP BY m.category ORDER BY total_volume DESC;",
        "base_pred_sql": "SELECT category, SUM(amount) FROM merchants JOIN transactions GROUP BY category;",
        "qlora_pred_sql": "SELECT m.category, SUM(t.amount_pkr) AS total_volume, COUNT(t.txn_id) AS txn_count FROM merchants m JOIN transactions t ON m.merchant_id = t.merchant_id GROUP BY m.category ORDER BY total_volume DESC;",
    },
    {
        "id": 7,
        "difficulty": "Hard",
        "question": "Find all customers who have both a Defaulted loan and at least one fraud-flagged transaction.",
        "gold_sql": "SELECT DISTINCT c.full_name, c.city, c.risk_tier FROM customers c JOIN loans l ON c.customer_id = l.customer_id JOIN accounts a ON c.customer_id = a.customer_id JOIN transactions t ON a.account_id = t.account_id WHERE l.loan_status = 'Defaulted' AND t.is_flagged_fraud = 1;",
        "base_pred_sql": "SELECT full_name FROM customers WHERE loan_status = 'Defaulted' AND is_flagged_fraud = 1;",
        "qlora_pred_sql": "SELECT DISTINCT c.full_name, c.city, c.risk_tier FROM customers c JOIN loans l ON c.customer_id = l.customer_id JOIN accounts a ON c.customer_id = a.customer_id JOIN transactions t ON a.account_id = t.account_id WHERE l.loan_status = 'Defaulted' AND t.is_flagged_fraud = 1;",
    },
    {
        "id": 8,
        "difficulty": "Hard",
        "question": "List merchants where the total fraud transaction amount exceeds 100,000 PKR.",
        "gold_sql": "SELECT m.merchant_name, m.category, SUM(t.amount_pkr) AS fraud_volume FROM merchants m JOIN transactions t ON m.merchant_id = t.merchant_id WHERE t.is_flagged_fraud = 1 GROUP BY m.merchant_id, m.merchant_name, m.category HAVING SUM(t.amount_pkr) > 100000;",
        "base_pred_sql": "SELECT m.merchant_name, SUM(t.amount_pkr) FROM merchants m JOIN transactions t ON m.merchant_id = t.merchant_id WHERE t.is_flagged_fraud = 1 AND SUM(t.amount_pkr) > 100000 GROUP BY m.merchant_name;",
        "qlora_pred_sql": "SELECT m.merchant_name, m.category, SUM(t.amount_pkr) AS fraud_volume FROM merchants m JOIN transactions t ON m.merchant_id = t.merchant_id WHERE t.is_flagged_fraud = 1 GROUP BY m.merchant_id, m.merchant_name, m.category HAVING SUM(t.amount_pkr) > 100000;",
    },
    {
        "id": 9,
        "difficulty": "Extra-Hard",
        "question": "Find accounts whose balance is strictly greater than the average balance of all Corporate accounts.",
        "gold_sql": "SELECT account_id, account_type, balance_pkr FROM accounts WHERE balance_pkr > (SELECT AVG(balance_pkr) FROM accounts WHERE account_type = 'Corporate');",
        "base_pred_sql": "SELECT account_id, account_type, balance_pkr FROM accounts WHERE balance_pkr > AVG(balance_pkr) AND account_type = 'Corporate';",
        "qlora_pred_sql": "SELECT account_id, account_type, balance_pkr FROM accounts WHERE balance_pkr > (SELECT AVG(balance_pkr) FROM accounts WHERE account_type = 'Corporate');",
    },
    {
        "id": 10,
        "difficulty": "Extra-Hard",
        "question": "Rank cities by their total defaulted loan principal and display the number of high-risk customers in each city.",
        "gold_sql": "SELECT c.city, SUM(CASE WHEN l.loan_status = 'Defaulted' THEN l.principal_pkr ELSE 0 END) AS defaulted_principal, COUNT(DISTINCT CASE WHEN c.risk_tier = 'High' THEN c.customer_id END) AS high_risk_customers FROM customers c LEFT JOIN loans l ON c.customer_id = l.customer_id GROUP BY c.city ORDER BY defaulted_principal DESC;",
        "base_pred_sql": "SELECT city, SUM(principal), COUNT(customer_id) FROM customers JOIN loans ON customer_id = customer_id WHERE loan_status = 'Defaulted' AND risk_tier = 'High' GROUP BY city;",
        "qlora_pred_sql": "SELECT c.city, SUM(CASE WHEN l.loan_status = 'Defaulted' THEN l.principal_pkr ELSE 0 END) AS defaulted_principal, COUNT(DISTINCT CASE WHEN c.risk_tier = 'High' THEN c.customer_id END) AS high_risk_customers FROM customers c LEFT JOIN loans l ON c.customer_id = l.customer_id GROUP BY c.city ORDER BY defaulted_principal DESC;",
    },
]

if __name__ == "__main__":
    init_database()
    print(f"Database '{DB_PATH}' created and seeded successfully.")

Here is a **very brief, clean, professional README** suitable for Milestone 2:

---

# **Library Management System – Milestone 2**

**CS-4347 Database Systems**

## **Overview**

This project implements the backend logic for a Library Management System. It provides SQL-driven functionality for book search, borrower management, book loans, and fine calculation. This milestone focuses on core database operations; GUI integration will be completed in Milestone 3.

## **Tech Stack**

* **Language:** Python 3.10
* **Database:** MySQL 8.x
* **Libraries:** `mysql-connector-python`
* **Schema:** Provided course schema with minor extensions (fully backward-compatible).

## **Features Implemented (Milestone 2)**

* Case-insensitive, substring book search (ISBN/title/author).
* Real-time availability status.
* Checkout with rules: max 3 active loans, no unpaid fines, book must be available.
* Check-in using ISBN, card number, or borrower name search.
* Borrower creation with SSN uniqueness check and auto-generated card number.
* Fine calculation/update at $0.25/day for returned and unreturned late books.
* Payment processing for fully returned books only; grouped fine totals.

## **How to Run**

1. Install dependencies:
   `pip install mysql-connector-python`
2. Import the SQL schema from `/sql/schema.sql` into MySQL.
3. Update the database credentials in `config.py`.
4. Run the application:
   `python main.py`

## **Project Structure**

```
/src
   main.py
   search.py
   loans.py
   borrowers.py
   fines.py
   database.py
/sql
   schema.sql
README.pdf
```

## **Notes**

* All functions return structured objects or error messages for GUI use in Milestone 3.
* No GUI is required in this milestone.

---
# Personal Expense Tracker

A simple web-based personal expense tracker built as part of a Software Engineer Practical Test.

The application allows users to add, view, edit, delete, filter, and summarize their personal expenses.



- Backend: Python, Flask
- **Database:** SQLite
- **Frontend:** HTML, CSS, JavaScript
- **API:** Flask REST-style API endpoints

## Why This Stack?

I chose Flask and SQLite because they are lightweight and quick to develop with.

- Flask provides a simple Python backend.
- SQLite does not require a separate database server.
- HTML, CSS, and JavaScript are sufficient for the frontend requirements.
- This stack allowed the core functionality to be implemented within the two-hour time limit.

---

## Features

### Add Expense

Users can add an expense with:

- Title
- Amount
- Category
- Date
- Optional note

Available categories:

- Food
- Transport
- Shopping
- Bills
- Entertainment
- Other

If no date is provided, the application uses today's date.

### View Expenses

All saved expenses are displayed in the expense list.

Expenses are sorted by date, with the most recent expenses shown first.

### Edit Expense

Existing expenses can be edited.

Users can update:

- Title
- Amount
- Category
- Date
- Note

### Delete Expense

Users can delete an existing expense.

If the requested expense does not exist, the backend returns a `404` response.

### Monthly Summary

The application provides a summary for the current month:

- Total amount spent
- Category-wise spending breakdown

### Filtering

Expenses can be filtered by:

- Category
- From date
- To date
- Title

The title filter supports partial text matching.

For example, searching for `coffee` can match:

```text
Coffee at Starbucks
Morning Coffee
Coffee with friend
```

Multiple filters can also be used together.

---

## Project Structure

```text
expense-tracker/
│
├── app.py
├── database.db
├── requirements.txt
│
├── templates/
│   └── index.html

```

`database.db` is created automatically when the application is started for the first time.

---

## Database

The application uses SQLite with an `expenses` table.

```text
expenses
--------------------------------
id        INTEGER PRIMARY KEY
title     TEXT NOT NULL
amount    REAL NOT NULL
category  TEXT NOT NULL
date      TEXT NOT NULL
note      TEXT
```

### Fields

| Field      | Description               |
| ---------- | ------------------------- |
| `id`       | Unique ID for the expense |
| `title`    | Short description         |
| `amount`   | Expense amount            |
| `category` | Expense category          |
| `date`     | Expense date              |
| `note`     | Optional note             |

---

# How to Run

## Requirements

- Python 3.x
- pip

## 1. Open the project folder


cd expense-tracker


## 2. Create a virtual environment


python -m venv venv


## 3. Activate the virtual environment

### Windows Command Prompt


venv\Scripts\activate

### Windows PowerShell


venv\Scripts\Activate.ps1


## 4. Install dependencies


pip install -r requirements.txt


If `requirements.txt` is not available:


pip install flask


## 5. Start the application

```bash
python app.py
```

The Flask application will start locally.

Open the URL shown in the terminal, usually:

```text
http://127.0.0.1:5000
```

---

# API Endpoints

## Get Expenses

```text
GET /api/expenses
```

Returns all expenses.

### Filter by Category

```text
GET /api/expenses?category=Food
```

### Filter by Date Range

```text
GET /api/expenses?from=2026-11-01&to=2026-11-10
```

### Filter by Title

```text
GET /api/expenses?title=coffee
```

### Combine Filters

```text
GET /api/expenses?category=Food&from=2026-11-01&to=2026-11-10&title=coffee
```

---

## Add Expense

```text
POST /api/expenses
```

Example request:

```json
{
    "title": "Coffee at Starbucks",
    "amount": 250,
    "category": "Food",
    "date": "2026-11-10",
    "note": "Morning coffee"
}
```

The date is optional. If omitted, the application uses today's date.

### Validation

The backend rejects:

- Empty titles
- Amounts less than or equal to zero
- Invalid categories

---

## Update Expense

```text
PUT /api/expenses/<id>
```

Example:

```text
PUT /api/expenses/1
```

Request body:

```json
{
    "title": "Coffee and snacks",
    "amount": 300,
    "category": "Food",
    "date": "2026-11-10",
    "note": "Updated expense"
}
```

If the expense does not exist, the API returns:

```text
404 Expense not found
```

---

## Delete Expense

```text
DELETE /api/expenses/<id>
```

Example:

```text
DELETE /api/expenses/1
```

If the expense does not exist, the API returns a `404` response.

---

## Monthly Summary

```text
GET /api/summary
```

Returns the total spending and category breakdown for the current month.

Example:

```json
{
    "month": "2026-11",
    "total": 5000,
    "breakdown": {
        "Food": 1500,
        "Transport": 1000,
        "Shopping": 1200,
        "Bills": 800,
        "Entertainment": 300,
        "Other": 200
    }
}
```

---

# Validation and Edge Cases

The application handles several basic edge cases.

### Empty Title

An expense cannot be created or updated without a title.

Response:

```text
Title is required
```

### Invalid Amount

The amount must be a valid number greater than zero.

For example:

```text
0
-100
abc
```

are rejected.

### Invalid Category

The category must be one of:

```text
Food
Transport
Shopping
Bills
Entertainment
Other
```

### Missing Expense

Trying to update or delete an expense that does not exist returns:

```text
Expense not found
```

with HTTP status `404`.

### Empty Results

If no expenses match the selected filters, the application displays an empty result instead of failing.

### Date Range

The `from` and `to` filters are applied to the expense date.

For example:

```text
from = 2026-11-01
to   = 2026-11-10
```

returns expenses between those dates.

---

# Sorting

Expenses are retrieved using:

```sql
ORDER BY date DESC
```

Therefore, the most recent expenses appear first.

---

# Monthly Summary

The current month is determined using:

```python
current_month = date.today().strftime("%Y-%m")
```

The application then calculates:

1. Total spending for the current month.
2. Spending grouped by category.

If there are no expenses during the current month, the total is returned as `0`.

---

# Testing

The main functionality can be manually tested using the following scenarios.

## 1. Add an Expense

1. Open the application.
2. Enter a title.
3. Enter an amount.
4. Select a category.
5. Select a date.
6. Optionally enter a note.
7. Submit the form.
8. Verify that the expense appears in the list.

## 2. Edit an Expense

1. Select an existing expense.
2. Change one or more fields.
3. Save the changes.
4. Verify the updated values.

## 3. Delete an Expense

1. Select an existing expense.
2. Delete it.
3. Verify that it is removed from the list.

## 4. Test Category Filter

Select:

```text
Food
```

Verify that only Food expenses are displayed.

## 5. Test Date Filter

Enter a `from` and `to` date.

Verify that only expenses within the selected date range are displayed.

## 6. Test Title Filter

Search for part of an expense title.

For example:

```text
coffee
```

Verify that matching expenses are displayed.

## 7. Test Combined Filters

Use multiple filters together:

```text
Category: Food
From: 2026-11-01
To: 2026-11-10
Title: coffee
```

Verify that only matching expenses are displayed.

## 8. Test Invalid Input

Try:

```text
Title: empty
Amount: 0
Amount: -100
```

The application should reject invalid input.

---

---

# What's Skipped

The following features were not implemented because they were outside the required scope or not necessary for the available two-hour development time:

- Authentication
- Multi-user support
- Multi-currency support
- Cloud deployment
- Automated test suite
- CSV/PDF export
- Advanced analytics
- Pagination

The priority was to build a smaller working application covering the core requirements rather than adding features that could make the application incomplete or unstable.

---

# Known Rough Edges

- The application is designed for local, single-user use.
- SQLite is suitable for this small application but would not be ideal for a large multi-user production system.
- There is no authentication because it was not required.
- The UI focuses on functionality rather than pixel-perfect design.
- Automated tests are not included.
- Validation could be expanded further for a production application.

---

# Possible Future Improvements

If additional development time were available, I would consider:

- Automated unit and integration tests
- Authentication and user accounts
- PostgreSQL for production use
- CSV export
- More detailed spending charts
- Pagination
- Improved error messages
- Confirmation before deleting expenses
- Stronger date validation
- Responsive/mobile improvements
- Docker support
- Production deployment

---

# Development Approach

The application was developed by prioritizing the required functionality:

1. Set up Flask.
2. Created the SQLite database.
3. Created the expense data model.
4. Implemented expense CRUD APIs.
5. Implemented filtering.
6. Implemented monthly summary calculations.
7. Connected the frontend to the backend.
8. Added basic validation.
9. Tested the main user flows manually.

The implementation intentionally uses a simple architecture to keep the code understandable and easy to run locally.

---

# Conclusion

This project implements a functional personal expense tracker using Python, Flask, SQLite, HTML, CSS, and JavaScript.

It provides the core functionality required by the practical test, including expense CRUD operations, filtering, monthly summaries, category breakdowns, and basic validation.

The application is designed to be simple, maintainable, and easy to run locally.

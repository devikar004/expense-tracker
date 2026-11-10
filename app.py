from flask import Flask, request, jsonify, render_template
import sqlite3
from datetime import date

app = Flask(__name__)

DB = "database.db"

CATEGORIES = [
    "Food",
    "Transport",
    "Shopping",
    "Bills",
    "Entertainment",
    "Other"
]


def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            note TEXT
        )
    """)

    conn.commit()
    conn.close()


@app.route("/")
def home():
    return render_template("index.html")



@app.route("/api/expenses", methods=["GET"])
def get_expenses():
    category = request.args.get("category", "")
    from_date = request.args.get("from", "")
    to_date = request.args.get("to", "")
    title = request.args.get("title", "")

    query = "SELECT * FROM expenses WHERE 1=1"
    params = []

    if category:
        query += " AND category = ?"
        params.append(category)

   
    if from_date:
        query += " AND date >= ?"
        params.append(from_date)

  
    if to_date:
        query += " AND date <= ?"
        params.append(to_date)

   
    if title:
        query += " AND title LIKE ?"
        params.append(f"%{title}%")

  
    query += " ORDER BY date DESC"

    conn = get_db()
    expenses = conn.execute(query, params).fetchall()
    conn.close()

    return jsonify([dict(expense) for expense in expenses])


@app.route("/api/expenses", methods=["POST"])
def add_expense():

    data = request.json

    title = data.get("title", "").strip()
    amount = data.get("amount")
    category = data.get("category")
    expense_date = data.get("date") or str(date.today())
    note = data.get("note", "").strip()

    if not title:
        return jsonify({"error": "Title is required"}), 400

    try:
        amount = float(amount)
        if amount <= 0:
            raise ValueError
    except:
        return jsonify({"error": "Amount must be greater than 0"}), 400

    if category not in CATEGORIES:
        return jsonify({"error": "Invalid category"}), 400

    if not expense_date:
        expense_date = str(date.today())

    conn = get_db()

    conn.execute("""
        INSERT INTO expenses
        (title, amount, category, date, note)
        VALUES (?, ?, ?, ?, ?)
    """, (title, amount, category, expense_date, note))

    conn.commit()
    conn.close()

    return jsonify({"message": "Expense added successfully"}), 201


@app.route("/api/expenses/<int:id>", methods=["PUT"])
def update_expense(id):

    data = request.json

    title = data.get("title", "").strip()
    amount = data.get("amount")
    category = data.get("category")
    expense_date = data.get("date")
    note = data.get("note", "").strip()

    if not title:
        return jsonify({"error": "Title is required"}), 400

    try:
        amount = float(amount)
        if amount <= 0:
            raise ValueError
    except:
        return jsonify({"error": "Invalid amount"}), 400

    if category not in CATEGORIES:
        return jsonify({"error": "Invalid category"}), 400

    conn = get_db()

    result = conn.execute("""
        UPDATE expenses
        SET title=?, amount=?, category=?, date=?, note=?
        WHERE id=?
    """, (title, amount, category, expense_date, note, id))

    conn.commit()
    conn.close()

    if result.rowcount == 0:
        return jsonify({"error": "Expense not found"}), 404

    return jsonify({"message": "Expense updated"})



@app.route("/api/expenses/<int:id>", methods=["DELETE"])
def delete_expense(id):

    conn = get_db()

    result = conn.execute(
        "DELETE FROM expenses WHERE id=?", (id,)
    )

    conn.commit()
    conn.close()

    if result.rowcount == 0:
        return jsonify({"error": "Expense not found"}), 404

    return jsonify({"message": "Expense deleted"})



@app.route("/api/summary", methods=["GET"])
def summary():

    current_month = date.today().strftime("%Y-%m")

    conn = get_db()

    total = conn.execute("""
        SELECT COALESCE(SUM(amount), 0)
        FROM expenses
        WHERE date LIKE ?
    """, (current_month + "%",)).fetchone()[0]

    rows = conn.execute("""
        SELECT category, SUM(amount) as total
        FROM expenses
        WHERE date LIKE ?
        GROUP BY category
    """, (current_month + "%",)).fetchall()

    conn.close()

    breakdown = {
        row["category"]: row["total"]
        for row in rows
    }

    return jsonify({
        "month": current_month,
        "total": total,
        "breakdown": breakdown
    })


if __name__ == "__main__":
    init_db()
    app.run(debug=True)


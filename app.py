from flask import Flask, render_template, request, redirect, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "library_secret_key"

# MySQL Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="19muktai@biradar2006",
    database="library_db"
)

cursor = db.cursor()

# Home Page
@app.route('/')
def home():
    return render_template('login.html')


# Login Function
@app.route('/login', methods=['POST'])
def login():

    username = request.form['username']
    password = request.form['password']

    query = "SELECT * FROM admin WHERE username=%s AND password=%s"
    values = (username, password)

    cursor.execute(query, values)

    admin = cursor.fetchone()

    if admin:
        session['admin_logged_in'] = True
        return redirect('/dashboard')

    else:
        return "Invalid Username or Password"
@app.route('/dashboard')
def dashboard():

    if 'admin_logged_in' in session:

        cursor = db.cursor()

        # Total Books
        cursor.execute("SELECT COUNT(*) FROM books")
        total_books = cursor.fetchone()[0]

        # Issued Books
        cursor.execute(
            "SELECT COUNT(*) FROM issued_books WHERE status='Issued'"
        )
        issued_books = cursor.fetchone()[0]

        # Returned Books
        cursor.execute(
            "SELECT COUNT(*) FROM issued_books WHERE status='Returned'"
        )
        returned_books = cursor.fetchone()[0]

        cursor.close()

        return render_template(
            'dashboard.html',

            total_books=total_books,
            issued_books=issued_books,
            returned_books=returned_books
        )

    else:
        return redirect('/')

# Books Page
@app.route('/books')
def books():

    search = request.args.get('search')

    if search:

        query = """
        SELECT * FROM books
        WHERE book_name LIKE %s
        OR author LIKE %s
        OR category LIKE %s
        """

        values = (
            "%" + search + "%",
            "%" + search + "%",
            "%" + search + "%"
        )

        cursor.execute(query, values)

    else:
        cursor.execute("SELECT * FROM books")

    all_books = cursor.fetchall()

    return render_template('books.html', books=all_books)


# Add Book
@app.route('/add_book', methods=['GET', 'POST'])
def add_book():

    if request.method == 'POST':

        book_name = request.form['book_name']
        author = request.form['author']
        category = request.form['category']
        quantity = request.form['quantity']

        query = """
        INSERT INTO books
        (book_name, author, category, quantity)
        VALUES (%s, %s, %s, %s)
        """

        values = (book_name, author, category, quantity)

        cursor.execute(query, values)

        db.commit()

        return redirect('/books')

    return render_template('add_book.html')


# Delete Book
@app.route('/delete_book/<int:id>')
def delete_book(id):

    query = "DELETE FROM books WHERE id=%s"

    values = (id,)

    cursor.execute(query, values)

    db.commit()

    return redirect('/books')


# Edit Book
@app.route('/edit_book/<int:id>', methods=['GET', 'POST'])
def edit_book(id):

    if request.method == 'POST':

        book_name = request.form['book_name']
        author = request.form['author']
        category = request.form['category']
        quantity = request.form['quantity']

        query = """
        UPDATE books
        SET book_name=%s,
            author=%s,
            category=%s,
            quantity=%s
        WHERE id=%s
        """

        values = (book_name, author, category, quantity, id)

        cursor.execute(query, values)

        db.commit()

        return redirect('/books')

    query = "SELECT * FROM books WHERE id=%s"

    values = (id,)

    cursor.execute(query, values)

    book = cursor.fetchone()

    return render_template('edit_book.html', book=book)
# Issue Book
@app.route('/issue_book', methods=['GET', 'POST'])
def issue_book():

    if request.method == 'POST':

        student_name = request.form['student_name']
        book_name = request.form['book_name']
        issue_date = request.form['issue_date']

        query = """
        INSERT INTO issued_books
        (student_name, book_name, issue_date, status)
        VALUES (%s, %s, %s, %s)
        """

        values = (student_name, book_name, issue_date, "Issued")

        cursor.execute(query, values)

        db.commit()

        return redirect('/issue_book')

    cursor.execute("SELECT * FROM issued_books")

    issued_data = cursor.fetchall()

    return render_template(
        'issue_book.html',
        issued_books=issued_data
    )

# Return Book

# Return Book
@app.route('/return_book/<int:id>')
def return_book(id):

    query = """
    UPDATE issued_books
    SET status=%s,
        return_date=CURDATE()
    WHERE id=%s
    """

    values = ("Returned", id)

    cursor.execute(query, values)

    db.commit()

    return redirect('/issue_book')


# Logout
@app.route('/logout')
def logout():

    session.pop('admin_logged_in', None)

    return redirect('/')


# Run App
if __name__ == '__main__':
    app.run(debug=True)


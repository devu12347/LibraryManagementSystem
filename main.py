import sqlite3
from datetime import datetime

conn = sqlite3.connect("library.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS Admin(
    username TEXT PRIMARY KEY,
    password TEXT
)
""")

conn.commit()
# Book Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Book(
    book_id INTEGER PRIMARY KEY,
    title TEXT,
    author TEXT,
    quantity INTEGER
)
""")

# Member Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Member(
    member_id INTEGER PRIMARY KEY,
    name TEXT,
    phone TEXT
)
""")

# Issue Book Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS IssueBook(
    issue_id INTEGER PRIMARY KEY,
    book_id INTEGER,
    member_id INTEGER,
    issue_date TEXT,
    return_date TEXT
)
""")

conn.commit()
cursor.execute(
    "INSERT OR IGNORE INTO Admin VALUES(?,?)",
    ("admin", "1234")
)

conn.commit()
username=input("enter the user name")
password=int(input("enter the password"))
cursor.execute(
    "SELECT * FROM Admin WHERE username=? AND password=?",
    (username, password)
)

admin = cursor.fetchone()

if admin:
    print("Login Successful")
else:
    print("Invalid Username or Password")
    conn.close()
    exit()
while True:

    print("\n===== LIBRARY MANAGEMENT SYSTEM =====")
    print("1. Add Book")
    print("2. View Books")
    print("3. Search Book")
    print("4. Update Quantity")
    print("5. Delete Book")
    print("6. Add Member")
    print("7. View Members")
    print("8. Search Member")
    print("9. Delete Member")
    print("10. Issue Book")
    print("11. Return Book")
    print("12. View Issued Books")
    print("13. Exit")

    choice = int(input("Enter Choice: "))

    # Add Book
    if choice == 1:

        book_id = int(input("Enter Book ID: "))
        title = input("Enter Title: ")
        author = input("Enter Author Name: ")
        quantity = int(input("Enter Quantity: "))

        cursor.execute(
            "INSERT INTO Book VALUES(?,?,?,?)",
            (book_id, title, author, quantity)
        )

        conn.commit()
        print("Book Added Successfully")

    # View Books
    elif choice == 2:

        cursor.execute("SELECT * FROM Book")
        books = cursor.fetchall()

        if books:
            for book in books:
                print(book)
        else:
            print("No Books Found")

    # Search Book
    elif choice == 3:

        book_id = int(input("Enter Book ID: "))

        cursor.execute(
            "SELECT * FROM Book WHERE book_id=?",
            (book_id,)
        )

        book = cursor.fetchone()

        if book:
            print(book)
        else:
            print("Book Not Found")

    # Update Quantity
    elif choice == 4:

        book_id = int(input("Enter Book ID: "))
        quantity = int(input("Enter New Quantity: "))

        cursor.execute(
            "UPDATE Book SET quantity=? WHERE book_id=?",
            (quantity, book_id)
        )

        conn.commit()
        print("Quantity Updated Successfully")

    # Delete Book
    elif choice == 5:

        book_id = int(input("Enter Book ID: "))

        cursor.execute(
            "DELETE FROM Book WHERE book_id=?",
            (book_id,)
        )

        conn.commit()
        print("Book Deleted Successfully")

    # Add Member
    elif choice == 6:

        member_id = int(input("Enter Member ID: "))
        name = input("Enter Member Name: ")
        phone = input("Enter Phone Number: ")

        cursor.execute(
            "INSERT INTO Member VALUES(?,?,?)",
            (member_id, name, phone)
        )

        conn.commit()
        print("Member Added Successfully")

    # View Members
    elif choice == 7:

        cursor.execute("SELECT * FROM Member")
        members = cursor.fetchall()

        if members:
            for member in members:
                print(member)
        else:
            print("No Members Found")

    # Search Member
    elif choice == 8:

        member_id = int(input("Enter Member ID: "))

        cursor.execute(
            "SELECT * FROM Member WHERE member_id=?",
            (member_id,)
        )

        member = cursor.fetchone()

        if member:
            print(member)
        else:
            print("Member Not Found")

    # Delete Member
    elif choice == 9:

        member_id = int(input("Enter Member ID: "))

        cursor.execute(
            "DELETE FROM Member WHERE member_id=?",
            (member_id,)
        )

        conn.commit()
        print("Member Deleted Successfully")

    # Issue Book
    elif choice == 10:

        issue_id = int(input("Enter Issue ID: "))
        book_id = int(input("Enter Book ID: "))
        member_id = int(input("Enter Member ID: "))
        issue_date = input("Enter Issue Date (DD-MM-YYYY): ")
        return_date = input("Enter Return Date (DD-MM-YYYY): ")

        cursor.execute(
            "SELECT quantity FROM Book WHERE book_id=?",
            (book_id,)
        )

        book = cursor.fetchone()

        if book and book[0] > 0:

            cursor.execute(
                "INSERT INTO IssueBook VALUES(?,?,?,?,?)",
                (issue_id, book_id, member_id,
                 issue_date, return_date)
            )

            cursor.execute(
                "UPDATE Book SET quantity=quantity-1 WHERE book_id=?",
                (book_id,)
            )

            conn.commit()
            print("Book Issued Successfully")

        else:
            print("Book Not Available")

    # Return Book
    elif choice == 11:

        issue_id = int(input("Enter Issue ID: "))

        cursor.execute(
            "SELECT book_id, return_date FROM IssueBook WHERE issue_id=?",
            (issue_id,)
        )

        record = cursor.fetchone()

        if record:

            book_id = record[0]
            expected_return_date = record[1]

            actual_return_date = input(
                "Enter Actual Return Date (DD-MM-YYYY): "
            )

            expected = datetime.strptime(
                expected_return_date,
                "%d-%m-%Y"
            )

            actual = datetime.strptime(
                actual_return_date,
                "%d-%m-%Y"
            )

            days_late = (actual - expected).days

            if days_late > 0:
                fine = days_late * 10
                print("Late by", days_late, "days")
                print("Fine Amount = ₹", fine)
            else:
                print("No Fine")

            cursor.execute(
                "DELETE FROM IssueBook WHERE issue_id=?",
                (issue_id,)
            )

            cursor.execute(
                "UPDATE Book SET quantity=quantity+1 WHERE book_id=?",
                (book_id,)
            )

            conn.commit()

            print("Book Returned Successfully")

        else:
            print("Issue Record Not Found")
    # View Issued Books
    elif choice == 12:

        cursor.execute("SELECT * FROM IssueBook")
        records = cursor.fetchall()

        if records:
            for record in records:
                print(record)
        else:
            print("No Books Issued")

    # Exit
    elif choice == 13:
        print("Thank You")
        break

    else:
        print("Invalid Choice")

conn.close()
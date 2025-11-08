from library_books import library_books
from datetime import datetime, timedelta

# -------- Level 1 --------
# TODO: Create a function to view all books that are currently available
# Output should include book ID, title, and author

def view_available_books(books):
    print("\nAvailable Books:")
    found_any = False
    for book in books:
        if book.available:
            print(f"{book.book_id}: {book.title} by {book.author}")
            found_any = True
    if not found_any:
        print("No books available right now.")


# -------- Level 2 --------
# TODO: Create a function to search books by author OR genre
# Search should be case-insensitive
# Return a list of matching books

def search_books(books, search_term):
    # Convert to lowercase for search
    search_term_lower = search_term.lower()
    
    # Find matching books - could probably optimize this but it works fine
    matching_books = []
    for book in books:
        if search_term_lower in book.author.lower() or search_term_lower in book.genre.lower():
            matching_books.append(book)

    print(f"\nSearch results for '{search_term}':")
    if len(matching_books) == 0:
        print("No matches found.")
    else:
        for book in matching_books:
            print(f"{book.book_id}: {book.title} by {book.author} ({book.genre})")
    
    return matching_books

# -------- Level 3 --------
# TODO: Create a function to checkout a book by ID
# If the book is available:
#   - Mark it unavailable
#   - Set the due_date to 2 weeks from today
#   - Increment the checkouts counter
# If it is not available:
#   - Print a message saying it's already checked out

def checkout_book(books, book_id):
    # Loop through books to find the one wanted
    for book in books:
        if book.book_id == book_id:
            book.checkout()  # Let the book handle its own checkout logic
            return
    # If not found, print this statement
    print("Book not found.")


# -------- Level 4 --------
# TODO: Create a function to return a book by ID
# Set its availability to True and clear the due_date

def return_book(books, book_id):
    for book in books:
        if book.book_id == book_id:
            book.return_book()  # Delegate to the book object
            return
    print("Book not found.")


# TODO: Create a function to list all overdue books
# A book is overdue if its due_date is before today AND it is still checked out

def list_overdue_books(books):
    print("\nOverdue Books:")
    overdue_books = []
    
    # Find all overdue books
    for book in books:
        if book.is_overdue():
            overdue_books.append(book)
    
    if len(overdue_books) == 0:
        print("No overdue books.")
    else:
        for book in overdue_books:
            print(f"{book.book_id}: {book.title} (due {book.due_date.date()})")


# -------- Level 5 --------
# TODO: Convert your data into a Book class with methods like checkout() and return_book()
# TODO: Add a simple menu that allows the user to choose different options like view, search, checkout, return, etc.

class Book:
    def __init__(self, book_id, title, author, genre, available=True, checkouts=0, due_date=None):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.genre = genre
        self.available = available
        self.checkouts = checkouts
        
        # Handle due_date conversion, sometimes it comes as a string
        if isinstance(due_date, str):
            self.due_date = datetime.strptime(due_date, "%Y-%m-%d") # Stack Overflow - isinstance and strptime
        else:
            self.due_date = due_date

    def checkout(self):
        if not self.available:
            print(f"'{self.title}' is already checked out.")
        else:
            self.available = False
            # Set due date to 2 weeks from now
            self.due_date = datetime.now() + timedelta(weeks=2)
            self.checkouts += 1
            print(f"You checked out '{self.title}'. Due on {self.due_date.date()}.")

    def return_book(self):
        if self.available:
            print(f"'{self.title}' wasn't checked out.")
        else:
            self.available = True
            self.due_date = None  # Clear the due date
            print(f"'{self.title}' has been returned. Thanks!")

    def is_overdue(self):
        # Book is overdue if it's checked out and past the due date
        return (not self.available) and self.due_date and self.due_date < datetime.now()


# Initialize book collection from the imported data
books = []
for book_data in library_books:
    book_data['book_id'] = book_data.pop('id') # Stack Overflow - pop extension
    books.append(Book(**book_data)) # ** is used to unpack the dictionary


# -------- Optional Advanced Features --------
# You can implement these to move into Tier 4:
# - Add a new book (via input) to the catalog
# - Sort and display the top 3 most checked-out books
# - Partial title/author search
# - Save/load catalog to file (CSV or JSON)
# - Anything else you want to build on top of the system!

def menu():
    while True:
        print("\n--- Library System ---")
        print("1. View Available Books")
        print("2. Search Books")
        print("3. Checkout Book")
        print("4. Return Book")
        print("5. View Overdue Books")
        print("6. Exit")

        user_choice = input("Choose an option (1-6): ").strip()

        # Conditionals based on option chosen by user
        if user_choice == "1":
            view_available_books(books)
        elif user_choice == "2":
            search_term = input("Enter author or genre to search: ")
            search_books(books, search_term)
        elif user_choice == "3":
            book_id = input("Enter book ID to checkout: ").upper()  # Convert to uppercase for consistency
            checkout_book(books, book_id)
        elif user_choice == "4":
            book_id = input("Enter book ID to return: ").upper()
            return_book(books, book_id)
        elif user_choice == "5":
            list_overdue_books(books)
        elif user_choice == "6":
            print("Thanks for using the library system. See you later!")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    menu()

mport json
import os
class Book:
    def __init__(self, book_id, title, author, year):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.year = year
        self.is_issued = False
    def to_dict(self):
        """Convert book object to dictionary for JSON storage"""
        return {
            'book_id': self.book_id,
            'title': self.title,
            'author': self.author,
            'year': self.year,
            'is_issued': self.is_issued
        }
        
    @staticmethod
    def from_dict(data):
        """Create book object from dictionary"""
        book = Book(data['book_id'], data['title'], data['author'], data['year'])
        book.is_issued = data['is_issued']
        return book
    
    def __str__(self):
        status = "Issued" if self.is_issued else "Available"
        return f"ID: {self.book_id} | {self.title} by {self.author} ({self.year}) - {status}"


class Library:
    def __init__(self, filename='library_data.json'):
        self.books = []
        self.filename = filename
        self.next_book_id = 121
        self.load_data() 
    
    def save_data(self):
        """Save library data to JSON file"""
        data = {
            'next_book_id': self.next_book_id,
            'books': [book.to_dict() for book in self.books]
        }
        try:
            with open(self.filename, 'w') as f:
                json.dump(data, f, indent=4)
            print("✓ Data saved successfully")
        except Exception as e:
            print(f"Error saving data: {e}")
    
    def load_data(self):
        """Load library data from JSON file"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    data = json.load(f)
                    self.next_book_id = data.get('next_book_id', 121)
          
                    self.books = [Book.from_dict(book_data) for book_data in data.get('books', [])]
                print(f"✓ Loaded {len(self.books)} books from file")
            except Exception as e:
                print(f"Error loading data: {e}")
                self.initialize_sample_books()
        else:
            print("No existing data found. Starting fresh...")
            self.initialize_sample_books()
    
    def initialize_sample_books(self):
        """Add sample books for first-time users"""
        self.add_book("The Great Gatsby", "F. Scott Fitzgerald", 1925, save=False)
        self.add_book("To Kill a Mockingbird", "Harper Lee", 1960, save=False)
        self.add_book("1984", "George Orwell", 1949, save=False)
        self.add_book("Pride and Prejudice", "Jane Austen", 1813, save=False)
        self.add_book("The Catcher in the Rye", "J.D. Salinger", 1951, save=False)
        self.save_data()
        print("Sample books added!")
    def add_book(self, title, author, year, save=True):
        book_id = self.next_book_id
        book = Book(book_id, title, author, year)
        self.books.append(book)
        self.next_book_id += 1
        print(f"Book added: {title} (ID: {book_id})")
        if save:
            self.save_data()
    def edit_book(self, book_id):
        """Edit book details"""
        book = self.binary_search_by_id(book_id)
        if not book:
            print("Book not found")
            return
        
        print(f"\nCurrent details: {book}")
        print("\nWhat would you like to edit?")
        print("1. Title")
        print("2. Author")
        print("3. Year")
        print("4. All details")
        print("5. Cancel")
        
        choice = input("Enter choice: ")
        
        if choice == '1':
            new_title = input(f"Enter new title (current: {book.title}): ")
            if new_title:
                book.title = new_title
                print("Title updated!")
        elif choice == '2':
            new_author = input(f"Enter new author (current: {book.author}): ")
            if new_author:
                book.author = new_author
                print("Author updated!")
        elif choice == '3':
            new_year = input(f"Enter new year (current: {book.year}): ")
            if new_year:
                book.year = int(new_year)
                print("Year updated!")
        elif choice == '4':
            new_title = input(f"Enter new title (current: {book.title}): ")
            new_author = input(f"Enter new author (current: {book.author}): ")
            new_year = input(f"Enter new year (current: {book.year}): ")
            if new_title:
                book.title = new_title
            if new_author:
                book.author = new_author
            if new_year:
                book.year = int(new_year)
            print("All details updated!")
        elif choice == '5':
            print("Edit cancelled")
            return
        else:
            print("Invalid choice")
            return
        
        self.save_data()
        print(f"Updated: {book}")
    
    def delete_book(self, book_id):
        """Delete a book from library"""
        book = self.binary_search_by_id(book_id)
        if book:
            confirm = input(f"Are you sure you want to delete '{book.title}'? (yes/no): ")
            if confirm.lower() == 'yes':
                self.books.remove(book)
                print(f"Book deleted: {book.title}")
                self.save_data()
            else:
                print("Deletion cancelled")
        else:
            print("Book not found")
    
    def display_books(self):
        if not self.books:
            print("No books in library")
            return
        print("\n--- All Books ---")
        for book in self.books:
            print(book)
    
    def binary_search_by_id(self, book_id):
        sorted_books = sorted(self.books, key=lambda x: x.book_id)
        left, right = 0, len(sorted_books) - 1
        
        while left <= right:
            mid = (left + right) // 2
            if sorted_books[mid].book_id == book_id:
                return sorted_books[mid]
            elif sorted_books[mid].book_id < book_id:
                left = mid + 1
            else:
                right = mid - 1
        return None
    
    def search_by_title(self, title):
        results = []
        for book in self.books:
            if title.lower() in book.title.lower():
                results.append(book)
        return results
    
    def search_by_author(self, author):
        results = []
        for book in self.books:
            if author.lower() in book.author.lower():
                results.append(book)
        return results
    
    def sort_by_title(self):
        self.books.sort(key=lambda x: x.title.lower())
        print("Books sorted by title")
    
    def sort_by_author(self):
        self.books.sort(key=lambda x: x.author.lower())
        print("Books sorted by author")
    
    def sort_by_year(self):
        self.books.sort(key=lambda x: x.year)
        print("Books sorted by year")
    
    def issue_book(self, book_id):
        book = self.binary_search_by_id(book_id)
        if book:
            if not book.is_issued:
                book.is_issued = True
                print(f"Book issued: {book.title}")
                self.save_data()
            else:
                print("Book is already issued")
        else:
            print("Book not found")
    
    def return_book(self, book_id):
        book = self.binary_search_by_id(book_id)
        if book:
            if book.is_issued:
                book.is_issued = False
                print(f"Book returned: {book.title}")
                self.save_data()
            else:
                print("Book was not issued")
        else:
            print("Book not found")


def main():
    library = Library()
    
    while True:
        print("\n=== Library Management System ===")
        print("1. Display all books")
        print("2. Add a book")
        print("3. Edit a book")
        print("4. Delete a book")
        print("5. Search book by ID")
        print("6. Search books by title")
        print("7. Search books by author")
        print("8. Sort books by title")
        print("9. Sort books by author")
        print("10. Sort books by year")
        print("11. Issue a book")
        print("12. Return a book")
        print("13. Exit")
        
        choice = input("\nEnter your choice: ")
        
        if choice == '1':
            library.display_books()
        
        elif choice == '2':
            title = input("Enter title: ")
            author = input("Enter author: ")
            year = int(input("Enter year: "))
            library.add_book(title, author, year)
        
        elif choice == '3':
            book_id = int(input("Enter book ID to edit: "))
            library.edit_book(book_id)
        
        elif choice == '4':
            book_id = int(input("Enter book ID to delete: "))
            library.delete_book(book_id)
        
        elif choice == '5':
            book_id = int(input("Enter book ID to search: "))
            book = library.binary_search_by_id(book_id)
            if book:
                print(f"\nFound: {book}")
            else:
                print("Book not found")
        
        elif choice == '6':
            title = input("Enter title to search: ")
            results = library.search_by_title(title)
            if results:
                print("\n--- Search Results ---")
                for book in results:
                    print(book)
            else:
                print("No books found")
        
        elif choice == '7':
            author = input("Enter author to search: ")
            results = library.search_by_author(author)
            if results:
                print("\n--- Search Results ---")
                for book in results:
                    print(book)
            else:
                print("No books found")
        
        elif choice == '8':
            library.sort_by_title()
            library.display_books()
        
        elif choice == '9':
            library.sort_by_author()
            library.display_books()
        
        elif choice == '10':
            library.sort_by_year()
            library.display_books()
        
        elif choice == '11':
            book_id = int(input("Enter book ID to issue: "))
            library.issue_book(book_id)
        
        elif choice == '12':
            book_id = int(input("Enter book ID to return: "))
            library.return_book(book_id)
        
        elif choice == '13':
            print("Thank you for using the Library Management System!")
            break
        
        else:
            print("Invalid choice! Please try again.")


if __name__ == "__main__":
    main()

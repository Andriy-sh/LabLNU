export interface Book {
  id: number;
  title: string;
  publication_year: number;
  isbn: string;
  copies_available: number;
  authors: Author[];
  categories: Category[];
  borrowed_records: BorrowedBook[];
}

export interface Author {
  id: number;
  first_name: string;
  last_name: string;
  biography: string;
  books: Book[];
}

export interface Category {
  id: number;
  name: string;
  description: string;
  books: Book[];
}

export interface User {
  id: number;
  first_name: string;
  last_name: string;
  email: string;
  registration_date: string;
  borrowed_books: BorrowedBook[];
}

export interface BorrowedBook {
  id: number;
  user_id: number;
  book_id: number;
  borrow_date: string;
  due_date: string;
  returned_date: string | null;
  user: User;
  book: Book;
}

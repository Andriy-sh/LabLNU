export interface BookCreate {
  title: string;
  publication_year: number;
  isbn: string;
  copies_available: number;
  author_ids: number[];
  category_ids: number[];
}

export interface AuthorCreate {
  first_name: string;
  last_name: string;
  biography: string;
}

export interface CategoryCreate {
  name: string;
  description: string;
}

export interface UserCreate {
  first_name: string;
  last_name: string;
  email: string;
}

export interface BorrowedBookCreate {
  user_id: number;
  book_id: number;
  due_date: string;
}
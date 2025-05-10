import { Author, Book, Category } from "./entities";

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  size: number;
  pages: number;
}

export interface ApiError {
  detail: string;
  status_code: number;
}

export interface Statistics {
  popular_books: {
    book: Book;
    borrow_count: number;
  }[];
  popular_authors: {
    author: Author;
    borrow_count: number;
  }[];
  popular_categories: {
    category: Category;
    borrow_count: number;
  }[];
}

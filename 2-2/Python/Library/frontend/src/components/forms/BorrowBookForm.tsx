"use client";

import { Book, User } from "@/types/entities";
import { useState, useEffect } from "react";
import axios from "axios";

export interface BorrowBookFormData {
  user_id: number;
  book_id: number;
  due_date: string;
}

interface BorrowBookFormProps {
  onSubmit: (data: BorrowBookFormData) => void;
}

export default function BorrowBookForm({ onSubmit }: BorrowBookFormProps) {
  const [formData, setFormData] = useState<BorrowBookFormData>({
    user_id: 0,
    book_id: 0,
    due_date: "",
  });

  const [books, setBooks] = useState<Book[]>([]);
  const [users, setUsers] = useState<User[]>([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [booksRes, usersRes] = await Promise.all([
          axios.get("http://localhost:/books/"),
          axios.get("http://localhost:/users/"),
        ]);
        console.log(booksRes.data);
        console.log(usersRes.data);
        setBooks(booksRes.data);
        setUsers(usersRes.data);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };
    fetchData();
  }, []);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4 max-w-lg mx-auto p-4">
      <div>
        <label
          htmlFor="book_id"
          className="block text-sm font-medium text-gray-700"
        >
          Book
        </label>
        <select
          id="book_id"
          value={formData.book_id}
          onChange={(e) =>
            setFormData({ ...formData, book_id: Number(e.target.value) })
          }
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
          required
        >
          <option value="">Select a book</option>
          {books.map((book) => (
            <option
              key={book.id}
              value={book.id}
              disabled={book.copies_available <= 0}
            >
              {book.title}
            </option>
          ))}
        </select>
      </div>

      <div>
        <label
          htmlFor="user_id"
          className="block text-sm font-medium text-gray-700"
        >
          User
        </label>
        <select
          id="user_id"
          value={formData.user_id}
          onChange={(e) =>
            setFormData({ ...formData, user_id: Number(e.target.value) })
          }
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
          required
        >
          <option value="">Select a user</option>
          {users.map((user) => (
            <option key={user.id} value={user.id}>
              {`${user.first_name} ${user.last_name}`}
            </option>
          ))}
        </select>
      </div>

      <div>
        <label
          htmlFor="due_date"
          className="block text-sm font-medium text-gray-700"
        >
          Due Date
        </label>
        <input
          type="date"
          id="due_date"
          value={formData.due_date}
          onChange={(e) =>
            setFormData({ ...formData, due_date: e.target.value })
          }
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
          required
          min={new Date().toISOString().split("T")[0]}
        />
      </div>

      <button
        type="submit"
        className="w-full bg-indigo-600 text-white px-4 py-2 rounded-md hover:bg-indigo-700"
      >
        Borrow Book
      </button>
    </form>
  );
}

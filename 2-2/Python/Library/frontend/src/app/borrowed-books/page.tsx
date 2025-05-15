"use client";

import { useState, useEffect } from "react";
import BorrowBookForm, {
  BorrowBookFormData,
} from "@/components/forms/BorrowBookForm";
import { Book, User } from "@/types/entities";

interface BorrowedBook {
  id: number;
  book_id: number;
  user_id: number;
  borrowed_date: string;
  due_date: string;
  returned_date: string | null;
}

export default function BorrowedBooks() {
  const [activeLoans, setActiveLoans] = useState<BorrowedBook[]>([]);
  const [allLoans, setAllLoans] = useState<BorrowedBook[]>([]);
  const [showAllLoans, setShowAllLoans] = useState(false);
  const [books, setBooks] = useState<Record<number, Book>>({});
  const [users, setUsers] = useState<Record<number, User>>({});

  const fetchData = async () => {
    try {
      const [loansRes, allLoansRes, booksRes, usersRes] = await Promise.all([
        fetch("http://localhost:/borrowed-books/active"),
        fetch("http://localhost:/borrowed-books/"),
        fetch("http://localhost:/books/"),
        fetch("http://localhost:/users/"),
      ]);

      const [loansData, allLoansData, booksData, usersData] = await Promise.all(
        [loansRes.json(), allLoansRes.json(), booksRes.json(), usersRes.json()]
      );

      const booksLookup = booksData.reduce((acc: any, book: Book) => {
        acc[book.id] = book;
        return acc;
      }, {});

      const usersLookup = usersData.reduce((acc: any, user: User) => {
        acc[user.id] = user;
        return acc;
      }, {});

      setBooks(booksLookup);
      setUsers(usersLookup);
      setActiveLoans(loansData);
      setAllLoans(allLoansData);
    } catch (error) {
      console.error("Error fetching data:", error);
      setActiveLoans([]);
      setAllLoans([]);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);
  const [showForm, setShowForm] = useState(false);

  const fetchActiveLoans = async () => {
    try {
      const response = await fetch(
        "http://localhost:/borrowed-books/active"
      );
      const data = await response.json();
      console.log("Active Loans Data:", data); 
      setActiveLoans(data);
    } catch (error) {
      console.error("Error fetching active loans:", error);
      setActiveLoans([]); 
    }
  };

  useEffect(() => {
    fetchActiveLoans();
  }, []);
  console.log("Active Loans:", activeLoans); 
  const handleBorrow = async (borrowData: BorrowBookFormData) => {
    try {
      const bookResponse = await fetch(
        `http://localhost:/books/${borrowData.book_id}`
      );
      const bookData = await bookResponse.json();

      const updateBookResponse = await fetch(
        `http://localhost:/books/${borrowData.book_id}`,
        {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            title: bookData.title,
            isbn: bookData.isbn,
            publication_year: bookData.publication_year,
            copies_available: bookData.copies_available - 1,
            author_ids: (bookData.authors || []).map(
              (author: any) => author.id
            ),
            category_ids: (bookData.categories || []).map(
              (category: any) => category.id
            ),
          }),
        }
      );

      if (!updateBookResponse.ok) {
        const errorData = await updateBookResponse.json();
        throw new Error(errorData.detail || "Failed to update book copies");
      }

      const response = await fetch("http://localhost:/borrowed-books/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(borrowData),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Failed to borrow book");
      }

      setShowForm(false);
      fetchData();
    } catch (error) {
      console.error("Error borrowing book:", error);
      alert(error instanceof Error ? error.message : "Failed to borrow book");
    }
  };


  const handleReturn = async (borrowedBookId: number) => {
    try {
      const borrowedResponse = await fetch(
        `http://localhost:/borrowed-books/${borrowedBookId}`
      );
      const borrowedData = await borrowedResponse.json();

      const bookResponse = await fetch(
        `http://localhost:/books/${borrowedData.book_id}`
      );
      const bookData = await bookResponse.json();

      const updateBookResponse = await fetch(
        `http://localhost:/books/${borrowedData.book_id}`,
        {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            title: bookData.title,
            isbn: bookData.isbn,
            publication_year: bookData.publication_year,
            copies_available: bookData.copies_available + 1,
            author_ids: (bookData.authors || []).map(
              (author: any) => author.id
            ),
            category_ids: (bookData.categories || []).map(
              (category: any) => category.id
            ),
          }),
        }
      );

      if (!updateBookResponse.ok) {
        const errorData = await updateBookResponse.json();
        throw new Error(errorData.detail || "Failed to update book copies");
      }

      const response = await fetch(
        `http://localhost:/borrowed-books/${borrowedBookId}/return`,
        {
          method: "POST",
        }
      );

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Failed to return book");
      }

      fetchData();
    } catch (error) {
      console.error("Error returning book:", error);
      alert(error instanceof Error ? error.message : "Failed to return book");
    }
  };

  return (
    <div className="container mx-auto py-8 px-4">
      <div className="flex justify-between items-center mb-6">
        <div className="flex items-center gap-4">
          <h1 className="text-2xl font-bold">Borrowed Books</h1>
          <div className="flex items-center gap-2">
            <label className="inline-flex items-center">
              <input
                type="checkbox"
                checked={showAllLoans}
                onChange={(e) => setShowAllLoans(e.target.checked)}
                className="form-checkbox h-5 w-5 text-indigo-600"
              />
              <span className="ml-2 text-gray-700">Show all loans</span>
            </label>
          </div>
        </div>
        <button
          onClick={() => setShowForm(!showForm)}
          className="bg-indigo-600 text-white px-4 py-2 rounded-md hover:bg-indigo-700"
        >
          {showForm ? "Cancel" : "Borrow Book"}
        </button>
      </div>

      {showForm && (
        <div className="mb-8">
          <BorrowBookForm onSubmit={handleBorrow} />
        </div>
      )}

      <div className="bg-white shadow-md rounded-lg overflow-hidden">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Book
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                User
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Borrow Date
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Due Date
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Actions
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {Array.isArray(showAllLoans ? allLoans : activeLoans) &&
            (showAllLoans ? allLoans : activeLoans).length > 0 ? (
              (showAllLoans ? allLoans : activeLoans).map((loan) => (
                <tr
                  key={loan.id}
                  className={loan.returned_date ? "bg-gray-50" : ""}
                >
                  <td className="px-6 py-4 whitespace-nowrap">
                    {books[loan.book_id]?.title || "Loading..."}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    {users[loan.user_id]
                      ? `${users[loan.user_id].first_name} ${
                          users[loan.user_id].last_name
                        }`
                      : "Loading..."}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    {new Date(loan.borrowed_date).toLocaleDateString()}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    {new Date(loan.due_date).toLocaleDateString()}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    {!loan.returned_date ? (
                      <button
                        onClick={() => handleReturn(loan.id)}
                        className="text-indigo-600 hover:text-indigo-900"
                      >
                        Return
                      </button>
                    ) : (
                      <span className="text-green-600">
                        Returned on{" "}
                        {new Date(loan.returned_date).toLocaleDateString()}
                      </span>
                    )}
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan={5} className="px-6 py-4 text-center text-gray-500">
                  No {showAllLoans ? "" : "active"} loans found
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

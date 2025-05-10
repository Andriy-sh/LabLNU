"use client";

import axios from "axios";
import Link from "next/link";
import { useEffect, useState } from "react";

interface Book {
  id: number;
  title: string;
  publication_year: number;
  isbn: string;
  copies_available: number;
  authors: { id: number; first_name: string; last_name: string }[];
  categories: { id: number; name: string }[];
}

const gradients = [
  "from-indigo-500 to-purple-500",
  "from-rose-400 to-red-500",
  "from-green-400 to-emerald-500",
  "from-blue-400 to-cyan-500",
  "from-yellow-400 to-orange-500",
  "from-pink-400 to-fuchsia-500",
];

export default function Home() {
  const [book, setBook] = useState<Book[]>([]);
  const [filteredBooks, setFilteredBooks] = useState<Book[]>([]);
  const [searchTitle, setSearchTitle] = useState("");
  const [selectedAuthor, setSelectedAuthor] = useState("");
  const [selectedCategory, setSelectedCategory] = useState("");
  const [authors, setAuthors] = useState<
    { id: number; first_name: string; last_name: string }[]
  >([]);
  const [categories, setCategories] = useState<{ id: number; name: string }[]>(
    []
  );

  const fetchBooks = async () => {
    try {
      const booksRes = await axios.get("http://localhost:8000/books");
      const booksData = await Promise.all(
        booksRes.data.map(async (book: Book) => {
          const [authorsRes, categoriesRes] = await Promise.all([
            axios.get(
              `http://localhost:8000/associations/book/${book.id}/authors`
            ),
            axios.get(
              `http://localhost:8000/associations/book/${book.id}/categories`
            ),
          ]);

          return {
            ...book,
            authors: authorsRes.data,
            categories: categoriesRes.data,
          };
        })
      );

      setBook(booksData);
      setFilteredBooks(booksData);
    } catch (error) {
      console.error("Error fetching books:", error);
      setBook([]);
      setFilteredBooks([]);
    }
  };

  const fetchFilters = async () => {
    try {
      const [authorsRes, categoriesRes] = await Promise.all([
        axios.get("http://localhost:8000/authors"),
        axios.get("http://localhost:8000/categories"),
      ]);
      setAuthors(authorsRes.data);
      setCategories(categoriesRes.data);
    } catch (error) {
      console.error("Error fetching filters:", error);
    }
  };

  useEffect(() => {
    fetchBooks();
    fetchFilters();
  }, []);

  useEffect(() => {
    let result = [...book];

    if (searchTitle) {
      result = result.filter((book) =>
        book.title.toLowerCase().includes(searchTitle.toLowerCase())
      );
    }

    if (selectedAuthor) {
      result = result.filter((book) =>
        book.authors?.some(
          (author) =>
            `${author.first_name} ${author.last_name}` === selectedAuthor
        )
      );
    }

    if (selectedCategory) {
      result = result.filter((book) =>
        book.categories?.some((category) => category.name === selectedCategory)
      );
    }

    setFilteredBooks(result);
  }, [book, searchTitle, selectedAuthor, selectedCategory]);

  const handleDelete = async (e: React.MouseEvent, bookId: number) => {
    e.preventDefault();
    try {
      await axios.delete(`http://localhost:8000/books/${bookId}`, {
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
        },
      });
      fetchBooks();
    } catch (error) {
      console.error("Error deleting book:", error);
      alert("Failed to delete book");
    }
  };

  // Генерує псевдовипадковий індекс для градієнта на основі book.id
  const getGradientClass = (id: number) => {
    const gradient = gradients[id % gradients.length];
    return `bg-gradient-to-br ${gradient}`;
  };

  return (
    <div className="max-w-7xl mx-auto py-12 px-6">
      <div className="mb-8 space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <input
            type="text"
            placeholder="Search by title..."
            value={searchTitle}
            onChange={(e) => setSearchTitle(e.target.value)}
            className="p-2 border rounded-md"
          />
          <select
            value={selectedAuthor}
            onChange={(e) => setSelectedAuthor(e.target.value)}
            className="p-2 border rounded-md"
          >
            <option value="">All Authors</option>
            {authors.map((author) => (
              <option
                key={author.id}
                value={`${author.first_name} ${author.last_name}`}
              >
                {author.first_name} {author.last_name}
              </option>
            ))}
          </select>
          <select
            value={selectedCategory}
            onChange={(e) => setSelectedCategory(e.target.value)}
            className="p-2 border rounded-md"
          >
            <option value="">All Categories</option>
            {categories.map((category) => (
              <option key={category.id} value={category.name}>
                {category.name}
              </option>
            ))}
          </select>
        </div>
      </div>

      <div className="grid gap-10 grid-cols-1 sm:grid-cols-2 lg:grid-cols-3">
        {filteredBooks.map((book) => (
          <Link key={book.id} href={`/books/${book.id}`}>
            <div className="relative bg-white rounded-3xl shadow-lg overflow-hidden border border-gray-200 hover:shadow-2xl transition-all duration-300 p-6">
              <button
                onClick={(e) => handleDelete(e, book.id)}
                className="absolute top-4 right-4 text-gray-400 hover:text-red-500 transition-colors"
              >
                ✕
              </button>
              <div className="flex justify-center mb-6">
                <div
                  className={`w-32 h-48 ${getGradientClass(
                    book.id
                  )} rounded-xl shadow-md flex items-center justify-center`}
                >
                  <span className="text-white text-xl font-bold opacity-60">
                    📖
                  </span>
                </div>
              </div>

              <h3 className="text-2xl font-bold text-gray-800 mb-3 text-center">
                {book.title}
              </h3>
              <ul className="text-gray-700 text-base font-medium space-y-1 text-center">
                <li>
                  👥 <span className="text-gray-900">Authors:</span>{" "}
                  {book.authors
                    ?.map(
                      (author) => `${author.first_name} ${author.last_name}`
                    )
                    .join(", ") || "No authors listed"}
                </li>
                <li>
                  📚 <span className="text-gray-900">Categories:</span>{" "}
                  {book.categories
                    ?.map((category) => category.name)
                    .join(", ") || "Uncategorized"}
                </li>
                <li>
                  📅 <span className="text-gray-900">Published:</span>{" "}
                  {book.publication_year}
                </li>
                <li>
                  🔢 <span className="text-gray-900">ISBN:</span> {book.isbn}
                </li>
                <li>
                  ✅ <span className="text-gray-900">Available:</span>{" "}
                  {book.copies_available}{" "}
                  {book.copies_available === 1 ? "copy" : "copies"}
                </li>
              </ul>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}

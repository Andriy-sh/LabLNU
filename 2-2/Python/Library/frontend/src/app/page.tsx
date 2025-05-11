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
  "from-purple-600 to-blue-500",
  "from-emerald-500 to-teal-400",
  "from-rose-500 to-orange-400",
  "from-amber-500 to-yellow-400",
  "from-indigo-500 to-blue-400",
  "from-pink-500 to-rose-400",
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

  const getGradientClass = (id: number) => {
    const gradient = gradients[id % gradients.length];
    return `bg-gradient-to-br ${gradient}`;
  };

  return (
    <div className="max-w-6xl mx-auto py-12 px-6">
      <div className="mb-12 space-y-6">
        <h1 className="text-4xl font-bold text-gray-800 text-center mb-8">
          Library Collection
        </h1>
        <div className=" grid grid-cols-3 gap-6">
          <input
            type="text"
            placeholder="Search by title..."
            value={searchTitle}
            onChange={(e) => setSearchTitle(e.target.value)}
            className="p-4 border-2 rounded-xl bg-white shadow-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all"
          />
          <select
            value={selectedAuthor}
            onChange={(e) => setSelectedAuthor(e.target.value)}
            className="p-4 border-2 rounded-xl bg-white shadow-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all"
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
            className="p-4 border-2 rounded-xl bg-white shadow-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all"
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

      <div className="grid gap-8 grid-cols-1 md:grid-cols-2">
        {filteredBooks.map((book) => (
          <Link key={book.id} href={`/books/${book.id}`}>
            <div className="bg-white rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 overflow-hidden">
              <div className={`${getGradientClass(book.id)} h-32 relative`}>
                <button
                  onClick={(e) => handleDelete(e, book.id)}
                  className="absolute top-4 right-4 bg-white/20 backdrop-blur-sm p-2 rounded-full hover:bg-white/40 transition-all"
                >
                  <span className="text-white">✕</span>
                </button>
              </div>

              <div className="p-6">
                <h3 className="text-2xl font-bold text-gray-800 mb-4">
                  {book.title}
                </h3>

                <div className="space-y-4">
                  <div className="flex flex-wrap gap-2">
                    {book.authors?.map((author, idx) => (
                      <div
                        key={author.id}
                        className="flex items-center bg-gray-100 rounded-full px-4 py-2"
                      >
                        <div className="w-8 h-8 rounded-full bg-gradient-to-br from-blue-500 to-purple-500 flex items-center justify-center text-white text-sm font-bold mr-2">
                          {author.first_name[0]}
                          {author.last_name[0]}
                        </div>
                        <span className="text-sm font-medium">
                          {author.first_name} {author.last_name}
                        </span>
                      </div>
                    ))}
                  </div>

                  <div className="flex flex-wrap gap-2">
                    {book.categories?.map((category) => (
                      <span
                        key={category.id}
                        className="px-3 py-1 bg-gray-100 rounded-full text-sm font-medium text-gray-600"
                      >
                        {category.name}
                      </span>
                    ))}
                  </div>

                  <div className="grid grid-cols-2 gap-4 mt-4">
                    <div className="text-sm">
                      <span className="block text-gray-500">Published</span>
                      <span className="font-medium">
                        {book.publication_year}
                      </span>
                    </div>
                    <div className="text-sm">
                      <span className="block text-gray-500">ISBN</span>
                      <span className="font-medium">{book.isbn}</span>
                    </div>
                    <div className="text-sm col-span-2">
                      <span className="block text-gray-500">
                        Available Copies
                      </span>
                      <span className="font-medium">
                        {book.copies_available}{" "}
                        {book.copies_available === 1 ? "copy" : "copies"}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}

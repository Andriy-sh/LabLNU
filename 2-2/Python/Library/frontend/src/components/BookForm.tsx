"use client";
import { useState, useEffect } from "react";
import { Author, Category } from "@/types/entities";

interface BookFormData {
  title: string;
  publication_year: number;
  isbn: string;
  copies_available: number;
  author_ids: number[];
  category_ids: number[];
}

interface BookFormProps {
  onSubmit: (data: BookFormData) => void;
}

export default function BookForm({ onSubmit }: BookFormProps) {
  const [formData, setFormData] = useState({
    title: "",
    publication_year: new Date().getFullYear(),
    isbn: "",
    copies_available: 1,
    author_ids: [] as number[],
    category_ids: [] as number[],
  });

  const [authors, setAuthors] = useState<Author[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [authorsRes, categoriesRes] = await Promise.all([
          fetch("http://localhost:/authors/"),
          fetch("http://localhost:/categories/"),
        ]);
        const [authorsData, categoriesData] = await Promise.all([
          authorsRes.json(),
          categoriesRes.json(),
        ]);
        setAuthors(authorsData);
        setCategories(categoriesData);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };
    fetchData();
  }, []);

  const handleAuthorChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const selectedOptions = Array.from(e.target.selectedOptions, (option) =>
      Number(option.value)
    );
    setFormData({ ...formData, author_ids: selectedOptions });
  };

  const handleCategoryChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const selectedOptions = Array.from(e.target.selectedOptions, (option) =>
      Number(option.value)
    );
    setFormData({ ...formData, category_ids: selectedOptions });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4 max-w-lg mx-auto">
      <div>
        <label
          htmlFor="title"
          className="block text-sm font-medium text-gray-700"
        >
          Title
        </label>
        <input
          type="text"
          id="title"
          value={formData.title}
          onChange={(e) => setFormData({ ...formData, title: e.target.value })}
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
          required
        />
      </div>

      <div>
        <label
          htmlFor="authors"
          className="block text-sm font-medium text-gray-700"
        >
          Authors
        </label>
        <select
          id="authors"
          multiple
          value={formData.author_ids}
          onChange={handleAuthorChange}
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
          required
          size={4}
        >
          {authors.map((author) => (
            <option key={author.id} value={author.id}>
              {`${author.first_name} ${author.last_name}`}
            </option>
          ))}
        </select>
        <p className="text-sm text-gray-500 mt-1">
          Hold Ctrl/Cmd to select multiple authors
        </p>
      </div>

      <div>
        <label
          htmlFor="categories"
          className="block text-sm font-medium text-gray-700"
        >
          Categories
        </label>
        <select
          id="categories"
          multiple
          value={formData.category_ids}
          onChange={handleCategoryChange}
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
          required
          size={4}
        >
          {categories.map((category) => (
            <option key={category.id} value={category.id}>
              {category.name}
            </option>
          ))}
        </select>
        <p className="text-sm text-gray-500 mt-1">
          Hold Ctrl/Cmd to select multiple categories
        </p>
      </div>

      <div>
        <label
          htmlFor="publication_year"
          className="block text-sm font-medium text-gray-700"
        >
          Publication Year
        </label>
        <input
          type="number"
          id="publication_year"
          value={formData.publication_year}
          onChange={(e) =>
            setFormData({
              ...formData,
              publication_year: parseInt(e.target.value),
            })
          }
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
          required
        />
      </div>

      <div>
        <label
          htmlFor="isbn"
          className="block text-sm font-medium text-gray-700"
        >
          ISBN
        </label>
        <input
          type="text"
          id="isbn"
          value={formData.isbn}
          onChange={(e) => setFormData({ ...formData, isbn: e.target.value })}
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
          required
        />
      </div>

      <div>
        <label
          htmlFor="copies_available"
          className="block text-sm font-medium text-gray-700"
        >
          Copies Available
        </label>
        <input
          type="number"
          id="copies_available"
          value={formData.copies_available}
          onChange={(e) =>
            setFormData({
              ...formData,
              copies_available: parseInt(e.target.value),
            })
          }
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
          required
        />
      </div>

      <button
        type="submit"
        className="w-full bg-indigo-600 text-white px-4 py-2 rounded-md hover:bg-indigo-700"
      >
        Add Book
      </button>
    </form>
  );
}

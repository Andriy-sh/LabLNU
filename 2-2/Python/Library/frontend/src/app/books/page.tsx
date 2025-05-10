"use client";

import BookForm from "@/components/BookForm";
import { useRouter } from "next/navigation";
interface BookFormData {
  title: string;
  publication_year: number;
  isbn: string;
  copies_available: number;
  author_ids: number[];
  category_ids: number[];
}

export default function AddBook() {
  const router = useRouter();

  const handleSubmit = async (bookData: BookFormData) => {
    try {
      const response = await fetch("http://localhost:8000/books/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(bookData),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Failed to add book");
      }

      router.push("/books");
    } catch (error) {
      console.error("Error adding book:", error);
      alert("Failed to add book: " + (error as Error).message);
    }
  };

  return (
    <div className="container mx-auto py-8">
      <h1 className="text-2xl font-bold mb-6 text-center">Add New Book</h1>
      <BookForm onSubmit={handleSubmit} />
    </div>
  );
}

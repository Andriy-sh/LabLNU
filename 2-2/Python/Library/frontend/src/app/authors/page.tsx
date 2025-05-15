"use client";

import AuthorForm, { AuthorFormData } from "@/components/forms/AuthorForm";
import { useState, useEffect } from "react";
import { Author } from "@/types/entities";

export default function AuthorsPage() {
  const [authors, setAuthors] = useState<Author[]>([]);
  const [editingAuthor, setEditingAuthor] = useState<Author | null>(null);

  const fetchAuthors = async () => {
    try {
      const response = await fetch("http://localhost:/authors/");
      const data = await response.json();
      setAuthors(data);
    } catch (error) {
      console.error("Error fetching authors:", error);
    }
  };

  useEffect(() => {
    fetchAuthors();
  }, []);

  const handleSubmit = async (authorData: AuthorFormData) => {
    try {
      const response = await fetch(
        editingAuthor
          ? `http://localhost:/authors/${editingAuthor.id}`
          : "http://localhost:/authors/",
        {
          method: editingAuthor ? "PUT" : "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(authorData),
        }
      );

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Failed to save author");
      }

      setEditingAuthor(null);
      fetchAuthors();
    } catch (error) {
      console.error("Error saving author:", error);
      alert("Failed to save author: " + (error as Error).message);
    }
  };

  const handleDelete = async (authorId: number) => {
    try {
      const response = await fetch(
        `http://localhost:/authors/${authorId}`,
        {
          method: "DELETE",
        }
      );

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Failed to delete author");
      }

      fetchAuthors();
    } catch (error) {
      console.error("Error deleting author:", error);
      alert("Failed to delete author: " + (error as Error).message);
    }
  };

  return (
    <div className="container mx-auto py-8 px-4">
      <h1 className="text-2xl font-bold mb-6">Authors</h1>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white shadow-md rounded-lg overflow-hidden">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Name
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {authors.map((author) => (
                <tr key={author.id}>
                  <td className="px-6 py-4 whitespace-nowrap">
                    {editingAuthor?.id === author.id ? (
                      <div className="flex gap-2">
                        <input
                          type="text"
                          value={editingAuthor.first_name}
                          onChange={(e) =>
                            setEditingAuthor({
                              ...editingAuthor,
                              first_name: e.target.value,
                            })
                          }
                          className="border rounded px-2 py-1 w-1/2"
                          placeholder="First Name"
                        />
                        <input
                          type="text"
                          value={editingAuthor.last_name}
                          onChange={(e) =>
                            setEditingAuthor({
                              ...editingAuthor,
                              last_name: e.target.value,
                            })
                          }
                          className="border rounded px-2 py-1 w-1/2"
                          placeholder="Last Name"
                        />
                      </div>
                    ) : (
                      `${author.first_name} ${author.last_name}`
                    )}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap space-x-2">
                    {editingAuthor?.id === author.id ? (
                      <>
                        <button
                          onClick={() => handleSubmit(editingAuthor)}
                          className="text-green-600 hover:text-green-900"
                        >
                          Save
                        </button>
                        <button
                          onClick={() => setEditingAuthor(null)}
                          className="text-gray-600 hover:text-gray-900 ml-2"
                        >
                          Cancel
                        </button>
                      </>
                    ) : (
                      <>
                        <button
                          onClick={() => setEditingAuthor(author)}
                          className="text-indigo-600 hover:text-indigo-900"
                        >
                          Edit
                        </button>
                        <button
                          onClick={() => handleDelete(author.id)}
                          className="text-red-600 hover:text-red-900 ml-4"
                        >
                          Delete
                        </button>
                      </>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className="bg-white shadow-md rounded-lg p-6">
          <h2 className="text-xl font-bold mb-4">Add New Author</h2>
          <AuthorForm onSubmit={handleSubmit} />
        </div>
      </div>
    </div>
  );
}

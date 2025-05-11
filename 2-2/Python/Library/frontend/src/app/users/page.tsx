"use client";

import UserForm, { UserFormData } from "@/components/forms/UserForm";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import axios from "axios";

interface User {
  id: number;
  first_name: string;
  last_name: string;
  email: string;
  registration_date: string;
}

export default function UsersPage() {
  const router = useRouter();
  const [users, setUsers] = useState<User[]>([]);
  const [editingUser, setEditingUser] = useState<number | null>(null);
  const [editFormData, setEditFormData] = useState<UserFormData>({
    first_name: "",
    last_name: "",
    email: "",
  });

  const fetchUsers = async () => {
    try {
      const response = await axios.get("http://localhost:8000/users");
      setUsers(response.data);
    } catch (error) {
      console.error("Error fetching users:", error);
    }
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  const handleSubmit = async (userData: UserFormData) => {
    try {
      await axios.post("http://localhost:8000/users", userData);
      fetchUsers();
    } catch (error: any) {
      console.error("Error saving user:", error);
      alert(
        "Failed to save user: " +
          (error.response?.data?.detail || error.message)
      );
    }
  };

  const handleEdit = (user: User) => {
    setEditingUser(user.id);
    setEditFormData({
      first_name: user.first_name,
      last_name: user.last_name,
      email: user.email,
    });
  };

  const handleUpdate = async (userId: number) => {
    try {
      await axios.put(`http://localhost:8000/users/${userId}`, editFormData);
      setEditingUser(null);
      fetchUsers();
    } catch (error) {
      console.error("Error updating user:", error);
      alert("Failed to update user");
    }
  };

  const handleDelete = async (userId: number) => {
    try {
      await axios.delete(`http://localhost:8000/users/${userId}`);
      fetchUsers();
    } catch (error) {
      console.error("Error deleting user:", error);
      alert("Failed to delete user");
    }
  };

  return (
    <div className="container mx-auto py-8 px-4">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-bold mb-4">Users List</h2>
          <div className="space-y-4">
            {users.map((user) => (
              <div
                key={user.id}
                className="p-4 bg-gray-50 rounded-lg hover:bg-gray-100"
              >
                {editingUser === user.id ? (
                  <div className="space-y-3">
                    <input
                      type="text"
                      value={editFormData.first_name}
                      onChange={(e) =>
                        setEditFormData({
                          ...editFormData,
                          first_name: e.target.value,
                        })
                      }
                      className="w-full p-2 border rounded"
                      placeholder="First Name"
                    />
                    <input
                      type="text"
                      value={editFormData.last_name}
                      onChange={(e) =>
                        setEditFormData({
                          ...editFormData,
                          last_name: e.target.value,
                        })
                      }
                      className="w-full p-2 border rounded"
                      placeholder="Last Name"
                    />
                    <input
                      type="email"
                      value={editFormData.email}
                      onChange={(e) =>
                        setEditFormData({
                          ...editFormData,
                          email: e.target.value,
                        })
                      }
                      className="w-full p-2 border rounded"
                      placeholder="Email"
                    />
                    <div className="flex justify-end space-x-2">
                      <button
                        onClick={() => handleUpdate(user.id)}
                        className="px-3 py-1 bg-blue-500 text-white rounded hover:bg-blue-600"
                      >
                        Save
                      </button>
                      <button
                        onClick={() => setEditingUser(null)}
                        className="px-3 py-1 bg-gray-500 text-white rounded hover:bg-gray-600"
                      >
                        Cancel
                      </button>
                    </div>
                  </div>
                ) : (
                  <div className="flex items-center justify-between">
                    <div>
                      <h3 className="font-medium">
                        {user.first_name} {user.last_name}
                      </h3>
                      <p className="text-sm text-gray-600">{user.email}</p>
                    </div>
                    <div className="flex space-x-2">
                      <button
                        onClick={() => handleEdit(user)}
                        className="text-blue-600 hover:text-blue-800"
                      >
                        ✎
                      </button>
                      <button
                        onClick={() => handleDelete(user.id)}
                        className="text-red-600 hover:text-red-800"
                      >
                        ✕
                      </button>
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-bold mb-4">Add New User</h2>
          <UserForm onSubmit={handleSubmit} />
        </div>
      </div>
    </div>
  );
}

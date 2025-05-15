"use client";

import { useAuth } from "@/hooks/useAuth";
import { useEffect, useState } from "react";
import axios from "axios";

interface User {
  email: string;
  first_name: string;
  last_name: string;
}

export default function ProfilePage() {
  const { isAuthenticated, isLoading } = useAuth(true);
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const token = localStorage.getItem("token");
        if (!token) return;

        const response = await axios.get("http://localhost:8000/users/me", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        setUser(response.data);
      } catch (error) {
        console.error("Error fetching user data:", error);
      }
    };

    if (isAuthenticated) {
      fetchUserData();
    }
  }, [isAuthenticated]);

  if (isLoading) {
    return <div>Завантаження...</div>;
  }

  if (!isAuthenticated) {
    return <div>Необхідно увійти в систему</div>;
  }

  return (
    <div className="max-w-4xl mx-auto py-8 px-4">
      <h1 className="text-2xl font-bold mb-6">Профіль користувача</h1>
      {user && (
        <div className="bg-white shadow rounded-lg p-6">
          <div className="space-y-4">
            <div>
              <h2 className="text-sm font-medium text-gray-500">Email</h2>
              <p className="mt-1 text-sm text-gray-900">{user.email}</p>
            </div>
            <div>
              <h2 className="text-sm font-medium text-gray-500">Ім'я</h2>
              <p className="mt-1 text-sm text-gray-900">{user.first_name}</p>
            </div>
            <div>
              <h2 className="text-sm font-medium text-gray-500">Прізвище</h2>
              <p className="mt-1 text-sm text-gray-900">{user.last_name}</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
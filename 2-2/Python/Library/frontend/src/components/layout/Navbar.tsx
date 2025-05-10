"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

export default function Navbar() {
  const pathname = usePathname();

  const isActive = (path: string) => {
    return pathname === path ? "bg-indigo-700" : "";
  };

  return (
    <nav className="bg-indigo-600">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center">
            <Link href="/" className="text-white font-bold text-xl">
              Library System
            </Link>
            <div className="hidden md:block">
              <div className="ml-10 flex items-baseline space-x-4">
                <Link
                  href="/books"
                  className={`${isActive(
                    "/books"
                  )} text-white px-3 py-2 rounded-md text-sm font-medium hover:bg-indigo-700`}
                >
                  Books
                </Link>
                <Link
                  href="/authors"
                  className={`${isActive(
                    "/authors"
                  )} text-white px-3 py-2 rounded-md text-sm font-medium hover:bg-indigo-700`}
                >
                  Authors
                </Link>
                <Link
                  href="/categories"
                  className={`${isActive(
                    "/categories"
                  )} text-white px-3 py-2 rounded-md text-sm font-medium hover:bg-indigo-700`}
                >
                  Categories
                </Link>
                <Link
                  href="/borrowed-books"
                  className={`${isActive(
                    "/borrowed-books"
                  )} text-white px-3 py-2 rounded-md text-sm font-medium hover:bg-indigo-700`}
                >
                  Borrowed Books
                </Link>
                <Link
                  href="/users"
                  className={`${isActive(
                    "/users"
                  )} text-white px-3 py-2 rounded-md text-sm font-medium hover:bg-indigo-700`}
                >
                  Users
                </Link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
}

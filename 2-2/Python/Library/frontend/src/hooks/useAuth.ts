import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';

export function useAuth(requireAuth = true) {
  const router = useRouter();
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token && requireAuth) {
      router.push('/login');
    } else if (token) {
      setIsAuthenticated(true);
    }
    setIsLoading(false);
  }, [requireAuth, router]);

  return { isAuthenticated, isLoading };
}
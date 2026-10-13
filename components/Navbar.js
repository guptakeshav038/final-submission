"use client";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useAuth } from "@/lib/auth";

export default function Navbar() {
  const { user, loading, logout } = useAuth();
  const router = useRouter();

  return (
    <header className="nav">
      <Link href="/" className="brand-mark">CreatorX</Link>
      <nav aria-label="Main">
        <Link href="/creators">Find creators</Link>
        {user && <Link href="/dashboard">Dashboard</Link>}
        {!loading && !user && (
          <>
            <Link href="/login">Sign in</Link>
            <Link href="/register" className="btn btn-small">Create account</Link>
          </>
        )}
        {user && (
          <button type="button" className="linklike" onClick={() => { logout(); router.push("/"); }}>
            Sign out
          </button>
        )}
      </nav>
    </header>
  );
}

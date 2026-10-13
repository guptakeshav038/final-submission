"use client";
import { useRouter } from "next/navigation";
import { useEffect } from "react";
import BrandDashboard from "@/components/BrandDashboard";
import CreatorDashboard from "@/components/CreatorDashboard";
import { useAuth } from "@/lib/auth";

export default function Dashboard() {
  const { user, loading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!loading && !user) router.replace("/login");
  }, [loading, user, router]);

  if (loading || !user) return <main className="page"><p className="muted">Loading</p></main>;

  return (
    <main className="page">
      <h1 className="page-title">{user.role === "brand" ? user.name : `Hi, ${user.name.split(" ")[0]}`}</h1>
      {user.role === "brand" ? <BrandDashboard /> : <CreatorDashboard />}
    </main>
  );
}

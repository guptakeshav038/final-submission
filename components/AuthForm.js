"use client";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { useState } from "react";
import { useAuth } from "@/lib/auth";

export default function AuthForm({ mode }) {
  const { login, register } = useAuth();
  const router = useRouter();
  const params = useSearchParams();
  const isRegister = mode === "register";

  const [form, setForm] = useState({ name: "", email: "", password: "", role: params.get("role") === "creator" ? "creator" : "brand" });
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const set = (k) => (e) => setForm({ ...form, [k]: e.target.value });

  async function submit(e) {
    e.preventDefault();
    setBusy(true);
    setError("");
    try {
      if (isRegister) await register(form);
      else await login(form.email, form.password);
      router.push("/dashboard");
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  }

  return (
    <main className="auth">
      <h1>{isRegister ? "Create your account" : "Sign in"}</h1>
      <form onSubmit={submit} className="stack">
        {isRegister && (
          <fieldset className="choice">
            <legend>I am a</legend>
            <label><input type="radio" name="role" value="brand" checked={form.role === "brand"} onChange={set("role")} /> Brand</label>
            <label><input type="radio" name="role" value="creator" checked={form.role === "creator"} onChange={set("role")} /> Creator</label>
          </fieldset>
        )}
        {isRegister && (
          <label>{form.role === "brand" ? "Brand name" : "Your name"}
            <input required value={form.name} onChange={set("name")} autoComplete="name" />
          </label>
        )}
        <label>Email
          <input type="email" required value={form.email} onChange={set("email")} autoComplete="email" />
        </label>
        <label>Password
          <input type="password" required minLength={isRegister ? 8 : undefined} value={form.password} onChange={set("password")} autoComplete={isRegister ? "new-password" : "current-password"} />
          {isRegister && <span className="hint">At least 8 characters</span>}
        </label>
        {error && <p className="error" role="alert">{error}</p>}
        <button className="btn" disabled={busy}>{busy ? "Please wait" : isRegister ? "Create account" : "Sign in"}</button>
      </form>
      <p className="muted">
        {isRegister ? <>Already have an account? <Link href="/login">Sign in</Link></> : <>New to CreatorX? <Link href="/register">Create an account</Link></>}
      </p>
    </main>
  );
}

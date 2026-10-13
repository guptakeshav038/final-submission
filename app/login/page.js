import { Suspense } from "react";
import AuthForm from "@/components/AuthForm";

export const metadata = { title: "Sign in · CreatorX" };

export default function Login() {
  return <Suspense><AuthForm mode="login" /></Suspense>;
}

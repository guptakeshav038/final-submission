"use client";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { compact, inr } from "@/lib/weights";

export default function Creators() {
  const [filters, setFilters] = useState({ q: "", country: "", min_followers: "" });
  const [creators, setCreators] = useState([]);
  const [state, setState] = useState("loading");
  const [error, setError] = useState("");

  async function load(f = filters) {
    setState("loading");
    const params = new URLSearchParams();
    if (f.q) params.set("q", f.q);
    if (f.country) params.set("country", f.country);
    if (f.min_followers) params.set("min_followers", f.min_followers);
    try {
      setCreators(await api(`/api/creators?${params}`));
      setState("ready");
    } catch (e) {
      setError(e.message);
      setState("error");
    }
  }

  useEffect(() => { load(); }, []); // eslint-disable-line react-hooks/exhaustive-deps

  const set = (k) => (e) => setFilters({ ...filters, [k]: e.target.value });

  return (
    <main className="page">
      <h1 className="page-title">Find creators</h1>
      <form className="filters" onSubmit={(e) => { e.preventDefault(); load(); }}>
        <label>Search<input value={filters.q} onChange={set("q")} placeholder="fitness, Pune, skincare" /></label>
        <label>Country<input value={filters.country} onChange={set("country")} placeholder="India" /></label>
        <label>Min followers<input type="number" min="0" value={filters.min_followers} onChange={set("min_followers")} /></label>
        <button className="btn">Search</button>
      </form>

      {state === "error" && <p className="error" role="alert">{error}</p>}
      {state === "ready" && creators.length === 0 && <p className="empty">No creators match these filters. Try a broader search.</p>}

      <ul className="creator-list">
        {creators.map((c) => (
          <li key={c.id} className="creator-row">
            <div>
              <h3>{c.name} <span className="muted">@{c.handle}</span></h3>
              <p>{c.bio}</p>
              <p className="muted">{c.niche}</p>
            </div>
            <dl>
              <div><dt>Followers</dt><dd>{compact(c.followers)}</dd></div>
              <div><dt>Engagement</dt><dd>{c.engagement_rate.toFixed(1)}%</dd></div>
              <div><dt>Genuine</dt><dd>{Math.round(c.genuine_engagement_ratio * 100)}%</dd></div>
              <div><dt>Location</dt><dd>{c.city || c.country || "Not set"}</dd></div>
              <div><dt>Per post</dt><dd>{inr(c.price_per_post)}</dd></div>
            </dl>
          </li>
        ))}
      </ul>
    </main>
  );
}

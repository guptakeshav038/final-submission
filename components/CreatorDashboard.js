"use client";
import { useEffect, useState } from "react";
import MatchCard from "@/components/MatchCard";
import { api } from "@/lib/api";

const AGES = ["18-24", "25-34", "35-44", "45+"];
const pct = (v) => Math.round((v || 0) * 1000) / 10;

function toForm(p) {
  return {
    handle: p.handle, bio: p.bio, niche: p.niche, followers: p.followers, engagement_rate: p.engagement_rate,
    genuine: pct(p.genuine_engagement_ratio), avg_reel_views: p.avg_reel_views, country: p.country, city: p.city,
    price_per_post: p.price_per_post,
    age: Object.fromEntries(AGES.map((a) => [a, pct(p.audience_age?.[a])])),
    female: pct(p.audience_gender?.female),
    home: pct(p.audience_countries?.[p.country]),
  };
}

export default function CreatorDashboard() {
  const [form, setForm] = useState(null);
  const [offers, setOffers] = useState([]);
  const [saved, setSaved] = useState(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    api("/api/creators/me").then((p) => setForm(toForm(p))).catch((e) => setError(e.message));
    api("/api/matches/me").then(setOffers).catch((e) => setError(e.message));
  }, []);

  if (!form) return error ? <p className="error" role="alert">{error}</p> : <p className="muted">Loading your profile</p>;

  const set = (k) => (e) => { setSaved(false); setForm({ ...form, [k]: e.target.value }); };
  const setAge = (a) => (e) => { setSaved(false); setForm({ ...form, age: { ...form.age, [a]: e.target.value } }); };
  const n = (v) => parseFloat(v) || 0;

  async function save(e) {
    e.preventDefault();
    setBusy(true);
    setError("");
    try {
      await api("/api/creators/me", {
        method: "PUT",
        body: {
          handle: form.handle, bio: form.bio, niche: form.niche, followers: Math.round(n(form.followers)),
          engagement_rate: n(form.engagement_rate), genuine_engagement_ratio: Math.min(1, n(form.genuine) / 100),
          avg_reel_views: Math.round(n(form.avg_reel_views)), country: form.country, city: form.city,
          price_per_post: Math.round(n(form.price_per_post)),
          audience_age: Object.fromEntries(AGES.map((a) => [a, n(form.age[a]) / 100])),
          audience_gender: { female: n(form.female) / 100, male: Math.max(0, 100 - n(form.female)) / 100 },
          audience_countries: form.country ? { [form.country]: n(form.home) / 100 } : {},
        },
      });
      setSaved(true);
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  }

  async function respond(match, status) {
    setBusy(true);
    try {
      const updated = await api(`/api/matches/${match.id}`, { method: "PATCH", body: { status } });
      setOffers(offers.map((o) => (o.id === updated.id ? updated : o)));
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="split">
      <section className="main">
        <h2>Offers</h2>
        {offers.length === 0 && <p className="empty">No offers yet. Brands find you through your profile, so the more complete it is, the better your matches.</p>}
        <div className="match-list">
          {offers.map((m) => <MatchCard key={m.id} match={m} mode="creator" onAction={respond} busy={busy} />)}
        </div>
      </section>

      <form className="panel stack side-form" onSubmit={save}>
        <h2>Your profile</h2>
        <label>Handle<input value={form.handle} onChange={set("handle")} /></label>
        <label>Bio<textarea rows={3} value={form.bio} onChange={set("bio")} /></label>
        <label>Content topics<input value={form.niche} onChange={set("niche")} placeholder="fitness, yoga" /><span className="hint">Separate topics with commas</span></label>
        <div className="row">
          <label>Followers<input type="number" min="0" value={form.followers} onChange={set("followers")} /></label>
          <label>Engagement rate (%)<input type="number" min="0" max="100" step="0.1" value={form.engagement_rate} onChange={set("engagement_rate")} /></label>
        </div>
        <div className="row">
          <label>Genuine interactions (%)<input type="number" min="0" max="100" value={form.genuine} onChange={set("genuine")} /></label>
          <label>Average reel views<input type="number" min="0" value={form.avg_reel_views} onChange={set("avg_reel_views")} /></label>
        </div>
        <div className="row">
          <label>Country<input value={form.country} onChange={set("country")} /></label>
          <label>City<input value={form.city} onChange={set("city")} /></label>
        </div>
        <label>Price per post (₹)<input type="number" min="0" value={form.price_per_post} onChange={set("price_per_post")} /></label>
        <fieldset className="choice">
          <legend>Audience age (% of followers)</legend>
          {AGES.map((a) => (
            <label key={a} className="mini">{a}<input type="number" min="0" max="100" value={form.age[a]} onChange={setAge(a)} /></label>
          ))}
        </fieldset>
        <div className="row">
          <label>Female audience (%)<input type="number" min="0" max="100" value={form.female} onChange={set("female")} /></label>
          <label>Audience in your country (%)<input type="number" min="0" max="100" value={form.home} onChange={set("home")} /></label>
        </div>
        {error && <p className="error" role="alert">{error}</p>}
        <button className="btn" disabled={busy}>Save profile</button>
        {saved && <p className="ok" role="status">Profile saved</p>}
      </form>
    </div>
  );
}

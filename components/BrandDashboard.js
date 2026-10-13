"use client";
import { useEffect, useState } from "react";
import MatchCard from "@/components/MatchCard";
import { api } from "@/lib/api";
import { GOALS, inr } from "@/lib/weights";

const AGES = ["18-24", "25-34", "35-44", "45+"];
const EMPTY = {
  title: "", description: "", niche: "", goal: "balanced", target_age_buckets: [], target_gender: "any",
  target_country: "", target_city: "", budget: "", min_followers: "", max_followers: "",
};

export default function BrandDashboard() {
  const [campaigns, setCampaigns] = useState([]);
  const [selectedId, setSelectedId] = useState(null);
  const [matches, setMatches] = useState([]);
  const [form, setForm] = useState(EMPTY);
  const [showForm, setShowForm] = useState(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  const selected = campaigns.find((c) => c.id === selectedId);

  useEffect(() => {
    api("/api/campaigns")
      .then((list) => {
        setCampaigns(list);
        if (list.length) setSelectedId(list[0].id);
        else setShowForm(true);
      })
      .catch((e) => setError(e.message));
  }, []);

  useEffect(() => {
    if (!selectedId) return;
    setMatches([]);
    api(`/api/campaigns/${selectedId}/matches`).then(setMatches).catch((e) => setError(e.message));
  }, [selectedId]);

  const set = (k) => (e) => setForm({ ...form, [k]: e.target.value });
  const toggleAge = (a) =>
    setForm({ ...form, target_age_buckets: form.target_age_buckets.includes(a) ? form.target_age_buckets.filter((x) => x !== a) : [...form.target_age_buckets, a] });

  async function createCampaign(e) {
    e.preventDefault();
    setBusy(true);
    setError("");
    try {
      const num = (v) => parseInt(v, 10) || 0;
      const created = await api("/api/campaigns", {
        method: "POST",
        body: { ...form, budget: num(form.budget), min_followers: num(form.min_followers), max_followers: num(form.max_followers) },
      });
      setCampaigns([created, ...campaigns]);
      setSelectedId(created.id);
      setForm(EMPTY);
      setShowForm(false);
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  }

  async function findMatches() {
    setBusy(true);
    setError("");
    try {
      setMatches(await api(`/api/campaigns/${selectedId}/match`, { method: "POST" }));
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  }

  async function changeStatus(match, status) {
    setBusy(true);
    try {
      const updated = await api(`/api/matches/${match.id}`, { method: "PATCH", body: { status } });
      setMatches(matches.map((m) => (m.id === updated.id ? updated : m)));
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="split">
      <aside className="side">
        <h2>Campaigns</h2>
        <ul className="camp-list">
          {campaigns.map((c) => (
            <li key={c.id}>
              <button type="button" aria-current={c.id === selectedId} onClick={() => { setSelectedId(c.id); setShowForm(false); }}>
                {c.title}
              </button>
            </li>
          ))}
        </ul>
        <button type="button" className="btn btn-ghost btn-small" onClick={() => setShowForm(!showForm)}>
          {showForm ? "Close form" : "New campaign"}
        </button>
      </aside>

      <section className="main">
        {error && <p className="error" role="alert">{error}</p>}

        {showForm && (
          <form onSubmit={createCampaign} className="panel stack">
            <h2>New campaign</h2>
            <label>Campaign title<input required value={form.title} onChange={set("title")} /></label>
            <label>What are you promoting?
              <textarea rows={3} value={form.description} onChange={set("description")} placeholder="Describe the product and the kind of content you want" />
            </label>
            <label>Content topics<input value={form.niche} onChange={set("niche")} placeholder="fitness, running, athleisure" /><span className="hint">Separate topics with commas</span></label>
            <label>Campaign goal
              <select value={form.goal} onChange={set("goal")}>
                {Object.entries(GOALS).map(([k, g]) => <option key={k} value={k}>{g.label}</option>)}
              </select>
              <span className="hint">The goal changes how much each factor counts toward the score</span>
            </label>
            <fieldset className="choice">
              <legend>Audience age</legend>
              {AGES.map((a) => (
                <label key={a}><input type="checkbox" checked={form.target_age_buckets.includes(a)} onChange={() => toggleAge(a)} /> {a}</label>
              ))}
            </fieldset>
            <div className="row">
              <label>Audience gender
                <select value={form.target_gender} onChange={set("target_gender")}>
                  <option value="any">Any</option><option value="female">Female</option><option value="male">Male</option><option value="other">Other</option>
                </select>
              </label>
              <label>Target country<input value={form.target_country} onChange={set("target_country")} placeholder="India" /></label>
              <label>Target city<input value={form.target_city} onChange={set("target_city")} placeholder="Pune" /></label>
            </div>
            <div className="row">
              <label>Max price per creator (₹)<input type="number" min="0" value={form.budget} onChange={set("budget")} /></label>
              <label>Min followers<input type="number" min="0" value={form.min_followers} onChange={set("min_followers")} /></label>
              <label>Max followers<input type="number" min="0" value={form.max_followers} onChange={set("max_followers")} /></label>
            </div>
            <button className="btn" disabled={busy}>Create campaign</button>
          </form>
        )}

        {selected && !showForm && (
          <>
            <div className="panel">
              <h2>{selected.title}</h2>
              <p className="muted">
                {GOALS[selected.goal].label}
                {selected.target_city || selected.target_country ? ` · ${selected.target_city || selected.target_country}` : ""}
                {selected.target_age_buckets.length ? ` · ages ${selected.target_age_buckets.join(", ")}` : ""}
                {` · budget ${inr(selected.budget)}`}
              </p>
              <button className="btn" onClick={findMatches} disabled={busy}>
                {busy ? "Scoring creators" : matches.length ? "Refresh matches" : "Find matches"}
              </button>
            </div>

            {matches.length === 0 && !busy && <p className="empty">No matches yet. Select Find matches to rank creators for this campaign.</p>}
            <div className="match-list">
              {matches.map((m) => <MatchCard key={m.id} match={m} mode="brand" onAction={changeStatus} busy={busy} />)}
            </div>
          </>
        )}
      </section>
    </div>
  );
}

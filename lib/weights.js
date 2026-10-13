// Mirrors backend/app/scoring.py so the landing-page demo and the API agree.
export const DIMENSIONS = [
  { key: "demographics", label: "Audience fit", color: "var(--c-demo)" },
  { key: "niche", label: "Niche relevance", color: "var(--c-niche)" },
  { key: "engagement", label: "Engagement quality", color: "var(--c-eng)" },
  { key: "location", label: "Location match", color: "var(--c-loc)" },
  { key: "content_quality", label: "Content quality", color: "var(--c-content)" },
  { key: "past_roi", label: "Past campaign ROI", color: "var(--c-roi)" },
];

export const GOALS = {
  balanced: { label: "Balanced", weights: { demographics: 0.3, niche: 0.25, engagement: 0.2, location: 0.1, content_quality: 0.1, past_roi: 0.05 } },
  awareness: { label: "Reach new audiences", weights: { demographics: 0.35, niche: 0.25, engagement: 0.15, location: 0.1, content_quality: 0.1, past_roi: 0.05 } },
  conversion: { label: "Drive sales", weights: { demographics: 0.25, niche: 0.2, engagement: 0.25, location: 0.1, content_quality: 0.05, past_roi: 0.15 } },
  local_launch: { label: "Local launch", weights: { demographics: 0.25, niche: 0.2, engagement: 0.15, location: 0.25, content_quality: 0.1, past_roi: 0.05 } },
};

export function buildBreakdown(scores, weights) {
  const out = {};
  for (const d of DIMENSIONS) {
    const s = scores[d.key];
    out[d.key] = { score: s, weight: weights[d.key], points: s * weights[d.key], reason: "" };
  }
  return out;
}

export const total = (breakdown) => Object.values(breakdown).reduce((sum, b) => sum + b.points, 0);

export function compact(n) {
  if (n >= 1_000_000) return `${(n / 1_000_000).toFixed(1)}M`;
  if (n >= 1_000) return `${(n / 1_000).toFixed(n >= 100_000 ? 0 : 1).replace(".0", "")}K`;
  return String(n);
}

export const inr = (n) => (n ? `₹${n.toLocaleString("en-IN")}` : "No cap");

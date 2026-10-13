import ScoreBar from "@/components/ScoreBar";
import { DIMENSIONS, compact, inr } from "@/lib/weights";

const STATUS_LABEL = { pending: "Suggested", invited: "Offer sent", accepted: "Accepted", declined: "Declined" };

export default function MatchCard({ match, mode, onAction, busy }) {
  const { creator: c, campaign } = match;
  const title = mode === "brand" ? c.name : campaign.title;
  const subtitle =
    mode === "brand"
      ? `@${c.handle} · ${c.city || c.country} · ${compact(c.followers)} followers · ${inr(c.price_per_post)} per post`
      : `${campaign.brand_name} · budget ${inr(campaign.budget)} per creator`;

  return (
    <article className="match">
      <div className="match-top">
        <div>
          <h3>{title}</h3>
          <p className="muted">{subtitle}</p>
        </div>
        <div className="match-score" aria-label={`Match score ${Math.round(match.score)} out of 100`}>
          {Math.round(match.score)}
        </div>
      </div>

      <ScoreBar breakdown={match.breakdown} />

      <details>
        <summary>Why this score</summary>
        <ul className="reasons">
          {DIMENSIONS.map((d) => (
            <li key={d.key}><strong>{d.label}:</strong> {match.breakdown[d.key]?.reason}</li>
          ))}
        </ul>
      </details>

      <div className="match-actions">
        <span className={`pill pill-${match.status}`}>{STATUS_LABEL[match.status]}</span>
        {mode === "brand" && match.status === "pending" && <button className="btn btn-small" disabled={busy} onClick={() => onAction(match, "invited")}>Send offer</button>}
        {mode === "brand" && match.status === "invited" && <button className="btn btn-small btn-ghost" disabled={busy} onClick={() => onAction(match, "pending")}>Withdraw offer</button>}
        {mode === "creator" && match.status === "invited" && (
          <>
            <button className="btn btn-small" disabled={busy} onClick={() => onAction(match, "accepted")}>Accept</button>
            <button className="btn btn-small btn-ghost" disabled={busy} onClick={() => onAction(match, "declined")}>Decline</button>
          </>
        )}
      </div>
    </article>
  );
}

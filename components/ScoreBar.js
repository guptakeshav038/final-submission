import { DIMENSIONS } from "@/lib/weights";

export default function ScoreBar({ breakdown, legend = true }) {
  return (
    <div className="scorebar">
      <div className="scorebar-track" role="img" aria-label="Score contribution by dimension">
        {DIMENSIONS.map((d) => {
          const b = breakdown[d.key];
          if (!b) return null;
          return <span key={d.key} style={{ width: `${b.points}%`, background: d.color }} title={`${d.label}: ${b.points.toFixed(1)} points`} />;
        })}
      </div>
      {legend && (
        <ul className="scorebar-legend">
          {DIMENSIONS.map((d) => {
            const b = breakdown[d.key];
            if (!b) return null;
            return (
              <li key={d.key}>
                <i style={{ background: d.color }} />
                <span className="lg-name">{d.label}</span>
                <span className="lg-val">
                  {Math.round(b.score)} <small>× {Math.round(b.weight * 100)}%</small>
                </span>
              </li>
            );
          })}
        </ul>
      )}
    </div>
  );
}

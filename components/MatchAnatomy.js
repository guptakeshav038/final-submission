"use client";
import { useState } from "react";
import ScoreBar from "@/components/ScoreBar";
import { GOALS, buildBreakdown, total } from "@/lib/weights";

const SAMPLE = { demographics: 94, niche: 90, engagement: 92, location: 96, content_quality: 88, past_roi: 80 };

export default function MatchAnatomy() {
  const [goal, setGoal] = useState("balanced");
  const breakdown = buildBreakdown(SAMPLE, GOALS[goal].weights);

  return (
    <div className="anatomy" aria-live="polite">
      <div className="anatomy-head">
        <div>
          <p className="anatomy-who">Aanya Rao</p>
          <p className="muted">Fitness creator, Pune, 38K followers</p>
        </div>
        <p className="anatomy-score">{total(breakdown).toFixed(0)}<small>/100</small></p>
      </div>
      <ScoreBar breakdown={breakdown} />
      <div className="anatomy-goals" role="group" aria-label="Campaign goal">
        <p className="muted">Campaign goal</p>
        <div className="seg">
          {Object.entries(GOALS).map(([key, g]) => (
            <button key={key} type="button" aria-pressed={goal === key} onClick={() => setGoal(key)}>
              {g.label}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}

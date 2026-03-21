import React from "react";

const severityColor = {
  critical: "#ef4444",
  moderate: "#f59e0b",
  minor: "#3b82f6",
  none: "#10b981"
};

const severityBg = {
  critical: "rgba(239,68,68,0.1)",
  moderate: "rgba(245,158,11,0.1)",
  minor: "rgba(59,130,246,0.1)",
  none: "rgba(16,185,129,0.1)"
};

const levelLabel = {
  none: "None",
  beginner: "Beginner",
  intermediate: "Intermediate",
  advanced: "Advanced"
};

const levelWidth = {
  none: 0,
  beginner: 33,
  intermediate: 66,
  advanced: 100
};

export default function SkillGapVisualizer({ gaps, matched }) {
  if (!gaps?.length && !matched?.length) return null;

  const allSkills = [
    ...(matched || []).map(m => ({
      skill: m.skill,
      current_level: m.current_level,
      required_level: m.required_level,
      gap_severity: "none",
      progress: 100
    })),
    ...(gaps || [])
  ];

  return (
    <div style={{
      background: "#1e1e2e", borderRadius: 20,
      padding: 28, marginBottom: 24,
      border: "1px solid rgba(99,102,241,0.2)"
    }}>
      <h2 style={{
        fontSize: 20, fontWeight: 800,
        color: "#e2e8f0", marginBottom: 6
      }}>
        Skill Gap Analysis
      </h2>
      <p style={{ color: "#64748b", fontSize: 14, marginBottom: 24 }}>
        Visual breakdown of your current skills vs requirements
      </p>

      {/* Legend */}
      <div style={{
        display: "flex", gap: 16, marginBottom: 20, flexWrap: "wrap"
      }}>
        {[
          { label: "Matched", color: "#10b981" },
          { label: "Minor gap", color: "#3b82f6" },
          { label: "Moderate gap", color: "#f59e0b" },
          { label: "Critical gap", color: "#ef4444" }
        ].map(l => (
          <div key={l.label} style={{
            display: "flex", alignItems: "center", gap: 6
          }}>
            <div style={{
              width: 10, height: 10, borderRadius: "50%",
              background: l.color
            }} />
            <span style={{ fontSize: 12, color: "#64748b" }}>{l.label}</span>
          </div>
        ))}
      </div>

      {/* Skills list */}
      <div style={{ display: "flex", flexDirection: "column", gap: 14 }}>
        {allSkills.map((skill, i) => (
          <div key={i}>
            <div style={{
              display: "flex", justifyContent: "space-between",
              alignItems: "center", marginBottom: 6
            }}>
              <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
                <span style={{
                  fontWeight: 600, fontSize: 14,
                  color: "#e2e8f0", textTransform: "capitalize"
                }}>
                  {skill.skill}
                </span>
                <span style={{
                  padding: "2px 8px", borderRadius: 12, fontSize: 11,
                  fontWeight: 600,
                  background: severityBg[skill.gap_severity],
                  color: severityColor[skill.gap_severity]
                }}>
                  {skill.gap_severity === "none" ? "✅ matched" : `${skill.gap_severity} gap`}
                </span>
              </div>
              <span style={{ fontSize: 12, color: "#64748b" }}>
                {levelLabel[skill.current_level]} → {levelLabel[skill.required_level]}
              </span>
            </div>

            {/* Progress bar */}
            <div style={{
              position: "relative", height: 8,
              background: "rgba(255,255,255,0.06)",
              borderRadius: 4, overflow: "hidden"
            }}>
              {/* Required level marker */}
              <div style={{
                position: "absolute",
                left: `${levelWidth[skill.required_level]}%`,
                top: 0, bottom: 0, width: 2,
                background: "rgba(255,255,255,0.2)",
                zIndex: 2
              }} />
              {/* Current level fill */}
              <div style={{
                height: "100%",
                width: `${levelWidth[skill.current_level]}%`,
                background: severityColor[skill.gap_severity],
                borderRadius: 4,
                transition: "width 0.5s ease"
              }} />
            </div>

            {/* Level markers */}
            <div style={{
              display: "flex", justifyContent: "space-between",
              marginTop: 4
            }}>
              {["None", "Beginner", "Intermediate", "Advanced"].map((l, idx) => (
                <span key={l} style={{
                  fontSize: 10, color: "#334155"
                }}>{l}</span>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

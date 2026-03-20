export default function ReasoningTrace({ trace }) {
  const sections = [
    { key: "extraction", label: "🔍 Skill extraction", color: "#6366f1" },
    { key: "gap_analysis", label: "📊 Gap analysis", color: "#f59e0b" },
    { key: "path_selection", label: "🗺 Path selection", color: "#10b981" },
  ];

  return (
    <div style={{ marginTop: 16, background: "#0f172a", color: "#94a3b8", borderRadius: 10, padding: 20, fontFamily: "monospace", fontSize: 13 }}>
      <div style={{ color: "#e2e8f0", fontWeight: 700, marginBottom: 16 }}>🧠 Reasoning Trace</div>
      {sections.map(({ key, label, color }) => (
        <div key={key} style={{ marginBottom: 16 }}>
          <div style={{ color, fontWeight: 600, marginBottom: 6 }}>{label}</div>
          {(trace[key] || []).map((line, i) => (
            <div key={i} style={{ paddingLeft: 12, borderLeft: `2px solid ${color}40`, marginBottom: 4, lineHeight: 1.5 }}>
              {typeof line === "string" ? line : JSON.stringify(line)}
            </div>
          ))}
        </div>
      ))}
    </div>
  );
}
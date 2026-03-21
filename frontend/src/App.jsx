import React, { useState } from "react";
import UploadPanel from "./components/UploadPanel";
import Roadmap from "./components/Roadmap";
import ReasoningTrace from "./components/ReasoningTrace";
import SkillGapVisualizer from "./components/SkillGapVisualizer";
import "./App.css";

const API = import.meta.env.VITE_API_URL || "http://localhost:8000";

export default function App() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [showTrace, setShowTrace] = useState(false);

  async function handleAnalyze(resumeText, jdText) {
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const controller = new AbortController();
      const timeout = setTimeout(() => controller.abort(), 120000);

      const res = await fetch(`${API}/analyze`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ resume_text: resumeText, jd_text: jdText }),
        signal: controller.signal
      });

      clearTimeout(timeout);
      const data = await res.json();
      setResult(data);
    } catch (e) {
      if (e.name === "AbortError") {
        setError("Server is warming up. Please wait 30 seconds and try again.");
      } else {
        setError("Analysis failed. Please try again.");
      }
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="app">
      <header className="hero">
        <div className="hero-bg" />
        <div className="hero-content">
          <div className="logo-badge">AI</div>
          <h1 className="hero-title">Skill<span>Bridge</span></h1>
          <p className="hero-subtitle">AI-powered adaptive onboarding engine</p>
          <div className="hero-tags">
            <span className="tag">🤖 Agentic AI</span>
            <span className="tag">📊 Gap Analysis</span>
            <span className="tag">🗺 Smart Pathways</span>
            <span className="tag">📧 Email Export</span>
          </div>
        </div>
      </header>

      <main className="main">
        <UploadPanel onAnalyze={handleAnalyze} loading={loading} />

        {error && (
          <div className="error-banner">
            <span>⚠️</span> {error}
            <button
              onClick={() => setError(null)}
              style={{
                marginLeft: "auto", background: "none",
                border: "none", color: "#fca5a5",
                cursor: "pointer", fontSize: 18
              }}
            >×</button>
          </div>
        )}

        {loading && (
          <div className="loading-card">
            <div className="spinner" />
            <div>
              <div className="loading-title">Agent is analyzing...</div>
              <div className="loading-sub">
                Extracting skills → Computing gaps → Building pathway
              </div>
              <div className="loading-sub" style={{ marginTop: 4, color: "#475569" }}>
                This may take 30-60 seconds on first run
              </div>
            </div>
          </div>
        )}

        {result && (
          <>
            <div className="stats-grid">
              {[
                {
                  label: "Skills matched",
                  value: result.skill_gap?.matched?.length ?? 0,
                  color: "#10b981",
                  icon: "✅"
                },
                {
                  label: "Skill gaps",
                  value: result.skill_gap?.gaps?.length ?? 0,
                  color: "#f59e0b",
                  icon: "📌"
                },
                {
                  label: "Coverage",
                  value: `${result.skill_gap?.coverage_pct ?? 0}%`,
                  color: "#6366f1",
                  icon: "📈"
                },
                {
                  label: "Modules",
                  value: result.pathway?.length ?? 0,
                  color: "#3b82f6",
                  icon: "📚"
                },
              ].map((s) => (
                <div
                  key={s.label}
                  className="stat-card"
                  style={{ "--accent": s.color }}
                >
                  <div className="stat-icon">{s.icon}</div>
                  <div className="stat-value" style={{ color: s.color }}>
                    {s.value}
                  </div>
                  <div className="stat-label">{s.label}</div>
                </div>
              ))}
            </div>

            <SkillGapVisualizer
              gaps={result.skill_gap?.gaps}
              matched={result.skill_gap?.matched}
            />

            <Roadmap
              pathway={result.pathway}
              skillGap={result.skill_gap}
            />

            <button
              className="trace-btn"
              onClick={() => setShowTrace(!showTrace)}
            >
              {showTrace ? "🙈 Hide" : "🧠 Show"} reasoning trace
            </button>

            {showTrace && (
              <ReasoningTrace trace={result.reasoning_trace} />
            )}
          </>
        )}
      </main>

      <footer className="footer">
        <p>SkillBridge © 2025 · Built with Agentic AI + Groq + Gmail</p>
      </footer>
    </div>
  );
}


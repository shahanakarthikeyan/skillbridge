import React, { useState } from "react";

const API = import.meta.env.VITE_API_URL || "http://localhost:8000";

export default function UploadPanel({ onAnalyze, loading }) {
  const [resumeText, setResumeText] = useState("");
  const [jdText, setJdText] = useState("");
  const [resumeFile, setResumeFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [uploadError, setUploadError] = useState("");

  async function handleFileUpload(e) {
    const file = e.target.files[0];
    if (!file) return;
    setResumeFile(file.name);
    setUploading(true);
    setUploadError("");
    try {
      const formData = new FormData();
      formData.append("file", file);

      const res = await fetch(`${API}/extract-text`, {
        method: "POST",
        body: formData,
      });

      const data = await res.json();
      console.log("Extract response:", data);

      if (data.text && data.text.trim().length > 50) {
        setResumeText(data.text);
      } else if (data.error) {
        setUploadError("PDF extraction failed. Please paste your resume text manually.");
      } else {
        setUploadError("Could not extract text. Please paste your resume manually.");
      }
    } catch (err) {
      console.error("Upload failed:", err);
      setUploadError("Upload failed. Please paste your resume text manually.");
    } finally {
      setUploading(false);
    }
  }

  const canGenerate = !loading && jdText && (resumeText || resumeFile);

  return (
    <div style={{
      background: "#1e1e2e",
      borderRadius: 20,
      padding: 28,
      border: "1px solid rgba(255,255,255,0.06)"
    }}>
      <h2 style={{
        fontSize: 18, fontWeight: 700,
        marginBottom: 20, color: "#e2e8f0"
      }}>
        Paste or upload your documents
      </h2>

      <div style={{
        display: "grid",
        gridTemplateColumns: "1fr 1fr",
        gap: 16,
        marginBottom: 20
      }}>
        {/* Resume side */}
        <div>
          <label style={{
            display: "block", marginBottom: 8, fontSize: 13,
            fontWeight: 600, color: "#818cf8",
            textTransform: "uppercase", letterSpacing: "0.05em"
          }}>
            Resume / CV
          </label>

          <label style={{
            display: "flex", alignItems: "center", gap: 8,
            padding: "10px 14px", borderRadius: 10,
            cursor: uploading ? "not-allowed" : "pointer",
            background: resumeText
              ? "rgba(16,185,129,0.1)"
              : "rgba(99,102,241,0.1)",
            border: resumeText
              ? "1px dashed rgba(16,185,129,0.4)"
              : "1px dashed rgba(99,102,241,0.4)",
            color: resumeText ? "#10b981" : "#818cf8",
            fontSize: 13, fontWeight: 600,
            marginBottom: 10, transition: "all 0.2s"
          }}>
            {uploading
              ? "Extracting text from PDF..."
              : resumeText
              ? `✅ ${resumeFile}`
              : "📎 Upload PDF or TXT file"}
            <input
              type="file"
              accept=".pdf,.txt"
              onChange={handleFileUpload}
              style={{ display: "none" }}
              disabled={uploading}
            />
          </label>

          {uploadError && (
            <div style={{
              marginBottom: 8, padding: "8px 12px",
              background: "rgba(239,68,68,0.1)",
              borderRadius: 8, color: "#fca5a5", fontSize: 12
            }}>
              {uploadError}
            </div>
          )}

          {resumeText && !uploading && (
            <div style={{
              marginBottom: 8, padding: "8px 12px",
              background: "rgba(16,185,129,0.1)",
              borderRadius: 8, color: "#10b981", fontSize: 12
            }}>
              ✅ {resumeText.length} characters extracted successfully
            </div>
          )}

          <textarea
            style={{
              width: "100%", minHeight: 160,
              padding: "14px 16px",
              background: "#0f0f1a", color: "#e2e8f0",
              border: "1px solid rgba(99,102,241,0.3)",
              borderRadius: 12, fontFamily: "inherit",
              fontSize: 14, resize: "vertical",
              outline: "none", boxSizing: "border-box",
              lineHeight: 1.6
            }}
            placeholder="Or paste your resume text here..."
            value={resumeText}
            onChange={(e) => setResumeText(e.target.value)}
          />
        </div>

        {/* JD side */}
        <div>
          <label style={{
            display: "block", marginBottom: 8, fontSize: 13,
            fontWeight: 600, color: "#f59e0b",
            textTransform: "uppercase", letterSpacing: "0.05em"
          }}>
            Job Description
          </label>

          <div style={{
            padding: "10px 14px", borderRadius: 10,
            background: "rgba(245,158,11,0.05)",
            border: "1px dashed rgba(245,158,11,0.2)",
            color: "#64748b", fontSize: 13, marginBottom: 10
          }}>
            📝 Paste job description below
          </div>

          <textarea
            style={{
              width: "100%", minHeight: 160,
              padding: "14px 16px",
              background: "#0f0f1a", color: "#e2e8f0",
              border: "1px solid rgba(245,158,11,0.3)",
              borderRadius: 12, fontFamily: "inherit",
              fontSize: 14, resize: "vertical",
              outline: "none", boxSizing: "border-box",
              lineHeight: 1.6
            }}
            placeholder="Paste the job description here..."
            value={jdText}
            onChange={(e) => setJdText(e.target.value)}
          />
        </div>
      </div>

      <button
        onClick={() => onAnalyze(resumeText, jdText)}
        disabled={!canGenerate}
        style={{
          width: "100%", padding: "16px 24px",
          background: !canGenerate
            ? "#1e293b"
            : "linear-gradient(135deg, #6366f1, #8b5cf6)",
          color: !canGenerate ? "#475569" : "white",
          border: !canGenerate
            ? "1px solid rgba(255,255,255,0.06)"
            : "none",
          borderRadius: 12, fontSize: 16,
          fontWeight: 700,
          cursor: !canGenerate ? "not-allowed" : "pointer",
          transition: "all 0.2s",
          boxShadow: !canGenerate
            ? "none"
            : "0 0 30px rgba(99,102,241,0.3)"
        }}
      >
        {loading
          ? "🤖 Agent analyzing your profile..."
          : !jdText
          ? "Add job description to continue"
          : !resumeText && !resumeFile
          ? "Upload or paste resume to continue"
          : "✨ Generate Learning Pathway →"}
      </button>
    </div>
  );
}

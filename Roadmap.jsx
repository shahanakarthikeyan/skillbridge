import { useState } from "react";

const API = import.meta.env.VITE_API_URL || "http://localhost:8000";

export default function Roadmap({ pathway, skillGap }) {
  const [email, setEmail] = useState("");
  const [name, setName] = useState("");
  const [emailStatus, setEmailStatus] = useState(null);
  const [emailError, setEmailError] = useState("");
  const totalHours = pathway?.reduce((s, p) => s + (p.estimated_hours || 0), 0) || 0;

  async function handleEmail() {
    setEmailStatus("sending");
    try {
      const res = await fetch(API + "/send-roadmap", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, name, pathway: pathway || [], coverage_pct: skillGap?.coverage_pct || 0 })
      });
      const data = await res.json();
      if (data.status === "sent") { setEmailStatus("sent"); }
      else { setEmailStatus("error"); setEmailError(data.error || "Unknown error"); }
    } catch (err) {
      setEmailStatus("error");
      setEmailError(err.message);
    }
  }

  if (!pathway?.length) return <div style={{textAlign:"center",padding:40,color:"#64748b"}}>No pathway generated yet.</div>;

  return (
    <div>
      <div style={{background:"#1e1e2e",borderRadius:20,padding:"24px 28px",marginBottom:24,border:"1px solid rgba(99,102,241,0.2)",display:"flex",justifyContent:"space-between",alignItems:"center",flexWrap:"wrap",gap:12}}>
        <div>
          <h2 style={{fontSize:22,fontWeight:800,color:"#e2e8f0",marginBottom:4}}>Your Learning Roadmap</h2>
          <p style={{color:"#64748b",fontSize:14}}>{pathway.length} modules - {totalHours} hours - Personalized by AI</p>
        </div>
        <div style={{background:"rgba(99,102,241,0.15)",borderRadius:12,padding:"10px 20px",border:"1px solid rgba(99,102,241,0.3)"}}>
          <span style={{color:"#818cf8",fontWeight:700,fontSize:20}}>{skillGap?.coverage_pct ?? 0}%</span>
          <span style={{color:"#64748b",fontSize:13,marginLeft:6}}>coverage</span>
        </div>
      </div>

      {pathway.map((step, i) => (
        <div key={i} style={{display:"flex",gap:16,marginBottom:16}}>
          <div style={{display:"flex",flexDirection:"column",alignItems:"center"}}>
            <div style={{width:40,height:40,borderRadius:"50%",background:"#6366f1",color:"white",fontWeight:800,fontSize:16,display:"flex",alignItems:"center",justifyContent:"center",flexShrink:0}}>{i+1}</div>
            {i < pathway.length-1 && <div style={{width:2,flex:1,background:"rgba(99,102,241,0.2)",marginTop:6}}/>}
          </div>
          <div style={{flex:1,background:"#1e1e2e",borderRadius:16,padding:"18px 22px",border:"1px solid rgba(255,255,255,0.06)",marginBottom:4}}>
            <div style={{display:"flex",justifyContent:"space-between",alignItems:"flex-start",flexWrap:"wrap",gap:8}}>
              <div>
                <div style={{fontWeight:700,fontSize:17,color:"#e2e8f0",marginBottom:6}}>{step.course?.title}</div>
                <div style={{fontSize:13,color:"#64748b"}}>
                  Skill: <span style={{color:"#a5b4fc",fontWeight:600}}>{step.skill_gap}</span> - {step.from_level} to {step.to_level}
                </div>
              </div>
              <span style={{padding:"4px 12px",borderRadius:20,fontSize:12,fontWeight:700,background:"rgba(239,68,68,0.1)",color:"#ef4444"}}>{step.priority} priority</span>
            </div>
            <div style={{display:"flex",gap:10,marginTop:14,flexWrap:"wrap"}}>
              <span style={{padding:"6px 12px",borderRadius:8,fontSize:13,background:"rgba(255,255,255,0.04)",color:"#94a3b8"}}>{step.estimated_hours}h</span>
              <span style={{padding:"6px 12px",borderRadius:8,fontSize:13,background:"rgba(255,255,255,0.04)",color:"#94a3b8"}}>{step.course?.category}</span>
              {step.course?.url && (
                <a href={step.course.url} target="_blank" rel="noreferrer" style={{padding:"6px 12px",borderRadius:8,fontSize:13,background:"rgba(99,102,241,0.1)",color:"#818cf8",textDecoration:"none",border:"1px solid rgba(99,102,241,0.2)"}}>Open course</a>
              )}
            </div>
          </div>
        </div>
      ))}

      <div style={{marginTop:32,background:"#1e1e2e",borderRadius:20,padding:28,border:"1px solid rgba(99,102,241,0.2)"}}>
        <h3 style={{fontSize:18,fontWeight:700,color:"#e2e8f0",marginBottom:6}}>Email this roadmap</h3>
        <p style={{color:"#64748b",fontSize:14,marginBottom:20}}>Send your personalized learning pathway to your inbox</p>
        <div style={{display:"flex",gap:12,flexWrap:"wrap"}}>
          <input placeholder="Your name" value={name} onChange={(e)=>setName(e.target.value)} style={{flex:1,minWidth:140,padding:"12px 16px",background:"#0f0f1a",color:"#e2e8f0",border:"1px solid rgba(99,102,241,0.3)",borderRadius:10,fontSize:14,outline:"none"}}/>
          <input placeholder="your@email.com" type="email" value={email} onChange={(e)=>setEmail(e.target.value)} style={{flex:2,minWidth:200,padding:"12px 16px",background:"#0f0f1a",color:"#e2e8f0",border:"1px solid rgba(99,102,241,0.3)",borderRadius:10,fontSize:14,outline:"none"}}/>
          <button onClick={handleEmail} disabled={!email||!name||emailStatus==="sending"} style={{padding:"12px 24px",background:(!email||!name)?"#1e293b":"#6366f1",color:"white",border:"none",borderRadius:10,fontWeight:700,cursor:(!email||!name)?"not-allowed":"pointer",fontSize:14}}>
            {emailStatus==="sending"?"Sending...":"Send PDF"}
          </button>
        </div>
        {emailStatus==="sent" && <div style={{marginTop:14,padding:"12px 16px",background:"rgba(16,185,129,0.1)",borderRadius:10,color:"#10b981",fontWeight:600}}>Sent to {email}!</div>}
        {emailStatus==="error" && <div style={{marginTop:14,padding:"12px 16px",background:"rgba(239,68,68,0.1)",borderRadius:10,color:"#fca5a5"}}>Failed: {emailError}</div>}
      </div>
    </div>
  );
}

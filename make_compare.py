#!/usr/bin/env python3
"""Generate /vs/<competitor>/ comparison pages from one template."""
import pathlib

ROOT = pathlib.Path(__file__).parent

FONTS = '<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,800&family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500&display=swap" rel="stylesheet">'

EXTRA_CSS = """
.compare-wrap{max-width:880px;margin:0 auto;padding:0 1.5rem 4rem}
.compare-hero{padding:3.5rem 0 2rem}
.compare-hero h1{font-size:clamp(2rem,4.5vw,3rem)}
.verdict{display:grid;grid-template-columns:1fr 1fr;gap:1.25rem;margin:2.25rem 0}
.verdict .card h3{font-family:var(--display);font-weight:600;font-size:1.05rem;margin-bottom:.5rem}
.verdict .card p{font-size:.93rem}
table.cmp{width:100%;border-collapse:collapse;margin:2.25rem 0;font-size:.95rem}
table.cmp th,table.cmp td{text-align:left;padding:.7rem .9rem;border-bottom:1px solid var(--line);vertical-align:top}
table.cmp th{font-family:var(--mono);font-size:.75rem;letter-spacing:.1em;text-transform:uppercase;color:var(--ash)}
table.cmp td:first-child{color:var(--ash);width:28%}
table.cmp td strong{color:var(--cream);font-weight:500}
.cmp-scroll{overflow-x:auto}
.prose{color:var(--ash);max-width:44rem}
.prose p{margin-bottom:1rem}
.prose strong{color:var(--cream);font-weight:500}
.prose h2{margin:2.5rem 0 .75rem}
.cta-band{margin:3rem 0 0;padding:1.75rem;border:1px solid var(--line);border-radius:12px;background:var(--soot)}
.cta-band p{color:var(--ash);margin-bottom:1rem}
"""

CTA = """<div class="cta-band">
  <p>Free, Apache-2.0, local-first. One command installs the whole layer.</p>
  <div class="install-cta">
    <code><span class="prompt">$</span> curl -fsSL contorch.com/install | bash</code>
  </div>
</div>"""


def page(slug, title, desc, h1, sub, verdict_them, verdict_us, them_name, rows, prose):
    trs = "\n".join(
        f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td></tr>" for r in rows
    )
    others = " · ".join(
        f'<a href="/vs/{s}/">vs {n}</a>'
        for s, n in [("granola", "Granola"), ("mem0", "Mem0"), ("otter", "Otter")]
        if s != slug
    )
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="https://contorch.com/vs/{slug}/">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="https://contorch.com/vs/{slug}/">
<link rel="icon" type="image/png" href="/favicon-64.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
{FONTS}
<link rel="stylesheet" href="/styles.css">
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-X0YNYJRMWB"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', 'G-X0YNYJRMWB');
</script>
<style>{EXTRA_CSS}</style>
</head>
<body>
<nav>
  <a class="brand" href="/">
    <img src="/logo-512.png" alt="" width="26" height="37">
    <span>contorch</span>
  </a>
  <div class="nav-links">
    <a href="/#how">How it runs</a>
    <a href="/#install">Install</a>
    <a href="https://github.com/contorch" rel="noopener">GitHub</a>
  </div>
</nav>
<div class="compare-wrap">
  <header class="compare-hero">
    <p class="eyebrow">an honest comparison</p>
    <h1>{h1}</h1>
    <p class="sub">{sub}</p>
  </header>

  <div class="verdict">
    <div class="card"><h3>Use {them_name} if…</h3><p>{verdict_them}</p></div>
    <div class="card"><h3>Use contorch if…</h3><p>{verdict_us}</p></div>
  </div>

  <div class="cmp-scroll">
  <table class="cmp">
    <thead><tr><th></th><th>{them_name}</th><th>contorch</th></tr></thead>
    <tbody>
{trs}
    </tbody>
  </table>
  </div>

  <div class="prose">
{prose}
  </div>

  {CTA}
</div>
<footer>
  <img src="/logo-512.png" alt="contorch" width="20" height="28">
  <p>contorch — context, carried forward.</p>
  <div class="foot-links">
    <a href="/">home</a>
    {others}
    <a href="https://github.com/contorch" rel="noopener">GitHub</a>
  </div>
  <p class="quiet">© 2026 contorch · comparisons reflect public docs at time of writing — tell us if something's outdated.</p>
</footer>
</body>
</html>
"""
    out = ROOT / "vs" / slug / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    return out


# ---------------------------------------------------------------- Granola
page(
    "granola",
    "Open-source Granola alternative — contorch vs Granola",
    "Granola turns meetings into polished notes for humans. contorch turns them into memory your coding agents use — open source, local Markdown, no bot. An honest comparison.",
    "Granola turns meetings into notes. contorch turns them into memory.",
    "Both capture your calls without a bot, straight from your Mac's audio, and label speakers Me and Them. What happens next is where they part ways: notes are for you to read — memory is for your agents to use.",
    "you want beautiful, human-readable summaries with templates, follow-up emails, sharing, and team features. Granola is excellent at its job, and its job is notes.",
    "you live in Claude Code (or any MCP agent) and want your meetings to become memory your agents actually use — verbatim local Markdown, searchable by meaning, recalled unprompted while agents work.",
    "Granola",
    [
        ("Bot joins your call", "No — captures locally", "No — captures locally"),
        ("Speaker labels", "Me / Them by default", "Me / Them"),
        ("The output", "Polished notes and summaries, written for humans",
         "<strong>Verbatim transcripts + a memory layer for agents</strong> — plain Markdown on your disk"),
        ("Transcription", "Cloud ASR (Deepgram / AssemblyAI per Granola's security docs); audio not stored",
         "Local capture; transcription via Gemini (audio sent transiently, then deleted) — disclosed plainly"),
        ("Where your data lives", "Granola's cloud", "<strong>Your disk</strong> — <code>~/transcripts</code> Markdown + a local index"),
        ("Your agents can use it", "No agent interface", "<strong>Any MCP agent</strong> — Claude Code, Codex, anything"),
        ("Beyond meetings", "Meetings only", "Notes, docs, tasks, and lessons agents save — one memory layer"),
        ("Open source", "No", "<strong>Apache-2.0</strong> — read every line that can hear you"),
        ("Price", "Subscription", "Free"),
    ],
    """<h2><span class="hash">##</span> The real difference</h2>
<p>Granola's pipeline ends when a human reads the notes. contorch's ends when an
agent <em>acts</em> on the memory — days later, unprompted, possibly on another
machine. When you told a client "it ships tonight, behind a flag," Granola gives
you a tidy summary containing that promise. contorch makes sure the agent
deploying that fix next week <strong>already knows</strong>, quotes your words
back, and ships it behind the flag.</p>
<p>If your work doesn't involve coding agents, Granola is probably the better
product for you today — genuinely. If it does, notes that only humans can read
are a dead end for the most useful thing your meetings produce: context.</p>""",
)

# ---------------------------------------------------------------- Mem0
page(
    "mem0",
    "contorch vs Mem0 — memory for using agents vs building them",
    "Mem0 is a memory SDK for developers building AI apps. contorch is a memory layer for people who use coding agents — zero integration, fed by your real work. An honest comparison.",
    "Mem0 is memory for agents you build. contorch is memory for agents you use.",
    "Both are open-source memory layers, and both deserve their stars. They just answer different questions: Mem0 asks 'how do I give my app a memory?' — contorch asks 'how do my agents remember my work?'",
    "you're a developer building an AI application and need a memory API — add/search calls, extraction from chat history, a hosted platform to scale on. Mem0 is the category leader at exactly that.",
    "you use Claude Code, Codex, or any MCP agent and want them to remember your project — meetings, decisions, docs, lessons — with zero integration code. Install a daemon; keep working.",
    "Mem0",
    [
        ("You are", "A developer building an agent app", "Someone who <strong>uses</strong> coding agents"),
        ("Integration", "SDK calls in your application code", "<strong>None</strong> — brew install, agents connect over MCP"),
        ("Memory comes from", "What your app explicitly stores — typically extracted from chat sessions",
         "Your actual work: <strong>meetings (spoken words)</strong>, docs, notes, lessons agents save"),
        ("Can it hear a meeting?", "No — its input surface is the API",
         "<strong>Yes — the only memory layer with ears.</strong> Botless macOS capture, Me/Them labeled"),
        ("Runs as", "Library + hosted platform", "Local daemon + MCP server; files on your disk"),
        ("Open source", "Apache-2.0", "Apache-2.0"),
        ("Works together?", "An app built on Mem0 can still read contorch's context over MCP", "—"),
    ],
    """<h2><span class="hash">##</span> Different questions, different layers</h2>
<p>The agent-memory category was built by and for <strong>agent builders</strong>:
you write code against an SDK, and the memory is whatever your application
chooses to store — which in practice means text that already passed through a
chat window. That's the right shape for products.</p>
<p>contorch starts from the other end: you already use excellent agents. What
they lack is your context — and most of your context never gets typed. It's
said in meetings, decided in calls, learned painfully in a deploy at 4:50pm on
a Friday. contorch captures that layer automatically and serves it to whatever
agent asks. No code, no integration, no app to build.</p>""",
)

# ---------------------------------------------------------------- Otter
page(
    "otter",
    "AI meeting notes without a bot — contorch vs Otter",
    "Otter sends a bot to your meetings and stores transcripts in its cloud. contorch captures locally on your Mac — no bot, Markdown on your disk, built to feed coding agents. An honest comparison.",
    "No bot in the room. No cloud archive. Still every word.",
    "Otter is a full transcription service: a bot (OtterPilot) joins your meetings, and transcripts live in Otter's cloud with team features on top. contorch takes the opposite architecture: nothing joins the call — your Mac transcribes what you already hear, into files you own.",
    "you want a mature transcription service with team workspaces, shared archives, mobile apps, and integrations — and you're comfortable with a bot in the room and transcripts in a vendor's cloud.",
    "you'd rather nothing join your calls, want transcripts as plain Markdown on your own disk, and want that context to feed your coding agents over MCP rather than sit in a web archive.",
    "Otter",
    [
        ("How it captures", "A bot (OtterPilot) joins the meeting as a participant",
         "<strong>Nothing joins.</strong> Your Mac transcribes its own audio — the same sound you hear"),
        ("Visible to others", "Bot appears in the participant list", "Nothing visible — you remain responsible for local recording-consent rules (see our docs)"),
        ("Where transcripts live", "Otter's cloud", "<strong>Your disk</strong> — <code>~/transcripts/*.md</code>, grep-able, yours to delete"),
        ("Built for", "Humans reading and sharing notes", "<strong>Agents using context</strong> — plus you, since it's just Markdown"),
        ("Speaker attribution", "Named speakers (with training)", "Me / Them, exact by construction"),
        ("Open source", "No", "<strong>Apache-2.0</strong>"),
        ("Price", "Free tier + subscription", "Free"),
    ],
    """<h2><span class="hash">##</span> Architecture is the feature</h2>
<p>A meeting bot is a third participant: everyone sees it, a vendor's cloud
receives the room's words, and your transcript archive lives behind someone
else's login. Sometimes that's exactly right — teams that live in a shared
archive get real value from it.</p>
<p>contorch's answer is architectural: capture happens on your machine, output
is a folder of Markdown, and the consumer isn't a web app — it's whatever agent
you point at it. Audio goes to one place only (Gemini, transiently, for
transcription — then it's deleted), and we say so plainly rather than
whispering it. If your meetings are going to become memory, you should own
the memory.</p>""",
)

print("generated:", [str(p.relative_to(ROOT)) for p in (ROOT / "vs").rglob("index.html")])

#!/usr/bin/env python3
"""Generate Claude Design preview cards for the contorch design system."""
import pathlib
import shutil

ROOT = pathlib.Path(__file__).parent
DS = ROOT / "ds"

FONTS = '<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,800&family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500&display=swap" rel="stylesheet">'

TOKENS = """
:root{--coal:#16110c;--soot:#211913;--pit:#0e0a07;--line:rgba(244,235,223,.10);
--cream:#f4ebdf;--ash:#a5937f;--flame:#ff6b35;--gold:#ffb454;
--display:"Bricolage Grotesque",system-ui,sans-serif;--body:"IBM Plex Sans",system-ui,sans-serif;
--mono:"IBM Plex Mono",ui-monospace,monospace}
*{margin:0;padding:0;box-sizing:border-box}
body{background:var(--coal);color:var(--cream);font-family:var(--body);line-height:1.65;padding:2.5rem}
a{color:var(--gold);text-decoration:none}
code{font-family:var(--mono);color:var(--gold);font-size:.92em}
"""

TERMINAL_CSS = """
.terminal{background:var(--pit);border:1px solid var(--line);border-radius:12px;max-width:620px;
box-shadow:0 30px 70px rgba(0,0,0,.45),0 0 60px rgba(255,107,53,.07)}
.term-bar{display:flex;align-items:center;gap:.45rem;padding:.7rem 1rem;border-bottom:1px solid var(--line)}
.term-bar i{width:.65rem;height:.65rem;border-radius:50%;background:var(--line)}
.term-bar i:first-child{background:rgba(255,107,53,.55)}
.term-bar span{margin-left:auto;font-family:var(--mono);font-size:.72rem;color:var(--ash)}
.term-body{padding:1.1rem 1.25rem 1.4rem;font-family:var(--mono);font-size:.82rem;line-height:1.75;white-space:pre-wrap}
.tl-dim{color:var(--ash)}.tl-comment{color:#6f6152}.tl-query{color:var(--gold)}
.tl-agent{color:var(--flame)}.tl-cite{color:var(--ash)}
.tl-them{color:var(--cream)}.tl-me{color:var(--gold)}
"""

TERMINAL_HTML = """<div class="terminal">
<div class="term-bar"><i></i><i></i><i></i><span>the context layer</span></div>
<div class="term-body"><span class="tl-dim">● meeting — zoom · 10:02</span>
<span class="tl-them">  Them   can we ship the retry fix before the freeze?</span>
<span class="tl-me">  Me     done — it ships tonight, behind a flag.</span>
<span class="tl-dim">✓ transcript → meeting-2026-07-11.md · indexed
+ doc      auth-spec-v2.pdf → task auth-refactor
+ lesson   "staging deploys need the flag service up first"</span>

<span class="tl-comment"># a week later — new laptop, fresh session, any agent</span>
<span class="tl-query">&gt; pick up the auth-refactor work</span>

<span class="tl-agent">agent</span>   context: 2 meetings · 3 docs · 1 lesson
        The retry fix shipped behind a flag — your words:
        “done — it ships tonight, behind a flag.”
        <span class="tl-cite">→ meeting-2026-07-11.md, 10:02</span></div>
</div>"""


def card(path: str, group: str, name: str, extra_css: str, body: str):
    p = DS / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(
        f'<!-- @dsCard group="{group}" name="{name}" -->\n'
        f'<!DOCTYPE html><html><head><meta charset="utf-8">{FONTS}'
        f"<style>{TOKENS}{extra_css}</style></head><body>{body}</body></html>\n",
        encoding="utf-8",
    )


# --- Brand: palette
sw = ""
for label, var, hexv in [
    ("coal — page", "--coal", "#16110C"), ("soot — cards", "--soot", "#211913"),
    ("pit — terminals", "--pit", "#0E0A07"), ("cream — text", "--cream", "#F4EBDF"),
    ("ash — muted", "--ash", "#A5937F"), ("flame — brand", "--flame", "#FF6B35"),
    ("gold — links", "--gold", "#FFB454"),
]:
    sw += (f'<div class="sw"><div class="chip" style="background:var({var})"></div>'
           f'<p>{label}</p><code>{hexv}</code></div>')
card("brand/palette.html", "Brand", "Palette",
     """.grid{display:grid;grid-template-columns:repeat(4,1fr);gap:1.2rem;max-width:760px}
.chip{height:72px;border-radius:10px;border:1px solid var(--line);margin-bottom:.5rem}
.sw p{font-size:.8rem;color:var(--ash)} .sw code{font-size:.75rem}""",
     f'<div class="grid">{sw}</div>')

# --- Brand: type
card("brand/type.html", "Brand", "Typography",
     """h1{font-family:var(--display);font-weight:800;font-size:3rem;line-height:1.05;letter-spacing:-.015em;margin-bottom:.4rem}
h2{font-family:var(--display);font-weight:600;font-size:1.5rem;margin:1.6rem 0 .3rem}
.lab{font-family:var(--mono);font-size:.72rem;letter-spacing:.18em;text-transform:uppercase;color:var(--flame);margin-top:1.6rem}
.mono{font-family:var(--mono);font-size:.85rem;color:var(--cream)}p{color:var(--ash);max-width:34rem}""",
     """<p class="lab">Display — Bricolage Grotesque 800</p>
<h1>Give your agents a&nbsp;memory.</h1>
<p class="lab">Heading — Bricolage Grotesque 600</p>
<h2>Any agent picks up where you left off.</h2>
<p class="lab">Body — IBM Plex Sans 400</p>
<p>contorch is a local, persistent context layer for coding agents. Meetings transcribe themselves, tasks and sources accumulate, repo knowledge sticks.</p>
<p class="lab">Terminal — IBM Plex Mono</p>
<p class="mono">$ curl -fsSL contorch.com/install | bash</p>""")

# --- Brand: logo
shutil.copy(ROOT / "logo-512.png", DS / "brand" / "logo-512.png")
card("brand/logo.html", "Brand", "Logomark",
     """.row{display:flex;gap:2.5rem;align-items:center}
.tile{display:flex;align-items:center;justify-content:center;width:180px;height:180px;border-radius:14px;border:1px solid var(--line)}
.brand{display:flex;align-items:center;gap:.65rem;font-family:var(--display);font-weight:800;font-size:1.3rem}
p{color:var(--ash);font-size:.85rem;margin-top:1.2rem;max-width:30rem}""",
     """<div class="row">
<div class="tile" style="background:var(--coal)"><img src="logo-512.png" width="84" alt="contorch mark"></div>
<div class="tile" style="background:var(--pit)"><div class="brand"><img src="logo-512.png" width="26" style="height:auto"> contorch</div></div>
</div><p>The C-flame mark: a C whose upper curl flickers into flame — context, carried like a torch. Vermilion mark on warm coal; never on white in product surfaces.</p>""")

# --- Component: terminal
card("components/terminal.html", "Components", "Recall terminal", TERMINAL_CSS, TERMINAL_HTML)

# --- Component: install CTA
card("components/install-cta.html", "Components", "Install command",
     """.install-cta{display:flex;max-width:34rem;border:1px solid var(--line);border-radius:10px;background:var(--pit);overflow:hidden}
.install-cta code{flex:1;padding:.85rem 1.1rem;font-family:var(--mono);font-size:.9rem;color:var(--cream);white-space:nowrap}
.install-cta .prompt{color:var(--flame)}
.install-cta button{border:0;border-left:1px solid var(--line);background:var(--soot);color:var(--gold);font-family:var(--mono);font-size:.8rem;padding:0 1.1rem;cursor:pointer}
.note{margin-top:.9rem;font-family:var(--mono);font-size:.78rem;color:var(--ash)}""",
     """<div class="install-cta"><code><span class="prompt">$</span> curl -fsSL contorch.com/install | bash</code><button>Copy</button></div>
<p class="note">Free · Apache-2.0 · local-first</p>""")

# --- Section: hero
card("sections/hero.html", "Sections", "Hero",
     TERMINAL_CSS + """
.hero{display:grid;grid-template-columns:1.05fr 1fr;gap:3rem;align-items:center;max-width:1080px}
.eyebrow{font-family:var(--mono);font-size:.8rem;letter-spacing:.22em;text-transform:uppercase;color:var(--flame);margin-bottom:1.1rem}
h1{font-family:var(--display);font-weight:800;font-size:3.4rem;line-height:1.04;letter-spacing:-.015em;margin-bottom:1.3rem}
.sub{color:var(--ash);max-width:34rem;margin-bottom:2rem}
.install-cta{display:flex;max-width:34rem;border:1px solid var(--line);border-radius:10px;background:var(--pit);overflow:hidden}
.install-cta code{flex:1;padding:.85rem 1.1rem;font-family:var(--mono);font-size:.9rem;color:var(--cream);white-space:nowrap}
.install-cta .prompt{color:var(--flame)}
.install-cta button{border:0;border-left:1px solid var(--line);background:var(--soot);color:var(--gold);font-family:var(--mono);font-size:.8rem;padding:0 1.1rem}""",
     f"""<div class="hero"><div>
<p class="eyebrow">context + torch</p>
<h1>Give your agents a&nbsp;memory.</h1>
<p class="sub">contorch is a local, persistent context layer for coding agents. Meetings transcribe themselves, tasks and sources accumulate, repo knowledge sticks — and any agent that speaks MCP can search all of it, in any session, on any day.</p>
<div class="install-cta"><code><span class="prompt">$</span> curl -fsSL contorch.com/install | bash</code><button>Copy</button></div>
</div>{TERMINAL_HTML}</div>""")

# --- Section: thesis
card("sections/thesis.html", "Sections", "Thesis interstitial",
     """.thesis{padding:3.5rem 0;border-top:1px solid var(--line);border-bottom:1px solid var(--line);text-align:center}
.thesis p{font-family:var(--display);font-weight:600;font-size:1.9rem;line-height:1.35}
.thesis span{color:var(--gold)}""",
     """<section class="thesis"><p>Most of what an agent needs already happened —<br>in a conversation, a doc, a lesson learned.<br><span>contorch just keeps it.</span></p></section>""")

# --- Section: sources (where context comes from)
SOURCE_CSS = """.grid{display:grid;grid-template-columns:repeat(2,1fr);gap:1.4rem;max-width:1000px}
.card{background:var(--soot);border:1px solid var(--line);border-radius:12px;padding:1.5rem 1.4rem}
.k{font-family:var(--mono);font-size:.75rem;letter-spacing:.12em;text-transform:uppercase;color:var(--flame);margin-bottom:.7rem}
.tag{display:inline-block;margin-left:.5rem;padding:.1rem .5rem;border:1px solid var(--line);border-radius:99px;color:var(--ash)}
h3{font-family:var(--display);font-weight:600;font-size:1.25rem;margin-bottom:.6rem}
.card p:not(.k){color:var(--ash);font-size:.93rem;margin-bottom:.8rem}
.card pre{background:var(--pit);border:1px solid var(--line);border-radius:8px;padding:.75rem .95rem;overflow-x:auto}
.card pre code{color:var(--ash);font-size:.78rem;line-height:1.7;display:block}
.tl-them{color:var(--cream)}.tl-me{color:var(--gold)}"""
card("sections/sources.html", "Sections", "Where context comes from", SOURCE_CSS,
     """<div class="grid">
<div class="card"><p class="k">Conversations <span class="tag">automatic</span></p><h3>Your meetings, word for word.</h3><p>Take the call like always. Both sides — Me and Them — land as Markdown. No bot joins.</p><pre><code><span class="tl-them">Them</span>  can we ship it before the freeze?
<span class="tl-me">Me</span>    done — it ships tonight.</code></pre></div>
<div class="card"><p class="k">Docs &amp; links <span class="tag">one drop</span></p><h3>The spec lives with the task.</h3><p>Files, PRs, dashboards attach to the work they belong to.</p><pre><code>+ add_source auth-spec-v2.pdf → auth-refactor</code></pre></div>
<div class="card"><p class="k">Decisions &amp; notes <span class="tag">one line</span></p><h3>Say it once, never again.</h3><p>Stop re-explaining project state to every fresh chat window.</p><pre><code>+ note "JWT rotation ships behind a flag"</code></pre></div>
<div class="card"><p class="k">Lessons agents learn <span class="tag">automatic</span></p><h3>Hard-won knowledge stays won.</h3><p>The next agent — or the next laptop — doesn't rediscover it.</p><pre><code>+ lesson "staging needs the flag service up first"</code></pre></div>
</div>""")

# --- Section: recall (what you get back)
card("sections/recall.html", "Sections", "What you get back",
     """.qa-list{display:grid;gap:1.1rem;max-width:46rem}
.qa{border-left:2px solid var(--flame);padding:.2rem 0 .2rem 1.2rem}
.q{font-family:var(--mono);font-size:.95rem;color:var(--gold);margin-bottom:.3rem}
.a{color:var(--ash);font-size:.95rem}
.cite{font-family:var(--mono);font-size:.78rem;color:#6f6152}""",
     """<div class="qa-list">
<div class="qa"><p class="q">&gt; what did we decide about pricing?</p><p class="a">Usage-based; the annual discount is parked until Q4. <span class="cite">→ meeting-2026-07-08.md, 14:31</span></p></div>
<div class="qa"><p class="q">&gt; pick up the auth-refactor work</p><p class="a">Loads the full manifest — 3 sources, 2 meetings, 1 lesson — and starts where you stopped.</p></div>
<div class="qa"><p class="q">&gt; why does staging keep failing?</p><p class="a">A lesson saved on Jun 12: staging deploys need the flag service up first. <span class="cite">→ repo knowledge</span></p></div>
</div>""")

# --- Full page: the real site, synced as-is for whole-page review
pages = DS / "pages"
pages.mkdir(exist_ok=True)
index = (ROOT / "index.html").read_text(encoding="utf-8")
(pages / "home.html").write_text(
    '<!-- @dsCard group="Pages" name="contorch.com — full page" -->\n' + index,
    encoding="utf-8",
)
for f in ["styles.css", "script.js", "logo-512.png", "favicon-64.png"]:
    shutil.copy(ROOT / f, pages / f)

print("cards:", sorted(str(p.relative_to(DS)) for p in DS.rglob("*") if p.is_file()))

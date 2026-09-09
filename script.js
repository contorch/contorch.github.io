// contorch.com — rotating hero demo + copy buttons. No dependencies.
// Three scenarios, each the same loop: capture → task → recall with a citation.

(function () {
  // Copy buttons read the command from the DOM (data-cmd on the <code>), so the
  // displayed and copied commands can never drift apart.
  function commandFor(btn) {
    var sel = btn.getAttribute("data-copy");
    var code = sel === "prev"
      ? btn.previousElementSibling
      : sel ? document.querySelector(sel)
      : btn.parentElement.querySelector("code[data-cmd]");
    return code ? code.getAttribute("data-cmd") : null;
  }
  Array.prototype.forEach.call(document.querySelectorAll("#copy-btn, button.copy"), function (btn) {
    btn.addEventListener("click", function () {
      var cmd = commandFor(btn);
      if (!cmd) return;
      navigator.clipboard.writeText(cmd).then(function () {
        var label = btn.textContent;
        btn.textContent = btn.id === "copy-btn" ? "Copied — now permissions ↓" : "Copied";
        setTimeout(function () { btn.textContent = label; }, 2200);
      });
    });
  });

  // Lines with `h: true` are trusted static HTML (two-tone annotations).
  // Speakers are only ever Me / Them — that is what capture actually labels.
  var SCENARIOS = [
    [
      { t: "● meeting — zoom · 10:02", c: "tl-dim", d: 550 },
      { t: "  Them   can we ship the retry fix before the freeze?", c: "tl-them", d: 900 },
      { t: "  Me     done — it ships tonight, behind a flag.", c: "tl-me", d: 900 },
      { t: "✓ saved → ~/transcripts/meeting-2026-07-11.md", c: "tl-dim", d: 600 },
      { t: "+ lesson  \"staging needs the flag service first\"", c: "tl-dim", d: 800 },
      { t: " ", c: "", d: 800 },
      { t: "# a week later — a fresh session on this Mac", c: "tl-comment", d: 700 },
      { t: "> deploy the retry fix to staging", c: "tl-query", d: 300, type: true },
      { t: "agent  working…", c: "tl-agent", d: 750 },
      { t: "  ◆ staging needs the flag service first <span class=\"ann\">· saved lesson</span>", c: "tl-recall", d: 950, h: true },
      { t: "  flag service up ✓ · deploying… ✓", c: "tl-answer", d: 800 },
      { t: "  ◆ “it ships tonight, behind a flag” <span class=\"ann\">· meeting-2026-07-11.md, 10:02</span>", c: "tl-recall", d: 950, h: true },
      { t: "  done — behind the flag, promise kept.", c: "tl-answer", d: 400 }
    ],
    [
      { t: "● retro — after the outage · May 2", c: "tl-dim", d: 550 },
      { t: "  Me     new rule: we don't deploy on Fridays.", c: "tl-me", d: 950 },
      { t: "✓ saved → ~/transcripts/meeting-2026-05-02.md", c: "tl-dim", d: 800 },
      { t: " ", c: "", d: 800 },
      { t: "# five weeks later — Friday, 4:50pm", c: "tl-comment", d: 700 },
      { t: "> ship the checkout fix", c: "tl-query", d: 300, type: true },
      { t: "agent  working…", c: "tl-agent", d: 750 },
      { t: "  ◆ “we don't deploy on Fridays” <span class=\"ann\">· meeting-2026-05-02.md</span>", c: "tl-recall", d: 1000, h: true },
      { t: "  it's Friday. Your retro rule says wait — ship anyway?", c: "tl-answer", d: 400 }
    ],
    [
      { t: "● standup · Tuesday", c: "tl-dim", d: 550 },
      { t: "  Them   ranking is mine now — route changes through me.", c: "tl-them", d: 950 },
      { t: "✓ saved → ~/transcripts/meeting-2026-07-07.md", c: "tl-dim", d: 800 },
      { t: " ", c: "", d: 800 },
      { t: "# the following week", c: "tl-comment", d: 700 },
      { t: "> open a PR for the ranking tweak", c: "tl-query", d: 300, type: true },
      { t: "agent  working…", c: "tl-agent", d: 750 },
      { t: "  ◆ ranking changes now route through its owner <span class=\"ann\">· meeting-2026-07-07.md</span>", c: "tl-recall", d: 1000, h: true },
      { t: "  PR drafted — noted the owner change in the description.", c: "tl-answer", d: 400 }
    ]
  ];
  var REST_MS = 4000;   // pause on a finished scenario before rotating
  var FADE_MS = 380;    // matches the CSS opacity transition

  var body = document.getElementById("term-body");
  var terminal = document.getElementById("terminal");
  if (!body || !terminal) return;

  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var current = 0;
  var timer = null;
  var playToken = 0; // invalidates in-flight line callbacks on scenario switch

  // Scenario dots in the terminal title bar.
  var bar = terminal.querySelector(".term-bar");
  var dots = [];
  if (bar) {
    var dotWrap = document.createElement("div");
    dotWrap.className = "term-dots";
    SCENARIOS.forEach(function (_, i) {
      var b = document.createElement("button");
      b.type = "button";
      b.setAttribute("aria-label", "Show example " + (i + 1));
      b.addEventListener("click", function () { show(i, true); });
      dotWrap.appendChild(b);
      dots.push(b);
    });
    bar.insertBefore(dotWrap, bar.querySelector("span"));
  }

  function markDot(i) {
    dots.forEach(function (d, j) { d.className = j === i ? "on" : ""; });
  }

  function setLine(div, l) {
    if (l.h) { div.innerHTML = l.t; } else { div.textContent = l.t; }
  }

  function renderAll(lines) {
    body.innerHTML = "";
    lines.forEach(function (l) {
      var div = document.createElement("div");
      setLine(div, l);
      if (l.c) div.className = l.c;
      body.appendChild(div);
    });
  }

  function typeLine(div, text, token, done) {
    var i = 0;
    div.classList.add("cursor");
    (function tick() {
      if (token !== playToken) return;
      div.textContent = text.slice(0, i);
      i++;
      if (i <= text.length) {
        setTimeout(tick, 34);
      } else {
        div.classList.remove("cursor");
        done();
      }
    })();
  }

  function play(lines, idx, token) {
    if (token !== playToken) return;
    if (idx >= lines.length) {
      timer = setTimeout(function () { show((current + 1) % SCENARIOS.length, false); }, REST_MS);
      return;
    }
    var l = lines[idx];
    var div = document.createElement("div");
    if (l.c) div.className = l.c;
    body.appendChild(div);
    if (l.type && !reduced) {
      setTimeout(function () {
        typeLine(div, l.t, token, function () {
          setTimeout(function () { play(lines, idx + 1, token); }, l.d);
        });
      }, 250);
    } else {
      setLine(div, l);
      timer = setTimeout(function () { play(lines, idx + 1, token); }, l.d);
    }
  }

  function show(i, immediate) {
    clearTimeout(timer);
    playToken++;
    current = i;
    markDot(i);
    if (reduced) {
      renderAll(SCENARIOS[i]);
      return;
    }
    var token = playToken;
    var start = function () {
      if (token !== playToken) return;
      body.innerHTML = "";
      body.classList.remove("fading");
      play(SCENARIOS[i], 0, token);
    };
    if (immediate || !body.children.length) {
      start();
    } else {
      body.classList.add("fading");
      setTimeout(start, FADE_MS);
    }
  }

  if (reduced) {
    markDot(0);
    renderAll(SCENARIOS[0]);
    return; // dots still switch scenarios; no auto-rotation
  }

  var started = false;
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting && !started) {
        started = true;
        io.disconnect();
        markDot(0);
        setTimeout(function () { show(0, true); }, 400);
      }
    });
  }, { threshold: 0.35 });
  io.observe(terminal);
})();

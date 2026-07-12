// contorch.com — terminal recall demo + copy button. No dependencies.

(function () {
  var copyBtn = document.getElementById("copy-btn");
  if (copyBtn) {
    copyBtn.addEventListener("click", function () {
      navigator.clipboard.writeText("curl -fsSL contorch.com/install | bash").then(function () {
        copyBtn.textContent = "Copied";
        setTimeout(function () { copyBtn.textContent = "Copy"; }, 1800);
      });
    });
  }

  // Lines with `h: true` are trusted static HTML (two-tone annotations).
  var LINES = [
    { t: "● meeting — zoom · 10:02", c: "tl-dim", d: 550 },
    { t: "  Them   can we ship the retry fix before the freeze?", c: "tl-them", d: 900 },
    { t: "  Me     done — it ships tonight, behind a flag.", c: "tl-me", d: 900 },
    { t: "✓ indexed → meeting-2026-07-11.md", c: "tl-dim", d: 600 },
    { t: "+ lesson  \"staging needs the flag service first\"", c: "tl-dim", d: 800 },
    { t: " ", c: "", d: 800 },
    { t: "# a week later — new laptop, fresh session, any agent", c: "tl-comment", d: 700 },
    { t: "> deploy the retry fix to staging", c: "tl-query", d: 300, type: true },
    { t: "agent  working…", c: "tl-agent", d: 750 },
    { t: "  ◆ staging needs the flag service first <span class=\"ann\">· nobody asked</span>", c: "tl-recall", d: 950, h: true },
    { t: "  flag service up ✓ · deploying… ✓", c: "tl-answer", d: 800 },
    { t: "  ◆ “it ships tonight, behind a flag” <span class=\"ann\">· your words, 10:02</span>", c: "tl-recall", d: 950, h: true },
    { t: "  done — behind the flag, promise kept.", c: "tl-answer", d: 400 }
  ];

  var body = document.getElementById("term-body");
  var terminal = document.getElementById("terminal");
  if (!body || !terminal) return;

  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function setLine(div, l) {
    if (l.h) { div.innerHTML = l.t; } else { div.textContent = l.t; }
  }

  function renderAll() {
    LINES.forEach(function (l) {
      var div = document.createElement("div");
      setLine(div, l);
      if (l.c) div.className = l.c;
      body.appendChild(div);
    });
  }

  function typeLine(div, text, done) {
    var i = 0;
    div.classList.add("cursor");
    (function tick() {
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

  function play(idx) {
    if (idx >= LINES.length) return;
    var l = LINES[idx];
    var div = document.createElement("div");
    if (l.c) div.className = l.c;
    body.appendChild(div);
    if (l.type && !reduced) {
      setTimeout(function () {
        typeLine(div, l.t, function () { setTimeout(function () { play(idx + 1); }, l.d); });
      }, 250);
    } else {
      setLine(div, l);
      setTimeout(function () { play(idx + 1); }, l.d);
    }
  }

  if (reduced) {
    renderAll();
    return;
  }

  var started = false;
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting && !started) {
        started = true;
        io.disconnect();
        setTimeout(function () { play(0); }, 400);
      }
    });
  }, { threshold: 0.35 });
  io.observe(terminal);
})();

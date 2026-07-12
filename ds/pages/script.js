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

  var LINES = [
    { t: "● meeting — zoom · 10:02", c: "tl-dim", d: 550 },
    { t: "  Them   can we ship the retry fix before the freeze?", c: "tl-them", d: 900 },
    { t: "  Me     done — it ships tonight, behind a flag.", c: "tl-me", d: 900 },
    { t: "✓ transcript → meeting-2026-07-11.md · indexed", c: "tl-dim", d: 700 },
    { t: "+ doc      auth-spec-v2.pdf → task auth-refactor", c: "tl-dim", d: 550 },
    { t: "+ lesson   \"staging deploys need the flag service up first\"", c: "tl-dim", d: 750 },
    { t: " ", c: "", d: 800 },
    { t: "# a week later — new laptop, fresh session, any agent", c: "tl-comment", d: 700 },
    { t: "> pick up the auth-refactor work", c: "tl-query", d: 300, type: true },
    { t: " ", c: "", d: 650 },
    { t: "agent   context: 2 meetings · 3 docs · 1 lesson", c: "tl-agent", d: 850 },
    { t: "        The retry fix shipped behind a flag — your words:", c: "tl-answer", d: 420 },
    { t: "        “done — it ships tonight, behind a flag.”", c: "tl-answer", d: 420 },
    { t: "        → meeting-2026-07-11.md, 10:02", c: "tl-cite", d: 400 }
  ];

  var body = document.getElementById("term-body");
  var terminal = document.getElementById("terminal");
  if (!body || !terminal) return;

  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function renderAll() {
    LINES.forEach(function (l) {
      var div = document.createElement("div");
      div.textContent = l.t;
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
      div.textContent = l.t;
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

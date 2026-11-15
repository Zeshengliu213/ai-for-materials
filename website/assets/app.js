/* ==========================================================================
   AI for Materials Science — Course Portal Client Helpers

   Markdown and syntax highlighting are rendered at build time, so this file
   only handles: KaTeX math, copy buttons, site search, table-of-contents
   scroll-spy, the solution gate, study-progress tracking and the module
   filter.
   Works over HTTP(S) and over the local file:// protocol.
   ========================================================================== */

(function () {
  "use strict";

  var SOLUTION_STORAGE_KEY = "ai4m-solution-revealed";
  var PROGRESS_STORAGE_KEY = "ai4m-progress";
  var THEME_STORAGE_KEY = "ai4m-theme";

  /* ------------------------------------------------------- screen readers */

  var liveRegion = null;

  function announce(message) {
    if (!liveRegion) {
      liveRegion = document.createElement("div");
      liveRegion.className = "visually-hidden";
      liveRegion.setAttribute("role", "status");
      liveRegion.setAttribute("aria-live", "polite");
      document.body.appendChild(liveRegion);
    }
    liveRegion.textContent = message;
  }

  /* ----------------------------------------------------------- dark theme */

  function initThemeToggle() {
    var button = document.getElementById("theme-toggle");
    if (!button) return;

    function current() {
      return document.documentElement.getAttribute("data-theme") === "dark" ? "dark" : "light";
    }

    function apply(theme) {
      document.documentElement.setAttribute("data-theme", theme);
      button.setAttribute("aria-pressed", theme === "dark" ? "true" : "false");
    }

    apply(current());

    button.addEventListener("click", function () {
      var next = current() === "dark" ? "light" : "dark";
      apply(next);
      try { localStorage.setItem(THEME_STORAGE_KEY, next); } catch (e) { /* ignore */ }
      announce(next === "dark" ? "已切换到深色主题" : "已切换到浅色主题");
    });

    if (window.matchMedia) {
      var media = window.matchMedia("(prefers-color-scheme: dark)");
      var onChange = function (event) {
        var stored = null;
        try { stored = localStorage.getItem(THEME_STORAGE_KEY); } catch (e) { /* ignore */ }
        if (!stored) apply(event.matches ? "dark" : "light");
      };
      if (media.addEventListener) media.addEventListener("change", onChange);
      else if (media.addListener) media.addListener(onChange);
    }
  }

  /* ---------------------------------------------------------------- math */

  function renderMath() {
    if (typeof katex === "undefined") return;
    document.querySelectorAll(".math-inline, .math-block").forEach(function (el) {
      var tex = el.getAttribute("data-tex");
      if (!tex) return;
      try {
        katex.render(tex, el, {
          displayMode: el.classList.contains("math-block"),
          throwOnError: false,
          strict: false,
        });
      } catch (e) {
        /* Leave the raw TeX in place when it cannot be parsed. */
      }
    });
  }

  /* ------------------------------------------------------------ copy code */

  function initCopyButtons() {
    document.querySelectorAll(".nb-copy-btn").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var cell = btn.closest(".nb-cell-code");
        var codeEl = cell && cell.querySelector("pre");
        if (!codeEl) return;
        var text = codeEl.innerText;
        if (!navigator.clipboard || !navigator.clipboard.writeText) return;
        navigator.clipboard.writeText(text).then(function () {
          var old = btn.textContent;
          btn.textContent = "已复制";
          announce("代码已复制到剪贴板");
          setTimeout(function () { btn.textContent = old; }, 1500);
        });
      });
    });
  }

  /* ------------------------------------------------------- module filter */

  function initModuleFilter() {
    var input = document.getElementById("module-search");
    if (!input) return;
    var cards = document.querySelectorAll(".module-card");
    input.addEventListener("input", function () {
      var q = input.value.trim().toLowerCase();
      cards.forEach(function (card) {
        var text = card.textContent.toLowerCase();
        card.style.display = !q || text.indexOf(q) !== -1 ? "" : "none";
      });
    });
  }

  /* ---------------------------------------------------------- site search */

  var KIND_LABEL = { module: "模块", notebook: "课件", solution: "答案" };

  function scoreEntry(entry, query) {
    var title = entry.title.toLowerCase();
    var text = (entry.text || "").toLowerCase();
    if (title.indexOf(query) !== -1) return 100 - title.indexOf(query);
    var hit = text.indexOf(query);
    if (hit !== -1) return 50 - Math.min(hit / 50, 40);
    return 0;
  }

  function excerptAround(text, query) {
    var lower = text.toLowerCase();
    var hit = lower.indexOf(query);
    if (hit === -1) return text.slice(0, 90);
    var start = Math.max(0, hit - 30);
    return (start > 0 ? "…" : "") + text.slice(start, start + 100) + "…";
  }

  function escapeHtml(value) {
    var div = document.createElement("div");
    div.textContent = value == null ? "" : String(value);
    return div.innerHTML;
  }

  function initSiteSearch() {
    var input = document.getElementById("site-search");
    var panel = document.getElementById("site-search-results");
    var index = window.AI4M_SEARCH_INDEX;
    if (!input || !panel) return;
    if (!index || !index.length) {
      var wrapper = input.closest(".global-search");
      if (wrapper) wrapper.hidden = true;
      return;
    }
    var base = window.AI4M_BASE || "";

    function close() {
      panel.hidden = true;
      panel.innerHTML = "";
    }

    function run() {
      var query = input.value.trim().toLowerCase();
      if (query.length < 1) return close();

      var hits = index
        .map(function (entry) { return { entry: entry, score: scoreEntry(entry, query) }; })
        .filter(function (item) { return item.score > 0; })
        .sort(function (a, b) { return b.score - a.score; })
        .slice(0, 12);

      if (!hits.length) {
        panel.innerHTML = '<div class="search-empty">没有找到匹配内容</div>';
        panel.hidden = false;
        return;
      }

      panel.innerHTML = hits
        .map(function (item) {
          var entry = item.entry;
          return (
            '<a class="search-hit" role="option" href="' + base + escapeHtml(entry.href) + '">' +
            '<span class="search-hit-kind search-kind-' + escapeHtml(entry.kind) + '">' +
            escapeHtml(KIND_LABEL[entry.kind] || entry.kind) + " " + escapeHtml(entry.module) +
            "</span>" +
            '<span class="search-hit-title">' + escapeHtml(entry.title) + "</span>" +
            '<span class="search-hit-text">' +
            escapeHtml(excerptAround(entry.text || "", query)) + "</span>" +
            "</a>"
          );
        })
        .join("");
      panel.hidden = false;
    }

    input.addEventListener("input", run);
    input.addEventListener("focus", run);
    input.addEventListener("keydown", function (event) {
      if (event.key === "Escape") { input.blur(); close(); }
      if (event.key === "Enter") {
        var first = panel.querySelector(".search-hit");
        if (first) window.location.href = first.getAttribute("href");
      }
    });
    document.addEventListener("click", function (event) {
      if (!event.target.closest(".global-search")) close();
    });
    document.addEventListener("keydown", function (event) {
      if (event.key === "/" && document.activeElement !== input) {
        event.preventDefault();
        input.focus();
      }
    });
  }

  /* ------------------------------------------------------ study progress */

  /* Completed notebooks are stored as a map of page href -> 1 in
     localStorage. Every surface (module table, home cards, sidebar, the
     buttons on a notebook page) reads the same map, so a tick made anywhere
     shows up everywhere on the next render. */

  function readProgress() {
    try {
      var raw = localStorage.getItem(PROGRESS_STORAGE_KEY);
      var parsed = raw ? JSON.parse(raw) : null;
      return parsed && typeof parsed === "object" ? parsed : {};
    } catch (e) {
      return {};
    }
  }

  function writeProgress(state) {
    try {
      localStorage.setItem(PROGRESS_STORAGE_KEY, JSON.stringify(state));
    } catch (e) { /* private mode or full quota: progress is best-effort */ }
  }

  function splitKeys(value) {
    return (value || "")
      .split(",")
      .map(function (key) { return key.trim(); })
      .filter(function (key) { return key.length > 0; });
  }

  function paintProgress() {
    var state = readProgress();

    document.querySelectorAll(".progress-check").forEach(function (box) {
      box.checked = state[box.getAttribute("data-progress-key")] === 1;
    });

    document.querySelectorAll("[data-progress-toggle]").forEach(function (btn) {
      var done = state[btn.getAttribute("data-progress-key")] === 1;
      btn.setAttribute("aria-pressed", done ? "true" : "false");
      btn.classList.toggle("btn-progress-done", done);
      btn.textContent = done ? "☑ 已学完（点击取消）" : "☐ 标记为已学完";
    });

    document.querySelectorAll("[data-progress-mark]").forEach(function (link) {
      link.classList.toggle(
        "progress-marked",
        state[link.getAttribute("data-progress-mark")] === 1
      );
    });

    document.querySelectorAll("[data-progress-keys]").forEach(function (panel) {
      var keys = splitKeys(panel.getAttribute("data-progress-keys"));
      var done = keys.filter(function (key) { return state[key] === 1; }).length;
      var pct = keys.length ? Math.round((done / keys.length) * 100) : 0;
      var fill = panel.querySelector("[data-progress-fill]");
      var count = panel.querySelector("[data-progress-count]");
      if (fill) fill.style.width = pct + "%";
      if (count) count.textContent = done + " / " + keys.length;
      panel.classList.toggle("progress-complete", keys.length > 0 && done === keys.length);
    });
  }

  function setDone(key, done) {
    if (!key) return;
    var state = readProgress();
    if (done) state[key] = 1;
    else delete state[key];
    writeProgress(state);
    paintProgress();
  }

  function initProgress() {
    document.querySelectorAll(".progress-check").forEach(function (box) {
      box.addEventListener("change", function () {
        setDone(box.getAttribute("data-progress-key"), box.checked);
        announce(box.checked ? "已标记为学完" : "已取消标记");
      });
    });

    document.querySelectorAll("[data-progress-toggle]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var key = btn.getAttribute("data-progress-key");
        var done = readProgress()[key] !== 1;
        setDone(key, done);
        announce(done ? "已标记为学完" : "已取消标记");
      });
    });

    var reset = document.getElementById("progress-reset");
    if (reset) {
      reset.addEventListener("click", function () {
        if (!window.confirm("确定清空本浏览器记录的全部学习进度吗？此操作不可撤销。")) return;
        try { localStorage.removeItem(PROGRESS_STORAGE_KEY); } catch (e) { /* ignore */ }
        paintProgress();
        announce("学习进度已重置");
      });
    }

    paintProgress();

    /* Keep tabs in sync: ticking a notebook in one tab updates the others. */
    window.addEventListener("storage", function (event) {
      if (!event.key || event.key === PROGRESS_STORAGE_KEY) paintProgress();
    });
  }

  /* ------------------------------------------------------------------ toc */

  function initToc() {
    var links = document.querySelectorAll(".toc-list a");
    if (!links.length || !("IntersectionObserver" in window)) return;

    var byId = {};
    links.forEach(function (link) {
      var id = decodeURIComponent(link.getAttribute("href").slice(1));
      byId[id] = link;
    });

    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          links.forEach(function (link) { link.classList.remove("toc-active"); });
          var link = byId[entry.target.id];
          if (link) link.classList.add("toc-active");
        });
      },
      { rootMargin: "-80px 0px -70% 0px", threshold: 0 }
    );

    Object.keys(byId).forEach(function (id) {
      var target = document.getElementById(id);
      if (target) observer.observe(target);
    });
  }

  /* -------------------------------------------------------- solution gate */

  function initSolutionGate() {
    var gate = document.getElementById("solution-gate");
    var body = document.getElementById("solution-body");
    var button = document.getElementById("solution-reveal");
    if (!gate || !body || !button) return;

    function reveal() {
      gate.hidden = true;
      body.hidden = false;
      renderMath();
    }

    try {
      if (sessionStorage.getItem(SOLUTION_STORAGE_KEY) === "1") {
        reveal();
        return;
      }
    } catch (e) { /* private mode: fall through to the gate */ }

    button.addEventListener("click", function () {
      try { sessionStorage.setItem(SOLUTION_STORAGE_KEY, "1"); } catch (e) { /* ignore */ }
      reveal();
    });
  }

  /* ------------------------------------------------------- mobile sidebar */

  function initResponsiveDisclosures() {
    if (window.matchMedia && window.matchMedia("(max-width: 900px)").matches) {
      document.querySelectorAll(".sidebar-disclosure, .toc-disclosure").forEach(function (el) {
        el.removeAttribute("open");
      });
    }
  }

  document.addEventListener("DOMContentLoaded", function () {
    initThemeToggle();
    renderMath();
    initCopyButtons();
    initModuleFilter();
    initSiteSearch();
    initToc();
    initProgress();
    initSolutionGate();
    initResponsiveDisclosures();
  });
})();

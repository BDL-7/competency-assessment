(() => {
  "use strict";

  const deckData = window.DECK;
  const speakerNotes = window.SPEAKER_NOTES || {};
  if (!deckData || !Array.isArray(deckData.slides)) {
    throw new Error("deck-content.js must define window.DECK with a slides array.");
  }

  const visualStyle = {
    fontFamily: deckData.meta?.visualStyle?.fontFamily || "system-sans",
    fontScale: deckData.meta?.visualStyle?.fontScale || "standard",
    colorScheme: deckData.meta?.visualStyle?.colorScheme || "midnight"
  };
  const fontFamilies = new Set(["system-sans", "humanist-sans", "scientific-serif"]);
  const colorSchemes = new Set(["midnight", "graphite", "deep-ocean"]);
  const fontScaleFactors = { compact: 0.92, standard: 1, large: 1.08 };
  document.documentElement.dataset.fontFamily = fontFamilies.has(visualStyle.fontFamily)
    ? visualStyle.fontFamily
    : "system-sans";
  document.documentElement.dataset.colorScheme = colorSchemes.has(visualStyle.colorScheme)
    ? visualStyle.colorScheme
    : "midnight";

  const deckEl = document.getElementById("deck");
  const countEl = document.getElementById("count");
  const colorMap = {
    blue: "var(--blue)",
    cyan: "var(--cyan)",
    purple: "var(--purple)",
    pink: "var(--pink)",
    green: "var(--green)",
    amber: "var(--amber)",
    red: "var(--red)"
  };

  const esc = (value = "") => String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");

  const accentClass = (name) => name ? `accent-${esc(name)}` : "";
  const accentStyle = (name) => colorMap[name] || colorMap.blue;

  function renderTitle(title, highlight) {
    const safeTitle = esc(title || "Untitled slide");
    if (!highlight) return safeTitle;
    const safeHighlight = esc(highlight);
    const index = safeTitle.indexOf(safeHighlight);
    if (index < 0) return safeTitle;
    return `${safeTitle.slice(0, index)}<span>${safeHighlight}</span>${safeTitle.slice(index + safeHighlight.length)}`;
  }

  function renderBullets(items = [], ordered = false) {
    if (!items.length) return "";
    const tag = ordered ? "ol" : "ul";
    const cls = ordered ? "clean numbered" : "clean";
    const rows = items.map((item) => {
      const text = typeof item === "string" ? esc(item) : (item.html || esc(item.text || ""));
      return `<li>${text}</li>`;
    }).join("");
    return `<${tag} class="${cls}">${rows}</${tag}>`;
  }

  function renderChips(chips = []) {
    if (!chips.length) return "";
    return `<div class="chips">${chips.map((chip) => `<i class="chip">${esc(chip)}</i>`).join("")}</div>`;
  }

  function renderTopbar(slide, index, total) {
    const bars = Array.from({ length: total }, (_, i) => {
      const cls = i < index ? "done" : (i === index ? "on" : "");
      return `<i class="${cls}"></i>`;
    }).join("");
    return `
      <div class="topbar">
        <div class="deck-id">${esc(deckData.meta?.shortTitle || deckData.meta?.title || "Presentation")}</div>
        <div class="progress">
          <div class="progress-label">${esc(slide.section || "Slide")} &middot; ${index + 1}/${total}</div>
          <div class="progress-bars">${bars}</div>
        </div>
      </div>`;
  }

  function renderHeading(slide) {
    return `
      <h1>${renderTitle(slide.title, slide.highlight)}</h1>
      ${slide.subtitle ? `<div class="subtitle">${esc(slide.subtitle)}</div>` : ""}`;
  }

  function renderCard(card, index, numbered) {
    return `
      <article class="card ${accentClass(card.accent)}">
        ${numbered ? `<div class="card-number">${index + 1}</div>` : ""}
        ${card.label ? `<div class="eyebrow">${esc(card.label)}</div>` : ""}
        ${card.value ? `<div class="big-number">${esc(card.value)}</div>` : ""}
        ${card.title ? `<h3>${esc(card.title)}</h3>` : ""}
        ${card.body ? `<p>${esc(card.body)}</p>` : ""}
        ${renderBullets(card.bullets)}
      </article>`;
  }

  function renderBlock(block) {
    if (!block) return `<div></div>`;
    if (block.kind === "image") {
      return `
        <div>
          <div class="image-frame ${block.cover ? "cover" : ""}">
            <img src="${esc(block.src)}" alt="${esc(block.alt || "Presentation visual")}">
          </div>
          ${block.caption ? `<div class="image-caption">${esc(block.caption)}</div>` : ""}
        </div>`;
    }
    if (block.kind === "quote") {
      return `<div class="quote">${block.html || esc(block.text || "")}</div>`;
    }
    if (block.kind === "html") {
      return `<div class="block-html">${block.html || ""}</div>`;
    }
    if (block.kind === "stack") {
      return `<div class="block-stack">${(block.blocks || []).map(renderBlock).join("")}</div>`;
    }
    const title = block.title ? `<h3>${esc(block.title)}</h3>` : "";
    const body = block.body ? `<p>${esc(block.body)}</p>` : "";
    return `
      <div class="block-list">
        <div class="panel ${accentClass(block.accent)}">
          ${title}${body}${renderBullets(block.bullets)}${renderChips(block.chips)}
        </div>
      </div>`;
  }

  function layoutTitle(slide) {
    return `
      <div class="cover-grid">
        <div class="cover-copy">
          ${slide.kicker ? `<div class="kicker">${esc(slide.kicker)}</div>` : ""}
          <h1>${renderTitle(slide.title, slide.highlight)}</h1>
          ${slide.subtitle ? `<div class="lead">${esc(slide.subtitle)}</div>` : ""}
          <div class="dotlist">
            ${(slide.bullets || []).map((item) => `
              <div class="dotitem">
                <span class="dot" style="background:${accentStyle(item.color)}"></span>
                <p>${item.html || esc(item.text || "")}</p>
              </div>`).join("")}
          </div>
        </div>
        ${slide.image ? `<div class="image-frame hero"><img src="${esc(slide.image)}" alt="${esc(slide.imageAlt || "Title slide visual")}"></div>` : ""}
      </div>
      ${slide.credits ? `<div class="cover-credits">${esc(slide.credits)}</div>` : ""}`;
  }

  function layoutImage(slide) {
    return `${renderHeading(slide)}
      <div class="single-image-wrap">
        <div class="image-frame ${slide.imageBackground === "light" ? "light" : ""}">
          <img src="${esc(slide.image)}" alt="${esc(slide.imageAlt || "Presentation visual")}">
        </div>
      </div>`;
  }

  function layoutCards(slide) {
    const cols = Math.min(5, Math.max(2, Number(slide.columns || slide.cards?.length || 3)));
    return `${renderHeading(slide)}
      <div class="grid cols-${cols}">
        ${(slide.cards || []).map((card, i) => renderCard(card, i, slide.numbered)).join("")}
      </div>`;
  }

  function layoutMetrics(slide) {
    const max = Math.max(1, ...(slide.bars || []).map((bar) => Number(bar.value || 0)));
    return `${renderHeading(slide)}
      <div class="metrics-grid">
        <div class="stat-stack">
          ${(slide.stats || []).map((stat) => `
            <div class="card stat-card ${accentClass(stat.accent)}">
              <div class="big-number">${esc(stat.value)}</div>
              <div class="label">${esc(stat.label)}</div>
            </div>`).join("")}
        </div>
        <div class="panel bar-panel">
          <h3>${esc(slide.barTitle || "Distribution")}</h3>
          ${(slide.bars || []).map((bar) => `
            <div class="bar-row">
              <span class="bar-label">${esc(bar.label)}</span>
              <b class="bar-value">${esc(bar.display ?? bar.value)}</b>
              <span class="bar-track"><i class="bar-fill" style="width:${Math.max(2, Number(bar.value || 0) / max * 100)}%;background:${accentStyle(bar.color)}"></i></span>
            </div>`).join("")}
        </div>
      </div>`;
  }

  function layoutSplit(slide) {
    const columns = esc(slide.columns || "1fr 1fr");
    return `${renderHeading(slide)}
      <div class="split-grid" style="grid-template-columns:${columns}">
        ${renderBlock(slide.left)}
        ${renderBlock(slide.right)}
      </div>`;
  }

  function layoutProcess(slide) {
    const steps = slide.steps || [];
    const columns = [];
    steps.forEach((_, i) => {
      columns.push("1fr");
      if (i < steps.length - 1) columns.push("32px");
    });
    const parts = [];
    steps.forEach((step, i) => {
      parts.push(`
        <div class="step">
          <h3>${esc(step.label || `Step ${i + 1}`)}</h3>
          ${step.code ? `<pre>${esc(step.code)}</pre>` : `<div class="step-text">${esc(step.text || "")}</div>`}
          ${step.note ? `<small>${esc(step.note)}</small>` : ""}
        </div>`);
      if (i < steps.length - 1) parts.push(`<b class="flow-arrow">&rarr;</b>`);
    });
    return `${renderHeading(slide)}
      <div class="process-flow" style="grid-template-columns:${columns.join(" ")}">${parts.join("")}</div>`;
  }

  function layoutLoop(slide) {
    const cycle = slide.cycle || ["Reason", "Act", "Observe"];
    return `${renderHeading(slide)}
      <div class="loop-grid">
        <div class="panel loop-card accent-cyan">
          <h2>${esc(slide.leftTitle || "Loop")}</h2>
          <div class="cycle">
            ${cycle.slice(0, 3).map((item) => `<div class="cycle-node">${esc(item)}</div>`).join("")}
            <span class="cycle-center">&#8635;</span>
          </div>
          ${slide.cycleNote ? `<p>${esc(slide.cycleNote)}</p>` : ""}
        </div>
        <div class="panel loop-card accent-purple">
          <h2>${esc(slide.rightTitle || "Decision stack")}</h2>
          <div class="stack-list">
            ${(slide.stack || []).map((item) => {
              const obj = typeof item === "string" ? { text: item } : item;
              return `<div class="stack-item ${obj.emphasis ? "emphasis" : ""}">${esc(obj.text)}</div>`;
            }).join("")}
          </div>
        </div>
      </div>`;
  }

  function layoutTimeline(slide) {
    const stages = slide.stages || [];
    return `${renderHeading(slide)}
      <div class="timeline" style="grid-template-columns:repeat(${Math.max(1, stages.length)}, minmax(0, 1fr))">
        ${stages.map((stage, i) => `
          <div class="timeline-node">
            <b class="timeline-number">${i + 1}</b>
            <h3>${esc(stage.title)}</h3>
            <h4>${esc(stage.subtitle || "")}</h4>
            ${renderBullets(stage.bullets)}
          </div>`).join("")}
      </div>
      ${(slide.deliverables || []).length ? `<div class="deliverables"><b>Deliverables</b>${slide.deliverables.map((d) => `<span>${esc(d)}</span>`).join("")}</div>` : ""}`;
  }

  function layoutClosing(slide) {
    return `${renderHeading(slide)}
      <div class="closing-grid">
        <div>
          <h2>${esc(slide.actionsTitle || "Immediate actions")}</h2>
          ${renderBullets(slide.actions)}
        </div>
        <div>
          <h2>${esc(slide.intakeTitle || "Brief intake")}</h2>
          ${renderBullets(slide.intake, true)}
        </div>
        <a class="closing-link" href="${esc(slide.link || "#")}" target="_blank" rel="noopener">
          <span class="link-label">${esc(slide.linkLabel || "Open link")}</span>
          <img src="${esc(slide.image)}" alt="${esc(slide.imageAlt || "Closing visual")}">
        </a>
      </div>`;
  }

  function layoutCustom(slide) {
    return `${renderHeading(slide)}<div class="custom-wrap">${slide.html || ""}</div>`;
  }

  const renderers = {
    title: layoutTitle,
    image: layoutImage,
    cards: layoutCards,
    metrics: layoutMetrics,
    split: layoutSplit,
    process: layoutProcess,
    loop: layoutLoop,
    timeline: layoutTimeline,
    closing: layoutClosing,
    custom: layoutCustom
  };

  function renderDeck() {
    const total = deckData.slides.length;
    deckEl.innerHTML = deckData.slides.map((slide, index) => {
      const layout = renderers[slide.layout] ? slide.layout : "custom";
      const classes = ["slide", `layout-${layout}`];
      if (layout === "title" && !slide.image) classes.push("no-image");
      const slideId = slide.id || `slide-${index + 1}`;
      return `<section class="${classes.join(" ")}" data-slide-index="${index}" data-slide-id="${esc(slideId)}" data-layout="${layout}">
        ${renderTopbar(slide, index, total)}
        ${renderers[layout](slide)}
        <div class="ppt-skill-credit">PPT-skill-credit: <a href="https://github.com/yyw-informatics/scientific-html-slides" target="_blank" rel="noopener noreferrer">github.com/yyw-informatics/scientific-html-slides</a></div>
      </section>`;
    }).join("");
    document.title = deckData.meta?.title || "Presentation";
  }

  renderDeck();

  function applyFontScale() {
    const factor = fontScaleFactors[visualStyle.fontScale] || 1;
    deckEl.dataset.fontScale = fontScaleFactors[visualStyle.fontScale] ? visualStyle.fontScale : "standard";
    if (factor === 1) return;
    const measurements = [...deckEl.querySelectorAll(".slide, .slide *")].map((element) => ({
      element,
      base: Number.parseFloat(getComputedStyle(element).fontSize)
    }));
    measurements.forEach(({ element, base }) => {
      if (Number.isFinite(base) && base > 0) {
        element.style.fontSize = `${Math.round(base * factor * 1000) / 1000}px`;
      }
    });
  }

  applyFontScale();

  const slides = [...document.querySelectorAll(".slide")];
  const total = slides.length;
  const notesPanel = document.getElementById("speaker-notes");
  const notesContent = document.getElementById("notes-content");
  const notesSlideId = document.getElementById("notes-slide-id");
  let current = 0;

  function fit() {
    const notesOpen = notesPanel && !document.body.classList.contains("notes-hidden");
    const availableWidth = Math.max(320, window.innerWidth - (notesOpen ? 380 : 0));
    const scale = Math.min(availableWidth / 1280, window.innerHeight / 720);
    deckEl.style.transform = `scale(${scale})`;
  }

  function noteSection(label, value) {
    const items = Array.isArray(value) ? value : (value ? [value] : []);
    if (!items.length) return "";
    return `<section class="note-section"><h3>${esc(label)}</h3>${renderBullets(items)}</section>`;
  }

  function updateSpeakerNotes() {
    if (!notesPanel || !notesContent || !notesSlideId) return;
    const slideId = slides[current]?.dataset.slideId || "";
    const note = speakerNotes[slideId] || {};
    notesSlideId.textContent = slideId;
    const duration = Number(note.durationSeconds);
    notesContent.innerHTML = `
      ${Number.isFinite(duration) && duration > 0 ? `<div class="note-duration">${Math.round(duration)} seconds</div>` : ""}
      ${noteSection("Talk track", note.talkTrack)}
      ${noteSection("Evidence", note.evidence)}
      ${noteSection("Caveats", note.caveats)}
      ${noteSection("Audience interaction", note.audienceInteraction)}
      ${noteSection("Sources", note.sources)}
      ${noteSection("From previous", note.transitionFromPrevious)}
      ${noteSection("To next", note.transitionToNext)}
      ${Object.keys(note).length ? "" : `<p class="notes-empty">No notes recorded for this slide.</p>`}`;
  }

  function toggleNotes(force) {
    if (!notesPanel) return;
    const hidden = typeof force === "boolean"
      ? !force
      : !document.body.classList.contains("notes-hidden");
    document.body.classList.toggle("notes-hidden", hidden);
    fit();
  }

  function updateUrl() {
    const hash = `#${current + 1}`;
    if (location.hash !== hash) history.replaceState(null, "", hash);
  }

  function show(index) {
    current = (index + total) % total;
    slides.forEach((slide, i) => slide.classList.toggle("active", i === current));
    countEl.textContent = `${current + 1} / ${total}`;
    updateUrl();
    updateSpeakerNotes();
    if (document.body.classList.contains("debug")) checkOverflow();
  }

  function requestedSlide() {
    const params = new URLSearchParams(location.search);
    const query = Number(params.get("slide"));
    if (Number.isFinite(query) && query >= 1 && query <= total) return query - 1;
    const hash = Number(location.hash.replace("#", ""));
    if (Number.isFinite(hash) && hash >= 1 && hash <= total) return hash - 1;
    return 0;
  }

  function checkOverflow() {
    slides.forEach((slide) => {
      slide.classList.remove("overflowing");
      slide.querySelectorAll(".debug-badge").forEach((badge) => badge.remove());
      const overflow = slide.scrollHeight > slide.clientHeight + 1 || slide.scrollWidth > slide.clientWidth + 1;
      if (overflow) {
        slide.classList.add("overflowing");
        const badge = document.createElement("div");
        badge.className = "debug-badge";
        badge.textContent = "OVERFLOW";
        slide.appendChild(badge);
        console.warn(`Slide ${Number(slide.dataset.slideIndex) + 1} overflows its 1280x720 canvas.`);
      }
    });
  }

  function toggleDebug(force) {
    const enabled = typeof force === "boolean" ? force : !document.body.classList.contains("debug");
    document.body.classList.toggle("debug", enabled);
    if (enabled) checkOverflow();
    else slides.forEach((slide) => slide.classList.remove("overflowing"));
  }

  window.addEventListener("resize", fit);
  window.addEventListener("hashchange", () => show(requestedSlide()));
  document.getElementById("prev").addEventListener("click", () => show(current - 1));
  document.getElementById("next").addEventListener("click", () => show(current + 1));
  document.addEventListener("keydown", (event) => {
    if (event.key === "ArrowRight" || event.key === " ") show(current + 1);
    if (event.key === "ArrowLeft") show(current - 1);
    if (event.key.toLowerCase() === "f") {
      if (!document.fullscreenElement) document.documentElement.requestFullscreen();
      else document.exitFullscreen();
    }
    if (event.key.toLowerCase() === "d") toggleDebug();
    if (event.key.toLowerCase() === "p") window.print();
    if (event.key.toLowerCase() === "n") toggleNotes();
  });

  document.fonts?.ready.then(() => {
    if (new URLSearchParams(location.search).get("notes") === "0") toggleNotes(false);
    fit();
    if (new URLSearchParams(location.search).get("debug") === "1") toggleDebug(true);
  });

  window.DECK_API = { show, fit, checkOverflow, toggleDebug, toggleNotes, total };
  fit();
  show(requestedSlide());
})();

const state = {
  manifest: null,
  searchIndex: null,
  searchPromise: null,
  currentPath: null,
  currentAnchor: null,
  flatDocs: [],
  searchResults: [],
  activeSearchIndex: -1,
  lastOpened: readLastOpened(),
};

const elements = {
  content: document.querySelector("#content"),
  sidebarNav: document.querySelector("#sidebar-nav"),
  sidebar: document.querySelector("#sidebar"),
  sidebarToggle: document.querySelector("#sidebar-toggle"),
  sidebarClose: document.querySelector("#sidebar-close"),
  sidebarScrim: document.querySelector("#sidebar-scrim"),
  tocNav: document.querySelector("#toc-nav"),
  tocPanel: document.querySelector("#toc-panel"),
  searchTrigger: document.querySelector("#search-trigger"),
  searchOverlay: document.querySelector("#search-overlay"),
  searchBackdrop: document.querySelector("#search-backdrop"),
  searchInput: document.querySelector("#search-input"),
  searchClose: document.querySelector("#search-close"),
  searchResults: document.querySelector("#search-results"),
  searchMeta: document.querySelector("#search-meta span:last-child"),
  themeToggle: document.querySelector("#theme-toggle"),
  revisionLabel: document.querySelector("#revision-label"),
  buildLabel: document.querySelector("#build-label"),
};

marked.setOptions({
  gfm: true,
  breaks: false,
  mangle: false,
});

document.addEventListener("DOMContentLoaded", start);
window.addEventListener("hashchange", route);
window.addEventListener("scroll", updateTocOnScroll, { passive: true });
window.addEventListener("resize", closeSidebarOnDesktop);
window.addEventListener("keydown", handleGlobalKeydown);

async function start() {
  setTheme(readTheme());
  bindShellEvents();
  refreshIcons();

  try {
    const response = await fetch("assets/manifest.json", { cache: "no-cache" });
    if (!response.ok) {
      throw new Error(`内容清单读取失败：HTTP ${response.status}`);
    }
    state.manifest = await response.json();
    state.flatDocs = flattenNavigation(state.manifest.nav).map((item) => item.path);
    elements.revisionLabel.textContent = `${state.manifest.stats.problems} 道题 · Java`;
    elements.buildLabel.textContent = `版本 ${state.manifest.revision} · 自动发布`;
    renderSidebar();
    route();
  } catch (error) {
    renderFatalError(error);
  }
}

function bindShellEvents() {
  elements.sidebarToggle.addEventListener("click", () => toggleSidebar(true));
  elements.sidebarClose.addEventListener("click", () => toggleSidebar(false));
  elements.sidebarScrim.addEventListener("click", () => toggleSidebar(false));
  elements.sidebarNav.addEventListener("click", handleSidebarClick);
  elements.searchTrigger.addEventListener("click", openSearch);
  elements.searchBackdrop.addEventListener("click", closeSearch);
  elements.searchClose.addEventListener("click", closeSearch);
  elements.searchInput.addEventListener("input", handleSearchInput);
  elements.themeToggle.addEventListener("click", toggleTheme);
  elements.content.addEventListener("click", handleContentClick);
}

function route() {
  const target = parseRoute();
  toggleSidebar(false);
  closeSearch();
  if (target.home) {
    renderHome();
    return;
  }
  loadDocument(target.path, target.anchor);
}

function parseRoute() {
  const raw = window.location.hash.replace(/^#\/?/, "");
  if (!raw) {
    return { home: true };
  }
  const [encodedPath, query = ""] = raw.split("?");
  if (!encodedPath.startsWith("doc/")) {
    return { home: true };
  }
  const path = encodedPath
    .slice(4)
    .split("/")
    .map((part) => decodeURIComponent(part))
    .join("/");
  const anchor = new URLSearchParams(query).get("id");
  return { home: false, path, anchor };
}

function docHref(path, anchor = "") {
  const encoded = path.split("/").map((part) => encodeURIComponent(part)).join("/");
  const suffix = anchor ? `?id=${encodeURIComponent(anchor)}` : "";
  return `#/doc/${encoded}${suffix}`;
}

function flattenNavigation(nav) {
  const items = [];
  for (const section of nav) {
    if (section.items) {
      items.push(...section.items);
    }
    if (section.topics) {
      for (const topic of section.topics) {
        items.push(...topic.items);
      }
    }
  }
  return items;
}

function renderSidebar() {
  const currentDoc = state.manifest.docs[state.currentPath];
  elements.sidebarNav.innerHTML = state.manifest.nav
    .map((section) => renderNavSection(section, currentDoc))
    .join("");
  refreshIcons();
  updateActiveNav();
}

function renderNavSection(section, currentDoc) {
  const isActiveSection = currentDoc?.category === section.id;
  const isProblemSection = section.id === "problems";
  const isOpen = isActiveSection || section.id === "start";
  const body = isProblemSection
    ? (section.topics || []).map((topic) => renderNavTopic(topic, currentDoc)).join("")
    : `<ul class="nav-list">${(section.items || []).map((item) => renderNavItem(item)).join("")}</ul>`;
  const sectionIcon = navSectionIcon(section.id);

  return `
    <section class="nav-section ${isOpen ? "is-open" : ""} ${isActiveSection ? "is-active" : ""}" data-section="${escapeAttribute(section.id)}">
      <button class="nav-section-toggle" type="button" aria-expanded="${String(isOpen)}">
        <i data-lucide="${sectionIcon}"></i>
        <span>${escapeHtml(section.label)}</span>
        <i class="chevron" data-lucide="chevron-right"></i>
      </button>
      <div class="nav-section-body">${body}</div>
    </section>
  `;
}

function renderNavTopic(topic, currentDoc) {
  const isOpen = currentDoc?.category === "problems" && currentDoc.topic === topic.label;
  return `
    <section class="nav-topic ${isOpen ? "is-open" : ""}" data-topic="${escapeAttribute(topic.label)}">
      <button class="nav-topic-toggle" type="button" aria-expanded="${String(isOpen)}">
        <i class="chevron" data-lucide="chevron-right"></i>
        <span>${escapeHtml(topic.label)}</span>
        <b class="nav-count">${topic.items.length}</b>
      </button>
      <div class="nav-topic-body">
        <ul class="nav-list">${topic.items.map((item) => renderNavItem(item)).join("")}</ul>
      </div>
    </section>
  `;
}

function renderNavItem(item) {
  const number = item.category === "problems"
    ? (item.path.match(/(\d+)/)?.[1] || "")
    : item.category.slice(0, 1).toUpperCase();
  const shortTitle = item.category === "problems" ? cleanProblemTitle(item.title) : item.title;
  return `
    <li>
      <a class="nav-link" href="${docHref(item.path)}" data-path="${escapeAttribute(item.path)}" title="${escapeAttribute(item.title)}">
        <span class="nav-number">${escapeHtml(number)}</span>
        <span class="nav-title">${escapeHtml(shortTitle)}</span>
      </a>
    </li>
  `;
}

function cleanProblemTitle(title) {
  return title
    .replace(/^\d+\.\s*/, "")
    .split("/")[0]
    .trim();
}

function navSectionIcon(id) {
  return {
    start: "play",
    problems: "list-checks",
    core: "boxes",
    models: "network",
    concepts: "git-branch",
    comparisons: "columns-3",
    java: "coffee",
    resources: "library",
  }[id] || "folder";
}

function handleSidebarClick(event) {
  const sectionToggle = event.target.closest(".nav-section-toggle");
  if (sectionToggle) {
    const section = sectionToggle.closest(".nav-section");
    section.classList.toggle("is-open");
    sectionToggle.setAttribute("aria-expanded", String(section.classList.contains("is-open")));
    return;
  }
  const topicToggle = event.target.closest(".nav-topic-toggle");
  if (topicToggle) {
    const topic = topicToggle.closest(".nav-topic");
    topic.classList.toggle("is-open");
    topicToggle.setAttribute("aria-expanded", String(topic.classList.contains("is-open")));
    return;
  }
  if (event.target.closest(".nav-link")) {
    toggleSidebar(false);
  }
}

function updateActiveNav(path = state.currentPath) {
  elements.sidebarNav.querySelectorAll(".nav-link.active").forEach((link) => link.classList.remove("active"));
  if (!path) {
    return;
  }
  const active = elements.sidebarNav.querySelector(`.nav-link[data-path="${cssEscape(path)}"]`);
  if (!active) {
    return;
  }
  active.classList.add("active");
  active.closest(".nav-section")?.classList.add("is-open");
  active.closest(".nav-topic")?.classList.add("is-open");
  requestAnimationFrame(() => active.scrollIntoView({ block: "nearest" }));
}

async function loadDocument(path, anchor = null) {
  const doc = state.manifest.docs[path];
  if (!doc) {
    renderNotFound(path);
    return;
  }
  state.currentPath = path;
  state.currentAnchor = anchor;
  updateActiveNav(path);
  rememberDocument(path);
  elements.tocNav.innerHTML = "";
  elements.content.innerHTML = loadingMarkup("正在打开文档...");

  try {
    const response = await fetch(`content/${encodePath(path)}`, { cache: "no-cache" });
    if (!response.ok) {
      throw new Error(`文档读取失败：HTTP ${response.status}`);
    }
    const markdown = stripFrontmatter(await response.text());
    const prepared = transformWikiLinks(markdown);
    const rendered = marked.parse(prepared);
    const safeHtml = DOMPurify.sanitize(rendered, {
      ADD_ATTR: ["data-doc", "target", "rel"],
    });
    elements.content.innerHTML = renderDocumentShell(doc, safeHtml);
    prepareArticle(path, doc);
    renderPager(path);
    document.title = `${doc.title} · ${state.manifest.title}`;
    refreshIcons();
    requestAnimationFrame(() => scrollToRequestedAnchor(anchor));
  } catch (error) {
    renderDocumentError(error, path);
  }
}

function renderDocumentShell(doc, safeHtml) {
  const meta = renderMeta(doc);
  const summary = doc.excerpt ? `<p class="page-summary">${escapeHtml(doc.excerpt)}</p>` : "";
  return `
    <header class="page-head">
      <nav class="breadcrumbs" aria-label="面包屑">
        <a href="#/">学习首页</a>
        <i data-lucide="chevron-right"></i>
        <a href="${docHref("README.md")}">总索引</a>
        <i data-lucide="chevron-right"></i>
        <span>${escapeHtml(doc.categoryLabel)}</span>
        ${doc.topic && doc.topic !== "总览" ? `<i data-lucide="chevron-right"></i><span>${escapeHtml(doc.topic)}</span>` : ""}
      </nav>
      <h1 class="page-title">${escapeHtml(doc.title)}</h1>
      ${summary}
      ${meta}
    </header>
    <div class="markdown-body">${safeHtml}</div>
  `;
}

function renderMeta(doc) {
  const chips = [];
  chips.push(`<span class="meta-chip"><i data-lucide="folder-tree"></i>${escapeHtml(doc.categoryLabel)}</span>`);
  if (doc.topic) {
    chips.push(`<span class="meta-chip"><i data-lucide="tag"></i>${escapeHtml(doc.topic)}</span>`);
  }
  if (doc.mastery) {
    chips.push(`<span class="meta-chip mastery-${escapeAttribute(doc.mastery)}"><i data-lucide="target"></i>${escapeHtml(doc.mastery)}</span>`);
  }
  if (doc.reviewStatus) {
    chips.push(`<span class="meta-chip review-${escapeAttribute(doc.reviewStatus)}"><i data-lucide="calendar-clock"></i>${escapeHtml(doc.reviewStatus)}</span>`);
  }
  return `<div class="meta-row">${chips.join("")}</div>`;
}

function prepareArticle(path, doc) {
  const markdownBody = elements.content.querySelector(".markdown-body");
  if (!markdownBody) {
    return;
  }

  const firstHeading = markdownBody.querySelector("h1");
  if (firstHeading && normalizeText(firstHeading.textContent) === normalizeText(doc.title)) {
    firstHeading.remove();
  }

  const usedIds = new Set();
  const headings = [];
  markdownBody.querySelectorAll("h1, h2, h3, h4").forEach((heading) => {
    const text = heading.textContent.trim();
    if (!text) {
      return;
    }
    let id = slugify(text) || "section";
    let suffix = 2;
    while (usedIds.has(id)) {
      id = `${slugify(text)}-${suffix}`;
      suffix += 1;
    }
    usedIds.add(id);
    heading.id = id;
    const anchorHref = docHref(path, id);
    heading.insertAdjacentHTML(
      "afterbegin",
      `<a class="heading-anchor" href="${escapeAttribute(anchorHref)}" aria-label="复制此章节链接">#</a>`
    );
    headings.push({
      level: Number(heading.tagName.slice(1)),
      text,
      id,
    });
  });

  postprocessLinks(markdownBody, path);
  addCopyButtons(markdownBody);
  markdownBody.querySelectorAll("pre code").forEach((block) => {
    if (window.hljs) {
      window.hljs.highlightElement(block);
    }
  });
  renderToc(headings);
}

function renderToc(headings) {
  const useful = headings.filter((heading) => heading.level <= 4).slice(0, 48);
  if (!useful.length) {
    elements.tocPanel.hidden = true;
    return;
  }
  elements.tocPanel.hidden = false;
  elements.tocNav.innerHTML = useful
    .map(
      (heading) => `
        <a class="toc-link depth-${heading.level}" href="${docHref(state.currentPath, heading.id)}" data-target="${escapeAttribute(heading.id)}">
          ${escapeHtml(heading.text)}
        </a>
      `
    )
    .join("");
}

function updateTocOnScroll() {
  if (!state.currentPath || elements.tocPanel.hidden) {
    return;
  }
  const headings = Array.from(elements.content.querySelectorAll(".markdown-body h2, .markdown-body h3, .markdown-body h4"));
  if (!headings.length) {
    return;
  }
  const threshold = document.querySelector(".topbar").getBoundingClientRect().height + 72;
  let active = headings[0];
  for (const heading of headings) {
    if (heading.getBoundingClientRect().top <= threshold) {
      active = heading;
    } else {
      break;
    }
  }
  elements.tocNav.querySelectorAll(".toc-link").forEach((link) => {
    link.classList.toggle("active", link.dataset.target === active.id);
  });
}

function renderPager(path) {
  const index = state.flatDocs.indexOf(path);
  const previous = index > 0 ? state.manifest.docs[state.flatDocs[index - 1]] : null;
  const next = index >= 0 && index < state.flatDocs.length - 1 ? state.manifest.docs[state.flatDocs[index + 1]] : null;
  if (!previous && !next) {
    return;
  }
  elements.content.insertAdjacentHTML(
    "beforeend",
    `
      <nav class="pager" aria-label="上一篇和下一篇">
        ${
          previous
            ? `<a class="pager-link previous" href="${docHref(previous.path)}"><small>上一篇</small><strong>${escapeHtml(previous.title)}</strong></a>`
            : "<span></span>"
        }
        ${
          next
            ? `<a class="pager-link next" href="${docHref(next.path)}"><small>下一篇</small><strong>${escapeHtml(next.title)}</strong></a>`
            : "<span></span>"
        }
      </nav>
    `
  );
}

function renderHome() {
  state.currentPath = null;
  state.currentAnchor = null;
  updateActiveNav(null);
  elements.tocPanel.hidden = true;
  const stats = state.manifest.stats;
  const problemsNav = state.manifest.nav.find((section) => section.id === "problems");
  const topics = problemsNav?.topics || [];
  const startItems = state.manifest.nav.find((section) => section.id === "start")?.items || [];
  const dueDocs = state.manifest.review.due.slice(0, 5).map((path) => state.manifest.docs[path]).filter(Boolean);
  const recentDocs = state.lastOpened
    .map((path) => state.manifest.docs[path])
    .filter((doc) => doc && doc.path !== "README.md")
    .slice(0, 5);

  const primaryTarget = dueDocs[0] || state.manifest.docs[state.manifest.homepage];
  elements.content.innerHTML = `
    <section class="home-intro">
      <p class="home-kicker">${escapeHtml(state.manifest.sourceLabel)}</p>
      <h1>把理解变成可回忆、可独立实现、可迁移的算法模型</h1>
      <p>
        当前收录 ${stats.problems} 道题、${stats.core} 张核心模型卡、${stats.models} 个完整建模专题与
        ${stats.java} 份 Java 速查。题目事实、权威代码、长推理和复习状态保持分层，不复制正文。
      </p>
      <div class="home-actions">
        <a class="primary-button" href="${docHref(primaryTarget.path)}">
          <i data-lucide="${dueDocs.length ? "calendar-check" : "book-open"}"></i>
          ${dueDocs.length ? `复习 ${cleanProblemTitle(primaryTarget.title)}` : "打开算法总索引"}
        </a>
        <a class="secondary-button" href="${docHref("学习看板/README.md")}">
          <i data-lucide="layout-dashboard"></i>
          学习看板
        </a>
        <a class="secondary-button" href="${docHref("03-资料/高效理解与回忆方法.md")}">
          <i data-lucide="brain"></i>
          高效回忆
        </a>
      </div>
    </section>

    <section class="home-band">
      <div class="band-head">
        <div>
          <h2>知识覆盖</h2>
          <p>数据在每次发布时从 Markdown 与属性区重新生成。</p>
        </div>
      </div>
      <div class="stats-grid">
        ${renderStat("标准题解", stats.problems, "题", "list-checks", "含官方事实与 Java 实现")}
        ${renderStat("核心模型", stats.core, "张", "boxes", "负责快速理解和复述")}
        ${renderStat("完整建模", stats.models, "篇", "network", "保留试错、证明与迁移")}
        ${renderStat("Java 速查", stats.java, "页", "coffee", "集合、队列、比较器与工具")}
      </div>
    </section>

    <section class="home-band home-columns">
      <div>
        <div class="band-head">
          <div>
            <h2>快速入口</h2>
            <p>按学习任务选择入口，而不是从目录里反复寻找。</p>
          </div>
        </div>
        <div class="link-list">
          ${startItems.map((item, index) => renderHomeLink(item, index)).join("")}
        </div>
      </div>
      <div>
        <div class="band-head">
          <div>
            <h2>${dueDocs.length ? "待复习" : "复习说明"}</h2>
            <p>${dueDocs.length ? "来自题解属性区的待复习状态。" : "状态由 Obsidian 属性区维护。"}</p>
          </div>
        </div>
        ${
          dueDocs.length
            ? `<div class="link-list">${dueDocs.map((item, index) => renderHomeLink(item, index)).join("")}</div>`
            : `
              <div class="home-note">
                <strong>当前没有到期题目</strong>
                在题目或核心卡的 frontmatter 中把 <code>reviewStatus</code> 设为“待复习”，下一次发布后会自动进入这里。
              </div>
            `
        }
        ${
          recentDocs.length
            ? `
              <div class="band-head" style="margin-top: 26px;">
                <div><h2>最近打开</h2><p>仅保存在当前浏览器。</p></div>
              </div>
              <div class="link-list">${recentDocs.map((item, index) => renderHomeLink(item, index)).join("")}</div>
            `
            : ""
        }
      </div>
    </section>

    <section class="home-band">
      <div class="band-head">
        <div>
          <h2>按主题浏览</h2>
          <p>物理目录代表主要模型，标签和状态仍保留在 Markdown 属性区。</p>
        </div>
        <a href="${docHref("README.md")}">查看完整题单</a>
      </div>
      <div class="topic-cloud">
        ${topics
          .map(
            (topic) => `
              <a class="topic-chip" href="${docHref(topic.items[0]?.path || "README.md")}">
                ${escapeHtml(topic.label)}
                <b>${topic.items.length}</b>
              </a>
            `
          )
          .join("")}
      </div>
    </section>
  `;
  document.title = `${state.manifest.title} · ${state.manifest.subtitle}`;
  window.scrollTo({ top: 0, behavior: "auto" });
  refreshIcons();
}

function renderStat(label, value, unit, icon, note) {
  return `
    <div class="stat">
      <span class="stat-label"><i data-lucide="${icon}"></i>${escapeHtml(label)}</span>
      <span class="stat-value">${value}<small> ${escapeHtml(unit)}</small></span>
      <span class="stat-note">${escapeHtml(note)}</span>
    </div>
  `;
}

function renderHomeLink(item, index) {
  return `
    <a class="link-row" href="${docHref(item.path)}">
      <span class="link-index">${String(index + 1).padStart(2, "0")}</span>
      <span class="link-copy">
        <strong>${escapeHtml(item.title)}</strong>
        <small>${escapeHtml(item.categoryLabel || item.topic || "")}</small>
      </span>
      <i data-lucide="arrow-right"></i>
    </a>
  `;
}

function handleContentClick(event) {
  const copyButton = event.target.closest(".copy-code");
  if (copyButton) {
    const code = copyButton.closest("pre")?.querySelector("code");
    if (code) {
      navigator.clipboard.writeText(code.textContent).then(() => {
        copyButton.innerHTML = `<i data-lucide="check"></i>已复制`;
        refreshIcons();
        window.setTimeout(() => {
          copyButton.innerHTML = `<i data-lucide="copy"></i>复制`;
          refreshIcons();
        }, 1400);
      });
    }
    return;
  }

  const anchor = event.target.closest('a[href^="#/doc/"]');
  if (anchor && anchor.dataset.doc) {
    const path = anchor.dataset.doc;
    if (!state.manifest.docs[path]) {
      event.preventDefault();
      anchor.classList.add("missing");
    }
  }
}

function addCopyButtons(container) {
  container.querySelectorAll("pre").forEach((pre) => {
    if (pre.querySelector(".copy-code")) {
      return;
    }
    const button = document.createElement("button");
    button.type = "button";
    button.className = "copy-code";
    button.innerHTML = `<i data-lucide="copy"></i>复制`;
    pre.append(button);
  });
}

function transformWikiLinks(markdown) {
  const lines = markdown.split("\n");
  const output = [];
  let fence = null;

  for (const line of lines) {
    const fenceMatch = line.match(/^\s*(```+|~~~+)/);
    if (fenceMatch) {
      const marker = fenceMatch[1][0];
      if (!fence) {
        fence = marker;
      } else if (marker === fence) {
        fence = null;
      }
      output.push(line);
      continue;
    }
    if (fence) {
      output.push(line);
      continue;
    }
    const segments = line.split(/(`+[^`]*`+)/g);
    output.push(
      segments
        .map((segment) => (segment.startsWith("`") ? segment : segment.replace(/\[\[([^\[\]]+)\]\]/g, wikiLinkReplacer)))
        .join("")
    );
  }
  return output.join("\n");
}

function wikiLinkReplacer(_match, raw) {
  const [rawTarget, rawLabel] = raw.split("|", 2);
  const [targetPart, anchor = ""] = rawTarget.split("#", 2);
  const target = normalizeDocTarget(targetPart);
  if (!isLikelyDocumentTarget(target)) {
    return _match;
  }
  const label = (rawLabel || rawTarget).trim();
  if (/\.(json|txt|csv|sh|py|ps1)$/i.test(target)) {
    return `<a class="wiki-link" href="content/${escapeAttribute(encodePath(target))}" data-doc="${escapeAttribute(target)}">${escapeHtml(label)}</a>`;
  }
  const href = docHref(target, anchor);
  return `<a class="wiki-link" href="${escapeAttribute(href)}" data-doc="${escapeAttribute(target)}">${escapeHtml(label)}</a>`;
}

function isLikelyDocumentTarget(target) {
  if (!target) {
    return false;
  }
  return (
    target.includes("/") ||
    /\.(md|json|txt|csv|sh|py|ps1)$/i.test(target) ||
    ["README", "AGENTS", "problems.json", "00-首页"].includes(target)
  );
}

function normalizeDocTarget(target) {
  let value = target.trim().replace(/^\.\//, "").replace(/^\/+/, "");
  if (!value || /\.[a-z0-9]+$/i.test(value)) {
    return value;
  }
  return `${value}.md`;
}

function postprocessLinks(container, currentPath) {
  container.querySelectorAll("a[href]").forEach((anchor) => {
    const original = anchor.getAttribute("href");
    if (!original || original.startsWith("#") || /^[a-z]+:/i.test(original)) {
      anchor.setAttribute("rel", "noreferrer");
      return;
    }
    const [pathPart, hashPart = ""] = original.split("#", 2);
    const resolved = resolveRelativePath(currentPath, decodeURI(pathPart));
    if (/\.md$/i.test(resolved)) {
      anchor.setAttribute("href", docHref(resolved, hashPart));
      anchor.dataset.doc = resolved;
      return;
    }
    if (resolved) {
      anchor.setAttribute("href", `content/${encodePath(resolved)}${hashPart ? `#${hashPart}` : ""}`);
    }
  });
}

function resolveRelativePath(currentPath, target) {
  if (!target) {
    return currentPath;
  }
  if (target.startsWith("/")) {
    return target.replace(/^\/+/, "");
  }
  const base = currentPath.split("/").slice(0, -1);
  const segments = target.split("/");
  for (const segment of segments) {
    if (!segment || segment === ".") {
      continue;
    }
    if (segment === "..") {
      base.pop();
    } else {
      base.push(segment);
    }
  }
  return base.join("/");
}

function scrollToRequestedAnchor(anchor) {
  window.scrollTo({ top: 0, behavior: "auto" });
  if (!anchor) {
    return;
  }
  const target = document.getElementById(anchor);
  if (target) {
    target.scrollIntoView({ block: "start" });
  }
}

function openSearch() {
  elements.searchOverlay.hidden = false;
  document.body.classList.add("search-open");
  elements.searchInput.value = "";
  state.searchResults = [];
  state.activeSearchIndex = -1;
  renderSearchResults();
  elements.searchInput.focus();
  loadSearchIndex();
}

function closeSearch() {
  elements.searchOverlay.hidden = true;
  document.body.classList.remove("search-open");
}

async function loadSearchIndex() {
  if (state.searchIndex) {
    return;
  }
  if (!state.searchPromise) {
    elements.searchMeta.textContent = "正在建立全文索引...";
    const revision = encodeURIComponent(state.manifest.revision || "local");
    state.searchPromise = fetch(`assets/search.json?v=${revision}`, { cache: "no-cache" })
      .then((response) => {
        if (!response.ok) {
          throw new Error(`搜索索引读取失败：HTTP ${response.status}`);
        }
        return response.json();
      })
      .then((index) => {
        state.searchIndex = index;
        elements.searchMeta.textContent = `已索引 ${index.length} 篇文档`;
        return index;
      })
      .catch((error) => {
        state.searchPromise = null;
        elements.searchMeta.textContent = error.message;
        throw error;
      });
  }
  await state.searchPromise;
}

async function handleSearchInput() {
  const query = elements.searchInput.value.trim();
  if (!query) {
    state.searchResults = [];
    state.activeSearchIndex = -1;
    renderSearchResults();
    return;
  }
  try {
    await loadSearchIndex();
    state.searchResults = searchDocuments(query).slice(0, 24);
    state.activeSearchIndex = state.searchResults.length ? 0 : -1;
    renderSearchResults(query);
  } catch {
    state.searchResults = [];
    renderSearchResults(query);
  }
}

function searchDocuments(query) {
  const terms = normalizeText(query).split(/\s+/).filter(Boolean);
  if (!terms.length || !state.searchIndex) {
    return [];
  }
  const results = [];
  for (const doc of state.searchIndex) {
    const title = normalizeText(doc.title);
    const topic = normalizeText(doc.topic);
    const category = normalizeText(doc.category);
    const headings = normalizeText((doc.headings || []).join(" "));
    const text = normalizeText(doc.text);
    let score = 0;
    let matched = true;
    for (const term of terms) {
      const inTitle = title.includes(term);
      const inTopic = topic.includes(term);
      const inCategory = category.includes(term);
      const inHeadings = headings.includes(term);
      const inText = text.includes(term);
      if (!inTitle && !inTopic && !inCategory && !inHeadings && !inText) {
        matched = false;
        break;
      }
      if (inTitle) score += 120;
      if (inTopic) score += 72;
      if (inCategory) score += 24;
      if (inHeadings) score += 32;
      if (inText) score += 10;
    }
    if (matched) {
      results.push({ ...doc, score });
    }
  }
  return results.sort((left, right) => right.score - left.score || left.title.localeCompare(right.title, "zh-CN"));
}

function renderSearchResults(query = "") {
  if (!state.searchResults.length) {
    elements.searchResults.innerHTML = `
      <div class="search-empty">
        <i data-lucide="${query ? "search-x" : "command"}"></i>
        <p>${query ? "没有找到匹配内容，尝试更短的题目名、模型名或 Java API。" : "可搜索题目名称、知识模型、Java API 和标题。"}</p>
      </div>
    `;
    refreshIcons();
    return;
  }

  elements.searchResults.innerHTML = state.searchResults
    .map((doc, index) => {
      const snippet = buildSnippet(doc, query);
      return `
        <a class="search-result ${index === state.activeSearchIndex ? "active" : ""}" href="${docHref(doc.path)}" data-result-index="${index}">
          <span class="search-result-main">
            <span class="search-result-title">${highlightText(doc.title, query)}</span>
            <span class="search-result-snippet">${snippet}</span>
            <span class="search-result-meta">
              <span>${escapeHtml(doc.category)}</span>
              ${doc.topic ? `<span>${escapeHtml(doc.topic)}</span>` : ""}
            </span>
          </span>
          <i data-lucide="corner-down-left"></i>
        </a>
      `;
    })
    .join("");
  refreshIcons();

  elements.searchResults.querySelectorAll(".search-result").forEach((result) => {
    result.addEventListener("mouseenter", () => {
      state.activeSearchIndex = Number(result.dataset.resultIndex);
      updateActiveSearchResult();
    });
    result.addEventListener("click", closeSearch);
  });
}

function buildSnippet(doc, query) {
  const text = doc.text || "";
  const normalized = normalizeText(text);
  const term = normalizeText(query).split(/\s+/).find(Boolean);
  let start = term ? normalized.indexOf(term) : -1;
  if (start < 0) {
    start = 0;
  }
  const from = Math.max(0, start - 70);
  const to = Math.min(text.length, start + 190);
  const prefix = from > 0 ? "..." : "";
  const suffix = to < text.length ? "..." : "";
  return `${prefix}${highlightText(text.slice(from, to), query)}${suffix}`;
}

function highlightText(text, query) {
  const escaped = escapeHtml(text);
  const terms = query
    .trim()
    .split(/\s+/)
    .filter(Boolean)
    .sort((left, right) => right.length - left.length);
  if (!terms.length) {
    return escaped;
  }
  const pattern = terms.map(escapeRegExp).join("|");
  return escaped.replace(new RegExp(`(${pattern})`, "gi"), "<mark>$1</mark>");
}

function updateActiveSearchResult() {
  elements.searchResults.querySelectorAll(".search-result").forEach((result) => {
    result.classList.toggle("active", Number(result.dataset.resultIndex) === state.activeSearchIndex);
  });
  const active = elements.searchResults.querySelector(".search-result.active");
  active?.scrollIntoView({ block: "nearest" });
}

function handleGlobalKeydown(event) {
  if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === "k") {
    event.preventDefault();
    openSearch();
    return;
  }
  if (event.key === "/" && !isTypingTarget(event.target)) {
    event.preventDefault();
    openSearch();
    return;
  }
  if (event.key === "Escape") {
    closeSearch();
    toggleSidebar(false);
    return;
  }
  if (elements.searchOverlay.hidden || !state.searchResults.length) {
    return;
  }
  if (event.key === "ArrowDown") {
    event.preventDefault();
    state.activeSearchIndex = Math.min(state.activeSearchIndex + 1, state.searchResults.length - 1);
    updateActiveSearchResult();
  } else if (event.key === "ArrowUp") {
    event.preventDefault();
    state.activeSearchIndex = Math.max(state.activeSearchIndex - 1, 0);
    updateActiveSearchResult();
  } else if (event.key === "Enter" && state.activeSearchIndex >= 0) {
    event.preventDefault();
    window.location.hash = docHref(state.searchResults[state.activeSearchIndex].path).slice(1);
    closeSearch();
  }
}

function isTypingTarget(target) {
  return target instanceof HTMLInputElement || target instanceof HTMLTextAreaElement || target?.isContentEditable;
}

function toggleSidebar(open) {
  document.body.classList.toggle("sidebar-open", open);
  elements.sidebarToggle.setAttribute("aria-expanded", String(open));
}

function closeSidebarOnDesktop() {
  if (window.innerWidth > 920) {
    toggleSidebar(false);
  }
}

function setTheme(theme) {
  document.documentElement.dataset.theme = theme;
  localStorage.setItem("algorithm-site-theme", theme);
  const isDark = theme === "dark";
  elements.themeToggle.innerHTML = `<i data-lucide="${isDark ? "sun" : "moon"}"></i>`;
  elements.themeToggle.setAttribute("aria-label", isDark ? "切换浅色模式" : "切换深色模式");
  document.querySelector('meta[name="theme-color"]')?.setAttribute("content", isDark ? "#11161a" : "#f4f6f8");
  refreshIcons();
}

function readTheme() {
  const stored = localStorage.getItem("algorithm-site-theme");
  if (stored === "light" || stored === "dark") {
    return stored;
  }
  return window.matchMedia?.("(prefers-color-scheme: dark)").matches ? "dark" : "light";
}

function toggleTheme() {
  setTheme(document.documentElement.dataset.theme === "dark" ? "light" : "dark");
}

function rememberDocument(path) {
  state.lastOpened = [path, ...state.lastOpened.filter((item) => item !== path)].slice(0, 8);
  localStorage.setItem("algorithm-site-recent", JSON.stringify(state.lastOpened));
}

function readLastOpened() {
  try {
    const value = JSON.parse(localStorage.getItem("algorithm-site-recent") || "[]");
    return Array.isArray(value) ? value : [];
  } catch {
    return [];
  }
}

function renderNotFound(path) {
  elements.content.innerHTML = `
    <div class="error-state">
      <i data-lucide="file-question"></i>
      <h1>没有找到这篇文档</h1>
      <p>${escapeHtml(path)} 不在当前导航清单中，可能已被合并、移动或改名。</p>
      <a class="primary-button" href="#/"><i data-lucide="house"></i>返回学习首页</a>
    </div>
  `;
  elements.tocPanel.hidden = true;
  document.title = `文档不存在 · ${state.manifest.title}`;
  refreshIcons();
}

function renderDocumentError(error, path) {
  elements.content.innerHTML = `
    <div class="error-state">
      <i data-lucide="circle-alert"></i>
      <h1>文档暂时无法打开</h1>
      <p>${escapeHtml(error.message)}</p>
      <p>${escapeHtml(path)}</p>
      <button class="secondary-button" type="button" onclick="window.location.reload()">
        <i data-lucide="refresh-cw"></i>重新加载
      </button>
    </div>
  `;
  elements.tocPanel.hidden = true;
  refreshIcons();
}

function renderFatalError(error) {
  elements.content.innerHTML = `
    <div class="error-state">
      <i data-lucide="circle-alert"></i>
      <h1>站点初始化失败</h1>
      <p>${escapeHtml(error.message)}</p>
      <p>请确认已运行 <code>python3 site/build.py</code> 并生成 <code>_site/assets/manifest.json</code>。</p>
    </div>
  `;
  elements.sidebarNav.innerHTML = "";
  refreshIcons();
}

function loadingMarkup(label) {
  return `<div class="page-loading"><span class="spinner"></span><p>${escapeHtml(label)}</p></div>`;
}

function stripFrontmatter(markdown) {
  if (!markdown.startsWith("---")) {
    return markdown;
  }
  const match = markdown.match(/^---\s*\n[\s\S]*?\n---\s*\n?/);
  return match ? markdown.slice(match[0].length) : markdown;
}

function slugify(text) {
  return text
    .trim()
    .toLowerCase()
    .replace(/[`*_~[\](){}<>#!?,.;:'"“”‘’、，。！？：；（）【】《》]/g, "")
    .replace(/\s+/g, "-")
    .replace(/-+/g, "-")
    .replace(/^-|-$/g, "");
}

function normalizeText(value) {
  return String(value || "").toLowerCase().replace(/\s+/g, " ").trim();
}

function encodePath(path) {
  return path.split("/").map((part) => encodeURIComponent(part)).join("/");
}

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function escapeAttribute(value) {
  return escapeHtml(value).replaceAll("`", "&#096;");
}

function escapeRegExp(value) {
  return value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

function cssEscape(value) {
  if (window.CSS?.escape) {
    return window.CSS.escape(value);
  }
  return String(value).replace(/["\\]/g, "\\$&");
}

function refreshIcons() {
  if (window.lucide) {
    window.lucide.createIcons({
      attrs: {
        "aria-hidden": "true",
      },
    });
  }
}

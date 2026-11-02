const state = {
  manifest: null,
  searchIndex: null,
  searchPromise: null,
  currentPath: null,
  currentAnchor: null,
  flatDocs: [],
  linkIndex: null,
  searchResults: [],
  activeSearchIndex: -1,
  lastOpened: readLastOpened(),
  reviewActive: false,
  reviewFilter: "due",
  reviewQuery: "",
  reviewPriority: "all",
  reviewDifficulty: "all",
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

const REVIEW_CHAIN_STEPS = [
  {
    index: "01",
    title: "对象与目标",
    question: "输入里到底有哪些对象、关系和作用范围？题目最后要求返回哪一个结果？",
    must: [
      "逐个指出数组、节点、区间、图或状态分别代表什么。",
      "说明哪些条件会限制后续动作，哪些只是输出格式。",
      "把最终返回值说成一个具体对象，而不是“求出答案”。",
    ],
    frame: "我处理的对象是……；这些对象之间的关系是……；题目最终要我返回……；因为题目规定……，所以后续不能……。",
    reject: "先说“双指针”“动态规划”或某个数据结构，却还说不清对象和目标。",
  },
  {
    index: "02",
    title: "最小人工过程",
    question: "不用算法术语，人在一个最小例子上会按什么时间顺序一步步做事？",
    must: [
      "写出初始例子、初始状态和第一次判断。",
      "每次只描述一个动作，并给出动作前后的具体值或对象。",
      "指出哪一个时刻产生答案，或哪一个条件令过程停止。",
    ],
    frame: "从初始状态……开始；我先做……，状态从……变成……；接着……；当……时，得到结果……。",
    reject: "直接从题目跳到结论，或用一个更大例子掩盖没有想清的第一步。",
  },
  {
    index: "03",
    title: "必须保存的信息",
    question: "哪项信息会继续影响未来判断？为什么丢掉它就无法完成下一步？",
    must: [
      "逐项说明需要保存的值、候选、区间、计数或关系。",
      "说明每项信息在未来的哪一个判断里被再次读取。",
      "说明它何时失效或可以被删除，不能只说“放进哈希表/栈”。",
    ],
    frame: "我必须保存……，因为后面要在……时读取它来判断……；当……发生后，它可以被……。",
    reject: "只报容器名，不说容器里保存的业务信息，也不说为什么需要它。",
  },
  {
    index: "04",
    title: "状态与更新",
    question: "哪个事件改变哪项信息？读取、写入、删除和覆盖的先后顺序是什么？",
    must: [
      "把每个事件拆成读取旧状态、计算、写入新状态和产生结果。",
      "在最小例子上逐轮列出关键变量，不只写“更新指针”。",
      "解释顺序颠倒后会出现哪一个错误结果。",
    ],
    frame: "第……轮先读取……；据此计算……；然后写入……；如果调换……和……，就会……。",
    reject: "无法预测下一轮状态，或只能通过运行代码来反推更新顺序。",
  },
  {
    index: "05",
    title: "不变量与安全性",
    question: "凭什么证明当前选择不会漏解、重复或破坏已经处理的结果？",
    must: [
      "写出每一步都成立的不变量，包括它覆盖了哪些对象。",
      "说明当前候选为什么能被安全保留、排除或结算。",
      "指出证明依赖的题目条件，并检查该条件在边界时仍成立。",
    ],
    frame: "循环每一轮开始时，我都能确认……；因此……不会漏掉；当……时，候选……可以安全排除，因为……。",
    reject: "用“这是标准做法”“贪心显然成立”或只复述复杂度来替代证明。",
  },
  {
    index: "06",
    title: "结构与代码映射",
    question: "需要哪些操作，为什么这个结构支持它们？每一段 Java 对应哪一个状态动作？",
    must: [
      "列出实际需要的查询、插入、删除、取极值或遍历操作。",
      "解释结构的选择理由和对应代价，不先写代码再猜理由。",
      "把初始化、循环、更新、终止和返回逐项映射回自然语言过程。",
    ],
    frame: "自然语言里的……动作对应代码中的……；这个标识符表示……；这一行必须放在这里，因为……。",
    reject: "函数能跑，但关键变量含义、更新位置或返回条件无法用自己的话解释。",
  },
  {
    index: "07",
    title: "反例与失效边界",
    question: "改动哪一个条件会让当前模型失效？最小反例最先在哪一步暴露问题？",
    must: [
      "主动构造一个能挑战不变量的最小输入，并完整演算。",
      "指出失效发生在读取、更新、排除候选还是结果产生的哪一步。",
      "区分题目边界和模型失效边界：空输入、单元素、重复值、负数等都要对应具体影响。",
    ],
    frame: "把条件……改成……后，模型会在第……步失效；最小反例是……；原因是原来的……不再成立。",
    reject: "只列一串边界名称，却说不清每个边界会改变哪项状态或哪条理由。",
  },
  {
    index: "08",
    title: "闭卷重建",
    question: "关闭全部参考后，能否重新生成过程、伪代码、Java 和自测，并解释每一处关键选择？",
    must: [
      "先口述完整链，再写伪代码，最后写可提交 Java。",
      "自己设计至少一个检查当前理解的输入并手算预期结果。",
      "完成后再对照资料，只记录第一处真实缺口，不把浏览当作验收。",
    ],
    frame: "我在不参考资料的情况下完成了……；我自己的检查输入是……；我第一处卡住的是……；下一次从这里继续……。",
    reject: "边看答案边抄写、运行通过但讲不出原因，或用“熟悉”“看懂了”代替独立证据。",
  },
];

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
    state.linkIndex = buildDocumentIndex(state.manifest.docs);
    state.flatDocs = flattenNavigation(state.manifest.nav).map((item) => item.path);
    elements.revisionLabel.textContent = `${state.manifest.stats.problems} 道题 · ${state.manifest.stats.reviews} 篇复习`;
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
  elements.content.addEventListener("input", handleReviewControls);
  elements.content.addEventListener("change", handleReviewControls);
}

function route() {
  const target = parseRoute();
  toggleSidebar(false);
  closeSearch();
  if (target.home) {
    renderHome();
    return;
  }
  if (target.review) {
    renderReviewCenter(target.query);
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
  if (encodedPath === "review") {
    return { review: true, query: new URLSearchParams(query) };
  }
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
  elements.sidebarNav.innerHTML = `
    <a class="review-nav-link ${state.reviewActive ? "active" : ""}" href="#/review">
      <span class="review-nav-icon"><i data-lucide="rotate-ccw"></i></span>
      <span>
        <strong>复习中心</strong>
        <small>完整推导链 · 8 个确认点</small>
      </span>
      <i data-lucide="arrow-up-right"></i>
    </a>
    ${state.manifest.nav
      .map((section) => renderNavSection(section, currentDoc))
      .join("")}
  `;
  refreshIcons();
  updateActiveNav();
}

function renderNavSection(section, currentDoc) {
  const isActiveSection = currentDoc?.category === section.id;
  const isOpen = isActiveSection || section.id === "start";
  const body = section.topics
    ? section.topics.map((topic) => renderNavTopic(topic, currentDoc, section.id)).join("")
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

function renderNavTopic(topic, currentDoc, sectionId) {
  const topicCategory = topic.category || sectionId;
  const isOpen = currentDoc?.category === topicCategory && currentDoc.topic === topic.label;
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
    : item.category === "review"
      ? (item.path.split("/").pop()?.match(/^(\d+)/)?.[1] || "·")
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
    review: "repeat-2",
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
  elements.sidebarNav
    .querySelectorAll(".nav-link.active, .review-nav-link.active")
    .forEach((link) => link.classList.remove("active"));
  if (state.reviewActive) {
    elements.sidebarNav.querySelector(".review-nav-link")?.classList.add("active");
    return;
  }
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
  state.reviewActive = false;
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
    const prepared = transformWikiLinks(markdown, path);
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
  const isReview = doc.category === "review";
  const indexTarget = isReview ? "LeetCode-系统复习/00-总入口.md" : "README.md";
  const indexLabel = isReview ? "复习总入口" : "总索引";
  const reviewStrip = doc.type === "problem" ? renderProblemReviewStrip(doc) : "";
  return `
    <header class="page-head">
      <nav class="breadcrumbs" aria-label="面包屑">
        <a href="#/">学习首页</a>
        <i data-lucide="chevron-right"></i>
        <a href="${docHref(indexTarget)}">${indexLabel}</a>
        <i data-lucide="chevron-right"></i>
        <span>${escapeHtml(doc.categoryLabel)}</span>
        ${doc.topic && doc.topic !== "总览" ? `<i data-lucide="chevron-right"></i><span>${escapeHtml(doc.topic)}</span>` : ""}
      </nav>
      <h1 class="page-title">${escapeHtml(doc.title)}</h1>
      ${summary}
      ${meta}
      ${reviewStrip}
    </header>
    <div class="markdown-body">${safeHtml}</div>
  `;
}

function renderProblemReviewStrip(doc) {
  const status = doc.reviewStatus || "未安排";
  const nextReview = doc.nextReview || "未排期";
  const attempts = Number.isInteger(doc.independentAttempts) ? doc.independentAttempts : 0;
  const errors = Array.isArray(doc.errorTags) ? doc.errorTags : [];
  const reviewHref = `#/review?query=${encodeURIComponent(cleanProblemTitle(doc.title))}`;
  return `
    <section class="problem-review-strip" aria-label="本题闭卷复习入口">
      <div class="problem-review-callout">
        <span><i data-lucide="git-branch"></i>完整链检查</span>
        <strong>先从代码解释倒推过程，再闭卷重建。</strong>
        <small>复习状态和日期只用于安排回访，不代表已经掌握。</small>
      </div>
      <div class="problem-review-actions">
        <a class="primary-button compact" href="${reviewHref}">
          <i data-lucide="book-open-check"></i>闭卷重建本题
        </a>
        <a class="secondary-button compact" href="${docHref("学习看板/单题复习工作台.md")}">
          <i data-lucide="list-checks"></i>记录断点
        </a>
      </div>
      <div class="problem-review-facts" aria-label="本题复习属性">
        <span><i class="review-status-dot review-status-${reviewStatusClass(status)}"></i>${escapeHtml(status)}</span>
        <span>${escapeHtml(doc.mastery || "未学")}</span>
        <span>${nextReview === "未排期" ? "未排期" : `下次 ${escapeHtml(nextReview)}`}</span>
        <span>独立 ${attempts} 次</span>
        <span class="problem-review-errors">${errors.length ? errors.map((tag) => escapeHtml(tag)).join("、") : "暂无错因"}</span>
      </div>
    </section>
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
  state.reviewActive = false;
  state.currentPath = null;
  state.currentAnchor = null;
  updateActiveNav(null);
  elements.tocPanel.hidden = true;
  const stats = state.manifest.stats;
  const problemsNav = state.manifest.nav.find((section) => section.id === "problems");
  const topics = problemsNav?.topics || [];
  const startItems = state.manifest.nav.find((section) => section.id === "start")?.items || [];
  const reviewItems = [
    "学习看板/单题复习工作台.md",
    "LeetCode-系统复习/00-总入口.md",
    "LeetCode-系统复习/01-复习计划/16周弹性计划.md",
    "LeetCode-系统复习/05-单题流程/单题时间切片.md",
    "LeetCode-系统复习/06-学习记录/单题复习记录模板.md",
  ]
    .map((path) => state.manifest.docs[path])
    .filter(Boolean);
  const dueDocs = state.manifest.review.due.slice(0, 5).map((path) => state.manifest.docs[path]).filter(Boolean);
  const scheduledDocs = state.manifest.review.scheduled
    .slice(0, 5)
    .map((path) => state.manifest.docs[path])
    .filter(Boolean);
  const unarrangedDocs = state.manifest.review.unarranged
    .slice(0, 5)
    .map((path) => state.manifest.docs[path])
    .filter(Boolean);
  const recentDocs = state.lastOpened
    .map((path) => state.manifest.docs[path])
    .filter((doc) => doc && doc.path !== "README.md")
    .slice(0, 5);

  const nextReviewDoc = dueDocs[0] || scheduledDocs[0] || unarrangedDocs[0];
  elements.content.innerHTML = `
    <section class="home-intro">
      <p class="home-kicker">${escapeHtml(state.manifest.sourceLabel)}</p>
      <h1>把理解变成可回忆、可独立实现、可迁移的算法模型</h1>
      <p>
        从题目对象和最小人工过程开始，一直走到状态更新、不变量、代码映射和反例。
        站点只负责保存事实、推导和记录；不能用一个方法名、一段代码或完成数量替代这条链。
      </p>
      <div class="home-actions">
        <a class="primary-button" href="#/review">
          <i data-lucide="git-branch"></i>
          开始完整推导链
        </a>
        <a class="secondary-button" href="${docHref("学习看板/单题复习工作台.md")}">
          <i data-lucide="clipboard-check"></i>
          单题工作台
        </a>
        <a class="secondary-button" href="${docHref("03-资料/高效理解与回忆方法.md")}">
          <i data-lucide="brain"></i>
          高效回忆
        </a>
        <a class="secondary-button" href="${docHref("LeetCode-系统复习/00-总入口.md")}">
          <i data-lucide="repeat-2"></i>
          系统复习
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
        ${renderStat("复习资料", stats.reviews, "篇", "repeat-2", "完整链、长时段、计划与记录")}
      </div>
    </section>

    <section class="home-band home-columns">
      <div>
        <div class="band-head">
          <div>
            <h2>单题复习</h2>
            <p>先重建完整因果链，再看代码和状态记录。</p>
          </div>
          <a href="#/review">打开推导链复习</a>
        </div>
        <div class="link-list">
          ${reviewItems.map((item, index) => renderHomeLink(item, index)).join("")}
        </div>
      </div>
      <div>
        <div class="band-head">
          <div>
            <h2>怎样确认一段真的通过</h2>
            <p>“熟悉”和“看懂了”都不是证据。</p>
          </div>
        </div>
        <div class="review-evidence-list">
          <div><span>复述</span><p>不看资料说出对象、状态、事件和结果，不夹带方法名。</p></div>
          <div><span>演算</span><p>在最小例子上逐轮写出关键信息，预测下一轮变化。</p></div>
          <div><span>反证</span><p>说明不变量为什么成立，并指出改动哪个条件会让它失效。</p></div>
          <div><span>重建</span><p>关闭参考后独立写伪代码、Java 和自己设计的检查输入。</p></div>
        </div>
        <div class="home-note compact">
          <strong>排期只是回访提醒</strong>
          ${
            nextReviewDoc
              ? `当前可优先回看「${escapeHtml(cleanProblemTitle(nextReviewDoc.title))}」，也可以从任意一道题开始完整链。`
              : "从题库任选一道题，先判断这条链是否真的能被重新生成。"
          }
        </div>
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
            <h2>最近打开</h2>
            <p>仅保存在当前浏览器，用于接续上一次工作。</p>
          </div>
        </div>
        ${
          recentDocs.length
            ? `<div class="link-list">${recentDocs.map((item, index) => renderHomeLink(item, index)).join("")}</div>`
            : `
              <div class="home-note">
                <strong>还没有最近记录</strong>
                打开一道标准题解或核心模型后，这里会显示当前浏览器里的访问顺序。
              </div>
            `
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

function renderReviewCenter(query = null) {
  state.reviewActive = true;
  state.currentPath = null;
  state.currentAnchor = null;
  elements.tocPanel.hidden = true;
  if (query?.get("status")) {
    state.reviewFilter = normalizeReviewFilter(query.get("status"));
  } else if (query?.get("query")) {
    state.reviewFilter = "all";
  } else if (query?.get("pick") === "1") {
    state.reviewFilter = "all";
  }
  if (query?.get("query")) {
    state.reviewQuery = query.get("query");
  }
  updateActiveNav(null);

  const review = state.manifest.review;
  const pickerOpen = query?.get("pick") === "1";
  const suggestedPath =
    review.due[0] ||
    review.upcoming[0] ||
    review.unarranged[0] ||
    review.reviewed[0];
  const suggested = suggestedPath ? state.manifest.docs[suggestedPath] : null;

  elements.content.innerHTML = `
    <section class="review-center">
      <header class="review-hero">
        <p class="review-eyebrow"><i data-lucide="git-branch"></i>推导链复习</p>
        <h1>把一条因果链重新生成，才算这一轮复习</h1>
        <p>
          不是先看“今天几道题”，也不是用完成数确认自己学会了。每次只选一道题，从对象和目标开始，
          把最小例子、状态更新、不变量、代码映射和失效边界逐段说清。只要一段依赖“显然”
          “标准做法”或“直接套模板”，这一轮就停在那个最早缺口。
        </p>
        <div class="review-hero-actions">
          ${
            suggested
              ? `<a class="primary-button" href="${docHref(suggested.path)}">
                  <i data-lucide="book-open-check"></i>
                  从「${escapeHtml(cleanProblemTitle(suggested.title))}」重建
                </a>`
              : ""
          }
          <a class="secondary-button" href="#/review?pick=1">
            <i data-lucide="list-filter"></i>自己选择题目
          </a>
          <a class="secondary-button" href="${docHref("学习看板/单题复习工作台.md")}">
            <i data-lucide="list-checks"></i>记录本轮断点
          </a>
          <a class="secondary-button" href="${docHref("03-资料/高效理解与回忆方法.md")}">
            <i data-lucide="brain"></i>理解与回忆方法
          </a>
        </div>
      </header>

      <section class="review-chain-section">
        <div class="review-section-head">
          <div>
            <h2>本次唯一主链：逐段生成，不逐段打勾</h2>
            <p>
              下面不是待办清单。每一段只有一个作用：要求你产出下一段所依赖的关系、数据和理由。
              链条没有闭合时，可以继续推导；只有同一处反复没有新证据时才保存断点。
            </p>
          </div>
          <span class="review-chain-count">8 个确认点</span>
        </div>
        <ol class="review-chain">
          ${REVIEW_CHAIN_STEPS.map(renderReviewChainStep).join("")}
        </ol>
      </section>

      <section class="review-evidence" aria-label="怎样确认这一段真的通过">
        <div class="review-section-head">
          <div>
            <h2>一段“通过”需要四种证据</h2>
            <p>能看懂参考答案，只能说明你能沿着别人的路径前进，不能证明你能自己生成这条路径。</p>
          </div>
        </div>
        <div class="review-evidence-grid">
          <div><span>01</span><strong>能复述</strong><p>不用方法名，按对象、事件和结果说清前后关系。</p></div>
          <div><span>02</span><strong>能演算</strong><p>在最小例子上预测下一轮状态，实际演算与预测一致。</p></div>
          <div><span>03</span><strong>能反证</strong><p>知道不变量依赖什么条件，改动它后能指出第一个失效点。</p></div>
          <div><span>04</span><strong>能重建</strong><p>不看答案重写伪代码、Java 和你自己的检查输入。</p></div>
        </div>
      </section>

      <section class="review-rules" aria-label="复习停止与推进规则">
        <div>
          <span><i data-lucide="unlink"></i>断点优先</span>
          <h3>卡住时只补最早断点</h3>
          <p>如果第 4 步说不清，不要跳到代码抄一遍。记录“哪一项状态在哪个事件后出错”，下一段从这里继续。</p>
        </div>
        <div>
          <span><i data-lucide="hourglass"></i>长时段允许</span>
          <h3>不把 20 分钟当成学习目标</h3>
          <p>状态允许且链条仍在产生新证据时，可以连续推进整条链。保存点只防止中断后丢失上下文，不是新的打卡指标。</p>
        </div>
        <div>
          <span><i data-lucide="badge-check"></i>证据验收</span>
          <h3>“看懂了”不是通过条件</h3>
          <p>通过条件只有：关系能复述、例子能演算、理由能反证、代码能独立重建。做不到时保留断点，不伪造完成。</p>
        </div>
      </section>

      <details class="review-picker" ${pickerOpen ? "open" : ""}>
        <summary>
          <span>
            <strong>选题辅助</strong>
            <small>日期、阶段和次数只帮助决定从哪里开始，不评价这一轮学得怎样。</small>
          </span>
          <i data-lucide="chevron-down"></i>
        </summary>
        <section class="review-picker-body">
          <div class="review-controls">
            <label class="review-search-control">
              <i data-lucide="search"></i>
              <input id="review-query" type="search" value="${escapeAttribute(state.reviewQuery)}" placeholder="题名、主题或错因">
            </label>
            <label>
              <span>回访范围</span>
              <select id="review-status-filter">
                ${renderReviewOption("all", "全部题目", state.reviewFilter)}
                ${renderReviewOption("due", "今日提醒", state.reviewFilter)}
                ${renderReviewOption("scheduled", "全部已排期", state.reviewFilter)}
                ${renderReviewOption("upcoming", "未来排期", state.reviewFilter)}
                ${renderReviewOption("unarranged", "尚未排期", state.reviewFilter)}
                ${renderReviewOption("reviewed", "已复习", state.reviewFilter)}
              </select>
            </label>
            <label>
              <span>优先级</span>
              <select id="review-priority-filter">
                ${renderReviewOption("all", "全部", state.reviewPriority)}
                ${renderReviewOption("P0", "P0", state.reviewPriority)}
                ${renderReviewOption("P1", "P1", state.reviewPriority)}
                ${renderReviewOption("P2", "P2", state.reviewPriority)}
              </select>
            </label>
            <label>
              <span>难度</span>
              <select id="review-difficulty-filter">
                ${renderReviewOption("all", "全部", state.reviewDifficulty)}
                ${renderReviewOption("Easy", "简单", state.reviewDifficulty)}
                ${renderReviewOption("Medium", "中等", state.reviewDifficulty)}
                ${renderReviewOption("Hard", "困难", state.reviewDifficulty)}
              </select>
            </label>
          </div>
          <div id="review-queue" class="review-queue" aria-live="polite">
            ${renderReviewQueue()}
          </div>
        </section>
      </details>
    </section>
  `;

  document.title = `推导链复习 · ${state.manifest.title}`;
  window.scrollTo({ top: 0, behavior: "auto" });
  refreshIcons();
}

function renderReviewChainStep(step) {
  return `
    <li>
      <span class="review-chain-index">${escapeHtml(step.index)}</span>
      <div class="review-chain-body">
        <h3>${escapeHtml(step.title)}</h3>
        <p>${escapeHtml(step.question)}</p>
        <ul class="review-chain-must">
          ${step.must.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}
        </ul>
        <div class="review-chain-frame">
          <span>这一段至少能完整说出</span>
          <p>${escapeHtml(step.frame)}</p>
        </div>
        <div class="review-chain-reject">
          <strong><i data-lucide="circle-x"></i>没有通过</strong>
          <span>${escapeHtml(step.reject)}</span>
        </div>
      </div>
    </li>
  `;
}

function renderReviewOption(value, label, selected) {
  return `<option value="${escapeAttribute(value)}" ${value === selected ? "selected" : ""}>${escapeHtml(label)}</option>`;
}

function normalizeReviewFilter(value) {
  return ["all", "due", "scheduled", "upcoming", "unarranged", "reviewed"].includes(value) ? value : "due";
}

function reviewStatusClass(status) {
  return {
    未安排: "unarranged",
    待复习: "scheduled",
    已复习: "reviewed",
  }[status] || "unarranged";
}

function renderReviewQueue() {
  const docs = filteredReviewDocs();
  if (!docs.length) {
    return `
      <div class="review-empty">
        <i data-lucide="list-filter"></i>
        <strong>当前筛选下没有题目</strong>
        <p>这不是前面的进度欠账。换一个队列，或直接打开单题复习工作台开始。</p>
      </div>
    `;
  }
  return docs
    .map((doc) => {
      const status = doc.reviewStatus || "未安排";
      const attempts = Number.isInteger(doc.independentAttempts) ? doc.independentAttempts : 0;
      const errors = Array.isArray(doc.errorTags) && doc.errorTags.length ? doc.errorTags.join("、") : "暂无错因";
      return `
        <a class="review-queue-row" href="${docHref(doc.path)}">
          <span class="review-priority review-priority-${escapeAttribute(doc.priority || "P2")}">${escapeHtml(doc.priority || "P?")}</span>
          <span class="review-queue-main">
            <strong>${escapeHtml(cleanProblemTitle(doc.title))}</strong>
            <small>${escapeHtml(doc.topic || "未分类")} · ${escapeHtml(difficultyLabel(doc.difficulty))} · ${escapeHtml(doc.mastery || "未学")}</small>
          </span>
          <span class="review-queue-status">
            <span><i class="review-status-dot review-status-${reviewStatusClass(status)}"></i>${escapeHtml(status)}</span>
            <small>${escapeHtml(doc.nextReview || "未排期")}</small>
          </span>
          <span class="review-queue-evidence">
            <span>独立 ${attempts} 次</span>
            <small>${escapeHtml(errors)}</small>
          </span>
          <i data-lucide="arrow-up-right"></i>
        </a>
      `;
    })
    .join("");
}

function filteredReviewDocs() {
  const review = state.manifest.review;
  const paths = review[state.reviewFilter] || [];
  const query = normalizeText(state.reviewQuery);
  return paths
    .map((path) => state.manifest.docs[path])
    .filter(Boolean)
    .filter((doc) => state.reviewPriority === "all" || doc.priority === state.reviewPriority)
    .filter((doc) => state.reviewDifficulty === "all" || doc.difficulty === state.reviewDifficulty)
    .filter((doc) => {
      if (!query) {
        return true;
      }
      return normalizeText(
        [
          doc.title,
          doc.topic,
          doc.primaryPattern,
          doc.mastery,
          ...(doc.errorTags || []),
        ].join(" ")
      ).includes(query);
    });
}

function difficultyLabel(value) {
  return {
    Easy: "简单",
    Medium: "中等",
    Hard: "困难",
  }[value] || value || "难度未知";
}

function handleReviewControls(event) {
  const target = event.target;
  if (!(target instanceof HTMLInputElement || target instanceof HTMLSelectElement)) {
    return;
  }
  if (target.id === "review-query") {
    state.reviewQuery = target.value;
  } else if (target.id === "review-status-filter") {
    state.reviewFilter = normalizeReviewFilter(target.value);
  } else if (target.id === "review-priority-filter") {
    state.reviewPriority = target.value;
  } else if (target.id === "review-difficulty-filter") {
    state.reviewDifficulty = target.value;
  } else {
    return;
  }
  const queue = document.querySelector("#review-queue");
  if (queue) {
    queue.innerHTML = renderReviewQueue();
    refreshIcons();
  }
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

function buildDocumentIndex(docs) {
  const paths = new Set(Object.keys(docs));
  const byBasename = new Map();
  for (const path of paths) {
    const filename = path.split("/").pop();
    const stem = filename.replace(/\.md$/i, "");
    for (const key of new Set([filename, stem])) {
      const matches = byBasename.get(key) || [];
      matches.push(path);
      byBasename.set(key, matches);
    }
  }
  return { paths, byBasename };
}

function transformWikiLinks(markdown, currentPath) {
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
        .map((segment) =>
          segment.startsWith("`")
            ? segment
            : segment.replace(/\[\[([^\[\]]+)\]\]/g, (match, raw) => wikiLinkReplacer(match, raw, currentPath))
        )
        .join("")
    );
  }
  return output.join("\n");
}

function wikiLinkReplacer(_match, raw, currentPath) {
  const [rawTarget, rawLabel] = raw.split("|", 2);
  const [targetPart, anchor = ""] = rawTarget.split("#", 2);
  const label = (rawLabel || rawTarget).trim();
  if (/^[a-z]+:/i.test(targetPart)) {
    return `<a href="${escapeAttribute(targetPart)}" rel="noreferrer" target="_blank">${escapeHtml(label)}</a>`;
  }
  const target = resolveDocumentPath(targetPart, currentPath);
  if (target) {
    const href = docHref(target, anchor);
    return `<a class="wiki-link" href="${escapeAttribute(href)}" data-doc="${escapeAttribute(target)}">${escapeHtml(label)}</a>`;
  }
  const attachment = resolveRelativePath(currentPath, targetPart.trim().replaceAll("\\", "/"));
  if (/\.(json|txt|csv|sh|py|ps1|base)$/i.test(attachment)) {
    return `<a class="wiki-link" href="content/${escapeAttribute(encodePath(attachment))}">${escapeHtml(label)}</a>`;
  }
  return `<span class="wiki-link missing" title="未找到 ${escapeAttribute(targetPart)}">${escapeHtml(label)}</span>`;
}

function resolveDocumentPath(target, currentPath) {
  const index = state.linkIndex;
  if (!target) {
    return currentPath;
  }
  if (!index) {
    return null;
  }

  const cleaned = target.trim().replaceAll("\\", "/");
  const candidates = [
    resolveRelativePath(currentPath, cleaned),
    cleaned.replace(/^\/+/, ""),
  ];
  for (const candidate of candidates) {
    for (const variant of documentPathVariants(normalizeSourcePath(candidate))) {
      if (index.paths.has(variant)) {
        return variant;
      }
    }
  }

  const rootTarget = cleaned.replace(/^\.?\//, "");
  const suffixKeys = documentPathVariants(rootTarget);
  for (const suffix of suffixKeys) {
    const matches = [...index.paths].filter((path) => path.endsWith(`/${suffix}`));
    if (matches.length === 1) {
      return matches[0];
    }
  }

  const basename = rootTarget.split("/").pop();
  const matches = index.byBasename.get(basename) || index.byBasename.get(basename.replace(/\.md$/i, "")) || [];
  return matches.length === 1 ? matches[0] : null;
}

function normalizeSourcePath(value) {
  return value.replace(/^学习文库\/算法学习\//, "");
}

function documentPathVariants(value) {
  const normalized = value.replace(/^\.\//, "");
  if (!normalized) {
    return [];
  }
  return /\.[a-z0-9]+$/i.test(normalized) ? [normalized] : [normalized, `${normalized}.md`];
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

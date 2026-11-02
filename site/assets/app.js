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

const HUMAN_READING_STEPS = [
  {
    index: "01",
    title: "只读原题事实",
    question: "在还不知道用什么算法时，题目原句到底给了什么、要求什么、明确禁止什么？",
    must: [
      "先分开抄下输入、输出、示例、约束和特殊保证，不把脑中的解释混进原题。",
      "区分“题目事实”“由事实推出的结论”和“我还不知道的部分”。",
      "此时不写方法名，也不根据题目标题或标签猜答案。",
    ],
    frame: "题目已经明确给出……；题目要求返回……；题目明确保证……；题目禁止……；我暂时还不知道……。",
    reject: "把“应该用哈希表”或“这是滑动窗口”写在读题笔记里，却还不能复述原题条件。",
  },
  {
    index: "02",
    title: "把题干扩写成完整生活过程",
    question: "把压缩的题面展开成“谁拿着什么，从哪里开始，重复做什么，何时停止，最后交出什么”。",
    must: [
      "补全题面中省略的主语、动作对象、动作顺序和结果产生时刻。",
      "每一条扩写都能指回原句；属于自己推测的内容必须标明“推测”。",
      "解释一个条件实际阻止了什么错误做法，而不是只把它抄一遍。",
    ],
    frame: "我手里有……；我从……开始；我反复做……；当……时停止；题目要交出的不是……，而是……；条件“……”意味着我不能……。",
    reject: "把题面换成几个抽象名词，却没有补出动作顺序、停止条件或条件的实际作用。",
  },
  {
    index: "03",
    title: "清点题目里的对象",
    question: "人话过程里反复出现的元素、位置、区间、节点、目标和结果，分别是什么？",
    must: [
      "先列业务对象，例如数字、位置、区间、节点、路径和答案。",
      "说明对象之间是先后、相邻、包含、依赖还是可达关系。",
      "区分题目对象和以后可能使用的代码对象，不把 Map、Queue 提前混进来。",
    ],
    frame: "题目中的主要对象是……；其中……表示……；它们之间具有……关系；最终答案描述的是……。",
    reject: "只报数组、哈希表和指针等实现名词，却说不清它们在题目世界里代表什么。",
  },
  {
    index: "04",
    title: "让一个人手工做最小例子",
    question: "不用任何算法技巧，一个普通人拿到最小但完整的例子，会按什么时间顺序动手？",
    must: [
      "先写最直接、可能很慢的做法，不急着优化。",
      "每一步只包含一个可观察动作，并写出动作前后的具体内容。",
      "至少有一个例子能从初始状态走到答案，不能只描述抽象流程。",
    ],
    frame: "以……为例，我先……；看到……以后，我接着……；这一轮得到……；最后在……时得到答案。",
    reject: "例子只写输入输出，中间过程由答案一句带过；或一开始就用未经验证的高级方法。",
  },
  {
    index: "05",
    title: "第一次捕捉变化",
    question: "手工过程中，哪一个信息在每一步发生变化？变化由什么事件触发，结果在哪一刻产生？",
    must: [
      "为关键对象写清“变化前 -> 触发事件 -> 变化后”。",
      "区分当前检查位置、历史信息、候选范围、累计结果和最终答案。",
      "指出哪些变化只是例子细节，哪些变化会决定下一步。",
    ],
    frame: "一开始……是……；当……发生时，……从……变成……；答案不是在开头出现，而是在……时产生。",
    reject: "只说“遍历数组、更新答案”，却说不清究竟哪个值在何时改变。",
  },
  {
    index: "06",
    title: "读范围，生成候选算法池",
    question: "官方约束允许多少操作？慢过程需要的操作，又能引出哪些仍待验证的方向？",
    must: [
      "把官方约束、自己推导的操作预算和候选方向分开写，不把学习推导冒充成官方推荐复杂度。",
      "用慢过程的大致运算量判断哪些复杂度家族首先不够，再根据查询历史、等待结算、区间维护、候选淘汰或子问题复用扩充候选。",
      "候选池只保留待验证方向；不把“看到 10^5 就用双指针”或标签匹配当成结论。",
    ],
    frame: "官方约束是……；如果每一步都重新检查全部对象，我推导大约会做……次操作；因此不能依赖……；由过程的……操作，候选池里有……；此刻仍不能决定……。",
    reject: "完全不看约束；只看 n 的大小；或范围分析结束后只会说“用 O(n)”，却没有产生可比较的候选。",
  },
  {
    index: "07",
    title: "第二次捕捉变化，寻找重复劳动",
    question: "这是重复查询、候选失效还是子问题复用？哪份历史值得保留，哪批候选已经不可能有用？",
    must: [
      "指出最昂贵或最频繁的重复动作，并判断它属于重复查询、候选失效、子问题复用，还是多种同时存在。",
      "问清这份信息未来是否还会被读取、读取时需要值/位置/次数/有效期，以及什么时候失效。",
      "写出为了消除重复劳动必须支持的操作，例如查询、插入、取极值、回溯或删除。",
    ],
    frame: "最浪费的重复动作是……，它属于……；未来第……步会回来问……；为了回答它，我必须能快速……；真正需要留下的信息是……；旧候选在……后可以丢弃。",
    reject: "还没找到重复劳动或候选寿命，就因为题目标签、候选池或数据规模直接点名某个算法。",
  },
  {
    index: "08",
    title: "确认算法方向，再进入推导链",
    question: "哪个候选方案真正满足当前过程所需操作和预算？其他看似可行的方法为什么不优先？",
    must: [
      "列出至少两个候选方向，分别说明所需操作、代价和失效条件。",
      "选择与当前过程最贴合的最小方案，不按“高级程度”选择。",
      "用自己的话确认方向；在确认之前不写完整 Java，不进入模板复述。",
    ],
    frame: "候选方案有……；其中……不能满足……；我选择……，因为它能支持……操作且符合……预算；如果条件变成……，这个选择才会失效。",
    reject: "只知道一个方法名，却说不出它替掉了哪份重复劳动、依赖哪些条件以及为什么不选更简单的方案。",
  },
];

const ALGORITHM_CHAIN_STEPS = [
  {
    index: "01",
    title: "定义状态的真实含义",
    question: "每个变量保存的是哪一个题目事实？它是否足够支持下一步判断？",
    must: [
      "用完整句子定义状态，例如“下标 i 之前出现过的数值及其位置”。",
      "区分状态、临时变量、输入本身和最终答案。",
      "说明状态为什么足够，以及哪些更细的信息可以被压缩掉。",
    ],
    frame: "变量……表示……；它覆盖的对象范围是……；我不保存……，因为后续判断只需要……。",
    reject: "只写 dp[i]、left、right 等名字，却不能在题目世界里说清它们代表什么。",
  },
  {
    index: "02",
    title: "确定初始状态、停止条件和答案时机",
    question: "过程从哪里开始，什么时候结束，结果在哪一步被产生或读取？",
    must: [
      "逐项写出初始值，并说明它对应的现实含义。",
      "说明循环或递归的停止条件，以及停止时哪些状态已经完整。",
      "指出答案是在过程中立即产生，还是最后从状态中读取。",
    ],
    frame: "在还没有处理任何对象前，……；当……时过程停止；答案在……时产生，因为从那时起……已经确定。",
    reject: "初始化靠模板记忆，停止条件与题目目标脱节，或说不出为什么最后返回这个变量。",
  },
  {
    index: "03",
    title: "写清一次状态转移",
    question: "当前事件到来后，先读什么、计算什么、写入什么？下一轮凭什么还能继续？",
    must: [
      "把一次转移拆成输入事件、旧状态、计算、新状态四部分。",
      "在最小例子上逐轮演算至少三轮，并预测下一轮。",
      "解释当前选择依赖的题目条件，不把转移写成只有代码才能读懂的形式。",
    ],
    frame: "第……轮读取……；根据……计算……；然后把……更新为……；下一轮因此可以继续做……。",
    reject: "能写出循环，却不能手算下一轮；或状态更新只能用运行结果反推。",
  },
  {
    index: "04",
    title: "确认更新顺序",
    question: "查询、计算、写入、删除和覆盖中，哪两个动作交换后会产生错误？",
    must: [
      "指出同一轮里多个写操作的依赖顺序。",
      "说明“先查后写”“先取后删”“先保存旧值再覆盖”等原因。",
      "构造一个最小输入，展示错误顺序实际会错在哪里。",
    ],
    frame: "必须先……再……，因为如果反过来，……会读取到本轮刚写入的……，导致……。",
    reject: "只会背代码顺序，不能指出交换顺序后产生的具体错误结果。",
  },
  {
    index: "05",
    title: "建立不变量与正确性理由",
    question: "每一步开始和结束时，什么关系始终成立？它如何保证不漏解、不重复、不误删？",
    must: [
      "写出与当前算法对象绑定的一条或几条不变量。",
      "说明每条不变量依赖哪些题目条件和更新顺序。",
      "把“不会漏”和“不会多”分别说清，而不是只给一个总体结论。",
    ],
    frame: "每一轮开始时始终有……；因此已经处理的范围内……不会漏；每次只在……时结算，因此不会……。",
    reject: "用“显然”“标准做法”或“模板保证”代替证明，或只复述复杂度。",
  },
  {
    index: "06",
    title: "从所需操作反推结构",
    question: "算法过程实际需要哪些查询和修改？所选结构的长处是否正好对应这些操作？",
    must: [
      "列出过程中必须支持的查询、插入、删除、取极值、遍历或回退。",
      "比较数组、哈希、栈、队列、堆、树或图结构的具体操作代价。",
      "说明更简单的结构为什么不够，以及当前结构的额外空间换来了什么。",
    ],
    frame: "过程必须频繁……；数组在这里需要……，而……可以在……时间内完成……；因此结构选择服务于……，不是为了套标签。",
    reject: "先写结构名再倒推理由，或无法说出同一操作在替代结构中的代价。",
  },
  {
    index: "07",
    title: "伪代码、Java 与过程逐段对齐",
    question: "每一段代码对应自然语言中的哪个对象和动作？关键标识符与更新位置能否一一指回？",
    must: [
      "先写与状态定义一致的伪代码，再写清晰 Java 基准实现。",
      "逐个解释初始化、循环、关键判断、状态写入和返回语句。",
      "保留能说明过程的中间变量，不以短代码替代尚未展开的推理。",
    ],
    frame: "伪代码中的……对应 Java 的……；这一行完成的是……；它必须位于……之后，因为……。",
    reject: "代码能运行，但换一个变量名或改变一行位置后，无法解释行为为什么变化。",
  },
  {
    index: "08",
    title: "反例、边界与闭卷重建",
    question: "改哪个条件会让模型失效？关闭资料后，能否独立重建过程、代码和自己的检查输入？",
    must: [
      "主动构造一个挑战不变量的最小输入并完整演算。",
      "把空输入、单元素、重复值、极端值等边界落到具体状态变化上。",
      "闭卷完成口述、手算、伪代码、Java 和自测，只记录最早真实缺口。",
    ],
    frame: "当条件……改变后，模型会在……失效，最小反例是……；我在闭卷时第一处卡住的是……，下一次从这里继续。",
    reject: "边看答案边抄、只列边界名称，或用“运行通过”和“看懂了”代替独立重建。",
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
        <small>人类读题 · 方向确认 · 推导链</small>
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
      <h1>先像人一样读懂题，再像计算机一样验证模型</h1>
      <p>
        先读原题、扩写成人话、清点对象、手工走例子，再用数据范围排除方向；
        确认算法以后，才进入状态、更新、不变量、代码和反例。不能反过来用方法名替代读题过程。
      </p>
      <div class="home-actions">
        <a class="primary-button" href="#/review">
          <i data-lucide="git-branch"></i>
          从人类读题开始
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
            <p>先重建人的判断过程，再验证算法和代码。</p>
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
            <p>能说出“我为什么想到”与能运行代码同样重要。</p>
          </div>
        </div>
        <div class="review-evidence-list">
          <div><span>扩写</span><p>补全谁在做什么、何时停止，每条扩写都能指回原句。</p></div>
          <div><span>手算</span><p>不跳步骤走完最小例子，并说清重复劳动在哪里。</p></div>
          <div><span>选向</span><p>用操作需求和数据预算比较候选方案，不靠标签猜方法。</p></div>
          <div><span>重建</span><p>闭卷重建状态、更新顺序、不变量、Java 和自己的检查输入。</p></div>
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
        <p class="review-eyebrow"><i data-lucide="git-branch"></i>人类读题与算法确认</p>
        <h1>先走完一个人会怎么想，再验证机器会怎么做</h1>
        <p>
          拿到题先只读事实，再把压缩题面扩写成完整生活过程；随后清点对象、手工做例子、
          第一次捕捉变化、读范围并生成候选池、第二次寻找重复劳动。只有说清“为什么需要这些操作”并比较候选确认方向，
          才进入状态、不变量、代码和反例。方法名不能替代这条人类判断路径。
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
          <a class="secondary-button" href="${docHref("LeetCode-系统复习/05-单题流程/人类读题与算法确认.md")}">
            <i data-lucide="route"></i>完整标准与示例
          </a>
          <a class="secondary-button" href="${docHref("LeetCode-系统复习/05-单题流程/人类推导样板与评分.md")}">
            <i data-lucide="notebook-tabs"></i>四题推导验收
          </a>
          <a class="secondary-button" href="${docHref("03-资料/高效理解与回忆方法.md")}">
            <i data-lucide="brain"></i>理解与回忆方法
          </a>
        </div>
      </header>

      <section class="review-chain-section">
        <div class="review-section-head">
          <div>
            <h2>第一层：从题面走到算法方向</h2>
            <p>
              这八个入口不是八个待办项，而是八次必须依次通过的人类判断。第 6 入口同时包含约束、操作预算和候选池；
              第一次捕捉变化是“发生了什么”，第二次捕捉变化才找重复、失效和复用。候选池不是结论，范围也不直接替你选算法。
            </p>
          </div>
          <span class="review-chain-count">8 个读题入口</span>
        </div>
        <ol class="review-chain">
          ${HUMAN_READING_STEPS.map(renderReviewChainStep).join("")}
        </ol>
      </section>

      <div class="review-phase-divider">
        <span><i data-lucide="shield-check"></i>方向闸门</span>
        <strong>没有确认“需要哪些操作、排除哪些方向”，不要进入代码。</strong>
        <p>方向确认不是说出算法名，而是能说明：哪份重复劳动要被消除，候选结构是否支持所需操作，以及数据范围为什么允许它。</p>
      </div>

      <section class="review-chain-section review-derivation-section">
        <div class="review-section-head">
          <div>
            <h2>第二层：算法方向确认后的推导链</h2>
            <p>
              从这里开始才讨论状态、更新和代码。每一段都继承第一层的判断；
              如果状态定义无法回到题干中的对象和变化，说明算法方向尚未真正确认。
            </p>
          </div>
          <span class="review-chain-count">8 个模型确认点</span>
        </div>
        <ol class="review-chain">
          ${ALGORITHM_CHAIN_STEPS.map(renderReviewChainStep).join("")}
        </ol>
      </section>

      <section class="review-evidence" aria-label="怎样确认这一段真的通过">
        <div class="review-section-head">
          <div>
            <h2>两层都通过，才算真正完成本轮</h2>
            <p>只证明代码正确还不够。至少要能重新生成“一个人为什么走到这个算法”的完整判断过程。</p>
          </div>
        </div>
        <div class="review-evidence-grid">
          <div><span>01</span><strong>能扩写</strong><p>把题干补成完整过程，每个新增解释都能追溯到原句。</p></div>
          <div><span>02</span><strong>能想到</strong><p>从朴素过程、预算和重复劳动推导候选方向，并说明排除理由。</p></div>
          <div><span>03</span><strong>能证明</strong><p>状态、更新顺序和不变量互相一致，改动条件能指出失效点。</p></div>
          <div><span>04</span><strong>能重建</strong><p>闭卷重走人类判断、写伪代码、Java 和自己设计的检查输入。</p></div>
        </div>
      </section>

      <section class="review-rules" aria-label="复习停止与推进规则">
        <div>
          <span><i data-lucide="scan-search"></i>先想人怎么做</span>
          <h3>不要从方法名倒推过程</h3>
          <p>如果还不能扩写题干或手工走完例子，先停在这里。看题解时也只补最早缺失的对象、动作或变化。</p>
        </div>
        <div>
          <span><i data-lucide="gauge"></i>范围只做排除</span>
          <h3>候选池不等于算法答案</h3>
          <p>先分开官方约束、操作预算和候选方向，再由重复操作、候选寿命和变化方式确认算法。</p>
        </div>
        <div>
          <span><i data-lucide="badge-check"></i>证据验收</span>
          <h3>方向与代码都要能解释</h3>
          <p>通过条件是可扩写、可手算、可解释方案选择、可证明更新，并能闭卷重建代码与测试。</p>
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

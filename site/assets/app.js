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
  factBank: null,
  factBankPromise: null,
  factBankRequest: 0,
  bankActive: false,
  bankView: "official",
  bankGroup: "all",
  bankQuery: "",
  bankDifficulty: "all",
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

const HANDOFFS = [
  {
    index: "01",
    stage: "阶段 1",
    stageTitle: "原题事实",
    title: "只读题目真正写了什么",
    question: "我刚打开题，题目到底给了我什么，要我交回什么？",
    whyNow: "手里只有题面文字，连哪些事实重要都还不知道，所以现在只能先收集有来源的事实。",
    paper: "先遮住数据范围、标签和题解；圈出返回要求；分栏抄输入、输出、保证、禁止、示例和未知；脑中冒出的方法只记成“记忆候选”。",
    evidence: "一份每条都能指回原句的题目事实表。",
    only: "题目明确写了什么，以及我此刻真实知道和不知道什么。",
    cannot: "一个普通人应该按什么顺序动手，更不知道哪类算法方向合适。",
    nextQuestion: "拿着这些对象，我第一步先做什么？",
    nextEvidence: "一条按时间可执行的人话过程。",
    returnTo: "原句，逐字检查输入、输出、返回形式、保证和禁止。",
    blocked: "具体方法名、结构名、复杂度结论，或题目没有写出的条件。",
  },
  {
    index: "02",
    stage: "阶段 2",
    stageTitle: "人话扩写",
    title: "把题干扩成普通人能执行的动作",
    question: "我手里拿着什么，第一步先碰谁，接下来反复做什么，何时停止？",
    whyNow: "题目事实已经分开，但它们仍是静态文字，没有先后动作，也没有停止时机。",
    paper: "逐句写“原句 -> 自己的话 -> 要做的动作 -> 忽略会错在哪”，再合成谁拿什么、先看哪里、重复做什么、哪个条件改变动作或停止。",
    evidence: "一条另一个人只读文字就能照着演完的人话过程。",
    only: "怎样机械地执行题意，以及每个条件防住了什么错误。",
    cannot: "值、位置和身份是否已经分清，也不知道哪一刻答案真的确定。",
    nextQuestion: "这里面谁是一个独立对象，值和位置怎样分开？",
    nextEvidence: "两个值相同但位置不同的最小身份证据。",
    returnTo: "原句，检查被漏掉的动作、身份、顺序或停止条件。",
    blocked: "优化理由、答案确定时刻、具体结构名，或题面没有保证的规则。",
  },
  {
    index: "03",
    stage: "阶段 3",
    stageTitle: "对象",
    title: "先分清谁有独立身份",
    question: "两个看起来一样的值，到底算同一个东西，还是两个不同位置上的对象？",
    whyNow: "人话过程已经能执行，但里面同时出现值和位置；如果身份混在一起，后面就无法保留正确答案。",
    paper: "把两个相同的值分别写在两个位置或时间下，再填对象表：对象、值和状态、身份依据、位置、关系、最终结果。",
    evidence: "每个对象的身份、位置、关系和结果归属，并且相同值不会被误合并。",
    only: "哪些信息必须跟着对象一起保留，哪些值可以相同但身份不同。",
    cannot: "一个普通人按什么顺序把对象走完，也不知道答案在何时确定。",
    nextQuestion: "照最直接的人类办法，第一眼先处理谁，接着处理谁？",
    nextEvidence: "一个最小但完整例子的逐行手算。",
    returnTo: "人话扩写，确认某条结果到底绑定在哪个对象、哪个位置上。",
    blocked: "代码容器、结构选择、优化结论，或没有身份证据就填写对象表。",
  },
  {
    index: "04",
    stage: "阶段 3",
    stageTitle: "慢过程",
    title: "走一遍最笨但正确的过程",
    question: "我现在到底按什么顺序执行，才能亲手得到正确答案？",
    whyNow: "对象已经分清，但它们还没有在时间上真正动起来，任何高效方向都还没有可比较的过程。",
    paper: "选一个最小但完整的例子，逐行写“看见谁 -> 处理谁 -> 做什么 -> 什么变了 -> 为什么继续”。",
    evidence: "一条能换例子复走的人工过程，而不是只有输入和输出。",
    only: "最直接的办法怎样得到正确答案，以及哪些对象在过程中参与。",
    cannot: "哪份工作重复得太多，也不知道答案在哪一刻成为确定结果。",
    nextQuestion: "过程里第一次真正变化的是谁，答案什么时候确定？",
    nextEvidence: "变化前、触发事件、变化后和写下答案的具体动作。",
    returnTo: "对象表和最小例子；例子太大就缩小，看不到关系就补一个会触发关系的对象。",
    blocked: "优化理由、最终结构、用输入输出摘要代替演算，或用“然后算法会……”补步骤。",
  },
  {
    index: "05",
    stage: "阶段 3",
    stageTitle: "第一次变化",
    title: "找出第一次变化与答案确定时刻",
    question: "哪一刻哪个对象从什么状态变成什么状态，答案为什么从这一刻开始确定？",
    whyNow: "完整过程刚走完，第一次停止、写入或候选成立的动作现在才真实可见。",
    paper: "在过程记录里圈出第一次变化，写清变化前、触发事件、变化后，以及题目凭什么允许此刻停止。",
    evidence: "第一次状态变化和答案确定时刻，并且能指回原题保证。",
    only: "过程里第一次发生了什么，哪个事件让答案成为确定结果。",
    cannot: "这份慢是否超预算，也不能回答应该保存什么或采用什么结构。",
    nextQuestion: "这种慢过程在最坏输入上大约要重复多少次？",
    nextEvidence: "完整约束、最坏输入形状和逐轮操作预算。",
    returnTo: "交接 4 的人工过程；如果答案时刻依赖题目保证，再回交接 1 核对原句。",
    blocked: "保存方案、最终结构或优化结论。",
  },
  {
    index: "06",
    stage: "阶段 4",
    stageTitle: "数据范围",
    title: "计算慢过程预算，降级方法记忆",
    question: "这份慢过程在最坏输入上会重复多少次，哪些复杂度家族先不能稳定承受，哪些方向只能先算待验证？",
    whyNow: "没有完整人工过程就没有资格数重复；现在过程已经走通，才第一次能估算它的代价，也才可能把脑中的方法记忆降级成待验证方向。",
    paper: "抄全约束，选最坏输入，数一轮核心动作并乘轮数；把官方约束、自己的预算和排除的复杂度家族分栏写。冒出方法记忆时，另写“待验证方向”并补齐六项证据。",
    evidence: "有来源的数据约束、自己的操作预算、被排除的复杂度家族，以及未获证明资格的待验证方向。",
    only: "哪些量级不能稳定承受最坏输入，以及方法记忆可能想消除哪份重复工作。",
    cannot: "具体应该保存什么，也不能替人宣布任何实现方向；待验证方向仍没有选择资格。",
    nextQuestion: "带着这份代价重看同一条过程，哪份信息真的被重复读取、过期、复用或必须保序？",
    nextEvidence: "同一条人工过程上的最小重复、失效、复用或顺序证据。",
    returnTo: "交接 4 和交接 5；没有过程就回去手算，没有答案时刻就先补第一次变化。",
    blocked: "待验证区外的裸方法名、六项不全的记忆候选、把待验证方向当结论，或用“看到某个范围就选某种做法”的暗号。",
  },
  {
    index: "07",
    stage: "阶段 5",
    stageTitle: "第二次变化",
    title: "证明哪份信息会重复或失效",
    question: "新事件到来后，哪些历史会被再次读取，哪批对象同时失效，哪条顺序不能乱？",
    whyNow: "预算已经说明慢过程可能太贵，但还没有回到过程里证明哪份工作真的重复。",
    paper: "回到同一条人工过程，用最小例子分别寻找重复查询、候选失效、子问题复用和顺序约束，再把现象翻译成查询、加入、删除、取极值或保序等操作。",
    evidence: "四类现象的发生状态、最小证据，以及未来必须支持的操作。",
    only: "未来需要读什么、何时可以丢弃、加入与结算必须遵守什么顺序。",
    cannot: "哪个具体容器承担这些操作，也不能提前写完整伪代码或代码。",
    nextQuestion: "哪些候选能承担这些操作，另一个熟悉方向为什么不够？",
    nextEvidence: "至少一个方向的支持、缺口、失效条件、时间空间代价。",
    returnTo: "交接 4 的同一段人工过程；没有预算依据则回交接 6。",
    blocked: "具体容器名、完整伪代码，或没有最小证据就宣布“暴力太慢，所以优化”。",
  },
  {
    index: "08",
    stage: "阶段 6",
    stageTitle: "方向确认",
    title: "比较候选并写出完整因果链",
    question: "哪个候选真正承担了交接 7 的操作，另一个候选在哪个条件下失效？",
    whyNow: "操作需求第一次具体到可以比较；在此之前，任何方法名都只是记忆或猜测。",
    paper: "把每个真实候选写成“支持什么、缺什么、何时失效、代价多少”，再写一句从重复劳动、预算、操作到选择的完整因果句。",
    evidence: "有取舍依据的方向确认句；没有第二个真实候选时如实写“没有形成候选”。",
    only: "当前方向为什么能承担已确认的操作和预算，以及替代方向为何不够。",
    cannot: "状态变量、更新顺序、不变量和完整代码怎样落地。",
    nextQuestion: "怎样把题目对象变成状态，并保证更新顺序不会污染当前判断？",
    nextEvidence: "状态定义、一次转移、更新顺序、不变量和最小反例。",
    returnTo: "交接 7 的操作需求或交接 6 的预算；没有真实歧义就不要编造假候选。",
    blocked: "只有方法名、没有取舍依据、完整代码，或把熟悉程度当作正确性证明。",
  },
  {
    index: "09",
    stage: "阶段 7",
    stageTitle: "完整思维链",
    title: "把对象、状态、代码和反例接成一条链",
    question: "每个状态代表哪个题目对象，先更新谁，为什么不会漏、重复或误删？",
    whyNow: "方向已经确认，代码现在才有资格落地；任何变量和顺序都必须回到前面的人工过程。",
    paper: "逐段填写“题目对象 -> 人工动作 -> 操作需求 -> 状态变量 -> 伪代码 -> 代码位置 -> 更新顺序或不变量 -> 对应反例”，再闭卷重建。",
    evidence: "可验证的状态语义、初始状态、转移、更新顺序、不变量、代码映射和最小反例。",
    only: "当前方向怎样被完整实现，以及换一个边界时最早从哪里失效。",
    cannot: "另一条算法方向是否更好；这里不再换方向，只用反例修正实现。",
    nextQuestion: "换一个边界或闭卷重写时，哪一处会最先断？",
    nextEvidence: "最小反例、边界输入和一次不看资料的完整重建。",
    returnTo: "最先说不清的交接；状态或顺序错误回本段反例，方向没有依据回交接 8。",
    blocked: "更换算法方向、用模板顺序冒充证明，或用“运行通过”补缺失推导。",
  },
];

const TWO_SUM_NINE_HANDOFF_DEMO = [
  {
    title: "原题事实",
    text: "要交回两个不同的原始下标；两个值可以相同，但位置不能相同；题目保证只有一个答案，顺序不限；没有保证数组有序。",
    transition: "这些仍是静态事实，所以下一问只能是“一个人先固定谁、再检查谁”。",
  },
  {
    title: "人话扩写",
    text: "先把一个位置当作 i，再从它右边逐个检查 j；两个位置上的数相加等于 target 就交回 i、j，否则继续换 j。",
    transition: "过程能演，但值、位置和答案对还没有被证明是不同对象。",
  },
  {
    title: "对象",
    text: "用 [3,3]、target=6：两个 3 的值相同，位置 0 和位置 1 却是不同对象。答案属于位置，不属于数值本身。",
    transition: "身份分清了，但还没有逐行走过寻找答案的过程。",
  },
  {
    title: "最笨但正确的过程",
    text: "用 [3,2,4]、target=6：先查 (0,1)=5，再查 (0,2)=7，再查 (1,2)=6；每一对都使用不同位置。",
    transition: "过程得到答案了，但还不知道第一次合法对为什么能直接停止。",
  },
  {
    title: "第一次变化",
    text: "变化前没有合法位置对；触发事件是 (1,2) 第一次满足和等于 target；变化后得到合法答案；题目唯一性让此刻成为答案确定时刻。",
    transition: "答案时刻有了，但这份逐对检查在最大输入上是否太慢还不知道。",
  },
  {
    title: "数据范围",
    text: "n 最多 10^4，最坏约检查 n(n-1)/2 个位置对，约五千万次；数值可达正负 10^9，不能把数值直接当连续下标。这里只排除平方级全量重扫和按值域开表的家族。",
    transition: "预算露出重复，但还没有从同一过程中证明哪份历史会被再次读取。",
  },
  {
    title: "第二次变化",
    text: "用 [3,3] 重走：处理第二个 3 时，需要问“补数以前是否出现、在哪个位置”。这是重复查询；当前元素不能提前进入历史，这是顺序约束。",
    transition: "现在只知道需要按值查历史、取回原位置，并且查询要先于加入；还不知道哪个候选能承担。",
  },
  {
    title: "候选比较与方向确认",
    text: "排序会丢掉原下标；继续重扫会重复平方级工作。保存“历史值 -> 原下标”能按补数查询并取回位置。用 [3,3] 证明必须先查后加，否则会查到自己。",
    transition: "方向确认了，但状态如何初始化、代码如何更新、反例如何锁住顺序还没有落地。",
  },
  {
    title: "状态、更新顺序、不变量和代码",
    text: "处理 i 时，历史只保存下标小于 i 的值和位置。先查 target-nums[i]；找到就返回两个位置；找不到才加入 nums[i] -> i。不变量保证历史不会包含当前元素。",
    transition: "闭卷时从事实、手算、预算、操作和反例重新生成整条链，才算真正完成。",
  },
];

const BEGINNER_ACTION_STEPS = [
  {
    gap: "刚打开题，只有题面文字",
    action: "先遮住约束区、标签和题解；圈出返回要求，分开写“题目给我什么”和“要我交回什么”。",
    evidence: "输入、输出、边界和还不知道的部分。",
    blocked: "猜方法，或把示例当完整规则。",
  },
  {
    gap: "知道要求，但还不会把题干扩写成动作",
    action: "逐句写“原句 -> 自己的话 -> 下一步动作 -> 忽略会错在哪”，再合成一段能照着执行的人话。",
    evidence: "一条普通人能照着执行的人话过程。",
    blocked: "只换同义词，或提前优化。",
  },
  {
    gap: "能讲大概过程，但对象混在一起",
    action: "先写当前卡点，圈一句原句或把相同值写在两个位置上；新增证据成立后，再填六列对象表。",
    evidence: "值、位置、身份、关系和结果归属能够分开。",
    blocked: "没有身份证据就填对象表，或先列代码容器。",
  },
  {
    gap: "对象分清，但不知道最笨但正确的过程怎样走",
    action: "用一个最小但完整的例子，逐步写先看谁、处理谁、做什么、什么变了、为什么继续。",
    evidence: "一条能换例子复走的人工过程。",
    blocked: "用输入输出摘要代替演算。",
  },
  {
    gap: "过程走通，但说不清第一次变化和答案时机",
    action: "在过程记录里圈出第一次状态变化，写清变化前、触发事件、变化后和答案确定时刻。",
    evidence: "第一次变化和答案为什么此刻确定。",
    blocked: "回答应该保存什么，或提前出现最终结构。",
  },
  {
    gap: "看见变化，但不知道是否值得处理",
    action: "现在才展开数据范围，在最坏输入上数核心动作重复量；范围只回答是否超预算和排除哪些量级，想到的方法另写成六项待验证方向。",
    evidence: "官方约束、操作预算、被排除的复杂度家族和未获证明资格的待验证方向。",
    blocked: "把待验证方向当结论，或在待验证区外直接写方法名。",
  },
  {
    gap: "知道贵，但不知道留下什么、何时丢掉",
    action: "回到同一过程，逐类检查重复查询、候选失效、子问题复用和顺序约束，再翻译成操作。",
    evidence: "四类现象的发生状态、最小证据和未来需要的操作。",
    blocked: "还没取证就报容器，或把候选池当成结论。",
  },
  {
    gap: "操作需求具体，但不知道哪个候选能承担",
    action: "把候选的支持、缺口、失效条件和代价逐项比较，写完整因果句。",
    evidence: "有取舍依据的方向确认句；没有真实候选时如实记录。",
    blocked: "只报方法名、编造假候选，或把熟悉程度当证明。",
  },
  {
    gap: "方向已经确认，但状态和代码接不上过程",
    action: "把对象、人工动作、状态、伪代码、Java 代码位置和反例逐段接起来。",
    evidence: "推导链、更新顺序和对应反例。",
    blocked: "让运行通过反过来补缺失的推导。",
  },
];

const HUMAN_ACCEPTANCE_RULES = [
  {
    index: "01",
    title: "题目事实错误一票否决",
    text: "原句、输入输出或约束读错时，后续过程、预算和方向全部失效，不能靠更长的解释补偿。",
  },
  {
    index: "02",
    title: "流畅解释、知道方法名和代码跑通都不等于理解",
    text: "它们只说明表达、记忆或运行结果，不能替代对象过程、操作预算、候选比较和代码映射。",
  },
  {
    index: "03",
    title: "闭卷后必须重新生成判断",
    text: "要重建题目事实、人工过程和方向确认；只复述最终答案或默写代码，不算通过。",
  },
];

const BEGINNER_QUESTION_CARD = [
  {
    index: "01",
    stage: "阶段 1 · 刚读完题",
    ask: "我刚读完题，题目到底给了我什么，要我交回什么？",
    gap: "我刚读完，只能抓住一些名词；题目事实、未知和脑中的方法名还没有分开，所以现在只能先问这一句。",
    evidence: "输入、输出、示例、保证、禁止和未知能分开，且每条都有原题来源。",
    unlock: "答完只得到有来源的题目事实；仍然不能选择算法。",
    blocked: "算法名、结构名、复杂度结论、题目没有保证的条件。",
  },
  {
    index: "02",
    stage: "阶段 2 · 能复述，但不会动手",
    ask: "每个字都懂，可一个普通人在纸上第一步做什么？",
    gap: "我能复述事实，却想不出谁拿着什么、先碰哪里、下一步做什么，所以现在自然要问这一句。",
    evidence: "别人只看扩写就能按时间演完；每个条件能说出它防止的具体错误。",
    unlock: "答完得到一个普通人能照着执行的完整过程；仍然没有优化依据。",
    blocked: "优化理由、最终方法名、没有来源的规则。",
  },
  {
    index: "03",
    stage: "阶段 3 · 先分清对象",
    ask: "两个看起来一样的值，算同一个对象，还是两个不同位置上的对象？",
    gap: "我能讲一个大概过程，却还分不清值、位置、身份和关系。此刻只能先写具体卡点，再做一个纸面动作并记录新增证据；证据出现后才填对象表，不能先选代码容器。",
    evidence: "实际纸面动作产生身份证据；元素、位置、身份、关系、目标和结果能分开，相同的值不会误当成同一个对象。",
    unlock: "答完得到有证据支持的题目对象和关系；此时还没有走人工过程，也还不知道答案何时确定。",
    blocked: "没有新增证据就列对象；代码容器、结构选择、优化结论、尚未手算就宣布的变化。",
  },
  {
    index: "04",
    stage: "阶段 3 · 再走最笨但正确的过程",
    ask: "照着最笨的办法，先看谁、接着看谁，什么时候停？",
    gap: "对象已经分清，但还没有一条能在最小完整例子上按时间走到答案的人工过程；所以现在只走最笨的过程，不解释优化理由。",
    evidence: "换一个最小完整例子仍能照着复走，且每一步都能指出处理了哪个对象。",
    unlock: "答完只得到人工过程；仍然不知道第一次变化和答案确定时刻。",
    blocked: "优化结论、最终结构，或用输入输出摘要替代完整演算。",
  },
  {
    index: "05",
    stage: "阶段 3 · 捕捉第一次变化",
    ask: "哪一刻哪个对象从什么状态变成什么状态，答案为什么从这一刻开始确定？",
    gap: "人工过程已经走完，第一次停止、写入或候选成立的动作现在才真实可见；此前无法回答答案何时确定。",
    evidence: "变化前、触发事件、变化后和答案确定时刻，且答案时刻能指回原题保证。",
    unlock: "答完只得到第一次变化和答案时机；仍然不能回答应该保存什么。",
    blocked: "保存方案、最终结构、优化结论，或把第一次算出候选直接当成答案。",
  },
  {
    index: "06",
    stage: "阶段 4 · 第一次变化之后才读数据范围",
    ask: "慢过程最坏重复多少，哪些复杂度家族承受不了？范围后的方法记忆有没有写成六项待验证方向？",
    gap: "第一次变化已经说清，但还没有操作预算；方法记忆可能同时出现，所以现在只计算代价，并把记忆降级为待验证方向。",
    evidence: "官方约束、操作预算和排除家族分开；待验证方向写全方向、想消除的重复、依赖条件、预算、缺失证据和不能选的理由六项。",
    unlock: "答完只得到预算、排除家族和未获证明资格的待验证方向；交接 8 前不能成为结论。",
    blocked: "把待验证方向当结论、在待验证区外直接写方法名，或从范围直接点名算法。",
  },
  {
    index: "07",
    stage: "阶段 5 · 带着预算回到同一过程",
    ask: "哪份信息会重复读取，哪批候选会失效，哪个子问题会复用，哪条顺序不能乱？",
    gap: "预算已经说明慢过程可能太贵，但还没有回到过程里证明哪份工作真的重复、失效、复用或必须保序。",
    evidence: "四类现象逐项标记发生或未发生，并有最小例子；真实现象已翻译成查询、加入、删除、取极值或保序操作。",
    unlock: "答完才形成操作需求；仍然不能报容器或完整伪代码。",
    blocked: "具体容器、完整伪代码，或没有最小证据就宣布优化。",
  },
  {
    index: "08",
    stage: "阶段 6 · 操作需求已经具体",
    ask: "哪个候选真能承担这些操作，另一个候选在哪个条件下失效？",
    gap: "操作需求已经具体，但候选还没有和操作、寿命、预算及失效条件逐项比较，所以现在才轮到具体方向。",
    evidence: "完整方向确认句；真实候选都有支持、缺口、失效条件和代价；没有真实歧义时不制造假候选。",
    unlock: "答完才允许进入状态、更新顺序和代码推导。",
    blocked: "只有方法名、没有取舍证据、直接写完整 Java。",
  },
  {
    index: "09",
    stage: "阶段 7 · 方向已经确认",
    ask: "对象怎样变成状态，先更新谁，为什么不会漏、重复或误删？",
    gap: "方向和操作需求已经确认，但变量、更新顺序和代码还没有逐段接上过程，所以现在才进入完整推导链。",
    evidence: "状态、转移、更新顺序、不变量、代码和反例都能回到题目对象、第一次变化与第二次变化。",
    unlock: "答完可以闭卷重建判断路径、伪代码、Java 和测试。",
    blocked: "新的算法方向、未经验证的模板顺序、用运行通过代替证明。",
  },
];

const READING_HARD_GATES = [
  {
    index: "01",
    title: "范围先算预算，再降级方法记忆",
    text: "先数慢过程重复了多少次核心动作，再排除不能稳定承受的复杂度家族。脑中的方法记忆只能写进明确标记的待验证方向，并补齐六项证据；它仍未获证明资格，范围不能替人宣布算法。",
  },
  {
    index: "02",
    title: "第二次变化后才确认方向",
    text: "第一次变化只说发生了什么；必须再用最小例子证明重复、失效或复用真实存在，之后才允许写完整方向确认句。",
  },
  {
    index: "03",
    title: "没有来源不能进入下一步",
    text: "关键结论只能来自原句事实、手算推导、操作预算、候选假设或设计选择。来源混用时要拆开重写。",
  },
];

const LIVE_GENERATION_RULES = [
  {
    index: "01",
    title: "我刚得到",
    text: "只写刚才由一条原句、一个最小例子、一次手算、一次预算或一项候选比较真正得到的证据。没有新增证据，就留在原处。",
  },
  {
    index: "02",
    title: "它只能说明",
    text: "限定这份证据当前能证明的最小范围。不要把“数值不同”扩成“身份不同”，也不要把一个例子的结果扩成全部输入。",
  },
  {
    index: "03",
    title: "它还不能说明",
    text: "指出它留下的最早空缺：对象、过程、变化、预算、操作需求或候选取舍中的哪一项仍未确定。",
  },
  {
    index: "04",
    title: "因此现在只允许问",
    text: "下一问只能用当前空缺回答，并且小到能当场用一条原句、最小例子、手算、预算或候选比较处理；回答并留下证据后，才允许再问下一句。",
  },
];

const READING_SOURCE_RULES = [
  ["原句事实", "题目写了什么", "不能证明算法方向"],
  ["手算推导", "这个例子发生了什么", "不能证明所有输入"],
  ["操作预算", "最多重复多少", "不能指定具体方法"],
  ["候选假设", "方向可能承担什么", "不能当成已选中"],
  ["设计选择", "状态和代码怎样落实", "不能反证方向正确"],
];

const ALGORITHM_CHAIN_STEPS = [
  {
    index: "01",
    title: "定义状态的真实含义",
    question: "每个变量保存的是哪一个题目事实？它是否足够支持下一步判断？",
    novice: "小白常以为变量名就是状态定义。真正的问题是：这个变量在题目世界里覆盖哪些对象，未来哪一步会读取它。",
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
    novice: "小白常靠模板决定初值。回到最小例子的起点，看每个初值在现实中代表什么，初始化才有来源。",
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
    novice: "小白常能写出循环，却不知道一次循环改变了什么。把一轮拆成读取、计算和写入，才能预测下一轮。",
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
    novice: "小白常背“先查后写”，却说不清交换后的错误。用一个最小输入让错误真的发生，顺序理由才成立。",
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
    novice: "小白常把正确性说成“模板保证”。不变量要分别回答为什么不会漏、不会重复，以及为什么可以安全丢弃。",
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
    novice: "小白常先选结构再找用途。反过来，从过程真正需要的查询、插入、删除和取极值，比较哪个结构最贴合。",
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
    novice: "小白常让代码跑通就算理解。逐段对齐是在确认每一行是否真的对应一个题目对象、动作或状态变化。",
    must: [
      "先写与状态定义一致的伪代码，再写清晰 Java 基准实现。",
      "先填“题目对象 -> 人工动作 -> 第二次变化提出的操作要求 -> 状态变量 -> 伪代码 -> Java 代码位置 -> 更新顺序或不变量 -> 对应反例”。",
      "逐个解释初始化、循环、判断、读取、写入和返回；任何一行接不上都回到最早缺口。",
      "保留能说明过程的中间变量，不以短代码替代尚未展开的推理。",
    ],
    frame: "题目对象……在人工过程里……；它要求……操作；因此状态变量是……；伪代码步骤……对应 Java 代码位置……；它必须位于……之后，因为……；如果反过来，反例……会出错。",
    reject: "代码能运行，但换一个变量名或改变一行位置后，无法解释行为为什么变化。",
  },
  {
    index: "08",
    title: "反例、边界与闭卷重建",
    question: "改哪个条件会让模型失效？关闭资料后，能否独立重建过程、代码和自己的检查输入？",
    novice: "小白常把闭卷重建变成默写代码。真正要重建的是读题、方向、模型、代码和自测之间的连续关系。",
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
  elements.content.addEventListener("input", handleContentControls);
  elements.content.addEventListener("change", handleContentControls);
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
  if (target.bank) {
    renderFactBank(target.query);
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
  if (encodedPath === "bank") {
    return { bank: true, query: new URLSearchParams(query) };
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
    <div class="landmark-links">
      <a class="review-nav-link fact-bank-nav-link ${state.bankActive ? "active" : ""}" href="#/bank">
        <span class="review-nav-icon"><i data-lucide="library-big"></i></span>
        <span>
          <strong>官方事实题库</strong>
          <small>原题事实 · 约束 · 四类视图</small>
        </span>
        <i data-lucide="arrow-up-right"></i>
      </a>
      <a class="review-nav-link ${state.reviewActive ? "active" : ""}" href="#/review">
        <span class="review-nav-icon"><i data-lucide="rotate-ccw"></i></span>
        <span>
          <strong>复习中心</strong>
          <small>人类读题 · 方向确认 · 推导链</small>
        </span>
        <i data-lucide="arrow-up-right"></i>
      </a>
    </div>
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
  if (state.bankActive) {
    elements.sidebarNav.querySelector(".fact-bank-nav-link")?.classList.add("active");
    return;
  }
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
  state.bankActive = false;
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
  state.bankActive = false;
  state.currentPath = null;
  state.currentAnchor = null;
  updateActiveNav(null);
  elements.tocPanel.hidden = true;
  const stats = state.manifest.stats;
  const problemsNav = state.manifest.nav.find((section) => section.id === "problems");
  const topics = problemsNav?.topics || [];
  const startItems = state.manifest.nav.find((section) => section.id === "start")?.items || [];
  const reviewItems = [
    "LeetCode-系统复习/05-单题流程/单题推导标准卡.md",
    "学习看板/单题复习工作台.md",
    "LeetCode-系统复习/00-总入口.md",
    "LeetCode-系统复习/01-复习计划/16周弹性计划.md",
    "LeetCode-系统复习/05-单题流程/单题时间切片.md",
    "LeetCode-系统复习/07-分析法实验/README.md",
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
        先读原题、扩写成人话、留下当前困惑和纸面动作、再填对象表并手工走例子，最后用数据范围排除方向；
        确认算法以后，才进入状态、更新、不变量、代码和反例。不能反过来用方法名替代读题过程。
      </p>
      <div class="home-actions">
        <a class="primary-button" href="#/bank">
          <i data-lucide="library-big"></i>
          从官方题面开始
        </a>
        <a class="secondary-button" href="#/review">
          <i data-lucide="git-branch"></i>
          推导链复习
        </a>
        <a class="secondary-button" href="${docHref("LeetCode-系统复习/05-单题流程/单题推导标准卡.md")}">
          <i data-lucide="route"></i>
          单题推导标准卡
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
        ${renderStat("官方题面事实", state.manifest.factBank?.stats.records || stats.problems, "题", "library-big", `${state.manifest.factBank?.stats.interview || 0} 道本地 P0 策展`)}
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

function handoffAnchorId(handoff) {
  return `handoff-${handoff.index}`;
}

function renderHandoffField(label, text, className, icon) {
  return `
    <div class="handoff-field ${className || ""}">
      <span><i data-lucide="${icon}"></i>${escapeHtml(label)}</span>
      <p>${escapeHtml(text)}</p>
    </div>
  `;
}

function renderHandoffCard(handoff, options = {}) {
  const compact = options.compact === true;
  return `
    <article class="handoff-card${compact ? " handoff-card-compact" : ""}" id="${handoffAnchorId(handoff)}">
      <header class="handoff-card-head">
        <span class="handoff-index">${escapeHtml(handoff.index)}</span>
        <div>
          <p class="handoff-stage">${escapeHtml(handoff.stage)} · ${escapeHtml(handoff.stageTitle)}</p>
          <h3>${escapeHtml(handoff.title)}</h3>
        </div>
      </header>
      <div class="handoff-fields">
        ${renderHandoffField("小白此刻真正的原话疑问", handoff.question, "handoff-field-question", "message-circle-question")}
        ${renderHandoffField("为什么这个疑问现在才出现", handoff.whyNow, "handoff-field-why", "clock-3")}
        ${renderHandoffField("纸上实际做了什么", handoff.paper, "handoff-field-paper", "pencil-line")}
        ${renderHandoffField("做完后新增了什么证据", handoff.evidence, "handoff-field-evidence", "file-check-2")}
        ${renderHandoffField("这份证据只能说明什么", handoff.only, "handoff-field-only", "circle-check")}
        ${renderHandoffField("它还不能说明什么", handoff.cannot, "handoff-field-cannot", "circle-slash-2")}
        ${renderHandoffField("因此下一问只能是什么", handoff.nextQuestion, "handoff-field-next", "arrow-down")}
        ${renderHandoffField("回答它需要什么证据", handoff.nextEvidence, "handoff-field-next-evidence", "scan-search")}
        ${renderHandoffField("如果答不出，退回哪里", handoff.returnTo, "handoff-field-return", "corner-up-left")}
      </div>
      <p class="handoff-blocked">
        <i data-lucide="shield-x"></i>
        <span><strong>这一段仍不能提前出现：</strong>${escapeHtml(handoff.blocked)}</span>
      </p>
    </article>
  `;
}

function renderHandoffContract(handoff) {
  return renderHandoffCard(handoff, { compact: true });
}

function renderReviewCenter(query = null) {
  state.reviewActive = true;
  state.bankActive = false;
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
        <h1>拿一张现场纸，按人真正会想到的顺序得到答案</h1>
        <p>
          开始前先遮住数据范围、标签、题解和讨论区。只读题意、示例和返回要求，然后依次留下题目事实、
          可执行人话、对象表、逐行手算、第一次变化、范围预算、第二次变化、方向确认和实现链。
          数据范围只回答“当前慢过程是否超预算、哪些复杂度家族先排除”，不能直接回答“该用哪个算法”。
          九个字段是整条现场走完后的证据留痕，不是开始前要背的表格。
        </p>
        <ol class="review-causal-path" aria-label="从小白读题到确认算法方向的九次交接">
          <li><span>01</span><strong>读题</strong><p>题目给了我什么，要我交回什么？</p></li>
          <li><span>02</span><strong>人话动作</strong><p>一个人先拿什么，反复做什么，何时停？</p></li>
          <li><span>03</span><strong>对象</strong><p>两个相同的值，是不是同一个对象？</p></li>
          <li><span>04</span><strong>笨过程</strong><p>最直接的人类办法怎样完整走一遍？</p></li>
          <li><span>05</span><strong>第一次变化</strong><p>哪一刻什么变了，答案何时算定？</p></li>
          <li><span>06</span><strong>范围预算</strong><p>最坏重复多少，哪些复杂度家族先排除？</p></li>
          <li><span>07</span><strong>第二次变化</strong><p>哪份信息重复、失效、复用或必须保序？</p></li>
          <li><span>08</span><strong>方向确认</strong><p>哪个候选能承担操作，另一个为什么不够？</p></li>
          <li><span>09</span><strong>思维链</strong><p>对象怎样变成状态、顺序、不变量和代码？</p></li>
        </ol>
        <div class="review-hero-actions">
          ${
            suggested
              ? `<a class="primary-button" href="${docHref(suggested.path)}">
                  <i data-lucide="book-open-check"></i>
                  从「${escapeHtml(cleanProblemTitle(suggested.title))}」按九次交接重建
                </a>`
              : ""
          }
          <a class="secondary-button" href="#/review?pick=1">
            <i data-lucide="list-filter"></i>自己选择题目
          </a>
          <a class="secondary-button" href="${docHref("学习看板/单题复习工作台.md")}">
            <i data-lucide="list-checks"></i>记录本轮断点
          </a>
          <a class="secondary-button" href="${docHref("LeetCode-系统复习/05-单题流程/单题推导标准卡.md")}">
            <i data-lucide="clipboard-list"></i>单题推导标准卡
          </a>
          <a class="secondary-button" href="${docHref("LeetCode-系统复习/05-单题流程/小白读题现场示范.md")}">
            <i data-lucide="message-circle-more"></i>小白现场示范
          </a>
          <a class="secondary-button" href="${docHref("LeetCode-系统复习/05-单题流程/人类推导样板与评分.md")}">
            <i data-lucide="notebook-tabs"></i>四题推导样板
          </a>
          <a class="secondary-button" href="${docHref("03-资料/高效理解与回忆方法.md")}">
            <i data-lucide="brain"></i>理解与回忆方法
          </a>
        </div>
      </header>

      <section class="review-chain-section review-handoff-main" aria-label="七阶段九次交接唯一主线">
        <div class="review-section-head">
          <div>
            <h2>唯一现场：七阶段、九次交接</h2>
            <p>
              阶段 3 不是一句“分析题意”，而是三次独立交接。交接 1 到 7 只产生题目事实、人工过程、
              第一次变化、预算和第二次变化；交接 8 才把具体候选放上桌；交接 9 才写完整状态和代码。
            </p>
          </div>
          <span class="review-chain-count">9 次交接 · 1 条证据链</span>
        </div>
        <div class="handoff-list">
          ${HANDOFFS.map((handoff) => renderHandoffCard(handoff)).join("")}
        </div>
      </section>

      <details class="handoff-demo" open>
        <summary>
          <span>
            <strong>两数之和：沿九次交接重新生成答案</strong>
            <small>重点不是“用映射”这个结论，而是每次交接为什么现在才轮到它。</small>
          </span>
          <i data-lucide="chevron-down"></i>
        </summary>
        <ol class="handoff-demo-list">
          ${TWO_SUM_NINE_HANDOFF_DEMO.map(
            (step, index) => `
              <li>
                <span>${HANDOFFS[index].index}</span>
                <div>
                  <small>${escapeHtml(HANDOFFS[index].stage)} · ${escapeHtml(HANDOFFS[index].stageTitle)}</small>
                  <strong>${escapeHtml(step.title)}</strong>
                  <p>${escapeHtml(step.text)}</p>
                  <em>${escapeHtml(step.transition)}</em>
                </div>
              </li>
            `,
          ).join("")}
        </ol>
      </details>

      <details class="review-diagnostics">
        <summary>
          <span>
            <strong>完成后诊断工具</strong>
            <small>九问、动作表、验收、来源和反写检查只用来定位最早断点，不是第二条解题主线。</small>
          </span>
          <i data-lucide="chevron-down"></i>
        </summary>
        <div class="review-diagnostics-body">
          <section class="review-chain-section" aria-label="完成后的九问复核">
            <div class="review-section-head">
              <div>
                <h2>完成后的九问复核</h2>
                <p>
                  回答时先写清“我刚得到什么、它还不能说明什么、因此现在只检查哪一问”，
                  再把问题对回最早缺失的那次交接。问题本身不推进现场。
                </p>
              </div>
              <span class="review-chain-count">事后查漏 · 9 个问题</span>
            </div>
            ${renderBeginnerQuestionCard()}
          </section>

          <section class="review-chain-section" aria-label="小白起步动作表">
            <div class="review-section-head">
              <div>
                <h2>卡住时先做哪一个纸面动作</h2>
                <p>
                  只处理最早空缺。做完动作后必须多出一份可核对证据；没有形成候选就写“没有形成候选”，
                  没有发生转折就写“没有发生转折”。
                </p>
              </div>
              <span class="review-chain-count">动作 → 证据</span>
            </div>
            ${renderBeginnerActionTable()}
          </section>

          <section class="review-chain-section" aria-label="人类解题验收标准">
            <div class="review-section-head">
              <div>
                <h2>人类解题验收标准</h2>
                <p>验收的是九次交接是否留下证据，以及代码能否逐段回到人工过程。</p>
              </div>
              <span class="review-chain-count">9 次交接 · 3 条硬规则</span>
            </div>
            ${renderHumanAcceptanceStandard()}
            <div class="review-live-gates" aria-label="人类解题验收三条硬规则">
              ${HUMAN_ACCEPTANCE_RULES.map(
                (rule) => `
                  <div>
                    <span>${escapeHtml(rule.index)}</span>
                    <strong>${escapeHtml(rule.title)}</strong>
                    <p>${escapeHtml(rule.text)}</p>
                  </div>
                `,
              ).join("")}
            </div>
          </section>

          <section class="review-chain-section" aria-label="证据来源与反写检查">
            <div class="review-section-head">
              <div>
                <h2>完成后的证据检查</h2>
                <p>
                  原句、手算、预算、候选假设和设计选择各自只能证明自己的部分；后面的代码不能替前面缺失的证据作证。
                </p>
              </div>
              <span class="review-chain-count">来源边界 · 反写检查</span>
            </div>
            ${renderReadingHardGates()}
            <div class="review-diagnostic-split">
              <div>${renderLiveGenerationRules()}</div>
              <div class="review-chain-frame">
                <span>写完后再反写一次</span>
                <p>
                  1. 隐藏最终方法名后，整条推导是否仍然成立？
                  2. 删掉当前证据后，下一问是否自然消失？
                  如果证据没了，下一问还照常存在，说明它来自答案而不是现场。
                </p>
              </div>
            </div>
          </section>

          <section class="review-chain-section" aria-label="交接之后的状态和代码检查">
            <div class="review-section-head">
              <div>
                <h2>交接 9 之后再检查状态、顺序和代码</h2>
                <p>
                  这里不生成新的算法方向。它只检查变量能否回到题目对象、更新顺序是否有反例、
                  不变量能否解释不漏不多，以及闭卷后能否重建。
                </p>
              </div>
              <span class="review-chain-count">实现检查 · 8 个确认点</span>
            </div>
            <ol class="review-chain">
              ${ALGORITHM_CHAIN_STEPS.map(renderReviewChainStep).join("")}
            </ol>
          </section>
        </div>
      </details>

      <section class="review-evidence" aria-label="怎样确认一轮真的完成">
        <div class="review-section-head">
          <div>
            <h2>一轮真正完成时，留下的是四类能力</h2>
            <p>不按题量或速度评价。只看这轮能否扩写、手算、解释方向并闭卷重建。</p>
          </div>
        </div>
        <div class="review-evidence-grid">
          <div><span>01</span><strong>能扩写</strong><p>每个新增解释都能追溯到原句。</p></div>
          <div><span>02</span><strong>能手算</strong><p>最笨过程能换一个最小例子重走，第一次变化有证据。</p></div>
          <div><span>03</span><strong>能解释方向</strong><p>候选从操作和预算长出来，取舍与失效条件说得清。</p></div>
          <div><span>04</span><strong>能重建</strong><p>状态、更新顺序、不变量和代码能逐段回到人工过程。</p></div>
        </div>
      </section>

      <section class="review-rules" aria-label="复习停止与推进规则">
        <div>
          <span><i data-lucide="scan-search"></i>先想人怎么做</span>
          <h3>不从方法名倒推过程</h3>
          <p>不能扩写或不走完例子时，先停在这里。看题解也只补最早缺失的对象、动作或变化。</p>
        </div>
        <div>
          <span><i data-lucide="gauge"></i>范围先算预算</span>
          <h3>候选池不等于算法答案</h3>
          <p>先分开官方约束、操作预算和复杂度家族；方法记忆放进六项待验证方向，再由重复操作、候选寿命和变化方式确认方向。</p>
        </div>
        <div>
          <span><i data-lucide="badge-check"></i>证据验收</span>
          <h3>方向与代码都要能解释</h3>
          <p>通过条件是九次交接留下证据，并能闭卷重建判断、伪代码、Java 和检查输入。</p>
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

  document.title = `七阶段九交接 · ${state.manifest.title}`;
  window.scrollTo({ top: 0, behavior: "auto" });
  refreshIcons();
}

function renderBeginnerQuestionCard() {
  return `
    <ol class="beginner-question-list">
      ${BEGINNER_QUESTION_CARD.map(
        (item) => `
          <li>
            <div class="beginner-question-stage">
              <span>${escapeHtml(item.index)}</span>
              <strong>${escapeHtml(item.stage)}</strong>
              <p>“${escapeHtml(item.ask)}”</p>
            </div>
            <div class="beginner-question-gap">
              <strong><i data-lucide="scan-search"></i>为什么现在只问这一问</strong>
              <p>${escapeHtml(item.gap)}</p>
            </div>
            <div class="beginner-question-contract">
              <div class="beginner-question-evidence">
                <strong><i data-lucide="circle-check"></i>过关证据</strong>
                <p>${escapeHtml(item.evidence)}</p>
              </div>
              <div class="beginner-question-unlock">
                <strong><i data-lucide="lock-open"></i>答完只多出</strong>
                <p>${escapeHtml(item.unlock)}</p>
              </div>
              <div class="beginner-question-blocked">
                <strong><i data-lucide="circle-slash-2"></i>仍不能出现</strong>
                <p>${escapeHtml(item.blocked)}</p>
              </div>
            </div>
          </li>
        `,
      ).join("")}
    </ol>
  `;
}

function renderBeginnerActionTable() {
  return `
    <ol class="beginner-action-list">
      ${BEGINNER_ACTION_STEPS.map(
        (item, index) => `
          <li>
            <div class="beginner-action-gap">
              <span>${String(index + 1).padStart(2, "0")}</span>
              <strong>${escapeHtml(item.gap)}</strong>
            </div>
            <div>
              <strong>现在先做</strong>
              <p>${escapeHtml(item.action)}</p>
            </div>
            <div>
              <strong>做完多出的证据</strong>
              <p>${escapeHtml(item.evidence)}</p>
            </div>
            <div>
              <strong>仍然不能做</strong>
              <p>${escapeHtml(item.blocked)}</p>
            </div>
          </li>
        `,
      ).join("")}
    </ol>
  `;
}

function renderHumanAcceptanceStandard() {
  return `
    <ol class="beginner-live-list beginner-acceptance-list">
      ${HANDOFFS.map(
        (item) => `
          <li>
            <div class="beginner-live-head">
              <span>${escapeHtml(item.index)}</span>
              <strong>${escapeHtml(item.stage)} · ${escapeHtml(item.stageTitle)}</strong>
            </div>
            <div class="beginner-live-grid beginner-acceptance-grid">
              <div class="beginner-live-cell beginner-acceptance-cell">
                <strong>先看什么</strong>
                <p>${escapeHtml(item.question)}</p>
              </div>
              <div class="beginner-live-cell beginner-acceptance-cell">
                <strong>下一件纸面动作</strong>
                <p>${escapeHtml(item.paper)}</p>
              </div>
              <div class="beginner-live-cell beginner-live-evidence beginner-acceptance-cell">
                <strong>允许继续的证据</strong>
                <p>${escapeHtml(item.evidence)}</p>
              </div>
              <div class="beginner-live-cell beginner-live-blocked beginner-acceptance-cell">
                <strong>仍禁止出现</strong>
                <p>${escapeHtml(item.blocked)}</p>
              </div>
              <div class="beginner-live-cell beginner-live-next beginner-acceptance-cell">
                <strong>说不通退回</strong>
                <p>${escapeHtml(item.returnTo)}</p>
              </div>
            </div>
          </li>
        `,
      ).join("")}
    </ol>
  `;
}

function renderReadingHardGates() {
  return `
    <div class="review-live-gates">
      ${READING_HARD_GATES.map(
        (gate) => `
          <div>
            <span>${escapeHtml(gate.index)}</span>
            <strong>${escapeHtml(gate.title)}</strong>
            <p>${escapeHtml(gate.text)}</p>
          </div>
        `,
      ).join("")}
    </div>
    <div class="review-source-rules">
      <div class="review-source-rules-head">
        <strong>每一步的结论必须有来源</strong>
        <span>来源指这一步凭什么可以这样说，不是参考文献</span>
      </div>
      ${READING_SOURCE_RULES.map(
        ([source, proves, cannot]) => `
          <div class="review-source-rule">
            <strong>${escapeHtml(source)}</strong>
            <span>${escapeHtml(proves)}</span>
            <small>不能证明：${escapeHtml(cannot)}</small>
          </div>
        `,
      ).join("")}
    </div>
  `;
}

function renderLiveGenerationRules() {
  return `
    <div class="review-live-gates review-live-gates-four">
      ${LIVE_GENERATION_RULES.map(
        (rule) => `
          <div>
            <span>${escapeHtml(rule.index)}</span>
            <strong>${escapeHtml(rule.title)}</strong>
            <p>${escapeHtml(rule.text)}</p>
          </div>
        `,
      ).join("")}
    </div>
  `;
}

function renderReviewChainStep(step) {
  const allowed = Array.isArray(step.allowed) ? step.allowed.join("；") : step.allowed;
  const hasStageContract = Boolean(step.entry || allowed || step.blocked);
  return `
    <li>
      <span class="review-chain-index">${escapeHtml(step.index)}</span>
      <div class="review-chain-body">
        <h3>${escapeHtml(step.title)}</h3>
        <p>${escapeHtml(step.question)}</p>
        <div class="review-chain-novice">
          <strong><i data-lucide="user-round"></i>小白的自然反应</strong>
          <span>${escapeHtml(step.novice)}</span>
        </div>
        <ul class="review-chain-must">
          ${step.must.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}
        </ul>
        <div class="review-chain-frame">
          <span>这一段至少能完整说出</span>
          <p>${escapeHtml(step.frame)}</p>
        </div>
        ${
          hasStageContract
            ? `<div class="review-chain-contract">
                <div>
                  <strong>进入条件</strong>
                  <span>${escapeHtml(step.entry || "先完成上一段留下的证据门槛。")}</span>
                </div>
                <div>
                  <strong>允许产物</strong>
                  <span>${escapeHtml(allowed || "只留下当前这一段能产生的证据。")}</span>
                </div>
                <div>
                  <strong>禁止产物</strong>
                  <span>${escapeHtml(step.blocked || step.reject)}</span>
                </div>
              </div>`
            : ""
        }
        <div class="review-chain-reject">
          <strong><i data-lucide="circle-x"></i>没有通过</strong>
          <span>${escapeHtml(step.reject)}</span>
        </div>
        ${
          step.returnTo
            ? `<div class="review-chain-return">
                <strong><i data-lucide="arrow-left"></i>说不清就退回</strong>
                <span>${escapeHtml(step.returnTo)}</span>
              </div>`
            : ""
        }
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

async function renderFactBank(query = new URLSearchParams()) {
  state.bankActive = true;
  state.reviewActive = false;
  state.currentPath = null;
  state.currentAnchor = null;
  elements.tocPanel.hidden = true;
  updateActiveNav();

  state.bankView = normalizeBankView(query.get("view") || "official");
  state.bankGroup = query.get("group") || "all";
  state.bankQuery = query.get("q") || "";
  state.bankDifficulty = normalizeBankDifficulty(query.get("difficulty"));
  const selectedId = Number(query.get("id"));
  const requestId = ++state.factBankRequest;

  elements.content.innerHTML = loadingMarkup("正在读取官方题面事实...");
  document.title = `官方事实题库 · ${state.manifest.title}`;

  try {
    await loadFactBank();
    if (requestId !== state.factBankRequest || !state.bankActive) {
      return;
    }
    const selected = Number.isInteger(selectedId) && selectedId > 0
      ? state.factBank.recordById[String(selectedId)] || null
      : null;
    elements.content.innerHTML = renderFactBankPage(selected);
    addCopyButtons(elements.content);
    elements.content.querySelectorAll("pre code").forEach((block) => {
      if (window.hljs) {
        window.hljs.highlightElement(block);
      }
    });
    document.title = selected
      ? `${selected.id}. ${selected.titleCn} · 官方事实题库`
      : `官方事实题库 · ${state.manifest.title}`;
    window.scrollTo({ top: 0, behavior: "auto" });
    refreshIcons();
  } catch (error) {
    if (requestId !== state.factBankRequest || !state.bankActive) {
      return;
    }
    elements.content.innerHTML = renderBankError(error);
    refreshIcons();
  }
}

async function loadFactBank() {
  if (state.factBank) {
    return state.factBank;
  }
  if (!state.factBankPromise) {
    const revision = encodeURIComponent(state.manifest.revision || "local");
    state.factBankPromise = fetch(`assets/fact-bank.json?v=${revision}`, { cache: "no-cache" })
      .then((response) => {
        if (!response.ok) {
          throw new Error(`官方题面事实读取失败：HTTP ${response.status}`);
        }
        return response.json();
      })
      .then((factBank) => {
        state.factBank = factBank;
        return factBank;
      })
      .catch((error) => {
        state.factBankPromise = null;
        throw error;
      });
  }
  return state.factBankPromise;
}

function normalizeBankView(value) {
  return ["official", "interview", "system", "tags"].includes(value) ? value : "official";
}

function normalizeBankDifficulty(value) {
  return ["Easy", "Medium", "Hard"].includes(value) ? value : "all";
}

function bankHref({ view = state.bankView, group = "all", q = "", difficulty = "all", id = null } = {}) {
  const params = new URLSearchParams();
  params.set("view", normalizeBankView(view));
  if (group && group !== "all") {
    params.set("group", group);
  }
  if (q) {
    params.set("q", q);
  }
  if (difficulty && difficulty !== "all") {
    params.set("difficulty", difficulty);
  }
  if (id !== null && id !== undefined && id !== "") {
    params.set("id", String(id));
  }
  return `#/bank?${params.toString()}`;
}

function renderFactBankPage(selectedRecord) {
  const factBank = state.factBank;
  const stats = factBank.stats;
  const views = factBank.views;
  const currentView = views[state.bankView];
  return `
    <section class="fact-bank">
      <header class="bank-hero">
        <p class="review-eyebrow"><i data-lucide="library-big"></i>官方题面事实</p>
        <h1>先读原题，再让推导长出来</h1>
        <p>
          这里只负责给出题面已经写了什么、明确约束了什么，以及哪些内容仍未知。
          不从标签直接宣布算法，也不把本地题解伪装成平台事实。先完成扩写，留下当前困惑、纸面动作和新增证据，再填对象表、走人工过程、读范围并做第二次变化。
        </p>
        <div class="bank-stat-line">
          <span><strong>${stats.records}</strong> 道原题事实</span>
          <span><strong>${stats.easy}</strong> 简单</span>
          <span><strong>${stats.medium}</strong> 中等</span>
          <span><strong>${stats.hard}</strong> 困难</span>
          <span><strong>${stats.interview}</strong> 道本地 P0</span>
        </div>
      </header>

      <nav class="bank-view-switch" aria-label="题面事实视图">
        ${Object.entries(views)
          .map(
            ([id, view]) => `
              <a class="bank-view-tab ${id === state.bankView ? "active" : ""}" href="${bankHref({ view: id })}">
                <span>${escapeHtml(view.label)}</span>
                <small>${escapeHtml(bankViewMeta(id))}</small>
              </a>
            `
          )
          .join("")}
      </nav>

      <section class="bank-view-note" aria-label="当前视图说明">
        <span>${escapeHtml(currentView.label)}</span>
        <p>${escapeHtml(currentView.description)}</p>
      </section>

      ${selectedRecord ? renderBankDetail(selectedRecord) : renderBankBrowser()}
    </section>
  `;
}

function bankViewMeta(view) {
  return {
    official: "Platform snapshot",
    interview: "Local P0 only",
    system: "By problem form",
    tags: "LeetCode tags",
  }[view] || "";
}

function renderBankBrowser() {
  const view = state.factBank.views[state.bankView];
  if (state.bankGroup !== "all" && !view.groups.some((group) => group.id === state.bankGroup)) {
    state.bankGroup = "all";
  }
  const groups = view.groups || [];
  return `
    <section class="bank-browser" id="bank-browser">
      <div class="bank-toolbar">
        <label class="bank-search-control">
          <span>搜索题面、标签或分类</span>
          <i data-lucide="search"></i>
          <input id="bank-query" type="search" value="${escapeAttribute(state.bankQuery)}" placeholder="例如：单调栈、text =、P0">
        </label>
        <label>
          <span>当前视图分组</span>
          <select id="bank-group-filter">
            <option value="all" ${state.bankGroup === "all" ? "selected" : ""}>全部（${state.factBank.stats.records}）</option>
            ${groups
              .map(
                (group) => `
                  <option value="${escapeAttribute(group.id)}" ${group.id === state.bankGroup ? "selected" : ""}>
                    ${escapeHtml(group.label)}（${group.problemIds.length}）
                  </option>
                `
              )
              .join("")}
          </select>
        </label>
        <label>
          <span>LeetCode 难度</span>
          <select id="bank-difficulty-filter">
            ${renderBankOption("all", "全部难度", state.bankDifficulty)}
            ${renderBankOption("Easy", "简单", state.bankDifficulty)}
            ${renderBankOption("Medium", "中等", state.bankDifficulty)}
            ${renderBankOption("Hard", "困难", state.bankDifficulty)}
          </select>
        </label>
      </div>
      <div id="bank-results" aria-live="polite">
        ${renderBankResults()}
      </div>
    </section>
  `;
}

function renderBankOption(value, label, selected) {
  return `<option value="${escapeAttribute(value)}" ${value === selected ? "selected" : ""}>${escapeHtml(label)}</option>`;
}

function renderBankResults() {
  const records = filteredBankRecords();
  const view = state.factBank.views[state.bankView];
  const group = view.groups.find((item) => item.id === state.bankGroup);
  const context = group ? group.label : view.label;
  return `
    <div class="bank-results-meta">
      <span>${escapeHtml(context)}</span>
      <strong>${records.length} 道</strong>
      <small>列表只显示题面事实与分类；打开题目后先停在读题阶段。</small>
    </div>
    ${
      records.length
        ? `<div class="bank-problem-list">${records.map(renderBankProblemRow).join("")}</div>`
        : `
          <div class="bank-empty">
            <i data-lucide="search-x"></i>
            <strong>当前条件下没有题目</strong>
            <p>换一个分组、难度或更短的关键词。筛选结果不是学习进度。</p>
          </div>
        `
    }
  `;
}

function filteredBankRecords() {
  const view = state.factBank.views[state.bankView];
  const group = view.groups.find((item) => item.id === state.bankGroup);
  const allowedIds = group ? new Set(group.problemIds.map(String)) : null;
  const query = normalizeText(state.bankQuery);
  return state.factBank.records
    .filter((record) => !allowedIds || allowedIds.has(String(record.id)))
    .filter((record) => state.bankDifficulty === "all" || record.difficulty === state.bankDifficulty)
    .filter((record) => !query || bankRecordSearchText(record).includes(query))
    .sort(
      (left, right) =>
        ["Easy", "Medium", "Hard"].indexOf(left.difficulty) -
          ["Easy", "Medium", "Hard"].indexOf(right.difficulty) ||
        left.id - right.id
    );
}

function bankRecordSearchText(record) {
  if (!record._searchText) {
    record._searchText = normalizeText(
      [
        record.id,
        record.titleCn,
        record.titleEn,
        record.primaryPattern,
        ...(record.priorities || []),
        ...(record.checklistTags || []),
        ...(record.officialTags || []).map((tag) => tag.translatedName),
        stripHtmlText(record.descriptionHtml),
        ...(record.constraints || []),
      ].join(" ")
    );
  }
  return record._searchText;
}

function renderBankProblemRow(record) {
  const priorities = record.priorities || [];
  return `
    <a class="bank-problem-row" href="${bankHref({
      view: state.bankView,
      group: state.bankGroup,
      q: state.bankQuery,
      difficulty: state.bankDifficulty,
      id: record.id,
    })}">
      <span class="bank-problem-number">${escapeHtml(String(record.id).padStart(2, "0"))}</span>
      <span class="bank-problem-main">
        <strong>${escapeHtml(record.titleCn)}</strong>
        <small>${escapeHtml(record.titleEn || "")} · ${escapeHtml(record.primaryPattern || "未分类")}</small>
      </span>
      <span class="bank-problem-tags">
        <span class="bank-difficulty bank-difficulty-${escapeAttribute(record.difficulty)}">${escapeHtml(difficultyLabel(record.difficulty))}</span>
        ${priorities.map((priority) => `<span class="bank-priority">${escapeHtml(priority)}</span>`).join("")}
        ${record.officialTags.slice(0, 2).map((tag) => `<span>${escapeHtml(tag.translatedName)}</span>`).join("")}
      </span>
      <i data-lucide="arrow-up-right"></i>
    </a>
  `;
}

function renderBankDetail(record) {
  const requiredComplexity = record.complexity?.required || [];
  const advancedComplexity = record.complexity?.advanced || [];
  const tags = (record.officialTags || []).map((tag) => tag.translatedName);
  const priorities = record.priorities || [];
  const solution = record.solution;
  const statement = sanitizeHtml(record.descriptionHtml);
  const sourceSha = record.sourceFactsSha256 ? record.sourceFactsSha256.slice(0, 12) : "未记录";
  return `
    <section class="bank-detail">
      <div class="bank-detail-top">
        <a class="secondary-button compact" href="${bankHref({
          view: state.bankView,
          group: state.bankGroup,
          q: state.bankQuery,
          difficulty: state.bankDifficulty,
        })}">
          <i data-lucide="arrow-left"></i>返回题目列表
        </a>
        <span>Source checked ${escapeHtml(record.sourceCheckedAt || "未记录")}</span>
      </div>

      <header class="bank-detail-head">
        <p class="bank-detail-number">LeetCode ${escapeHtml(record.id)} · ${escapeHtml(difficultyLabel(record.difficulty))}</p>
        <h1>${escapeHtml(record.titleCn)}</h1>
        <p>${escapeHtml(record.titleEn || "")}</p>
        <div class="bank-chip-row">
          ${priorities.map((priority) => `<span class="bank-priority">${escapeHtml(priority)}</span>`).join("")}
          <span><i data-lucide="network"></i>${escapeHtml(record.system?.label || "未分类")}</span>
          ${tags.map((tag) => `<span>${escapeHtml(tag)}</span>`).join("")}
        </div>
      </header>

      <ol class="bank-stage-list" aria-label="人类读题阶段">
        ${[
          ["01", "原题事实"],
          ["02", "人话扩写"],
          ["03", "对象、慢过程与第一次变化 · 交接 3-5"],
          ["04", "数据范围与慢过程预算"],
          ["05", "第二次变化"],
          ["06", "候选比较与方向确认"],
          ["07", "状态、更新顺序、不变量、代码、反例"],
        ]
          .map(
            ([index, label], position) => `
              <li class="${position === 0 ? "active" : ""}">
                <b>${index}</b>
                <span>${label}</span>
              </li>
            `
          )
          .join("")}
      </ol>

      <div class="bank-detail-layout">
        <div class="bank-detail-main">
          <section class="bank-fact-section">
            <div class="bank-section-heading">
              <span>01</span>
              <div>
                <h2>先只读原题事实</h2>
                <p>下面保持题面原样。先把事实、由事实推出的结论和你的猜测分开。</p>
              </div>
            </div>
            ${renderHandoffContract(HANDOFFS[0])}
            <div class="markdown-body bank-statement">${statement}</div>
          </section>

          <section class="bank-fact-section">
            <div class="bank-section-heading">
              <span>02</span>
              <div>
                <h2>先逐句扩写，再合成一个人能执行的过程</h2>
                <p>还不要想对象清单或算法。先确认每个原句新增了谁、什么动作、什么顺序、什么限制，以及忽略它会犯什么具体错误。</p>
              </div>
            </div>
            ${renderHandoffContract(HANDOFFS[1])}
            <ol class="bank-question-list">
              <li>这句话新增了哪个对象、动作、身份、顺序或停止条件？</li>
              <li>如果忽略这句话，我会在过程里做错哪一个具体动作或交回什么错误结果？</li>
              <li>哪一句改变了谁先处理、谁后处理，或者哪个对象不能提前丢掉？</li>
              <li>把这些句子按时间合起来以后，一个普通人从哪里开始、反复做什么、何时停下、最后交出什么？</li>
              <li>扩写里有没有题面没有保证的内容？它只能标成推测，不能拿去证明后面的方向。</li>
            </ol>
            <div class="bank-reading-links">
              <a href="${docHref("LeetCode-系统复习/05-单题流程/单题推导标准卡.md")}">
                <i data-lucide="clipboard-list"></i>按标准卡写下自己的扩写
              </a>
              <a href="${docHref("LeetCode-系统复习/05-单题流程/小白读题现场示范.md")}">
                <i data-lucide="message-circle-more"></i>看小白怎样停下来问下一步
              </a>
            </div>
          </section>

          <section class="bank-fact-section">
            <div class="bank-section-heading">
              <span>03</span>
              <div>
                <h2>先分对象，再走慢过程，最后只记录第一次变化</h2>
                <p>阶段 3 是三次独立交接。交接 3 先产生身份证据并填对象表；交接 4 才能用最小完整例子走最笨但正确的过程；交接 5 只记录变化前、触发事件、变化后和答案确定时刻。</p>
              </div>
            </div>
            <div class="bank-handoff-stack">
              ${renderHandoffContract(HANDOFFS[2])}
              ${renderHandoffContract(HANDOFFS[3])}
              ${renderHandoffContract(HANDOFFS[4])}
            </div>
            ${
              record.officialExamples?.length
                ? `<div class="bank-examples">
                    <p class="bank-muted">用下面示例核对手工过程。示例只检查过程，不替代边界和反例。</p>
                    ${record.officialExamples
                      .map(
                        (example, index) => `
                          <div class="bank-example">
                            <span>示例 ${index + 1}</span>
                            <pre><code>输入：${escapeHtml(example.input || "")}\n输出：${escapeHtml(example.output || "")}${
                              example.explanation ? `\n解释：${escapeHtml(example.explanation)}` : ""
                            }</code></pre>
                          </div>
                        `
                      )
                      .join("")}
                  </div>`
                : `<p class="bank-muted">当前快照没有结构化示例。</p>`
            }
          </section>

          <section class="bank-fact-section">
            <div class="bank-section-heading">
              <span>04</span>
              <div>
                <h2>交接 6：数据范围与慢过程预算</h2>
                <p>先抄官方约束，再单独估算慢过程在最坏输入上的操作量并排除复杂度家族。冒出的方法记忆只能放进“待验证方向”，写全六项证据，仍然不能直接成为结论。</p>
              </div>
            </div>
            ${renderHandoffContract(HANDOFFS[5])}
            <div class="bank-constraint-block">
              <h3>官方约束</h3>
              ${
                record.constraints?.length
                  ? `<ul>${record.constraints.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}</ul>`
                  : `<p class="bank-muted">当前快照没有结构化提示。</p>`
              }
            </div>
            <div class="bank-complexity-grid">
              <div>
                <h3>题面明确要求</h3>
                ${
                  requiredComplexity.length
                    ? `<ul>${requiredComplexity.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}</ul>`
                    : `<p class="bank-muted">题面无明确复杂度要求。</p>`
                }
              </div>
              <div>
                <h3>官方“进阶”建议</h3>
                ${
                  advancedComplexity.length
                    ? `<ul>${advancedComplexity.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}</ul>`
                    : `<p class="bank-muted">题面无额外进阶复杂度建议。</p>`
                }
              </div>
            </div>
            <div class="bank-budget-prompt">
              <strong>接下来由你补上的三层</strong>
              <p>官方事实：上面已经列出。操作预算：最慢的人工过程大约重复多少次？排除范围：哪些复杂度家族不能稳定承受最坏输入？方法记忆另写成六项待验证方向，不把熟悉感当成选择依据。</p>
            </div>
          </section>

          <section class="bank-fact-section">
            <div class="bank-section-heading">
              <span>05</span>
              <div>
                <h2>带着预算第二次捕捉变化</h2>
                <p>第一次变化只说明过程里发生了什么。现在带着操作预算重看，找出真正重复、会失效或可复用的工作，再写清未来需要哪些操作。</p>
              </div>
            </div>
            ${renderHandoffContract(HANDOFFS[6])}
            <ol class="bank-question-list">
              <li>哪份工作被反复做，保留什么历史才能不再重扫？</li>
              <li>哪批候选会在同一个事件后一起失效，为什么可以安全丢掉？</li>
              <li>同一个子问题会不会从多条路径重复到达，需要复用吗？</li>
            </ol>
          </section>

          <section class="bank-fact-section">
            <div class="bank-section-heading">
              <span>06</span>
              <div>
                <h2>交接 8：比较候选，确认算法方向</h2>
                <p>现在才允许具体方法名进入比较。候选必须能承担交接 7 的查询、插入、删除、取极值或恢复现场，并通过交接 6 的预算。</p>
              </div>
            </div>
            ${renderHandoffContract(HANDOFFS[7])}
            <ol class="bank-question-list">
              <li>这个候选消除了第二次变化里的哪份重复劳动或失效扫描？</li>
              <li>它需要哪些操作，时间和额外空间在当前范围里是否允许？</li>
              <li>有真实替代方向时，它在当前题目哪个条件下失效或代价过高？</li>
              <li>没有形成真实歧义时，我检查过的熟悉替代方向为什么不能承担当前操作？</li>
              <li>我能不能不报方法名，先用完整因果句说清“为什么必须是这类操作”？</li>
            </ol>
            ${
              solution
                ? `<div class="bank-solution-gate">
                    <strong>方向确认以后，再用正式文档校验</strong>
                    <p>先自己写出方向确认句，再打开现有题解。若还说不清“为什么需要这些操作”，先退回交接 7 或交接 6。</p>
                    <div class="bank-reading-links">
                      <a href="${docHref(solution.path, solution.reasoningAnchor)}"><i data-lucide="git-branch"></i>人的推导</a>
                      <a href="${docHref(solution.path, solution.answerAnchor)}"><i data-lucide="shield-check"></i>答案与不变量</a>
                      <a href="${docHref(solution.path, solution.codeAnchor)}"><i data-lucide="code-2"></i>Java 实现</a>
                    </div>
                  </div>`
                : `<p class="bank-muted">当前快照没有关联到本地标准题解。</p>`
            }
          </section>

          <section class="bank-fact-section">
            <div class="bank-section-heading">
              <span>07</span>
              <div>
                <h2>交接 9：状态、更新顺序、不变量、代码和反例</h2>
                <p>从这里开始只讨论实现。任何一项都必须能回到交接 3 的对象、交接 5 的第一次变化和交接 7 的第二次变化。</p>
              </div>
            </div>
            ${renderHandoffContract(HANDOFFS[8])}
            <ol class="bank-question-list">
              <li>每个状态在题目世界里代表什么，覆盖哪段对象，何时被读取和更新？</li>
              <li>初始值、停止条件和答案时机分别对应现实过程中的哪一刻？</li>
              <li>交换两个更新动作后，哪一个最小输入会产生错误结果？</li>
              <li>不变量为什么能证明不会漏、不会多、不会误删？</li>
              <li>每一段代码对应哪个对象、状态和动作，关闭资料后能否重建？</li>
            </ol>
            <details class="bank-code-gate">
              <summary>
                <span>
                  <strong>我已经完成方向确认，展开签名与 Java 模板</strong>
                  <small>如果还说不清主方向、所需操作和适用边界，先不要展开。</small>
                </span>
                <i data-lucide="chevron-down"></i>
              </summary>
              <div class="bank-code-body">
                <p>${escapeHtml(renderSignatureText(record.signature))}</p>
                <pre><code class="language-java">${escapeHtml(record.javaTemplate || "当前快照没有 Java 模板。")}</code></pre>
              </div>
            </details>
          </section>

          <details class="bank-official-hints">
            <summary>
              <span>
                <strong>查看平台提示（可能提前泄露思考方向）</strong>
                <small>${record.officialHints?.length || 0} 条官方提示，阅读前先写下自己的当前困惑。</small>
              </span>
              <i data-lucide="chevron-down"></i>
            </summary>
            <ol>
              ${
                record.officialHints?.length
                  ? record.officialHints.map((hint) => `<li>${sanitizeHtml(hint)}</li>`).join("")
                  : "<li>当前快照没有官方提示。</li>"
              }
            </ol>
          </details>
        </div>

        <aside class="bank-detail-aside">
          <section>
            <span class="bank-aside-label">事实源</span>
            <a href="${escapeAttribute(record.sourceUrl || "#")}" target="_blank" rel="noreferrer">
              打开 LeetCode 原题<i data-lucide="external-link"></i>
            </a>
            <dl class="bank-source-facts">
              <div><dt>核验日期</dt><dd>${escapeHtml(record.sourceCheckedAt || "未记录")}</dd></div>
              <div><dt>快照摘要</dt><dd><code>${escapeHtml(sourceSha)}</code></dd></div>
              <div><dt>主分类</dt><dd>${escapeHtml(record.primaryPattern || "未分类")}</dd></div>
            </dl>
          </section>
          <section>
            <span class="bank-aside-label">怎样区分</span>
            <p><strong>官方事实</strong>来自题面快照。</p>
            <p><strong>P0 与体系形态</strong>来自本地策展，不冒充平台评级或推荐解法。</p>
            <p><strong>Java 模板</strong>只是函数签名，不证明算法方向。</p>
          </section>
          <section>
            <span class="bank-aside-label">当前断点</span>
            <p>如果第二次变化还说不清，就把最早缺失的问题写在单题工作台，不要用打开题解替代推导。</p>
            <a href="${docHref("学习看板/单题复习工作台.md")}">记录本题断点<i data-lucide="arrow-right"></i></a>
          </section>
        </aside>
      </div>
    </section>
  `;
}

function renderSignatureText(signature) {
  if (!signature?.name) {
    return "当前快照没有结构化函数签名。";
  }
  const params = (signature.params || [])
    .map((param) => `${param.type || "unknown"} ${param.name || ""}`.trim())
    .join(", ");
  const returnType = signature.return?.type || "unknown";
  return `${signature.name}(${params}) -> ${returnType}`;
}

function sanitizeHtml(fragment) {
  if (!window.DOMPurify) {
    return "";
  }
  return DOMPurify.sanitize(fragment || "", {
    ADD_ATTR: ["target", "rel"],
  });
}

function stripHtmlText(fragment) {
  if (!fragment) {
    return "";
  }
  const documentFragment = new DOMParser().parseFromString(String(fragment), "text/html");
  return documentFragment.body?.textContent || "";
}

function renderBankError(error) {
  return `
    <div class="error-state">
      <i data-lucide="database-zap"></i>
      <h1>官方事实题库暂时无法读取</h1>
      <p>${escapeHtml(error.message)}</p>
      <p>请先运行 <code>python3 site/build.py</code>，确认生成了 <code>_site/assets/fact-bank.json</code>。</p>
      <a class="primary-button" href="#/">返回学习首页</a>
    </div>
  `;
}

function handleContentControls(event) {
  handleReviewControls(event);
  handleBankControls(event);
}

function handleBankControls(event) {
  const target = event.target;
  if (!(target instanceof HTMLInputElement || target instanceof HTMLSelectElement)) {
    return;
  }
  if (target.id === "bank-query") {
    state.bankQuery = target.value;
  } else if (target.id === "bank-group-filter") {
    state.bankGroup = target.value;
  } else if (target.id === "bank-difficulty-filter") {
    state.bankDifficulty = normalizeBankDifficulty(target.value);
  } else {
    return;
  }
  const results = document.querySelector("#bank-results");
  if (results) {
    results.innerHTML = renderBankResults();
    refreshIcons();
  }
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
  const target = document.getElementById(anchor) || document.getElementById(slugify(anchor));
  if (target) {
    target.scrollIntoView({ block: "start" });
    return;
  }
  const normalizedAnchor = normalizeText(anchor);
  const matchingHeading = Array.from(
    elements.content.querySelectorAll(".markdown-body h1, .markdown-body h2, .markdown-body h3, .markdown-body h4")
  ).find((heading) => {
    const copy = heading.cloneNode(true);
    copy.querySelector(".heading-anchor")?.remove();
    return normalizeText(copy.textContent) === normalizedAnchor;
  });
  matchingHeading?.scrollIntoView({ block: "start" });
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
        <a class="search-result ${index === state.activeSearchIndex ? "active" : ""}" href="${searchResultHref(doc)}" data-result-index="${index}">
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
    window.location.hash = searchResultHref(state.searchResults[state.activeSearchIndex]).slice(1);
    closeSearch();
  }
}

function searchResultHref(doc) {
  return doc.href || docHref(doc.path);
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

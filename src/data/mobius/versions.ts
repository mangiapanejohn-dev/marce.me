/**
 * The MØBIUS version log, rendered by `/mobius` and `/zh/mobius`.
 *
 * This is the file a new version appends to. The hub page has one URL for the
 * life of the project — versions multiply here, not in the address bar — so
 * shipping a slice means one entry below, plus (optionally) a post whose slug
 * goes in `post`. A row with no `post` still shows; it just doesn't link.
 */

export type MobiusVersion = {
  /** "V29", "ADR 0013" — printed verbatim in the left column. */
  v: string;
  /**
   * When the slice actually landed: the timestamp of its last commit in the MØBIUS repository,
   * with that commit's own UTC offset, verbatim.
   *
   * **Never `new Date()` and never the day you got round to writing the post.** Several versions
   * land on one day — 2026-09-04 carries five — so a date alone cannot order them, and a
   * publication date would record when it was written up rather than when it happened. The
   * command is `git log -1 --date=format:'%Y-%m-%dT%H:%M:%S%z' --format='%ad' <commit>`, and the
   * `/reup` skill runs it rather than asking anyone to remember.
   *
   * Rendered in `SITE.timezone`, so the reader sees one clock no matter where the commit was made.
   */
  at: string;
  /** The version's own title. Always a claim, never a topic. */
  claim: string;
  claimZh: string;
  /** Two sentences. What was found, not what was built. */
  blurb: string;
  blurbZh: string;
  /** Slug of the published post, if there is one. Rendered as a link to /posts/<slug>. */
  post?: string;
};

/**
 * The long-form pieces, which are about a span of the work rather than one version.
 *
 * They sit below the version log in the research feed rather than inside it: a row in the log is
 * one slice, and neither of these is. Titles and dates are read from the content collection at
 * render time — only the span label lives here, because only this file knows it.
 */
export type MobiusEssay = {
  /** Slug in `src/data/blog/`. */
  slug: string;
  span: string;
  spanZh: string;
};

export const essays: MobiusEssay[] = [
  {
    slug: "mobius-who-owns-the-runtime",
    span: "V19–V22",
    spanZh: "V19–V22",
  },
  {
    slug: "mobius-not-another-ai-wrapper",
    span: "Preface",
    spanZh: "开场",
  },
];

export const versions: MobiusVersion[] = [
  {
    v: "ADR 0013",
    at: "2026-09-02T14:24:18-04:00",
    claim: "A suspended run is a log position, not a paused process",
    claimZh: "挂起的 run 是日志里的一个位置，不是一个暂停的进程",
    blurb:
      "The decision eight slices rest on. Option B ends the run and lets a second run over the same journal answer the question, so only the durable log has to survive.",
    blurbZh:
      "后面八片都压在这个决定上。方案 B 让第一个 run 直接结束，由同一份 journal 上的第二个 run 来回答问题——需要活下来的只有那份持久日志。",
  },
  {
    v: "V24",
    at: "2026-09-02T14:25:04-04:00",
    claim: "mobiusd becomes a process a real client can connect to",
    claimZh: "mobiusd 成为一个真客户端能连上的进程",
    blurb:
      "Suspension recorded and resumed; the question becomes a server-to-client request; a Unix socket, hand-written RFC 6455 framing, and turn/start running a real loop. No build step, no new dependency.",
    blurbZh:
      "挂起被记录、被恢复；那个问题变成一次服务端到客户端的请求；一个 Unix socket、手写的 RFC 6455 分帧，以及跑真循环的 turn/start。没有构建步骤，没有新依赖。",
  },
  {
    v: "V25",
    at: "2026-09-02T14:25:22-04:00",
    claim: "A real TUI connects, and finds six defects",
    claimZh: "真 TUI 接上来，找出六个缺陷",
    blurb:
      "codex-cli 0.149.0 against a real daemon. Every earlier claim about this wire had been checked against clients we wrote ourselves — which is why the six existed.",
    blurbZh:
      "codex-cli 0.149.0 对上一个真的 daemon。此前关于这条线的每一条断言，都只对着我们自己写的客户端验证过——这正是那六个缺陷存在的原因。",
  },
  {
    v: "V26",
    at: "2026-09-02T14:26:54-04:00",
    claim: "A well-formed message must not kill the daemon",
    claimZh: "一条格式正确的消息不该杀死 daemon",
    blurb:
      "A duplicate response id ended the process. Also: five RFC 6455 violations accepted and one committed, and 1,098 leaked temp directories from a single session.",
    blurbZh:
      "一个重复的 response id 就能终结进程。同时还有：五处被接受的 RFC 6455 违规、一处自己犯的，以及单次会话泄漏的 1,098 个临时目录。",
  },
  {
    v: "V27",
    at: "2026-09-03T01:13:21-04:00",
    claim: "Acting is not grading",
    claimZh: "干活不是打分",
    blurb:
      "A chat prompt produced a run that asked a person to judge work it had never done. The goal says there is work; only the person says whether it succeeded.",
    blurbZh:
      "一个聊天提示产生的 run，会请人去判断它根本没做过的工作。目标说明有事要做；只有人能说它是否成功。",
  },
  {
    v: "V28",
    at: "2026-09-03T11:28:33-04:00",
    claim: "The run says why it stopped",
    claimZh: "run 要说清自己为什么停了",
    blurb:
      'Three facts stopped sharing one undefined. The prompt\'s own escape hatch — {"satisfies": []} — had been refused as malformed, so a model doing exactly as instructed killed the run.',
    blurbZh:
      '三个事实不再共用同一个 undefined。提示词自己给出的退出口——{"satisfies": []}——一直被当作格式错误拒绝，于是一个完全照指令行事的模型反而杀死了这个 run。',
  },
  {
    v: "V29",
    at: "2026-09-03T11:44:45-04:00",
    claim: "Work already carried out is not work",
    claimZh: "已经做过的事不算事",
    blurb:
      "A model that kept proposing one effect, and a person who approved it once, wrote the same file eight times. Nothing in the runtime decided to stop; a constant in the model port did.",
    blurbZh:
      "一个反复提议同一个副作用的模型，加上一个只批准过一次的人，把同一个文件写了八遍。运行时里没有任何东西决定停下来——决定停下来的是模型端口里的一个常量。",
  },
  {
    v: "V30",
    at: "2026-09-04T10:38:14-04:00",
    claim: "Boundaries: the ledger, and being told to stop",
    claimZh: "边界：账本，以及被叫停",
    blurb:
      "Spend survives a re-entry because the projection counts it; --max-actions reaches a chat goal; turn/interrupt lands; and a dropped connection stops its turn instead of pulling the world away.",
    blurbZh:
      "花销能跨越重新进入，因为投影会把它数进去；--max-actions 能到达聊天目标；turn/interrupt 落地；断线会让它的 turn 停下来，而不是把整个世界从底下抽走。",
  },
  {
    v: "V31",
    at: "2026-09-04T10:53:38-04:00",
    claim: "The rule I got wrong, measured with the thing it was about",
    claimZh: "我搞错的那条规则，用它所描述的东西量了一遍",
    blurb:
      "Nothing in packages/ changed. An instrument, five assertions, one vocabulary entry — and a thirty-line Rust program checked in so the next reader can re-run it instead of trusting this one.",
    blurbZh:
      "packages/ 里一行没动。一个量具、五条断言、一个词条——外加一个三十行的 Rust 程序提交进仓库，好让下一个读者去重跑，而不是相信我。",
  },
  {
    v: "V32",
    at: "2026-09-04T11:14:25-04:00",
    claim: "When the runtime is breaking a tie, it says so",
    claimZh: "运行时在打破平局时，会说出来",
    blurb:
      "Measuring what is actually exposed changed what there was to do: the harm was already caught twice over, and the gap was that an approval never said the score was a coin-flip. It carries the margin now.",
    blurbZh:
      "去量真正暴露出来的东西，改变了该做的事：伤害早已被挡下两道，缺口只是一次批准从没说过那个分数其实是掷硬币。现在它带上了差值。",
  },
  {
    v: "V33",
    at: "2026-09-04T11:47:12-04:00",
    claim: "A signal takes the same release a dropped socket does",
    claimZh: "一个信号走的是断掉的 socket 走的那条释放路径",
    blurb:
      "SIGTERM mid-pass left a journal ending at goal.created — a run that began and recorded no ending, with exit code 0. Two shutdown paths, and only one of them was polite.",
    blurbZh:
      "在一趟中途 SIGTERM，留下一份停在 goal.created 的 journal——一个开了头却没有记录任何结尾的 run，退出码还是 0。两条关停路径，只有一条是有礼貌的。",
  },
  {
    v: "V34",
    at: "2026-09-04T13:22:28-04:00",
    claim: "A session that was let go is not a session that never was",
    claimZh: "被放走的会话，不等于从未存在过的会话",
    blurb:
      'One branch answered two questions. An invented id really is an invariant being violated; a released world stopped nothing, and now says so: "nothing refused it."',
    blurbZh:
      '一个分支回答了两个问题。一个凭空捏造的 id 确实是不变量被破坏；而一个已释放的世界什么都没拦——现在它这么说了："没有东西拒绝它。"',
  },
  {
    v: "V35",
    // Landed, and this is now the commit's own timestamp as the rule requires. The four rows V35
    // through V38 carry the *same* one because they landed in the same commit: their production
    // code shares one file that each of the four rewrote, so no sequence of commits exists that
    // means "V35 landed, then V36 landed". Giving them distinct times would be inventing an
    // ordering the repository does not have. Array order carries the sequence instead.
    at: "2026-09-05T14:19:03-04:00",
    claim: "A proposal is a prediction, and the log can already grade it",
    claimZh: "提案本身就是预测，而日志早就能给它打分",
    blurb:
      "Every dispatch was described before it happened and verified after, and nothing had ever read the two as a pair. So this version built the scorer rather than another forecaster — and the kill condition it registered first, that a real proposer might only ever be right, did not hold.",
    blurbZh:
      "每一次派发事前都被描述过、事后都被验证过，而从来没有东西把这两半当作一对来读。所以这一版造的是打分器，不是又一个预测器——而它事先登记的那条死刑条件（真实提议者会不会永远只说对），没有成立。",
    post: "mobius-v35-a-proposal-is-a-prediction",
  },
  {
    v: "V36",
    at: "2026-09-05T14:19:03-04:00",
    claim: "A world that moved is not a wrong forecast",
    claimZh: "世界动了，不等于预测错了",
    blurb:
      "A verdict read from a world the action did not produce charges the proposer for the weather, so drift became a third resolution beside graded and ungraded. Then its own first cut failed: the write counter it trusted is bumped inside the provider's write path, and is blind to anyone who edits the file directly.",
    blurbZh:
      "一个从「并非该动作造出来的世界」里读出的裁决，等于把天气算在提议者头上，所以 drift 成了 graded 和 ungraded 之外的第三种判定。然后它自己的第一版就挂了：它信任的那个写计数器是在 provider 自己的写路径里递增的，对任何直接改文件的人都是瞎的。",
    post: "mobius-v36-v38-a-forecast-is-about-a-world",
  },
  {
    v: "V37",
    at: "2026-09-05T14:19:03-04:00",
    claim: "Drift is a resource changing identity, not a counter moving",
    claimZh: "drift 是资源的内容标识变了，不是某个计数器动了",
    blurb:
      "The counter failed in both directions at once — blind to a writer who bypasses the provider, and over-broad about a file the assertions never read. V36's own P3 stands refuted in place, because rewriting it would remove the only trace that a rule was wrong in a way its own battery could not see.",
    blurbZh:
      "那个计数器同时错在两个方向——对绕过 provider 的写入是瞎的，对一个断言从没读过的文件又过宽。V36 自己的 P3 以「被推翻」的状态原样留着，因为改写它就等于抹掉「一条规则曾经错在它自己的 battery 看不见的地方」的唯一痕迹。",
    post: "mobius-v36-v38-a-forecast-is-about-a-world",
  },
  {
    v: "V38",
    at: "2026-09-05T14:19:03-04:00",
    claim: "The world a prediction was made in was bindable all along",
    claimZh: "一次预测所处的世界，一直都是可绑定的",
    blurb:
      "V36 concluded the pre-action world was unavailable, from a fixture with one action in it — and its pin ran on a stub that discards the grounding input, so it held whatever the loop did. The observation that verifies one action is the grounding stamped on the next, and has been since V21-2.",
    blurbZh:
      "V36 断定动作之前的世界不可用，而那是从一个只有一个动作的 fixture 里推广出来的——并且它的 pin 跑在一个丢掉 grounding 输入的 stub 上，所以不管 loop 做什么它都成立。验证一个动作的那次观测，正是盖在下一个动作上的 grounding，从 V21-2 起就是。",
    post: "mobius-v36-v38-a-forecast-is-about-a-world",
  },
  {
    v: "V39",
    at: "2026-09-05T14:19:16-04:00",
    claim: "The prior value was in the journal the whole time",
    claimZh: "前值一直就在 journal 里",
    blurb:
      "The plane escalates to a fresh observation because a changed assertion has no prior value — and then the observation cannot decide it either, measured with a perfect look. The baseline input had been accepted and unsupplied since the plane was written; the action already named an observation taken before it ran.",
    blurbZh:
      "平面之所以升级去取一次新观测，是因为 changed 断言没有前值——然后那次观测同样裁决不了它，这是用一次完美的 look 测出来的。baseline 这个输入从平面写成那天起就被接受着、从来没人供给过；而动作本身早就指名了一次在它之前取的观测。",
    post: "mobius-v39-the-prior-value-was-in-the-journal",
  },
  {
    v: "V40",
    at: "2026-09-05T14:19:30-04:00",
    claim: "A battery cannot refute what it does not run",
    claimZh: "battery 无法推翻它没有跑过的东西",
    blurb:
      "The change passed all four of its predictions and a five-mutation battery with nothing surviving, and was still wrong: the full suite found it restoring work on an off-target look. Reverted. A battery measures the tests you hand it, and all six of those had been chosen from what the version was about.",
    blurbZh:
      "这个改动通过了它全部四条预测、通过了五条 mutation 的 battery 且零存活，而它依然是错的：全套件发现它会在一次跑偏的 look 上恢复工作。已回滚。battery 衡量的是你交给它的那些测试，而那六个文件全都是按「这一版讲什么」挑的。",
    post: "mobius-v40-a-battery-cannot-refute-what-it-does-not-run",
  },
  {
    v: "V41",
    at: "2026-09-05T15:14:04-04:00",
    claim: "Why the runtime never looks before it acts",
    claimZh: "为什么 runtime 从不在动作之前先看一眼",
    blurb:
      "The one mechanism that would make it look first never produces a usable look, for three independent reasons — and this version fixed none of them. Repairing the routing alone turns a failure that costs nothing into one that costs 31 charged observations.",
    blurbZh:
      "那个唯一能让它先看一眼的机制，因为三个独立原因从来产不出一次可用的 look——而这一版一个都没修。只修路由，会把一个不花钱的失败换成一个要花 31 次计费观测的失败。",
    post: "mobius-v41-v45-why-it-never-looked-first",
  },
  {
    v: "V42",
    at: "2026-09-05T15:45:14-04:00",
    claim: "Only one of the two meanings is ever promised",
    claimZh: "两个含义里，只有一个被承诺出去",
    blurb:
      "A field meant the precondition's subject where it was written and criterion ids where it was read. Emptying it at the writer broke a reader that depended on it — filing evidence under the subject is the mechanism, not the mislabel. The fix is at the boundary that makes a promise.",
    blurbZh:
      "一个字段在写它的地方指前置条件的 subject，在读它的地方指 criterion id。在写入方清空它，打断了一个依赖它的读取方——把证据归档到 subject 下不是标错，那就是机制。修在真正做出承诺的那个边界上。",
    post: "mobius-v41-v45-why-it-never-looked-first",
  },
  {
    v: "V43",
    at: "2026-09-05T16:12:24-04:00",
    claim: "A resolution the look did not produce is not recorded",
    claimZh: "一次 look 没产出的「解决」，不该被记录",
    blurb:
      "One question was marked answered 31 times by looks that came back carrying nothing, and the runtime's own projection already disbelieved every one of them. They were not claims anything acted on; they were false records.",
    blurbZh:
      "一个问题被 31 次什么都没带回来的 look 标记为「已回答」，而 runtime 自己的投影早就一个都不信。它们不是被采信的声明，是假记录。",
    post: "mobius-v41-v45-why-it-never-looked-first",
  },
  {
    v: "V44",
    at: "2026-09-05T16:50:53-04:00",
    claim: "A question already asked of the world is not still open",
    claimZh: "已经问过世界的问题，不算还开着",
    blurb:
      "The stop, the reason and the filter were all already there. What was missing was one fact — this unknown has been asked — and the two places that had to read it. A test that had been green for years turned out to be passing on the defect.",
    blurbZh:
      "停止状态、理由、过滤器全都早就在。缺的是一个事实——这个 unknown 已经问过了——和两个必须读它的地方。一个绿了很多年的测试，原来一直靠着这个缺陷才通过。",
    post: "mobius-v41-v45-why-it-never-looked-first",
  },
  {
    v: "V45",
    at: "2026-09-06T04:31:39-04:00",
    claim: "The runtime knows what the look is for, and now says so",
    claimZh: "runtime 知道这次 look 是为了什么，现在它说出来了",
    blurb:
      "The reflex could always have routed the look; the runtime could not say what the look was for. The proposer had a slot channel and the runtime had none — so whether it was allowed to look at a file it could see was decided by the wording of a sentence written for a human.",
    blurbZh:
      "reflex 一直都能路由这次 look；说不出「这次 look 是为了什么」的是 runtime。提议者有 slot 通道而 runtime 没有——于是它能不能去看一个它看得见的文件，由一句写给人看的话的措辞决定。",
    post: "mobius-v41-v45-why-it-never-looked-first",
  },
  {
    v: "V46",
    at: "2026-09-06T05:01:46-04:00",
    claim: "An action's premise is what it said it rested on",
    claimZh: "一个动作的 premise，是它自己说过依赖什么",
    blurb:
      "A field existed for exactly the missing scope and every provider wrote []. The obvious way to fill it reproduces the scope already rejected — the grounding observation is the premise. The declaration was in the action's own preconditions all along.",
    blurbZh:
      "缺的那个作用域恰好有一个字段，而每个 provider 都写 []。显而易见的填法重现的正是早已被否决的作用域——grounding 观测就是 premise。声明一直在动作自己的前置条件里。",
    post: "mobius-v46-the-premise-is-what-it-declared",
  },
  {
    v: "V47",
    at: "2026-09-06T05:50:48-04:00",
    claim: "Two witnesses and one interpretation",
    claimZh: "两个证人，一种解释",
    blurb:
      "Four evidence refs, two roots — the verdict's observed ref is the receipt's, carried forward. The one path with two independent reads finds them disagreeing at the same world revision, and the runtime has exactly one reading of that. H5 is located, not closed.",
    blurbZh:
      "四条证据 ref，两个根——裁决里那条 observed ref 就是 receipt 那一条带下来的。唯一有两次独立读取的路径，发现它们在同一个世界版本上互相矛盾，而 runtime 对此只有一种读法。H5 是被定位了，不是被关闭了。",
    post: "mobius-v47-two-witnesses-one-interpretation",
  },
  {
    v: "V48",
    at: "2026-09-06T08:58:09-04:00",
    claim: "A second reader exists, and its blind spots are disjoint",
    claimZh: "第二个读取者是存在的，而且它们的盲区互不重叠",
    blurb:
      "The repository reports that a path changed, never to what — so the obvious per-path corroboration does not exist. What does: a content token and a status token whose blind spots are disjoint, and a filesystem digest that agrees with one of them about one file. H5 moves from unreachable to reachable and possibly not worth reaching.",
    blurbZh:
      "仓库只报一个路径变了，从不报变成了什么——所以显而易见的逐路径互证并不存在。存在的是：一个内容 token 和一个状态 token，盲区互不重叠，以及一个在某一个文件上与其中之一达成一致的文件系统摘要。H5 从够不着，变成了够得着、而且可能不值得去够。",
    post: "mobius-v48-a-second-reader",
  },
];

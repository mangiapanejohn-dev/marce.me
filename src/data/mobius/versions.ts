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
  /** The version's own title. Always a claim, never a topic. */
  claim: string;
  claimZh: string;
  /** Two sentences. What was found, not what was built. */
  blurb: string;
  blurbZh: string;
  /** Slug of the published post, if there is one. Rendered as a link to /posts/<slug>. */
  post?: string;
};

export const versions: MobiusVersion[] = [
  {
    v: "ADR 0013",
    claim: "A suspended run is a log position, not a paused process",
    claimZh: "挂起的 run 是日志里的一个位置，不是一个暂停的进程",
    blurb:
      "The decision eight slices rest on. Option B ends the run and lets a second run over the same journal answer the question, so only the durable log has to survive.",
    blurbZh:
      "后面八片都压在这个决定上。方案 B 让第一个 run 直接结束，由同一份 journal 上的第二个 run 来回答问题——需要活下来的只有那份持久日志。",
  },
  {
    v: "V24",
    claim: "mobiusd becomes a process a real client can connect to",
    claimZh: "mobiusd 成为一个真客户端能连上的进程",
    blurb:
      "Suspension recorded and resumed; the question becomes a server-to-client request; a Unix socket, hand-written RFC 6455 framing, and turn/start running a real loop. No build step, no new dependency.",
    blurbZh:
      "挂起被记录、被恢复；那个问题变成一次服务端到客户端的请求；一个 Unix socket、手写的 RFC 6455 分帧，以及跑真循环的 turn/start。没有构建步骤，没有新依赖。",
  },
  {
    v: "V25",
    claim: "A real TUI connects, and finds six defects",
    claimZh: "真 TUI 接上来，找出六个缺陷",
    blurb:
      "codex-cli 0.149.0 against a real daemon. Every earlier claim about this wire had been checked against clients we wrote ourselves — which is why the six existed.",
    blurbZh:
      "codex-cli 0.149.0 对上一个真的 daemon。此前关于这条线的每一条断言，都只对着我们自己写的客户端验证过——这正是那六个缺陷存在的原因。",
  },
  {
    v: "V26",
    claim: "A well-formed message must not kill the daemon",
    claimZh: "一条格式正确的消息不该杀死 daemon",
    blurb:
      "A duplicate response id ended the process. Also: five RFC 6455 violations accepted and one committed, and 1,098 leaked temp directories from a single session.",
    blurbZh:
      "一个重复的 response id 就能终结进程。同时还有：五处被接受的 RFC 6455 违规、一处自己犯的，以及单次会话泄漏的 1,098 个临时目录。",
  },
  {
    v: "V27",
    claim: "Acting is not grading",
    claimZh: "干活不是打分",
    blurb:
      "A chat prompt produced a run that asked a person to judge work it had never done. The goal says there is work; only the person says whether it succeeded.",
    blurbZh:
      "一个聊天提示产生的 run，会请人去判断它根本没做过的工作。目标说明有事要做；只有人能说它是否成功。",
  },
  {
    v: "V28",
    claim: "The run says why it stopped",
    claimZh: "run 要说清自己为什么停了",
    blurb:
      'Three facts stopped sharing one undefined. The prompt\'s own escape hatch — {"satisfies": []} — had been refused as malformed, so a model doing exactly as instructed killed the run.',
    blurbZh:
      '三个事实不再共用同一个 undefined。提示词自己给出的退出口——{"satisfies": []}——一直被当作格式错误拒绝，于是一个完全照指令行事的模型反而杀死了这个 run。',
  },
  {
    v: "V29",
    claim: "Work already carried out is not work",
    claimZh: "已经做过的事不算事",
    blurb:
      "A model that kept proposing one effect, and a person who approved it once, wrote the same file eight times. Nothing in the runtime decided to stop; a constant in the model port did.",
    blurbZh:
      "一个反复提议同一个副作用的模型，加上一个只批准过一次的人，把同一个文件写了八遍。运行时里没有任何东西决定停下来——决定停下来的是模型端口里的一个常量。",
  },
  {
    v: "V30",
    claim: "Boundaries: the ledger, and being told to stop",
    claimZh: "边界：账本，以及被叫停",
    blurb:
      "Spend survives a re-entry because the projection counts it; --max-actions reaches a chat goal; turn/interrupt lands; and a dropped connection stops its turn instead of pulling the world away.",
    blurbZh:
      "花销能跨越重新进入，因为投影会把它数进去；--max-actions 能到达聊天目标；turn/interrupt 落地；断线会让它的 turn 停下来，而不是把整个世界从底下抽走。",
  },
  {
    v: "V31",
    claim: "The rule I got wrong, measured with the thing it was about",
    claimZh: "我搞错的那条规则，用它所描述的东西量了一遍",
    blurb:
      "Nothing in packages/ changed. An instrument, five assertions, one vocabulary entry — and a thirty-line Rust program checked in so the next reader can re-run it instead of trusting this one.",
    blurbZh:
      "packages/ 里一行没动。一个量具、五条断言、一个词条——外加一个三十行的 Rust 程序提交进仓库，好让下一个读者去重跑，而不是相信我。",
  },
  {
    v: "V32",
    claim: "When the runtime is breaking a tie, it says so",
    claimZh: "运行时在打破平局时，会说出来",
    blurb:
      "Measuring what is actually exposed changed what there was to do: the harm was already caught twice over, and the gap was that an approval never said the score was a coin-flip. It carries the margin now.",
    blurbZh:
      "去量真正暴露出来的东西，改变了该做的事：伤害早已被挡下两道，缺口只是一次批准从没说过那个分数其实是掷硬币。现在它带上了差值。",
  },
  {
    v: "V33",
    claim: "A signal takes the same release a dropped socket does",
    claimZh: "一个信号走的是断掉的 socket 走的那条释放路径",
    blurb:
      "SIGTERM mid-pass left a journal ending at goal.created — a run that began and recorded no ending, with exit code 0. Two shutdown paths, and only one of them was polite.",
    blurbZh:
      "在一趟中途 SIGTERM，留下一份停在 goal.created 的 journal——一个开了头却没有记录任何结尾的 run，退出码还是 0。两条关停路径，只有一条是有礼貌的。",
  },
  {
    v: "V34",
    claim: "A session that was let go is not a session that never was",
    claimZh: "被放走的会话，不等于从未存在过的会话",
    blurb:
      'One branch answered two questions. An invented id really is an invariant being violated; a released world stopped nothing, and now says so: "nothing refused it."',
    blurbZh:
      '一个分支回答了两个问题。一个凭空捏造的 id 确实是不变量被破坏；而一个已释放的世界什么都没拦——现在它这么说了："没有东西拒绝它。"',
  },
];

/**
 * The MØBIUS papers and formal notes, rendered by `<ResearchFeed />` on `/research` and the
 * homepage's research tab.
 *
 * Every entry is a **document, with a status** — not a publication list. Two of these are drafts
 * whose central novelty framing has since been narrowed by the project's own prior-art work, and
 * one records a research direction that was retired. That is the whole reason the `status` field
 * exists and is printed beside the title rather than buried in the PDF: a paper on this site is a
 * dated record of what was believed and measured, and the reader is told immediately where it
 * stands today.
 *
 * Newest first. Files live in `public/research/papers/` (the FTR note predates the folder and stays
 * at its published path, because its URL is already linked from a post).
 */

export type MobiusPaper = {
  /** Printed as the card's title. */
  title: string;
  /** The subtitle line from the paper itself, when it has one. */
  subtitle?: string;
  /** Public path of the PDF. */
  href: string;
  /** ISO day the build is dated. */
  at: string;
  pages: number;
  /**
   * Where the document stands today, in three words or so, plus the tone class it is printed in.
   * `kind` maps to the `.st-*` classes in global.css.
   */
  status: string;
  kind: "measured" | "open" | "retired" | "killed" | "ne" | "prior";
  /** Two or three sentences: what it argues, and what it is for. */
  blurb: string;
  blurbZh: string;
  /** What has changed since it was written. Printed in smaller type under the blurb. */
  since?: string;
  sinceZh?: string;
};

export const papers: MobiusPaper[] = [
  {
    title: "FTR — Core Formalization",
    subtitle: "Future trajectory representation for autonomous-agent runtimes",
    href: "/research/FTR_Core_Formalization_2026-09-19.pdf",
    at: "2026-09-19",
    pages: 12,
    status: "Retired direction · record",
    kind: "killed",
    blurb:
      "The full formalization FTR ended with: possible futures, disagreement, future information requirements, proof obligations, risk, resolution and calibration. It is kept as the record of what was formalized and why it did not survive.",
    blurbZh:
      "FTR 最终的完整形式化：可能未来、分歧度、未来信息需求、证明义务、风险、结算与校准。作为「它被形式化成什么、又为什么没能活下来」的记录保留。",
    since:
      "Every sub-claim failed the threshold written for it, reduced to prior art, or proved not evaluable. The one question that outlives it — which facts must be kept before an action — is marked open inside.",
    sinceZh:
      "每一条子主张要么没过自己写下的判据，要么归约为先验工作，要么根本无法评估。唯一活下来的问题——动作之前必须保留哪些事实——在文中标为 open。",
  },
  {
    title: "Premise-Bound Execution",
    subtitle: "Approval Validity under Mutable World State in an Agent Runtime",
    href: "/research/papers/mobius-premise-bound-execution-2026-09-15.pdf",
    at: "2026-09-15",
    pages: 47,
    status: "Draft · partly superseded",
    kind: "retired",
    blurb:
      "The long-form record of the approval line: 272 arms across one run, a run boundary and a resume; a human approval that authorises an effect after the world that justified it has changed, with every gate on the path locally correct; and the model that explains it — an approval is a memoized decision whose validity key is the state it was about.",
    blurbZh:
      "审批线的长篇记录：跨越一次运行、一次运行边界与一次 resume 的 272 个实验臂；一个在「为它辩护的世界已经改变」之后仍然放行效果的人类批准，而路径上每道门各自都是对的；以及解释它的模型——批准是一次被记忆化的决定，其有效性键是它所针对的那个世界状态。",
    since:
      "The measurements stand. The novelty framing does not: after 15 September the same design family turned up published — commit-time authorization, dependency-scoped validation, automatic read-set reconstruction. Read it as measurement and model, not as a claim of being first.",
    sinceZh:
      "测量本身成立，「新颖性」的表述不成立：9 月 15 日之后发现同一设计族已有发表工作——提交时授权、依赖域校验、读集自动重建。请把它当作测量与模型来读，而不是「首创」主张。",
  },
  {
    title: "Approvals as Memoized Decisions",
    subtitle: "Validity under Mutable World State in an Agent Runtime",
    href: "/research/papers/mobius-approvals-as-memoized-decisions-2026-09-15.pdf",
    at: "2026-09-15",
    pages: 22,
    status: "Conference draft · not submitted",
    kind: "ne",
    blurb:
      "The short version of the same work, written to a conference page budget and built anonymously for review. Targeted at USENIX OSDI ’27 and never submitted: the project's own readiness audit returned a conditional no-go, and the literature has since removed the mechanism contribution it rested on.",
    blurbZh:
      "同一份工作的短版本，按会议页数写成，并以匿名方式构建以备评审。原本瞄准 USENIX OSDI ’27，从未投出：项目自己的就绪性审计给出有条件的 NO-GO，而此后的文献又拿走了它所依赖的机制贡献。",
    since: "Kept because a draft that was not sent is still part of the record of what was believed in September 2026.",
    sinceZh: "保留它，是因为一份没有寄出的草稿，同样是 2026 年 9 月「当时相信什么」的记录的一部分。",
  },
];

#!/usr/bin/env node
/**
 * FTR Core Formalization, 2026-09-19 — the PDF linked from
 * src/data/blog/mobius-a-correct-world-is-not-a-proven-one.md.
 *
 * No LaTeX toolchain on the machine that built it, so: HTML with KaTeX rendered at build time, printed to A4 by
 * headless Chrome. Figures are the post's own light SVGs; the closing page carries the author's existing
 * signature image (the one his email templates already use), unmodified.
 *
 *   node scripts/research/ftr-formalization.mjs
 *     → public/research/FTR_Core_Formalization_2026-09-19.pdf
 *
 * Env: CHROME (path to a Chrome binary), SIGNATURE (path to the signature PNG).
 */
import katex from "katex";
import { execFileSync } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..", "..");
const out = path.join(root, "public", "research", "FTR_Core_Formalization_2026-09-19.pdf");
const chrome = process.env.CHROME ?? "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const signature =
  process.env.SIGNATURE ?? path.join(os.homedir(), "Developer/main/shcool-it/apps/web/public/assets/marc-ellington-signature-transparent.png");
const katexCss = pathToFileURL(path.join(root, "node_modules/katex/dist/katex.min.css")).href;
const fig = name => pathToFileURL(path.join(root, "public/research", `${name}.svg`)).href;

if (!fs.existsSync(signature)) throw new Error(`signature asset not found: ${signature} — refusing to build without it`);

const M = tex => katex.renderToString(tex, { displayMode: true, throwOnError: true, strict: "ignore" });
const m = tex => katex.renderToString(tex, { displayMode: false, throwOnError: true, strict: "ignore" });
/** Inline math in prose: \( … \). */
const t = s => s.replace(/\\\((.+?)\\\)/g, (_, x) => m(x));

const tag = (k, label) => `<span class="st st-${k}">${label}</span>`;
const OPEN = tag("open", "OPEN"), KILLED = tag("killed", "KILLED"), RETIRED = tag("retired", "RETIRED"),
  PRIOR = tag("prior", "PRIOR ART"), MEAS = tag("measured", "MEASURED"), NE = tag("ne", "NOT EVALUABLE"),
  CAND = tag("retired", "CANDIDATE"), UNS = tag("killed", "UNSUPPORTED");

const R = String.raw;

const body = String.raw`
<section class="cover">
  <div class="kicker">MØBIUS research note · working specification</div>
  <h1>FTR</h1>
  <div class="subtitle">Core Formalization</div>
  <div class="subsub">Future trajectory representation for autonomous-agent runtimes:<br/>possible futures, disagreement, future information requirements, proof obligations, risk, resolution and calibration.</div>
  <div class="coverformula">${M(R`\mathcal{F}_t=\big(P_t(\tau),\ D_t,\ \mathcal{H}_t,\ \Omega_t^{*},\ P_t^{\mathrm{proof}},\ R_t,\ \Gamma_t\big)`)}</div>
  <div class="warn">
    <strong>Status.</strong> FTR is <strong>not a validated theory</strong>. Everything here marked ${OPEN} is a hypothesis or a
    candidate formalization; nothing in this document is implemented as FTR in MØBIUS, and no FTR experiment has yet produced a result.
    Known abstractions — probabilistic forecasting, runtime verification, provenance, value of information — are not relabelled here as
    FTR novelty.
  </div>
  <table class="meta">
    <tr><td>Version</td><td>2026-09-19 · supersedes the undated working specification</td></tr>
    <tr><td>Evidence base</td><td>MØBIUS repository at <code>61f7100</code> (R3 handoff), evidence directories <code>r1/f9b27dd</code>, <code>r2/f9b27dd</code>, <code>p4-expectations/ba4f291</code>; research-lead records of 18–19 Sep 2026</td></tr>
    <tr><td>Companion post</td><td>marcyy.me/posts/mobius-a-correct-world-is-not-a-proven-one</td></tr>
    <tr><td>Author</td><td>Marc Ellington · MØBIUS Research</td></tr>
  </table>
</section>

<h2>0 · What changed in this version</h2>
<ul>
  <li><strong>Evidence horizon, corrected.</strong> The previous version implied information that becomes <em>unrecoverable</em> after an action. In every R3 P3 journal with a transition-shaped criterion, the pre-state <em>was</em> captured before the first effect; it was absent from the judge's <em>view</em>, not from the journal. The unrecoverable variant has not been observed and is kept as a hypothesis (§6).</li>
  <li><strong>Transition witness, downgraded.</strong> Retired as a new primitive (before-image + provenance edge + past-time operator). Kept as a candidate <em>representation</em> (§7).</li>
  <li><strong>Measured additions.</strong> Hand-coded cause of all 74 <code>cannot-tell</code> verdicts; a manual audit of all 20 <code>established</code> verdicts (one unsupported); certificate closure measured at 0 of 11 (§12).</li>
  <li><strong>Vacuity made explicit.</strong> R3 P3's "0 false completions" had zero opportunities to fail (39/39 rows passed their checker) and is recorded as not evaluable (§15).</li>
  <li><strong>Write-set anticipation.</strong> Stated precisely: a kill threshold fixed before the computation, on an experiment-arm corpus, not a workload (§15).</li>
</ul>

<h2>1 · Motivation — what the evidence points at</h2>
<p>MØBIUS's completion plane was the place its questions moved in September 2026. A separate model call (the <em>judge</em>, ADR 0043) decides whether a criterion no assertion checks is <code>established</code>, <code>not-established</code> or <code>cannot-tell</code>, from the observations it is shown (ADR 0045: the binding's evidence plus the run's latest non-stale observation of each other resource). In R3 P3 (<code>claude-opus-5</code>, three repetitions, 39 valid rows) the judge ruled 114 times: 20 / 20 / 74.</p>
<table class="data">
  <tr><th>what a <code>cannot-tell</code> reason says is missing</th><th>n</th></tr>
  <tr><td>prior state only</td><td>40</td></tr>
  <tr><td>prior state and an unread current resource</td><td>5</td></tr>
  <tr><td>an unread current resource only</td><td>28</td></tr>
  <tr><td>judge call timed out</td><td>1</td></tr>
</table>
<p>The 45 reasons that cite a missing past sit in three unrelated task shapes — rename (10/10), edit-to-spec with "nothing else changed" (20/22), split a document (15/27) — and in none of the other three tasks (0/15). Their criteria are predicates over a <em>transition</em>, not a state:</p>
${M(R`C \neq f(W_{\mathrm{post}}), \qquad C = f(W_{\mathrm{pre}},\, A,\, W_{\mathrm{post}})`)}
<p>FTR's surviving question follows from this: <strong>can a runtime know, before it acts, what a future decision or a future proof will need it to have kept?</strong></p>

<h2>2 · Runtime state and history</h2>
${M(R`X_t = \big(W_t,\ H_t,\ G_t,\ M_t,\ C_t,\ E_t,\ \Gamma_t\big)`)}
${M(R`H_t = \big(O_0,\ A_0,\ E_1,\ O_1,\ A_1,\ E_2,\ \ldots,\ A_{t-1},\ E_t,\ O_t\big)`)}
<p>History is not state. A current state is a function of history, and not an injective one:</p>
${M(R`H_t \not\equiv W_t, \qquad W_t(h_i) = W_t(h_j) \;\not\Rightarrow\; h_i = h_j`)}
<p>This matters whenever a criterion concerns preservation, movement, non-modification, provenance or causality — any past-to-present relation.</p>

<h2>3 · Possible futures as the object</h2>
${M(R`\tau_{t:t+k} = \big(S_t,\ A_t,\ E_{t+1},\ O_{t+1},\ S_{t+1},\ \ldots,\ A_{t+k-1},\ E_{t+k},\ O_{t+k},\ S_{t+k}\big)`)}
${M(R`P_t(\tau) = P_\theta\big(\tau_{t:t+k} \mid H_t,\ W_t,\ G_t,\ C_t,\ M_t\big), \qquad \mathcal{T}_t = \{(\tau_i,\ p_i)\}_{i=1}^{N},\ \ p_i \ge 0,\ \ \sum_{i=1}^{N} p_i = 1`)}
<p>The target is a distribution over structured trajectories — actions, effects, observations, failures, retries, human intervention, evidence capture, verification, completion — and never "the next action".</p>

<h2>4 · FTR is not a plan</h2>
${M(R`\mathcal{F}_t \neq \mathit{Plan}_t, \qquad P(\tau \mid X_t,\ \mathit{Plan}_t) \neq \mathbf{1}[\tau = \mathit{Plan}_t]`)}
<p>A plan is prescriptive: <em>what do I intend to do?</em> FTR is anticipatory: <em>which futures remain reachable from here, where do they diverge, what will they require, and what should the runtime preserve or inspect now because of that?</em> It must admit futures in which the plan fails, branches, stalls on a person, loses its evidence or is replaced. <strong>Kill condition:</strong> an FTR implementation that reduces to the planner under another name.</p>

<h2>5 · Future disagreement and uncertainty</h2>
<p>Let \(z \in Z\) be equivalence classes of materially distinct outcomes or trajectory shapes.</p>
${M(R`D_t = 1 - \sum_{z \in Z} P(z \mid X_t)^2, \qquad \mathcal{H}_t = -\sum_{i=1}^{N} p_i \log p_i`)}
<p>\(D_t\) is the Gini–Simpson index over outcome classes: \(D_t \approx 0\) when rollouts agree, \(D_t \to 1\) when they scatter. It does not require knowing which future is correct. ${PRIOR} Sample disagreement as an uncertainty estimate: self-consistency (Wang et al., ICLR 2023), semantic entropy over equivalence classes (Kuhn, Gal, Farquhar, ICLR 2023), conformal ask-for-help sets (Ren et al., CoRL 2023). ${OPEN} Whether divergence is a useful <em>runtime trigger</em> — for observation, preservation, a question to a person, or delaying an irreversible effect.</p>

<h2>6 · Future information requirements and proof obligations</h2>
<p>Let \(E_\Omega(h)\) be the evidence history \(h\) exposes when the fact set \(\Omega\) is captured, and \(C(h) \in \{0,1\}\) whether the criterion holds in \(h\). The cheapest sufficient capture:</p>
${M(R`\Omega_t^{*} = \arg\min_{\Omega}\ \mathrm{Cost}(\Omega) \quad \text{s.t.} \quad \forall h_i, h_j:\ E_\Omega(h_i) = E_\Omega(h_j) \Rightarrow C(h_i) = C(h_j)`)}
<p>Equivalently \(C(h_i) \neq C(h_j) \Rightarrow E_\Omega(h_i) \neq E_\Omega(h_j)\): no two possible histories may look identical under the evidence while disagreeing on the criterion. This is the indistinguishability test for evidential soundness. For the rename, \(\Omega_t^{*} = \{\mathrm{digest}(\mathit{notes}_{\mathrm{pre}})\}\).</p>
${M(R`P_t^{\mathrm{proof}}(a) = P\big(\neg\,\mathrm{Provable}(C_{t+k}) \mid a,\ X_t\big) \qquad \text{is not} \qquad P(\mathit{TaskFailure} \mid a)`)}
${M(R`\Delta_{\mathrm{preserve}} = P_t^{\mathrm{proof}}(a) - P_t^{\mathrm{proof}}\big(a \mid \mathrm{preserve}(\Omega)\big), \qquad \mathrm{preserve}(\Omega)\ \text{worthwhile iff}\ \Delta_{\mathrm{preserve}} \cdot V_{\mathrm{proof}} > \mathrm{Cost}(\Omega)`)}
<p>An action may be operationally safe and epistemically dangerous: \(P(\text{succeeds} \mid a) \approx 1\) while \(P(\mathrm{Provable}(C) \mid a) \ll 1\). ${MEAS} T4 is one real instance of the second quantity collapsing <em>for the judge's view</em> after a move, although the journal still held the proof. ${OPEN} Whether \(\Omega^{*}\) or \(P^{\mathrm{proof}}\) can be estimated before an action, for criteria written in natural language. ${OPEN} The <em>unrecoverable</em> case — a fact that exists only before the action — has a minimal construction (move with no prior read) and no observed instance.</p>

<h2>7 · Transition witnesses</h2>
${M(R`\omega_t = \big(\phi_{\mathrm{pre}}(W_t),\ a_t,\ \phi_{\mathrm{post}}(W_{t+1}),\ \rho(W_t, a_t, W_{t+1})\big), \qquad \mathcal{T}_{t \to t+1} = (W_t,\ A_t,\ W_{t+1},\ R_t)`)}
${M(R`\rho_{\mathrm{move}}:\ \mathrm{digest}(\mathit{src}@t) = \mathrm{digest}(\mathit{dst}@t{+}1)\ \wedge\ \mathrm{exists}(\mathit{src}@t{+}1) = 0\ \wedge\ \mathrm{exists}(\mathit{dst}@t{+}1) = 1 \;\Rightarrow\; \omega_t \models C`)}
<p>${RETIRED} as a new primitive: it is a before-image, a provenance edge and a past-time temporal operator (Havelund &amp; Roşu, TACAS 2002; Snodgrass &amp; Ahn 1986; Buneman et al. 2001; Green et al. 2007). ${CAND} as a representation. ${OPEN} The systems question is narrower: which transitions an agent runtime must make first-class evidence, and how it decides that <em>before</em> acting. A digest shows equal bytes, not the causal path; for "moved, not rewritten" it is insufficient.</p>

<h2>8 · Risk over possible futures</h2>
${M(R`R_t(a) = \underbrace{\mathbb{E}_{\tau \sim P_t}\big[L(\tau, a)\big]}_{\text{bad outcome}} + \underbrace{\lambda_D\, D_t(a)}_{\text{divergence}} + \underbrace{\lambda_P\, P_t^{\mathrm{proof}}(a)}_{\text{unprovable completion}}`)}

<h2>9 · Runtime metareasoning</h2>
${M(R`\mathcal{X}_t = \{\textit{act},\ \textit{observe},\ \textit{test},\ \textit{ask},\ \textit{fork},\ \textit{replan},\ \textit{preserve},\ \textit{wait}\}`)}
${M(R`V(\mathcal{F}_t) = -\big[\alpha\,\mathcal{H}_t + \beta D_t + \gamma R_t + \delta P_t^{\mathrm{proof}}\big]`)}
${M(R`x_t^{*} = \arg\max_{x \in \mathcal{X}_t}\Big[\mathbb{E}\big[V(\mathcal{F}_{t+1}) \mid x,\ X_t\big] - V(\mathcal{F}_t) - \lambda_C\,\mathrm{Cost}(x) - \lambda_L\,\mathrm{Latency}(x)\Big]`)}
<p>${PRIOR} Value of information (Howard 1966) and rational metareasoning (Russell &amp; Wefald 1991) supply the decision rule; speculative execution (Nightingale et al., SOSP 2005) is the systems precedent for acting on a predicted future. The only candidate contribution is the <em>state</em> the rule is computed over — in particular <em>preserve</em>, choosing what to keep because of what a future proof will need. Its cheapest rival is a wholesale snapshot, which on a filesystem costs almost nothing.</p>

<h2>10 · Forecast identity, resolution and calibration</h2>
${M(R`f_i = (W_i,\ B_i,\ \tau_i,\ p_i,\ \Omega_i,\ T_i), \qquad \mathrm{Valid}(f_i, t) \iff B_i \simeq B_t \ \wedge\ W_i \simeq W_t`)}
<table class="defs">
  <tr><td>${m("W_i")}</td><td>world version the forecast was made against</td></tr>
  <tr><td>${m("B_i")}</td><td>basis: observations, evidence, assumptions, runtime state</td></tr>
  <tr><td>${m(R`\tau_i`)}</td><td>forecast trajectory or outcome class</td></tr>
  <tr><td>${m("p_i")}</td><td>probability / confidence</td></tr>
  <tr><td>${m(R`\Omega_i`)}</td><td>predicted future information requirement</td></tr>
  <tr><td>${m("T_i")}</td><td>resolution condition / horizon</td></tr>
</table>
${M(R`\mathrm{Resolve}(f_i,\ O_{i+1:t}) \in \{\textsf{satisfied},\ \textsf{violated},\ \textsf{void}\}`)}
<p><strong>satisfied</strong> — the basis held and the predicted event occurred. <strong>violated</strong> — the basis held and it did not. <strong>void</strong> — the world or premise changed so the forecast no longer applies; not a prediction error. The same version-binding appears in MØBIUS's shipped approval revalidation (<code>reusable | superseded | unevaluable</code>) and in published commit-time authorization (CommitGuard, arXiv 2607.10487) — it is ${PRIOR} as a pattern.</p>
${M(R`y_i = \mathbf{1}\big[\mathrm{Resolve}(f_i) = \textsf{satisfied}\big], \qquad \mathrm{BS} = \frac{\sum_{i:\,r_i \neq \textsf{void}} (p_i - y_i)^2}{\big|\{i : r_i \neq \textsf{void}\}\big|}`)}
${M(R`\Gamma_t = \mathrm{CalibrationHistory}(f_1, \ldots, f_t), \qquad \mathit{Trust}_{t+1} = g(\Gamma_t)`)}
<p>${NE} on existing data. R3 P4 resolved 1,345 model-written <code>expected</code> assertions from 104 journals: they are bare Booleans. A constant forecast has one bin, so the Murphy resolution term is zero by definition whatever the outcomes, and a kill criterion "resolution ≈ 0" fires on arithmetic. Calibration is a <em>requirement</em> on any future FTR experiment, not a result.</p>

<h2>11 · The candidate object and its loop</h2>
${M(R`\mathcal{F}_t = P_\theta\big(\tau_{t:t+k},\ \Omega_{t:t+k},\ R_{t:t+k} \mid H_t,\ W_t,\ G_t,\ C_t,\ M_t\big)`)}
${M(R`X_t \rightarrow \mathcal{F}_t \rightarrow x_t^{*} \rightarrow A_t \rightarrow (O_{t+1},\ W_{t+1}) \rightarrow \mathrm{Resolve} \rightarrow \Gamma_{t+1} \rightarrow \mathcal{F}_{t+1}`)}
<figure><img class="figw" src="${fig("mobius-r3-ftr-loop")}" alt=""/><figcaption>Figure 1. FTR as a candidate closed loop. Only a Boolean expectation layer exists in code.</figcaption></figure>

<h2>12 · Completion soundness and certificate closure</h2>
<p>Let \(J_i\) be the evidence the judge was actually shown for criterion \(i\) and \(C_i\) the evidence the final completion record keeps.</p>
${M(R`\begin{aligned} &\text{closure:} && J_i \subseteq C_i \\ &\text{replay:} && \mathrm{Judge}(\mathit{Criterion}_i,\ C_i) = \mathit{OriginalDecision}_i \\ &\text{soundness:} && \mathrm{Judge}(C, E) = \textsf{established} \Rightarrow E \models C \end{aligned}`)}
${M(R`\boxed{\ \text{world correctness} \;\not\Rightarrow\; \text{evidential correctness}\ }`)}
<p>${MEAS} In MØBIUS at <code>f9b27dd</code> the judge is shown \(J_i = E_{\mathrm{binding}} \cup E_{\mathrm{runView}}\), while <code>#bindClaimed</code> records \(C_i = E_{\mathrm{binding}}\) and <code>goal.completed</code> carries it. Across R3 P3, 11 judge-bound criteria appear in completed runs; \(J_i \subseteq C_i\) holds in <strong>0</strong>; in 8 the omitted evidence carries part of what the judge's own reason cites. The journal's <code>criterion.judged</code> event still names \(J_i\): the gap is in the certificate, not the log. Replay has not been run.</p>
<p>${MEAS} Manual audit of all 20 <code>established</code> verdicts: 19 supported by what the judge was shown (3 only on a literal reading); <strong>1 not</strong> — R1 T4 repetition 3, where the judge answered <code>cannot-tell</code> correctly, was then shown only a read of <code>archive.txt</code>, and answered <code>established</code> with a reason that never mentions the former content. One in twenty is an existence proof, not a rate.</p>
<figure><img class="figw" src="${fig("mobius-r3-certificate")}" alt=""/><figcaption>Figure 2. The judge's basis against the completion record, T4 repetition 3.</figcaption></figure>

<h2>13 · A worked temporal example</h2>
<p>Criterion \(C\): <em>archive.txt exists with the former content of notes.txt, and notes.txt no longer exists.</em></p>
${M(R`E_{\mathrm{post}} = \{\ \mathit{archive}_{t+1} = \text{“the note”},\ \neg\,\mathrm{exists}(\mathit{notes}_{t+1})\ \}`)}
${M(R`\begin{aligned} h_1 &:\ \mathit{notes}_t = \text{“the note”} \to \mathit{archive}_{t+1} = \text{“the note”} && C(h_1) = 1 \\ h_2 &:\ \mathit{notes}_t = \text{“other”} \to \mathit{archive}_{t+1} = \text{“the note”} && C(h_2) = 0 \end{aligned}`)}
${M(R`E_{\mathrm{post}}(h_1) = E_{\mathrm{post}}(h_2) \;\Rightarrow\; E_{\mathrm{post}} \not\models C`)}
${M(R`\Omega = \{\mathrm{digest}(\mathit{notes}_t)\}: \quad \mathrm{digest}(\mathit{notes}_t) = \mathrm{digest}(\mathit{archive}_{t+1}) \wedge \neg\,\mathrm{exists}(\mathit{notes}_{t+1}) \Rightarrow C`)}
<p>In the real journal (<code>r1/f9b27dd/P3-control-b/T4-rename/rep-3</code>) both digests are <code>sha256:6862e454af825d8f…</code>: event 7, before the move, and event 17, after it.</p>
<figure><img class="figw" src="${fig("mobius-r3-two-histories")}" alt=""/><figcaption>Figure 3. Same post-state evidence, opposite criterion truth.</figcaption></figure>

<h2>14 · Notation</h2>
<table class="defs">
  <tr><td>${m("W_t")}</td><td>versioned external world state at \(t\)</td></tr>
  <tr><td>${m("H_t")}</td><td>execution history: observations, actions, effects</td></tr>
  <tr><td>${m("G_t,\\ C_t")}</td><td>active goals; completion criteria</td></tr>
  <tr><td>${m("M_t")}</td><td>agent / runtime internal state: plan, tasks, subagents, tool context</td></tr>
  <tr><td>${m("E_t")}</td><td>evidence currently available (to whom — journal, proposer, judge — must be stated)</td></tr>
  <tr><td>${m(R`\Gamma_t`)}</td><td>forecast resolution and calibration history</td></tr>
  <tr><td>${m(R`\tau,\ P_t(\tau),\ \mathcal{T}_t`)}</td><td>trajectory; distribution over trajectories; sampled approximation</td></tr>
  <tr><td>${m(R`D_t,\ \mathcal{H}_t`)}</td><td>disagreement (Gini–Simpson over outcome classes); entropy</td></tr>
  <tr><td>${m(R`\Omega_t^{*}`)}</td><td>cheapest fact set that keeps criterion-distinct histories distinguishable</td></tr>
  <tr><td>${m(R`P_t^{\mathrm{proof}}`)}</td><td>probability that completion becomes unprovable</td></tr>
  <tr><td>${m("R_t(a)")}</td><td>risk of action \(a\) over futures</td></tr>
  <tr><td>${m(R`\mathcal{X}_t,\ x_t^{*}`)}</td><td>meta-action set; chosen meta-action</td></tr>
  <tr><td>${m("f_i,\\ \\mathrm{Resolve},\\ \\mathrm{BS}")}</td><td>forecast instance; resolution; Brier score over non-void forecasts</td></tr>
  <tr><td>${m("J_i,\\ C_i")}</td><td>evidence the judge was shown; evidence the completion record keeps</td></tr>
</table>

<h2>15 · Research status, 19 September 2026</h2>
<table class="data status">
  <tr><th>claim / component</th><th>status</th><th>basis</th></tr>
  <tr><td>FTR overall</td><td>${OPEN}</td><td>reopened by the author as a question after a recommendation to retire it; no measurement yet</td></tr>
  <tr><td>future prediction itself as novelty</td><td>${RETIRED}</td><td>predictive runtime verification (Lindemann et al., arXiv 2211.01539)</td></tr>
  <tr><td>exact prediction of future actions</td><td>${UNS}</td><td>not the surviving claim</td></tr>
  <tr><td>read-only pre-write write-set anticipation</td><td>${KILLED}</td><td>median read coverage 0.25 (33 of 69 zero) against a recall &lt; 0.5 threshold fixed before computing; experiment-arm corpus, so only the shape split (edit vs create/rename) generalises</td></tr>
  <tr><td>Boolean <code>expected</code> → Brier / resolution</td><td>${NE}</td><td>constant forecasts; resolution zero by definition</td></tr>
  <tr><td>rollout disagreement as runtime signal</td><td>${OPEN}</td><td>as uncertainty: prior art; as trigger: untested</td></tr>
  <tr><td>future information requirement \(\Omega^{*}\)</td><td>${OPEN}</td><td>formalised; no estimator</td></tr>
  <tr><td>anticipatory evidence preservation</td><td>${OPEN}</td><td>experiment E4</td></tr>
  <tr><td>proof-failure prediction</td><td>${OPEN}</td><td>one instance of the quantity; no predictor</td></tr>
  <tr><td>transition witness</td><td>${CAND}</td><td>retired as a primitive; kept as representation</td></tr>
  <tr><td>evidence horizon (past out of judge's view)</td><td>${MEAS} ${OPEN}</td><td>45 / 74 cannot-tell; three task shapes; general version open</td></tr>
  <tr><td>unsupported establishment</td><td>${MEAS} ${OPEN}</td><td>1 clear case in 20; rate unknown (E1)</td></tr>
  <tr><td>certificate closure / replayability</td><td>${MEAS} ${OPEN}</td><td>0 / 11 closed; replay not run (E3)</td></tr>
  <tr><td>version-bound decisions and forecasts</td><td>${PRIOR}</td><td>implemented and measured in MØBIUS; published (CommitGuard, PlanFence)</td></tr>
  <tr><td>value of information / computation</td><td>${PRIOR}</td><td>decision machinery, not FTR novelty</td></tr>
  <tr><td>three-valued outcomes / partial observation</td><td>${PRIOR}</td><td>not a novelty claim</td></tr>
  <tr><td>"0 false completions" (R3 P3)</td><td>${NE}</td><td>0 opportunities: 39 / 39 valid rows passed their checker</td></tr>
</table>

<h2>16 · Prior-art boundary</h2>
<p>Before any FTR component is claimed as new it must be separated from: predictive runtime verification and conformal prediction for STL (arXiv 2211.01539); past-time LTL monitoring (TACAS 2002) and runtime verification generally (Leucker &amp; Schallhart, JLAP 2009); temporal databases (Snodgrass &amp; Ahn 1986); provenance (ICDT 2001; PODS 2007); proof-carrying code (POPL 1997); ATMS (de Kleer 1986); value of information (Howard 1966) and rational metareasoning (Russell &amp; Wefald 1991); speculative execution (SOSP 2005); sampling-based uncertainty (arXiv 2203.11171, 2302.09664, 2307.01928); commit-time and dependency-scoped validation for LLM agents (arXiv 2607.10487, 2609.03340) and read-set reconstruction (arXiv 2605.17076); false success in LLM agents (arXiv 2606.09863).</p>

<h2>17 · Candidate invariants</h2>
<ol class="inv">
  <li>A forecast carries explicit \(W, B, T, p\).</li>
  <li>Invalidation of a forecast's basis resolves it as <em>void</em>, never as an ordinary error.</li>
  <li>Before a world-changing action, evidence-loss and proof-loss are evaluated.</li>
  <li>Preserved evidence is attributable to a pre-action world version.</li>
  <li>\(\textsf{established} \Rightarrow E \models C\) for the evidence actually shown.</li>
  <li>The completion record contains the decision basis: \(J_i \subseteq C_i\).</li>
  <li>A forecast's influence on action is weighted by measured calibration, never by its rhetoric.</li>
  <li>Every existence claim is reported with its opportunity count; zero opportunities is "not tested".</li>
</ol>

<h2>18 · Open experiments</h2>
<p><strong>E1 · Evidential soundness replay.</strong> Freeze criterion, prompt, evidence and model for T4 post-only evidence (\(E \not\models C\)); re-ask \(N\) times.</p>
${M(R`\hat p_{\mathrm{est}} = \frac{1}{N}\sum_{i=1}^{N} \mathbf{1}\big[\mathrm{Judge}_i(C, E) = \textsf{established}\big]`)}
<p>\(\hat p_{\mathrm{est}} > 0\) with \(E \not\models C\): unsupported establishment is a property of the judge under that evidence. \(\hat p_{\mathrm{est}} = 0\): repetition 3 is not reproducible from its inputs.</p>
<p><strong>E2 · Evidence-horizon intervention.</strong></p>
${M(R`A_0 = E_{\mathrm{post}}, \quad A_1 = E_{\mathrm{post}} \cup E_{\mathrm{pre}}, \quad A_2 = E_{\mathrm{post}} \cup \omega_{\mathrm{transition}}, \quad A_3 = E_{\mathrm{post}} \cup \text{proposer self-claim}`)}
<p>Measure \(P(\textsf{established} \mid A_k)\), \(P(\textsf{cannot-tell} \mid A_k)\), \(P(\text{unsupported} \mid A_k)\). Hypothesis: \(A_1, A_2 \gg A_0\) for justified establishment and \(A_3 \approx A_0\). If \(A_3\) moves the judge like \(A_1\), the judge reads assertions rather than evidence.</p>
<p><strong>E3 · Certificate closure audit and replay.</strong> \(\chi_i = \mathbf{1}[J_i \subseteq C_i]\), \(\mathrm{ClosureRate} = \tfrac{1}{N}\sum_i \chi_i\) (0/11 today); re-judge from \(C_i\) alone before any fix, so the fix has a baseline.</p>
<p><strong>E4 · Anticipatory evidence preservation.</strong> Before a world-changing action, offer <em>preserve</em> or <em>proceed</em>; trigger \(\mathbf{1}[P_t^{\mathrm{proof}}(a) > \eta]\). Compare with preserve-nothing and preserve-everything (snapshot) baselines on tasks where a later criterion depends on pre-state and matched tasks where it does not:</p>
${M(R`\Delta CT = CT_{\mathrm{base}} - CT_{\mathrm{FTR}}, \quad \Delta UE = UE_{\mathrm{base}} - UE_{\mathrm{FTR}}, \quad \Delta\mathrm{Cost} = \mathrm{Cost}_{\mathrm{FTR}} - \mathrm{Cost}_{\mathrm{base}}`)}
<p><strong>Kill:</strong> no reduction in cannot-tell or unsupported establishment beyond the snapshot baseline at comparable cost, or no generalisation beyond the three task shapes. Every arm reports its opportunity count.</p>

<h2>19 · Evidence index</h2>
<table class="data small">
  <tr><td>R2 pilot (0/6 checker, 5/6 declared complete)</td><td><code>evidence/r2/de5b79b</code></td></tr>
  <tr><td>ADR 0043 re-run (false 0/6, runtime 0/6; R1 6/7)</td><td><code>evidence/{r2,r1}/33e599e</code></td></tr>
  <tr><td>R3 P3 (39 valid rows, 114 judgements)</td><td><code>evidence/r2/f9b27dd/{P3-judge-run,P3-judge-run-b}</code>, <code>evidence/r1/f9b27dd/{P3-control,P3-control-b}</code></td></tr>
  <tr><td>R3 P4 (1,345 assertions, 104 journals)</td><td><code>evidence/p4-expectations/ba4f291</code></td></tr>
  <tr><td>layered determinism (0.923 / 0.795 / CV 0.129)</td><td>re-derived from R3 P3 journals, 13 tasks × 3</td></tr>
  <tr><td>judge and certificate code</td><td><code>packages/runtime-core/src/loop.ts</code> — <code>#bindClaimed</code>, <code>#established</code>, <code>#runView</code></td></tr>
</table>

<section class="closing">
  <div class="closing-inner">
    <p class="closing-line">What is clearer now is not what the answer is,<br/>but what it is not — and which questions are worth the next experiment.</p>
    <div class="sig-block">
      <div class="sig-name">Marc Ellington</div>
      <div class="sig-role">MØBIUS Research</div>
      <img class="sig" src="${pathToFileURL(signature).href}" alt="Marc Ellington — signature"/>
      <div class="sig-date">19 September 2026</div>
    </div>
  </div>
</section>
`;

const html = `<!doctype html><html lang="en"><head><meta charset="utf-8"/>
<title>FTR Core Formalization — 2026-09-19</title>
<link rel="stylesheet" href="${katexCss}"/>
<style>
  @page { size: A4; margin: 20mm 19mm 22mm; @bottom-center { content: "MØBIUS · FTR Core Formalization · 2026-09-19 · " counter(page); font: 8pt 'Helvetica Neue', Helvetica, Arial, sans-serif; color: #8a867b; } }
  @page :first { @bottom-center { content: none; } }
  html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
  body { font-family: 'STIX Two Text', Georgia, serif; font-size: 10.4pt; line-height: 1.5; color: #262521; margin: 0; }
  h1, h2, .kicker, .subtitle, .meta, table, figcaption, .warn, .st { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }
  h2 { font-size: 12.5pt; color: #262521; margin: 20pt 0 6pt; padding-top: 6pt; border-top: 0.6pt solid #d8d2c2; break-after: avoid; }
  p { margin: 5pt 0; text-align: justify; hyphens: auto; }
  code { font-family: Menlo, 'SF Mono', monospace; font-size: 8.4pt; background: #f1ede3; padding: 0.5pt 2.5pt; border-radius: 2pt; }
  ul, ol { margin: 4pt 0 4pt 16pt; padding: 0; } li { margin: 2.5pt 0; }
  .katex-display { margin: 7pt 0; overflow: hidden; break-inside: avoid; }
  .katex { font-size: 1.05em; }
  .cover { min-height: 245mm; display: flex; flex-direction: column; justify-content: center; break-after: page; }
  .kicker { font-size: 9pt; letter-spacing: 0.08em; text-transform: uppercase; color: #b3562f; }
  h1 { font-size: 54pt; margin: 6pt 0 0; letter-spacing: 0.02em; color: #262521; }
  .subtitle { font-size: 20pt; color: #4a4842; margin-top: 2pt; }
  .subsub { font-size: 11pt; color: #6b6a63; margin: 14pt 0 10pt; line-height: 1.5; }
  .coverformula { margin: 16pt 0; padding: 10pt 0; border-top: 0.6pt solid #d8d2c2; border-bottom: 0.6pt solid #d8d2c2; }
  .warn { font-size: 9.2pt; line-height: 1.5; background: #f7eadf; border-left: 3pt solid #c4623f; padding: 9pt 12pt; margin: 12pt 0 18pt; }
  table { border-collapse: collapse; width: 100%; font-size: 8.8pt; margin: 7pt 0; break-inside: avoid; }
  td, th { border-bottom: 0.5pt solid #e0dace; padding: 3.5pt 5pt; vertical-align: top; text-align: left; }
  th { font-weight: 700; border-bottom: 0.9pt solid #b9b3a3; }
  table.meta td:first-child { color: #8a867b; width: 26mm; }
  table.defs td:first-child { width: 36mm; }
  table.status td:nth-child(2) { width: 30mm; white-space: nowrap; }
  table.small td { font-size: 8.2pt; }
  .st { display: inline-block; font-size: 6.6pt; font-weight: 700; letter-spacing: 0.03em; padding: 0.3pt 3pt; border: 0.6pt solid currentColor; border-radius: 2pt; white-space: nowrap; vertical-align: 1pt; }
  .st-open { color: #b3562f; } .st-killed { color: #8f2f2f; } .st-retired { color: #6b6a63; } .st-prior { color: #4f6340; } .st-measured { color: #2f5d7a; } .st-ne { color: #8a6124; }
  figure { margin: 10pt 0; break-inside: avoid; text-align: center; }
  .figw { width: 108mm; max-width: 100%; }
  figcaption { font-size: 8.4pt; color: #6b6a63; margin-top: 4pt; }
  .inv li { margin: 2pt 0; }
  .closing { break-before: page; min-height: 240mm; display: flex; align-items: center; justify-content: center; }
  .closing-inner { width: 120mm; text-align: left; }
  .closing-line { font-style: italic; color: #4a4842; font-size: 11.5pt; line-height: 1.6; text-align: left; margin-bottom: 26mm; }
  .sig-block { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }
  .sig-name { font-size: 11pt; font-weight: 600; color: #262521; }
  .sig-role { font-size: 9pt; color: #8a867b; margin-top: 1pt; }
  .sig { display: block; width: 46mm; height: auto; margin: 9mm 0 5mm -2mm; }
  .sig-date { font-size: 9pt; color: #6b6a63; }
</style></head><body>${t(body)}</body></html>`;

const tmp = fs.mkdtempSync(path.join(os.tmpdir(), "ftr-pdf-"));
const htmlPath = path.join(tmp, "ftr.html");
fs.writeFileSync(htmlPath, html);
execFileSync(chrome, [
  "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--allow-file-access-from-files",
  `--print-to-pdf=${out}`, pathToFileURL(htmlPath).href,
], { stdio: "inherit" });
fs.rmSync(tmp, { recursive: true, force: true });
console.log("wrote", path.relative(root, out));

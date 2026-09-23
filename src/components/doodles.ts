/**
 * Hand-drawn section doodles for the reading-progress rail.
 *
 * Each is a 48×48 line drawing in two inks — `ink` for the part that stays put, `hot` (the accent)
 * for the part that moves — and each has one small motion that loops while its section is being
 * read. The motions live in ReadingProgress.astro under `.rp-doodle`.
 *
 * A section gets its doodle from words in its heading; the first rule that matches wins, so the
 * more specific verdicts (killed, judged, witnessed) sit above the general ones. No two sections of
 * one post share a doodle: a heading whose best match is taken falls to its next match, and then to
 * an unused doodle in an order seeded by the post's headings — so posts differ from one another,
 * and a rebuild draws the same post the same way.
 *
 * `cheer` is not in the pool. It is the one shown when the reader reaches the end.
 */

export type DoodleName =
  | "gear"
  | "check"
  | "scale"
  | "eye"
  | "magnifier"
  | "gauge"
  | "cross"
  | "gate"
  | "seedling"
  | "flag"
  | "question"
  | "pen"
  | "lightbulb"
  | "compass"
  | "hourglass"
  | "book";

const rules: [RegExp, DoodleName][] = [
  [/kill|negative|withdr|fail|杀|否定|失败|撤回/i, "cross"],
  [/judg|verdict|判|裁决/i, "scale"],
  [/witness|observ|见证|观察/i, "eye"],
  [/probe|jepsen|search|prior art|literature|探针|检索|文献/i, "magnifier"],
  [/instrument|measur|bench|仪器|测量|度量/i, "gauge"],
  [/gate|reduction|门|归约/i, "gate"],
  [/approv|grant|批准|审批|授权/i, "check"],
  [/attribut|author|who wrote|归因|作者/i, "pen"],
  [/changed|grow|learn|how i|改变|成长|变了/i, "seedling"],
  [/stand|status|where|现状|处境|在哪/i, "flag"],
  [/coda|thesis|question|open|尾声|论点|问题|未解/i, "question"],
  [/lesson|insight|idea|hypothes|why|教训|启发|想法|假设|为什么/i, "lightbulb"],
  [
    /method|direction|\bnext\b|\bplan|route|approach|方法|方向|下一步|计划|路线/i,
    "compass",
  ],
  // Whole words: "runtime" is not about time, and "late-bound" is taken by the witness rule above.
  [
    /\bdays?\b|\btime(line)?s?\b|history|\bhours?\b|\bwhen\b|天|时间|历史|时刻/i,
    "hourglass",
  ],
  [
    /journal|record|ledger|\bnotes?\b|essay|\bread|日志|记录|账本|笔记|文章/i,
    "book",
  ],
  [/runtime|feature|system|architect|运行时|特性|系统|架构/i, "gear"],
];

const pool: DoodleName[] = [
  "pen",
  "lightbulb",
  "compass",
  "book",
  "hourglass",
  "gear",
  "seedling",
  "magnifier",
  "eye",
  "gauge",
  "flag",
  "question",
  "scale",
  "gate",
  "check",
  "cross",
];

/** One doodle per heading, none repeated within the post while the pool lasts. */
export function assignDoodles(headings: string[]): DoodleName[] {
  // Seeded from the headings, so the fallback order differs between posts but not between builds.
  let seed = 1;
  for (const ch of headings.join("|"))
    seed = (seed * 31 + ch.charCodeAt(0)) % 2147483647;
  const rand = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
  const fallback = [...pool].sort(() => rand() - 0.5);

  const used = new Set<DoodleName>();
  return headings.map(heading => {
    const matches = rules.filter(([re]) => re.test(heading)).map(([, d]) => d);
    const pick =
      matches.find(d => !used.has(d)) ??
      fallback.find(d => !used.has(d)) ??
      matches[0] ??
      fallback[used.size % fallback.length];
    used.add(pick);
    return pick;
  });
}

// Teeth for the gear: eight short strokes between r = 9.2 and r = 13.4 around (24, 24).
const teeth = Array.from({ length: 8 }, (_, k) => {
  const a = (k * Math.PI) / 4;
  const [c, s] = [Math.cos(a), Math.sin(a)];
  const p = (r: number) =>
    `${(24 + r * c).toFixed(2)} ${(24 + r * s).toFixed(2)}`;
  return `M${p(9.2)} L${p(13.4)}`;
}).join(" ");

export const doodles: Record<DoodleName, string> = {
  gear: `
    <g class="d-spin">
      <path class="hot" d="M24 14.6 C29.4 14.4 33.6 18.6 33.4 24 C33.6 29.3 29.4 33.6 24 33.4 C18.6 33.5 14.4 29.3 14.6 24 C14.5 18.7 18.4 14.7 23.2 14.5"/>
      <path class="hot" d="${teeth}"/>
      <path class="ink" d="M27.4 24 C27.4 26 26 27.5 24 27.5 C22 27.5 20.6 26 20.6 24 C20.6 22 22 20.5 24 20.5 C25.7 20.5 27.1 21.6 27.4 23.2"/>
    </g>`,
  check: `
    <path class="ink" d="M11 13 C18 12.4 29 12.6 36.5 13.2 C37 20 36.8 29 36.2 35.8 C28 36.4 19 36.2 11.6 35.6 C11 28 11.2 20 11.2 13.6"/>
    <path class="hot d-draw" pathLength="1" d="M16.5 24.5 C18.5 26.4 20.4 28.6 22 30.6 C25.4 24.6 29.4 19.6 33.5 15.5"/>`,
  scale: `
    <path class="ink" d="M24 13 L24 38 M16.5 38.6 C21 38.1 27 38.1 31.5 38.6"/>
    <g class="d-tilt">
      <path class="hot" d="M11 14.2 C18 13.5 30 13.5 37 14.2"/>
      <path class="ink" d="M12 14.2 L8.6 25 M12 14.2 L15.4 25 M36 14.2 L32.6 25 M36 14.2 L39.4 25"/>
      <path class="hot" d="M7.6 25 C9.6 28.8 14.4 28.8 16.4 25 M31.6 25 C33.6 28.8 38.4 28.8 40.4 25"/>
    </g>`,
  eye: `
    <g class="d-blink">
      <path class="ink" d="M5.5 24.2 C12 15.4 36 15.2 42.5 23.8 C36 32.6 12 32.8 5.5 24.2"/>
      <g class="d-look">
        <path class="hot" d="M29.6 24 C29.6 27.2 27.1 29.6 24 29.6 C20.9 29.6 18.4 27.2 18.4 24 C18.4 20.9 20.9 18.4 24 18.4 C26.6 18.4 28.8 20.1 29.4 22.4"/>
        <circle class="hot-fill" cx="24" cy="24" r="2.3"/>
      </g>
    </g>`,
  magnifier: `
    <g class="d-orbit">
      <path class="ink" d="M29 20 C29 25 25 29 20 29 C15 29 11 25 11 20 C11 15 15 11 20 11 C24.6 11 28.4 14.4 28.9 18.8"/>
      <path class="hot" d="M15.2 17.2 C16 15.6 17.4 14.6 19 14.4"/>
      <path class="hot thick" d="M26.8 27.2 L37.6 38"/>
    </g>`,
  gauge: `
    <path class="ink" d="M9 32.4 C8.6 22.2 16 14.6 24 14.6 C32 14.6 39.4 22.2 39 32.4"/>
    <path class="ink" d="M12.6 22.4 L15.2 24 M24 14.6 L24 17.6 M35.4 22.4 L32.8 24"/>
    <g class="d-needle">
      <path class="hot" d="M24 32 L24.4 19.4"/>
    </g>
    <circle class="hot-fill" cx="24" cy="32" r="2.2"/>`,
  cross: `
    <path class="hot d-draw-a" pathLength="1" d="M14 14 C20 20.5 27.5 28 34.2 34.6"/>
    <path class="hot d-draw-b" pathLength="1" d="M34.6 13.4 C28 20 21 27 13.4 34.2"/>`,
  gate: `
    <path class="ink" d="M10 12 L10 38.4 M38 12 L38 38.4 M6 38.8 C18 38.2 30 38.2 42 38.8"/>
    <g class="d-lift">
      <path class="hot" d="M10 20 C20 19.4 30 19.4 37.6 20"/>
      <path class="hot" d="M16 19.8 L14 24.2 M23 19.6 L21 24 M30 19.6 L28 24"/>
    </g>`,
  seedling: `
    <path class="ink" d="M12 38.6 C20 38 28 38 36 38.6"/>
    <g class="d-grow">
      <path class="hot" d="M24 38 C24.2 32 23.6 27 24 21"/>
      <g class="d-sway">
        <path class="hot" d="M24 27.4 C19 27.4 15.6 24.2 15 19.6 C20 19.6 23.4 22.6 24 27.4"/>
        <path class="hot" d="M24 23.2 C28.2 23 32.4 19.8 33 15 C28.6 15.2 24.6 18.2 24 23.2"/>
      </g>
    </g>`,
  flag: `
    <path class="ink" d="M15 9.6 L15.2 39"/>
    <g class="d-wave">
      <path class="hot" d="M15.2 11 C21 9 26 13.6 34 11 C33 15.6 33 19 34 23.2 C26 25.6 21 21 15.2 23"/>
    </g>`,
  question: `
    <g class="d-bob">
      <path class="hot" d="M17.6 17 C17.4 12.2 21 9.6 24.6 9.6 C29 9.6 32.2 12.6 31.6 16.6 C31 20.6 26 21.6 24.6 25 C24.1 26.4 24 28 24 29.6"/>
      <circle class="hot-fill d-pulse" cx="24" cy="36" r="1.9"/>
    </g>`,
  pen: `
    <g class="d-nib">
      <path class="ink" d="M30.4 9.6 L38.4 17.6 L20.2 35.8 L12.2 37.8 L14.2 29.8 Z M14.2 29.8 L20.2 35.8"/>
    </g>
    <path class="hot d-draw" pathLength="1" d="M7.6 42.4 C11.6 39.4 13.6 44.4 17.6 41.4 C21.6 38.4 23.6 44.4 27.6 41.4 C31.6 38.4 33.6 44.4 40 41.2"/>`,
  lightbulb: `
    <path class="ink" d="M18.6 27.6 C14.6 24.8 13 20.6 14.4 16.4 C16 12 20 9.8 24 9.8 C28.2 9.8 32 12.2 33.6 16.6 C35 20.6 33.4 24.8 29.4 27.6 L29.2 31.4 L18.8 31.4 Z"/>
    <path class="ink" d="M19.4 34.6 L28.6 34.4 M21 37.8 L27 37.8"/>
    <path class="hot" d="M21 27.4 L22.4 20.8 L24 23.4 L25.6 20.8 L27 27.4"/>
    <path class="hot d-glow" d="M24 3.2 L24 6 M10.4 9.6 L12.4 11.6 M37.6 9.6 L35.6 11.6 M6.2 20.2 L9 20.4 M41.8 20.2 L39 20.4"/>`,
  compass: `
    <path class="ink" d="M38 24 C38 31.8 31.8 38 24 38 C16.2 38 10 31.8 10 24 C10 16.2 16.2 10 24 10 C31.2 10 37.2 15.4 37.9 22.4"/>
    <path class="ink" d="M24 11.8 L24 14 M24 34 L24 36.2 M11.8 24 L14 24 M34 24 L36.2 24"/>
    <g class="d-wobble">
      <path class="hot" d="M24 15.2 L27.2 24 L24 32.8 L20.8 24 Z"/>
      <path class="hot-fill" d="M24 15.2 L27.2 24 L20.8 24 Z"/>
    </g>`,
  hourglass: `
    <g class="d-flip">
      <path class="ink" d="M14 9.6 L34 9.6 M14 38.4 L34 38.4"/>
      <path class="ink" d="M16 9.8 C16 17 22 20 24 24 C26 28 32 31 32 38.2 M32 9.8 C32 17 26 20 24 24 C22 28 16 31 16 38.2"/>
      <path class="hot" d="M19.6 34.8 C21.6 32.4 26.4 32.4 28.4 34.8 M24 25.4 L24 30.6 M20.4 14.4 C22.6 15.6 25.4 15.6 27.6 14.4"/>
    </g>`,
  book: `
    <path class="ink" d="M24 14 C19 11.6 13 11.2 8 12.4 L8 35.6 C13 34.4 19 34.8 24 37.2 C29 34.8 35 34.4 40 35.6 L40 12.4 C35 11.2 29 11.6 24 14 L24 37.2"/>
    <g class="d-page">
      <path class="hot" d="M24 14.4 C27.8 12.8 31.8 12.4 35.6 13 L35.6 33.4 C31.8 32.9 27.8 33.3 24 35"/>
    </g>`,
};

// The end of the post: a star drawn by hand, and a ring of short strokes bursting out around it.
const rays = Array.from({ length: 10 }, (_, k) => {
  const a = (k * Math.PI) / 5 + Math.PI / 10;
  const [c, s] = [Math.cos(a), Math.sin(a)];
  const p = (r: number) =>
    `${(24 + r * c).toFixed(2)} ${(24 + r * s).toFixed(2)}`;
  return `M${p(15.5)} L${p(20.5)}`;
}).join(" ");

export const cheer = `
  <g class="d-burst">
    <path class="hot" d="${rays}"/>
  </g>
  <g class="d-pop">
    <path class="hot" d="M24 13.6 L26.8 20.4 L33.8 21.2 L28.4 25.8 L30.2 32.8 L24.1 29 L17.8 32.9 L19.7 25.9 L14.2 21.3 L21.3 20.5 Z"/>
    <path class="hot-fill" d="M24 18.6 L25.4 22 L28.8 22.4 L26.2 24.6 L27 28 L24 26.2 L21 28 L21.8 24.6 L19.2 22.4 L22.6 22 Z"/>
  </g>`;

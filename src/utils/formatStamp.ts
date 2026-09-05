/**
 * Render a version's `at` timestamp.
 *
 * ## Why this does not convert to a timezone
 *
 * The obvious thing is to format through `Intl.DateTimeFormat` in `SITE.timezone`, the way post
 * dates are. Doing that here moves the **day**: `2026-09-04T13:22:28-04:00` is 01:22 on the 5th in
 * Asia/Shanghai, so V34 would read "Sep 5" on the site while `PUBLICATION.md` — and the commit,
 * and the plan document — all say the 4th. Four of the twelve versions shift like this.
 *
 * A version's date is the working day it landed on, not a clock reading somewhere else. So the
 * string's own parts are printed verbatim and the offset is carried in the `dateTime` attribute,
 * where a reader who cares can recover the exact instant and a machine can parse it properly.
 */

const MONTHS_EN = [
  "Jan", "Feb", "Mar", "Apr", "May", "Jun",
  "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
];

/** `2026-09-04T13:22:28-04:00` → `4 Sep 2026 · 13:22` / `2026年9月4日 13:22`. */
export function formatStamp(at: string, lang: "en" | "zh"): string {
  const [date, rest] = at.split("T");
  const parts = (date ?? "").split("-");
  const year = parts[0];
  const month = parts[1];
  const day = parts[2];
  const time = (rest ?? "").slice(0, 5);

  if (year === undefined || month === undefined || day === undefined) return at;

  if (lang === "zh") {
    return `${year}年${Number(month)}月${Number(day)}日 ${time}`;
  }
  return `${Number(day)} ${MONTHS_EN[Number(month) - 1]} ${year} · ${time}`;
}

/**
 * The day alone, for things whose clock is not real.
 *
 * Posts carry `pubDatetime: …T12:00:00Z` by convention across this whole blog — noon is a
 * placeholder nobody chose, so printing it beside a version's actual commit minute would put false
 * precision next to real precision and make both look the same.
 */
export function formatDay(at: string, lang: "en" | "zh"): string {
  const parts = (at.split("T")[0] ?? "").split("-");
  const year = parts[0];
  const month = parts[1];
  const day = parts[2];

  if (year === undefined || month === undefined || day === undefined) return at;

  if (lang === "zh") return `${year}年${Number(month)}月${Number(day)}日`;
  return `${Number(day)} ${MONTHS_EN[Number(month) - 1]} ${year}`;
}

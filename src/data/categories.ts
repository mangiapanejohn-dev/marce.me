/**
 * The category vocabulary. One entry per category, with its display name in each locale.
 *
 * ## Why this is a closed set and tags are not
 *
 * A tag is free text: a typo costs one orphan tag page nobody visits. A category is navigation —
 * it has its own route, its own index, and a place in the header — so a typo silently forks the
 * archive into two categories with the same intent. `content.config.ts` derives a `z.enum` from
 * the keys below, which means a category that is not declared here fails `astro check`, and
 * `astro check` runs inside `npm run build`. Adding a category is a deliberate edit to this file.
 *
 * The other thing this buys, which tags cannot have: a display name per locale. A tag renders as
 * its own literal string, so `MØBIUS` is `MØBIUS` on both sites. A category renders through the
 * map below, so the same slug is "Research" on `/categories/research` and 「研究」 on
 * `/zh/categories/research`.
 */

export const categories = {
  research: { en: "Research", zh: "研究" },
  notes: { en: "Notes", zh: "随笔" },
} as const;

export type CategorySlug = keyof typeof categories;

/** The keys, in a shape `z.enum` accepts. Order is the declaration order above. */
export const categorySlugs = Object.keys(categories) as [
  CategorySlug,
  ...CategorySlug[],
];

/** The default for the 20-odd posts written before categories existed. */
export const defaultCategory: CategorySlug = "notes";

/** Display name for `slug` in `lang`, falling back to the English name. */
export function categoryName(slug: CategorySlug, lang: "en" | "zh"): string {
  return categories[slug][lang] || categories[slug].en;
}

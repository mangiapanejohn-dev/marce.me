import type { CollectionEntry } from "astro:content";
import { categorySlugs, type CategorySlug } from "@/data/categories";
import postFilter from "./postFilter";

interface CategoryCount {
  category: CategorySlug;
  count: number;
}

/**
 * The categories that actually have posts, in declaration order, with their counts.
 *
 * Declaration order rather than alphabetical — unlike tags, the vocabulary in
 * `@/data/categories` is authored, so the order it is written in is a choice worth keeping. A
 * declared category with no posts gets no route and no chip: the archive shows what exists.
 */
const getUniqueCategories = (
  posts: CollectionEntry<"blog">[]
): CategoryCount[] => {
  const published = posts.filter(postFilter);

  return categorySlugs
    .map(category => ({
      category,
      count: published.filter(post => post.data.category === category).length,
    }))
    .filter(({ count }) => count > 0);
};

export default getUniqueCategories;

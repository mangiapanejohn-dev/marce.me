import type { CollectionEntry } from "astro:content";
import type { CategorySlug } from "@/data/categories";
import getSortedPosts from "./getSortedPosts";

/**
 * Posts in one category, newest first.
 *
 * The counterpart of `getPostsByTag`, minus the slugify step: a tag's slug is derived from its
 * own display string, while a category's slug *is* the key in `@/data/categories` and its display
 * name is looked up from it. That is what lets the same category read "Research" on the English
 * site and 「研究」 on the Chinese one.
 */
const getPostsByCategory = (
  posts: CollectionEntry<"blog">[],
  category: CategorySlug
) => getSortedPosts(posts.filter(post => post.data.category === category));

export default getPostsByCategory;

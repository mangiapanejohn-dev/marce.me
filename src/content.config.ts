import { defineCollection, z } from "astro:content";
import { glob } from "astro/loaders";
import { SITE } from "@/config";
import { categorySlugs, defaultCategory } from "@/data/categories";

export const BLOG_PATH = "src/data/blog";

const blog = defineCollection({
  loader: glob({ pattern: "**/[^_]*.md", base: `./${BLOG_PATH}` }),
  schema: ({ image }) =>
    z.object({
      author: z.string().default(SITE.author),
      lang: z.enum(["en", "zh"]).default("en"),
      pubDatetime: z.date(),
      modDatetime: z.date().optional().nullable(),
      title: z.string(),
      featured: z.boolean().optional(),
      draft: z.boolean().optional(),
      tags: z.array(z.string()).default(["others"]),
      // Closed set, declared in `@/data/categories`. A category outside it fails `astro check`,
      // which runs inside `npm run build` — so a typo is a failed deploy, not a forked archive.
      // Defaulted because every post written before categories existed has no `category:` line.
      category: z.enum(categorySlugs).default(defaultCategory),
      /**
       * The series this post belongs to, when it belongs to one.
       *
       * Prev/next navigation walks the series rather than the whole blog, so a reader working
       * through the MØBIUS version log is not handed a personal essay at V35. Optional, and a post
       * without it navigates the whole blog exactly as before.
       *
       * A field rather than a reuse of `category` or a tag: `category: "research"` happens to equal
       * this set today and would silently absorb the first non-MØBIUS research post, and the
       * `MØBIUS` tag already sits on a career post that is not part of the log.
       */
      series: z.string().optional(),
      cover: z.string().optional(),
      ogImage: image().or(z.string()).optional(),
      description: z.string(),
      canonicalURL: z.string().optional(),
      hideEditPost: z.boolean().optional(),
      timezone: z.string().optional(),
    }),
});

export const collections = { blog };

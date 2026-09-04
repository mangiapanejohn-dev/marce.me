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
      cover: z.string().optional(),
      ogImage: image().or(z.string()).optional(),
      description: z.string(),
      canonicalURL: z.string().optional(),
      hideEditPost: z.boolean().optional(),
      timezone: z.string().optional(),
    }),
});

export const collections = { blog };

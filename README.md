# marce.me

Personal site & dev diary of **Mark Ellington** (Marc / BUG) — Vibe Coder, building AI tools that actually remember you.

🌐 Live at **[marcyy.me](https://marcyy.me)**

Most of what I build ends up on GitHub for you to fork & remix. This site is where I write the dev diaries behind them — DiscorverX, Pawly, MarcStar, RE CODE, Resonix-AG, and more.

## Tech

- [Astro](https://astro.build) (based on the [AstroPaper](https://github.com/satnaing/astro-paper) theme)
- Tailwind CSS v4
- Pagefind full-text search · dynamic OG images · RSS · sitemap
- Deployed on Vercel

## Local development

```bash
npm install
npm run dev      # start dev server at localhost:4321
npm run build    # production build + search index
npm run preview  # preview the build
```

Blog posts live in [`src/data/blog/`](src/data/blog/) as Markdown. Site config is in [`src/config.ts`](src/config.ts).

## Self-hosted install pages

Two hidden pages ship my Claude Code tooling as a one-line install:

| Page | What it ships | Bundle source | Build script |
| --- | --- | --- | --- |
| `/ø` | `/omega` + `/omega-update` + 7 council agents + weekly automation | [`omega-dist/`](omega-dist/) | [`scripts/build-omega-bundle.sh`](scripts/build-omega-bundle.sh) |
| `/ƒ` | 14 style modes — 9 persistent + 5 one-shot | [`skills-dist/`](skills-dist/) | [`scripts/build-skills-bundle.sh`](scripts/build-skills-bundle.sh) |

Both follow the same shape, and it's worth saying why, because "just make the repo
public and `git clone` it" is the obvious alternative:

- **The source repos are private and stay private.** They hold personal
  knowledge-base skills alongside the shareable ones. Self-hosting a bundle lets
  me publish a curated subset without opening the whole repo, and the build step
  is where the curation is enforced — `build-skills-bundle.sh` ships an explicit
  14-name allowlist rather than globbing `~/.claude/skills`, so a personal skill
  added later can never be swept into a public download.
- **The build script is also the privacy gate.** It refuses to package if it finds
  absolute home paths, `Marc Brain` references or anything key-shaped, and it
  checks each `SKILL.md`'s `name` against its directory.
- **The cost:** the bundle is a snapshot, not a live mirror. Change a skill and
  nothing ships until you re-run the build script and redeploy.

To cut a new release: run the build script, eyeball `git diff` on the `*-dist/`
snapshot, then commit and push — Vercel deploys the rest.

```bash
bash scripts/build-skills-bundle.sh    # refresh skills-dist/ + public/ƒ/*.tar.gz|zip|VERSION
```

The `/ƒ` architecture diagram is generated from [`scripts/f-architecture.mmd`](scripts/f-architecture.mmd):

```bash
npx -y @mermaid-js/mermaid-cli@11 -i scripts/f-architecture.mmd -o public/ƒ/architecture.png -w 2400 -b '#F5F1EA'
```

Both pages are `noindex`, excluded from the sitemap ([`astro.config.ts`](astro.config.ts))
and disallowed in [`robots.txt`](src/pages/robots.txt.ts) — under both the literal
glyph and its percent-encoded form. They're shared by link, not by search.

## License

Content © Mark Ellington. Theme under MIT (see [LICENSE](LICENSE)).

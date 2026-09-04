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

### Windows must stay ASCII

`public/f/` and `public/omega/` are byte-identical ASCII mirrors of the glyph
directories, and the build scripts keep them in sync. The Windows install command
points at those, not at `/ƒ` or `/ø`, because three separate things break otherwise:

1. A Windows console on a legacy code page mangles a pasted `ƒ`/`ø` before .NET
   ever sees the URL.
2. Vercel serves an unknown extension as `application/octet-stream`, so
   `Invoke-RestMethod` hands `iex` a byte array instead of a string.
   [`vercel.json`](vercel.json) forces `text/plain; charset=utf-8` on `.ps1`/`.sh`.
3. Without that charset, PowerShell 5.1 latin-1-decodes the response, corrupting
   any non-ASCII byte in the script — including a glyph inside `$BaseUrl`.

So every `install.ps1` is pure ASCII and every installer's base URL is the ASCII
path. Both build scripts fail hard if a non-ASCII byte creeps into an `install.ps1`.

## Research posts

The MØBIUS work is published as it happens: one post per version slice, filed under the
**Research** category, with a Chinese counterpart. The running hub is [`/mobius`](https://marcyy.me/mobius),
whose version log is data — [`src/data/mobius/versions.ts`](src/data/mobius/versions.ts) — so a new
version is an appended entry rather than an edited page. The hub keeps one URL for the life of the
project; the posts are the part that multiplies.

Publishing one slice:

1. `src/data/blog/mobius-v<N>-<claim-slug>.md` — `category: "research"`, `tags: ["MØBIUS", "Research", …]`.
   The title is the version's own claim; the description is what prompted it, in one sentence.
2. `src/data/blog/mobius-v<N>-<claim-slug>.zh.md` — the Chinese counterpart. It needs all three of
   `lang: "zh"`, `slug: "<basename>.zh"` and the `.zh.md` filename, or it silently detaches from its
   original. Note that every listing on this site enumerates English posts only, so a Chinese post
   without an English original appears in no index at all.
3. Figures, if the slice has a shape worth drawing (below).
4. An entry in `src/data/mobius/versions.ts`.
5. Push to `main`. Then record the live URL in the MØBIUS repo's `docs/architecture/PUBLICATION.md`,
   whose test goes red for any version plan with no post.

### Figures

Diagram sources live in [`scripts/research/`](scripts/research) as plain Mermaid, and render to
`public/research/` as a light/dark SVG pair:

```bash
scripts/render-figures.sh                        # everything
scripts/render-figures.sh mobius-suspended-run   # one, by name
```

The `.mmd` files carry **no** `%%{init}%%` block — the palette is in `theme-light.json` /
`theme-dark.json` beside them, so one source renders both variants and a palette change is one edit
rather than one per diagram. The script refuses a source that themes itself. Backgrounds are
transparent; the page ground shows through in either theme.

Embed the pair, and let CSS pick (the rule is at the end of [`src/styles/global.css`](src/styles/global.css)):

```html
<img class="fig-light" src="/research/mobius-suspended-run.svg" alt="…" />
<img class="fig-dark"  src="/research/mobius-suspended-run-dark.svg" alt="" aria-hidden="true" />
```

## License

Content © Mark Ellington. Theme under MIT (see [LICENSE](LICENSE)).

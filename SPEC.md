# marce.me - Personal Blog Website Specification

## 1. Project Overview

- **Project name**: marce.me
- **Type**: Personal blog website (static site)
- **Core functionality**: A minimalist blog with personal introduction, article listings, and about page
- **Target users**: Readers interested in the author's thoughts and writing

## 2. Technology Stack

- **Framework**: Astro 5.x
- **Styling**: Tailwind CSS
- **UI**: React (for interactive components)
- **Language**: TypeScript
- **Deployment**: Vercel-ready

## 3. UI/UX Specification

### Layout Structure

- **Header**: Site logo/name, navigation links (Blog, About)
- **Main content**: Blog posts list or page content
- **Footer**: Copyright, social links

### Responsive Breakpoints
- Mobile: < 640px
- Tablet: 640px - 1024px
- Desktop: > 1024px

### Visual Design

**Color Palette (Light Mode)**
- Background: `#fafafa`
- Text primary: `#171717`
- Text secondary: `#737373`
- Accent: `#2563eb` (blue)
- Border: `#e5e5e5`

**Color Palette (Dark Mode)**
- Background: `#0a0a0a`
- Text primary: `#ededed`
- Text secondary: `#a3a3a3`
- Accent: `#3b82f6` (blue)
- Border: `#262626`

**Typography**
- Headings: System font (San Francisco on macOS)
- Body: System font
- Code: JetBrains Mono, monospace
- Base size: 16px
- Line height: 1.75

### Components

1. **Header**
   - Site title/name (left)
   - Navigation: Blog, About (right)
   - Theme toggle button

2. **Blog Post Card**
   - Title (link)
   - Date
   - Excerpt (optional)
   - Tags (optional)

3. **Blog Post Page**
   - Title
   - Date
   - Content (Markdown rendered)
   - Back link

4. **Footer**
   - Copyright text
   - Social links (GitHub, Twitter/X, Email)

## 4. Page Structure

### Pages
1. **Home** (`/`) - Blog posts listing, latest posts
2. **Blog** (`/blog`) - All blog posts (by year)
3. **Blog Post** (`/blog/[slug]`) - Individual post
4. **About** (`/about`) - About the author

### Blog Post Organization
- Posts stored in `src/content/blog/`
- Filename format: `YYYY-MM-DD-title.md`
- Frontmatter: title, date, description, tags

## 5. Functionality

### Core Features
- [x] Static site generation
- [x] Blog post listing (sorted by date, newest first)
- [x] Blog post individual pages
- [x] Markdown content rendering
- [x] Dark/Light mode toggle
- [x] Responsive design
- [x] SEO meta tags

### Data Handling
- Content Collections API (Astro)
- Markdown frontmatter for post metadata

## 6. Acceptance Criteria

- [ ] Home page shows list of recent blog posts
- [ ] Each post is clickable and shows full content
- [ ] Dark/Light mode toggle works
- [ ] Site is responsive on mobile/tablet/desktop
- [ ] About page shows author information
- [ ] No build errors
- [ ] No console errors on page load
---
layout: ../layouts/AboutLayout.astro
title: "About"
---

<div class="flex flex-col md:flex-row gap-8 items-start md:items-stretch">
  <div class="w-full md:w-auto md:flex-shrink-0 md:max-w-[281px]">
    <img src="/about-profile.jpg" alt="Marc Ellington" class="w-full h-auto md:h-full object-cover rounded-lg" />
  </div>
  <div class="flex-1 min-w-0">
    <p>Yoo! I'm Marc</p>
    <p>You can call me Silicon Life Nutrition Guru, or more simply — Vibe Coder.</p>
    <p>My daily life is a seamless switch between full-stack developer and full-time tourist:</p>
    <ul>
      <li>Work Mode: Listening to Lo-Fi music, staring at the screen until that feeling of "this code is actually fire" hits, then bang out some bug-free logic.</li>
      <li>Life Mode: Dragging my suitcase around Changsha, pretending "Do Not Lean" at Yuelu Mountain. For me, a good meal or a cool photo isn't for flex — it's to recharge my brain and keep that Vibe alive.</li>
    </ul>
    <p>I don't grind, and I don't slack. I'm just finding the best resonant frequency between code and life.</p>
    <p>Nice to meet you. Hope we can vibe together.</p>
  </div>
</div>

## Stay Connected

<div class="bg-muted/30 border border-accent rounded-lg p-6 my-8">
  <p class="mt-0 mb-4 text-sm text-foreground/70">
    New posts, shipping stories, and nerdy links straight to your inbox.
  </p>
  <!--email_off-->
  <div class="flex flex-col gap-3 sm:flex-row sm:items-center sm:gap-4">
    <a href="mailto:mangiapanejohn@icloud.com?subject=Subscribe%20to%20marc.me&body=Hi%20Marc%2C%0A%0APlease%20add%20me%20to%20your%20list.%0A%0A" class="sub-cta inline-block rounded-md bg-accent-text px-6 py-2 text-center font-medium whitespace-nowrap text-background no-underline transition-colors hover:bg-accent-text/90 hover:text-background">Email me to subscribe</a>
    <p class="m-0 text-sm text-foreground/70">
      or write to <span class="font-medium text-foreground">mangiapanejohn@icloud.com</span>
      <button type="button" data-copy="mangiapanejohn@icloud.com" data-copied="Copied" aria-live="polite" class="ms-1 rounded border border-border px-2 py-0.5 text-xs text-foreground/80 transition-colors hover:border-accent hover:text-accent-text">Copy</button>
    </p>
  </div>
  <!--/email_off-->
  <p class="mt-3 mb-0 text-xs text-foreground/65">
    2× per month, pure signal, zero fluff.
  </p>
</div>

## Connect

If you'd like to connect or have questions about my work, feel free to reach out through any of the links below.

<script>
  // Copy the address for readers without a mail app set up. Bound once on the document: this inline
  // script runs again after every view-transition navigation.
  (() => {
    if (window.__copyBound) return;
    window.__copyBound = true;
    document.addEventListener("click", async event => {
      const button = event.target.closest && event.target.closest("button[data-copy]");
      if (!button) return;
      try {
        await navigator.clipboard.writeText(button.dataset.copy);
      } catch (e) {
        return;
      }
      const label = button.textContent;
      button.textContent = button.dataset.copied;
      setTimeout(() => (button.textContent = label), 1600);
    });
  })();
</script>

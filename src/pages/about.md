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
  <p class="text-sm text-foreground/70 mb-4">
    New posts, shipping stories, and nerdy links straight to your inbox.
  </p>
  <form action="/api/subscribe" method="post" data-subscribe class="flex flex-col sm:flex-row gap-3">
    <input type="hidden" name="lang" value="en" />
    <input type="text" name="website" tabindex="-1" autocomplete="off" aria-hidden="true" class="hidden" />
    <input type="text" name="name" autocomplete="name" maxlength="100" aria-label="Name" placeholder="Your Name" class="min-w-0 flex-1 px-4 py-2 border border-border rounded-md bg-background text-foreground placeholder-foreground/65 focus:outline-none focus:ring-2 focus:ring-accent focus:border-transparent" />
    <input type="email" name="email" autocomplete="email" required aria-label="Email" placeholder="Your Email" class="min-w-0 flex-1 px-4 py-2 border border-border rounded-md bg-background text-foreground placeholder-foreground/65 focus:outline-none focus:ring-2 focus:ring-accent focus:border-transparent" />
    <button type="submit" data-busy="Sending…" class="px-6 py-2 bg-accent-text hover:bg-accent-text/90 disabled:opacity-60 disabled:cursor-wait rounded-md transition-colors font-medium whitespace-nowrap text-background">
      Subscribe
    </button>
  </form>
  <p class="sub-status" role="status" aria-live="polite" hidden data-ok="Got it — thanks! I'll be in touch." data-invalid="That email doesn't look right." data-failed="Couldn't send that. Try again, or write to mangiapanejohn@icloud.com."></p>
  <p id="subscribed" class="sub-anchor sub-ok">Got it — thanks! I'll be in touch.</p>
  <p id="subscribe-failed" class="sub-anchor">Couldn't send that. Try again, or write to mangiapanejohn@icloud.com.</p>
  <p class="text-xs text-foreground/65 mt-3">
    2× per month, pure signal, zero fluff.
  </p>
</div>

## Connect

If you'd like to connect or have questions about my work, feel free to reach out through any of the links below.

<style>
  .sub-status,
  .sub-anchor {
    margin-top: 0.75rem;
    font-size: 0.875rem;
  }
  .sub-status[data-state="ok"],
  .sub-ok {
    color: var(--accent-text);
    font-weight: 600;
  }
  /* Without JavaScript the form posts, and the server sends the reader back to one of these. */
  .sub-anchor {
    display: none;
  }
  .sub-anchor:target {
    display: block;
  }
</style>

<script>
  // Post the form in place and say how it went, instead of leaving the page. Bound once on the
  // document: this inline script runs again after every view-transition navigation.
  (() => {
    if (window.__subscribeBound) return;
    window.__subscribeBound = true;
    document.addEventListener("submit", async event => {
      const form = event.target.closest && event.target.closest("form[data-subscribe]");
      if (!form) return;
      event.preventDefault();
      const button = form.querySelector("button[type=submit]");
      const status = form.parentElement.querySelector(".sub-status");
      const label = button.textContent;
      button.disabled = true;
      button.textContent = button.dataset.busy;
      let result = { ok: false, error: "failed" };
      try {
        const res = await fetch(form.action, {
          method: "POST",
          body: new FormData(form),
          headers: { Accept: "application/json" },
        });
        result = await res.json();
      } catch (e) {}
      status.hidden = false;
      status.dataset.state = result.ok ? "ok" : "error";
      status.textContent = result.ok
        ? status.dataset.ok
        : result.error === "invalid"
          ? status.dataset.invalid
          : status.dataset.failed;
      button.disabled = false;
      button.textContent = label;
      if (result.ok) form.reset();
    });
  })();
</script>

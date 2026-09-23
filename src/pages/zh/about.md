---
layout: ../../layouts/AboutLayout.astro
title: "关于"
---

<div class="flex flex-col md:flex-row gap-8 items-start md:items-stretch">
  <div class="w-full md:w-auto md:flex-shrink-0 md:max-w-[281px]">
    <img src="/about-profile.jpg" alt="Marc Ellington" class="w-full h-auto md:h-full object-cover rounded-lg" />
  </div>
  <div class="flex-1 min-w-0">
    <p>嗨!我是 Marc。</p>
    <p>你可以叫我「硅基生命营养师」,或者更简单点 —— Vibe Coder。</p>
    <p>我的日常就是在全栈开发者和全职旅行者之间无缝切换:</p>
    <ul>
      <li>工作模式:放着 Lo-Fi,盯着屏幕,直到「这段代码是真的顶」的感觉冒出来,然后敲出一段没有 bug 的逻辑。</li>
      <li>生活模式:拖着行李箱在长沙乱逛,在岳麓山假装「禁止倚靠」。对我来说,一顿好饭、一张好照片不是为了炫,而是给大脑充电,让那股 Vibe 一直在线。</li>
    </ul>
    <p>我不卷,也不躺。我只是在代码和生活之间,寻找最舒服的共振频率。</p>
    <p>很高兴认识你,希望我们能一起 vibe。</p>
  </div>
</div>

## 保持联系

<div class="bg-muted/30 border border-accent rounded-lg p-6 my-8">
  <p class="text-sm text-foreground/70 mb-4">
    新文章、上线故事和有意思的链接,直接发到你的邮箱。
  </p>
  <form action="/api/subscribe" method="post" data-subscribe class="flex flex-col sm:flex-row gap-3">
    <input type="hidden" name="lang" value="zh" />
    <input type="text" name="website" tabindex="-1" autocomplete="off" aria-hidden="true" class="hidden" />
    <input type="text" name="name" autocomplete="name" maxlength="100" aria-label="名字" placeholder="你的名字" class="min-w-0 flex-1 px-4 py-2 border border-border rounded-md bg-background text-foreground placeholder-foreground/65 focus:outline-none focus:ring-2 focus:ring-accent focus:border-transparent" />
    <input type="email" name="email" autocomplete="email" required aria-label="邮箱" placeholder="你的邮箱" class="min-w-0 flex-1 px-4 py-2 border border-border rounded-md bg-background text-foreground placeholder-foreground/65 focus:outline-none focus:ring-2 focus:ring-accent focus:border-transparent" />
    <button type="submit" data-busy="发送中…" class="px-6 py-2 bg-accent-text hover:bg-accent-text/90 disabled:opacity-60 disabled:cursor-wait rounded-md transition-colors font-medium whitespace-nowrap text-background">
      订阅
    </button>
  </form>
  <p class="sub-status" role="status" aria-live="polite" hidden data-ok="收到啦，谢谢！我会联系你。" data-invalid="这个邮箱格式好像不对。" data-failed="没发出去，再试一次，或者直接写信到 mangiapanejohn@icloud.com。"></p>
  <p id="subscribed" class="sub-anchor sub-ok">收到啦，谢谢！我会联系你。</p>
  <p id="subscribe-failed" class="sub-anchor">没发出去，再试一次，或者直接写信到 mangiapanejohn@icloud.com。</p>
  <p class="text-xs text-foreground/65 mt-3">
    每月两封,纯干货,不灌水。
  </p>
</div>

## 联系我

如果你想交流,或者对我的项目有任何问题,欢迎通过下面任意一个链接找我。

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

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
  <p class="mt-0 mb-4 text-sm text-foreground/70">
    新文章、上线故事和有意思的链接,直接发到你的邮箱。
  </p>
  <div class="flex flex-col gap-3 sm:flex-row sm:items-center sm:gap-4">
    <a href="mailto:mangiapanejohn@icloud.com?subject=%E8%AE%A2%E9%98%85%20marc.me&body=Marc%20%E4%BD%A0%E5%A5%BD%EF%BC%8C%0A%0A%E6%83%B3%E8%AE%A2%E9%98%85%E4%BD%A0%E7%9A%84%E6%9B%B4%E6%96%B0%E3%80%82%0A%0A" class="sub-cta inline-block rounded-md bg-accent-text px-6 py-2 text-center font-medium whitespace-nowrap text-background no-underline transition-colors hover:bg-accent-text/90 hover:text-background">发邮件订阅</a>
    <p class="m-0 text-sm text-foreground/70">
      或者直接写信到 <span class="font-medium text-foreground">mangiapanejohn@icloud.com</span>
      <button type="button" data-copy="mangiapanejohn@icloud.com" data-copied="已复制" aria-live="polite" class="ms-1 rounded border border-border px-2 py-0.5 text-xs text-foreground/80 transition-colors hover:border-accent hover:text-accent-text">复制</button>
    </p>
  </div>
  <p class="mt-3 mb-0 text-xs text-foreground/65">
    每月两封,纯干货,不灌水。
  </p>
</div>

## 联系我

如果你想交流,或者对我的项目有任何问题,欢迎通过下面任意一个链接找我。

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

# marc.me 设计规范

这份文件记录网站现在的样子和背后的决定。以后改 UI 先读它；改动了设计，就回来更新它。
`SPEC.md` 是项目最早的规划，已经过时（蓝色主色、React、`/blog` 路由都不是现状），以本文件为准。

## 定位

两类读者并重：看 MØBIUS 研究记录的工程师/研究者，和关注 Marc 本人的朋友。
所以首页保留个人自述和玩笑语气，研究内容有独立入口（Research ▸ Log / Papers / MØBIUS）。

**保留、不要再提议去掉的东西**：全站等宽字体、首页那段长自述、`@marcE` 无限循环的打字动画。
这些是站点的个性，修 bug 和无障碍时绕着它们做，不删它们。

**试过并被否掉的**：首页 Featured Projects 卡片区（删了）、目录里贯穿整行的分隔线（太重）、
1.25rem 的短分隔（太短）、进度线小圈里写章节号、当前章节旁边写标题文字、emoji 式图标。

## 颜色

定义在 `src/styles/global.css`，一律用变量，不写死色值。

| Token | 浅色 | 深色 | 用途 |
|---|---|---|---|
| `--background` | `#f0eee6` | `#30302b` | 页面底色 |
| `--foreground` | `#262521` | `#edebe3` | 正文 |
| `--accent` | `#d97757` | `#e08a6b` | 珊瑚色：图标、下划线、边框、进度线等**装饰** |
| `--accent-text` | `#a84d2c` | `#e08a6b` | 主色**做文字**时用（浅色下 4.8:1） |
| `--muted` / `--border` | `#e7e3d7` / `#e0dcce` | `#3b3a34` / `#47463f` | 浅底块、分隔 |

- 文字要主色时用 `text-accent-text` 或 `var(--accent-text)`，不要用 `text-accent`：珊瑚色在浅色底上只有 2.7:1。
- 次要文字的透明度不低于 0.65（约 4.5:1）；更淡的只给不需要读的装饰。

## 字体

Google Sans Code，全站等宽，包括长文正文。长文的可读性靠行高、段距、目录和进度来补，不换字体。

## 布局

- 正文列 `max-w-3xl`（48rem），居中。
- **长文（≥4 个 h2）在 ≥1280px 时整体右移 `--post-shift: 4rem`**。原因：左边目录是一整块文字、右边只有一条细线，
  严格居中的正文看起来偏左。移动写在 `PostDetails.astro` 的 `.post-shift`。
- 两侧的目录和进度都贴着**窗口边缘**（离边 1.5rem），不是贴着正文列。它们的定位公式里减/加了 `--post-shift`，
  所以正文怎么挪它们都不动：
  - 左：`inset-inline-start: calc(1.5rem - (100vw - 48rem) / 2 - 1rem - var(--post-shift, 0rem))`
  - 右：`inset-inline-end: calc(1.5rem - (100vw - 48rem) / 2 - 1rem + var(--post-shift, 0rem))`
- 顶部导航整行约需 500px（在站名旁边），所以 **<768px 用汉堡菜单**，≥768px 才展开成一行；
  导航项间距 8px，整行不超出正文列。
- 任何宽度都不能出现横向滚动。加了位移/绝对定位的东西要在 375px 和 1280px 下检查 `scrollWidth`。

## 长文阅读：目录（左）

`src/components/TableOfContents.astro`

- 只在文章有 ≥4 个 h2 时出现。<1280px 折叠在标题下，≥1280px 固定在窗口左边并跟随滚动。
- 标题里的编号（"2 · Completion judgement"）拆成单独一列（2.1em 宽，放得下"十一"这样的两个汉字），标题折行时对齐自己。
- 条目之间是一条 **5rem 的短线**，从标题起点开始。
- 当前章节：文字变 `--accent-text`，编号加粗。不用底色块，不用侧边竖条。
- "当前章节"的判定线是屏幕上方 **1/4** 处。目录和进度条用同一条线，并且都监听文章高度变化
  （懒加载图片会把标题往下推，却不触发滚动事件），两者永远一致。

## 长文阅读：手绘进度（右）

`src/components/ReadingProgress.astro` + `src/components/doodles.ts`

- 一条手绘感的竖线（带种子的轻微抖动，同一篇每次构建都一样），读到哪里用珊瑚色描到哪里。
- 每节一个一笔画的小圈（首尾略微交叠，像手画的）：未读空心、已读浅珊瑚、当前实心并放大。**圈里不写数字。**
- 小圈之间至少 24px；填充线按同样的映射分段换算，所以填充总是正好停在当前小圈上。
- 当前小圈左边显示该节的**手绘小动画**，读这一节时循环播放。**旁边不写文字。**
- 底部：百分比 + 大约剩余分钟（英文按 220 词/分钟，中文按 400 字/分钟，混排两者相加）。
- 读完（进度 ≥99%，或滚到页面最底）：换成"加油"动画（手绘星星 + 一圈迸发的短线），
  文字"读完啦，加油！"/"Read it all. Onward!"。

### 手绘小动画的规则

每个图标都在 `doodles.ts` 里，动作写在 `ReadingProgress.astro` 的全局样式 `.rp-doodle` 下。

- **画法**：48×48 的 viewBox，只用线条；描边 1.9、圆头圆角；路径故意画得略不规整（手绘感）。
- **两种墨色**：`ink`（前景色 72%，不动的部分）和 `hot`（珊瑚色，会动的部分）；实心小点用 `hot-fill`。
  深色模式自动跟随，不需要单独画一版。
- **一个图标只做一个动作**，幅度小、节奏慢（1.4–4s 一轮），缓动用 ease-out / ease-in-out，不弹跳。
- 整个图标还有一层 0.3px 级的"抖动"（`d-boil`，steps 动画），模仿手绘动画里线条的颤动。
- **不用 emoji，不用品牌 logo**（包括 Claude 的星芒标志）。风格参考"暖色、克制的手绘线稿"，不是照搬某个品牌。
- `prefers-reduced-motion: reduce` 时所有动作停止，需要"画出来"的线条直接显示完整状态。

### 同一篇文章里不重复

`assignDoodles()` 给每节挑一个：

1. 按章节标题里的关键词匹配规则（中英文都有），越具体的规则排越前（否定/判定/见证在前，泛泛的"系统"在后）。
2. 最佳匹配已经被本文用过，就用它的下一个匹配。
3. 都用过了，就从图标池里挑一个没用过的；挑选顺序由本文所有标题算出的种子决定，
   所以**不同文章的组合不同，同一篇每次构建一样**。
4. 章节多于图标池（现在 16 个）时才允许重复。

现有图标和动作：

| 图标 | 动作 | 典型关键词 |
|---|---|---|
| 叉 cross | 两笔依次画出 | kill, negative, 否定 |
| 天平 scale | 横梁左右摆 | judge, 判 |
| 眼睛 eye | 左右看、偶尔眨眼 | witness, 见证 |
| 放大镜 magnifier | 小范围绕圈 | probe, search, 文献 |
| 仪表 gauge | 指针回摆 | instrument, measure |
| 闸门 gate | 横杆抬起放下 | gate, reduction |
| 勾 check | 一笔画出 | approval, 批准 |
| 笔 pen | 写出波浪线 | attribution, author |
| 幼苗 seedling | 生长、叶子摆 | changed, learn |
| 旗子 flag | 飘动 | where, status |
| 问号 question | 上下浮动，点在闪 | coda, thesis, 问题 |
| 灯泡 lightbulb | 光线明灭 | lesson, why, 启发 |
| 指南针 compass | 指针摆动 | method, next, 方向 |
| 沙漏 hourglass | 定时翻转 | day, time, 历史（整词匹配） |
| 书 book | 翻页 | journal, record, 笔记 |
| 齿轮 gear | 慢转 | runtime, system |
| 星星迸发 cheer | 弹出 + 一圈短线散开 | 仅用于读完 |

### 加一个新图标

1. 在 `doodles.ts` 的 `DoodleName`、`doodles`、`pool` 里加上，按上面的画法画。
2. 需要的话在 `rules` 里加关键词（注意整词匹配，别让 "runtime" 命中 "time" 这种情况）。
3. 在 `ReadingProgress.astro` 的全局样式里加它的动作类和 `@keyframes`，并确认 reduced-motion 下是静止的。
4. 用几篇长文检查：同一篇里不重复、深浅两种主题都清楚。

## 交互与无障碍

- 首页 Blog/Research 是标准 tablist（方向键切换）；"Read more"带 `aria-expanded`。
- 手机菜单是浮层：Esc、点外部都能关；文案都走 `src/i18n/ui.ts`。
- 搜索：头部图标或 ⌘K / Ctrl+K 打开弹层（Pagefind，首次打开才加载）；没 JS 时图标仍链接到 `/search`。
- About 页"保持联系"：访客用自己设备上的邮箱给 Marc 发信。按钮打开预填好主题和正文的 `mailto:`，
  旁边显示地址并可一键复制（照顾没配置邮件应用的电脑）。**不接第三方邮件服务**（试过 Resend，Marc 不要）；
  也不要用 `<form action="mailto:">`，那种写法在很多浏览器里点了没反应。
- 所有动画都要有 reduced-motion 的替代。

## 性能

- Service Worker 只预缓存外壳（css/js/字体，约 1.4MB），图片第一次看到时再缓存。不要把图片加回 `globPatterns`。
- 新图片放进 `public/` 前先压缩：截图宽度 ≤2000px，照片 JPEG 质量 ~82；架构图保持原分辨率只做无损/调色板压缩。

## 工作方式

- 改动在分支上做，每个阶段一个提交，都要过 `npm run build`（0 错误 0 警告）并在浏览器里看过桌面和手机两种宽度。
- 推到 `main` 就会触发 Vercel 部署上线，push 前要 Marc 确认。

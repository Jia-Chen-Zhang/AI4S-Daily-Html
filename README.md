# AI4S 每日研判 · 公开静态站

AI4S 每日资讯报告的公开归档站点，纯静态（Vue 3 + Vite + Tailwind），托管于 GitHub Pages。
数据来自主系统（ai-daily）每日生成的报告，经 `scripts/export.py` 导出为 JSON 随仓库提交。

**隐私边界**：仅包含公开报告内容（总览 / 今日洞察 / 问题发现 / 今日热点 / Hacker News）。
「与当前工作的相关性」板块与工作文档**不导出**，只保留在本机完整版中。

## 首次部署到 GitHub Pages

```bash
cd gitweb
git init -b main
git add -A
git commit -m "初始提交: AI4S 每日研判静态站"
git remote add origin git@github.com:<你的用户名>/<仓库名>.git
git push -u origin main
```

然后到仓库 **Settings → Pages → Build and deployment → Source 选 "GitHub Actions"**。
之后每次 push 到 main，Actions 会自动构建并部署，地址为
`https://<你的用户名>.github.io/<仓库名>/`。

> 注意：GitHub Pages 免费版要求仓库 **public**，且站点本身全网公开——请勿把任何内部内容放入 `public/data/`。

## 每日更新（在主仓库 ai-daily 中）

报告推送完成后执行：

```bash
./gitweb/scripts/publish.sh           # 导出 + 提交 + 推送,一步到位
```

可加入主系统的 push job 之后（cron / systemd `ExecStartPost`），实现每日自动发布。

## 本地开发

```bash
# 更新数据(在主仓库根目录,使用其 venv 的 pyyaml)
uv run python gitweb/scripts/export.py

cd gitweb
npm ci
npm run dev      # 开发预览(数据已导出到 public/data,无需后端)
npm run build    # 构建到 dist/
```

## 目录结构

```
├── src/                    # Vue 3 前端(归档列表 / 报告详情 / 五个栏目流)
├── public/data/            # 导出的静态 JSON(提交到仓库)
│   ├── reports.json        #   报告摘要列表
│   ├── details/{id}.json   #   报告详情(板块数组,已剔除 relevance)
│   └── sections/{key}.json #   栏目流(overview/insights/gaps/rss/hackernews)
├── scripts/export.py       # news-data → public/data 导出(自包含,仅依赖 pyyaml)
├── scripts/publish.sh      # 导出 + git commit + push
└── .github/workflows/      # Pages 自动构建部署
```

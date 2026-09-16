# ConnerQiu.github.io
Personal Page of Ronghe QIU

## 维护入口

本仓库是网站唯一的后续维护目录。网站从 `ronghe-website` 迁移而来，保留四页结构和全部样式、照片与论文配图。

- `content/site.json`：个人简介、论文、News、经历、证书及照片信息。
- `build.py`：生成四个页面，仅需 Python 3，无第三方依赖。
- `assets/styles.css`：网站样式，直接在此修改。
- `assets/images/`：网站使用的图片。
- `index.html`、`resume.html`、`beyond.html`、`contact.html`：生成后的页面，放在根目录以支持 GitHub Pages。
- `robots.txt`、`sitemap.xml`：构建时生成的搜索引擎抓取规则与四页站点地图。

修改内容或页面结构后，在本仓库执行：

```sh
python3 build.py
```

不要直接修改生成的 HTML；下一次生成会覆盖它们。样式和图片不会被生成器覆盖。

## 本地预览

```sh
python3 -m http.server 4173 --bind 127.0.0.1
```

浏览器访问 http://127.0.0.1:4173/ 。

## GitHub Pages 发布

1. 正式发布前，将 `content/site.json` 的 `draft` 改为 `false` 并重新生成页面，以移除搜索引擎屏蔽标记。
2. 将本仓库的内容及生成页面提交、推送到 GitHub。
3. 在 GitHub 的 Settings → Pages 中选择 Deploy from a branch，选择 `main` 分支和 `/ (root)`。
4. 发布成功后访问 https://connerqiu.github.io/ 。`.nojekyll` 让 GitHub 直接使用现成页面。

当前已设为正式发布模式（`draft: false`），页面包含规范网址，允许搜索引擎抓取。每次更新内容后，重新生成页面并提交、推送即可更新网站。

## Google 收录

1. 网站上线后，打开 Google Search Console（https://search.google.com/search-console/）。
2. 添加网址前缀资源 `https://connerqiu.github.io/`，选择 HTML 文件验证；将 Google 提供的验证文件放在仓库根目录，提交并推送，待部署完成后点击验证。保留验证文件。
3. 在“站点地图”中提交 `sitemap.xml`。
4. 在“网址检查”中输入首页完整网址，测试实际网址并请求编入索引。其余三页也可分别申请。

允许抓取和提交站点地图不保证 Google 收录或排名；可在 Search Console 查看实际索引状态。

## 本地资料与反馈

原始简历、设计草稿和历史反馈留在仓库外的原项目目录。原来的 Research.md、Resume.md、Beyond research.md、Contact.md 仍可用于本地反馈，之后的修改落实到本仓库。

本仓库仅包含可公开的网站内容和维护文件。不要将原始简历、未公开资料或历史反馈复制到公开仓库。

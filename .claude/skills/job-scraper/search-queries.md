# Search Queries for Job Scraper

<!-- SETUP: Customize these queries based on your skills, target roles, and location -->

## Search Sites

Primary (Chinese job market):
- **zhipin.com** - BOSS 直聘（最大互联网招聘平台，反爬强，优先用 WebSearch 标题+摘要）
- **lagou.com** - 拉勾（互联网岗位集中）
- **liepin.com** - 猎聘（中高端岗位）
- **zhaopin.com** - 智联招聘（综合招聘）
- **51job.com** - 前程无忧（综合招聘）

Secondary:
- **linkedin.com/jobs** - 领英（外企/出海岗位）
- Direct Google/Bing searches with `site:` filters for known target companies

## Query Categories

Queries are grouped by priority. Each query should be combined with your location terms (e.g. "北京", "上海", "深圳", "杭州") where the site supports it.

### Priority 1: [YOUR_PRIMARY_ROLE_TYPE]

These match your strongest and most desired career direction.

```
site:zhipin.com "[YOUR_PRIMARY_JOB_TITLE]" [YOUR_CITY]
site:lagou.com "[YOUR_PRIMARY_JOB_TITLE]" [YOUR_CITY]
site:liepin.com "[YOUR_PRIMARY_JOB_TITLE]" [YOUR_CITY]
site:linkedin.com/jobs "[YOUR_PRIMARY_JOB_TITLE]" [YOUR_COUNTRY]
```

### Priority 2: [YOUR_DOMAIN_EXPERTISE]

These match your domain expertise.

```
site:zhipin.com [YOUR_DOMAIN_KEYWORD_1] [YOUR_CITY]
site:lagou.com [YOUR_DOMAIN_KEYWORD_2] [YOUR_CITY]
site:liepin.com [YOUR_DOMAIN_KEYWORD_1] [YOUR_CITY]
```

### Priority 3: [YOUR_ADJACENT_ROLE_TYPE]

Adjacent roles you could pivot into.

```
site:zhipin.com "[YOUR_ADJACENT_TITLE_1]" [YOUR_KEY_SKILL] [YOUR_CITY]
site:lagou.com "[YOUR_ADJACENT_TITLE_2]" [YOUR_KEY_SKILL] [YOUR_CITY]
```

### Priority 4: Broader Technical Roles

Wider net for general technical roles.

```
site:zhipin.com [YOUR_KEY_SKILL] 开发 [YOUR_CITY]
site:lagou.com [YOUR_KEY_SKILL] 工程师 [YOUR_CITY]
site:liepin.com [YOUR_KEY_SKILL] 架构师 [YOUR_CITY]
```

## Location Filter

When evaluating results, verify the job location is within reasonable commute distance from your home. Define acceptable areas:
- [YOUR_CITY] 及周边
- [ACCEPTABLE_AREA_1]
- [ACCEPTABLE_AREA_2]
- [BORDERLINE_AREA]（borderline - 通勤约 X 分钟）
- [TOO_FAR_AREA]（too far）

## Date Filter

Only include jobs posted within the last 14 days, or with an application deadline that has not yet passed. If a posting date cannot be determined, include it but flag as "date unknown".

## Adapting Queries

If the user specifies a focus area, select queries from the matching category and also generate 2-3 custom queries for that focus. For example:
- "/scrape [focus_area]" -> relevant category queries + custom focus-specific queries

## Note on Chinese Portals

BOSS 直聘、拉勾、猎聘等平台对自动化访问限制较严。`/scrape` 默认使用 WebSearch 获取职位标题和摘要；如需完整职位描述，建议用户复制链接或职位描述后使用 `/apply <链接>` 或 `/apply <粘贴描述>`。

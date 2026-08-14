/** 栏目(板块)共享配置:侧边栏导航 / 卡片徽章 / 栏目页标题统一从这里取 */

export interface SectionNavItem {
  key: string
  label: string // 侧边栏全名
  short: string // 卡片徽章短名
  icon: string
}

export const SECTIONS: SectionNavItem[] = [
  { key: 'overview', label: '总览', short: '总览', icon: '📋' },
  { key: 'insights', label: '今日洞察', short: '洞察', icon: '💡' },
  { key: 'gaps', label: '问题发现', short: '问题发现', icon: '🔬' },
  { key: 'rss', label: '今日热点', short: 'Top热点', icon: '📰' },
  { key: 'hackernews', label: 'Hacker News 热议', short: 'HN', icon: '🟧' },
]

export const SECTION_SHORT: Record<string, string> = Object.fromEntries(
  SECTIONS.map((s) => [s.key, s.short]),
)

export const SECTION_LABEL: Record<string, string> = Object.fromEntries(
  SECTIONS.map((s) => [s.key, s.label]),
)

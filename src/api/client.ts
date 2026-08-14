import type { ReportDetail, ReportSummary, SectionEntry } from '../types'

// 静态数据源:GitHub Pages 无后端,直接读构建时导出的 JSON
// (由 scripts/export.py 生成到 public/data/,随仓库提交)
const BASE = 'data'

async function request<T>(path: string): Promise<T> {
  const resp = await fetch(`${BASE}/${path}`)
  if (!resp.ok) {
    throw new Error(`请求失败: ${resp.status}`)
  }
  return resp.json() as Promise<T>
}

export function listReports(): Promise<ReportSummary[]> {
  return request<ReportSummary[]>('reports.json')
}

export function getReport(id: string): Promise<ReportDetail> {
  return request<ReportDetail>(`details/${encodeURIComponent(id)}.json`)
}

// 栏目流 JSON 一次性导出全量,前端本地分页
const sectionCache = new Map<string, Promise<SectionEntry[]>>()

function loadSection(key: string): Promise<SectionEntry[]> {
  if (!sectionCache.has(key)) {
    sectionCache.set(key, request<SectionEntry[]>(`sections/${key}.json`))
  }
  return sectionCache.get(key)!
}

export async function getSectionStream(
  key: string,
  limit = 30,
  offset = 0,
): Promise<SectionEntry[]> {
  const all = await loadSection(key)
  return all.slice(offset, offset + limit)
}

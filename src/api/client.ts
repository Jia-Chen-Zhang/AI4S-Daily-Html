import type {
  ReportDetail,
  ReportSummary,
  SectionEntry,
  Settings,
  WorkDocContent,
  WorkDocMeta,
} from '../types'

const BASE = '/api'

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const resp = await fetch(`${BASE}${path}`, init)
  if (!resp.ok) {
    let detail = `请求失败: ${resp.status}`
    try {
      const body = await resp.json()
      if (body?.detail) detail = body.detail
    } catch {
      /* 非 JSON 错误体,用默认信息 */
    }
    throw new Error(detail)
  }
  if (resp.status === 204) return undefined as T
  return resp.json() as Promise<T>
}

export function listReports(): Promise<ReportSummary[]> {
  return request<ReportSummary[]>('/reports?limit=200')
}

export function getReport(id: string): Promise<ReportDetail> {
  return request<ReportDetail>(`/reports/${encodeURIComponent(id)}`)
}

export function getSectionStream(
  key: string,
  limit = 30,
  offset = 0,
): Promise<SectionEntry[]> {
  return request<SectionEntry[]>(`/sections/${key}?limit=${limit}&offset=${offset}`)
}

// ─── 当前工作维护 ───

export function listWorkDocs(): Promise<WorkDocMeta[]> {
  return request<WorkDocMeta[]>('/workdocs')
}

export function getWorkDoc(name: string): Promise<WorkDocContent> {
  return request<WorkDocContent>(`/workdocs/${encodeURIComponent(name)}`)
}

export function uploadWorkDoc(file: File): Promise<void> {
  return request<void>(`/workdocs/${encodeURIComponent(file.name)}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/octet-stream' },
    body: file,
  })
}

export function deleteWorkDoc(name: string): Promise<void> {
  return request<void>(`/workdocs/${encodeURIComponent(name)}`, {
    method: 'DELETE',
  })
}

// ─── 设置 ───

export function getSettings(): Promise<Settings> {
  return request<Settings>('/settings')
}

export function saveSettings(model: string): Promise<Settings> {
  return request<Settings>('/settings', {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ model }),
  })
}

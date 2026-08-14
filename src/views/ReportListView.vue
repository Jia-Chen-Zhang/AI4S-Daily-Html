<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { listReports } from '../api/client'
import type { ReportSummary } from '../types'
import ReportCard from '../components/ReportCard.vue'

const reports = ref<ReportSummary[]>([])
const loading = ref(true)
const error = ref('')

onMounted(async () => {
  try {
    reports.value = await listReports()
  } catch (e) {
    error.value = e instanceof Error ? e.message : '加载失败'
  } finally {
    loading.value = false
  }
})

// 按日期分组(报告本身已按时间倒序)
const grouped = computed(() => {
  const groups: { date: string; items: ReportSummary[] }[] = []
  for (const r of reports.value) {
    const last = groups[groups.length - 1]
    if (last && last.date === r.date) {
      last.items.push(r)
    } else {
      groups.push({ date: r.date, items: [r] })
    }
  }
  return groups
})

function fmtDate(date: string) {
  const [, m, d] = date.split('-')
  return { md: `${Number(m)}月${Number(d)}日`, year: date.slice(0, 4) }
}
</script>

<template>
  <div>
    <div v-if="loading" class="py-20 text-center text-sm text-stone-400">
      载入中…
    </div>
    <div v-else-if="error" class="py-20 text-center text-sm text-red-500">
      {{ error }}
    </div>
    <div
      v-else-if="!grouped.length"
      class="py-20 text-center text-sm text-stone-400"
    >
      暂无归档报告
    </div>

    <div v-else class="space-y-12">
      <section v-for="group in grouped" :key="group.date" class="relative">
        <!-- 日期大标 -->
        <div class="mb-5 flex items-baseline gap-3">
          <h2 class="font-serif text-3xl font-bold tabular-nums text-stone-900 dark:text-stone-50">
            {{ fmtDate(group.date).md }}
          </h2>
          <span class="text-sm tabular-nums text-stone-400">
            {{ fmtDate(group.date).year }}
          </span>
          <span class="text-xs text-stone-400">
            {{ group.items.length }} 期
          </span>
          <div class="ml-2 flex-1 border-t border-stone-200 dark:border-stone-800" />
        </div>

        <div class="grid gap-4 sm:grid-cols-2">
          <ReportCard
            v-for="report in group.items"
            :key="report.id"
            :report="report"
          />
        </div>
      </section>
    </div>
  </div>
</template>

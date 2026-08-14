<script setup lang="ts">
import { onMounted, ref } from 'vue'
import {
  deleteWorkDoc,
  getWorkDoc,
  listWorkDocs,
  uploadWorkDoc,
} from '../api/client'
import type { WorkDocContent, WorkDocMeta } from '../types'
import MarkdownBody from '../components/MarkdownBody.vue'

const docs = ref<WorkDocMeta[]>([])
const loading = ref(true)
const error = ref('')
const notice = ref('')

const opened = ref<WorkDocContent | null>(null)
const opening = ref(false)
const uploading = ref(false)
const fileInput = ref<HTMLInputElement | null>(null)

async function reload() {
  loading.value = true
  error.value = ''
  try {
    docs.value = await listWorkDocs()
  } catch (e) {
    error.value = e instanceof Error ? e.message : '加载失败'
  } finally {
    loading.value = false
  }
}

onMounted(reload)

async function toggleOpen(name: string) {
  if (opened.value?.name === name) {
    opened.value = null
    return
  }
  opening.value = true
  error.value = ''
  try {
    opened.value = await getWorkDoc(name)
  } catch (e) {
    error.value = e instanceof Error ? e.message : '加载失败'
  } finally {
    opening.value = false
  }
}

function pickFile() {
  fileInput.value?.click()
}

async function onFileChange(ev: Event) {
  const input = ev.target as HTMLInputElement
  const file = input.files?.[0]
  input.value = '' // 允许重复选择同一文件
  if (!file) return
  uploading.value = true
  error.value = ''
  notice.value = ''
  try {
    await uploadWorkDoc(file)
    notice.value = `已上传: ${file.name}`
    await reload()
  } catch (e) {
    error.value = e instanceof Error ? e.message : '上传失败'
  } finally {
    uploading.value = false
  }
}

async function remove(name: string) {
  if (!window.confirm(`确定删除「${name}」吗?此操作不可恢复。`)) return
  error.value = ''
  notice.value = ''
  try {
    await deleteWorkDoc(name)
    if (opened.value?.name === name) opened.value = null
    notice.value = `已删除: ${name}`
    await reload()
  } catch (e) {
    error.value = e instanceof Error ? e.message : '删除失败'
  }
}

function fmtSize(bytes: number) {
  if (bytes < 1024) return `${bytes} B`
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`
  return `${(bytes / 1024 / 1024).toFixed(1)} MB`
}

function fmtTime(iso: string) {
  return iso.replace('T', ' ')
}
</script>

<template>
  <div>
    <header class="mb-8">
      <h2 class="font-serif text-3xl font-bold text-stone-900 dark:text-stone-50">
        当前工作维护
      </h2>
      <p class="mt-2 text-sm text-stone-500 dark:text-stone-400">
        管理 <code class="text-accent">ongoing_work/</code>
        下的工作文档——「与当前工作的相关性」板块每天基于这些文档分析今日消息。支持
        .md / .txt / .docx。
      </p>
      <div class="mt-4 border-t-2 border-stone-900 dark:border-stone-100" />
      <div class="mt-[3px] border-t border-stone-400 dark:border-stone-600" />
    </header>

    <div class="mb-5 flex items-center gap-3">
      <button
        type="button"
        class="bg-accent px-4 py-2 text-sm font-medium text-white transition-opacity hover:opacity-90 disabled:opacity-50"
        :disabled="uploading"
        @click="pickFile"
      >
        {{ uploading ? '上传中…' : '＋ 上传新任务' }}
      </button>
      <input
        ref="fileInput"
        type="file"
        accept=".md,.txt,.docx"
        class="hidden"
        @change="onFileChange"
      />
      <span v-if="notice" class="text-sm text-green-600 dark:text-green-400">
        {{ notice }}
      </span>
      <span v-if="error" class="text-sm text-red-500">{{ error }}</span>
    </div>

    <div v-if="loading" class="py-16 text-center text-sm text-stone-400">载入中…</div>
    <div
      v-else-if="!docs.length"
      class="border border-dashed border-stone-300 py-16 text-center text-sm text-stone-400 dark:border-stone-700"
    >
      暂无工作文档,点击上方「上传新任务」添加
    </div>

    <ul v-else class="space-y-3">
      <li
        v-for="doc in docs"
        :key="doc.name"
        class="border border-stone-200 bg-white dark:border-stone-800 dark:bg-stone-900"
      >
        <div class="flex items-center gap-3 px-5 py-4">
          <span
            class="shrink-0 bg-stone-100 px-1.5 py-0.5 text-[11px] font-semibold uppercase tracking-wide text-stone-500 dark:bg-stone-800 dark:text-stone-400"
          >
            {{ doc.ext }}
          </span>
          <button
            type="button"
            class="min-w-0 flex-1 truncate text-left text-sm font-medium text-stone-800 hover:text-accent dark:text-stone-100"
            @click="toggleOpen(doc.name)"
          >
            {{ doc.name }}
          </button>
          <span class="shrink-0 text-xs tabular-nums text-stone-400">
            {{ fmtSize(doc.size) }}
          </span>
          <span class="hidden shrink-0 text-xs tabular-nums text-stone-400 sm:inline">
            {{ fmtTime(doc.modified) }}
          </span>
          <button
            type="button"
            class="shrink-0 border border-stone-300 px-2.5 py-1 text-xs text-stone-500 transition-colors hover:border-red-400 hover:text-red-500 dark:border-stone-700 dark:text-stone-400"
            @click="remove(doc.name)"
          >
            删除
          </button>
        </div>

        <!-- 展开查看内容 -->
        <div
          v-if="opened?.name === doc.name"
          class="border-t border-stone-200 px-5 py-4 dark:border-stone-800"
        >
          <MarkdownBody v-if="opened.ext === 'md'" :source="opened.text" />
          <pre
            v-else
            class="max-h-[32rem] overflow-y-auto whitespace-pre-wrap text-sm leading-relaxed text-stone-600 dark:text-stone-300"
            >{{ opened.text }}</pre
          >
        </div>
        <div
          v-else-if="opening"
          class="border-t border-stone-200 px-5 py-3 text-xs text-stone-400 dark:border-stone-800"
        >
          载入中…
        </div>
      </li>
    </ul>
  </div>
</template>

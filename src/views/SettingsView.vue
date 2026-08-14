<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { getSettings, saveSettings } from '../api/client'

const model = ref('')
const defaultModel = ref('')
const loading = ref(true)
const saving = ref(false)
const error = ref('')
const notice = ref('')

onMounted(async () => {
  try {
    const s = await getSettings()
    model.value = s.model
    defaultModel.value = s.defaultModel
  } catch (e) {
    error.value = e instanceof Error ? e.message : '加载失败'
  } finally {
    loading.value = false
  }
})

async function save() {
  saving.value = true
  error.value = ''
  notice.value = ''
  try {
    const s = await saveSettings(model.value)
    model.value = s.model
    notice.value = '已保存到 config.json,下次抓取/推送生效'
  } catch (e) {
    error.value = e instanceof Error ? e.message : '保存失败'
  } finally {
    saving.value = false
  }
}

function resetDefault() {
  model.value = defaultModel.value
}
</script>

<template>
  <div>
    <header class="mb-8">
      <h2 class="font-serif text-3xl font-bold text-stone-900 dark:text-stone-50">
        设置
      </h2>
      <div class="mt-4 border-t-2 border-stone-900 dark:border-stone-100" />
      <div class="mt-[3px] border-t border-stone-400 dark:border-stone-600" />
    </header>

    <div v-if="loading" class="py-16 text-center text-sm text-stone-400">载入中…</div>

    <form v-else class="max-w-xl" @submit.prevent="save">
      <label
        for="llm-model"
        class="block text-sm font-medium text-stone-700 dark:text-stone-300"
      >
        LLM 模型
      </label>
      <p class="mt-1 text-xs text-stone-400 dark:text-stone-500">
        写入 <code class="text-accent">config.json</code> 的
        <code class="text-accent">llm.model</code>,全管线(评分/行文/板块分析)共用;
        默认值 {{ defaultModel }}
      </p>
      <div class="mt-3 flex gap-2">
        <input
          id="llm-model"
          v-model="model"
          type="text"
          spellcheck="false"
          class="min-w-0 flex-1 border border-stone-300 bg-white px-3 py-2 font-mono text-sm text-stone-800 focus:border-accent focus:outline-none dark:border-stone-700 dark:bg-stone-900 dark:text-stone-100"
          :placeholder="defaultModel"
        />
        <button
          type="button"
          class="shrink-0 border border-stone-300 px-3 py-2 text-sm text-stone-500 transition-colors hover:border-accent hover:text-accent dark:border-stone-700 dark:text-stone-400"
          @click="resetDefault"
        >
          恢复默认
        </button>
        <button
          type="submit"
          class="shrink-0 bg-accent px-5 py-2 text-sm font-medium text-white transition-opacity hover:opacity-90 disabled:opacity-50"
          :disabled="saving || !model.trim()"
        >
          {{ saving ? '保存中…' : '保存' }}
        </button>
      </div>
      <p v-if="notice" class="mt-3 text-sm text-green-600 dark:text-green-400">
        {{ notice }}
      </p>
      <p v-if="error" class="mt-3 text-sm text-red-500">{{ error }}</p>
    </form>
  </div>
</template>

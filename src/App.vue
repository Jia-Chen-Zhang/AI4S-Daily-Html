<script setup lang="ts">
import AppSidebar from './components/AppSidebar.vue'
</script>

<template>
  <div class="min-h-screen lg:flex">
    <AppSidebar />
    <div class="min-w-0 flex-1">
      <main class="mx-auto max-w-4xl px-4 py-8 sm:px-6">
        <router-view />
      </main>
      <footer
        class="border-t border-stone-200 py-6 text-center text-xs text-stone-400 dark:border-stone-800 dark:text-stone-600"
      >
        AI4S 每日研判 · 归档 — 由 AI 每日资讯推送系统生成
      </footer>
    </div>
  </div>
</template>

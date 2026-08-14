<script setup lang="ts">
import { SECTIONS } from '../sections'
import ThemeToggle from './ThemeToggle.vue'
</script>

<template>
  <!-- 桌面端:固定左侧边栏 -->
  <aside
    class="hidden w-60 shrink-0 flex-col border-r border-stone-200 bg-white lg:sticky lg:top-0 lg:flex lg:h-screen dark:border-stone-800 dark:bg-stone-900"
  >
    <!-- 刊头 -->
    <router-link to="/archive" class="block px-6 pb-6 pt-8">
      <p class="text-[10px] font-medium uppercase tracking-[0.3em] text-accent">
        AI4S Daily
      </p>
      <h1 class="mt-1 font-serif text-2xl font-bold text-stone-900 dark:text-stone-50">
        每日研判
      </h1>
      <div class="mt-4 border-t-2 border-stone-900 dark:border-stone-100" />
      <div class="mt-[2px] border-t border-stone-300 dark:border-stone-700" />
    </router-link>

    <!-- 栏目导航 -->
    <nav class="flex-1 overflow-y-auto px-3" aria-label="栏目">
      <router-link
        v-for="sec in SECTIONS"
        :key="sec.key"
        :to="`/sections/${sec.key}`"
        class="mb-0.5 flex items-center gap-2.5 rounded px-3 py-2 text-sm transition-colors"
        :class="
          $route.path === `/sections/${sec.key}`
            ? 'bg-accent/10 font-semibold text-accent'
            : 'text-stone-600 hover:bg-stone-100 hover:text-stone-900 dark:text-stone-400 dark:hover:bg-stone-800 dark:hover:text-stone-100'
        "
      >
        <span aria-hidden="true">{{ sec.icon }}</span>
        {{ sec.label }}
      </router-link>

      <div class="mx-3 my-3 border-t border-stone-200 dark:border-stone-800" />

      <router-link
        to="/workdocs"
        class="mb-0.5 flex items-center gap-2.5 rounded px-3 py-2 text-sm transition-colors"
        :class="
          $route.path.startsWith('/workdocs')
            ? 'bg-accent/10 font-semibold text-accent'
            : 'text-stone-600 hover:bg-stone-100 hover:text-stone-900 dark:text-stone-400 dark:hover:bg-stone-800 dark:hover:text-stone-100'
        "
      >
        <span aria-hidden="true">🛠️</span>
        当前工作维护
      </router-link>

      <router-link
        to="/archive"
        class="mb-0.5 flex items-center gap-2.5 rounded px-3 py-2 text-sm transition-colors"
        :class="
          $route.path.startsWith('/archive') || $route.path.startsWith('/report/')
            ? 'bg-accent/10 font-semibold text-accent'
            : 'text-stone-600 hover:bg-stone-100 hover:text-stone-900 dark:text-stone-400 dark:hover:bg-stone-800 dark:hover:text-stone-100'
        "
      >
        <span aria-hidden="true">🗞️</span>
        每日研判归档
      </router-link>

      <router-link
        to="/settings"
        class="flex items-center gap-2.5 rounded px-3 py-2 text-sm transition-colors"
        :class="
          $route.path.startsWith('/settings')
            ? 'bg-accent/10 font-semibold text-accent'
            : 'text-stone-600 hover:bg-stone-100 hover:text-stone-900 dark:text-stone-400 dark:hover:bg-stone-800 dark:hover:text-stone-100'
        "
      >
        <span aria-hidden="true">⚙️</span>
        设置
      </router-link>
    </nav>

    <div class="border-t border-stone-200 px-6 py-4 dark:border-stone-800">
      <ThemeToggle />
    </div>
  </aside>

  <!-- 移动端:顶部品牌条 + 横向滚动栏目 -->
  <div class="lg:hidden">
    <div
      class="flex items-center justify-between border-b border-stone-200 bg-white px-4 py-3 dark:border-stone-800 dark:bg-stone-900"
    >
      <router-link to="/archive" class="font-serif text-lg font-bold text-stone-900 dark:text-stone-50">
        每日研判
      </router-link>
      <ThemeToggle />
    </div>
    <nav
      class="flex gap-1 overflow-x-auto border-b border-stone-200 bg-white px-3 py-2 dark:border-stone-800 dark:bg-stone-900"
      aria-label="栏目"
    >
      <router-link
        v-for="sec in SECTIONS"
        :key="sec.key"
        :to="`/sections/${sec.key}`"
        class="shrink-0 rounded-full px-3 py-1 text-xs transition-colors"
        :class="
          $route.path === `/sections/${sec.key}`
            ? 'bg-accent/10 font-semibold text-accent'
            : 'text-stone-500 dark:text-stone-400'
        "
      >
        {{ sec.icon }} {{ sec.label }}
      </router-link>
      <router-link
        to="/workdocs"
        class="shrink-0 rounded-full px-3 py-1 text-xs transition-colors"
        :class="
          $route.path.startsWith('/workdocs')
            ? 'bg-accent/10 font-semibold text-accent'
            : 'text-stone-500 dark:text-stone-400'
        "
      >
        🛠️ 工作
      </router-link>
      <router-link
        to="/archive"
        class="shrink-0 rounded-full px-3 py-1 text-xs transition-colors"
        :class="
          $route.path.startsWith('/archive') || $route.path.startsWith('/report/')
            ? 'bg-accent/10 font-semibold text-accent'
            : 'text-stone-500 dark:text-stone-400'
        "
      >
        🗞️ 归档
      </router-link>
      <router-link
        to="/settings"
        class="shrink-0 rounded-full px-3 py-1 text-xs transition-colors"
        :class="
          $route.path.startsWith('/settings')
            ? 'bg-accent/10 font-semibold text-accent'
            : 'text-stone-500 dark:text-stone-400'
        "
      >
        ⚙️ 设置
      </router-link>
    </nav>
  </div>
</template>

import { createRouter, createWebHistory } from 'vue-router'
import SectionStreamView from '../views/SectionStreamView.vue'
import WorkDocsView from '../views/WorkDocsView.vue'
import ReportListView from '../views/ReportListView.vue'
import ReportDetailView from '../views/ReportDetailView.vue'
import SettingsView from '../views/SettingsView.vue'

export const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', redirect: '/sections/overview' },
    {
      path: '/sections/:key',
      name: 'section',
      component: SectionStreamView,
      // key 是 Vue 保留属性名,不能作为 prop 传递,映射为 sectionKey
      props: (route) => ({ sectionKey: route.params.key }),
    },
    { path: '/workdocs', name: 'workdocs', component: WorkDocsView },
    { path: '/archive', name: 'list', component: ReportListView },
    { path: '/report/:id', name: 'detail', component: ReportDetailView, props: true },
    { path: '/settings', name: 'settings', component: SettingsView },
  ],
  scrollBehavior() {
    return { top: 0 }
  },
})

import { createRouter, createWebHashHistory } from 'vue-router'
import SectionStreamView from '../views/SectionStreamView.vue'
import ReportListView from '../views/ReportListView.vue'
import ReportDetailView from '../views/ReportDetailView.vue'

export const router = createRouter({
  history: createWebHashHistory(),  // GitHub Pages 无服务端 rewrite,用 hash 路由
  routes: [
    { path: '/', redirect: '/sections/overview' },
    {
      path: '/sections/:key',
      name: 'section',
      component: SectionStreamView,
      // key 是 Vue 保留属性名,不能作为 prop 传递,映射为 sectionKey
      props: (route) => ({ sectionKey: route.params.key }),
    },
    { path: '/archive', name: 'list', component: ReportListView },
    { path: '/report/:id', name: 'detail', component: ReportDetailView, props: true },
  ],
  scrollBehavior() {
    return { top: 0 }
  },
})

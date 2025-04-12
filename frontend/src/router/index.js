import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/views/Home.vue'
import Login from '@/views/Login.vue'
import Register from '@/views/Register.vue'
import Callback from '@/views/Callback.vue'
import DistrictDetail from '@/views/DistrictDetail.vue'
import CityDetail from '@/views/CityDetail.vue'
import CTDT from '@/views/CTDT.vue'
import PointCount from '@/views/PointCount.vue'
import QAList from '@/views/QAList.vue'
import QADetail from '@/views/QADetail.vue'
import QACreate from '@/views/QACreate.vue'
import SchoolDetail from '@/views/SchoolDetail.vue'
import Upload from '@/views/Upload.vue'
import SchoolPriority from '@/views/SchoolPriority.vue'

const routes = [
  { path: '/', name: 'Home', component: Home, meta: { title: 'Homepage - ITF Help Student 2025' } },
  { path: '/login', name: 'Login', component: Login, meta: { title: 'Sign in to Your Account' } },
  { path: '/register', name: 'Register', component: Register, meta: { title: 'Create a New Account' } },
  { path: '/callback', name: 'Callback', component: Callback },
  { path: '/district/:district_id', name: 'DistrictDetail', component: DistrictDetail , meta: { title: 'District Detail' } },
  { path: '/city/:city_id', name: 'CityDetail', component: CityDetail , meta: { title: 'City Detail' } },
  { path: '/ctdt', name: 'CTDT', component: CTDT, meta: {title: 'IT Program'} },
  { path: '/point-count', name: 'PointCount', component: PointCount, meta: { title: 'Point Count - ITF Help Student 2025' } },
  { path: '/qa', name: 'QAList', component: QAList, meta: { requiresAuth: true, title: 'Q&A - ITF Help Student 2025' } },
  { path: '/qa/:question_id', name: 'QADetail', component: QADetail },
  { path: '/qa/create', name: 'QACreate', component: QACreate },
  { path: '/school/:school_id', name: 'SchoolDetail', component: SchoolDetail,  meta: { title: 'School Detail' } },
  { path: '/upload', name: 'Upload', component: Upload, meta: { requiresAuth: true } },
  { path: '/school-priority', name: 'SchoolPriority', component: SchoolPriority, meta: { title: 'School Priority - ITF Help Student 2025' } },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

// Router guard: kiểm tra yêu cầu đăng nhập
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  if (to.meta.requiresAuth && !token) {
    next({ name: 'Login' })
  } else {
    next()
  }
})

router.afterEach((to) => {
  document.title = to.meta.title || 'ITF Help Student 2025'
})

export default router

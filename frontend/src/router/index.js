import { createRouter, createWebHistory } from 'vue-router'
import store from '@/store'
import Home from '@/views/Home.vue'
import Login from '@/views/Login.vue'
import Register from '@/views/Register.vue'
import Callback from '@/views/Callback.vue'
import DistrictDetail from '@/views/DistrictDetail.vue'
import CityDetail from '@/views/CityDetail.vue'
import CTDT from '@/views/CTDT.vue'
import PointCount from '@/views/PointCount.vue'
import QAList from '@/views/qnaListView.vue'
import QADetail from '@/views/qnaDetailView.vue'
import QACreate from '@/views/qnaCreateView.vue'
import SchoolDetail from '@/views/SchoolDetail.vue'
import Upload from '@/views/Upload.vue'
import SchoolPriority from '@/views/SchoolPriority.vue'
import Admission from '@/views/AdmissionView.vue'
import Admission_THPT from '@/views/TnTHPTView.vue'
import Admission_HB from '@/views/HBTHPTView.vue'
import Admission_XTT from '@/views/XTTView.vue'
import Admission_XTR from '@/views/XTRView.vue'
import Admission_DGNL from '@/views/DGNLView.vue'
import Admission_DGTD from '@/views/DGTDView.vue'
import preAdmission from '@/views/preAdmission.vue'
import preAdmittedStudent from '@/views/preAdmittedStudent.vue'
import UserController from '@/controllers/userController'

// Admin pages import
import AdminLayout from '@/views/admins/AdminLayout.vue'
import AdminHome from '@/views/admins/AdminHome.vue'

// Admin User Management
import AdminUsers from '@/views/admins/AdminUsers.vue'
import AdminUserDetail from '@/views/admins/AdminUserDetail.vue'
import AdminUserCreate from '@/views/admins/AdminUserCreate.vue'

// Admin Faculty Management
import AdminFaculties from '@/views/admins/AdminFaculties.vue'
import AdminFacultyDetail from '@/views/admins/AdminFacultyDetail.vue'
import AdminFacultyCreate from '@/views/admins/AdminFacultyCreate.vue'

// Admin Major Management
import AdminMajors from '@/views/admins/AdminMajors.vue'
import AdminMajorDetail from '@/views/admins/AdminMajorDetail.vue'
import AdminMajorCreate from '@/views/admins/AdminMajorCreate.vue'

// Add these import lines after the existing imports
import AdminAdmissionMethods from '@/views/admins/AdminAdmissionMethods.vue'
import AdminAdmissionMethodDetail from '@/views/admins/AdminAdmissionMethodDetail.vue'
import AdminAdmissionMethodCreate from '@/views/admins/AdminAdmissionMethodCreate.vue'
import AdminAdmissionMethodMajors from '@/views/admins/AdminAdmissionMethodMajors.vue'
import AdminMajorAdmissionMethods from '@/views/admins/AdminMajorAdmissionMethods.vue'

// Add these import lines
import AdminSubjects from '@/views/admins/AdminSubjects.vue'
import AdminSubjectCreate from '@/views/admins/AdminSubjectCreate.vue'
import AdminSubjectDetail from '@/views/admins/AdminSubjectDetail.vue'
import AdminSubjectGroups from '@/views/admins/AdminSubjectGroups.vue'
import AdminSubjectGroupCreate from '@/views/admins/AdminSubjectGroupCreate.vue'
import AdminSubjectGroupDetail from '@/views/admins/AdminSubjectGroupDetail.vue'

// Define normal routes and admin routes separately
const normalRoutes = [
  { path: '/', name: 'Home', component: Home, meta: { title: 'Trang chủ' } },
  { path: '/login', name: 'Login', component: Login, meta: { title: 'Sign in to Your Account' } },
  { path: '/register', name: 'Register', component: Register, meta: { title: 'Create a New Account' } },
  { path: '/callback', name: 'Callback', component: Callback },
  { path: '/district/:district_id', name: 'DistrictDetail', component: DistrictDetail , meta: { title: 'District Detail' } },
  { path: '/city/:city_id', name: 'CityDetail', component: CityDetail , meta: { title: 'City Detail' } },
  { path: '/ctdt/:id', name: 'CTDT', component: CTDT, meta: { title: 'Program' } },
  { path: '/point-count', name: 'PointCount', component: PointCount, meta: { title: 'Point Count - ITF Help Student 2025' } },
  { path: '/qa', name: 'QAList', component: QAList, meta: { requiresAuth: true, title: 'Q&A' } },
  { path: '/qa/:question_id', name: 'QADetail', component: QADetail, meta: { requiresAuth: true, title: 'Q&A - Chi tiết câu hỏi' } },
  { path: '/qa/create', name: 'QACreate', component: QACreate , meta: { requiresAuth: true, title: 'Q&A - Tạo câu hỏi' }},
  { path: '/qa/update/:question_id', name: 'QAUpdate', component: QACreate, meta: { requiresAuth: true, title: 'Q&A - Cập nhật câu hỏi' } },
  { path: '/school/:school_id', name: 'SchoolDetail', component: SchoolDetail,  meta: { title: 'School Detail' } },
  { path: '/upload', name: 'Upload', component: Upload, meta: { requiresAuth: true } },
  { path: '/school-priority', name: 'SchoolPriority', component: SchoolPriority, meta: { title: 'School Priority - ITF Help Student 2025' } },
  { path: '/admission', name: 'University Admission', component: Admission, meta: {title: 'Thông tin tuyển sinh năm 2025'}},
  { path: '/admission/totnghiep_thpt', name: 'University Admission - TN THPT', component: Admission_THPT, meta: {title: 'Thông tin tuyển sinh năm 2025 - Điểm tốt nghiệp THPT'}},
  { path: '/admission/hocba_thpt', name: 'University Admission - HB THPT', component: Admission_HB, meta: {title: 'Thông tin tuyển sinh năm 2025 - Điểm học tập cấp THPT'}},
  { path: '/admission/xettuyenthang', name: 'University Admission - XTT', component: Admission_XTT, meta: {title: 'Thông tin tuyển sinh năm 2025 - Xét tuyển thẳng'}},
  { path: '/admission/xettuyenrieng', name: 'University Admission - XTR', component: Admission_XTR, meta: {title: 'Thông tin tuyển sinh năm 2025 - Xét tuyển riêng'}},
  { path: '/admission/danhgianangluc', name: 'University Admission - DGNL', component: Admission_DGNL, meta: {title: 'Thông tin tuyển sinh năm 2025 - Đánh giá năng lực'}},
  { path: '/admission/danhgiatuduy', name: 'University Admission - DGTD', component: Admission_DGTD, meta: {title: 'Thông tin tuyển sinh năm 2025 - Đánh giá tư duy'}},
  { path: '/statistics/previous-admission', name: 'PreAdmission', component: preAdmission, meta: {title: 'Thông tin tuyển sinh năm 2025 - Điểm chuẩn các năm trước'}},
  { path: '/statistics/pre-admitted-student', name: 'PreAdmittedStudent', component: preAdmittedStudent, meta: {title: 'Thông tin tuyển sinh năm 2025 - Thống kê sinh viên các năm trước'}}
]

// Admin routes with AdminLayout as the parent
const adminRoutes = [
  { 
    path: '/admins', 
    component: AdminLayout, 
    meta: { requiresAuth: true, requiresAdmin: true },
    children: [
      { 
        path: '', 
        name: 'AdminHome', 
        component: AdminHome, 
        meta: { title: 'Dashboard - Quản trị hệ thống' }
      },
      // User Management Routes
      { 
        path: 'users', 
        name: 'AdminUsers', 
        component: AdminUsers, 
        meta: { title: 'Quản lý người dùng' }
      },
      { 
        path: 'users/create', 
        name: 'AdminUserCreate', 
        component: AdminUserCreate, 
        meta: { title: 'Tạo người dùng mới' }
      },
      { 
        path: 'users/:userId', 
        name: 'AdminUserDetail', 
        component: AdminUserDetail, 
        props: true, 
        meta: { title: 'Chi tiết người dùng' }
      },
      
      // Faculty Management Routes
      {
        path: 'faculties',
        name: 'AdminFaculties',
        component: AdminFaculties,
        meta: { title: 'Quản lý khoa' }
      },
      {
        path: 'faculties/create',
        name: 'AdminFacultyCreate',
        component: AdminFacultyCreate,
        meta: { title: 'Tạo khoa mới' }
      },
      {
        path: 'faculties/:facultyId',
        name: 'AdminFacultyDetail',
        component: AdminFacultyDetail,
        props: true,
        meta: { title: 'Chi tiết khoa' }
      },
      
      // Major Management Routes
      {
        path: 'majors',
        name: 'AdminMajors',
        component: AdminMajors,
        meta: { title: 'Quản lý ngành' }
      },
      {
        path: 'majors/create',
        name: 'AdminMajorCreate',
        component: AdminMajorCreate,
        meta: { title: 'Tạo ngành mới' }
      },
      {
        path: 'majors/:majorId',
        name: 'AdminMajorDetail',
        component: AdminMajorDetail,
        props: true,
        meta: { title: 'Chi tiết ngành' }
      },
      {
        path: 'majors/faculty/:facultyId',
        name: 'AdminMajorsByFaculty',
        component: AdminMajors,
        props: true,
        meta: { title: 'Danh sách ngành theo khoa' }
      },
      {
        path: 'admission-methods',
        name: 'AdminAdmissionMethods',
        component: AdminAdmissionMethods,
        meta: { title: 'Quản lý phương thức tuyển sinh' }
      },
      {
        path: 'admission-methods/create',
        name: 'AdminAdmissionMethodCreate',
        component: AdminAdmissionMethodCreate,
        meta: { title: 'Tạo phương thức tuyển sinh mới' }
      },
      {
        path: 'admission-methods/:admissionMethodId',
        name: 'AdminAdmissionMethodDetail',
        component: AdminAdmissionMethodDetail,
        props: true,
        meta: { title: 'Chi tiết phương thức tuyển sinh' }
      },
      {
        path: 'admission-methods/:admissionMethodId/majors',
        name: 'AdminAdmissionMethodMajors',
        component: AdminAdmissionMethodMajors,
        props: true,
        meta: { title: 'Quản lý ngành áp dụng phương thức tuyển sinh' }
      },
      {
        path: 'majors/:majorId/admission-methods',
        name: 'AdminMajorAdmissionMethods',
        component: AdminMajorAdmissionMethods,
        props: true,
        meta: { title: 'Quản lý phương thức tuyển sinh áp dụng cho ngành' }
      },
      {
        path: 'subjects',
        name: 'AdminSubjects',
        component: AdminSubjects,
        meta: { title: 'Quản lý môn thi' }
      },
      {
        path: 'subjects/create',
        name: 'AdminSubjectCreate',
        component: AdminSubjectCreate,
        meta: { title: 'Tạo môn thi mới' }
      },
      {
        path: 'subjects/:subjectId',
        name: 'AdminSubjectDetail',
        component: AdminSubjectDetail,
        props: true,
        meta: { title: 'Chi tiết môn thi' }
      },
      // Subject Group Management Routes
      {
        path: 'subject-groups',
        name: 'AdminSubjectGroups',
        component: AdminSubjectGroups,
        meta: { title: 'Quản lý tổ hợp môn thi' }
      },
      {
        path: 'subject-groups/create',
        name: 'AdminSubjectGroupCreate',
        component: AdminSubjectGroupCreate,
        meta: { title: 'Tạo tổ hợp môn thi mới' }
      },
      {
        path: 'subject-groups/:groupId',
        name: 'AdminSubjectGroupDetail',
        component: AdminSubjectGroupDetail,
        props: true,
        meta: { title: 'Chi tiết tổ hợp môn thi' }
      },
    ]
  }
]

// Combine all routes
const routes = [
  ...normalRoutes,
  ...adminRoutes
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

// Router guard: kiểm tra yêu cầu đăng nhập và quyền admin
router.beforeEach(async (to, from, next) => {
  const token = sessionStorage.getItem('token')

  // Check if route is part of admin area
  const isAdminRoute = to.path.startsWith('/admins')

  if (to.meta.requiresAuth) {
    if (!token) {
      // Không có token => chuyển đến Login
      alert('Vui lòng đăng nhập.')
      next({ name: 'Login' })
    } else if (!store.isTokenValid()) {
      // Token hết hạn
      alert('Phiên đăng nhập đã hết hạn. Vui lòng đăng nhập lại.')
      store.clearToken()
      next({ name: 'Login' })
    } else if (to.meta.requiresAdmin) {
      // Kiểm tra quyền admin bằng cách gọi getCurrentUser()
      try {
        const user = await UserController.getCurrentUser()
        if (user && user.role === 'admin') {
          next() // User có quyền admin, cho phép tiếp tục
        } else {
          alert('Bạn không có quyền truy cập trang này.')
          next({ name: 'Home' })
        }
      } catch (error) {
        console.error('Error checking user role:', error)
        alert('Có lỗi xảy ra khi xác thực quyền truy cập. Vui lòng đăng nhập lại.')
        store.clearToken()
        next({ name: 'Login' })
      }
    } else {
      // Token hợp lệ => cho phép đi tiếp
      next()
    }
  } else {
    next()
  }
})

router.afterEach((to) => {
  document.title = to.meta.title || 'Tư vấn tuyển sinh năm 2025'
})

export default router
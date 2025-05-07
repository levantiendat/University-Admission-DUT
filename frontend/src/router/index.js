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

import AdminPreviousAdmissions from '@/views/admins/AdminPreviousAdmissions.vue'
import AdminPreviousAdmissionCreate from '@/views/admins/AdminPreviousAdmissionCreate.vue'
import AdminPreviousAdmissionDetail from '@/views/admins/AdminPreviousAdmissionDetail.vue'
import AdminAdmissionDescriptions from '@/views/admins/AdminAdmissionDescriptions.vue'
import AdminAdmissionDescriptionCreate from '@/views/admins/AdminAdmissionDescriptionCreate.vue'
import AdminAdmissionDescriptionDetail from '@/views/admins/AdminAdmissionDescriptionDetail.vue'

import AdminConvertPoints from '@/views/admins/AdminConvertPoints.vue'
import AdminConvertPointCreate from '@/views/admins/AdminConvertPointCreate.vue'
import AdminConvertPointDetail from '@/views/admins/AdminConvertPointDetail.vue'

import AdminMajorCourses from '@/views/admins/AdminMajorCourses.vue'
import AdminMajorCourseCreate from '@/views/admins/AdminMajorCourseCreate.vue'
import AdminMajorCourseDetail from '@/views/admins/AdminMajorCourseDetail.vue'

import AdminCourses from '@/views/admins/AdminCourses.vue'
import AdminCourseCreate from '@/views/admins/AdminCourseCreate.vue'
import AdminCourseDetail from '@/views/admins/AdminCourseDetail.vue'


import AdminMajorCourseDetailEdit from '@/views/admins/AdminMajorCourseDetailEdit.vue'

import AdminSchoolPriorities from '@/views/admins/AdminSchoolPriorities.vue'
import AdminCityCreate from '@/views/admins/AdminCityCreate.vue'
import AdminCityDetail from '@/views/admins/AdminCityDetail.vue'
import AdminDistrictCreate from '@/views/admins/AdminDistrictCreate.vue'
import AdminDistrictDetail from '@/views/admins/AdminDistrictDetail.vue'
import AdminSchoolCreate from '@/views/admins/AdminSchoolCreate.vue'
import AdminSchoolDetail from '@/views/admins/AdminSchoolDetail.vue'

import AdminQnaQuestions from '@/views/admins/AdminQnaQuestions.vue'
import AdminQnaDetail from '@/views/admins/AdminQnaDetail.vue'
import AdminQnaCreate from '@/views/admins/AdminQnaCreate.vue'
import AdminQnaEdit from '@/views/admins/AdminQnaEdit.vue'

import ChatRasaView from '@/views/ChatRasaView.vue'

import CalculateScoreHB from '@/views/CalculateScoreHB.vue'
import CalculateScoreTHPT from '@/views/CalculateScoreTHPT.vue'

import MajorList from '@/views/MajorList.vue'
import MajorDetail from '@/views/MajorDetail.vue'

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
  { path: '/statistics/pre-admitted-student', name: 'PreAdmittedStudent', component: preAdmittedStudent, meta: {title: 'Thông tin tuyển sinh năm 2025 - Thống kê sinh viên các năm trước'}},
  { 
    path: '/chat', 
    name: 'Chat', 
    component: ChatRasaView, 
    meta: { 
      requiresAuth: true, 
      title: 'Chat với trợ lý tư vấn tuyển sinh' 
    } 
  },
  { 
    path: '/calculatescore/hb', 
    name: 'CalculateScoreHB', 
    component: CalculateScoreHB, 
    meta: { title: 'Tính điểm xét tuyển học bạ THPT' } 
  },
  { 
    path: '/calculatescore/thpt', 
    name: 'CalculateScoreTHPT', 
    component: CalculateScoreTHPT, 
    meta: { title: 'Tính điểm xét tuyển thi THPT' } 
  },
  { 
    path: '/major', 
    name: 'MajorList', 
    component: MajorList, 
    meta: { title: 'Danh sách ngành tuyển sinh năm 2025' } 
  },
  { 
    path: '/major/:id', 
    name: 'MajorDetail', 
    component: MajorDetail, 
    props: true,
    meta: { title: 'Chi tiết ngành tuyển sinh' } 
  },
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
      {
        path: 'previous-admissions',
        name: 'AdminPreviousAdmissions',
        component: AdminPreviousAdmissions,
        meta: { title: 'Quản lý điểm chuẩn các năm trước' }
      },
      {
        path: 'previous-admissions/create',
        name: 'AdminPreviousAdmissionCreate',
        component: AdminPreviousAdmissionCreate,
        meta: { title: 'Thêm điểm chuẩn mới' }
      },
      {
        path: 'previous-admissions/:admissionId',
        name: 'AdminPreviousAdmissionDetail',
        component: AdminPreviousAdmissionDetail,
        props: true,
        meta: { title: 'Chi tiết điểm chuẩn' }
      },
      {
        path: 'admission-descriptions',
        name: 'AdminAdmissionDescriptions',
        component: AdminAdmissionDescriptions,
        meta: { title: 'Quản lý lĩnh vực/môn học xét tuyển' }
      },
      {
        path: 'admission-descriptions/create',
        name: 'AdminAdmissionDescriptionCreate',
        component: AdminAdmissionDescriptionCreate,
        meta: { title: 'Thêm lĩnh vực/môn học xét tuyển mới' }
      },
      {
        path: 'admission-descriptions/:descriptionId',
        name: 'AdminAdmissionDescriptionDetail',
        component: AdminAdmissionDescriptionDetail,
        props: true,
        meta: { title: 'Chi tiết lĩnh vực/môn học xét tuyển' }
      },
      {
        path: 'convert-points',
        name: 'AdminConvertPoints',
        component: AdminConvertPoints,
        meta: { title: 'Quản lý quy đổi điểm' }
      },
      {
        path: 'convert-points/create',
        name: 'AdminConvertPointCreate',
        component: AdminConvertPointCreate,
        meta: { title: 'Thêm quy đổi điểm mới' }
      },
      {
        path: 'convert-points/:convertPointId',
        name: 'AdminConvertPointDetail',
        component: AdminConvertPointDetail,
        props: true,
        meta: { title: 'Chi tiết quy đổi điểm' }
      },
      {
        path: 'major-courses',
        name: 'AdminMajorCourses',
        component: AdminMajorCourses,
        meta: { title: 'Quản lý khung chương trình đào tạo' }
      },
      {
        path: 'major-courses/create',
        name: 'AdminMajorCourseCreate',
        component: AdminMajorCourseCreate,
        meta: { title: 'Thêm khung chương trình đào tạo mới' }
      },
      {
        path: 'major-courses/:majorCourseId',
        name: 'AdminMajorCourseDetail',
        component: AdminMajorCourseDetail,
        props: true,
        meta: { title: 'Chi tiết khung chương trình đào tạo' }
      },
      {
        path: 'major-courses/details/:detailId',
        name: 'AdminMajorCourseDetailEdit',
        component: AdminMajorCourseDetailEdit,
        props: true,
        meta: { title: 'Sửa thông tin học phần trong khung chương trình' }
      },
      {
        path: 'courses',
        name: 'AdminCourses',
        component: AdminCourses,
        meta: { title: 'Quản lý lớp học phần' }
      },
      {
        path: 'courses/create',
        name: 'AdminCourseCreate',
        component: AdminCourseCreate,
        meta: { title: 'Thêm lớp học phần mới' }
      },
      {
        path: 'courses/:courseId',
        name: 'AdminCourseDetail',
        component: AdminCourseDetail,
        props: true,
        meta: { title: 'Chi tiết lớp học phần' }
      },
      {
        path: 'school-priorities',
        name: 'AdminSchoolPriorities',
        component: AdminSchoolPriorities,
        meta: { title: 'Quản lý khu vực ưu tiên' }
      },
      {
        path: 'school-priorities/cities/create',
        name: 'AdminCityCreate',
        component: AdminCityCreate,
        meta: { title: 'Tạo tỉnh/thành phố mới' }
      },
      {
        path: 'school-priorities/cities/:cityId',
        name: 'AdminCityDetail',
        component: AdminCityDetail,
        props: true,
        meta: { title: 'Chi tiết tỉnh/thành phố' }
      },
      {
        path: 'school-priorities/districts/create',
        name: 'AdminDistrictCreate',
        component: AdminDistrictCreate,
        meta: { title: 'Tạo quận/huyện mới' }
      },
      {
        path: 'school-priorities/districts/:districtId',
        name: 'AdminDistrictDetail',
        component: AdminDistrictDetail,
        props: true,
        meta: { title: 'Chi tiết quận/huyện' }
      },
      {
        path: 'school-priorities/schools/create',
        name: 'AdminSchoolCreate',
        component: AdminSchoolCreate,
        meta: { title: 'Tạo trường học mới' }
      },
      {
        path: 'school-priorities/schools/:schoolId',
        name: 'AdminSchoolDetail',
        component: AdminSchoolDetail,
        props: true,
        meta: { title: 'Chi tiết trường học' }
      },
      {
        path: 'qna',
        name: 'AdminQna',
        component: AdminQnaQuestions,
        meta: { title: 'Quản lý hỏi đáp (Q&A)' }
      },
      {
        path: 'qna/create',
        name: 'AdminQnaCreate',
        component: AdminQnaCreate,
        meta: { title: 'Tạo câu hỏi mới' }
      },
      {
        path: 'qna/:questionId',
        name: 'AdminQnaDetail',
        component: AdminQnaDetail,
        props: true,
        meta: { title: 'Chi tiết câu hỏi' }
      },
      {
        path: 'qna/:questionId/edit',
        name: 'AdminQnaEdit',
        component: AdminQnaEdit,
        props: true,
        meta: { title: 'Chỉnh sửa câu hỏi' }
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
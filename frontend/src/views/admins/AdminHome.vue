<template>
  <div class="admin-home">
    <div class="admin-page-header">
      <h2 class="admin-page-title">Dashboard</h2>
      <p class="admin-page-description">Chào mừng đến với hệ thống quản trị tuyển sinh</p>
    </div>

    <!-- Stats Cards -->
    <div class="stats-container">
      <div class="row">
        <!-- Majors Stats -->
        <div class="col-md-3 col-sm-6 mb-4">
          <div class="admin-stat-card">
            <div class="admin-stat-icon bg-success">
              <i class="bi bi-book"></i>
            </div>
            <div class="admin-stat-content">
              <h3 class="admin-stat-value">{{ majorCount }}</h3>
              <p class="admin-stat-label">Ngành</p>
            </div>
          </div>
        </div>
        
        <!-- Faculties Stats -->
        <div class="col-md-3 col-sm-6 mb-4">
          <div class="admin-stat-card">
            <div class="admin-stat-icon bg-info">
              <i class="bi bi-building"></i>
            </div>
            <div class="admin-stat-content">
              <h3 class="admin-stat-value">{{ facultyCount }}</h3>
              <p class="admin-stat-label">Khoa</p>
            </div>
          </div>
        </div>

        <!-- Admission Methods Stats -->
        <div class="col-md-3 col-sm-6 mb-4">
          <div class="admin-stat-card">
            <div class="admin-stat-icon bg-purple">
              <i class="bi bi-clipboard-check"></i>
            </div>
            <div class="admin-stat-content">
              <h3 class="admin-stat-value">{{ admissionMethodCount }}</h3>
              <p class="admin-stat-label">Phương thức tuyển sinh</p>
            </div>
          </div>
        </div>

        <!-- Previous Admissions Stats -->
        <div class="col-md-3 col-sm-6 mb-4">
          <div class="admin-stat-card">
            <div class="admin-stat-icon bg-teal">
              <i class="bi bi-bar-chart-line"></i>
            </div>
            <div class="admin-stat-content">
              <h3 class="admin-stat-value">{{ previousAdmissionCount }}</h3>
              <p class="admin-stat-label">Điểm chuẩn</p>
            </div>
          </div>
        </div>

        <!-- Subjects Stats -->
        <div class="col-md-3 col-sm-6 mb-4">
          <div class="admin-stat-card">
            <div class="admin-stat-icon bg-secondary">
              <i class="bi bi-journal-text"></i>
            </div>
            <div class="admin-stat-content">
              <h3 class="admin-stat-value">{{ subjectCount }}</h3>
              <p class="admin-stat-label">Môn thi</p>
            </div>
          </div>
        </div>

        <!-- Subject Groups Stats -->
        <div class="col-md-3 col-sm-6 mb-4">
          <div class="admin-stat-card">
            <div class="admin-stat-icon bg-indigo">
              <i class="bi bi-diagram-3"></i>
            </div>
            <div class="admin-stat-content">
              <h3 class="admin-stat-value">{{ subjectGroupCount }}</h3>
              <p class="admin-stat-label">Tổ hợp môn</p>
            </div>
          </div>
        </div>
        
        <!-- Major Courses Stats -->
        <div class="col-md-3 col-sm-6 mb-4">
          <div class="admin-stat-card">
            <div class="admin-stat-icon bg-orange">
              <i class="bi bi-mortarboard-fill"></i>
            </div>
            <div class="admin-stat-content">
              <h3 class="admin-stat-value">{{ majorCourseCount }}</h3>
              <p class="admin-stat-label">Khung chương trình</p>
            </div>
          </div>
        </div>
        
        <!-- Courses Stats -->
        <div class="col-md-3 col-sm-6 mb-4">
          <div class="admin-stat-card">
            <div class="admin-stat-icon bg-blue">
              <i class="bi bi-journals"></i>
            </div>
            <div class="admin-stat-content">
              <h3 class="admin-stat-value">{{ courseCount }}</h3>
              <p class="admin-stat-label">Lớp học phần</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Management Sections -->
    <div class="management-container">
      <h3 class="section-title">Quản lý cơ bản</h3>
      <div class="row">
        <!-- Faculty Management -->
        <div class="col-md-6 col-lg-4 mb-4">
          <div class="admin-card">
            <div class="admin-card-header">
              <div class="admin-card-icon bg-info">
                <i class="bi bi-building"></i>
              </div>
              <h4 class="admin-card-title">Quản lý khoa</h4>
            </div>
            <div class="admin-actions">
              <router-link to="/admins/faculties" class="admin-action-btn">
                <i class="bi bi-list-ul me-2"></i>
                Danh sách khoa
              </router-link>
              
              <router-link to="/admins/faculties/create" class="admin-action-btn">
                <i class="bi bi-plus-circle me-2"></i>
                Thêm khoa mới
              </router-link>
            </div>
          </div>
        </div>
        
        <!-- Major Management -->
        <div class="col-md-6 col-lg-4 mb-4">
          <div class="admin-card">
            <div class="admin-card-header">
              <div class="admin-card-icon bg-success">
                <i class="bi bi-book"></i>
              </div>
              <h4 class="admin-card-title">Quản lý ngành</h4>
            </div>
            <div class="admin-actions">
              <router-link to="/admins/majors" class="admin-action-btn">
                <i class="bi bi-list-ul me-2"></i>
                Danh sách ngành
              </router-link>
              
              <router-link to="/admins/majors/create" class="admin-action-btn">
                <i class="bi bi-plus-circle me-2"></i>
                Thêm ngành mới
              </router-link>
            </div>
          </div>
        </div>

        <!-- User Management -->
        <div class="col-md-6 col-lg-4 mb-4">
          <div class="admin-card">
            <div class="admin-card-header">
              <div class="admin-card-icon bg-primary">
                <i class="bi bi-people-fill"></i>
              </div>
              <h4 class="admin-card-title">Quản lý người dùng</h4>
            </div>
            <div class="admin-actions">
              <router-link to="/admins/users" class="admin-action-btn">
                <i class="bi bi-list-ul me-2"></i>
                Danh sách người dùng
              </router-link>
              
              <router-link to="/admins/users/create" class="admin-action-btn">
                <i class="bi bi-person-plus-fill me-2"></i>
                Thêm người dùng mới
              </router-link>
            </div>
          </div>
        </div>
      </div>

      <h3 class="section-title">Quản lý tuyển sinh</h3>
      <div class="row">
        <!-- Admission Method Management -->
        <div class="col-md-6 col-lg-4 mb-4">
          <div class="admin-card">
            <div class="admin-card-header">
              <div class="admin-card-icon bg-purple">
                <i class="bi bi-clipboard-check"></i>
              </div>
              <h4 class="admin-card-title">Phương thức xét tuyển</h4>
            </div>
            <div class="admin-actions">
              <router-link to="/admins/admission-methods" class="admin-action-btn">
                <i class="bi bi-list-ul me-2"></i>
                Danh sách phương thức
              </router-link>
      
              <router-link to="/admins/admission-methods/create" class="admin-action-btn">
                <i class="bi bi-plus-circle me-2"></i>
                Thêm phương thức mới
              </router-link>
            </div>
          </div>
        </div>

        <!-- Subject Management -->
        <div class="col-md-6 col-lg-4 mb-4">
          <div class="admin-card">
            <div class="admin-card-header">
              <div class="admin-card-icon bg-secondary">
                <i class="bi bi-journal-text"></i>
              </div>
              <h4 class="admin-card-title">Quản lý môn thi</h4>
            </div>
            <div class="admin-actions">
              <router-link to="/admins/subjects" class="admin-action-btn">
                <i class="bi bi-list-ul me-2"></i>
                Danh sách môn thi
              </router-link>
      
              <router-link to="/admins/subjects/create" class="admin-action-btn">
                <i class="bi bi-plus-circle me-2"></i>
                Thêm môn thi mới
              </router-link>
            </div>
          </div>
        </div>

        <!-- Subject Group Management -->
        <div class="col-md-6 col-lg-4 mb-4">
          <div class="admin-card">
            <div class="admin-card-header">
              <div class="admin-card-icon bg-indigo">
                <i class="bi bi-diagram-3"></i>
              </div>
              <h4 class="admin-card-title">Tổ hợp môn thi</h4>
            </div>
            <div class="admin-actions">
              <router-link to="/admins/subject-groups" class="admin-action-btn">
                <i class="bi bi-list-ul me-2"></i>
                Danh sách tổ hợp
              </router-link>
      
              <router-link to="/admins/subject-groups/create" class="admin-action-btn">
                <i class="bi bi-plus-circle me-2"></i>
                Thêm tổ hợp mới
              </router-link>
            </div>
          </div>
        </div>

        <!-- Previous Admission Scores Management -->
        <div class="col-md-6 col-lg-4 mb-4">
          <div class="admin-card">
            <div class="admin-card-header">
              <div class="admin-card-icon bg-teal">
                <i class="bi bi-bar-chart-line"></i>
              </div>
              <h4 class="admin-card-title">Điểm chuẩn các năm</h4>
            </div>
            <div class="admin-actions">
              <router-link to="/admins/previous-admissions" class="admin-action-btn">
                <i class="bi bi-list-ul me-2"></i>
                Danh sách điểm chuẩn
              </router-link>
      
              <router-link to="/admins/previous-admissions/create" class="admin-action-btn">
                <i class="bi bi-plus-circle me-2"></i>
                Thêm điểm chuẩn mới
              </router-link>
            </div>
          </div>
        </div>
        
        <!-- Convert Points Management -->
        <div class="col-md-6 col-lg-4 mb-4">
          <div class="admin-card">
            <div class="admin-card-header">
              <div class="admin-card-icon bg-cyan">
                <i class="bi bi-calculator"></i>
              </div>
              <h4 class="admin-card-title">Quy đổi điểm</h4>
            </div>
            <div class="admin-actions">
              <router-link to="/admins/convert-points" class="admin-action-btn">
                <i class="bi bi-list-ul me-2"></i>
                Danh sách quy đổi điểm
              </router-link>
      
              <router-link to="/admins/convert-points/create" class="admin-action-btn">
                <i class="bi bi-plus-circle me-2"></i>
                Thêm quy đổi điểm mới
              </router-link>
            </div>
          </div>
        </div>
        
        <!-- Admission Descriptions Management -->
        <div class="col-md-6 col-lg-4 mb-4">
          <div class="admin-card">
            <div class="admin-card-header">
              <div class="admin-card-icon bg-coral">
                <i class="bi bi-award"></i>
              </div>
              <h4 class="admin-card-title">Lĩnh vực/Môn học xét tuyển</h4>
            </div>
            <div class="admin-actions">
              <router-link to="/admins/admission-descriptions" class="admin-action-btn">
                <i class="bi bi-list-ul me-2"></i>
                Danh sách lĩnh vực/môn học
              </router-link>
      
              <router-link to="/admins/admission-descriptions/create" class="admin-action-btn">
                <i class="bi bi-plus-circle me-2"></i>
                Thêm lĩnh vực/môn học mới
              </router-link>
            </div>
          </div>
        </div>
      </div>
      
      <h3 class="section-title">Quản lý đào tạo</h3>
      <div class="row">
        <!-- Major Courses Management -->
        <div class="col-md-6 mb-4">
          <div class="admin-card">
            <div class="admin-card-header">
              <div class="admin-card-icon bg-orange">
                <i class="bi bi-mortarboard-fill"></i>
              </div>
              <h4 class="admin-card-title">Khung chương trình đào tạo</h4>
            </div>
            <div class="admin-actions">
              <router-link to="/admins/major-courses" class="admin-action-btn">
                <i class="bi bi-list-ul me-2"></i>
                Danh sách khung chương trình
              </router-link>
      
              <router-link to="/admins/major-courses/create" class="admin-action-btn">
                <i class="bi bi-plus-circle me-2"></i>
                Thêm khung chương trình mới
              </router-link>
            </div>
          </div>
        </div>

        <!-- Course Management -->
        <div class="col-md-6 mb-4">
          <div class="admin-card highlight-card">
            <div class="admin-card-header">
              <div class="admin-card-icon bg-blue">
                <i class="bi bi-journals"></i>
              </div>
              <h4 class="admin-card-title">Lớp học phần</h4>
            </div>
            <div class="admin-actions">
              <router-link to="/admins/courses" class="admin-action-btn">
                <i class="bi bi-list-ul me-2"></i>
                Danh sách lớp học phần
              </router-link>
      
              <router-link to="/admins/courses/create" class="admin-action-btn">
                <i class="bi bi-plus-circle me-2"></i>
                Thêm lớp học phần mới
              </router-link>
            </div>
          </div>
        </div>
      </div>
      
      <h3 class="section-title">Quản lý khu vực ưu tiên</h3>
      <div class="row">
        <div class="col-md-12 mb-4">
          <div class="admin-card">
            <div class="admin-card-header">
              <div class="admin-card-icon bg-green">
                <i class="bi bi-geo-alt-fill"></i>
              </div>
              <h4 class="admin-card-title">Quản lý khu vực ưu tiên</h4>
            </div>
            <div class="admin-actions">
              <router-link to="/admins/school-priorities" class="admin-action-btn">
                <i class="bi bi-list-ul me-2"></i>
                Danh sách tỉnh/thành phố
              </router-link>
              
              <router-link to="/admins/school-priorities/cities/create" class="admin-action-btn">
                <i class="bi bi-plus-circle me-2"></i>
                Thêm tỉnh/thành phố mới
              </router-link>
            </div>
          </div>
        </div>
      </div>
      
      <!-- System Stats -->
      <div class="col-md-12">
        <div class="admin-card">
          <div class="admin-card-header">
            <div class="admin-card-icon bg-warning">
              <i class="bi bi-bar-chart-fill"></i>
            </div>
            <h4 class="admin-card-title">Thống kê hệ thống</h4>
          </div>
          <div class="system-stats">
            <div class="row">
              <div class="col-md-6">
                <div class="system-stat-item">
                  <span class="system-stat-label">Tổng lượt truy cập:</span>
                  <span class="system-stat-value">{{ totalVisitors }}</span>
                </div>
                <div class="system-stat-item">
                  <span class="system-stat-label">Người dùng hiện tại:</span>
                  <span class="system-stat-value">{{ currentVisitors }}</span>
                </div>
              </div>
              <div class="col-md-6">
                <div class="system-stat-item">
                  <span class="system-stat-label">Thời gian hiện tại:</span>
                  <span class="system-stat-value">{{ currentDateTime }}</span>
                </div>
                <div class="system-stat-item">
                  <span class="system-stat-label">Người đang đăng nhập:</span>
                  <span class="system-stat-value">{{ currentUser }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import UserController from '@/controllers/admins/UserController'
import FacultyController from '@/controllers/admins/FacultyController'
import MajorController from '@/controllers/admins/MajorController'
import AdmissionMethodController from '@/controllers/admins/AdmissionMethodController'
import SubjectController from '@/controllers/admins/SubjectController'
import SubjectGroupController from '@/controllers/admins/SubjectGroupController'
import PreviousAdmissionController from '@/controllers/admins/PreviousAdmissionController'
import AdmissionDescriptionController from '@/controllers/admins/AdmissionDescriptionController'
import ConvertPointController from '@/controllers/admins/ConvertPointController'
import MajorCourseController from '@/controllers/admins/MajorCourseController'
import CourseController from '@/controllers/admins/CourseController'
import axios from 'axios'
import config from '@/config/apiConfig'

const BASE_API_URL = config?.BASE_API_URL || 'https://university-admission-dut-hzdahmckevehhpdf.southeastasia-01.azurewebsites.net/api'

export default {
  name: 'AdminHome',
  setup() {
    const userCount = ref(0)
    const facultyCount = ref(0)
    const majorCount = ref(0)
    const currentVisitors = ref(0)
    const totalVisitors = ref(0)
    const admissionMethodCount = ref(0)
    const subjectCount = ref(0)
    const subjectGroupCount = ref(0)
    const previousAdmissionCount = ref(0)
    const admissionDescriptionCount = ref(0)
    const convertPointCount = ref(0)
    const majorCourseCount = ref(0)
    const courseCount = ref(0)
    const currentUser = ref(sessionStorage.getItem('username') || 'levantiendatBạn')

    // Get current date and time in Vietnam timezone
    const currentDateTime = computed(() => {
      const now = new Date()
      return now.toLocaleString('vi-VN', {
        timeZone: 'Asia/Ho_Chi_Minh',
        dateStyle: 'full',
        timeStyle: 'medium'
      })
    })

    // Hàm lấy số lượng người dùng
    const fetchUserCount = async () => {
      try {
        const users = await UserController.getAllUsers()
        userCount.value = users.length
      } catch (error) {
        console.error('Error fetching user count:', error)
      }
    }
    
    // Hàm lấy số lượng khoa
    const fetchFacultyCount = async () => {
      try {
        const faculties = await FacultyController.getAllFaculties()
        facultyCount.value = faculties.length
      } catch (error) {
        console.error('Error fetching faculty count:', error)
      }
    }
    
    // Hàm lấy số lượng ngành
    const fetchMajorCount = async () => {
      try {
        const majors = await MajorController.getAllMajors()
        majorCount.value = majors.length
      } catch (error) {
        console.error('Error fetching major count:', error)
      }
    }

    // Hàm lấy thông tin người truy cập
    const fetchVisitorStats = async () => {
      try {
        const response = await axios.get(`${BASE_API_URL}/visitors/stats`, {
          withCredentials: true
        })
        
        if (response.data) {
          currentVisitors.value = response.data.current_visitors
          totalVisitors.value = response.data.total_visitors
        }
      } catch (error) {
        console.error('Error fetching visitor stats:', error)
      }
    }

    const fetchAdmissionMethodCount = async () => {
      try {
        const methods = await AdmissionMethodController.getAllAdmissionMethods()
        admissionMethodCount.value = methods.length
      } catch (error) {
        console.error('Error fetching admission method count:', error)
      }
    }

    const fetchSubjectCount = async () => {
      try {
        const subjects = await SubjectController.getAllSubjects()
        subjectCount.value = subjects.length
      } catch (error) {
        console.error('Error fetching subject count:', error)
      }
    }

    const fetchSubjectGroupCount = async () => {
      try {
        const groups = await SubjectGroupController.getAllSubjectGroups()
        subjectGroupCount.value = groups.length
      } catch (error) {
        console.error('Error fetching subject group count:', error)
      }
    }
    
    const fetchPreviousAdmissionCount = async () => {
      try {
        const admissions = await PreviousAdmissionController.getAllPreviousAdmissions()
        previousAdmissionCount.value = admissions.length
      } catch (error) {
        console.error('Error fetching previous admission count:', error)
        previousAdmissionCount.value = 0
      }
    }
    
    const fetchAdmissionDescriptionCount = async () => {
      try {
        const descriptions = await AdmissionDescriptionController.getAllAdmissionDescriptions()
        admissionDescriptionCount.value = descriptions.length
      } catch (error) {
        console.error('Error fetching admission description count:', error)
        admissionDescriptionCount.value = 0
      }
    }
    
    const fetchConvertPointCount = async () => {
      try {
        const convertPoints = await ConvertPointController.getAllConvertPoints()
        convertPointCount.value = convertPoints.length
      } catch (error) {
        console.error('Error fetching convert points count:', error)
        convertPointCount.value = 0
      }
    }
    
    const fetchMajorCourseCount = async () => {
      try {
        const majorCourses = await MajorCourseController.getAllMajorCourses()
        majorCourseCount.value = majorCourses.length
      } catch (error) {
        console.error('Error fetching major courses count:', error)
        majorCourseCount.value = 0
      }
    }
    
    const fetchCourseCount = async () => {
      try {
        const courses = await CourseController.getAllCourses()
        courseCount.value = courses.length
      } catch (error) {
        console.error('Error fetching courses count:', error)
        courseCount.value = 0
      }
    }

    onMounted(() => {
      fetchUserCount()
      fetchFacultyCount()
      fetchMajorCount()
      fetchVisitorStats()
      fetchAdmissionMethodCount()
      fetchSubjectCount()
      fetchSubjectGroupCount()
      fetchPreviousAdmissionCount()
      fetchAdmissionDescriptionCount()
      fetchConvertPointCount()
      fetchMajorCourseCount()
      fetchCourseCount()
    })

    return {
      userCount,
      facultyCount,
      majorCount,
      currentVisitors,
      totalVisitors,
      admissionMethodCount,
      subjectCount,
      subjectGroupCount,
      previousAdmissionCount,
      admissionDescriptionCount,
      convertPointCount,
      majorCourseCount,
      courseCount,
      currentDateTime,
      currentUser
    }
  }
}
</script>

<style scoped>
.admin-home {
  width: 100%;
}

.admin-page-header {
  margin-bottom: 2rem;
}

.admin-page-title {
  font-size: 1.75rem;
  font-weight: 600;
  color: #0B2942;
  margin-bottom: 0.5rem;
}

.admin-page-description {
  color: #6c757d;
  font-size: 0.95rem;
}

.section-title {
  font-size: 1.35rem;
  font-weight: 600;
  color: #0B2942;
  margin: 2rem 0 1.25rem 0;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid #e9ecef;
}

/* Stats Cards */
.stats-container {
  margin-bottom: 1.5rem;
}

.admin-stat-card {
  background-color: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  padding: 1.25rem;
  display: flex;
  align-items: center;
  height: 100%;
  transition: transform 0.3s, box-shadow 0.3s;
}

.admin-stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
}

.admin-stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 1rem;
  color: #fff;
  font-size: 1.75rem;
}

.admin-stat-content {
  flex: 1;
}

.admin-stat-value {
  font-size: 1.75rem;
  font-weight: 600;
  margin: 0;
  color: #0B2942;
}

.admin-stat-label {
  font-size: 0.9rem;
  color: #6c757d;
  margin-top: 0.25rem;
  margin-bottom: 0;
}

/* Management Cards */
.management-container {
  margin-top: 2rem;
}

.admin-card {
  background-color: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  padding: 1.5rem;
  margin-bottom: 1rem;
  height: 100%;
  transition: transform 0.3s, box-shadow 0.3s;
}

.admin-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
}

/* Highlight the new feature */
.highlight-card {
  border: 2px solid #1e88e5;
  position: relative;
  overflow: hidden;
}

.highlight-card::before {
  content: "Mới";
  position: absolute;
  top: -10px;
  right: -25px;
  background-color: #1e88e5;
  color: white;
  padding: 20px 25px 5px 25px;
  font-size: 12px;
  font-weight: bold;
  transform: rotate(45deg);
}

.admin-card-header {
  display: flex;
  align-items: center;
  margin-bottom: 1.25rem;
}

.admin-card-icon {
  width: 48px;
  height: 48px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 1rem;
  color: #fff;
  font-size: 1.5rem;
}

.admin-card-title {
  font-size: 1.2rem;
  font-weight: 600;
  color: #0B2942;
  margin: 0;
}

.admin-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}

.admin-action-btn {
  display: inline-flex;
  align-items: center;
  background-color: #0B2942;
  color: #fff;
  padding: 0.75rem 1.25rem;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s;
  border: none;
  cursor: pointer;
  flex: 1;
  min-width: 200px;
  justify-content: center;
}

.admin-action-btn:hover {
  background-color: #4da0ff;
  color: #fff;
  transform: translateY(-2px);
}

/* System Stats */
.system-stats {
  padding: 0.5rem 0;
}

.system-stat-item {
  display: flex;
  justify-content: space-between;
  padding: 0.75rem 0;
  border-bottom: 1px solid #f1f1f1;
}

.system-stat-item:last-child {
  border-bottom: none;
}

.system-stat-label {
  font-weight: 500;
  color: #6c757d;
}

.system-stat-value {
  font-weight: 500;
  color: #0B2942;
}

/* Background Colors */
.bg-primary {
  background-color: #4da0ff !important;
}

.bg-info {
  background-color: #17a2b8 !important;
}

.bg-success {
  background-color: #28a745 !important;
}

.bg-warning {
  background-color: #ffc107 !important;
}

.bg-indigo {
  background-color: #6610f2 !important;
}

.bg-purple {
  background-color: #8c54ff !important;
}

.bg-secondary {
  background-color: #6c757d !important;
}

.bg-teal {
  background-color: #20c997 !important;
}

.bg-coral {
  background-color: #ff7f50 !important;
}

.bg-cyan {
  background-color: #00bcd4 !important;
}

.bg-orange {
  background-color: #ff9800 !important;
}

.bg-blue {
  background-color: #1e88e5 !important;
}

.bg-green {
  background-color: #2ecc71 !important;
}

@media (max-width: 768px) {
  .admin-stat-card {
    margin-bottom: 1rem;
  }
  
  .admin-actions {
    flex-direction: column;
  }
  
  .admin-action-btn {
    width: 100%;
  }
}
</style>
<template>
    <div class="admin-home">
      <div class="admin-page-header">
        <h2 class="admin-page-title">Dashboard</h2>
        <p class="admin-page-description">Chào mừng đến với hệ thống quản trị tuyển sinh</p>
      </div>
  
      <div class="row mt-4">
        <div class="col-md-3">
          <div class="admin-stat-card">
            <div class="admin-stat-icon">
              <i class="bi bi-people-fill"></i>
            </div>
            <div class="admin-stat-content">
              <h3 class="admin-stat-value">{{ userCount }}</h3>
              <p class="admin-stat-label">Người dùng</p>
            </div>
          </div>
        </div>
        
        <div class="col-md-3">
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
        
        <div class="col-md-3">
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
        
        <div class="col-md-3">
          <div class="admin-stat-card">
            <div class="admin-stat-icon bg-warning">
              <i class="bi bi-bar-chart-fill"></i>
            </div>
            <div class="admin-stat-content">
              <h3 class="admin-stat-value">{{ totalVisitors }}</h3>
              <p class="admin-stat-label">Lượt truy cập</p>
            </div>
          </div>
        </div>
      </div>

      <div class="col-md-3">
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

      <div class="col-md-3">
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

      <div class="col-md-3">
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
  
      <div class="row mt-4">
        <div class="col-12">
          <div class="admin-card">
            <h3 class="admin-card-title">Quản lý người dùng</h3>
            <div class="admin-actions">
              <router-link to="/admins/users" class="admin-action-btn">
                <i class="bi bi-people-fill me-2"></i>
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
      
      <div class="row mt-4">
        <div class="col-md-6">
          <div class="admin-card">
            <h3 class="admin-card-title">Quản lý khoa</h3>
            <div class="admin-actions">
              <router-link to="/admins/faculties" class="admin-action-btn">
                <i class="bi bi-building me-2"></i>
                Danh sách khoa
              </router-link>
              
              <router-link to="/admins/faculties/create" class="admin-action-btn">
                <i class="bi bi-plus-circle me-2"></i>
                Thêm khoa mới
              </router-link>
            </div>
          </div>
        </div>
        
        <div class="col-md-6">
          <div class="admin-card">
            <h3 class="admin-card-title">Quản lý ngành</h3>
            <div class="admin-actions">
              <router-link to="/admins/majors" class="admin-action-btn">
                <i class="bi bi-book me-2"></i>
                Danh sách ngành
              </router-link>
              
              <router-link to="/admins/majors/create" class="admin-action-btn">
                <i class="bi bi-plus-circle me-2"></i>
                Thêm ngành mới
              </router-link>
            </div>
          </div>
        </div>

        <div class="row mt-4">
            <div class="col-12">
                <div class="admin-card">
                    <h3 class="admin-card-title">Quản lý tuyển sinh</h3>
                    <div class="admin-actions">
                        <router-link to="/admins/admission-methods" class="admin-action-btn">
                            <i class="bi bi-clipboard-check me-2"></i>
                            Danh sách phương thức tuyển sinh
                        </router-link>
        
                        <router-link to="/admins/admission-methods/create" class="admin-action-btn">
                            <i class="bi bi-plus-circle me-2"></i>
                            Thêm phương thức mới
                        </router-link>
                    </div>
                </div>
            </div>
        </div>
        <div class="row mt-4">
          <div class="col-md-6">
            <div class="admin-card">
              <h3 class="admin-card-title">Quản lý môn thi</h3>
              <div class="admin-actions">
                <router-link to="/admins/subjects" class="admin-action-btn">
                  <i class="bi bi-journal-text me-2"></i>
                  Danh sách môn thi
                </router-link>
        
                <router-link to="/admins/subjects/create" class="admin-action-btn">
                  <i class="bi bi-plus-circle me-2"></i>
                  Thêm môn thi mới
                </router-link>
              </div>
            </div>
          </div>
  
          <div class="col-md-6">
            <div class="admin-card">
              <h3 class="admin-card-title">Quản lý tổ hợp môn thi</h3>
              <div class="admin-actions">
                <router-link to="/admins/subject-groups" class="admin-action-btn">
                  <i class="bi bi-diagram-3 me-2"></i>
                  Danh sách tổ hợp
                </router-link>
        
                <router-link to="/admins/subject-groups/create" class="admin-action-btn">
                  <i class="bi bi-plus-circle me-2"></i>
                  Thêm tổ hợp mới
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, onMounted } from 'vue'
  import UserController from '@/controllers/admins/UserController'
  import FacultyController from '@/controllers/admins/FacultyController'
  import MajorController from '@/controllers/admins/MajorController'
  import AdmissionMethodController from '@/controllers/admins/AdmissionMethodController'
  import SubjectController from '@/controllers/admins/SubjectController'
  import SubjectGroupController from '@/controllers/admins/SubjectGroupController'
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
  
      onMounted(() => {
        fetchUserCount()
        fetchFacultyCount()
        fetchMajorCount()
        fetchVisitorStats()
        fetchAdmissionMethodCount()
        fetchSubjectCount()
        fetchSubjectGroupCount()
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
      }
    }
  }
  </script>
  
  <style scoped>
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
  
  .admin-stat-card {
    background-color: #fff;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    padding: 1.5rem;
    display: flex;
    align-items: center;
    height: 100%;
    transition: transform 0.3s, box-shadow 0.3s;
  }
  
  .admin-stat-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.08);
  }
  
  .admin-stat-icon {
    width: 60px;
    height: 60px;
    border-radius: 50%;
    background-color: #4da0ff;
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
    font-size: 2rem;
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
  
  .admin-card {
    background-color: #fff;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    height: 100%;
  }
  
  .admin-card-title {
    font-size: 1.25rem;
    font-weight: 600;
    color: #0B2942;
    margin-bottom: 1.25rem;
    padding-bottom: 0.75rem;
    border-bottom: 1px solid #e9ecef;
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
  }
  
  .admin-action-btn:hover {
    background-color: #4da0ff;
    color: #fff;
  }
  .bg-purple {
  background-color: #8c54ff !important;
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

.bg-secondary {
  background-color: #6c757d !important;
}
  
  @media (max-width: 768px) {
    .admin-stat-card {
      margin-bottom: 1rem;
    }
  }
  </style>
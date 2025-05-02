<template>
    <div class="admin-major-courses">
      <div class="admin-page-header d-flex justify-content-between align-items-center">
        <div>
          <h2 class="admin-page-title">Quản lý khung chương trình đào tạo</h2>
          <p class="admin-page-description">Quản lý các khung chương trình đào tạo theo ngành</p>
        </div>
        <router-link to="/admins/major-courses/create" class="btn-create">
          <i class="bi bi-plus-circle me-2"></i>Thêm khung chương trình
        </router-link>
      </div>
  
      <!-- Search and Filter -->
      <div class="admin-card mb-4">
        <div class="row">
          <div class="col-md-4 mb-3">
            <div class="form-group">
              <label for="major-filter">Lọc theo ngành</label>
              <select id="major-filter" v-model="filters.majorId" class="form-select" @change="applyFilters">
                <option value="">Tất cả ngành</option>
                <option v-for="major in majors" :key="major.id" :value="major.id">
                  {{ major.name }}
                </option>
              </select>
            </div>
          </div>
          <div class="col-md-3 mb-3">
            <div class="form-group">
              <label for="year-filter">Lọc theo năm</label>
              <select id="year-filter" v-model="filters.year" class="form-select" @change="applyFilters">
                <option value="">Tất cả năm</option>
                <option v-for="year in availableYears" :key="year" :value="year">
                  {{ year }}
                </option>
              </select>
            </div>
          </div>
          <div class="col-md-3 mb-3">
            <div class="form-group">
              <label for="type-filter">Lọc theo loại đào tạo</label>
              <select id="type-filter" v-model="filters.type" class="form-select" @change="applyFilters">
                <option value="">Tất cả loại</option>
                <option value="Cử nhân">Cử nhân</option>
                <option value="Kỹ sư">Kỹ sư</option>
                <option value="Kiến trúc sư">Kiến trúc sư</option>
              </select>
            </div>
          </div>
          <div class="col-md-2 mb-3">
            <div class="form-group">
              <label for="search-input">Tìm kiếm</label>
              <div class="search-box">
                <i class="bi bi-search search-icon"></i>
                <input 
                  type="text" 
                  id="search-input"
                  v-model="searchQuery" 
                  class="search-input" 
                  placeholder="Tìm kiếm..." 
                  @input="applyFilters"
                >
              </div>
            </div>
          </div>
        </div>
      </div>
  
      <!-- Loading Indicator -->
      <div v-if="loading" class="loading-container">
        <div class="spinner">
          <div class="bounce1"></div>
          <div class="bounce2"></div>
          <div class="bounce3"></div>
        </div>
        <p class="loading-text">Đang tải danh sách khung chương trình...</p>
      </div>
  
      <!-- Error Message -->
      <div v-else-if="error" class="error-message">
        <i class="bi bi-exclamation-triangle-fill error-icon"></i>
        <span>{{ error }}</span>
      </div>
  
      <!-- Major Courses Table -->
      <div v-else class="admin-card">
        <div class="table-responsive">
          <table class="data-table">
            <thead>
              <tr>
                <th width="5%">ID</th>
                <th width="45%">Ngành đào tạo</th>
                <th width="15%">Năm</th>
                <th width="20%">Loại đào tạo</th>
                <th width="15%">Thao tác</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="course in filteredMajorCourses" :key="course.id" class="data-row">
                <td><span class="id-badge">#{{ course.id }}</span></td>
                <td>
                  <span class="major-name">{{ getMajorName(course.major_id) }}</span>
                </td>
                <td><span class="year-badge">{{ course.year }}</span></td>
                <td>
                  <span 
                    class="type-badge" 
                    :class="{
                      'bachelor': course.type === 'Cử nhân',
                      'engineer': course.type === 'Kỹ sư',
                      'architect': course.type === 'Kiến trúc sư'
                    }"
                  >
                    {{ course.type }}
                  </span>
                </td>
                <td>
                  <div class="action-buttons">
                    <router-link :to="`/admins/major-courses/${course.id}`" class="btn-action edit" title="Xem và chỉnh sửa">
                      <i class="bi bi-pencil-square"></i>
                    </router-link>
                    <button 
                      class="btn-action delete"
                      @click="confirmDelete(course)"
                      title="Xóa khung chương trình"
                    >
                      <i class="bi bi-trash"></i>
                    </button>
                  </div>
                </td>
              </tr>
  
              <!-- Empty State -->
              <tr v-if="filteredMajorCourses.length === 0">
                <td colspan="5">
                  <div class="empty-state">
                    <i class="bi bi-mortarboard-fill empty-icon"></i>
                    <h4>Không tìm thấy khung chương trình nào</h4>
                    <p v-if="hasFilters">Thử thay đổi các bộ lọc</p>
                    <p v-else>Chưa có dữ liệu khung chương trình đào tạo trong hệ thống</p>
                    <router-link to="/admins/major-courses/create" class="btn-create-empty">
                      <i class="bi bi-plus-circle me-2"></i>Thêm khung chương trình
                    </router-link>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
  
      <!-- Delete Confirmation Modal -->
      <div v-if="showDeleteModal" class="modal-overlay" @click="cancelDelete">
        <div class="modal-content" @click.stop>
          <div class="modal-header">
            <h4 class="modal-title">Xác nhận xóa khung chương trình</h4>
            <button type="button" class="btn-close" @click="cancelDelete"></button>
          </div>
          <div class="modal-body">
            <p>Bạn có chắc chắn muốn xóa khung chương trình <strong>{{ majorCourseToDelete?.type }}</strong> của ngành <strong>{{ getMajorName(majorCourseToDelete?.major_id) }}</strong> năm <strong>{{ majorCourseToDelete?.year }}</strong>?</p>
            <p class="text-danger">
              <i class="bi bi-exclamation-triangle me-2"></i>
              Thao tác này không thể khôi phục lại!
            </p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn-cancel" @click="cancelDelete">Hủy</button>
            <button type="button" class="btn-delete" @click="deleteMajorCourse" :disabled="isDeleting">
              <span v-if="isDeleting">Đang xóa...</span>
              <span v-else>Xác nhận xóa</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, reactive, computed, onMounted } from 'vue'
  import MajorCourseController from '@/controllers/admins/MajorCourseController'
  import MajorController from '@/controllers/admins/MajorController'
  
  export default {
    name: 'AdminMajorCourses',
    setup() {
      const majorCourses = ref([])
      const filteredMajorCourses = ref([])
      const loading = ref(true)
      const error = ref(null)
      const searchQuery = ref('')
      
      const majors = ref([])
      
      // Delete modal state
      const showDeleteModal = ref(false)
      const majorCourseToDelete = ref(null)
      const isDeleting = ref(false)
  
      // Filters
      const filters = reactive({
        majorId: '',
        year: '',
        type: ''
      })
      
      // Computed to extract available years from data
      const availableYears = computed(() => {
        const years = [...new Set(majorCourses.value.map(mc => mc.year))].sort((a, b) => b - a) // Sort years in descending order
        return years
      })
      
      // Check if any filters are applied
      const hasFilters = computed(() => {
        return filters.majorId || filters.year || filters.type || searchQuery.value
      })
      
      // Get major name by ID
      const getMajorName = (majorId) => {
        const major = majors.value.find(m => m.id === majorId)
        return major ? major.name : 'Không xác định'
      }
  
      // Apply filters and search
      const applyFilters = () => {
        filteredMajorCourses.value = majorCourses.value.filter(course => {
          // Apply major filter
          if (filters.majorId && course.major_id !== parseInt(filters.majorId)) {
            return false
          }
          
          // Apply year filter
          if (filters.year && course.year !== parseInt(filters.year)) {
            return false
          }
          
          // Apply type filter
          if (filters.type && course.type !== filters.type) {
            return false
          }
          
          // Apply search query
          if (searchQuery.value) {
            const majorName = getMajorName(course.major_id).toLowerCase()
            const query = searchQuery.value.toLowerCase()
            
            return majorName.includes(query) || course.type.toLowerCase().includes(query) || course.year.toString().includes(query)
          }
          
          return true
        })
      }
  
      // Show delete confirmation modal
      const confirmDelete = (course) => {
        majorCourseToDelete.value = course
        showDeleteModal.value = true
      }
  
      // Cancel delete action
      const cancelDelete = () => {
        showDeleteModal.value = false
        majorCourseToDelete.value = null
      }
  
      // Delete major course
      const deleteMajorCourse = async () => {
        if (!majorCourseToDelete.value) return
        
        try {
          isDeleting.value = true
          await MajorCourseController.deleteMajorCourse(majorCourseToDelete.value.id)
          
          // Remove from lists
          majorCourses.value = majorCourses.value.filter(mc => mc.id !== majorCourseToDelete.value.id)
          applyFilters() // Update filtered list
          
          // Close modal and reset
          showDeleteModal.value = false
          majorCourseToDelete.value = null
          
          alert('Xóa khung chương trình thành công!')
        } catch (err) {
          alert(`Lỗi: ${err.message}`)
        } finally {
          isDeleting.value = false
        }
      }
  
      // Load major courses and majors
      const loadData = async () => {
        try {
          loading.value = true
          error.value = null
          
          // Load all data in parallel
          const [coursesData, majorsData] = await Promise.all([
            MajorCourseController.getAllMajorCourses(),
            MajorController.getAllMajors()
          ])
          
          majorCourses.value = coursesData
          majors.value = majorsData
          
          // Apply initial filtering
          applyFilters()
        } catch (err) {
          error.value = `Không thể tải dữ liệu: ${err.message}`
        } finally {
          loading.value = false
        }
      }
  
      onMounted(() => {
        loadData()
      })
  
      return {
        majorCourses,
        filteredMajorCourses,
        loading,
        error,
        searchQuery,
        majors,
        showDeleteModal,
        majorCourseToDelete,
        isDeleting,
        filters,
        availableYears,
        hasFilters,
        getMajorName,
        applyFilters,
        confirmDelete,
        cancelDelete,
        deleteMajorCourse
      }
    }
  }
  </script>
  
  <style scoped>
  .admin-major-courses {
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
  
  .admin-card {
    background-color: #fff;
    border-radius: 12px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    transition: all 0.3s ease;
  }
  
  .admin-card:hover {
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
  }
  
  .btn-create {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    background-color: #0B2942;
    color: #fff;
    font-weight: 500;
    padding: 0.75rem 1.25rem;
    border-radius: 8px;
    text-decoration: none;
    transition: all 0.3s;
    border: none;
    cursor: pointer;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  }
  
  .btn-create:hover, .btn-create:focus {
    background-color: #4da0ff;
    color: #fff;
    transform: translateY(-2px);
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
  }
  
  /* Filter and Search Styles */
  .form-group {
    margin-bottom: 1rem;
  }
  
  .form-group label {
    display: block;
    font-weight: 500;
    margin-bottom: 0.5rem;
    color: #0B2942;
  }
  
  .form-select {
    width: 100%;
    padding: 0.75rem;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    font-size: 0.95rem;
    transition: all 0.3s;
    background-color: #fff;
  }
  
  .form-select:focus {
    outline: none;
    border-color: #4da0ff;
    box-shadow: 0 0 0 3px rgba(77, 160, 255, 0.25);
  }
  
  .search-box {
    position: relative;
  }
  
  .search-icon {
    position: absolute;
    left: 15px;
    top: 50%;
    transform: translateY(-50%);
    color: #95a5a6;
  }
  
  .search-input {
    width: 100%;
    padding: 0.75rem 0.75rem 0.75rem 40px;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    font-size: 0.95rem;
    transition: all 0.3s;
  }
  
  .search-input:focus {
    outline: none;
    border-color: #4da0ff;
    box-shadow: 0 0 0 3px rgba(77, 160, 255, 0.25);
  }
  
  /* Loading Animation */
  .loading-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 3rem 0;
  }
  
  .spinner {
    margin: 0 auto;
    width: 70px;
    text-align: center;
  }
  
  .spinner > div {
    width: 18px;
    height: 18px;
    background-color: #0B2942;
    border-radius: 100%;
    display: inline-block;
    animation: sk-bouncedelay 1.4s infinite ease-in-out both;
    margin: 0 3px;
  }
  
  .spinner .bounce1 {
    animation-delay: -0.32s;
  }
  
  .spinner .bounce2 {
    animation-delay: -0.16s;
  }
  
  @keyframes sk-bouncedelay {
    0%, 80%, 100% { transform: scale(0); }
    40% { transform: scale(1.0); }
  }
  
  .loading-text {
    margin-top: 1rem;
    color: #6c757d;
    font-size: 1rem;
  }
  
  /* Error Message */
  .error-message {
    background-color: #f8d7da;
    color: #721c24;
    padding: 1rem;
    border-radius: 8px;
    display: flex;
    align-items: center;
    margin-bottom: 1.5rem;
  }
  
  .error-icon {
    font-size: 1.25rem;
    margin-right: 0.75rem;
  }
  
  /* Table Styling */
  .data-table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
  }
  
  .data-table th {
    background-color: #f8f9fa;
    color: #0B2942;
    font-weight: 600;
    padding: 1rem;
    text-align: left;
    border-bottom: 2px solid #dee2e6;
    position: sticky;
    top: 0;
    z-index: 10;
  }
  
  .data-table td {
    padding: 1rem;
    vertical-align: middle;
    border-bottom: 1px solid #edf2f7;
  }
  
  .data-row {
    transition: background-color 0.3s;
  }
  
  .data-row:hover {
    background-color: rgba(77, 160, 255, 0.05);
  }
  
  .id-badge {
    font-weight: 600;
    color: #6c757d;
  }
  
  .major-name {
    font-weight: 500;
    color: #0B2942;
  }
  
  .year-badge {
    display: inline-block;
    padding: 0.35rem 0.75rem;
    border-radius: 50px;
    font-size: 0.85rem;
    font-weight: 500;
    background-color: #f1f8ff;
    color: #1a73e8;
  }
  
  .type-badge {
    display: inline-block;
    padding: 0.35rem 0.75rem;
    border-radius: 50px;
    font-size: 0.85rem;
    font-weight: 500;
  }
  
  .type-badge.bachelor {
    background-color: #e3f2fd;
    color: #0d6efd;
  }
  
  .type-badge.engineer {
    background-color: #e8f5e9;
    color: #28a745;
  }
  
  .type-badge.architect {
    background-color: #fff8e1;
    color: #ffc107;
  }
  
  .action-buttons {
    display: flex;
    gap: 0.5rem;
  }
  
  .btn-action {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 36px;
    height: 36px;
    border-radius: 8px;
    border: none;
    background-color: transparent;
    transition: all 0.3s ease;
  }
  
  .btn-action.edit {
    color: #0B2942;
  }
  
  .btn-action.delete {
    color: #dc3545;
  }
  
  .btn-action:hover {
    background-color: #f8f9fa;
    transform: translateY(-2px);
  }
  
  .btn-action.edit:hover {
    color: #0B2942;
    background-color: rgba(11, 41, 66, 0.1);
  }
  
  .btn-action.delete:hover {
    color: #dc3545;
    background-color: rgba(220, 53, 69, 0.1);
  }
  
  /* Empty State */
  .empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 3rem 0;
    text-align: center;
  }
  
  .empty-icon {
    font-size: 3rem;
    color: #6c757d;
    margin-bottom: 1rem;
  }
  
  .empty-state h4 {
    font-size: 1.25rem;
    color: #0B2942;
    margin-bottom: 0.5rem;
  }
  
  .empty-state p {
    color: #6c757d;
    margin-bottom: 1.5rem;
  }
  
  .btn-create-empty {
    display: inline-flex;
    align-items: center;
    background-color: #0B2942;
    color: #fff;
    padding: 0.75rem 1.25rem;
    border-radius: 8px;
    text-decoration: none;
    transition: all 0.3s;
  }
  
  .btn-create-empty:hover {
    background-color: #4da0ff;
    color: #fff;
  }
  
  /* Modal Styling */
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1050;
  }
  
  .modal-content {
    background-color: #fff;
    border-radius: 12px;
    width: 90%;
    max-width: 500px;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
    overflow: hidden;
  }
  
  .modal-header {
    padding: 1rem 1.5rem;
    border-bottom: 1px solid #e9ecef;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
  
  .modal-title {
    font-size: 1.25rem;
    color: #0B2942;
    margin: 0;
  }
  
  .btn-close {
    background: transparent;
    border: none;
    font-size: 1.5rem;
    line-height: 1;
    color: #6c757d;
    cursor: pointer;
  }
  
  .modal-body {
    padding: 1.5rem;
  }
  
  .modal-footer {
    padding: 1rem 1.5rem;
    border-top: 1px solid #e9ecef;
    display: flex;
    align-items: center;
    justify-content: flex-end;
    gap: 0.5rem;
  }
  
  .btn-cancel {
    padding: 0.5rem 1rem;
    background-color: #f8f9fa;
    color: #6c757d;
    border: 1px solid #e0e0e0;
    border-radius: 6px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s;
  }
  
  .btn-cancel:hover {
    background-color: #e9ecef;
    color: #0B2942;
  }
  
  .btn-delete {
    padding: 0.5rem 1rem;
    background-color: #dc3545;
    color: #fff;
    border: none;
    border-radius: 6px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s;
  }
  
  .btn-delete:hover:not(:disabled) {
    background-color: #c82333;
  }
  
  .btn-delete:disabled {
    background-color: #e9ecef;
    color: #6c757d;
    cursor: not-allowed;
  }
  
  .text-danger {
    color: #dc3545;
  }
  
  @media (max-width: 768px) {
    .admin-page-header {
      flex-direction: column;
      align-items: flex-start;
      gap: 1rem;
    }
    
    .btn-create {
      width: 100%;
    }
  }
  </style>
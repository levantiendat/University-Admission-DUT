<template>
    <div class="admin-courses">
      <div class="admin-page-header d-flex justify-content-between align-items-center">
        <div>
          <h2 class="admin-page-title">Quản lý lớp học phần</h2>
          <p class="admin-page-description">Quản lý danh sách các lớp học phần trong chương trình đào tạo</p>
        </div>
        <router-link to="/admins/courses/create" class="btn-create">
          <i class="bi bi-plus-circle me-2"></i>Thêm học phần mới
        </router-link>
      </div>
  
      <!-- Search and Filter -->
      <div class="admin-card mb-4">
        <div class="row">
          <div class="col-md-4 mb-3">
            <div class="form-group">
              <label for="credits-filter">Lọc theo số tín chỉ</label>
              <select id="credits-filter" v-model="filters.credits" class="form-select" @change="applyFilters">
                <option value="">Tất cả số tín chỉ</option>
                <option v-for="credit in availableCredits" :key="credit" :value="credit">
                  {{ credit }} tín chỉ
                </option>
              </select>
            </div>
          </div>
          <div class="col-md-8 mb-3">
            <div class="form-group">
              <label for="search-input">Tìm kiếm</label>
              <div class="search-box">
                <i class="bi bi-search search-icon"></i>
                <input 
                  type="text" 
                  id="search-input"
                  v-model="searchQuery" 
                  class="search-input" 
                  placeholder="Tìm kiếm theo mã học phần hoặc tên học phần..." 
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
        <p class="loading-text">Đang tải danh sách lớp học phần...</p>
      </div>
  
      <!-- Error Message -->
      <div v-else-if="error" class="error-message">
        <i class="bi bi-exclamation-triangle-fill error-icon"></i>
        <span>{{ error }}</span>
      </div>
  
      <!-- Courses Table -->
      <div v-else class="admin-card">
        <div class="table-responsive">
          <table class="data-table">
            <thead>
              <tr>
                <th width="5%">ID</th>
                <th width="15%">Mã học phần</th>
                <th width="55%">Tên học phần</th>
                <th width="10%">Số tín chỉ</th>
                <th width="15%">Thao tác</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="course in filteredCourses" :key="course.id" class="data-row">
                <td><span class="id-badge">#{{ course.id }}</span></td>
                <td><span class="course-code">{{ course.course_code }}</span></td>
                <td><span class="course-name">{{ course.name }}</span></td>
                <td><span class="credits-badge">{{ course.credits }}</span></td>
                <td>
                  <div class="action-buttons">
                    <router-link :to="`/admins/courses/${course.id}`" class="btn-action edit" title="Xem và chỉnh sửa">
                      <i class="bi bi-pencil-square"></i>
                    </router-link>
                    <button 
                      class="btn-action delete"
                      @click="confirmDelete(course)"
                      title="Xóa lớp học phần"
                    >
                      <i class="bi bi-trash"></i>
                    </button>
                  </div>
                </td>
              </tr>
  
              <!-- Empty State -->
              <tr v-if="filteredCourses.length === 0">
                <td colspan="5">
                  <div class="empty-state">
                    <i class="bi bi-journals empty-icon"></i>
                    <h4>Không tìm thấy lớp học phần nào</h4>
                    <p v-if="hasFilters">Thử thay đổi các bộ lọc</p>
                    <p v-else>Chưa có dữ liệu lớp học phần trong hệ thống</p>
                    <router-link to="/admins/courses/create" class="btn-create-empty">
                      <i class="bi bi-plus-circle me-2"></i>Thêm học phần mới
                    </router-link>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
  
        <!-- Pagination -->
        <div v-if="totalPages > 1" class="pagination-container">
          <div class="pagination">
            <button 
              class="pagination-button" 
              :class="{ disabled: currentPage === 1 }"
              @click="changePage(currentPage - 1)"
              :disabled="currentPage === 1"
            >
              <i class="bi bi-chevron-left"></i>
            </button>
            
            <button 
              v-for="page in displayedPages" 
              :key="page" 
              class="pagination-button"
              :class="{ active: currentPage === page }"
              @click="changePage(page)"
            >
              {{ page }}
            </button>
            
            <button 
              class="pagination-button" 
              :class="{ disabled: currentPage === totalPages }"
              @click="changePage(currentPage + 1)"
              :disabled="currentPage === totalPages"
            >
              <i class="bi bi-chevron-right"></i>
            </button>
          </div>
        </div>
      </div>
  
      <!-- Delete Confirmation Modal -->
      <div v-if="showDeleteModal" class="modal-overlay" @click="cancelDelete">
        <div class="modal-content" @click.stop>
          <div class="modal-header">
            <h4 class="modal-title">Xác nhận xóa lớp học phần</h4>
            <button type="button" class="btn-close" @click="cancelDelete"></button>
          </div>
          <div class="modal-body">
            <p>Bạn có chắc chắn muốn xóa lớp học phần <strong>{{ courseToDelete?.name }}</strong> ({{ courseToDelete?.course_code }})?</p>
            <p class="text-danger">
              <i class="bi bi-exclamation-triangle me-2"></i>
              Thao tác này không thể khôi phục lại!
            </p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn-cancel" @click="cancelDelete">Hủy</button>
            <button type="button" class="btn-delete" @click="deleteCourse" :disabled="isDeleting">
              <span v-if="isDeleting">Đang xóa...</span>
              <span v-else>Xác nhận xóa</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, reactive, computed, onMounted, watch } from 'vue'
  import CourseController from '@/controllers/admins/CourseController'
  
  export default {
    name: 'AdminCourses',
    setup() {
      const courses = ref([])
      const filteredCourses = ref([])
      const paginatedCourses = ref([])
      const loading = ref(true)
      const error = ref(null)
      const searchQuery = ref('')
      
      // Pagination state
      const itemsPerPage = 10
      const currentPage = ref(1)
      
      // Delete modal state
      const showDeleteModal = ref(false)
      const courseToDelete = ref(null)
      const isDeleting = ref(false)
  
      // Filters
      const filters = reactive({
        credits: '',
      })
      
      // Check if any filters are applied
      const hasFilters = computed(() => {
        return filters.credits || searchQuery.value
      })
      
      // Get unique credits values
      const availableCredits = computed(() => {
        const creditsSet = new Set(courses.value.map(course => course.credits))
        return [...creditsSet].sort((a, b) => a - b)
      })
      
      // Total pages for pagination
      const totalPages = computed(() => {
        return Math.ceil(filteredCourses.value.length / itemsPerPage)
      })
      
      // Calculate displayed page numbers
      const displayedPages = computed(() => {
        const delta = 2; // Number of pages before and after current page
        const pages = []
        
        if (totalPages.value <= 5) {
          // If 5 or fewer pages, show all
          for (let i = 1; i <= totalPages.value; i++) {
            pages.push(i)
          }
        } else {
          // Always show first page
          pages.push(1)
          
          // Calculate start and end page numbers
          let startPage = Math.max(2, currentPage.value - delta)
          let endPage = Math.min(totalPages.value - 1, currentPage.value + delta)
          
          // Add ellipsis if needed
          if (startPage > 2) {
            pages.push('...')
          }
          
          // Add pages around current page
          for (let i = startPage; i <= endPage; i++) {
            pages.push(i)
          }
          
          // Add ellipsis if needed
          if (endPage < totalPages.value - 1) {
            pages.push('...')
          }
          
          // Always show last page
          if (totalPages.value > 1) {
            pages.push(totalPages.value)
          }
        }
        
        return pages
      })
      
      // Apply filters and search
      const applyFilters = () => {
        filteredCourses.value = courses.value.filter(course => {
          // Apply credits filter
          if (filters.credits && course.credits !== parseFloat(filters.credits)) {
            return false
          }
          
          // Apply search query
          if (searchQuery.value) {
            const query = searchQuery.value.toLowerCase()
            return course.name.toLowerCase().includes(query) || 
                   course.course_code.toLowerCase().includes(query)
          }
          
          return true
        })
        
        // Reset to first page when filters change
        currentPage.value = 1
        
        // Update paginated data
        updatePaginatedData()
      }
      
      // Update paginated data based on current page
      const updatePaginatedData = () => {
        const startIndex = (currentPage.value - 1) * itemsPerPage
        const endIndex = startIndex + itemsPerPage
        paginatedCourses.value = filteredCourses.value.slice(startIndex, endIndex)
      }
      
      // Change current page
      const changePage = (page) => {
        if (page === '...') return
        currentPage.value = page
        updatePaginatedData()
      }
  
      // Show delete confirmation modal
      const confirmDelete = (course) => {
        courseToDelete.value = course
        showDeleteModal.value = true
      }
  
      // Cancel delete action
      const cancelDelete = () => {
        showDeleteModal.value = false
        courseToDelete.value = null
      }
  
      // Delete course
      const deleteCourse = async () => {
        if (!courseToDelete.value) return
        
        try {
          isDeleting.value = true
          await CourseController.deleteCourse(courseToDelete.value.id)
          
          // Remove from lists
          courses.value = courses.value.filter(c => c.id !== courseToDelete.value.id)
          applyFilters() // This will also update paginatedCourses
          
          // Close modal and reset
          showDeleteModal.value = false
          courseToDelete.value = null
          
          alert('Xóa lớp học phần thành công!')
        } catch (err) {
          alert(`Lỗi: ${err.message}`)
        } finally {
          isDeleting.value = false
        }
      }
  
      // Load courses
      const loadData = async () => {
        try {
          loading.value = true
          error.value = null
          
          const coursesData = await CourseController.getAllCourses()
          courses.value = coursesData
          
          // Apply initial filtering
          applyFilters()
        } catch (err) {
          error.value = `Không thể tải dữ liệu: ${err.message}`
        } finally {
          loading.value = false
        }
      }
      
      // Watch for current page changes to update paginated data
      watch(currentPage, () => {
        updatePaginatedData()
      })
      
      // Watch filtered data for changes and update paginated data
      watch(filteredCourses, () => {
        updatePaginatedData()
      })
  
      onMounted(() => {
        loadData()
      })
  
      return {
        courses,
        filteredCourses,
        paginatedCourses,
        loading,
        error,
        searchQuery,
        showDeleteModal,
        courseToDelete,
        isDeleting,
        filters,
        currentPage,
        totalPages,
        displayedPages,
        hasFilters,
        availableCredits,
        applyFilters,
        changePage,
        confirmDelete,
        cancelDelete,
        deleteCourse
      }
    }
  }
  </script>
  
  <style scoped>
  .admin-courses {
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
  
  .course-code {
    font-family: monospace;
    font-weight: 500;
    padding: 0.3rem 0.5rem;
    background-color: #f8f9fa;
    border-radius: 4px;
    color: #0B2942;
  }
  
  .course-name {
    font-weight: 500;
    color: #0B2942;
  }
  
  .credits-badge {
    display: inline-block;
    padding: 0.25rem 0.5rem;
    background-color: #e8f5e9;
    color: #28a745;
    font-weight: 600;
    border-radius: 4px;
    text-align: center;
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
  
  /* Pagination */
  .pagination-container {
    display: flex;
    justify-content: center;
    margin-top: 1.5rem;
  }
  
  .pagination {
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }
  
  .pagination-button {
    width: 36px;
    height: 36px;
    border-radius: 8px;
    border: 1px solid #dee2e6;
    background-color: #fff;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #0B2942;
    transition: all 0.3s;
    font-weight: 500;
    cursor: pointer;
  }
  
  .pagination-button.active {
    background-color: #0B2942;
    color: #fff;
    border-color: #0B2942;
  }
  
  .pagination-button:hover:not(.disabled):not(.active) {
    background-color: #f8f9fa;
    border-color: #dee2e6;
  }
  
  .pagination-button.disabled {
    opacity: 0.5;
    cursor: not-allowed;
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
<template>
    <div class="admin-majors">
      <div class="admin-page-header d-flex justify-content-between align-items-center">
        <div>
          <h2 class="admin-page-title">
            {{ facultyId ? `Ngành thuộc ${facultyName}` : 'Quản lý ngành' }}
          </h2>
          <p class="admin-page-description">
            {{ facultyId ? `Danh sách các ngành thuộc khoa ${facultyName}` : 'Quản lý tất cả ngành đào tạo' }}
          </p>
        </div>
        <router-link to="/admins/majors/create" class="btn-create">
          <i class="bi bi-plus-circle me-2"></i>Thêm ngành mới
        </router-link>
      </div>
  
      <!-- Search and Filter -->
      <div class="admin-card mb-4">
        <div class="row align-items-center">
          <div class="col-md-8 mb-3 mb-md-0">
            <div class="search-box">
              <i class="bi bi-search search-icon"></i>
              <input 
                type="text" 
                v-model="searchQuery" 
                class="search-input" 
                placeholder="Tìm kiếm ngành theo tên hoặc mã ngành..." 
                @input="filterMajors"
              >
            </div>
          </div>
          <div class="col-md-4" v-if="!facultyId">
            <div class="filter-box">
              <select v-model="facultyFilter" class="filter-select" @change="filterMajors">
                <option value="">Tất cả khoa</option>
                <option v-for="faculty in faculties" :key="faculty.id" :value="faculty.id">
                  {{ faculty.name }}
                </option>
              </select>
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
        <p class="loading-text">Đang tải danh sách ngành...</p>
      </div>
  
      <!-- Error Message -->
      <div v-else-if="error" class="error-message">
        <i class="bi bi-exclamation-triangle-fill error-icon"></i>
        <span>{{ error }}</span>
      </div>
  
      <!-- Majors Table -->
      <div v-else class="admin-card">
        <div class="table-responsive">
          <table class="data-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Mã ngành</th>
                <th>Tên ngành</th>
                <th v-if="!facultyId">Khoa</th>
                <th>Chỉ tiêu</th>
                <th>Ngày tạo</th>
                <th>Thao tác</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="major in filteredMajors" :key="major.id" class="data-row">
                <td><span class="id-badge">#{{ major.id }}</span></td>
                <td><span class="code-badge">{{ major.major_code }}</span></td>
                <td><span class="name-text">{{ major.name }}</span></td>
                <td v-if="!facultyId">
                  <router-link :to="`/admins/faculties/${major.faculty_id}`" class="faculty-link">
                    {{ getFacultyName(major.faculty_id) }}
                  </router-link>
                </td>
                <td><span class="seats-badge">{{ major.seats }}</span></td>
                <td>{{ formatDate(major.created_at) }}</td>
                <td>
                  <div class="action-buttons">
                    <router-link :to="`/admins/majors/${major.id}`" class="btn-action edit" title="Xem và chỉnh sửa thông tin">
                      <i class="bi bi-pencil-square"></i>
                    </router-link>
                    <button 
                      class="btn-action delete"
                      @click="confirmDelete(major)"
                      title="Xóa ngành"
                    >
                      <i class="bi bi-trash"></i>
                    </button>
                  </div>
                </td>
              </tr>
  
              <!-- Empty State -->
              <tr v-if="filteredMajors.length === 0">
                <td :colspan="facultyId ? 6 : 7">
                  <div class="empty-state">
                    <i class="bi bi-book empty-icon"></i>
                    <h4>Không tìm thấy ngành</h4>
                    <p v-if="searchQuery || facultyFilter">Thử thay đổi bộ lọc hoặc từ khóa tìm kiếm</p>
                    <p v-else>Chưa có ngành nào trong hệ thống</p>
                    <router-link to="/admins/majors/create" class="btn-create-empty">
                      <i class="bi bi-plus-circle me-2"></i>Thêm ngành mới
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
            <h4 class="modal-title">Xác nhận xóa ngành</h4>
            <button type="button" class="btn-close" @click="cancelDelete"></button>
          </div>
          <div class="modal-body">
            <p>Bạn có chắc chắn muốn xóa ngành <strong>{{ majorToDelete?.name }}</strong>?</p>
            <p class="text-danger">
              <i class="bi bi-exclamation-triangle me-2"></i>
              Thao tác này không thể khôi phục lại!
            </p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn-cancel" @click="cancelDelete">Hủy</button>
            <button type="button" class="btn-delete" @click="deleteMajor" :disabled="isDeleting">
              <span v-if="isDeleting">Đang xóa...</span>
              <span v-else>Xác nhận xóa</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, onMounted, computed } from 'vue'
  import { useRouter } from 'vue-router'
  import MajorController from '@/controllers/admins/MajorController'
  import FacultyController from '@/controllers/admins/FacultyController'
  
  export default {
    name: 'AdminMajors',
    props: {
      facultyId: {
        type: [String, Number],
        required: false,
        default: null
      }
    },
    setup(props) {
      const router = useRouter()
      const majors = ref([])
      const faculties = ref([])
      const filteredMajors = ref([])
      const loading = ref(true)
      const error = ref(null)
      const searchQuery = ref('')
      const facultyFilter = ref('')
      const facultyName = ref('')
      
      // Delete modal state
      const showDeleteModal = ref(false)
      const majorToDelete = ref(null)
      const isDeleting = ref(false)
  
      // Format date
      const formatDate = (dateString) => {
        const date = new Date(dateString)
        return new Intl.DateTimeFormat('vi-VN', { 
          day: '2-digit', 
          month: '2-digit', 
          year: 'numeric',
          hour: '2-digit',
          minute: '2-digit'
        }).format(date)
      }
  
      // Get faculty name by id
      const getFacultyName = (id) => {
        const faculty = faculties.value.find(f => f.id === id)
        return faculty ? faculty.name : 'N/A'
      }
  
      // Filter majors based on search query and faculty filter
      const filterMajors = () => {
        if (!majors.value.length) return
        
        filteredMajors.value = majors.value.filter(major => {
          const matchesQuery = !searchQuery.value || 
            major.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
            major.major_code.toLowerCase().includes(searchQuery.value.toLowerCase())
          
          const matchesFaculty = props.facultyId ? 
            parseInt(major.faculty_id) === parseInt(props.facultyId) :
            !facultyFilter.value || parseInt(major.faculty_id) === parseInt(facultyFilter.value)
          
          return matchesQuery && matchesFaculty
        })
      }
  
      // Show delete confirmation modal
      const confirmDelete = (major) => {
        majorToDelete.value = major
        showDeleteModal.value = true
      }
  
      // Cancel delete action
      const cancelDelete = () => {
        showDeleteModal.value = false
        majorToDelete.value = null
      }
  
      // Delete major
      const deleteMajor = async () => {
        if (!majorToDelete.value) return
        
        try {
          isDeleting.value = true
          await MajorController.deleteMajor(majorToDelete.value.id)
          
          // Remove from lists
          majors.value = majors.value.filter(m => m.id !== majorToDelete.value.id)
          filterMajors() // Update filtered list
          
          // Close modal and reset
          showDeleteModal.value = false
          majorToDelete.value = null
          
          alert('Xóa ngành thành công!')
        } catch (err) {
          alert(`Lỗi: ${err.message}`)
        } finally {
          isDeleting.value = false
        }
      }
  
      // Load faculties
      const loadFaculties = async () => {
        try {
          const data = await FacultyController.getAllFaculties()
          faculties.value = data
          
          // If we have a facultyId prop, find the faculty name
          if (props.facultyId) {
            const faculty = data.find(f => parseInt(f.id) === parseInt(props.facultyId))
            if (faculty) {
              facultyName.value = faculty.name
            }
          }
        } catch (err) {
          console.error('Error loading faculties:', err)
        }
      }
  
      // Load majors
      const loadMajors = async () => {
        try {
          loading.value = true
          error.value = null
          
          // Load all majors or majors for a specific faculty
          const data = props.facultyId ?
            await MajorController.getMajorsByFaculty(props.facultyId) :
            await MajorController.getAllMajors()
          
          majors.value = data
          filteredMajors.value = [...data]
        } catch (err) {
          error.value = `Không thể tải danh sách ngành: ${err.message}`
        } finally {
          loading.value = false
        }
      }
  
      onMounted(async () => {
        await loadFaculties()
        await loadMajors()
      })
  
      return {
        majors,
        filteredMajors,
        faculties,
        loading,
        error,
        searchQuery,
        facultyFilter,
        facultyName,
        showDeleteModal,
        majorToDelete,
        isDeleting,
        formatDate,
        getFacultyName,
        filterMajors,
        confirmDelete,
        cancelDelete,
        deleteMajor
      }
    }
  }
  </script>
  
  <style scoped>
  .admin-majors {
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
  
  /* Search Box */
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
  
  /* Filter Box */
  .filter-select {
    width: 100%;
    padding: 0.75rem;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    font-size: 0.95rem;
    appearance: none;
    background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3e%3cpath fill='none' stroke='%23343a40' stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M2 5l6 6 6-6'/%3e%3c/svg%3e");
    background-repeat: no-repeat;
    background-position: right 0.75rem center;
    background-size: 16px 12px;
    transition: all 0.3s;
  }
  
  .filter-select:focus {
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
  
  .code-badge {
    display: inline-block;
    padding: 0.35rem 0.75rem;
    border-radius: 50px;
    font-size: 0.85rem;
    font-weight: 500;
    background-color: #e3f2fd;
    color: #0d6efd;
  }
  
  .name-text {
    font-weight: 500;
    color: #0B2942;
  }
  
  .faculty-link {
    color: #0B2942;
    text-decoration: none;
    font-weight: 500;
    transition: all 0.3s;
  }
  
  .faculty-link:hover {
    color: #4da0ff;
    text-decoration: underline;
  }
  
  .seats-badge {
    display: inline-block;
    padding: 0.25rem 0.75rem;
    border-radius: 50px;
    font-size: 0.85rem;
    font-weight: 500;
    background-color: #e3faeb;
    color: #198754;
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
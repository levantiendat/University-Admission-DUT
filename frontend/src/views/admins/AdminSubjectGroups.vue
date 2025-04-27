<template>
    <div class="admin-subject-groups">
      <div class="admin-page-header d-flex justify-content-between align-items-center">
        <div>
          <h2 class="admin-page-title">Quản lý tổ hợp môn thi</h2>
          <p class="admin-page-description">Quản lý tất cả các tổ hợp môn thi trong hệ thống</p>
        </div>
        <router-link to="/admins/subject-groups/create" class="btn-create">
          <i class="bi bi-plus-circle me-2"></i>Thêm tổ hợp mới
        </router-link>
      </div>
  
      <!-- Search -->
      <div class="admin-card mb-4">
        <div class="row align-items-center">
          <div class="col-md-12">
            <div class="search-box">
              <i class="bi bi-search search-icon"></i>
              <input 
                type="text" 
                v-model="searchQuery" 
                class="search-input" 
                placeholder="Tìm kiếm tổ hợp môn thi theo tên..." 
                @input="filterGroups"
              >
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
        <p class="loading-text">Đang tải danh sách tổ hợp môn thi...</p>
      </div>
  
      <!-- Error Message -->
      <div v-else-if="error" class="error-message">
        <i class="bi bi-exclamation-triangle-fill error-icon"></i>
        <span>{{ error }}</span>
      </div>
  
      <!-- Subject Groups -->
      <div v-else>
        <div class="row">
          <div v-for="group in filteredGroups" :key="group.id" class="col-md-6 col-lg-4 mb-4">
            <div class="subject-group-card">
              <div class="subject-group-header">
                <h3 class="subject-group-name">{{ group.name }}</h3>
                <span class="subject-group-id">#{{ group.id }}</span>
              </div>
              <div class="subject-group-footer">
                <div class="subject-group-date">
                  <i class="bi bi-calendar3 me-1"></i> {{ formatDate(group.created_at) }}
                </div>
                <div class="subject-group-actions">
                  <router-link :to="`/admins/subject-groups/${group.id}`" class="btn-action edit" title="Xem và chỉnh sửa thông tin">
                    <i class="bi bi-pencil-square"></i>
                  </router-link>
                  <button 
                    class="btn-action delete"
                    @click="confirmDelete(group)"
                    title="Xóa tổ hợp môn thi"
                  >
                    <i class="bi bi-trash"></i>
                  </button>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Empty State -->
          <div v-if="filteredGroups.length === 0" class="col-12">
            <div class="empty-state">
              <i class="bi bi-diagram-3 empty-icon"></i>
              <h4>Không tìm thấy tổ hợp môn thi</h4>
              <p v-if="searchQuery">Thử thay đổi từ khóa tìm kiếm</p>
              <p v-else>Chưa có tổ hợp môn thi nào trong hệ thống</p>
              <router-link to="/admins/subject-groups/create" class="btn-create-empty">
                <i class="bi bi-plus-circle me-2"></i>Thêm tổ hợp mới
              </router-link>
            </div>
          </div>
        </div>
      </div>
  
      <!-- Delete Confirmation Modal -->
      <div v-if="showDeleteModal" class="modal-overlay" @click="cancelDelete">
        <div class="modal-content" @click.stop>
          <div class="modal-header">
            <h4 class="modal-title">Xác nhận xóa tổ hợp môn thi</h4>
            <button type="button" class="btn-close" @click="cancelDelete"></button>
          </div>
          <div class="modal-body">
            <p>Bạn có chắc chắn muốn xóa tổ hợp môn thi <strong>{{ groupToDelete?.name }}</strong>?</p>
            <p class="text-danger">
              <i class="bi bi-exclamation-triangle me-2"></i>
              Thao tác này sẽ xóa tổ hợp môn thi và tất cả liên kết của nó với các ngành, và không thể khôi phục lại!
            </p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn-cancel" @click="cancelDelete">Hủy</button>
            <button type="button" class="btn-delete" @click="deleteGroup" :disabled="isDeleting">
              <span v-if="isDeleting">Đang xóa...</span>
              <span v-else>Xác nhận xóa</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, onMounted } from 'vue'
  import SubjectGroupController from '@/controllers/admins/SubjectGroupController'
  
  export default {
    name: 'AdminSubjectGroups',
    setup() {
      const groups = ref([])
      const filteredGroups = ref([])
      const loading = ref(true)
      const error = ref(null)
      const searchQuery = ref('')
      
      // Delete modal state
      const showDeleteModal = ref(false)
      const groupToDelete = ref(null)
      const isDeleting = ref(false)
  
      // Format date
      const formatDate = (dateString) => {
        if (!dateString) return 'N/A';
        const date = new Date(dateString)
        return new Intl.DateTimeFormat('vi-VN', { 
          day: '2-digit', 
          month: '2-digit', 
          year: 'numeric'
        }).format(date)
      }
  
      // Filter groups based on search query
      const filterGroups = () => {
        if (!groups.value.length) return
        
        filteredGroups.value = groups.value.filter(group => {
          const matchesQuery = !searchQuery.value || 
            group.name.toLowerCase().includes(searchQuery.value.toLowerCase())
          
          return matchesQuery
        })
      }
  
      // Show delete confirmation modal
      const confirmDelete = (group) => {
        groupToDelete.value = group
        showDeleteModal.value = true
      }
  
      // Cancel delete action
      const cancelDelete = () => {
        showDeleteModal.value = false
        groupToDelete.value = null
      }
  
      // Delete group
      const deleteGroup = async () => {
        if (!groupToDelete.value) return
        
        try {
          isDeleting.value = true
          await SubjectGroupController.deleteSubjectGroup(groupToDelete.value.id)
          
          // Remove from lists
          groups.value = groups.value.filter(g => g.id !== groupToDelete.value.id)
          filterGroups() // Update filtered list
          
          // Close modal and reset
          showDeleteModal.value = false
          groupToDelete.value = null
          
          alert('Xóa tổ hợp môn thi thành công!')
        } catch (err) {
          alert(`Lỗi: ${err.message}`)
        } finally {
          isDeleting.value = false
        }
      }
  
      // Load groups
      const loadGroups = async () => {
        try {
          loading.value = true
          error.value = null
          
          const data = await SubjectGroupController.getAllSubjectGroups()
          groups.value = data
          filteredGroups.value = [...data]
        } catch (err) {
          error.value = `Không thể tải danh sách tổ hợp môn thi: ${err.message}`
        } finally {
          loading.value = false
        }
      }
  
      onMounted(() => {
        loadGroups()
      })
  
      return {
        groups,
        filteredGroups,
        loading,
        error,
        searchQuery,
        showDeleteModal,
        groupToDelete,
        isDeleting,
        formatDate,
        filterGroups,
        confirmDelete,
        cancelDelete,
        deleteGroup
      }
    }
  }
  </script>
  
  <style scoped>
  .admin-subject-groups {
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
  
  /* Subject Group Card */
  .subject-group-card {
    background-color: #fff;
    border-radius: 12px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
    padding: 1.5rem;
    height: 100%;
    transition: all 0.3s ease;
    display: flex;
    flex-direction: column;
  }
  
  .subject-group-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
  }
  
  .subject-group-header {
    border-bottom: 1px solid #e9ecef;
    padding-bottom: 1rem;
    margin-bottom: 1rem;
  }
  
  .subject-group-name {
    font-size: 1.1rem;
    font-weight: 600;
    color: #0B2942;
    margin-bottom: 0.5rem;
  }
  
  .subject-group-id {
    display: inline-block;
    padding: 0.2rem 0.5rem;
    border-radius: 50px;
    font-size: 0.8rem;
    font-weight: 500;
    background-color: #f1f8ff;
    color: #1a73e8;
  }
  
  .subject-group-footer {
    margin-top: auto;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  .subject-group-date {
    color: #6c757d;
    font-size: 0.85rem;
  }
  
  .subject-group-actions {
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
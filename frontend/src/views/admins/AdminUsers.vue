<template>
    <div class="admin-users">
      <div class="admin-page-header d-flex justify-content-between align-items-center">
        <div>
          <h2 class="admin-page-title">Quản lý người dùng</h2>
          <p class="admin-page-description">Quản lý tất cả tài khoản người dùng trong hệ thống</p>
        </div>
        <router-link to="/admins/users/create" class="btn-create">
          <i class="bi bi-person-plus-fill me-2"></i>Thêm người dùng
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
                placeholder="Tìm kiếm người dùng theo tên, email hoặc số điện thoại..." 
                @input="filterUsers"
              >
            </div>
          </div>
          <div class="col-md-4">
            <div class="filter-box">
              <select v-model="roleFilter" class="filter-select" @change="filterUsers">
                <option value="">Tất cả vai trò</option>
                <option value="user">User</option>
                <option value="instructor">Instructor</option>
              </select>
              <i class="bi bi-funnel-fill filter-icon"></i>
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
        <p class="loading-text">Đang tải danh sách người dùng...</p>
      </div>
  
      <!-- Error Message -->
      <div v-else-if="error" class="error-message">
        <i class="bi bi-exclamation-triangle-fill error-icon"></i>
        <span>{{ error }}</span>
      </div>
  
      <!-- User Table -->
      <div v-else class="admin-card">
        <div class="table-responsive">
          <table class="user-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Họ tên</th>
                <th>Email</th>
                <th>Số điện thoại</th>
                <th>Vai trò</th>
                <th>Ngày tạo</th>
                <th>Thao tác</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="user in filteredUsers" :key="user.id" class="user-row">
                <td><span class="user-id">#{{ user.id }}</span></td>
                <td><span class="user-name">{{ user.name }}</span></td>
                <td><span class="user-email">{{ user.email }}</span></td>
                <td>{{ user.phone_number || 'Chưa cập nhật' }}</td>
                <td>
                  <span :class="['role-badge', user.role === 'user' ? 'role-user' : 'role-instructor']">
                    {{ user.role }}
                  </span>
                </td>
                <td>{{ formatDate(user.created_at) }}</td>
                <td>
                  <div class="action-buttons">
                    <router-link :to="`/admins/users/${user.id}`" class="btn-action edit" title="Chỉnh sửa thông tin">
                      <i class="bi bi-pencil-square"></i>
                    </router-link>
                    <button 
                      class="btn-action toggle-role"
                      @click="toggleUserRole(user)"
                      :title="user.role === 'user' ? 'Chuyển sang Instructor' : 'Chuyển sang User'"
                    >
                      <i :class="user.role === 'user' ? 'bi bi-person-check' : 'bi bi-person'"></i>
                    </button>
                  </div>
                </td>
              </tr>
  
              <!-- Empty State -->
              <tr v-if="filteredUsers.length === 0">
                <td colspan="7">
                  <div class="empty-state">
                    <i class="bi bi-people-fill empty-icon"></i>
                    <h4>Không tìm thấy người dùng</h4>
                    <p v-if="searchQuery || roleFilter">Thử thay đổi bộ lọc hoặc từ khóa tìm kiếm</p>
                    <p v-else>Chưa có người dùng nào trong hệ thống</p>
                    <router-link to="/admins/users/create" class="btn-create-empty">
                      <i class="bi bi-person-plus-fill me-2"></i>Thêm người dùng mới
                    </router-link>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, onMounted } from 'vue'
  import UserController from '@/controllers/admins/UserController'
  
  export default {
    name: 'AdminUsers',
    setup() {
      const users = ref([])
      const filteredUsers = ref([])
      const loading = ref(true)
      const error = ref(null)
      const searchQuery = ref('')
      const roleFilter = ref('')
  
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
  
      // Filter users based on search query and role filter
      const filterUsers = () => {
        if (!users.value.length) return
        
        filteredUsers.value = users.value.filter(user => {
          const matchesQuery = !searchQuery.value || 
            user.name?.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
            user.email?.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
            (user.phone_number && user.phone_number.includes(searchQuery.value))
            
          const matchesRole = !roleFilter.value || user.role === roleFilter.value
          
          return matchesQuery && matchesRole
        })
      }
  
      // Toggle user role between 'user' and 'instructor'
      const toggleUserRole = async (user) => {
        if (user.role === 'admin') {
          alert('Không thể thay đổi quyền của tài khoản admin!')
          return
        }
        
        try {
          const newRole = user.role === 'user' ? 'instructor' : 'user'
          await UserController.updateUserRole(user.id, newRole)
          user.role = newRole
          
          // Update the user in the original array
          const index = users.value.findIndex(u => u.id === user.id)
          if (index !== -1) {
            users.value[index].role = newRole
          }
          
          // Reapply filters
          filterUsers()
          
          alert(`Đã cập nhật vai trò người dùng thành ${newRole}`)
        } catch (error) {
          alert(`Lỗi: ${error.message}`)
        }
      }
  
      // Load users
      const loadUsers = async () => {
        try {
          loading.value = true
          error.value = null
          
          const data = await UserController.getAllUsers()
          users.value = data
          filteredUsers.value = [...data]
        } catch (err) {
          error.value = `Không thể tải danh sách người dùng: ${err.message}`
        } finally {
          loading.value = false
        }
      }
  
      onMounted(() => {
        loadUsers()
      })
  
      return {
        users,
        filteredUsers,
        loading,
        error,
        searchQuery,
        roleFilter,
        formatDate,
        filterUsers,
        toggleUserRole
      }
    }
  }
  </script>
  
  <style scoped>
  .admin-users {
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
  .filter-box {
    position: relative;
  }
  
  .filter-select {
    width: 100%;
    padding: 0.75rem;
    padding-right: 40px;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    font-size: 0.95rem;
    appearance: none;
    background-color: #fff;
    transition: all 0.3s;
  }
  
  .filter-select:focus {
    outline: none;
    border-color: #4da0ff;
    box-shadow: 0 0 0 3px rgba(77, 160, 255, 0.25);
  }
  
  .filter-icon {
    position: absolute;
    right: 15px;
    top: 50%;
    transform: translateY(-50%);
    color: #95a5a6;
    pointer-events: none;
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
  .user-table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
  }
  
  .user-table th {
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
  
  .user-table td {
    padding: 1rem;
    vertical-align: middle;
    border-bottom: 1px solid #edf2f7;
  }
  
  .user-row {
    transition: background-color 0.3s;
  }
  
  .user-row:hover {
    background-color: rgba(77, 160, 255, 0.05);
  }
  
  .user-id {
    font-weight: 600;
    color: #6c757d;
  }
  
  .user-name {
    font-weight: 500;
    color: #0B2942;
  }
  
  .user-email {
    color: #4da0ff;
  }
  
  .role-badge {
    display: inline-block;
    padding: 0.35rem 0.75rem;
    border-radius: 50px;
    font-size: 0.85rem;
    font-weight: 500;
    text-transform: capitalize;
  }
  
  .role-user {
    background-color: #e3f2fd;
    color: #0d6efd;
  }
  
  .role-instructor {
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
    color: #6c757d;
    transition: all 0.3s ease;
  }
  
  .btn-action.edit {
    color: #0B2942;
  }
  
  .btn-action.toggle-role {
    color: #4da0ff;
  }
  
  .btn-action:hover {
    background-color: #f8f9fa;
    transform: translateY(-2px);
  }
  
  .btn-action.edit:hover {
    color: #0B2942;
    background-color: rgba(11, 41, 66, 0.1);
  }
  
  .btn-action.toggle-role:hover {
    color: #4da0ff;
    background-color: rgba(77, 160, 255, 0.1);
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
  
  @media (max-width: 992px) {
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
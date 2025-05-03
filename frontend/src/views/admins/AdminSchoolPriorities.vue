<template>
    <div class="admin-school-priorities">
      <div class="admin-page-header d-flex justify-content-between align-items-center">
        <div>
          <h2 class="admin-page-title">Quản lý khu vực ưu tiên</h2>
          <p class="admin-page-description">Quản lý các tỉnh thành trên toàn quốc</p>
        </div>
        <div>
          <router-link to="/admins/school-priorities/cities/create" class="btn-create">
            <i class="bi bi-plus-circle me-2"></i>Thêm tỉnh/thành phố
          </router-link>
        </div>
      </div>
  
      <!-- Search and Filter -->
      <div class="admin-card mb-4">
        <div class="row">
          <div class="col-md-12">
            <div class="form-group">
              <label for="search-input">Tìm kiếm tỉnh/thành phố</label>
              <div class="search-box">
                <i class="bi bi-search search-icon"></i>
                <input 
                  type="text" 
                  id="search-input" 
                  v-model="searchQuery" 
                  class="search-input" 
                  placeholder="Tìm theo mã hoặc tên tỉnh/thành phố..." 
                  @input="filterCities"
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
        <p class="loading-text">Đang tải danh sách tỉnh/thành phố...</p>
      </div>
  
      <!-- Error Message -->
      <div v-else-if="error" class="error-message">
        <i class="bi bi-exclamation-triangle-fill error-icon"></i>
        <span>{{ error }}</span>
      </div>
  
      <!-- Cities List -->
      <div v-else class="admin-card">
        <div class="d-flex justify-content-between align-items-center mb-3">
          <h3 class="section-title mb-0">Danh sách tỉnh/thành phố</h3>
          <div class="results-count">Hiển thị {{ filteredCities.length }} tỉnh/thành phố</div>
        </div>
  
        <div class="table-responsive">
          <table class="data-table">
            <thead>
              <tr>
                <th width="10%">Mã tỉnh</th>
                <th width="65%">Tên tỉnh/thành phố</th>
                <th width="15%">Số quận/huyện</th>
                <th width="10%">Thao tác</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="city in filteredCities" :key="city.id" class="data-row">
                <td><span class="city-code">{{ city.city_code }}</span></td>
                <td>
                  <router-link :to="`/admins/school-priorities/cities/${city.id}`" class="city-name-link">
                    {{ city.name }}
                  </router-link>
                </td>
                <td>
                  <span class="district-count">{{ getDistrictCountForCity(city.id) }}</span>
                </td>
                <td>
                  <div class="action-buttons">
                    <router-link 
                      :to="`/admins/school-priorities/cities/${city.id}`" 
                      class="btn-action edit" 
                      title="Xem và chỉnh sửa"
                    >
                      <i class="bi bi-pencil-square"></i>
                    </router-link>
                    <button 
                      class="btn-action delete"
                      @click="confirmDeleteCity(city)"
                      title="Xóa tỉnh/thành phố"
                    >
                      <i class="bi bi-trash"></i>
                    </button>
                  </div>
                </td>
              </tr>
  
              <!-- Empty State -->
              <tr v-if="filteredCities.length === 0">
                <td colspan="4">
                  <div class="empty-state">
                    <i class="bi bi-geo-fill empty-icon"></i>
                    <h4>Không tìm thấy tỉnh/thành phố nào</h4>
                    <p v-if="searchQuery">Thử tìm kiếm với từ khóa khác</p>
                    <p v-else>Chưa có dữ liệu tỉnh/thành phố trong hệ thống</p>
                    <router-link to="/admins/school-priorities/cities/create" class="btn-create-empty">
                      <i class="bi bi-plus-circle me-2"></i>Thêm tỉnh/thành phố mới
                    </router-link>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
  
      <!-- Delete City Confirmation Modal -->
      <div v-if="showDeleteCityModal" class="modal-overlay" @click="cancelDeleteCity">
        <div class="modal-content" @click.stop>
          <div class="modal-header">
            <h4 class="modal-title">Xác nhận xóa tỉnh/thành phố</h4>
            <button type="button" class="btn-close" @click="cancelDeleteCity"></button>
          </div>
          <div class="modal-body">
            <p>Bạn có chắc chắn muốn xóa tỉnh/thành phố <strong>{{ cityToDelete?.name }}</strong>?</p>
            <p class="text-warning">
              <i class="bi bi-exclamation-triangle me-2"></i>
              Việc xóa tỉnh/thành phố sẽ xóa tất cả quận/huyện và trường học thuộc tỉnh/thành phố này!
            </p>
            <p class="text-danger">
              <i class="bi bi-exclamation-triangle me-2"></i>
              Thao tác này không thể khôi phục lại!
            </p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn-cancel" @click="cancelDeleteCity">Hủy</button>
            <button type="button" class="btn-delete" @click="deleteCity" :disabled="isDeleting">
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
  import { useRouter } from 'vue-router'
  import SchoolPriorityController from '@/controllers/admins/SchoolPriorityController'
  
  export default {
    name: 'AdminSchoolPriorities',
    setup() {
      // States
      const loading = ref(true)
      const error = ref(null)
      const cities = ref([])
      const filteredCities = ref([])
      const districts = ref([])
      const searchQuery = ref('')
      
      // Delete modals
      const showDeleteCityModal = ref(false)
      const cityToDelete = ref(null)
      const isDeleting = ref(false)
      
      // Get district count for each city
      const getDistrictCountForCity = (cityId) => {
        return districts.value.filter(d => d.city_id === cityId).length
      }
      
      // Filter cities based on search
      const filterCities = () => {
        if (!searchQuery.value) {
          filteredCities.value = cities.value
          return
        }
        
        const query = searchQuery.value.toLowerCase()
        filteredCities.value = cities.value.filter(city => {
          const matchesCode = city.city_code.toLowerCase().includes(query)
          const matchesName = city.name.toLowerCase().includes(query)
          return matchesCode || matchesName
        })
      }
      
      // Delete handlers
      const confirmDeleteCity = (city) => {
        cityToDelete.value = city
        showDeleteCityModal.value = true
      }
      
      const cancelDeleteCity = () => {
        showDeleteCityModal.value = false
        cityToDelete.value = null
      }
      
      const deleteCity = async () => {
        if (!cityToDelete.value) return
        
        try {
          isDeleting.value = true
          await SchoolPriorityController.deleteCity(cityToDelete.value.id)
          
          // Update local state
          cities.value = cities.value.filter(c => c.id !== cityToDelete.value.id)
          filteredCities.value = filteredCities.value.filter(c => c.id !== cityToDelete.value.id)
          
          // Also remove associated districts from local state
          districts.value = districts.value.filter(d => d.city_id !== cityToDelete.value.id)
          
          showDeleteCityModal.value = false
          cityToDelete.value = null
          
          alert('Xóa tỉnh/thành phố thành công!')
        } catch (err) {
          alert(`Lỗi: ${err.message}`)
        } finally {
          isDeleting.value = false
        }
      }
      
      // Load initial data
      const loadData = async () => {
        try {
          loading.value = true
          error.value = null
          
          // Load all cities
          const citiesData = await SchoolPriorityController.getAllCities()
          cities.value = citiesData
          filteredCities.value = citiesData
          
          // Load all districts for district counts
          let allDistricts = []
          for (const city of citiesData) {
            const cityDistricts = await SchoolPriorityController.getDistrictsByCity(city.id)
            allDistricts = [...allDistricts, ...cityDistricts]
          }
          districts.value = allDistricts
          
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
        loading,
        error,
        cities,
        filteredCities,
        districts,
        searchQuery,
        showDeleteCityModal,
        cityToDelete,
        isDeleting,
        getDistrictCountForCity,
        filterCities,
        confirmDeleteCity,
        cancelDeleteCity,
        deleteCity
      }
    }
  }
  </script>
  
  <style scoped>
  .admin-school-priorities {
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
  
  .section-title {
    font-size: 1.25rem;
    font-weight: 600;
    color: #0B2942;
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
  .results-count {
    color: #6c757d;
    font-size: 0.9rem;
  }
  
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
  
  .city-code {
    font-weight: 600;
    color: #0B2942;
    display: inline-block;
    background: #f8f9fa;
    padding: 0.25rem 0.5rem;
    border-radius: 4px;
    font-size: 0.85rem;
  }
  
  .city-name-link {
    font-weight: 500;
    color: #0B2942;
    text-decoration: none;
    position: relative;
    transition: color 0.2s;
  }
  
  .city-name-link:hover {
    color: #4da0ff;
  }
  
  .city-name-link:hover::after {
    content: "";
    position: absolute;
    bottom: -2px;
    left: 0;
    width: 100%;
    height: 1px;
    background-color: #4da0ff;
  }
  
  .district-count {
    display: inline-block;
    background-color: #e9ecef;
    color: #495057;
    font-size: 0.85rem;
    font-weight: 600;
    padding: 0.35rem 0.65rem;
    border-radius: 50px;
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
    cursor: pointer;
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
    background-color: rgba(11, 41, 66, 0.1);
  }
  
  .btn-action.delete:hover {
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
    margin-bottom: 1.5rem;
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
    border: none;
    cursor: pointer;
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
  
  .btn-delete {
    padding: 0.75rem 1.5rem;
    background-color: #dc3545;
    border: none;
    border-radius: 8px;
    color: #fff;
    font-weight: 500;
    transition: all 0.3s;
    display: inline-flex;
    align-items: center;
  }
  
  .btn-delete:hover:not(:disabled) {
    background-color: #c82333;
  }
  
  .btn-delete:disabled {
    background-color: #e9ecef;
    color: #6c757d;
    cursor: not-allowed;
  }
  
  .btn-cancel {
    padding: 0.75rem 1.5rem;
    background-color: #f8f9fa;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    color: #6c757d;
    font-weight: 500;
    transition: all 0.3s;
    display: inline-flex;
    align-items: center;
  }
  
  .btn-cancel:hover {
    background-color: #e9ecef;
    color: #0B2942;
  }
  
  .text-danger {
    color: #dc3545 !important;
  }
  
  .text-warning {
    color: #ffc107 !important;
  }
  
  /* Responsive adjustments */
  @media (max-width: 768px) {
    .admin-page-header {
      flex-direction: column;
      gap: 1rem;
      align-items: flex-start !important;
    }
  
    .action-buttons {
      justify-content: flex-end;
    }
  }
  </style>
<template>
    <div class="admin-district-detail">
      <div class="admin-page-header">
        <div class="d-flex align-items-center">
          <router-link to="/admins/school-priorities" class="btn-back">
            <i class="bi bi-arrow-left"></i>
          </router-link>
          <div>
            <h2 class="admin-page-title">Chi tiết quận/huyện</h2>
            <p class="admin-page-description">Xem và chỉnh sửa thông tin quận/huyện</p>
          </div>
        </div>
      </div>
  
      <!-- Loading State -->
      <div v-if="loading" class="loading-container">
        <div class="spinner">
          <div class="bounce1"></div>
          <div class="bounce2"></div>
          <div class="bounce3"></div>
        </div>
        <p class="loading-text">Đang tải thông tin quận/huyện...</p>
      </div>
  
      <!-- Error State -->
      <div v-else-if="error" class="error-message">
        <i class="bi bi-exclamation-triangle-fill error-icon"></i>
        <span>{{ error }}</span>
      </div>
  
      <div v-else class="admin-card">
        <form @submit.prevent="updateDistrict" class="district-form">
          <div class="form-group">
            <label for="city-id">Tỉnh/Thành phố <span class="required">*</span></label>
            <select 
              id="city-id" 
              v-model="formData.city_id" 
              class="form-select" 
              :class="{ 'is-invalid': errors.city_id }"
              required
            >
              <option v-for="city in cities" :key="city.id" :value="city.id">
                {{ city.name }}
              </option>
            </select>
            <div v-if="errors.city_id" class="invalid-feedback">
              {{ errors.city_id }}
            </div>
          </div>
  
          <div class="form-group">
            <label for="district-code">Mã quận/huyện <span class="required">*</span></label>
            <input 
              type="text" 
              id="district-code" 
              v-model="formData.district_code" 
              class="form-control" 
              :class="{ 'is-invalid': errors.district_code }"
              placeholder="Nhập mã quận/huyện" 
              required
            >
            <div v-if="errors.district_code" class="invalid-feedback">
              {{ errors.district_code }}
            </div>
          </div>
  
          <div class="form-group">
            <label for="name">Tên quận/huyện <span class="required">*</span></label>
            <input 
              type="text" 
              id="name" 
              v-model="formData.name" 
              class="form-control" 
              :class="{ 'is-invalid': errors.name }" 
              placeholder="Nhập tên quận/huyện" 
              required
            >
            <div v-if="errors.name" class="invalid-feedback">
              {{ errors.name }}
            </div>
          </div>
  
          <div class="meta-info">
            <div class="meta-item">
              <span class="meta-label">ID:</span>
              <span class="meta-value">#{{ district.id }}</span>
            </div>
            <div class="meta-item">
              <span class="meta-label">Ngày tạo:</span>
              <span class="meta-value">{{ formatDate(district.created_at) }}</span>
            </div>
            <div class="meta-item">
              <span class="meta-label">Cập nhật:</span>
              <span class="meta-value">{{ formatDate(district.updated_at) }}</span>
            </div>
          </div>
  
          <div v-if="updateError" class="alert alert-danger">
            <i class="bi bi-exclamation-triangle-fill me-2"></i>
            {{ updateError }}
          </div>
  
          <div class="form-actions">
            <button type="submit" class="btn-save" :disabled="isUpdating">
              <i class="bi bi-check-circle me-2"></i>
              {{ isUpdating ? 'Đang lưu...' : 'Lưu thay đổi' }}
            </button>
            <button type="button" class="btn-delete" @click="confirmDelete">
              <i class="bi bi-trash me-2"></i>
              Xóa quận/huyện
            </button>
            <router-link to="/admins/school-priorities" class="btn-cancel">
              <i class="bi bi-x-circle me-2"></i>
              Hủy
            </router-link>
          </div>
        </form>
      </div>
  
      <!-- Schools Section -->
      <div v-if="!loading && !error" class="admin-card mt-4">
        <div class="d-flex justify-content-between align-items-center mb-3">
          <h3 class="section-title mb-0">Trường học thuộc quận/huyện này</h3>
          <router-link :to="`/admins/school-priorities/schools/create?districtId=${districtId}`" class="btn-add">
            <i class="bi bi-plus-circle me-2"></i>Thêm trường học mới
          </router-link>
        </div>
  
        <!-- Loading Schools -->
        <div v-if="loadingSchools" class="loading-container py-3">
          <div class="spinner">
            <div class="bounce1"></div>
            <div class="bounce2"></div>
            <div class="bounce3"></div>
          </div>
        </div>
        
        <!-- Schools Table -->
        <div v-else-if="schools.length > 0" class="table-responsive">
          <table class="data-table">
            <thead>
              <tr>
                <th width="15%">Mã trường</th>
                <th width="45%">Tên trường</th>
                <th width="20%">Khu vực ưu tiên</th>
                <th width="20%">Thao tác</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="school in schools" :key="school.id" class="data-row">
                <td><span class="school-code">{{ school.school_code }}</span></td>
                <td>
                  <span class="school-name">{{ school.name }}</span>
                  <span class="school-address">{{ school.address }}</span>
                </td>
                <td>
                  <span :class="['priority-badge', getPriorityClass(school.priority_area)]">
                    {{ school.priority_area }}
                  </span>
                </td>
                <td>
                  <div class="action-buttons">
                    <router-link 
                      :to="`/admins/school-priorities/schools/${school.id}`" 
                      class="btn-action edit" 
                      title="Xem và chỉnh sửa"
                    >
                      <i class="bi bi-pencil-square"></i>
                    </router-link>
                    <button 
                      class="btn-action delete"
                      @click="confirmDeleteSchool(school)"
                      title="Xóa trường học"
                    >
                      <i class="bi bi-trash"></i>
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        
        <!-- Empty Schools State -->
        <div v-else class="empty-state">
          <i class="bi bi-building-fill empty-icon"></i>
          <h4>Chưa có trường học nào thuộc quận/huyện này</h4>
          <router-link :to="`/admins/school-priorities/schools/create?districtId=${districtId}`" class="btn-create-empty">
            <i class="bi bi-plus-circle me-2"></i>Thêm trường học mới
          </router-link>
        </div>
      </div>
  
      <!-- Delete District Confirmation Modal -->
      <div v-if="showDeleteModal" class="modal-overlay" @click="cancelDelete">
        <div class="modal-content" @click.stop>
          <div class="modal-header">
            <h4 class="modal-title">Xác nhận xóa quận/huyện</h4>
            <button type="button" class="btn-close" @click="cancelDelete"></button>
          </div>
          <div class="modal-body">
            <p>Bạn có chắc chắn muốn xóa quận/huyện <strong>{{ district.name }}</strong>?</p>
            <p class="text-warning">
              <i class="bi bi-exclamation-triangle me-2"></i>
              Việc xóa quận/huyện sẽ xóa tất cả trường học thuộc quận/huyện này!
            </p>
            <p class="text-danger">
              <i class="bi bi-exclamation-triangle me-2"></i>
              Thao tác này không thể khôi phục lại!
            </p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn-cancel" @click="cancelDelete">Hủy</button>
            <button type="button" class="btn-delete" @click="deleteDistrict" :disabled="isDeleting">
              <span v-if="isDeleting">Đang xóa...</span>
              <span v-else>Xác nhận xóa</span>
            </button>
          </div>
        </div>
      </div>
  
      <!-- Delete School Confirmation Modal -->
      <div v-if="showDeleteSchoolModal" class="modal-overlay" @click="cancelDeleteSchool">
        <div class="modal-content" @click.stop>
          <div class="modal-header">
            <h4 class="modal-title">Xác nhận xóa trường học</h4>
            <button type="button" class="btn-close" @click="cancelDeleteSchool"></button>
          </div>
          <div class="modal-body">
            <p>Bạn có chắc chắn muốn xóa trường <strong>{{ schoolToDelete?.name }}</strong>?</p>
            <p class="text-danger">
              <i class="bi bi-exclamation-triangle me-2"></i>
              Thao tác này không thể khôi phục lại!
            </p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn-cancel" @click="cancelDeleteSchool">Hủy</button>
            <button type="button" class="btn-delete" @click="deleteSchool" :disabled="isDeleting">
              <span v-if="isDeleting">Đang xóa...</span>
              <span v-else>Xác nhận xóa</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, reactive, onMounted } from 'vue'
  import { useRouter } from 'vue-router'
  import SchoolPriorityController from '@/controllers/admins/SchoolPriorityController'
  
  export default {
    name: 'AdminDistrictDetail',
    props: {
      districtId: {
        type: [String, Number],
        required: true
      }
    },
    setup(props) {
      const router = useRouter()
      const district = ref({})
      const formData = reactive({
        district_code: '',
        name: '',
        city_id: ''
      })
      const cities = ref([])
      const schools = ref([])
      const loading = ref(true)
      const loadingSchools = ref(true)
      const error = ref(null)
      const errors = reactive({
        district_code: '',
        name: '',
        city_id: ''
      })
      const updateError = ref(null)
      const isUpdating = ref(false)
  
      // Delete modal state
      const showDeleteModal = ref(false)
      const isDeleting = ref(false)
      
      // Delete school modal state
      const showDeleteSchoolModal = ref(false)
      const schoolToDelete = ref(null)
      
      // Format date
      const formatDate = (dateString) => {
        if (!dateString) return 'N/A'
        
        const date = new Date(dateString)
        return new Intl.DateTimeFormat('vi-VN', { 
          day: '2-digit', 
          month: '2-digit', 
          year: 'numeric',
          hour: '2-digit',
          minute: '2-digit'
        }).format(date)
      }
      
      // Get priority class for styling
      const getPriorityClass = (priorityArea) => {
        switch (priorityArea) {
          case 'KV1': return 'priority-1'
          case 'KV2': return 'priority-2'
          case 'KV2NT': return 'priority-2nt'
          case 'KV3': return 'priority-3'
          default: return ''
        }
      }
      
      // Load district data
      const loadDistrictData = async () => {
        try {
          loading.value = true
          
          // Load cities first
          const citiesData = await SchoolPriorityController.getAllCities()
          cities.value = citiesData
          
          // Then load district
          const districtData = await SchoolPriorityController.getDistrictById(props.districtId)
          district.value = districtData
          
          // Set form data
          formData.district_code = districtData.district_code
          formData.name = districtData.name
          formData.city_id = districtData.city_id
          
          // Load schools
          loadSchools()
        } catch (err) {
          error.value = `Không thể tải thông tin quận/huyện: ${err.message}`
        } finally {
          loading.value = false
        }
      }
      
      // Load schools
      const loadSchools = async () => {
        try {
          loadingSchools.value = true
          
          const schoolsData = await SchoolPriorityController.getSchoolsByDistrict(props.districtId)
          schools.value = schoolsData
        } catch (err) {
          console.error(`Error loading schools: ${err.message}`)
        } finally {
          loadingSchools.value = false
        }
      }
      
      // Validate form
      const validateForm = () => {
        let isValid = true
        
        // Reset errors
        errors.district_code = ''
        errors.name = ''
        errors.city_id = ''
        updateError.value = null
        
        // Validate city_id
        if (!formData.city_id) {
          errors.city_id = 'Vui lòng chọn tỉnh/thành phố'
          isValid = false
        }
        
        // Validate district_code
        if (!formData.district_code || formData.district_code.trim() === '') {
          errors.district_code = 'Mã quận/huyện không được để trống'
          isValid = false
        }
        
        // Validate name
        if (!formData.name || formData.name.trim() === '') {
          errors.name = 'Tên quận/huyện không được để trống'
          isValid = false
        }
        
        return isValid
      }
      
      // Update district
      const updateDistrict = async () => {
        if (!validateForm()) {
          return
        }
        
        try {
          isUpdating.value = true
          
          await SchoolPriorityController.updateDistrict(props.districtId, {
            district_code: formData.district_code.trim(),
            name: formData.name.trim(),
            city_id: parseInt(formData.city_id)
          })
          
          // Update local state
          district.value.district_code = formData.district_code.trim()
          district.value.name = formData.name.trim()
          district.value.city_id = parseInt(formData.city_id)
          district.value.updated_at = new Date().toISOString()
          
          alert('Cập nhật quận/huyện thành công!')
        } catch (err) {
          updateError.value = err.message
        } finally {
          isUpdating.value = false
        }
      }
      
      // Delete district
      const confirmDelete = () => {
        showDeleteModal.value = true
      }
      
      const cancelDelete = () => {
        showDeleteModal.value = false
      }
      
      const deleteDistrict = async () => {
        try {
          isDeleting.value = true
          
          await SchoolPriorityController.deleteDistrict(props.districtId)
          
          alert('Xóa quận/huyện thành công!')
          router.push('/admins/school-priorities')
        } catch (err) {
          alert(`Lỗi: ${err.message}`)
        } finally {
          isDeleting.value = false
          showDeleteModal.value = false
        }
      }
      
      // Delete school
      const confirmDeleteSchool = (school) => {
        schoolToDelete.value = school
        showDeleteSchoolModal.value = true
      }
      
      const cancelDeleteSchool = () => {
        showDeleteSchoolModal.value = false
        schoolToDelete.value = null
      }
      
      const deleteSchool = async () => {
        if (!schoolToDelete.value) return
        
        try {
          isDeleting.value = true
          
          await SchoolPriorityController.deleteSchool(schoolToDelete.value.id)
          
          // Update local state
          schools.value = schools.value.filter(s => s.id !== schoolToDelete.value.id)
          
          alert('Xóa trường học thành công!')
        } catch (err) {
          alert(`Lỗi: ${err.message}`)
        } finally {
          isDeleting.value = false
          showDeleteSchoolModal.value = false
          schoolToDelete.value = null
        }
      }
      
      onMounted(() => {
        loadDistrictData()
      })
  
      return {
        district,
        formData,
        cities,
        schools,
        loading,
        loadingSchools,
        error,
        errors,
        updateError,
        isUpdating,
        showDeleteModal,
        isDeleting,
        showDeleteSchoolModal,
        schoolToDelete,
        formatDate,
        getPriorityClass,
        validateForm,
        updateDistrict,
        confirmDelete,
        cancelDelete,
        deleteDistrict,
        confirmDeleteSchool,
        cancelDeleteSchool,
        deleteSchool
      }
    }
  }
  </script>
  
  <style scoped>
  .admin-district-detail {
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
  
  .btn-back {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background-color: #f8f9fa;
    color: #0B2942;
    text-decoration: none;
    margin-right: 1rem;
    transition: all 0.2s ease;
  }
  
  .btn-back:hover {
    background-color: #e9ecef;
    transform: translateX(-2px);
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
  
  .district-form {
    max-width: 700px;
    margin: 0 auto;
  }
  
  .form-group {
    margin-bottom: 1.5rem;
  }
  
  .form-group label {
    display: block;
    font-weight: 500;
    margin-bottom: 0.5rem;
    color: #0B2942;
  }
  
  .required {
    color: #dc3545;
  }
  
  .form-control, .form-select {
    width: 100%;
    padding: 0.75rem;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    font-size: 0.95rem;
    transition: all 0.3s;
  }
  
  .form-control:focus, .form-select:focus {
    outline: none;
    border-color: #4da0ff;
    box-shadow: 0 0 0 3px rgba(77, 160, 255, 0.25);
  }
  
  .form-control.is-invalid, .form-select.is-invalid {
    border-color: #dc3545;
  }
  
  .invalid-feedback {
    color: #dc3545;
    font-size: 0.875em;
    margin-top: 0.25rem;
  }
  
  .meta-info {
    margin: 1.5rem 0;
    padding: 1rem;
    background-color: #f8f9fa;
    border-radius: 8px;
  }
  
  .meta-item {
    display: flex;
    justify-content: space-between;
    margin-bottom: 0.5rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid #e9ecef;
  }
  
  .meta-item:last-child {
    margin-bottom: 0;
    padding-bottom: 0;
    border-bottom: none;
  }
  
  .meta-label {
    font-weight: 500;
    color: #6c757d;
  }
  
  .meta-value {
    color: #0B2942;
    font-weight: 500;
  }
  
  .form-actions {
    display: flex;
    gap: 1rem;
    margin-top: 2rem;
  }
  
  .btn-save {
    padding: 0.75rem 1.5rem;
    background-color: #0B2942;
    border: none;
    border-radius: 8px;
    color: #fff;
    font-weight: 500;
    transition: all 0.3s;
    display: inline-flex;
    align-items: center;
    cursor: pointer;
  }
  
  .btn-save:hover:not(:disabled) {
    background-color: #4da0ff;
  }
  
  .btn-save:disabled {
    background-color: #e9ecef;
    color: #6c757d;
    cursor: not-allowed;
  }
  
  .btn-delete {
    padding: 0.75rem 1.5rem;
    background-color: #f8f9fa;
    border: 1px solid #dc3545;
    border-radius: 8px;
    color: #dc3545;
    font-weight: 500;
    transition: all 0.3s;
    display: inline-flex;
    align-items: center;
    cursor: pointer;
  }
  
  .btn-delete:hover:not(:disabled) {
    background-color: #dc3545;
    color: white;
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
    text-decoration: none;
  }
  
  .btn-cancel:hover {
    background-color: #e9ecef;
    color: #0B2942;
  }
  
  .btn-add {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    background-color: #0B2942;
    color: #fff;
    font-weight: 500;
    padding: 0.5rem 1rem;
    border-radius: 8px;
    text-decoration: none;
    transition: all 0.3s;
    border: none;
    cursor: pointer;
    font-size: 0.875rem;
  }
  
  .btn-add:hover, .btn-add:focus {
    background-color: #4da0ff;
    color: #fff;
  }
  
  .alert {
    padding: 1rem;
    margin-bottom: 1rem;
    border-radius: 8px;
  }
  
  .alert-danger {
    background-color: #f8d7da;
    color: #721c24;
    border: 1px solid #f5c2c7;
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
  .section-title {
    font-size: 1.25rem;
    font-weight: 600;
    color: #0B2942;
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
  
  .school-code {
    font-weight: 600;
    color: #0B2942;
    display: inline-block;
    background: #f8f9fa;
    padding: 0.25rem 0.5rem;
    border-radius: 4px;
    font-size: 0.85rem;
  }
  
  .school-name {
    font-weight: 500;
    color: #0B2942;
    display: block;
  }
  
  .school-address {
    font-size: 0.85rem;
    color: #6c757d;
    display: block;
    margin-top: 0.25rem;
  }
  
  .priority-badge {
    display: inline-block;
    padding: 0.3rem 0.6rem;
    border-radius: 50px;
    font-size: 0.85rem;
    font-weight: 600;
    text-align: center;
  }
  
  .priority-1 {
    background-color: #d1e7dd;
    color: #0f5132;
  }
  
  .priority-2 {
    background-color: #fff3cd;
    color: #856404;
  }
  
  .priority-2nt {
    background-color: #e8f5e9;
    color: #2e7d32;
  }
  
  .priority-3 {
    background-color: #f8d7da;
    color: #842029;
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
  
  .text-danger {
    color: #dc3545 !important;
  }
  
  .text-warning {
    color: #ffc107 !important;
  }
  
  @media (max-width: 768px) {
    .form-actions {
      flex-direction: column;
    }
    
    .btn-save, .btn-cancel, .btn-delete {
      width: 100%;
    }
  }
  </style>
<template>
    <div class="admin-school-detail">
      <div class="admin-page-header">
        <div class="d-flex align-items-center">
          <router-link to="/admins/school-priorities" class="btn-back">
            <i class="bi bi-arrow-left"></i>
          </router-link>
          <div>
            <h2 class="admin-page-title">Chi tiết trường học</h2>
            <p class="admin-page-description">Xem và chỉnh sửa thông tin trường học</p>
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
        <p class="loading-text">Đang tải thông tin trường học...</p>
      </div>
  
      <!-- Error State -->
      <div v-else-if="error" class="error-message">
        <i class="bi bi-exclamation-triangle-fill error-icon"></i>
        <span>{{ error }}</span>
      </div>
  
      <div v-else class="admin-card">
        <form @submit.prevent="updateSchool" class="school-form">
          <div class="row">
            <div class="col-md-6">
              <div class="form-group">
                <label for="city-id">Tỉnh/Thành phố <span class="required">*</span></label>
                <select 
                  id="city-id" 
                  v-model="formData.city_id" 
                  class="form-select" 
                  :class="{ 'is-invalid': errors.city_id }"
                  required
                  @change="handleCityChange"
                >
                  <option v-for="city in cities" :key="city.id" :value="city.id">
                    {{ city.name }}
                  </option>
                </select>
                <div v-if="errors.city_id" class="invalid-feedback">
                  {{ errors.city_id }}
                </div>
              </div>
            </div>
  
            <div class="col-md-6">
              <div class="form-group">
                <label for="district-id">Quận/Huyện <span class="required">*</span></label>
                <select 
                  id="district-id" 
                  v-model="formData.district_id" 
                  class="form-select" 
                  :class="{ 'is-invalid': errors.district_id }"
                  :disabled="!formData.city_id || !filteredDistricts.length"
                  required
                >
                  <option v-for="district in filteredDistricts" :key="district.id" :value="district.id">
                    {{ district.name }}
                  </option>
                </select>
                <div v-if="errors.district_id" class="invalid-feedback">
                  {{ errors.district_id }}
                </div>
              </div>
            </div>
          </div>
  
          <div class="row">
            <div class="col-md-6">
              <div class="form-group">
                <label for="school-code">Mã trường <span class="required">*</span></label>
                <input 
                  type="text" 
                  id="school-code" 
                  v-model="formData.school_code" 
                  class="form-control" 
                  :class="{ 'is-invalid': errors.school_code }"
                  placeholder="Nhập mã trường" 
                  required
                >
                <div v-if="errors.school_code" class="invalid-feedback">
                  {{ errors.school_code }}
                </div>
              </div>
            </div>
  
            <div class="col-md-6">
              <div class="form-group">
                <label for="priority-area">Khu vực ưu tiên <span class="required">*</span></label>
                <select 
                  id="priority-area" 
                  v-model="formData.priority_area" 
                  class="form-select" 
                  :class="{ 'is-invalid': errors.priority_area }"
                  required
                >
                  <option value="KV1">Khu vực 1 (KV1)</option>
                  <option value="KV2">Khu vực 2 (KV2)</option>
                  <option value="KV2NT">Khu vực 2 nông thôn (KV2NT)</option>
                  <option value="KV3">Khu vực 3 (KV3)</option>
                </select>
                <div v-if="errors.priority_area" class="invalid-feedback">
                  {{ errors.priority_area }}
                </div>
              </div>
            </div>
          </div>
  
          <div class="form-group">
            <label for="name">Tên trường <span class="required">*</span></label>
            <input 
              type="text" 
              id="name" 
              v-model="formData.name" 
              class="form-control" 
              :class="{ 'is-invalid': errors.name }" 
              placeholder="Nhập tên trường" 
              required
            >
            <div v-if="errors.name" class="invalid-feedback">
              {{ errors.name }}
            </div>
          </div>
  
          <div class="form-group">
            <label for="address">Địa chỉ <span class="required">*</span></label>
            <textarea 
              id="address" 
              v-model="formData.address" 
              class="form-control" 
              :class="{ 'is-invalid': errors.address }" 
              placeholder="Nhập địa chỉ trường" 
              rows="3"
              required
            ></textarea>
            <div v-if="errors.address" class="invalid-feedback">
              {{ errors.address }}
            </div>
          </div>
  
          <div class="meta-info">
            <div class="meta-item">
              <span class="meta-label">ID:</span>
              <span class="meta-value">#{{ school.id }}</span>
            </div>
            <div class="meta-item">
              <span class="meta-label">Ngày tạo:</span>
              <span class="meta-value">{{ formatDate(school.created_at) }}</span>
            </div>
            <div class="meta-item">
              <span class="meta-label">Cập nhật:</span>
              <span class="meta-value">{{ formatDate(school.updated_at) }}</span>
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
              Xóa trường học
            </button>
            <router-link to="/admins/school-priorities" class="btn-cancel">
              <i class="bi bi-x-circle me-2"></i>
              Hủy
            </router-link>
          </div>
        </form>
      </div>
  
      <!-- Delete School Confirmation Modal -->
      <div v-if="showDeleteModal" class="modal-overlay" @click="cancelDelete">
        <div class="modal-content" @click.stop>
          <div class="modal-header">
            <h4 class="modal-title">Xác nhận xóa trường học</h4>
            <button type="button" class="btn-close" @click="cancelDelete"></button>
          </div>
          <div class="modal-body">
            <p>Bạn có chắc chắn muốn xóa trường <strong>{{ school.name }}</strong>?</p>
            <p class="text-danger">
              <i class="bi bi-exclamation-triangle me-2"></i>
              Thao tác này không thể khôi phục lại!
            </p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn-cancel" @click="cancelDelete">Hủy</button>
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
  import { ref, reactive, computed, onMounted } from 'vue'
  import { useRouter } from 'vue-router'
  import SchoolPriorityController from '@/controllers/admins/SchoolPriorityController'
  
  export default {
    name: 'AdminSchoolDetail',
    props: {
      schoolId: {
        type: [String, Number],
        required: true
      }
    },
    setup(props) {
      const router = useRouter()
      const school = ref({})
      const formData = reactive({
        school_code: '',
        name: '',
        address: '',
        district_id: '',
        priority_area: '',
        city_id: '' // For UI selection
      })
      const cities = ref([])
      const districts = ref([])
      const loading = ref(true)
      const error = ref(null)
      const errors = reactive({
        school_code: '',
        name: '',
        address: '',
        district_id: '',
        priority_area: '',
        city_id: ''
      })
      const updateError = ref(null)
      const isUpdating = ref(false)
      const showDeleteModal = ref(false)
      const isDeleting = ref(false)
  
      // Computed for filtered districts based on selected city
      const filteredDistricts = computed(() => {
        if (!formData.city_id) return []
        return districts.value.filter(district => district.city_id === parseInt(formData.city_id))
      })
      
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
      
      // Load school data
      const loadSchoolData = async () => {
        try {
          loading.value = true
          
          // Load cities first
          const citiesData = await SchoolPriorityController.getAllCities()
          cities.value = citiesData
          
          // Load all districts
          let allDistricts = []
          for (const city of citiesData) {
            const cityDistricts = await SchoolPriorityController.getDistrictsByCity(city.id)
            allDistricts = [...allDistricts, ...cityDistricts]
          }
          districts.value = allDistricts
          
          // Then load school
          const schoolData = await SchoolPriorityController.getSchoolById(props.schoolId)
          school.value = schoolData
          
          // Find the district to get the city_id
          const district = districts.value.find(d => d.id === schoolData.district_id)
          
          // Set form data
          formData.school_code = schoolData.school_code
          formData.name = schoolData.name
          formData.address = schoolData.address
          formData.district_id = schoolData.district_id
          formData.priority_area = schoolData.priority_area
          
          if (district) {
            formData.city_id = district.city_id
          }
          
        } catch (err) {
          error.value = `Không thể tải thông tin trường học: ${err.message}`
        } finally {
          loading.value = false
        }
      }
      
      // Handle city change
      const handleCityChange = () => {
        // Reset district selection when city changes
        formData.district_id = ''
      }
      
      // Validate form
      const validateForm = () => {
        let isValid = true
        
        // Reset errors
        Object.keys(errors).forEach(key => errors[key] = '')
        updateError.value = null
  
        // Validate city_id
        if (!formData.city_id) {
          errors.city_id = 'Vui lòng chọn tỉnh/thành phố'
          isValid = false
        }
        
        // Validate district_id
        if (!formData.district_id) {
          errors.district_id = 'Vui lòng chọn quận/huyện'
          isValid = false
        }
  
        // Validate school_code
        if (!formData.school_code || formData.school_code.trim() === '') {
          errors.school_code = 'Mã trường không được để trống'
          isValid = false
        }
  
        // Validate name
        if (!formData.name || formData.name.trim() === '') {
          errors.name = 'Tên trường không được để trống'
          isValid = false
        }
        
        // Validate address
        if (!formData.address || formData.address.trim() === '') {
          errors.address = 'Địa chỉ trường không được để trống'
          isValid = false
        }
        
        // Validate priority_area
        if (!formData.priority_area) {
          errors.priority_area = 'Vui lòng chọn khu vực ưu tiên'
          isValid = false
        }
  
        return isValid
      }
      
      // Update school
      const updateSchool = async () => {
        if (!validateForm()) {
          return
        }
        
        try {
          isUpdating.value = true
          
          await SchoolPriorityController.updateSchool(props.schoolId, {
            school_code: formData.school_code.trim(),
            name: formData.name.trim(),
            address: formData.address.trim(),
            district_id: parseInt(formData.district_id),
            priority_area: formData.priority_area
          })
          
          // Update local state
          school.value = {
            ...school.value,
            school_code: formData.school_code.trim(),
            name: formData.name.trim(),
            address: formData.address.trim(),
            district_id: parseInt(formData.district_id),
            priority_area: formData.priority_area,
            updated_at: new Date().toISOString()
          }
          
          alert('Cập nhật trường học thành công!')
        } catch (err) {
          updateError.value = err.message
        } finally {
          isUpdating.value = false
        }
      }
      
      // Delete school
      const confirmDelete = () => {
        showDeleteModal.value = true
      }
      
      const cancelDelete = () => {
        showDeleteModal.value = false
      }
      
      const deleteSchool = async () => {
        try {
          isDeleting.value = true
          
          await SchoolPriorityController.deleteSchool(props.schoolId)
          
          alert('Xóa trường học thành công!')
          router.push('/admins/school-priorities')
        } catch (err) {
          alert(`Lỗi: ${err.message}`)
        } finally {
          isDeleting.value = false
          showDeleteModal.value = false
        }
      }
  
      onMounted(() => {
        loadSchoolData()
      })
  
      return {
        school,
        formData,
        cities,
        districts,
        loading,
        error,
        errors,
        updateError,
        isUpdating,
        showDeleteModal,
        isDeleting,
        filteredDistricts,
        formatDate,
        handleCityChange,
        validateForm,
        updateSchool,
        confirmDelete,
        cancelDelete,
        deleteSchool
      }
    }
  }
  </script>
  
  <style scoped>
  .admin-school-detail {
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
  
  .school-form {
    max-width: 800px;
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
  
  @media (max-width: 768px) {
    .form-actions {
      flex-direction: column;
    }
    
    .btn-save, .btn-cancel, .btn-delete {
      width: 100%;
    }
  }
  </style>
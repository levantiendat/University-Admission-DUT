<template>
    <div class="admin-district-create">
      <div class="admin-page-header">
        <div class="d-flex align-items-center">
          <router-link to="/admins/school-priorities" class="btn-back">
            <i class="bi bi-arrow-left"></i>
          </router-link>
          <div>
            <h2 class="admin-page-title">Thêm quận/huyện mới</h2>
            <p class="admin-page-description">Tạo mới quận/huyện trong hệ thống</p>
          </div>
        </div>
      </div>
  
      <div class="admin-card">
        <form @submit.prevent="createDistrict" class="district-form">
          <div class="form-group">
            <label for="city-id">Tỉnh/Thành phố <span class="required">*</span></label>
            <select 
              id="city-id" 
              v-model="formData.city_id" 
              class="form-select" 
              :class="{ 'is-invalid': errors.city_id }"
              required
            >
              <option value="" disabled>Chọn tỉnh/thành phố</option>
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
  
          <div class="alert alert-info" role="alert">
            <i class="bi bi-info-circle me-2"></i>
            <span>Mã quận/huyện nên là duy nhất trong mỗi tỉnh/thành phố.</span>
          </div>
  
          <div v-if="submitError" class="alert alert-danger">
            <i class="bi bi-exclamation-triangle-fill me-2"></i>
            {{ submitError }}
          </div>
  
          <div class="form-actions">
            <button type="submit" class="btn-save" :disabled="isSubmitting">
              <i class="bi bi-check-circle me-2"></i>
              {{ isSubmitting ? 'Đang lưu...' : 'Lưu quận/huyện' }}
            </button>
            <router-link to="/admins/school-priorities" class="btn-cancel">
              <i class="bi bi-x-circle me-2"></i>
              Hủy
            </router-link>
          </div>
        </form>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, reactive, onMounted, watch } from 'vue'
  import { useRouter, useRoute } from 'vue-router'
  import SchoolPriorityController from '@/controllers/admins/SchoolPriorityController'
  
  export default {
    name: 'AdminDistrictCreate',
    setup() {
      const router = useRouter()
      const route = useRoute()
      
      const cities = ref([])
      const formData = reactive({
        district_code: '',
        name: '',
        city_id: ''
      })
  
      const errors = reactive({
        district_code: '',
        name: '',
        city_id: ''
      })
  
      const isSubmitting = ref(false)
      const submitError = ref('')
      const loadingCities = ref(true)
  
      // Get cities
      const getCities = async () => {
        try {
          loadingCities.value = true
          const citiesData = await SchoolPriorityController.getAllCities()
          cities.value = citiesData
          
          // If cityId is in query params, set it in formData
          const cityIdParam = route.query.cityId
          if (cityIdParam) {
            formData.city_id = parseInt(cityIdParam)
          }
        } catch (error) {
          submitError.value = `Không thể tải danh sách tỉnh/thành phố: ${error.message}`
        } finally {
          loadingCities.value = false
        }
      }
  
      const validateForm = () => {
        let isValid = true
        
        // Reset errors
        errors.district_code = ''
        errors.name = ''
        errors.city_id = ''
        submitError.value = ''
  
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
  
      const createDistrict = async () => {
        if (!validateForm()) {
          return
        }
  
        try {
          isSubmitting.value = true
          
          await SchoolPriorityController.createDistrict({
            district_code: formData.district_code.trim(),
            name: formData.name.trim(),
            city_id: parseInt(formData.city_id)
          })
          
          alert('Tạo quận/huyện thành công!')
          
          // If we came from a city detail page, go back there
          if (route.query.cityId) {
            router.push(`/admins/school-priorities/cities/${route.query.cityId}`)
          } else {
            router.push('/admins/school-priorities')
          }
        } catch (error) {
          submitError.value = error.message
        } finally {
          isSubmitting.value = false
        }
      }
  
      onMounted(() => {
        getCities()
      })
  
      return {
        cities,
        formData,
        errors,
        isSubmitting,
        submitError,
        createDistrict
      }
    }
  }
  </script>
  
  <style scoped>
  .admin-district-create {
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
  
  .alert-info {
    background-color: #e1f5fe;
    color: #0c5460;
    border: 1px solid #bee5eb;
  }
  
  @media (max-width: 768px) {
    .form-actions {
      flex-direction: column;
    }
    
    .btn-save, .btn-cancel {
      width: 100%;
    }
  }
  </style>
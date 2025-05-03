<template>
    <div class="admin-school-create">
      <div class="admin-page-header">
        <div class="d-flex align-items-center">
          <router-link to="/admins/school-priorities" class="btn-back">
            <i class="bi bi-arrow-left"></i>
          </router-link>
          <div>
            <h2 class="admin-page-title">Thêm trường học mới</h2>
            <p class="admin-page-description">Tạo mới trường học trong hệ thống</p>
          </div>
        </div>
      </div>
  
      <div class="admin-card">
        <form @submit.prevent="createSchool" class="school-form">
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
                  <option value="" disabled>Chọn tỉnh/thành phố</option>
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
                  <option value="" disabled>{{ formData.city_id ? 'Chọn quận/huyện' : 'Vui lòng chọn tỉnh/thành phố trước' }}</option>
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
                  <option value="" disabled>Chọn khu vực ưu tiên</option>
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
  
          <div class="alert alert-info" role="alert">
            <i class="bi bi-info-circle me-2"></i>
            <span>Khu vực ưu tiên ảnh hưởng đến điểm ưu tiên của thí sinh khi xét tuyển.</span>
          </div>
  
          <div v-if="submitError" class="alert alert-danger">
            <i class="bi bi-exclamation-triangle-fill me-2"></i>
            {{ submitError }}
          </div>
  
          <div class="form-actions">
            <button type="submit" class="btn-save" :disabled="isSubmitting">
              <i class="bi bi-check-circle me-2"></i>
              {{ isSubmitting ? 'Đang lưu...' : 'Lưu trường học' }}
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
  import { ref, reactive, computed, onMounted, watch } from 'vue'
  import { useRouter, useRoute } from 'vue-router'
  import SchoolPriorityController from '@/controllers/admins/SchoolPriorityController'
  
  export default {
    name: 'AdminSchoolCreate',
    setup() {
      const router = useRouter()
      const route = useRoute()
      
      const cities = ref([])
      const districts = ref([])
      const formData = reactive({
        school_code: '',
        name: '',
        address: '',
        district_id: '',
        priority_area: '',
        city_id: ''  // Just for UI selection, not sent to API
      })
  
      const errors = reactive({
        school_code: '',
        name: '',
        address: '',
        district_id: '',
        priority_area: '',
        city_id: ''
      })
  
      const isSubmitting = ref(false)
      const submitError = ref('')
      const loadingCities = ref(true)
      const loadingDistricts = ref(false)
  
      // Computed for filtered districts based on selected city
      const filteredDistricts = computed(() => {
        if (!formData.city_id) return []
        return districts.value.filter(district => district.city_id === parseInt(formData.city_id))
      })
  
      // Get cities and districts
      const getCities = async () => {
        try {
          loadingCities.value = true
          const citiesData = await SchoolPriorityController.getAllCities()
          cities.value = citiesData
          
          // Load all districts for all cities
          await getDistricts()
          
          // If cityId or districtId in query params, set them in formData
          const cityIdParam = route.query.cityId
          const districtIdParam = route.query.districtId
          
          if (districtIdParam) {
            // Find the district first to get its city
            const district = districts.value.find(d => d.id === parseInt(districtIdParam))
            if (district) {
              formData.district_id = parseInt(districtIdParam)
              formData.city_id = district.city_id
            }
          } else if (cityIdParam) {
            formData.city_id = parseInt(cityIdParam)
          }
        } catch (error) {
          submitError.value = `Không thể tải danh sách tỉnh/thành phố: ${error.message}`
        } finally {
          loadingCities.value = false
        }
      }
      
      const getDistricts = async () => {
        try {
          loadingDistricts.value = true
          let allDistricts = []
          
          // For each city, fetch districts
          for (const city of cities.value) {
            const cityDistricts = await SchoolPriorityController.getDistrictsByCity(city.id)
            allDistricts = [...allDistricts, ...cityDistricts]
          }
          
          districts.value = allDistricts
        } catch (error) {
          submitError.value = `Không thể tải danh sách quận/huyện: ${error.message}`
        } finally {
          loadingDistricts.value = false
        }
      }
      
      // Handle city change
      const handleCityChange = () => {
        // Reset district selection when city changes
        formData.district_id = ''
      }
  
      const validateForm = () => {
        let isValid = true
        
        // Reset errors
        Object.keys(errors).forEach(key => errors[key] = '')
        submitError.value = ''
  
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
  
      const createSchool = async () => {
        if (!validateForm()) {
          return
        }
  
        try {
          isSubmitting.value = true
          
          await SchoolPriorityController.createSchool({
            school_code: formData.school_code.trim(),
            name: formData.name.trim(),
            address: formData.address.trim(),
            district_id: parseInt(formData.district_id),
            priority_area: formData.priority_area
          })
          
          alert('Tạo trường học thành công!')
          
          // If we came from a district detail page, go back there
          if (route.query.districtId) {
            router.push(`/admins/school-priorities/districts/${route.query.districtId}`)
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
        districts,
        formData,
        errors,
        isSubmitting,
        submitError,
        filteredDistricts,
        handleCityChange,
        createSchool
      }
    }
  }
  </script>
  
  <style scoped>
  .admin-school-create {
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
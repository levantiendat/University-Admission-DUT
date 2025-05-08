<template>
  <main class="school-priority-container">
    <div class="search-card">
      <header class="card-header">
        <h1 class="card-title">
          <i class="bi bi-search" aria-hidden="true"></i> Tra cứu khu vực ưu tiên
        </h1>
        <p class="card-subtitle">
          Công cụ tra cứu khu vực ưu tiên trường THPT
          <small class="data-update">Cập nhật: 30.04.2024</small>
        </p>
      </header>
      
      <section class="quick-search-section" aria-labelledby="quick-search-label">
        <h2 id="quick-search-label" class="search-label">
          <i class="bi bi-lightning-fill" aria-hidden="true"></i> Tìm kiếm nhanh
        </h2>
        <div class="search-input-group">
          <input 
            type="text" 
            id="globalSearch" 
            class="search-input" 
            placeholder="Nhập tên tỉnh, quận/huyện hoặc trường..." 
            v-model="globalQuery"
            autocomplete="off"
            aria-label="Tìm kiếm toàn cục"
          />
          <span class="search-icon" aria-hidden="true">
            <i class="bi bi-search"></i>
          </span>
        </div>
        
        <div class="suggestions-container" v-show="suggestions.length > 0" role="listbox">
          <div 
            v-for="item in suggestions" 
            :key="`${item.type}-${item.id}`" 
            class="suggestion-item"
            @click="goToDetail(item)"
            role="option"
          >
            <div class="suggestion-icon" aria-hidden="true">
              <i v-if="item.type === 'cities'" class="bi bi-geo-alt-fill"></i>
              <i v-else-if="item.type === 'districts'" class="bi bi-geo"></i>
              <i v-else-if="item.type === 'schools'" class="bi bi-building"></i>
            </div>
            <div class="suggestion-content">
              <div class="suggestion-name">{{ item.name }}</div>
              <div class="suggestion-type">
                {{ item.type === 'cities' ? 'Tỉnh/Thành phố' : 
                   item.type === 'districts' ? 'Quận/Huyện' : 'Trường THPT' }}
              </div>
            </div>
          </div>
        </div>
      </section>
      
      <div class="divider">
        <span>hoặc</span>
      </div>
      
      <section aria-labelledby="form-search-label">
        <h2 id="form-search-label" class="visually-hidden">Tìm kiếm theo bộ lọc</h2>
        <form @submit.prevent="searchSchool" class="dropdown-search-form">
          <div class="form-section">
            <label for="city" class="form-label">
              <i class="bi bi-building-fill" aria-hidden="true"></i> Tỉnh/Thành phố
            </label>
            <select 
              id="city" 
              class="form-select" 
              v-model="selectedCity" 
              @change="handleCityChange">
              <option value="">-- Chọn Tỉnh/Thành phố --</option>
              <option v-for="city in cities" :key="city.id" :value="city.id">{{ city.name }}</option>
            </select>
          </div>
          
          <div class="form-section">
            <label for="district" class="form-label">
              <i class="bi bi-geo-alt" aria-hidden="true"></i> Quận/Huyện
            </label>
            <select 
              id="district" 
              class="form-select" 
              v-model="selectedDistrict" 
              @change="handleDistrictChange"
              :disabled="!districts.length">
              <option value="">-- Chọn Quận/Huyện --</option>
              <option v-for="district in districts" :key="district.id" :value="district.id">{{ district.name }}</option>
            </select>
          </div>
          
          <div class="form-section">
            <label for="school" class="form-label">
              <i class="bi bi-book" aria-hidden="true"></i> Trường THPT
            </label>
            <select 
              id="school" 
              class="form-select" 
              v-model="selectedSchool"
              :disabled="!schools.length">
              <option value="">-- Chọn Trường THPT --</option>
              <option v-for="school in schools" :key="school.id" :value="school.id">{{ school.name }}</option>
            </select>
          </div>
          
          <div class="form-actions">
            <button 
              type="submit" 
              class="search-button"
              :disabled="!selectedSchool">
              <i class="bi bi-search" aria-hidden="true"></i> Tra cứu
            </button>
          </div>
        </form>
      </section>
    </div>
  </main>
</template>

<script>
import { ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import debounce from 'lodash/debounce'
import SchoolPriorityController from '@/controllers/schoolpriorityController'

export default {
  name: 'SchoolPriority',
  setup() {
    const router = useRouter()
    
    const cities = ref([])
    const districts = ref([])
    const schools = ref([])
    const selectedCity = ref('')
    const selectedDistrict = ref('')
    const selectedSchool = ref('')
    const globalQuery = ref('')
    const suggestions = ref([])
    
    // Create debounced search function
    const debouncedSearch = debounce(async (query) => {
      if (query.length >= 2) {
        try {
          const results = await SchoolPriorityController.performGlobalSearch(query)
          suggestions.value = results
        } catch (error) {
          console.error('Error in global search:', error)
          suggestions.value = []
        }
      } else {
        suggestions.value = []
      }
    }, 300)
    
    // Watch for changes to search query
    watch(globalQuery, (newQuery) => {
      debouncedSearch(newQuery)
    })
    
    // Initial data loading
    onMounted(async () => {
      try {
        cities.value = await SchoolPriorityController.loadCities()
      } catch (error) {
        console.error('Failed to load cities:', error)
      }
    })
    
    // Handle city selection change
    const handleCityChange = async () => {
      selectedDistrict.value = ''
      selectedSchool.value = ''
      schools.value = []
      
      if (selectedCity.value) {
        try {
          districts.value = await SchoolPriorityController.loadDistricts(selectedCity.value)
        } catch (error) {
          console.error('Error loading districts:', error)
          districts.value = []
        }
      } else {
        districts.value = []
      }
    }
    
    // Handle district selection change
    const handleDistrictChange = async () => {
      selectedSchool.value = ''
      
      if (selectedDistrict.value) {
        try {
          schools.value = await SchoolPriorityController.loadSchools(selectedDistrict.value)
        } catch (error) {
          console.error('Error loading schools:', error)
          schools.value = []
        }
      } else {
        schools.value = []
      }
    }
    
    // Handle form submission
    const searchSchool = () => {
      if (selectedSchool.value) {
        router.push(`/school/${selectedSchool.value}`)
      }
    }
    
    // Handle selection from suggestions
    const goToDetail = (item) => {
      if (item.type === 'cities') {
        router.push(`/city/${item.id}`)
      } else if (item.type === 'districts') {
        router.push(`/district/${item.id}`)
      } else if (item.type === 'schools') {
        router.push(`/school/${item.id}`)
      }
    }
    
    return {
      cities,
      districts,
      schools,
      selectedCity,
      selectedDistrict,
      selectedSchool,
      globalQuery,
      suggestions,
      handleCityChange,
      handleDistrictChange,
      searchSchool,
      goToDetail
    }
  }
}
</script>

<style scoped>
.school-priority-container {
  background-color: #f5f9ff;
  min-height: 70vh;
  padding: 1.5rem 1rem;
  display: flex;
  justify-content: center;
  align-items: flex-start;
}

.search-card {
  background-color: #ffffff;
  border-radius: 0.75rem;
  box-shadow: 0 0.25rem 1rem rgba(0, 41, 103, 0.1);
  width: 100%;
  max-width: 600px;
  overflow: hidden;
  margin: 0 auto;
  padding: 0;
  position: relative;
}

.card-header {
  background-color: #0B2942;
  color: white;
  padding: 1.25rem;
  text-align: center;
  position: relative;
}

.card-header::after {
  content: '';
  position: absolute;
  bottom: -8px;
  left: 50%;
  transform: translateX(-50%);
  width: 40px;
  height: 3px;
  background-color: #4da0ff;
  border-radius: 3px;
}

.card-title {
  font-weight: 700;
  font-size: 1.3rem;
  margin-bottom: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.card-subtitle {
  font-size: 0.85rem;
  opacity: 0.9;
  margin-bottom: 0;
}

.data-update {
  display: block;
  font-size: 0.75rem;
  opacity: 0.7;
  margin-top: 0.25rem;
}

.quick-search-section {
  padding: 1.25rem 1.25rem 0.75rem;
  position: relative;
}

.search-label {
  display: block;
  color: #0B2942;
  font-weight: 600;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
}

.search-input-group {
  position: relative;
}

.search-input {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 1px solid #e0e6f0;
  border-radius: 0.5rem;
  font-size: 0.9rem;
  transition: all 0.3s;
}

.search-input:focus {
  outline: none;
  border-color: #4da0ff;
  box-shadow: 0 0 0 2px rgba(77, 160, 255, 0.15);
}

.search-icon {
  position: absolute;
  right: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  color: #0B2942;
  font-size: 0.9rem;
}

.suggestions-container {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  max-height: 250px;
  overflow-y: auto;
  background-color: white;
  border-radius: 0.5rem;
  box-shadow: 0 0.25rem 1rem rgba(0, 41, 103, 0.1);
  z-index: 1000;
  margin: 0.25rem 1.25rem;
  border: 1px solid #e0e6f0;
}

.suggestion-item {
  padding: 0.75rem;
  display: flex;
  align-items: center;
  cursor: pointer;
  border-bottom: 1px solid #f0f0f0;
  transition: background-color 0.2s;
}

.suggestion-item:last-child {
  border-bottom: none;
}

.suggestion-item:hover {
  background-color: #f5f9ff;
}

.suggestion-icon {
  width: 2rem;
  height: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #ebf5ff;
  color: #0B2942;
  border-radius: 0.5rem;
  margin-right: 0.75rem;
  font-size: 0.9rem;
}

.suggestion-content {
  flex: 1;
}

.suggestion-name {
  font-weight: 600;
  color: #0B2942;
  font-size: 0.85rem;
}

.suggestion-type {
  font-size: 0.75rem;
  color: #6c757d;
  margin-top: 0.125rem;
}

.divider {
  display: flex;
  align-items: center;
  text-align: center;
  color: #6c757d;
  padding: 0 1.25rem;
  margin: 0.5rem 0;
}

.divider::before,
.divider::after {
  content: '';
  flex: 1;
  border-bottom: 1px solid #e0e6f0;
}

.divider span {
  padding: 0 0.5rem;
  font-size: 0.8rem;
}

.dropdown-search-form {
  padding: 0.75rem 1.25rem 1.25rem;
}

.form-section {
  margin-bottom: 0.75rem;
}

.form-label {
  display: block;
  color: #0B2942;
  font-weight: 600;
  margin-bottom: 0.375rem;
  font-size: 0.85rem;
}

.form-select {
  width: 100%;
  padding: 0.5rem 0.75rem;
  border: 1px solid #e0e6f0;
  border-radius: 0.5rem;
  appearance: none;
  background: white url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' fill='%230B2942' viewBox='0 0 16 16'%3E%3Cpath d='M7.247 11.14L2.451 5.658C1.885 5.013 2.345 4 3.204 4h9.592a1 1 0 0 1 .753 1.659l-4.796 5.48a1 1 0 0 1-1.506 0z'/%3E%3C/svg%3E") no-repeat;
  background-position: right 0.75rem center;
  background-size: 0.75rem;
  font-size: 0.85rem;
  transition: all 0.2s;
}

.form-select:focus {
  outline: none;
  border-color: #4da0ff;
  box-shadow: 0 0 0 2px rgba(77, 160, 255, 0.15);
}

.form-select:disabled {
  background-color: #f5f9ff;
  cursor: not-allowed;
  opacity: 0.7;
}

.form-actions {
  text-align: center;
  margin-top: 1rem;
}

.search-button {
  background-color: #0B2942;
  color: white;
  border: none;
  border-radius: 1rem;
  padding: 0.5rem 1.25rem;
  font-weight: 600;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.3s;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.search-button:hover {
  background-color: #164675;
  transform: translateY(-2px);
  box-shadow: 0 3px 8px rgba(11, 41, 66, 0.2);
}

.search-button:disabled {
  background-color: #a0b1c5;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.visually-hidden {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

/* Responsive adjustments */
@media (max-width: 480px) {
  .school-priority-container {
    padding: 0.75rem 0.5rem;
  }
  
  .card-header {
    padding: 1rem;
  }
  
  .card-title {
    font-size: 1.1rem;
  }
  
  .quick-search-section,
  .dropdown-search-form {
    padding-left: 1rem;
    padding-right: 1rem;
  }
  
  .suggestions-container {
    margin: 0.25rem 1rem;
  }
}
</style>
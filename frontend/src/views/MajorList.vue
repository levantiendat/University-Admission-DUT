<template>
  <div class="major-list-container">
    <div class="container-fluid py-2 py-md-3">
      <article class="card main-card shadow-sm">
        <!-- Header Section with improved accessibility -->
        <header class="card-header bg-primary text-white" aria-labelledby="major-list-title">
          <div class="d-flex justify-content-center align-items-center">
            <div class="header-icon me-2" aria-hidden="true">
              <i class="bi bi-book-fill"></i>
            </div>
            <h1 id="major-list-title" class="mb-0 fs-5">DANH SÁCH NGÀNH TUYỂN SINH NĂM 2025</h1>
          </div>
        </header>
        
        <!-- Description Section -->
        <div class="description-section bg-light p-2 border-bottom">
          <div class="container">
            <p class="description-text mb-0">
              <i class="bi bi-info-circle me-2" aria-hidden="true"></i>
              Danh sách các ngành đào tạo và chỉ tiêu tuyển sinh của Trường Đại học Bách khoa - Đại học Đà Nẵng năm 2025.
            </p>
          </div>
        </div>
        
        <!-- Main Content with improved loading states -->
        <div class="card-body">
          <!-- Loading State -->
          <div v-if="loading" class="text-center py-3" role="status" aria-live="polite">
            <div class="spinner-border text-primary" aria-hidden="true"></div>
            <p class="mt-2 fs-6">Đang tải dữ liệu ngành tuyển sinh...</p>
          </div>
          
          <!-- Error State -->
          <div v-else-if="error" class="alert alert-danger" role="alert">
            <i class="bi bi-exclamation-triangle-fill me-2" aria-hidden="true"></i>
            {{ error }}
          </div>
          
          <!-- Content when data is loaded -->
          <div v-else>
            <!-- Search and Filter Section - improved for mobile -->
            <section class="filter-section mb-3" aria-labelledby="filter-heading">
              <h2 id="filter-heading" class="visually-hidden">Tìm kiếm và lọc ngành học</h2>
              <div class="row g-2">
                <div class="col-12 col-md-6">
                  <div class="input-group search-box">
                    <span class="input-group-text bg-primary text-white" aria-hidden="true">
                      <i class="bi bi-search"></i>
                    </span>
                    <label for="search-input" class="visually-hidden">Tìm kiếm ngành học</label>
                    <input 
                      id="search-input"
                      type="text" 
                      class="form-control" 
                      placeholder="Tìm kiếm ngành học..." 
                      v-model="searchQuery"
                    >
                  </div>
                </div>
                
                <div class="col-12 col-md-6">
                  <div class="input-group">
                    <span class="input-group-text bg-primary text-white" aria-hidden="true">
                      <i class="bi bi-filter"></i>
                    </span>
                    <label for="faculty-filter" class="visually-hidden">Lọc theo khoa</label>
                    <select id="faculty-filter" class="form-select" v-model="selectedFaculty">
                      <option value="all">Tất cả các khoa</option>
                      <option v-for="faculty in faculties" :key="faculty.id" :value="faculty.id">
                        {{ faculty.faculty_code }} - {{ faculty.name }}
                      </option>
                    </select>
                  </div>
                </div>
              </div>
            </section>
            
            <!-- Major List Table - improved for mobile -->
            <section class="table-container mb-3" aria-labelledby="major-table-heading">
              <h2 id="major-table-heading" class="visually-hidden">Danh sách ngành học</h2>
              
              <!-- Mobile card view (shows on small screens) -->
              <div class="d-md-none">
                <div v-for="(major, index) in filteredMajors" :key="major.id" class="major-card mb-2">
                  <div class="card">
                    <div class="card-header bg-primary text-white d-flex justify-content-between align-items-center py-1">
                      <span class="badge bg-light text-dark">{{ index + 1 }}</span>
                      <h3 class="h6 mb-0 text-truncate small">{{ major.name }}</h3>
                    </div>
                    <div class="card-body p-2">
                      <div class="mb-1 small">
                        <span class="fw-bold">Mã ngành:</span> {{ major.major_code }}
                      </div>
                      <div class="mb-1 small">
                        <span class="fw-bold">Khoa:</span> {{ major.faculty_name }}
                      </div>
                      <div class="d-flex justify-content-between align-items-center mb-1 small">
                        <span class="fw-bold">Chỉ tiêu:</span>
                        <span class="badge bg-success">{{ major.seats }}</span>
                      </div>
                      <div class="d-flex justify-content-between align-items-center mb-2 small">
                        <span class="fw-bold">Phương thức:</span>
                        <span class="badge bg-info">{{ major.method_count }}</span>
                      </div>
                      <div class="d-grid gap-1">
                        <div class="btn-group btn-group-sm">
                          <button class="btn btn-outline-primary btn-sm py-0" @click="showMajorInfo(major.id)">
                            <i class="bi bi-eye" aria-hidden="true"></i> Xem
                          </button>
                          <router-link :to="{ name: 'MajorDetail', params: { id: major.id }}" class="btn btn-primary btn-sm py-0">
                            <i class="bi bi-info-circle" aria-hidden="true"></i> Chi tiết
                          </router-link>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              
              <!-- Desktop table view (shows on medium screens and up) -->
              <div class="table-responsive d-none d-md-block">
                <table class="table table-hover border table-sm">
                  <caption class="visually-hidden">Danh sách ngành học tại Trường ĐH Bách Khoa</caption>
                  <thead>
                    <tr class="bg-primary text-white">
                      <th scope="col" class="text-center" style="width: 5%">STT</th>
                      <th scope="col" style="width: 12%">Mã ngành</th>
                      <th scope="col" style="width: 25%">Tên ngành</th>
                      <th scope="col" style="width: 25%">Khoa</th>
                      <th scope="col" class="text-center" style="width: 8%">Chỉ tiêu</th>
                      <th scope="col" class="text-center" style="width: 15%">PT xét tuyển</th>
                      <th scope="col" class="text-center" style="width: 10%">Thao tác</th>
                    </tr>
                  </thead>
                  <tbody>
                    <template v-for="(major, index) in filteredMajors" :key="major.id">
                      <tr>
                        <td class="text-center">{{ index + 1 }}</td>
                        <td>{{ major.major_code }}</td>
                        <td class="fw-medium">{{ major.name }}</td>
                        <td>{{ major.faculty_name }}</td>
                        <td class="text-center fw-bold">{{ major.seats }}</td>
                        <td class="text-center">
                          <div class="method-count">
                            <span class="badge bg-info">
                              {{ major.method_count }}
                            </span>
                          </div>
                        </td>
                        <td class="text-center">
                          <div class="d-flex justify-content-center flex-wrap gap-1">
                            <button class="btn btn-sm btn-outline-primary py-0" @click="showMajorInfo(major.id)">
                              <i class="bi bi-eye" aria-hidden="true"></i> Xem
                            </button>
                            <router-link :to="{ name: 'MajorDetail', params: { id: major.id }}" class="btn btn-sm btn-primary py-0">
                              <i class="bi bi-info-circle" aria-hidden="true"></i> Chi tiết
                            </router-link>
                          </div>
                        </td>
                      </tr>
                    </template>
                  </tbody>
                </table>
              </div>
              
              <!-- No results message -->
              <div v-if="filteredMajors.length === 0" class="text-center py-3 my-2 bg-light rounded">
                <div class="no-results">
                  <i class="bi bi-search fs-4 text-muted" aria-hidden="true"></i>
                  <p class="mt-2 fs-6">Không tìm thấy ngành phù hợp với tiêu chí tìm kiếm.</p>
                  <button class="btn btn-outline-primary btn-sm mt-1" @click="resetFilters">
                    <i class="bi bi-arrow-counterclockwise me-2" aria-hidden="true"></i>
                    Đặt lại bộ lọc
                  </button>
                </div>
              </div>
            </section>
            
            <!-- Statistics Section - improved grid for mobile -->
            <section class="stats-section mt-3" aria-labelledby="stats-heading">
              <h2 id="stats-heading" class="visually-hidden">Thống kê ngành đào tạo</h2>
              <div class="row g-2">
                <div class="col-4">
                  <div class="card stat-card bg-primary text-white h-100">
                    <div class="card-body py-2 px-3">
                      <div class="d-flex align-items-center">
                        <div class="stat-icon me-2" aria-hidden="true">
                          <i class="bi bi-building"></i>
                        </div>
                        <div>
                          <small class="mb-0 fs-7">Tổng số khoa</small>
                          <p class="mb-0 fs-5 fw-bold">{{ faculties.length }}</p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                
                <div class="col-4">
                  <div class="card stat-card bg-success text-white h-100">
                    <div class="card-body py-2 px-3">
                      <div class="d-flex align-items-center">
                        <div class="stat-icon me-2" aria-hidden="true">
                          <i class="bi bi-book"></i>
                        </div>
                        <div>
                          <small class="mb-0 fs-7">Tổng số ngành</small>
                          <p class="mb-0 fs-5 fw-bold">{{ majors.length }}</p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                
                <div class="col-4">
                  <div class="card stat-card bg-info text-white h-100">
                    <div class="card-body py-2 px-3">
                      <div class="d-flex align-items-center">
                        <div class="stat-icon me-2" aria-hidden="true">
                          <i class="bi bi-people"></i>
                        </div>
                        <div>
                          <small class="mb-0 fs-7">Tổng chỉ tiêu</small>
                          <p class="mb-0 fs-5 fw-bold">{{ totalSeats }}</p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </section>
          </div>
        </div>
      </article>
    </div>
    
    <!-- Information Widget (Replaces the Modal) -->
    <MajorInfoWidget 
      :majorId="selectedMajorId" 
      :visible="showInfoWidget"
      @close="hideInfoWidget"
    />
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import DetailMajorController from '@/controllers/DetailMajorController'
import MajorInfoWidget from '@/components/MajorQuickView.vue'

export default {
  name: 'MajorList',
  components: {
    MajorInfoWidget
  },
  setup() {
    // States
    const majors = ref([])
    const faculties = ref([])
    const searchQuery = ref('')
    const selectedFaculty = ref('all')
    const loading = ref(true)
    const error = ref(null)
    
    // Info widget state (replaces modal state)
    const selectedMajorId = ref(null)
    const showInfoWidget = ref(false)
    
    // Computed properties
    const filteredMajors = computed(() => {
      let result = majors.value

      // Lọc theo khoa nếu đã chọn khoa
      if (selectedFaculty.value !== 'all') {
        result = result.filter(major => major.faculty_id === selectedFaculty.value)
      }

      // Lọc theo từ khóa tìm kiếm
      if (searchQuery.value) {
        const query = searchQuery.value.toLowerCase()
        result = result.filter(major => 
          major.major_code.toLowerCase().includes(query) ||
          major.name.toLowerCase().includes(query) ||
          major.faculty_name?.toLowerCase().includes(query)
        )
      }

      return result
    })
    
    const totalSeats = computed(() => {
      return majors.value.reduce((sum, major) => sum + major.seats, 0)
    })
    
    // Methods
    const loadData = async () => {
      try {
        loading.value = true
        
        // Lấy danh sách ngành và số phương thức xét tuyển cho mỗi ngành
        const majorsData = await DetailMajorController.getMajors()
        const methodsPromises = majorsData.map(major => 
          DetailMajorController.getMajorAdmissionMethods(major.id)
            .then(methods => ({
              majorId: major.id,
              methodCount: methods.length
            }))
            .catch(() => ({ majorId: major.id, methodCount: 0 }))
        )
        
        const methodsCounts = await Promise.all(methodsPromises)
        
        // Thêm số lượng phương thức xét tuyển vào mỗi ngành
        majorsData.forEach(major => {
          const methodData = methodsCounts.find(m => m.majorId === major.id)
          major.method_count = methodData ? methodData.methodCount : 0
        })
        
        majors.value = majorsData
        faculties.value = await DetailMajorController.getFaculties()
        
      } catch (err) {
        console.error('Lỗi khi tải dữ liệu:', err)
        error.value = 'Đã xảy ra lỗi khi tải dữ liệu. Vui lòng thử lại sau.'
      } finally {
        loading.value = false
      }
    }
    
    // Show info widget (replaces showMajorQuickView)
    const showMajorInfo = (majorId) => {
      selectedMajorId.value = majorId
      showInfoWidget.value = true
    }
    
    // Hide info widget
    const hideInfoWidget = () => {
      showInfoWidget.value = false
      selectedMajorId.value = null
    }
    
    const resetFilters = () => {
      searchQuery.value = ''
      selectedFaculty.value = 'all'
    }
    
    // Mounted hook
    onMounted(() => {
      loadData()
    })
    
    return {
      majors,
      faculties,
      loading,
      error,
      searchQuery,
      selectedFaculty,
      filteredMajors,
      totalSeats,
      resetFilters,
      selectedMajorId,
      showInfoWidget,
      showMajorInfo,
      hideInfoWidget
    }
  }
}
</script>

<style scoped>
/* Base Container */
.major-list-container {
  min-height: 100vh;
  background-color: #f5f5f5;
  margin: 0;
  padding: 0 5px;
}

@media (min-width: 768px) {
  .major-list-container {
    margin: 0 2vw;
    padding: 0;
  }
}

/* Main Card */
.main-card {
  border: none;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.1) !important;
}

/* Header */
.card-header {
  background-color: #0d47a1 !important;
  padding: 0.6rem;
}

.header-icon {
  font-size: 1.3rem;
}

/* Description Section */
.description-section {
  background-color: #e8f1ff !important;
  border-bottom: 1px solid #dee2e6;
}

.description-text {
  font-size: 0.8rem;
  line-height: 1.3;
  color: #495057;
}

/* Filter Section */
.filter-section {
  background-color: #f8f9fa;
  padding: 0.75rem;
  border-radius: 6px;
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.05);
}

/* Table and Form Controls */
.form-control, .form-select {
  font-size: 0.875rem;
  padding: 0.25rem 0.5rem;
}

.input-group-text {
  padding: 0.25rem 0.5rem;
  font-size: 0.875rem;
}

.table {
  font-size: 0.8rem;
  margin-bottom: 0.5rem;
}

.table th,
.table td {
  padding: 0.4rem 0.5rem;
  vertical-align: middle;
}

/* Buttons */
.btn-sm {
  padding: 0.15rem 0.4rem;
  font-size: 0.75rem;
}

/* Mobile Card View */
.major-card .card {
  border: none;
  border-radius: 6px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.major-card .badge {
  font-size: 0.7rem;
  padding: 0.2rem 0.4rem;
}

/* Stats Section */
.stats-section .card {
  border: none;
  border-radius: 6px;
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.05);
}

.stat-icon {
  font-size: 1.2rem;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 6px;
}

/* Font size utility not in Bootstrap */
.fs-7 {
  font-size: 0.75rem !important;
}

/* Modal Quick View */
.modal-content {
  border: none;
  border-radius: 8px;
  overflow: hidden;
}

.major-name {
  color: #0d47a1;
  font-weight: 700;
}

/* Detail Cards */
.detail-card {
  background-color: #f8f9fa;
  border-radius: 6px;
  padding: 0.75rem;
  text-align: center;
  box-shadow: 0 1px 5px rgba(0, 0, 0, 0.05);
}

.detail-card-title {
  color: #495057;
  font-size: 0.75rem;
  margin-bottom: 0.2rem;
}

.detail-card-value {
  font-size: 1.25rem;
  font-weight: 700;
  color: #0d47a1;
}

.detail-card.quota .detail-card-value {
  color: #28a745;
}

/* Section Styling */
.quick-view-section {
  margin-top: 1rem;
  padding-top: 0.8rem;
  border-top: 1px solid #e9ecef;
}

.section-heading {
  color: #0d47a1;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

/* Method Cards */
.method-cards {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.5rem;
  margin-top: 0.5rem;
}

@media (min-width: 768px) {
  .method-cards {
    grid-template-columns: repeat(3, 1fr);
  }
}

.method-card {
  background-color: #e8f1ff;
  border-left: 3px solid #0d47a1;
  padding: 0.5rem;
  border-radius: 6px;
}

.method-name {
  font-weight: 500;
  color: #0d47a1;
}

/* Subject Groups */
.subject-group-section:not(:first-child) {
  margin-top: 0.8rem;
}

.group-cards {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
  margin-top: 0.4rem;
}

.group-card {
  background-color: rgba(13, 71, 161, 0.1);
  color: #0d47a1;
  border: 1px solid rgba(13, 71, 161, 0.2);
  padding: 0.25rem 0.5rem;
  border-radius: 20px;
  font-size: 0.7rem;
}

/* Previous Scores */
.score-year-section:not(:first-child) {
  margin-top: 0.8rem;
}

.year-title {
  font-weight: 600;
  color: #495057;
  margin-bottom: 0.4rem;
}

.score-cards {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.5rem;
}

@media (min-width: 576px) {
  .score-cards {
    grid-template-columns: repeat(4, 1fr);
  }
}

.score-card {
  background-color: #f8f9fa;
  border-radius: 6px;
  padding: 0.5rem;
  border-left: 3px solid #28a745;
}

.score-value {
  font-size: 1.1rem;
  font-weight: 700;
  color: #28a745;
  margin-top: 0.2rem;
}

/* Loading Animation */
.spinner-border {
  width: 1.5rem;
  height: 1.5rem;
}

.spinner-border-sm {
  width: 1rem;
  height: 1rem;
}

/* No Results */
.no-results {
  padding: 1rem;
}

/* Accessibility Helpers */
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
</style>
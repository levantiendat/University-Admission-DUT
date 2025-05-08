<template>
  <main class="admission-container bg-light">
    <div class="container-fluid py-3">
      <article class="card main-card shadow-sm">
        <header class="card-header bg-primary text-white">
          <div class="d-flex justify-content-center align-items-center">
            <div class="header-icon me-2" aria-hidden="true">
              <i class="bi bi-mortarboard-fill"></i>
            </div>
            <h1 class="mb-0 fs-5">THÔNG TIN TUYỂN SINH NĂM 2025</h1>
          </div>
        </header>
        
        <div class="description-section bg-light p-2 border-bottom">
          <div class="container">
            <p class="description-text small mb-0">
              <i class="bi bi-info-circle me-2" aria-hidden="true"></i>
              Thông tin về các phương thức xét tuyển của trường Đại học Bách khoa - Đại học Đà Nẵng năm 2025. 
              Thí sinh có thể tìm hiểu chi tiết về từng phương thức xét tuyển và các ngành đào tạo.
            </p>
          </div>
        </div>
        
        <div class="card-body p-2 p-md-3">
          <div v-if="loading" class="text-center py-3">
            <div class="spinner-border spinner-border-sm text-primary" role="status">
              <span class="visually-hidden">Đang tải...</span>
            </div>
            <p class="mt-2 small">Đang tải dữ liệu tuyển sinh...</p>
          </div>
          
          <div v-else-if="error" class="alert alert-danger py-2" role="alert">
            <i class="bi bi-exclamation-triangle-fill me-2" aria-hidden="true"></i>
            {{ error }}
          </div>
          
          <div v-else>
            <!-- Bộ lọc và tìm kiếm -->
            <section class="filter-section mb-3" aria-labelledby="filter-heading">
              <h2 id="filter-heading" class="visually-hidden">Bộ lọc tìm kiếm</h2>
              <div class="row g-2">
                <div class="col-12 col-md-6">
                  <div class="input-group search-box">
                    <span class="input-group-text bg-primary text-white py-1">
                      <i class="bi bi-search" aria-hidden="true"></i>
                    </span>
                    <input 
                      type="text" 
                      class="form-control" 
                      placeholder="Tìm kiếm ngành học..." 
                      v-model="searchQuery"
                      aria-label="Tìm kiếm ngành học"
                    >
                  </div>
                </div>
                
                <div class="col-12 col-md-6">
                  <div class="input-group">
                    <span class="input-group-text bg-primary text-white py-1">
                      <i class="bi bi-filter" aria-hidden="true"></i>
                    </span>
                    <select class="form-select" v-model="selectedFaculty" aria-label="Chọn khoa">
                      <option value="all">Tất cả các khoa</option>
                      <option v-for="faculty in faculties" :key="faculty.id" :value="faculty.id">
                        {{ faculty.faculty_code }} - {{ faculty.name }}
                      </option>
                    </select>
                  </div>
                </div>
              </div>
            </section>
            
            <!-- Bảng thông tin tuyển sinh -->
            <section class="table-responsive admission-table" aria-labelledby="admission-table-heading">
              <h2 id="admission-table-heading" class="visually-hidden">Danh sách ngành tuyển sinh</h2>
              <table class="table table-hover table-sm border">
                <caption class="visually-hidden">Danh sách ngành đào tạo và phương thức xét tuyển</caption>
                <thead>
                  <tr class="bg-primary text-white">
                    <th scope="col" class="text-center" style="width: 5%">STT</th>
                    <th scope="col" style="width: 10%">Mã ngành</th>
                    <th scope="col" style="width: 25%">Tên ngành</th>
                    <th scope="col" class="text-center" style="width: 10%">Chỉ tiêu</th>
                    <template v-for="method in admissionMethods" :key="method.id">
                      <th scope="col" class="text-center" style="width: auto">
                        <span class="method-title" :title="method.description">
                          {{ getShortMethodName(method.name) }}
                          <i class="bi bi-info-circle-fill ms-1" aria-hidden="true"></i>
                        </span>
                      </th>
                    </template>
                  </tr>
                </thead>
                <tbody>
                  <template v-for="(major, index) in filteredMajors" :key="major.major_code">
                    <tr>
                      <td class="text-center">{{ index + 1 }}</td>
                      <td>{{ major.major_code }}</td>
                      <td class="fw-medium">{{ major.name }}</td>
                      <td class="text-center fw-bold">
                        {{ major.seats }}
                      </td>
                      <template v-for="method in admissionMethods" :key="method.id">
                        <td class="text-center">
                          <span 
                            class="status-indicator"
                            :class="major['method_' + method.id] ? 'available' : 'not-available'"
                            data-bs-toggle="tooltip" 
                            :title="method.description"
                            aria-label="Ngành này {{ major['method_' + method.id] ? 'áp dụng' : 'không áp dụng' }} phương thức xét tuyển {{ method.name }}"
                          >
                            <i 
                              :class="`bi ${major['method_' + method.id] ? 'bi-check-circle-fill' : 'bi-x-circle-fill'}`"
                              aria-hidden="true"
                            ></i>
                          </span>
                        </td>
                      </template>
                    </tr>
                  </template>
                  
                  <tr v-if="filteredMajors.length === 0">
                    <td colspan="100%" class="text-center py-3">
                      <div class="no-results">
                        <i class="bi bi-search fs-5 text-muted" aria-hidden="true"></i>
                        <p class="mt-2 small">Không tìm thấy ngành phù hợp với tiêu chí tìm kiếm.</p>
                        <button class="btn btn-outline-primary btn-sm mt-2" @click="resetFilters">
                          <i class="bi bi-arrow-counterclockwise me-1" aria-hidden="true"></i>
                          Đặt lại bộ lọc
                        </button>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </section>
            
            <!-- Thống kê -->
            <section class="stats-section mt-3" aria-labelledby="stats-section-heading">
              <h2 id="stats-section-heading" class="visually-hidden">Thống kê tuyển sinh</h2>
              <div class="row g-2">
                <div class="col-4">
                  <div class="card stat-card bg-primary text-white h-100">
                    <div class="card-body py-2">
                      <div class="d-flex align-items-center">
                        <div class="stat-icon me-2" aria-hidden="true">
                          <i class="bi bi-building"></i>
                        </div>
                        <div>
                          <small class="mb-0 d-block">Tổng số khoa</small>
                          <span class="fw-bold fs-5">{{ faculties.length }}</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                
                <div class="col-4">
                  <div class="card stat-card bg-success text-white h-100">
                    <div class="card-body py-2">
                      <div class="d-flex align-items-center">
                        <div class="stat-icon me-2" aria-hidden="true">
                          <i class="bi bi-book"></i>
                        </div>
                        <div>
                          <small class="mb-0 d-block">Tổng số ngành</small>
                          <span class="fw-bold fs-5">{{ majors.length }}</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                
                <div class="col-4">
                  <div class="card stat-card bg-info text-white h-100">
                    <div class="card-body py-2">
                      <div class="d-flex align-items-center">
                        <div class="stat-icon me-2" aria-hidden="true">
                          <i class="bi bi-people"></i>
                        </div>
                        <div>
                          <small class="mb-0 d-block">Tổng chỉ tiêu</small>
                          <span class="fw-bold fs-5">{{ totalSeats }}</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </section>
            
            <!-- Chú thích -->
            <section class="legend-section mt-3" aria-labelledby="legend-heading">
              <div class="card bg-light">
                <div class="card-body p-2">
                  <h2 id="legend-heading" class="card-title h6">
                    <i class="bi bi-info-circle me-1" aria-hidden="true"></i>
                    Chú thích phương thức tuyển sinh:
                  </h2>
                  <div class="row g-2">
                    <div class="col-md-6">
                      <ul class="legend-list mb-2">
                        <li v-for="(method, index) in admissionMethods.slice(0, Math.ceil(admissionMethods.length/2))" :key="method.id" class="small">
                          <strong>{{ getShortMethodName(method.name) }}:</strong> {{ method.name }}
                        </li>
                      </ul>
                    </div>
                    <div class="col-md-6">
                      <ul class="legend-list mb-2">
                        <li v-for="method in admissionMethods.slice(Math.ceil(admissionMethods.length/2))" :key="method.id" class="small">
                          <strong>{{ getShortMethodName(method.name) }}:</strong> {{ method.name }}
                        </li>
                      </ul>
                    </div>
                  </div>
                  
                  <div class="mt-2">
                    <h3 class="h6">Trạng thái phương thức:</h3>
                    <div class="d-flex flex-wrap small">
                      <div class="me-3 mb-2">
                        <span class="status-indicator available me-1" aria-hidden="true">
                          <i class="bi bi-check-circle-fill"></i>
                        </span>
                        Ngành áp dụng phương thức
                      </div>
                      <div>
                        <span class="status-indicator not-available me-1" aria-hidden="true">
                          <i class="bi bi-x-circle-fill"></i>
                        </span>
                        Ngành không áp dụng phương thức
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
  </main>
</template>

<script>
import AdmissionController from '@/controllers/admissionController'

export default {
  name: 'AdmissionView',
  data() {
    return {
      majors: [],
      admissionMethods: [],
      faculties: [],
      loading: true,
      error: null,
      searchQuery: '',
      selectedFaculty: 'all',
    }
  },
  computed: {
    filteredMajors() {
      let result = this.majors

      // Lọc theo khoa nếu đã chọn khoa
      if (this.selectedFaculty !== 'all') {
        result = result.filter(major => major.faculty_id === this.selectedFaculty)
      }

      // Lọc theo từ khóa tìm kiếm
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase()
        result = result.filter(major => 
          major.major_code.toLowerCase().includes(query) ||
          major.name.toLowerCase().includes(query) ||
          major.faculty_name.toLowerCase().includes(query)
        )
      }

      return result
    },

    totalSeats() {
      return this.majors.reduce((sum, major) => sum + major.seats, 0)
    }
  },
  async mounted() {
    try {
      const data = await AdmissionController.getAdmissionData()
      this.majors = data.majors
      this.admissionMethods = data.admissionMethods
      this.faculties = data.faculties
      this.initializeTooltips()
    } catch (error) {
      this.error = 'Đã xảy ra lỗi khi tải dữ liệu tuyển sinh. Vui lòng thử lại sau.'
      console.error(error)
    } finally {
      this.loading = false
    }
  },
  methods: {
    initializeTooltips() {
      // Khởi tạo tooltips của Bootstrap
      this.$nextTick(() => {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
        if (window.bootstrap && window.bootstrap.Tooltip) {
          tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl, {
              html: true
            })
          })
        }
      })
    },

    getShortMethodName(fullName) {
      // Tạo tên viết tắt cho phương thức tuyển sinh
      if (fullName.includes('Xét tuyển thẳng')) return 'Xét tuyển thẳng'
      if (fullName.includes('Xét kết quả học tập cấp THPT (học bạ)')) return 'Xét học bạ'
      if (fullName.includes('Xét kết quả thi tốt nghiệp Trung Học Phổ Thông')) return 'Xét điểm thi THPT'
      if (fullName.includes('Xét kết quả thi đánh giá năng lực do ĐHQG TP.HCM tổ chức')) return 'Xét điểm thi ĐGNL'
      if (fullName.includes('Xét tuyển theo phương thức xét tuyển riêng')) return 'Tuyển sinh riêng'
      if (fullName.includes('Xét kết quả thi đánh giá tư duy do Đại Học Bách Khoa Hà Nội tổ chức')) return 'Xét điểm thi ĐGTD'

      // Nếu không khớp với các mẫu trên, lấy các chữ cái đầu tiên
      const words = fullName.split(' ')
      if (words.length <= 2) return fullName

      return words
        .filter(word => word.length > 1)
        .map(word => word.charAt(0))
        .join('')
    },

    resetFilters() {
      this.searchQuery = ''
      this.selectedFaculty = 'all'
    }
  }
}
</script>

<style scoped>
.admission-container {
  min-height: 100vh;
  background-color: #f5f5f5;
  margin: 0;
  padding: 0 5px;
}

@media (min-width: 768px) {
  .admission-container {
    margin: 0 2vw;
  }
}

.main-card {
  border: none;
  border-radius: 0.5rem;
  overflow: hidden;
  box-shadow: 0 0.25rem 0.5rem rgba(0, 0, 0, 0.1) !important;
}

.card-header {
  background-color: #0d47a1 !important;
  padding: 0.75rem;
}

.header-icon {
  font-size: 1.25rem;
}

.description-section {
  background-color: #e8f1ff !important;
  border-bottom: 1px solid #dee2e6;
}

.description-text {
  line-height: 1.4;
  color: #495057;
}

.filter-section {
  background-color: #f8f9fa;
  padding: 0.75rem;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.search-box .form-control:focus {
  border-color: #0d47a1;
  box-shadow: 0 0 0 0.15rem rgba(13, 71, 161, 0.25);
}

.admission-table {
  border-radius: 0.5rem;
  overflow: hidden;
}

/* Thiết lập cho các ô trong header: tự động xuống dòng và giảm kích thước chữ */
.table th {
  vertical-align: middle;
  white-space: normal; /* Cho phép xuống dòng */
  font-size: 0.8rem;
  padding: 0.4rem;
}

/* Giảm kích thước chữ cho dữ liệu bảng */
.table td {
  font-size: 0.8rem;
  vertical-align: middle;
  padding: 0.4rem;
}

/* Cho tiêu đề của phương thức tuyển sinh xuống dòng khi cần */
.method-title {
  cursor: help;
  white-space: normal;
  line-height: 1.2;
  font-size: 0.75rem;
}

/* Hiệu ứng hover cho các dòng */
.table tbody tr:hover {
  background-color: rgba(13, 71, 161, 0.05);
}

.status-indicator {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 1.5rem;
  height: 1.5rem;
  border-radius: 50%;
  font-size: 0.9rem;
}

.status-indicator.available {
  background-color: rgba(40, 167, 69, 0.1);
  color: #28a745;
}

.status-indicator.not-available {
  background-color: rgba(220, 53, 69, 0.1);
  color: #dc3545;
}

.stats-section .card {
  border: none;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  transition: transform 0.2s;
}

.stats-section .card:hover {
  transform: translateY(-2px);
}

.stat-icon {
  font-size: 1.25rem;
  width: 2rem;
  height: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 0.5rem;
}

.legend-section .card {
  border: none;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.legend-list {
  list-style-type: none;
  padding-left: 0;
  margin-bottom: 0;
}

.legend-list li {
  margin-bottom: 0.25rem;
}

.no-results {
  padding: 1rem 0;
}

/* Accessibility - hidden visually but available for screen readers */
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
  .table th, .table td {
    font-size: 0.7rem;
    padding: 0.3rem;
  }

  .status-indicator {
    width: 1.25rem;
    height: 1.25rem;
    font-size: 0.8rem;
  }
  
  .stat-icon {
    font-size: 1rem;
    width: 1.75rem;
    height: 1.75rem;
  }
}
</style>
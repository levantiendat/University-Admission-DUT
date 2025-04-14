<template>
    <div class="admission-container bg-light">
      <div class="container-fluid py-5">
        <div class="card main-card shadow">
          <div class="card-header bg-primary text-white">
            <div class="d-flex justify-content-center align-items-center">
              <div class="header-icon me-3">
                <i class="bi bi-mortarboard-fill"></i>
              </div>
              <h2 class="mb-0">THÔNG TIN TUYỂN SINH NĂM 2025</h2>
            </div>
          </div>
          
          <div class="card-body">
            <div v-if="loading" class="text-center py-5">
              <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Đang tải...</span>
              </div>
              <p class="mt-3">Đang tải dữ liệu tuyển sinh...</p>
            </div>
            
            <div v-else-if="error" class="alert alert-danger" role="alert">
              <i class="bi bi-exclamation-triangle-fill me-2"></i>
              {{ error }}
            </div>
            
            <div v-else>
              <!-- Bộ lọc và tìm kiếm -->
              <div class="filter-section mb-4">
                <div class="row g-3">
                  <div class="col-md-6">
                    <div class="input-group search-box">
                      <span class="input-group-text bg-primary text-white">
                        <i class="bi bi-search"></i>
                      </span>
                      <input 
                        type="text" 
                        class="form-control" 
                        placeholder="Tìm kiếm ngành học..." 
                        v-model="searchQuery"
                      >
                    </div>
                  </div>
                  
                  <div class="col-md-6">
                    <div class="input-group">
                      <span class="input-group-text bg-primary text-white">
                        <i class="bi bi-filter"></i>
                      </span>
                      <select class="form-select" v-model="selectedFaculty">
                        <option value="all">Tất cả các khoa</option>
                        <option v-for="faculty in faculties" :key="faculty.id" :value="faculty.id">
                          {{ faculty.faculty_code }} - {{ faculty.name }}
                        </option>
                      </select>
                    </div>
                  </div>
                </div>
              </div>
              
              <!-- Bảng thông tin tuyển sinh -->
              <div class="table-responsive admission-table">
                <table class="table table-hover border">
                  <thead>
                    <tr class="bg-primary text-white">
                      <th scope="col" class="text-center">STT</th>
                      <th scope="col">Mã ngành</th>
                      <th scope="col">Tên ngành</th>
                      <th scope="col" class="text-center">Chỉ tiêu</th>
                      <template v-for="method in admissionMethods" :key="method.id">
                        <th scope="col" class="text-center">
                          <span class="method-title" :title="method.description">
                            {{ getShortMethodName(method.name) }}
                            <i class="bi bi-info-circle-fill ms-1"></i>
                          </span>
                        </th>
                      </template>
                      <th scope="col" class="text-center">Chi tiết</th>
                    </tr>
                  </thead>
                  <tbody>
                    <template v-for="(major, index) in filteredMajors" :key="major.major_code">
                      <tr :class="{'table-active': expandedMajor === major.major_code}">
                        <td class="text-center">{{ index + 1 }}</td>
                        <td>{{ major.major_code }}</td>
                        <td>{{ major.name }}</td>
                        <td class="text-center">
                          <span class="badge bg-info text-dark">{{ major.seats }}</span>
                        </td>
                        <template v-for="method in admissionMethods" :key="method.id">
                          <td class="text-center">
                            <span 
                              class="status-indicator"
                              :class="major['method_' + method.id] ? 'available' : 'not-available'"
                              data-bs-toggle="tooltip" 
                              :title="method.description"
                            >
                              <i 
                                :class="`bi ${major['method_' + method.id] ? 'bi-check-circle-fill' : 'bi-x-circle-fill'}`"
                              ></i>
                            </span>
                          </td>
                        </template>
                        <td class="text-center">
                          <button 
                            class="btn btn-sm" 
                            :class="expandedMajor === major.major_code ? 'btn-danger' : 'btn-outline-primary'" 
                            @click="toggleMajorDetails(major.major_code)"
                          >
                            <i class="bi" :class="expandedMajor === major.major_code ? 'bi-dash-lg' : 'bi-plus-lg'"></i>
                            {{ expandedMajor === major.major_code ? 'Đóng' : 'Xem' }}
                          </button>
                        </td>
                      </tr>
                      <tr v-if="expandedMajor === major.major_code">
                        <td colspan="100%" class="p-0">
                          <div class="major-details">
                            <div class="card border-0">
                              <div class="card-body">
                                <h5 class="card-title">
                                  <i class="bi bi-mortarboard me-2"></i>
                                  Thông tin chi tiết về ngành {{ major.name }}
                                </h5>
                                <div class="row">
                                  <div class="col-md-6">
                                    <p><strong>Mã ngành:</strong> {{ major.major_code }}</p>
                                    <p><strong>Thuộc khoa:</strong> {{ major.faculty_name }} ({{ major.faculty_code }})</p>
                                    <p><strong>Chỉ tiêu:</strong> {{ major.seats }} sinh viên</p>
                                  </div>
                                  <div class="col-md-6">
                                    <p><strong>Phương thức tuyển sinh áp dụng:</strong></p>
                                    <ul>
                                      <li v-for="method in admissionMethods" :key="method.id" v-if="major['method_' + method.id]">
                                        {{ method.name }}
                                      </li>
                                    </ul>
                                  </div>
                                </div>
                                <div class="mt-3">
                                  <p><strong>Mô tả ngành:</strong></p>
                                  <p>{{ major.description }}</p>
                                </div>
                              </div>
                            </div>
                          </div>
                        </td>
                      </tr>
                    </template>
                    
                    <tr v-if="filteredMajors.length === 0">
                      <td colspan="100%" class="text-center py-5">
                        <div class="no-results">
                          <i class="bi bi-search fs-1 text-muted"></i>
                          <p class="mt-3">Không tìm thấy ngành phù hợp với tiêu chí tìm kiếm.</p>
                          <button class="btn btn-outline-primary mt-2" @click="resetFilters">
                            <i class="bi bi-arrow-counterclockwise me-2"></i>
                            Đặt lại bộ lọc
                          </button>
                        </div>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
              
              <!-- Thống kê -->
              <div class="stats-section mt-4">
                <div class="row g-3">
                  <div class="col-md-4">
                    <div class="card stat-card bg-primary text-white">
                      <div class="card-body">
                        <div class="d-flex align-items-center">
                          <div class="stat-icon me-3">
                            <i class="bi bi-building"></i>
                          </div>
                          <div>
                            <h6 class="mb-0">Tổng số khoa</h6>
                            <h3 class="mb-0">{{ faculties.length }}</h3>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  <div class="col-md-4">
                    <div class="card stat-card bg-success text-white">
                      <div class="card-body">
                        <div class="d-flex align-items-center">
                          <div class="stat-icon me-3">
                            <i class="bi bi-book"></i>
                          </div>
                          <div>
                            <h6 class="mb-0">Tổng số ngành</h6>
                            <h3 class="mb-0">{{ majors.length }}</h3>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  <div class="col-md-4">
                    <div class="card stat-card bg-info text-white">
                      <div class="card-body">
                        <div class="d-flex align-items-center">
                          <div class="stat-icon me-3">
                            <i class="bi bi-people"></i>
                          </div>
                          <div>
                            <h6 class="mb-0">Tổng chỉ tiêu</h6>
                            <h3 class="mb-0">{{ totalSeats }}</h3>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              
              <!-- Chú thích -->
              <div class="legend-section mt-4">
                <div class="card bg-light">
                  <div class="card-body">
                    <h5 class="card-title">
                      <i class="bi bi-info-circle me-2"></i>
                      Chú thích phương thức tuyển sinh:
                    </h5>
                    <div class="row">
                      <div class="col-md-6">
                        <ul class="legend-list">
                          <li v-for="(method, index) in admissionMethods.slice(0, Math.ceil(admissionMethods.length/2))" :key="method.id">
                            <strong>{{ getShortMethodName(method.name) }}:</strong> {{ method.name }}
                          </li>
                        </ul>
                      </div>
                      <div class="col-md-6">
                        <ul class="legend-list">
                          <li v-for="method in admissionMethods.slice(Math.ceil(admissionMethods.length/2))" :key="method.id">
                            <strong>{{ getShortMethodName(method.name) }}:</strong> {{ method.name }}
                          </li>
                        </ul>
                      </div>
                    </div>
                    
                    <div class="mt-3">
                      <h6>Trạng thái phương thức:</h6>
                      <div class="d-flex flex-wrap">
                        <div class="me-4 mb-2">
                          <span class="status-indicator available me-2">
                            <i class="bi bi-check-circle-fill"></i>
                          </span>
                          Ngành áp dụng phương thức
                        </div>
                        <div>
                          <span class="status-indicator not-available me-2">
                            <i class="bi bi-x-circle-fill"></i>
                          </span>
                          Ngành không áp dụng phương thức
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
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
        expandedMajor: null
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
          tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl, {
              html: true
            })
          })
        })
      },
      
      toggleMajorDetails(majorCode) {
        if (this.expandedMajor === majorCode) {
          this.expandedMajor = null
        } else {
          this.expandedMajor = majorCode
        }
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
        this.expandedMajor = null
      }
    }
  }
  </script>
  
  <style scoped>
  .admission-container {
    min-height: 100vh;
    background-color: #f5f5f5;
    margin-left: 5vw;
    margin-right: 5vw;
  }
  
  .main-card {
    border: none;
    border-radius: 15px;
    overflow: hidden;
    box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15) !important;
  }
  
  .card-header {
    background-color: #0d47a1 !important;
    padding: 1.5rem;
  }
  
  .header-icon {
    font-size: 2rem;
  }
  
  .filter-section {
    background-color: #f8f9fa;
    padding: 1.25rem;
    border-radius: 10px;
    box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
  }
  
  .search-box .form-control:focus {
    border-color: #0d47a1;
    box-shadow: 0 0 0 0.25rem rgba(13, 71, 161, 0.25);
  }
  
  .admission-table {
    box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
    border-radius: 10px;
    overflow: hidden;
  }
  
  .table th {
    vertical-align: middle;
    white-space: nowrap;
  }
  
  .table tbody tr:hover {
    background-color: rgba(13, 71, 161, 0.05);
  }
  
  .method-title {
    cursor: help;
    white-space: nowrap;
  }
  
  .status-indicator {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 30px;
    height: 30px;
    border-radius: 50%;
    font-size: 1rem;
  }
  
  .status-indicator.available {
    background-color: rgba(40, 167, 69, 0.15);
    color: #28a745;
  }
  
  .status-indicator.not-available {
    background-color: rgba(220, 53, 69, 0.15);
    color: #dc3545;
  }
  
  .major-details {
    background-color: #f8f9fa;
    padding: 1rem;
    border-top: 1px dashed #dee2e6;
    border-bottom: 1px dashed #dee2e6;
  }
  
  .stats-section .card {
    border: none;
    border-radius: 10px;
    box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
    transition: transform 0.3s;
  }
  
  .stats-section .card:hover {
    transform: translateY(-5px);
  }
  
  .stat-icon {
    font-size: 2rem;
    width: 50px;
    height: 50px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(255, 255, 255, 0.2);
    border-radius: 10px;
  }
  
  .legend-section .card {
    border: none;
    border-radius: 10px;
    box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
  }
  
  .legend-list {
    list-style-type: none;
    padding-left: 0;
  }
  
  .legend-list li {
    margin-bottom: 0.5rem;
  }
  
  .no-results {
    padding: 2rem 0;
  }
  
  /* Responsive adjustments */
  @media (max-width: 768px) {
    .card-header h2 {
      font-size: 1.5rem;
    }
    
    .header-icon {
      font-size: 1.5rem;
    }
    
    .stats-section .card {
      margin-bottom: 1rem;
    }
  }
  </style>
<template>
    <div class="admission-container bg-light">
      <div class="container py-5">
        <div class="card shadow-sm">
          <div class="card-header bg-primary text-white">
            <h2 class="text-center mb-0">THÔNG TIN TUYỂN SINH NĂM 2025</h2>
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
              <div class="mb-4">
                <div class="input-group">
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
              
              <!-- Bảng thông tin tuyển sinh -->
              <div class="table-responsive">
                <table class="table table-striped table-hover border">
                  <thead class="table-primary">
                    <tr>
                      <th scope="col" class="text-center">STT</th>
                      <th scope="col">Mã ngành</th>
                      <th scope="col">Tên ngành</th>
                      <th scope="col" class="text-center">Chỉ tiêu</th>
                      <template v-for="method in admissionMethods" :key="method.id">
                        <th scope="col" class="text-center">{{ method.name }}</th>
                      </template>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="(major, index) in filteredMajors" :key="major.major_code">
                      <td class="text-center">{{ index + 1 }}</td>
                      <td>{{ major.major_code }}</td>
                      <td>{{ major.name }}</td>
                      <td class="text-center">{{ major.seats }}</td>
                      <template v-for="method in admissionMethods" :key="method.id">
                        <td class="text-center">
                          <i 
                            :class="`bi ${major['method_' + method.id] ? 'bi-check-circle-fill text-success' : 'bi-x-circle-fill text-danger'}`"
                            data-bs-toggle="tooltip"
                            :title="method.description"
                          ></i>
                        </td>
                      </template>
                    </tr>
                    
                    <tr v-if="filteredMajors.length === 0">
                      <td colspan="100%" class="text-center py-4">
                        <i class="bi bi-info-circle me-2"></i>
                        Không tìm thấy ngành phù hợp với từ khóa tìm kiếm.
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
              
              <!-- Thông tin bổ sung -->
              <div class="mt-4">
                <div class="card bg-primary text-white">
                  <div class="card-body">
                    <h5 class="card-title"><i class="bi bi-info-circle me-2"></i>Chú thích:</h5>
                    <div class="row">
                      <div class="col-md-6">
                        <p><i class="bi bi-check-circle-fill text-success me-2"></i> Ngành áp dụng phương thức tuyển sinh</p>
                      </div>
                      <div class="col-md-6">
                        <p><i class="bi bi-x-circle-fill text-danger me-2"></i> Ngành không áp dụng phương thức tuyển sinh</p>
                      </div>
                    </div>
                    <p class="mb-0"><i class="bi bi-lightbulb me-2"></i> Di chuột qua biểu tượng để xem chi tiết phương thức tuyển sinh.</p>
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
        loading: true,
        error: null,
        searchQuery: ''
      }
    },
    computed: {
      filteredMajors() {
        if (!this.searchQuery) return this.majors
        
        const query = this.searchQuery.toLowerCase()
        return this.majors.filter(major => 
          major.major_code.toLowerCase().includes(query) ||
          major.name.toLowerCase().includes(query)
        )
      }
    },
    async mounted() {
      try {
        const data = await AdmissionController.getAdmissionData()
        this.majors = data.majors
        this.admissionMethods = data.admissionMethods
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
            return new bootstrap.Tooltip(tooltipTriggerEl)
          })
        })
      }
    }
  }
  </script>
  
  <style scoped>
  .admission-container {
    min-height: 100vh;
    background-color: #f5f5f5;
  }
  
  .card {
    border: none;
    border-radius: 10px;
  }
  
  .card-header {
    background-color: #0d47a1 !important;
    border-radius: 10px 10px 0 0 !important;
    padding: 1.5rem;
  }
  
  .table-primary {
    background-color: #bbdefb;
  }
  
  th {
    vertical-align: middle;
  }
  
  .bi-check-circle-fill {
    font-size: 1.2rem;
  }
  
  .bi-x-circle-fill {
    font-size: 1.2rem;
  }
  
  .card-title {
    font-weight: 600;
  }
  
  /* Responsive adjustments */
  @media (max-width: 768px) {
    .card-header h2 {
      font-size: 1.5rem;
    }
  }
  </style>
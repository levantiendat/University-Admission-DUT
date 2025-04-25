<template>
  <div class="hocba-container bg-light">
    <div class="container-fluid py-5">
      <div class="card main-card shadow no-copy">
        <div class="card-header bg-primary text-white">
          <div class="d-flex justify-content-center align-items-center">
            <div class="header-icon me-3">
              <i class="bi bi-journal-check"></i>
            </div>
            <h2 class="mb-0">XÉT TUYỂN RIÊNG THEO ĐỀ ÁN TUYỂN SINH</h2>
          </div>
        </div>
        
        <div class="description-section bg-light p-3 border-bottom">
          <div class="container">
            <p class="description-text mb-0">
              <i class="bi bi-info-circle me-2"></i>
              <strong>Phương thức xét tuyển:</strong> Xét tuyển riêng theo đề án tuyển sinh
              | <strong>Mã phương thức:</strong> 500
              | <strong>Điều kiện:</strong> Thí sinh đạt giải các cấp trong các cuộc thi học sinh giỏi, khoa học kỹ thuật. Lĩnh vực / Môn học đạt giải phải phù hợp với ngành đăng kí xét tuyển.
            </p>
          </div>
        </div>
        
        <div class="card-body">
          <div v-if="loading" class="text-center py-5">
            <div class="spinner-border text-primary" role="status">
              <span class="visually-hidden">Đang tải...</span>
            </div>
            <p class="mt-3 fs-5">Đang tải dữ liệu xét tuyển RIÊNG...</p>
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
                      class="form-control form-control-lg" 
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
                    <select class="form-select form-select-lg" v-model="selectedFaculty">
                      <option value="all">Tất cả các khoa</option>
                      <option v-for="faculty in faculties" :key="faculty.id" :value="faculty.falculty_id">
                        {{ faculty.faculty_code }} - {{ faculty.faculty_name }}
                      </option>
                    </select>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- Bảng thông tin tuyển sinh -->
            <div class="table-responsive hocba-table custom-scroll">
              <table class="table table-hover border">
                <thead>
                  <tr class="bg-primary text-white">
                    <th scope="col" class="text-center" style="width: 5%">STT</th>
                    <th scope="col" style="width: 10%">Mã ngành</th>
                    <th scope="col" style="width: 25%">Tên ngành</th>
                    <th scope="col" class="text-center" style="width: 10%">Chỉ tiêu</th>
                    <th scope="col" class="text-center" style="width: 50%">Môn học hoặc Lĩnh vực Khoa học kỹ thuật đạt giải</th>
                  </tr>
                </thead>
                <tbody>
                  <template v-for="(major, index) in filteredMajors" :key="major.id">
                    <tr>
                      <td class="text-center">{{ index + 1 }}</td>
                      <td>{{ major.major_code }}</td>
                      <td class="fw-medium">{{ major.major_name }}</td>
                      <td class="text-center fw-bold fs-5">
                        {{ major.seats }}
                      </td>
                      <td>
                        <div class="d-flex flex-wrap gap-2">
                          <span 
                            v-for="(subject, sIndex) in major.admission_fields" 
                            :key="sIndex"
                            class="badge subject-combo"
                            :class="getSubjectBadgeClass(sIndex)"
                            v-show="sIndex < 20"
                            data-bs-toggle="tooltip"
                            :title="getSubjectDescription(subject)"
                          >
                            {{ subject.field_or_subject_name }}
                          </span>
                        </div>
                      </td>
                    </tr>
                  </template>
                  
                  <tr v-if="filteredMajors.length === 0">
                    <td colspan="5" class="text-center py-5">
                      <div class="no-results">
                        <i class="bi bi-search fs-1 text-muted"></i>
                        <p class="mt-3 fs-5">Không tìm thấy ngành phù hợp với tiêu chí tìm kiếm.</p>
                        <button class="btn btn-outline-primary mt-2 btn-lg" @click="resetFilters">
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
            
            <!-- Chi tiết điều kiện -->
            <div class="info-section mt-4">
              <div class="card bg-light">
                <div class="card-body">
                  <h5 class="card-title fs-4">
                    <i class="bi bi-info-circle me-2"></i>
                    Chi tiết điều kiện xét tuyển riêng
                  </h5>
                  <div class="mt-3 fs-5">
                    <ul>
                      <li class="mb-2"> Thí sinh đạt giải Khuyến khích cuộc thi học sinh giỏi cấp quốc gia các môn Toán, Vật lý, Hóa học, Sinh học, Tin học; giải Khuyến khích cuộc thi khoa học kỹ thuật cấp quốc gia.</li>
                      <li class="mb-2"> Thí sinh đạt giải Nhất, Nhì, Ba, Khuyến khích (Giải Tư) tại cuộc thi học sinh giỏi các môn Toán, Vật lý, Hoá học, Sinh học, Tin học cấp tỉnh, thành phố trực thuộc trung ương.</li>
                      <li class="mb-2"> Thí sinh đạt giải Nhất, Nhì, Ba, Khuyến khích (Giải Tư) tại cuộc thi khoa học, kỹ thuật cấp tỉnh, thành phố trực thuộc trung ương.</li>
                      <li class="mb-2"> Lĩnh vực / Môn học đạt giải phù hợp với ngành đăng kí xét tuyển.</li>
                    </ul>
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
import xtrController from '@/controllers/xtRiengController'

export default {
  name: 'XTRView',
  data() {
    return {
      majors: [],
      faculties: [],
      loading: true,
      error: null,
      searchQuery: '',
      selectedFaculty: 'all',
      subjectBadgeClasses: [
        'badge-blue',
        'badge-green',
        'badge-red',
        'badge-yellow',
        'badge-teal',
        'badge-purple'
      ]
    }
  },
  computed: {
    filteredMajors() {
      let result = this.majors

      // Lọc theo khoa nếu đã chọn khoa
      if (this.selectedFaculty !== 'all') {
        result = result.filter(major => major.falculty_id == this.selectedFaculty)
      }

      // Lọc theo từ khóa tìm kiếm
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase()
        result = result.filter(major => 
          major.major_code.toLowerCase().includes(query) ||
          major.major_name.toLowerCase().includes(query) ||
          major.faculty_name?.toLowerCase().includes(query)
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
      const data = await xtrController.getXTRData()
      this.majors = data.xtr
      
      // Tạo danh sách các khoa duy nhất
      const uniqueFaculties = {}
      this.majors.forEach(major => {
        if (!uniqueFaculties[major.falculty_id]) {
          uniqueFaculties[major.falculty_id] = {
            falculty_id: major.falculty_id,
            faculty_code: major.faculty_code,
            faculty_name: major.faculty_name
          }
        }
      })
      this.faculties = Object.values(uniqueFaculties)
      
      this.initializeTooltips()
    } catch (error) {
      this.error = 'Đã xảy ra lỗi khi tải dữ liệu xét tuyển riêng. Vui lòng thử lại sau.'
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

    getSubjectBadgeClass(index) {
      return this.subjectBadgeClasses[index % this.subjectBadgeClasses.length]
    },
    
    getSubjectDescription(subject) {
      // Mô tả chi tiết về các môn học trong tổ hợp
      return `Giải HSG / Lĩnh vực khoa học kỹ thuật: ${subject.field_or_subject_name}`
    },

    resetFilters() {
      this.searchQuery = ''
      this.selectedFaculty = 'all'
    }
  }
}
</script>

<style scoped>
.hocba-container {
  min-height: 100vh;
  background-color: #f5f5f5;
  margin: 0 5vw;
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

.card-header h2 {
  font-size: 1.5rem;
  margin: 0;
  color: #fff;
}

.header-icon {
  font-size: 2.5rem;
}

.description-section {
  background-color: #e8f1ff !important;
  border-bottom: 1px solid #dee2e6;
}

.description-text {
  font-size: 1.1rem;
  line-height: 1.5;
  color: #495057;
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

.hocba-table {
  border-radius: 10px;
  overflow: hidden;
}

/* Tạo hiệu ứng cuộn nếu bảng vượt quá kích thước màn hình */
.custom-scroll {
  overflow-x: auto;
  overflow-y: auto;
  max-height: 70vh;
}

/* Thiết lập cho các ô trong header: tự động xuống dòng và giảm kích thước chữ */
.table th {
  vertical-align: middle;
  white-space: normal; /* Cho phép xuống dòng */
  font-size: 1.1rem;
  padding: 0.75rem;
}

/* Tăng kích thước chữ cho dữ liệu bảng */
.table td {
  font-size: 1rem;
  vertical-align: middle;
  padding: 0.75rem;
}

/* Hiệu ứng hover cho các dòng */
.table tbody tr:hover {
  background-color: rgba(13, 71, 161, 0.05);
}

/* Thiết kế mới cho các subject combo */
.subject-combo {
  font-size: 1rem;
  padding: 0.5rem 0.65rem;
  border-radius: 6px;
  font-weight: 500;
  margin-bottom: 0.3rem;
  cursor: help;
}

.badge-blue {
  background-color: rgba(13, 110, 253, 0.15);
  color: #0d6efd;
  border: 1px solid rgba(13, 110, 253, 0.3);
}

.badge-green {
  background-color: rgba(25, 135, 84, 0.15);
  color: #198754;
  border: 1px solid rgba(25, 135, 84, 0.3);
}

.badge-red {
  background-color: rgba(220, 53, 69, 0.15);
  color: #dc3545;
  border: 1px solid rgba(220, 53, 69, 0.3);
}

.badge-yellow {
  background-color: rgba(255, 193, 7, 0.15);
  color: #664d03;
  border: 1px solid rgba(255, 193, 7, 0.3);
}

.badge-teal {
  background-color: rgba(13, 202, 240, 0.15);
  color: #0dcaf0;
  border: 1px solid rgba(13, 202, 240, 0.3);
}

.badge-purple {
  background-color: rgba(111, 66, 193, 0.15);
  color: #6f42c1;
  border: 1px solid rgba(111, 66, 193, 0.3);
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
  font-size: 2.5rem;
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 10px;
}

.info-section .card {
  border: none;
  border-radius: 10px;
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
  background-color: #f8f9fa;
}

.calculation-section .card {
  background-color: #f8f9fa;
  border-left: 4px solid #0d47a1;
}

.no-results {
  padding: 2rem 0;
}

.no-copy {
  user-select: none;
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
}

.no-copy::selection {
  background: transparent;
}

.no-copy::-moz-selection {
  background: transparent;
}

.no-copy td, .no-copy th {
  -webkit-touch-callout: none;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .card-header h2 {
    font-size: 1.0rem;
  }
  
  .header-icon {
    font-size: 1.8rem;
  }
  
  .stats-section .card {
    margin-bottom: 1rem;
  }
  
  /* Giảm kích thước chữ cho bảng trên màn hình nhỏ nhưng vẫn đảm bảo đủ lớn để đọc */
  .table th, .table td {
    font-size: 0.8rem;
    padding: 0.5rem;
  }
  
  .subject-combo {
    font-size: 0.9rem;
    padding: 0.35rem 0.5rem;
  }
}

@media (max-width: 480px) {
  .description-text {
    font-size: 0.95rem;
  }
  
  .card-header h2 {
    font-size: 0.8rem;
  }
  
  .table th, .table td {
    font-size: 0.6rem;
    padding: 0.4rem;
  }
  
  .subject-combo {
    font-size: 0.85rem;
    padding: 0.25rem 0.4rem;
  }
}
</style>
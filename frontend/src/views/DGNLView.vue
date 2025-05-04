<template>
  <div class="dgnl-container bg-light">
    <div class="container-fluid py-4">
      <div class="card main-card shadow no-copy">
        <div class="card-header bg-primary text-white">
          <div class="d-flex justify-content-center align-items-center">
            <div class="header-icon me-3">
              <i class="bi bi-journal-check"></i>
            </div>
            <h2 class="mb-0">XÉT TUYỂN THEO ĐIỂM THI ĐÁNH GIÁ NĂNG LỰC CỦA ĐẠI HỌC QUỐC GIA TPHCM</h2>
          </div>
        </div>
        
        <div class="announcement-section p-3 border-bottom">
          <div class="container">
            <h5 class="fw-bold mb-3">Trường Đại học Bách khoa, Đại học Đà Nẵng thông báo tuyển sinh đào tạo trình độ đại học chính quy vào các ngành thuộc Trường năm 2025, theo phương thức xét kết quả thi Đánh giá năng lực do Đại học Quốc gia Thành phố Hồ Chí Minh tổ chức như sau:</h5>
            
            <div class="mb-3">
              <h6 class="fw-bold">1. Ngành đào tạo, mã xét tuyển</h6>
              <p class="mb-1">Danh mục các ngành tuyển sinh đào tạo, mã xét tuyển được quy định trong Phụ lục đính kèm.</p>
            </div>
            
            <div class="mb-3">
              <h6 class="fw-bold">2. Đối tượng tuyển sinh</h6>
              <ul class="mb-2 ps-3">
                <li>Đối tượng: thí sinh đã tốt nghiệp trung học phổ thông hoặc tương đương và có kết quả kỳ thi đánh giá năng lực của Đại học Quốc gia Thành phố Hồ Chí Minh năm 2025.</li>
              </ul>
            </div>
            
            <div class="info-box">
              <p class="mb-0">
                <i class="bi bi-info-circle me-2"></i>
                <strong>Phương thức xét tuyển:</strong> Xét tuyển theo điểm thi đánh giá năng lực của Đại học Quốc Gia TPHCM
                | <strong>Mã phương thức:</strong> 402
                | <strong>Điều kiện:</strong> Thí sinh tham dự kỳ thi đánh giá năng lực của Đại Học Quốc Gia TPHCM tổ chức năm 2025 và đạt điểm sàn theo quy định.
              </p>
            </div>
          </div>
        </div>
        
        <div class="card-body">
          <div v-if="loading" class="text-center py-4">
            <div class="spinner-border text-primary" role="status">
              <span class="visually-hidden">Đang tải...</span>
            </div>
            <p class="mt-3">Đang tải dữ liệu xét tuyển...</p>
          </div>
          
          <div v-else-if="error" class="alert alert-danger" role="alert">
            <i class="bi bi-exclamation-triangle-fill me-2"></i>
            {{ error }}
          </div>
          
          <div v-else>
            <!-- Bộ lọc và tìm kiếm -->
            <div class="filter-section mb-3">
              <div class="row g-2">
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
                      <option v-for="faculty in faculties" :key="faculty.id" :value="faculty.falculty_id">
                        {{ faculty.faculty_code }} - {{ faculty.faculty_name }}
                      </option>
                    </select>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- Bảng thông tin tuyển sinh -->
            <div class="table-responsive">
              <table class="table table-hover border">
                <thead>
                  <tr class="bg-primary text-white">
                    <th scope="col" class="text-center" style="width: 5%">STT</th>
                    <th scope="col" style="width: 15%">Mã ngành</th>
                    <th scope="col" style="width: 80%">Tên ngành</th>
                  </tr>
                </thead>
                <tbody>
                  <template v-for="(major, index) in filteredMajors" :key="major.id">
                    <tr>
                      <td class="text-center">{{ index + 1 }}</td>
                      <td>{{ major.major_code }}</td>
                      <td>{{ major.major_name }}</td>
                    </tr>
                  </template>
                  
                  <tr v-if="filteredMajors.length === 0">
                    <td colspan="3" class="text-center py-4">
                      <div class="no-results">
                        <i class="bi bi-search fs-6 text-muted"></i>
                        <p class="mt-2">Không tìm thấy ngành phù hợp với tiêu chí tìm kiếm.</p>
                        <button class="btn btn-outline-primary mt-2 btn-sm" @click="resetFilters">
                          <i class="bi bi-arrow-counterclockwise me-1"></i>
                          Đặt lại bộ lọc
                        </button>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
            
            <!-- Thông tin chi tiết về phương thức -->
            <div class="info-section mt-4">
              <div class="card">
                <div class="card-body">
                  <h5 class="card-title">
                    <i class="bi bi-info-circle me-2"></i>
                    Thông tin về kỳ thi đánh giá năng lực
                  </h5>
                  <div class="mt-3">
                    <p>Kỳ thi đánh giá năng lực (ĐGNL) là kì thi do Đại học Quốc gia TPHCM tổ chức, giúp xác định trình độ hiểu biết, kỹ năng cơ bản, tư duy logic của thí sinh.</p>
                    <p class="fw-medium">Cấu trúc đề thi Đánh giá năng lực:</p>
                    <ul>
                      <li>Phần 1: Sử dụng ngôn ngữ (60 Câu hỏi)</li>
                      <li>Phần 2: Toán học (30 Câu hỏi)</li>
                      <li>Phần 3: Tư duy khoa học (30 Câu hỏi)</li>
                    </ul>
                    <p class="fw-medium">Thang điểm: từ 0 đến 1200, trong đó:</p>
                    <ul>
                      <li>Điểm trung bình: khoảng 550-650</li>
                      <li>Điểm cao: từ 800 trở lên</li>
                    </ul>
                    <p>Thí sinh cần đạt ngưỡng điểm sàn do nhà trường quy định để đủ điều kiện xét tuyển vào các ngành học.</p>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- Thông tin liên hệ -->
            <div class="contact-section mt-4">
              <div class="card bg-light">
                <div class="card-body">
                  <h6 class="card-title fw-bold">
                    <i class="bi bi-info-circle me-2"></i>
                    3. Thông tin liên hệ:
                  </h6>
                  <div class="mt-2">
                    <p>Muốn biết thêm chi tiết, thí sinh vui lòng truy cập trang tuyển sinh của Trường Đại học Bách khoa, Đại học Đà Nẵng tại địa chỉ <a href="https://tuyensinh.dut.udn.vn/" target="_blank">https://tuyensinh.dut.udn.vn/</a> hoặc trang Tuyển sinh của Đại học Đà Nẵng tại địa chỉ <a href="http://ts.udn.vn" target="_blank">http://ts.udn.vn</a></p>
                    
                    <ul class="contact-list">
                      <li>Hoặc liên hệ với bộ phận Tuyển sinh của Trường Đại học Bách khoa. Số 54 Nguyễn Lương Bằng, quận Liên Chiểu, thành phố Đà Nẵng</li>
                      <li>Số điện thoại hỗ trợ: 0888.477.377, 0888.577.277, 0888.377.177, 0236.3620.999;</li>
                      <li>Email: <a href="mailto:tuyensinhbkdn@dut.udn.vn">tuyensinhbkdn@dut.udn.vn</a>.</li>
                      <li>Fanpage: <a href="https://www.facebook.com/DUTpage" target="_blank">https://www.facebook.com/DUTpage</a>.</li>
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
import dgnlController from '@/controllers/DGNLController'

export default {
  name: 'DGNLView',
  data() {
    return {
      majors: [],
      faculties: [],
      loading: true,
      error: null,
      searchQuery: '',
      selectedFaculty: 'all'
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
    }
  },
  async mounted() {
    try {
      const data = await dgnlController.getDGNLData()
      this.majors = data.dgnl
      
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
      this.error = 'Đã xảy ra lỗi khi tải dữ liệu xét tuyển đánh giá năng lực. Vui lòng thử lại sau.'
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

    resetFilters() {
      this.searchQuery = ''
      this.selectedFaculty = 'all'
    }
  }
}
</script>

<style scoped>
.dgnl-container {
  min-height: 100vh;
  background-color: #f5f5f5;
  margin: 0 5vw;
}

.main-card {
  border: none;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 0.25rem 0.75rem rgba(0, 0, 0, 0.15);
}

.card-header {
  background-color: #0d47a1 !important;
  padding: 1rem;
}

.card-header h2 {
  font-size: 1.3rem;
  margin: 0;
  color: #fff;
}

.header-icon {
  font-size: 2rem;
}

.announcement-section {
  background-color: #e8f1ff !important;
  border-bottom: 1px solid #dee2e6;
  font-size: 0.9rem;
}

.announcement-section h5 {
  font-size: 1.1rem;
  color: #0d47a1;
}

.announcement-section h6 {
  font-size: 0.95rem;
  color: #0d47a1;
}

.announcement-section ul {
  margin-bottom: 0.5rem;
  list-style-type: disc;
}

.info-box {
  background-color: #f8f9fa;
  border-radius: 8px;
  padding: 0.8rem;
  margin-top: 1rem;
  border-left: 4px solid #0d47a1;
  font-size: 0.85rem;
}

.filter-section {
  background-color: #f8f9fa;
  padding: 0.75rem;
  border-radius: 8px;
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.05);
}

.search-box .form-control:focus {
  border-color: #0d47a1;
  box-shadow: 0 0 0 0.2rem rgba(13, 71, 161, 0.25);
}

/* Smaller font sizes for table */
.table th {
  vertical-align: middle;
  white-space: normal;
  font-size: 0.9rem;
  padding: 0.6rem;
}

.table td {
  font-size: 0.85rem;
  vertical-align: middle;
  padding: 0.6rem;
}

/* Hiệu ứng hover cho các dòng */
.table tbody tr:hover {
  background-color: rgba(13, 71, 161, 0.05);
}

.info-section .card {
  border: none;
  border-radius: 10px;
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
  background-color: #f0f7ff;
  font-size: 0.9rem;
}

.info-section .card-title {
  font-size: 1.1rem;
  color: #0d47a1;
  font-weight: 600;
}

.contact-section .card {
  border: none;
  border-radius: 8px;
  background-color: #f8f9fa;
}

.contact-list {
  padding-left: 1rem;
  margin-bottom: 0;
  font-size: 0.85rem;
}

.contact-list li {
  margin-bottom: 0.5rem;
}

.contact-list a {
  color: #0d47a1;
  text-decoration: none;
}

.contact-list a:hover {
  text-decoration: underline;
}

.no-results {
  padding: 1rem 0;
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
    font-size: 1.5rem;
  }
  
  .announcement-section {
    font-size: 0.8rem;
  }
  
  .announcement-section h5 {
    font-size: 1rem;
  }
  
  .announcement-section h6 {
    font-size: 0.85rem;
  }
  
  .table th, .table td {
    font-size: 0.75rem;
    padding: 0.5rem;
  }
  
  .info-section .card {
    font-size: 0.8rem;
  }
}

@media (max-width: 480px) {
  .card-header h2 {
    font-size: 0.85rem;
  }
  
  .announcement-section {
    font-size: 0.75rem;
  }
  
  .table th, .table td {
    font-size: 0.7rem;
    padding: 0.4rem;
  }
}
</style>
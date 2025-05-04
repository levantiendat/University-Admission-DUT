<template>
  <div class="tnthpt-container bg-light">
    <div class="container-fluid py-4">
      <div class="card main-card shadow no-copy">
        <div class="card-header bg-primary text-white">
          <div class="d-flex justify-content-center align-items-center">
            <div class="header-icon me-3">
              <i class="bi bi-file-earmark-text"></i>
            </div>
            <h2 class="mb-0">PHƯƠNG THỨC XÉT ĐIỂM THI TỐT NGHIỆP THPT</h2>
          </div>
        </div>
        
        <div class="announcement-section p-3 border-bottom">
          <div class="container">
            <h5 class="fw-bold mb-3">1. Ngành đào tạo, chỉ tiêu và tiêu chí xét tuyển</h5>
            <p class="mb-3">Danh mục các ngành tuyển sinh đào tạo, tổ hợp, mã tổ hợp và tiêu chí xét tuyển được quy định trong Phụ lục đính kèm.</p>
            
            <h5 class="fw-bold mb-2">2. Đối tượng xét tuyển</h5>
            <p class="mb-3">Thí sinh tốt nghiệp THPT năm 2025, đạt ngưỡng chất lượng đầu vào do Trường quy định (sẽ thông báo sau).</p>
            
            <h5 class="fw-bold mb-2">3. Nguyên tắc đăng ký và xét tuyển</h5>
            <ul class="mb-3 ps-3">
              <li>Ngưỡng ĐBCL đầu vào được công bố sau khi có kết quả thi THPT.</li>
              <li>Điểm xét tuyển = Tổng điểm 3 môn thuộc tổ hợp xét tuyển với hệ số tương ứng mỗi môn, quy về thang điểm 30 + Điểm cộng (nếu có) + Điểm ưu tiên khu vực, đối tượng theo quy định (nếu có).</li>
            </ul>
            
            <div class="info-box">
              <p class="mb-0">
                <i class="bi bi-info-circle me-2"></i>
                <strong>Phương thức xét tuyển:</strong> Xét kết quả thi tốt nghiệp Trung Học Phổ Thông
                | <strong>Mã phương thức:</strong> 100
                | <strong>Điều kiện:</strong> Thí sinh có kết quả thi tốt nghiệp THPT năm 2025 và đạt ngưỡng đảm bảo chất lượng đầu vào.
              </p>
            </div>
          </div>
        </div>
        
        <div class="card-body">
          <div v-if="loading" class="text-center py-4">
            <div class="spinner-border text-primary" role="status">
              <span class="visually-hidden">Đang tải...</span>
            </div>
            <p class="mt-3">Đang tải dữ liệu phương thức xét tuyển...</p>
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
                    <th scope="col" style="width: 12%">Mã ngành</th>
                    <th scope="col" style="width: 30%">Tên ngành</th>
                    <th scope="col" style="width: 53%">Tổ hợp môn xét tuyển</th>
                  </tr>
                </thead>
                <tbody>
                  <template v-for="(major, index) in filteredMajors" :key="major.id">
                    <tr>
                      <td class="text-center">{{ index + 1 }}</td>
                      <td>{{ major.major_code }}</td>
                      <td>{{ major.major_name }}</td>
                      <td>
                        <div class="d-flex flex-wrap gap-1">
                          <span 
                            v-for="(subject, sIndex) in major.subject_score_method_majors" 
                            :key="sIndex"
                            class="badge subject-combo"
                            :class="getSubjectBadgeClass(sIndex)"
                          >
                            {{ subject.name }}
                          </span>
                        </div>
                      </td>
                    </tr>
                  </template>
                  
                  <tr v-if="filteredMajors.length === 0">
                    <td colspan="4" class="text-center py-4">
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
            
            <!-- Thông tin liên hệ -->
            <div class="contact-section mt-4">
              <div class="card bg-light">
                <div class="card-body">
                  <h6 class="card-title fw-bold">
                    <i class="bi bi-info-circle me-2"></i>
                    5. Thông tin liên hệ:
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
import TNTHPTController from '@/controllers/tnTHPTController'

export default {
  name: 'TNTHPTView',
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
    }
  },
  async mounted() {
    try {
      const data = await TNTHPTController.getTNTHPTData()
      this.majors = data.testTHPT
      
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
      this.error = 'Đã xảy ra lỗi khi tải dữ liệu phương thức xét tuyển. Vui lòng thử lại sau.'
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

    resetFilters() {
      this.searchQuery = ''
      this.selectedFaculty = 'all'
    }
  }
}
</script>

<style scoped>
.tnthpt-container {
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

/* Thiết kế nhỏ gọn hơn cho các subject combo */
.subject-combo {
  font-size: 0.8rem;
  padding: 0.3rem 0.5rem;
  border-radius: 4px;
  font-weight: 500;
  margin-bottom: 0.2rem;
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
  
  .table th, .table td {
    font-size: 0.75rem;
    padding: 0.5rem;
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
  
  .subject-combo {
    font-size: 0.65rem;
    padding: 0.2rem 0.3rem;
  }
}
</style>
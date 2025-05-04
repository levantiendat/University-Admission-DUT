<template>
  <div class="xtr-container bg-light">
    <div class="container-fluid py-4">
      <div class="card main-card shadow no-copy">
        <div class="card-header bg-primary text-white">
          <div class="d-flex justify-content-center align-items-center">
            <div class="header-icon me-3">
              <i class="bi bi-journal-check"></i>
            </div>
            <h2 class="mb-0">XÉT TUYỂN RIÊNG THEO ĐỀ ÁN TUYỂN SINH</h2>
          </div>
        </div>
        
        <div class="announcement-section p-3 border-bottom">
          <div class="container">
            <h5 class="fw-bold mb-3">Trường Đại học Bách khoa, Đại học Đà Nẵng thông báo tuyển sinh đào tạo trình độ đại học hệ chính quy năm 2025 theo phương thức xét tuyển sinh riêng như sau:</h5>
            
            <div class="mb-3">
              <h6 class="fw-bold">1. Ngành tuyển sinh, mã tuyển sinh</h6>
              <p class="mb-1">Xem Bảng trong danh sách</p>
            </div>
            
            <div class="mb-3">
              <h6 class="fw-bold">2. Đối tượng xét tuyển</h6>
              <p class="mb-1">Thí sinh tốt nghiệp THPT năm 2025 thuộc các nhóm:</p>
              
              <p class="mb-1"><strong>a) Nhóm 1:</strong> Thí sinh đoạt giải Khuyến khích cuộc thi học sinh giỏi cấp quốc gia các môn Toán, Vật lý, Hóa học, Sinh học, Tin học; giải Khuyến khích cuộc thi khoa học, kỹ thuật cấp quốc gia. Thời gian đoạt giải không quá 3 năm tính tới thời điểm xét tuyển.</p>
              
              <p class="mb-1"><em>- Ngành xét tuyển:</em></p>
              <p class="mb-1">Thí sinh đoạt giải tại cuộc thi học sinh giỏi quốc gia được xét tuyển vào một trong số các ngành của Trường, tuỳ thuộc môn thi đoạt giải của thí sinh (xem Phụ lục II).</p>
              <p class="mb-1">Thí sinh đoạt giải tại cuộc thi khoa học, kỹ thuật cấp quốc gia được xét tuyển vào một trong số các ngành tuỳ thuộc lĩnh vực đoạt giải của thí sinh (xem Phụ lục III).</p>
              
              <p class="mb-1"><strong>b) Nhóm 2:</strong> Thí sinh đoạt giải Nhất, Nhì, Ba, Khuyến khích (Giải Tư) tại cuộc thi học sinh giỏi các môn Toán, Vật lý, Hoá học, Sinh học, Tin học cấp tỉnh, thành phố trực thuộc trung ương. Thời gian đoạt giải không quá 3 năm tính tới thời điểm xét tuyển.</p>
              
              <p class="mb-1"><em>- Ngành xét tuyển:</em> Thí sinh được xét trúng tuyển vào một trong các ngành của Trường tuỳ thuộc môn thi đoạt giải của thí sinh (xem Phụ lục II).</p>
              
              <p class="mb-1"><strong>c) Nhóm 3:</strong> Thí sinh đoạt giải Nhất, Nhì, Ba, Khuyến khích (Giải Tư) tại cuộc thi Khoa học kỹ thuật cấp tỉnh, thành phố trực thuộc trung ương. Thời gian đoạt giải không quá 3 năm tính tới thời điểm xét tuyển.</p>
              
              <p class="mb-1"><em>- Ngành xét tuyển:</em> Thí sinh được xét tuyển vào một trong số các ngành tuỳ thuộc lĩnh vực đoạt giải của thí sinh (xem Phụ lục III).</p>
              
              <p class="mb-1"><strong>Lưu ý:</strong> Thí sinh đăng ký xét tuyển ngành Kiến trúc phải dự thi môn năng khiếu Vẽ mỹ thuật do Trường Đại học Bách khoa, Đại học Đà Nẵng tổ chức năm 2025, có điểm thi đạt từ 5,00 điểm trở lên.</p>
            </div>
          </div>
        </div>
        
        <div class="card-body">
          <div v-if="loading" class="text-center py-4">
            <div class="spinner-border text-primary" role="status">
              <span class="visually-hidden">Đang tải...</span>
            </div>
            <p class="mt-3">Đang tải dữ liệu xét tuyển RIÊNG...</p>
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
                    <th scope="col" style="width: 23%">Tên ngành</th>
                    <th scope="col" style="width: 30%">Môn học đạt giải HSG (Phụ lục II)</th>
                    <th scope="col" style="width: 30%">Lĩnh vực KHKT đạt giải (Phụ lục III)</th>
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
                            v-for="(subject, sIndex) in getSubjects(major.admission_fields)" 
                            :key="sIndex"
                            class="badge subject-combo"
                            :class="getSubjectBadgeClass(sIndex)"
                            data-bs-toggle="tooltip"
                            :title="getSubjectDescription(subject, 'subject')"
                          >
                            {{ subject.field_or_subject_name }}
                          </span>
                        </div>
                      </td>
                      <td>
                        <div class="d-flex flex-wrap gap-1">
                          <span 
                            v-for="(field, fIndex) in getFields(major.admission_fields)" 
                            :key="fIndex"
                            class="badge subject-combo"
                            :class="getFieldBadgeClass(fIndex)"
                            data-bs-toggle="tooltip"
                            :title="getSubjectDescription(field, 'field')"
                          >
                            {{ field.field_or_subject_name }}
                          </span>
                        </div>
                      </td>
                    </tr>
                  </template>
                  
                  <tr v-if="filteredMajors.length === 0">
                    <td colspan="5" class="text-center py-4">
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
                    3. Thông tin liên hệ:
                  </h6>
                  <div class="mt-2">
                    <ul class="contact-list">
                      <li>Muốn biết thêm chi tiết, thí sinh vui lòng truy cập trang Tuyển sinh của Trường Đại học Bách khoa tại địa chỉ: <a href="https://tuyensinh.dut.udn.vn/" target="_blank">https://tuyensinh.dut.udn.vn/</a> hoặc trang Tuyển sinh của Đại học Đà Nẵng tại địa chỉ <a href="http://ts.udn.vn" target="_blank">http://ts.udn.vn</a>.</li>
                      <li>Hoặc liên hệ với bộ phận Tuyển sinh của Trường Đại học Bách khoa, số 54 Nguyễn Lương Bằng, TP. Đà Nẵng qua số hotline: 0888 477 377; 0888 377 177; 0888 577 277; 0236 36 20 999;</li>
                      <li>Email: <a href="mailto:tuyensinhbkdn@dut.udn.vn">tuyensinhbkdn@dut.udn.vn</a>;</li>
                      <li>Fanpage: <a href="https://www.facebook.com/DUTpage" target="_blank">https://www.facebook.com/DUTpage</a>;</li>
                      <li>Hoặc liên hệ với Ban Đào tạo, Đại học Đà Nẵng, số 41 Lê Duẩn, TP. Đà Nẵng.</li>
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
      // Định nghĩa chính xác các môn học (không phải lĩnh vực KHKT)
      exactSubjects: ['Toán', 'Vật Lý', 'Hóa Học', 'Sinh Học', 'Tin Học'],
      subjectBadgeClasses: [
        'badge-blue',
        'badge-red',
        'badge-green',
        'badge-teal',
        'badge-purple'
      ],
      fieldBadgeClasses: [
        'badge-yellow',
        'badge-orange',
        'badge-pink',
        'badge-cyan',
        'badge-brown'
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

    // Phương thức lọc ra các môn học (Phụ lục II) - phải khớp chính xác
    getSubjects(admissionFields) {
      if (!admissionFields) return []
      return admissionFields.filter(item => 
        this.exactSubjects.includes(item.field_or_subject_name)
      )
    },

    // Phương thức lọc ra các lĩnh vực KHKT (Phụ lục III) - tất cả các lĩnh vực còn lại
    getFields(admissionFields) {
      if (!admissionFields) return []
      return admissionFields.filter(item => 
        !this.exactSubjects.includes(item.field_or_subject_name)
      )
    },
    
    getSubjectDescription(subject, type) {
      // Mô tả chi tiết về các môn học hoặc lĩnh vực
      if (type === 'subject') {
        return `Môn học đạt giải: ${subject.field_or_subject_name} (Phụ lục II)`
      } else {
        return `Lĩnh vực KHKT đạt giải: ${subject.field_or_subject_name} (Phụ lục III)`
      }
    },

    getSubjectBadgeClass(index) {
      return this.subjectBadgeClasses[index % this.subjectBadgeClasses.length]
    },

    getFieldBadgeClass(index) {
      return this.fieldBadgeClasses[index % this.fieldBadgeClasses.length]
    },

    resetFilters() {
      this.searchQuery = ''
      this.selectedFaculty = 'all'
    }
  }
}
</script>

<style scoped>
.xtr-container {
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
}

.announcement-section h6 {
  font-size: 0.95rem;
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
  cursor: help;
}

/* Các màu cho môn học (Phụ lục II) */
.badge-blue {
  background-color: rgba(13, 110, 253, 0.15);
  color: #0d6efd;
  border: 1px solid rgba(13, 110, 253, 0.3);
}

.badge-red {
  background-color: rgba(220, 53, 69, 0.15);
  color: #dc3545;
  border: 1px solid rgba(220, 53, 69, 0.3);
}

.badge-green {
  background-color: rgba(25, 135, 84, 0.15);
  color: #198754;
  border: 1px solid rgba(25, 135, 84, 0.3);
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

/* Các màu cho lĩnh vực KHKT (Phụ lục III) */
.badge-yellow {
  background-color: rgba(255, 193, 7, 0.15);
  color: #664d03;
  border: 1px solid rgba(255, 193, 7, 0.3);
}

.badge-orange {
  background-color: rgba(253, 126, 20, 0.15);
  color: #fd7e14;
  border: 1px solid rgba(253, 126, 20, 0.3);
}

.badge-pink {
  background-color: rgba(214, 51, 132, 0.15);
  color: #d63384;
  border: 1px solid rgba(214, 51, 132, 0.3);
}

.badge-cyan {
  background-color: rgba(32, 201, 151, 0.15);
  color: #20c997;
  border: 1px solid rgba(32, 201, 151, 0.3);
}

.badge-brown {
  background-color: rgba(165, 42, 42, 0.15);
  color: #a52a2a;
  border: 1px solid rgba(165, 42, 42, 0.3);
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
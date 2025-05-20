<template>
  <div class="dgtd-container">
    <div class="container-fluid py-2 py-md-3">
      <article class="card main-card shadow-sm">
        <!-- Header Section with improved accessibility -->
        <header class="card-header bg-primary text-white" aria-labelledby="dgtd-title">
          <div class="d-flex justify-content-center align-items-center">
            <div class="header-icon me-2" aria-hidden="true">
              <i class="bi bi-journal-check"></i>
            </div>
            <h1 id="dgtd-title" class="mb-0 fs-5">XÉT TUYỂN THEO ĐIỂM THI ĐÁNH GIÁ TƯ DUY CỦA ĐHBK HÀ NỘI</h1>
          </div>
        </header>
        
        <!-- Description Section - simplified and more accessible -->
        <div class="description-section bg-light p-2 border-bottom">
          <div class="container">
            <!-- Accordion for collapsible content -->
            <div class="accordion accordion-flush" id="announcementAccordion">
              <!-- Introduction -->
              <p class="mb-2 small">Trường Đại học Bách khoa, Đại học Đà Nẵng thông báo tuyển sinh đào tạo trình độ đại học chính quy vào các ngành thuộc Trường năm 2025 theo phương thức xét tuyển điểm thi đánh giá tư duy.</p>
              
              <!-- Section 1 -->
              <div class="accordion-item">
                <h2 class="accordion-header">
                  <button class="accordion-button collapsed p-2 fs-7" type="button" data-bs-toggle="collapse" data-bs-target="#section1" aria-expanded="false" aria-controls="section1">
                    <strong>1. Ngành đào tạo, mã xét tuyển</strong>
                  </button>
                </h2>
                <div id="section1" class="accordion-collapse collapse" data-bs-parent="#announcementAccordion">
                  <div class="accordion-body p-2 fs-7">
                    <p class="mb-1">Danh mục các ngành tuyển sinh đào tạo, mã xét tuyển được quy định trong Phụ lục đính kèm.</p>
                  </div>
                </div>
              </div>
              
              <!-- Section 2 -->
              <div class="accordion-item">
                <h2 class="accordion-header">
                  <button class="accordion-button collapsed p-2 fs-7" type="button" data-bs-toggle="collapse" data-bs-target="#section2" aria-expanded="false" aria-controls="section2">
                    <strong>2. Đối tượng tuyển sinh</strong>
                  </button>
                </h2>
                <div id="section2" class="accordion-collapse collapse" data-bs-parent="#announcementAccordion">
                  <div class="accordion-body p-2 fs-7">
                    <ul class="mb-1 ps-3">
                      <li>Đối tượng: thí sinh đã tốt nghiệp THPT hoặc tương đương và có kết quả kỳ thi Đánh giá tư duy do Đại học Bách khoa Hà Nội tổ chức.</li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- Info box with key information -->
            <div class="info-box mt-2">
              <p class="mb-0 small">
                <i class="bi bi-info-circle me-1" aria-hidden="true"></i>
                <strong>Phương thức:</strong> Xét tuyển theo điểm thi đánh giá tư duy của ĐHBK Hà Nội
                <span class="d-block d-sm-inline"><span class="d-none d-sm-inline">|</span> <strong>Mã phương thức:</strong> 402</span>
                <span class="d-block d-sm-inline"><span class="d-none d-sm-inline">|</span> <strong>Điều kiện:</strong> Tham dự kỳ thi năm 2024, 2025 và đạt điểm sàn theo quy định.</span>
              </p>
            </div>
          </div>
        </div>
        
        <!-- Main Content Section with improved loading states -->
        <div class="card-body py-2">
          <!-- Loading State -->
          <div v-if="loading" class="text-center py-3" role="status" aria-live="polite">
            <div class="spinner-border text-primary" aria-hidden="true"></div>
            <p class="mt-2 fs-6">Đang tải dữ liệu xét tuyển...</p>
          </div>
          
          <!-- Error State -->
          <div v-else-if="error" class="alert alert-danger" role="alert">
            <i class="bi bi-exclamation-triangle-fill me-2" aria-hidden="true"></i>
            {{ error }}
          </div>
          
          <!-- Content when data is loaded -->
          <div v-else>
            <!-- Search and Filter Section -->
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
                      <option v-for="faculty in faculties" :key="faculty.falculty_id" :value="faculty.falculty_id">
                        {{ faculty.faculty_code }} - {{ faculty.faculty_name }}
                      </option>
                    </select>
                  </div>
                </div>
              </div>
            </section>
            
            <!-- Major List with responsive design -->
            <section class="table-container mb-3" aria-labelledby="dgtd-table-heading">
              <h2 id="dgtd-table-heading" class="visually-hidden">Danh sách ngành xét tuyển theo điểm ĐGTD</h2>
              
              <!-- Mobile card view (shows on small screens) -->
              <div class="d-md-none">
                <div v-for="(major, index) in filteredMajors" :key="major.id" class="major-card mb-2">
                  <div class="card">
                    <div class="card-header bg-primary text-white d-flex justify-content-between align-items-center py-1">
                      <span class="badge bg-light text-dark">{{ index + 1 }}</span>
                      <h3 class="h6 mb-0 text-truncate small">{{ major.major_name }}</h3>
                    </div>
                    <div class="card-body p-2">
                      <div class="mb-1 small">
                        <span class="fw-bold">Mã ngành:</span> {{ major.major_code }}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              
              <!-- Desktop table view -->
              <div class="table-responsive d-none d-md-block">
                <table class="table table-hover border table-sm">
                  <caption class="visually-hidden">Danh sách ngành xét tuyển theo điểm đánh giá tư duy</caption>
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
                    
                    <!-- No results message -->
                    <tr v-if="filteredMajors.length === 0">
                      <td colspan="3" class="text-center py-3">
                        <div class="no-results">
                          <i class="bi bi-search fs-4 text-muted" aria-hidden="true"></i>
                          <p class="mt-2 fs-6">Không tìm thấy ngành phù hợp với tiêu chí tìm kiếm.</p>
                          <button class="btn btn-outline-primary btn-sm mt-1" @click="resetFilters">
                            <i class="bi bi-arrow-counterclockwise me-2" aria-hidden="true"></i>
                            Đặt lại bộ lọc
                          </button>
                        </div>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </section>
            
            <!-- Info Section about ĐGTD Exam -->
            <section class="info-section mt-3" aria-labelledby="dgtd-info-heading">
              <div class="card">
                <div class="card-body p-2">
                  <h2 id="dgtd-info-heading" class="card-title fs-6 mb-2">
                    <i class="bi bi-info-circle me-2" aria-hidden="true"></i>
                    Thông tin về kỳ thi đánh giá tư duy
                  </h2>
                  <div class="mt-2 small">
                    <p class="mb-2">Kỳ thi đánh giá tư duy (ĐGTD) là một kì thi do Đại học Bách Khoa Hà Nội tổ chức, nhằm đánh giá khả năng tư duy logic, giải quyết vấn đề và năng lực học tập của thí sinh.</p>
                    <p class="fw-medium mb-1">Cấu trúc đề thi Đánh giá tư duy:</p>
                    <ul class="mb-2 ps-3">
                      <li>Phần 1: Tư duy toán học (40 Câu hỏi)</li>
                      <li>Phần 2: Tư duy đọc hiểu (20 Câu hỏi)</li>
                      <li>Phần 3: Tư duy khoa học - Giải quyết vấn đề (40 Câu hỏi)</li>
                    </ul>
                    <p class="fw-medium mb-1">Thang điểm: từ 0 đến 100, trong đó:</p>
                    <ul class="mb-2 ps-3">
                      <li>Điểm trung bình: khoảng 45-55</li>
                      <li>Điểm cao: từ 65 trở lên</li>
                    </ul>
                    <p class="mb-0">Thí sinh cần đạt ngưỡng điểm sàn do trường quy định để đủ điều kiện xét tuyển vào các ngành học.</p>
                  </div>
                </div>
              </div>
            </section>
            
            <!-- Contact Information -->
            <section class="contact-section mt-3" aria-labelledby="contact-heading">
              <div class="card bg-light">
                <div class="card-body p-2">
                  <h2 id="contact-heading" class="card-title fs-6 mb-2">
                    <i class="bi bi-info-circle me-2" aria-hidden="true"></i>
                    3. Thông tin liên hệ
                  </h2>
                  <div class="mt-1">
                    <p class="mb-2 small">Muốn biết thêm chi tiết, thí sinh vui lòng truy cập trang tuyển sinh của Trường Đại học Bách khoa, Đại học Đà Nẵng tại địa chỉ <a href="https://tuyensinh.dut.udn.vn/" target="_blank" rel="noopener noreferrer">tuyensinh.dut.udn.vn</a></p>
                    
                    <ul class="contact-list">
                      <li>Bộ phận Tuyển sinh: 54 Nguyễn Lương Bằng, Liên Chiểu, Đà Nẵng</li>
                      <li>Hotline: <a href="tel:0888477377">0888.477.377</a>, <a href="tel:0888577277">0888.577.277</a></li>
                      <li>Email: <a href="mailto:tuyensinhbkdn@dut.udn.vn">tuyensinhbkdn@dut.udn.vn</a></li>
                      <li>Fanpage: <a href="https://www.facebook.com/DUTpage" target="_blank" rel="noopener noreferrer">facebook.com/DUTpage</a></li>
                    </ul>
                  </div>
                </div>
              </div>
            </section>
          </div>
        </div>
      </article>
    </div>
  </div>
</template>

<script>
import dgtdController from '@/controllers/DGTDController'

export default {
  name: 'DGTDView',
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
      const data = await dgtdController.getDGTDData()
      this.majors = data.dgtd
      
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
      this.initializeAccordion()
    } catch (error) {
      this.error = 'Đã xảy ra lỗi khi tải dữ liệu xét tuyển đánh giá tư duy. Vui lòng thử lại sau.'
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
    
    initializeAccordion() {
      // Khởi tạo accordion nếu cần
      this.$nextTick(() => {
        // Bootstrap 5 tự khởi tạo accordion
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
/* Base Container */
.dgtd-container {
  min-height: 100vh;
  background-color: #f5f5f5;
  margin: 0;
  padding: 0 5px;
}

@media (min-width: 768px) {
  .dgtd-container {
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

/* Accordion Styling */
.accordion-button {
  font-size: 0.85rem;
}

.accordion-button:not(.collapsed) {
  background-color: rgba(13, 110, 253, 0.1);
  color: #0d47a1;
}

.accordion-button:focus {
  box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.25);
}

.info-box {
  background-color: #f8f9fa;
  border-radius: 6px;
  padding: 0.7rem;
  border-left: 3px solid #0d47a1;
}

/* Filter Section */
.filter-section {
  background-color: #f8f9fa;
  padding: 0.75rem;
  border-radius: 6px;
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.05);
}

.form-control, .form-select {
  font-size: 0.875rem;
  padding: 0.25rem 0.5rem;
}

.input-group-text {
  padding: 0.25rem 0.5rem;
  font-size: 0.875rem;
}

/* Table Styling */
.table {
  font-size: 0.8rem;
  margin-bottom: 0.5rem;
}

.table th,
.table td {
  padding: 0.4rem 0.5rem;
  vertical-align: middle;
}

/* Mobile Card View */
.major-card .card {
  border: none;
  border-radius: 6px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.major-card .card-header {
  padding: 0.4rem 0.75rem;
}

.major-card .badge {
  font-size: 0.7rem;
  padding: 0.2rem 0.4rem;
}

/* Info Section */
.info-section .card {
  border: none;
  border-radius: 6px;
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.05);
  background-color: #f0f7ff;
}

/* Contact Section */
.contact-section .card {
  border: none;
  border-radius: 6px;
}

.contact-list {
  padding-left: 1rem;
  margin-bottom: 0;
  font-size: 0.8rem;
}

.contact-list li {
  margin-bottom: 0.4rem;
}

.contact-list a {
  color: #0d47a1;
  text-decoration: none;
}

.contact-list a:hover {
  text-decoration: underline;
}

/* No Results */
.no-results {
  padding: 0.75rem;
}

/* Font size utility */
.fs-7 {
  font-size: 0.75rem !important;
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

/* Responsive adjustments */
@media (max-width: 576px) {
  .header-icon {
    font-size: 1.1rem;
  }
  
  #dgtd-title {
    font-size: 0.95rem !important;
  }
  
  .contact-list {
    font-size: 0.75rem;
  }
}
</style>
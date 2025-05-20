<template>
  <div class="tnthpt-container">
    <div class="container-fluid py-2 py-md-3">
      <article class="card main-card shadow-sm">
        <!-- Header Section with improved accessibility -->
        <header class="card-header bg-primary text-white" aria-labelledby="tnthpt-title">
          <div class="d-flex justify-content-center align-items-center">
            <div class="header-icon me-2" aria-hidden="true">
              <i class="bi bi-file-earmark-text"></i>
            </div>
            <h1 id="tnthpt-title" class="mb-0 fs-5">PHƯƠNG THỨC XÉT ĐIỂM THI TỐT NGHIỆP THPT</h1>
          </div>
        </header>
        
        <!-- Description Section - simplified and more accessible -->
        <div class="description-section bg-light p-2 border-bottom">
          <div class="container">
            <!-- Accordion for collapsible content -->
            <div class="accordion accordion-flush" id="announcementAccordion">
              <!-- Section 1 -->
              <div class="accordion-item">
                <h2 class="accordion-header">
                  <button class="accordion-button p-2 fs-7" type="button" data-bs-toggle="collapse" data-bs-target="#section1" aria-expanded="true" aria-controls="section1">
                    <strong>1. Ngành đào tạo, chỉ tiêu và tiêu chí xét tuyển</strong>
                  </button>
                </h2>
                <div id="section1" class="accordion-collapse collapse show" data-bs-parent="#announcementAccordion">
                  <div class="accordion-body p-2 fs-7">
                    <p class="mb-2">Danh mục các ngành tuyển sinh đào tạo, tổ hợp, mã tổ hợp và tiêu chí xét tuyển được quy định trong Phụ lục đính kèm.</p>
                  </div>
                </div>
              </div>
              
              <!-- Section 2 -->
              <div class="accordion-item">
                <h2 class="accordion-header">
                  <button class="accordion-button collapsed p-2 fs-7" type="button" data-bs-toggle="collapse" data-bs-target="#section2" aria-expanded="false" aria-controls="section2">
                    <strong>2. Đối tượng xét tuyển</strong>
                  </button>
                </h2>
                <div id="section2" class="accordion-collapse collapse" data-bs-parent="#announcementAccordion">
                  <div class="accordion-body p-2 fs-7">
                    <p class="mb-1">Thí sinh tốt nghiệp THPT năm 2025, đạt ngưỡng chất lượng đầu vào do Trường quy định (sẽ thông báo sau).</p>
                  </div>
                </div>
              </div>
              
              <!-- Section 3 -->
              <div class="accordion-item">
                <h2 class="accordion-header">
                  <button class="accordion-button collapsed p-2 fs-7" type="button" data-bs-toggle="collapse" data-bs-target="#section3" aria-expanded="false" aria-controls="section3">
                    <strong>3. Nguyên tắc đăng ký và xét tuyển</strong>
                  </button>
                </h2>
                <div id="section3" class="accordion-collapse collapse" data-bs-parent="#announcementAccordion">
                  <div class="accordion-body p-2 fs-7">
                    <ul class="mb-1 ps-3">
                      <li>Ngưỡng ĐBCL đầu vào được công bố sau khi có kết quả thi THPT.</li>
                      <li>Điểm xét tuyển = Tổng điểm 3 môn thuộc tổ hợp xét tuyển với hệ số tương ứng mỗi môn, quy về thang điểm 30 + Điểm cộng (nếu có)</li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- Info box with key information -->
            <div class="info-box mt-3">
              <p class="mb-0 small">
                <i class="bi bi-info-circle me-1" aria-hidden="true"></i>
                <strong>Phương thức xét tuyển:</strong> Xét kết quả thi tốt nghiệp THPT
                <span class="d-block d-sm-inline"><span class="d-none d-sm-inline">|</span> <strong>Mã phương thức:</strong> 100</span>
                <span class="d-block d-sm-inline"><span class="d-none d-sm-inline">|</span> <strong>Điều kiện:</strong> Tốt nghiệp THPT năm 2025 và đạt ngưỡng đảm bảo chất lượng đầu vào.</span>
              </p>
            </div>
          </div>
        </div>
        
        <!-- Main Content Section with improved loading states -->
        <div class="card-body py-2">
          <!-- Loading State -->
          <div v-if="loading" class="text-center py-3" role="status" aria-live="polite">
            <div class="spinner-border text-primary" aria-hidden="true"></div>
            <p class="mt-2 fs-6">Đang tải dữ liệu phương thức xét tuyển...</p>
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
            <section class="table-container mb-3" aria-labelledby="tnthpt-table-heading">
              <h2 id="tnthpt-table-heading" class="visually-hidden">Danh sách ngành xét tuyển</h2>
              
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
                      <div class="mb-2 small">
                        <span class="fw-bold">Tổ hợp môn xét tuyển:</span>
                        <div class="d-flex flex-wrap gap-1 mt-1">
                          <span 
                            v-for="(subject, sIndex) in major.subject_score_method_majors" 
                            :key="sIndex"
                            class="badge subject-combo"
                            :class="getSubjectBadgeClass(sIndex)"
                          >
                            {{ subject.name }}
                          </span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              
              <!-- Desktop table view -->
              <div class="table-responsive d-none d-md-block">
                <table class="table table-hover border table-sm">
                  <caption class="visually-hidden">Danh sách ngành xét tuyển theo điểm thi THPT</caption>
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
                    
                    <!-- No results message -->
                    <tr v-if="filteredMajors.length === 0">
                      <td colspan="4" class="text-center py-3">
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
            
            <!-- Contact Information -->
            <section class="contact-section mt-3" aria-labelledby="contact-heading">
              <div class="card bg-light">
                <div class="card-body p-2">
                  <h2 id="contact-heading" class="card-title fs-6 mb-2">
                    <i class="bi bi-info-circle me-2" aria-hidden="true"></i>
                    5. Thông tin liên hệ:
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
      this.initializeAccordion()
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
    
    initializeAccordion() {
      // Khởi tạo accordion nếu cần
      this.$nextTick(() => {
        // Không cần code đặc biệt vì Bootstrap 5 tự khởi tạo accordion
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
/* Base Container */
.tnthpt-container {
  min-height: 100vh;
  background-color: #f5f5f5;
  margin: 0;
  padding: 0 5px;
}

@media (min-width: 768px) {
  .tnthpt-container {
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
  margin-top: 0.5rem;
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

/* Subject Badges */
.subject-combo {
  font-size: 0.75rem;
  padding: 0.25rem 0.4rem;
  border-radius: 4px;
  font-weight: 500;
  margin-bottom: 0.2rem;
}

/* Badge Colors */
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
  
  #tnthpt-title {
    font-size: 0.95rem !important;
  }
  
  .contact-list {
    font-size: 0.75rem;
  }
  
  .subject-combo {
    font-size: 0.7rem;
    padding: 0.2rem 0.3rem;
  }
}
</style>
<template>
  <div class="xtt-container">
    <div class="container-fluid py-2 py-md-3">
      <article class="card main-card shadow-sm">
        <!-- Header Section with improved accessibility -->
        <header class="card-header bg-primary text-white" aria-labelledby="xtt-title">
          <div class="d-flex justify-content-center align-items-center">
            <div class="header-icon me-2" aria-hidden="true">
              <i class="bi bi-journal-check"></i>
            </div>
            <h1 id="xtt-title" class="mb-0 fs-5">XÉT TUYỂN THẲNG THEO QUY ĐỊNH CỦA BỘ GIÁO DỤC VÀ ĐÀO TẠO</h1>
          </div>
        </header>
        
        <!-- Description Section - simplified and more accessible -->
        <div class="description-section bg-light p-2 border-bottom">
          <div class="container">
            <p class="description-text mb-1">
              <strong>Trường Đại học Bách khoa (ĐHBK), Đại học Đà Nẵng thông báo tuyển sinh đào tạo trình độ đại học hệ chính quy năm 2025 theo phương thức xét tuyển thẳng.</strong>
            </p>
            
            <div class="announcement-content">
              <!-- Accordion for collapsible content -->
              <div class="accordion accordion-flush" id="announcementAccordion">
                <!-- 1. Ngành tuyển sinh -->
                <div class="accordion-item">
                  <h2 class="accordion-header">
                    <button class="accordion-button collapsed p-2 fs-7" type="button" data-bs-toggle="collapse" data-bs-target="#section1" aria-expanded="false" aria-controls="section1">
                      <strong>1. Ngành tuyển sinh, chỉ tiêu và tiêu chí xét tuyển</strong>
                    </button>
                  </h2>
                  <div id="section1" class="accordion-collapse collapse" data-bs-parent="#announcementAccordion">
                    <div class="accordion-body p-2 fs-7">
                      <p class="mb-1">Xem Danh sách dưới đây</p>
                    </div>
                  </div>
                </div>
                
                <!-- 2. Vùng tuyển -->
                <div class="accordion-item">
                  <h2 class="accordion-header">
                    <button class="accordion-button collapsed p-2 fs-7" type="button" data-bs-toggle="collapse" data-bs-target="#section2" aria-expanded="false" aria-controls="section2">
                      <strong>2. Vùng tuyển, chính sách ưu tiên</strong>
                    </button>
                  </h2>
                  <div id="section2" class="accordion-collapse collapse" data-bs-parent="#announcementAccordion">
                    <div class="accordion-body p-2 fs-7">
                      <ul class="mb-1 ps-3">
                        <li>Vùng tuyển: tuyển sinh trong cả nước.</li>
                        <li>Chính sách ưu tiên: theo quy chế tuyển sinh hiện hành.</li>
                      </ul>
                    </div>
                  </div>
                </div>
                
                <!-- 3. Đối tượng xét tuyển -->
                <div class="accordion-item">
                  <h2 class="accordion-header">
                    <button class="accordion-button collapsed p-2 fs-7" type="button" data-bs-toggle="collapse" data-bs-target="#section3" aria-expanded="false" aria-controls="section3">
                      <strong>3. Đối tượng xét tuyển</strong>
                    </button>
                  </h2>
                  <div id="section3" class="accordion-collapse collapse" data-bs-parent="#announcementAccordion">
                    <div class="accordion-body p-2 fs-7">
                      <p class="mb-1">Nhà trường xét tuyển thẳng cho các nhóm đối tượng sau:</p>
                      
                      <p class="mb-1"><strong>a) Anh hùng lao động, Anh hùng lực lượng vũ trang nhân dân, Chiến sĩ thi đua toàn quốc.</strong></p>
                      
                      <p class="mb-1"><strong>b) Thí sinh đoạt giải nhất, nhì, ba trong kỳ thi chọn học sinh giỏi quốc gia, quốc tế.</strong></p>
                      <p class="mb-1">Thí sinh tốt nghiệp THPT năm 2025.</p>
                      <p class="mb-1">Xem Phụ lục II</p>
                      
                      <p class="mb-1"><strong>c) Thí sinh đoạt giải nhất, nhì, ba trong kỳ thi khoa học, kỹ thuật cấp quốc gia, quốc tế.</strong></p>
                      <p class="mb-1">Thí sinh tốt nghiệp THPT năm 2025.</p>
                      <p class="mb-1">Xem Phụ lục III</p>
                    </div>
                  </div>
                </div>
                
                <!-- 4. Nguyên tắc xét tuyển -->
                <div class="accordion-item">
                  <h2 class="accordion-header">
                    <button class="accordion-button collapsed p-2 fs-7" type="button" data-bs-toggle="collapse" data-bs-target="#section4" aria-expanded="false" aria-controls="section4">
                      <strong>4. Nguyên tắc xét tuyển</strong>
                    </button>
                  </h2>
                  <div id="section4" class="accordion-collapse collapse" data-bs-parent="#announcementAccordion">
                    <div class="accordion-body p-2 fs-7">
                      <ul class="mb-1 ps-3">
                        <li>Xét tuyển vào ngành đúng trước, sau đó xét tuyển vào ngành gần.</li>
                        <li>Mỗi thí sinh trúng tuyển 1 nguyện vọng sẽ không được xét tuyển các nguyện vọng tiếp theo.</li>
                      </ul>
                    </div>
                  </div>
                </div>
                
                <!-- 5. Hồ sơ và lệ phí -->
                <div class="accordion-item">
                  <h2 class="accordion-header">
                    <button class="accordion-button collapsed p-2 fs-7" type="button" data-bs-toggle="collapse" data-bs-target="#section5" aria-expanded="false" aria-controls="section5">
                      <strong>5. Hồ sơ và lệ phí đăng ký xét tuyển</strong>
                    </button>
                  </h2>
                  <div id="section5" class="accordion-collapse collapse" data-bs-parent="#announcementAccordion">
                    <div class="accordion-body p-2 fs-7">
                      <ul class="mb-1 ps-3">
                        <li>Thời gian nhận hồ sơ: Thông báo sau.</li>
                        <li>Đối với ngành Kiến trúc, thí sinh phải dự thi môn năng khiếu "Vẽ mỹ thuật".</li>
                        <li>Đăng ký và nộp hồ sơ xét tuyển: theo hình thức trực tuyến, tại địa chỉ: <a href="https://tuyensinh.dut.udn.vn/" target="_blank" rel="noopener noreferrer">https://tuyensinh.dut.udn.vn</a></li>
                      </ul>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Main Content Section with improved loading states -->
        <div class="card-body py-2">
          <!-- Loading State -->
          <div v-if="loading" class="text-center py-3" role="status" aria-live="polite">
            <div class="spinner-border text-primary" aria-hidden="true"></div>
            <p class="mt-2 fs-6">Đang tải dữ liệu xét tuyển thẳng...</p>
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
            
            <!-- Major List Table with responsive design -->
            <section class="table-container mb-3" aria-labelledby="xtt-table-heading">
              <h2 id="xtt-table-heading" class="visually-hidden">Danh sách ngành xét tuyển thẳng</h2>
              
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
                        <span class="fw-bold">Môn học đạt giải HSG:</span>
                        <div class="d-flex flex-wrap gap-1 mt-1">
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
                      </div>
                      <div class="mb-1 small">
                        <span class="fw-bold">Lĩnh vực KHKT đạt giải:</span>
                        <div class="d-flex flex-wrap gap-1 mt-1">
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
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              
              <!-- Desktop table view -->
              <div class="table-responsive d-none d-md-block">
                <table class="table table-hover border table-sm">
                  <caption class="visually-hidden">Danh sách ngành xét tuyển thẳng tại Trường ĐH Bách Khoa</caption>
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
                    
                    <!-- No results message -->
                    <tr v-if="filteredMajors.length === 0">
                      <td colspan="5" class="text-center py-3 my-2">
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
                    6. Thông tin liên hệ:
                  </h2>
                  <div class="mt-1">
                    <ul class="contact-list">
                      <li>Muốn biết thêm chi tiết, thí sinh vui lòng truy cập trang Tuyển sinh của Trường Đại học Bách khoa tại địa chỉ: <a href="https://tuyensinh.dut.udn.vn/" target="_blank" rel="noopener noreferrer">https://tuyensinh.dut.udn.vn</a></li>
                      <li>Hotline: <a href="tel:0888477377">0888 477 377</a>; <a href="tel:0888477533">0888 477 533</a></li>
                      <li>Email: <a href="mailto:tuyensinhbkdn@dut.udn.vn">tuyensinhbkdn@dut.udn.vn</a></li>
                      <li>Fanpage: <a href="https://www.facebook.com/DUTpage" target="_blank" rel="noopener noreferrer">https://www.facebook.com/DUTpage</a></li>
                      <li>Zalo: <a href="https://zalo.me/dhbkdn2022" target="_blank" rel="noopener noreferrer">https://zalo.me/dhbkdn2022</a></li>
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
import xttController from '@/controllers/xtThangController'

export default {
  name: 'XTTView',
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
      const data = await xttController.getXTTData()
      this.majors = data.xtt
      
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
      this.error = 'Đã xảy ra lỗi khi tải dữ liệu xét tuyển thẳng. Vui lòng thử lại sau.'
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
        // Nhưng có thể thêm tuỳ chỉnh ở đây
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
/* Base Container */
.xtt-container {
  min-height: 100vh;
  background-color: #f5f5f5;
  margin: 0;
  padding: 0 5px;
}

@media (min-width: 768px) {
  .xtt-container {
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
  font-size: 0.85rem;
  line-height: 1.3;
  color: #495057;
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

/* Subject & Field Badges */
.subject-combo {
  font-size: 0.75rem;
  padding: 0.25rem 0.4rem;
  border-radius: 4px;
  font-weight: 500;
  margin-bottom: 0.2rem;
  cursor: help;
}

/* Badge Colors for Subjects */
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

/* Badge Colors for Fields */
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

/* Loading & Error States */
.spinner-border {
  width: 1.5rem;
  height: 1.5rem;
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
  
  #xtt-title {
    font-size: 0.95rem !important;
  }
  
  .description-text, 
  .accordion-button,
  .contact-list {
    font-size: 0.75rem;
  }
  
  .subject-combo {
    font-size: 0.7rem;
    padding: 0.2rem 0.3rem;
  }
}
</style>
<template>
    <div class="major-detail-container">
      <div class="container-fluid py-4">
        <div v-if="loading" class="text-center py-5">
          <div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">Đang tải...</span>
          </div>
          <p class="mt-3 fs-5">Đang tải thông tin chi tiết ngành...</p>
        </div>
        
        <div v-else-if="error" class="alert alert-danger p-4 text-center" role="alert">
          <i class="bi bi-exclamation-triangle-fill me-2"></i>
          {{ error }}
          <div class="mt-3">
            <router-link to="/major" class="btn btn-primary">
              <i class="bi bi-arrow-left me-2"></i> Quay lại danh sách ngành
            </router-link>
          </div>
        </div>
        
        <div v-else-if="majorData">
          <!-- Breadcrumb navigation -->
          <nav aria-label="breadcrumb" class="mb-3">
            <ol class="breadcrumb">
              <li class="breadcrumb-item">
                <router-link to="/" class="text-decoration-none">
                  <i class="bi bi-house-fill"></i> Trang chủ
                </router-link>
              </li>
              <li class="breadcrumb-item">
                <router-link to="/major" class="text-decoration-none">
                  Danh sách ngành
                </router-link>
              </li>
              <li class="breadcrumb-item active" aria-current="page">
                {{ majorData.major.name }}
              </li>
            </ol>
          </nav>
          
          <!-- Header card -->
          <div class="card header-card mb-4">
            <div class="card-body">
              <div class="row align-items-center">
                <div class="col-lg-8">
                  <h1 class="major-title">{{ majorData.major.name }}</h1>
                  <div class="major-meta">
                    <span class="badge bg-primary me-2">Mã ngành: {{ majorData.major.major_code }}</span>
                    <span class="badge bg-info">{{ majorData.major.faculty_name }}</span>
                  </div>
                  <div class="description mt-3">
                    <p>{{ majorData.major.description || 'Chưa có mô tả cho ngành này.' }}</p>
                  </div>
                </div>
                <div class="col-lg-4 mt-4 mt-lg-0">
                  <div class="row g-3">
                    <div class="col-6">
                      <div class="info-card">
                        <div class="info-card-icon">
                          <i class="bi bi-people-fill"></i>
                        </div>
                        <div class="info-card-content">
                          <div class="info-card-label">Chỉ tiêu 2025</div>
                          <div class="info-card-value text-primary">{{ majorData.major.seats }}</div>
                        </div>
                      </div>
                    </div>
                    <div class="col-6">
                      <div class="info-card">
                        <div class="info-card-icon">
                          <i class="bi bi-clipboard2-check-fill"></i>
                        </div>
                        <div class="info-card-content">
                          <div class="info-card-label">Phương thức xét tuyển</div>
                          <div class="info-card-value text-success">{{ majorData.admissionMethods.length }}</div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Main content tabs -->
          <div class="card content-card">
            <div class="card-header">
              <ul class="nav nav-tabs card-header-tabs" id="majorDetailTabs" role="tablist">
                <li class="nav-item" role="presentation">
                  <button class="nav-link active" id="admission-methods-tab" data-bs-toggle="tab" data-bs-target="#admission-methods" type="button" role="tab" aria-controls="admission-methods" aria-selected="true">
                    <i class="bi bi-list-check me-1"></i> Phương thức xét tuyển
                  </button>
                </li>
                <li class="nav-item" role="presentation">
                  <button class="nav-link" id="subject-groups-tab" data-bs-toggle="tab" data-bs-target="#subject-groups" type="button" role="tab" aria-controls="subject-groups" aria-selected="false">
                    <i class="bi bi-grid-3x3-gap me-1"></i> Tổ hợp xét tuyển
                  </button>
                </li>
                <li class="nav-item" role="presentation">
                  <button class="nav-link" id="achievements-tab" data-bs-toggle="tab" data-bs-target="#achievements" type="button" role="tab" aria-controls="achievements" aria-selected="false">
                    <i class="bi bi-trophy me-1"></i> Thành tích xét tuyển
                  </button>
                </li>
                <li class="nav-item" role="presentation">
                  <button class="nav-link" id="previous-scores-tab" data-bs-toggle="tab" data-bs-target="#previous-scores" type="button" role="tab" aria-controls="previous-scores" aria-selected="false">
                    <i class="bi bi-bar-chart-line me-1"></i> Điểm chuẩn các năm
                  </button>
                </li>
              </ul>
            </div>
            <div class="card-body">
              <div class="tab-content" id="majorDetailTabsContent">
                <!-- Phương thức xét tuyển tab -->
                <div class="tab-pane fade show active" id="admission-methods" role="tabpanel" aria-labelledby="admission-methods-tab">
                  <h4 class="section-title">Các phương thức xét tuyển áp dụng</h4>
                  <p class="text-muted">
                    Ngành {{ majorData.major.name }} áp dụng {{ majorData.admissionMethods.length }} phương thức xét tuyển sau:
                  </p>
                  
                  <div class="row g-4">
                    <div v-for="method in majorData.admissionMethods" :key="method.admission_methods_id" class="col-md-6">
                      <div class="method-card">
                        <div class="method-card-header">
                          <span class="method-number">{{ method.admission_methods_id }}</span>
                          <h5>{{ method.name }}</h5>
                        </div>
                        <div class="method-card-body">
                          <p>{{ method.description || 'Không có mô tả chi tiết cho phương thức này.' }}</p>
                          <div class="method-info" v-if="method.min_score || method.max_score">
                            <span class="method-info-item" v-if="method.min_score">
                              <i class="bi bi-arrow-down-square me-1"></i> Điểm tối thiểu: {{ method.min_score }}
                            </span>
                            <span class="method-info-item" v-if="method.max_score">
                              <i class="bi bi-arrow-up-square me-1"></i> Điểm tối đa: {{ method.max_score }}
                            </span>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                
                <!-- Tổ hợp xét tuyển tab -->
                <div class="tab-pane fade" id="subject-groups" role="tabpanel" aria-labelledby="subject-groups-tab">
                  <h4 class="section-title">Tổ hợp xét tuyển</h4>
                  
                  <div v-if="majorData.subjectGroups.length === 0" class="alert alert-info">
                    <i class="bi bi-info-circle me-2"></i>
                    Ngành này không có tổ hợp xét tuyển nào được áp dụng.
                  </div>
                  
                  <div v-else>
                    <div v-for="(methodGroups, index) in majorData.subjectGroups" :key="index" class="method-group-section">
                      <h5 class="method-group-title">
                        <i class="bi bi-journal-check me-2"></i>
                        {{ methodGroups.method_name }}
                      </h5>
                      
                      <div v-if="methodGroups.groups.length === 0" class="alert alert-warning">
                        <i class="bi bi-exclamation-triangle me-2"></i>
                        Không có thông tin về tổ hợp xét tuyển cho phương thức này.
                      </div>
                      
                      <div v-else class="row g-3">
                        <div v-for="group in methodGroups.groups" :key="group.id" class="col-md-4">
                          <div class="group-card">
                            <i class="bi bi-grid-3x3"></i>
                            <div class="group-name">{{ group.name }}</div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                
                <!-- Thành tích xét tuyển tab -->
                <div class="tab-pane fade" id="achievements" role="tabpanel" aria-labelledby="achievements-tab">
                  <h4 class="section-title">Thành tích xét tuyển thẳng & xét tuyển riêng</h4>
                  
                  <div v-if="!majorData.admissionDescriptions || (!majorData.admissionDescriptions.subjects.length && !majorData.admissionDescriptions.fields.length)" class="alert alert-info">
                    <i class="bi bi-info-circle me-2"></i>
                    Ngành này không có thông tin về thành tích xét tuyển thẳng và xét tuyển riêng.
                  </div>
                  
                  <div v-else class="row">
                    <div class="col-md-6">
                      <div class="achievement-section">
                        <h5 class="achievement-title">
                          <i class="bi bi-book me-2"></i> Môn học đạt giải
                        </h5>
                        
                        <div v-if="majorData.admissionDescriptions.subjects.length === 0" class="alert alert-warning">
                          <i class="bi bi-exclamation-triangle me-2"></i>
                          Không có môn học nào được áp dụng.
                        </div>
                        
                        <div v-else class="achievement-items">
                          <div v-for="subject in majorData.admissionDescriptions.subjects" :key="subject.id" class="achievement-item subjects">
                            <span class="achievement-name">{{ subject.field_or_subject_name }}</span>
                          </div>
                        </div>
                      </div>
                    </div>
                    
                    <div class="col-md-6">
                      <div class="achievement-section">
                        <h5 class="achievement-title">
                          <i class="bi bi-lightbulb me-2"></i> Lĩnh vực KHKT đạt giải
                        </h5>
                        
                        <div v-if="majorData.admissionDescriptions.fields.length === 0" class="alert alert-warning">
                          <i class="bi bi-exclamation-triangle me-2"></i>
                          Không có lĩnh vực nào được áp dụng.
                        </div>
                        
                        <div v-else class="achievement-items">
                          <div v-for="field in majorData.admissionDescriptions.fields" :key="field.id" class="achievement-item fields">
                            <span class="achievement-name">{{ field.field_or_subject_name }}</span>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                
                <!-- Điểm chuẩn các năm tab -->
                <div class="tab-pane fade" id="previous-scores" role="tabpanel" aria-labelledby="previous-scores-tab">
                  <h4 class="section-title">Điểm chuẩn trúng tuyển các năm trước</h4>
                  
                  <div v-if="Object.keys(majorData.previousScores).length === 0" class="alert alert-info">
                    <i class="bi bi-info-circle me-2"></i>
                    Chưa có thông tin điểm chuẩn các năm trước cho ngành này.
                  </div>
                  
                  <div v-else class="previous-scores-wrapper">
                    <div v-for="(scores, year) in majorData.previousScores" :key="year" class="previous-scores-section">
                      <h5 class="year-title">Năm {{ year }}</h5>
                      
                      <div class="table-responsive">
                        <table class="table table-hover">
                          <thead class="table-primary">
                            <tr>
                              <th scope="col" style="width: 5%">STT</th>
                              <th scope="col" style="width: 55%">Phương thức xét tuyển</th>
                              <th scope="col" class="text-center" style="width: 40%">Điểm chuẩn</th>
                            </tr>
                          </thead>
                          <tbody>
                            <tr v-for="(score, index) in scores" :key="score.id">
                              <td>{{ index + 1 }}</td>
                              <td>{{ score.method_name }}</td>
                              <td class="text-center fw-bold score-value">{{ score.score }}</td>
                            </tr>
                          </tbody>
                        </table>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Back button -->
          <div class="text-center mt-4">
            <router-link to="/major" class="btn btn-outline-primary btn-lg">
              <i class="bi bi-arrow-left me-2"></i> Quay lại danh sách ngành
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, onMounted } from 'vue'
  import { useRoute } from 'vue-router'
  import DetailMajorController from '@/controllers/DetailMajorController'
  
  export default {
    name: 'MajorDetail',
    setup() {
      const route = useRoute()
      const majorId = route.params.id
      
      const majorData = ref(null)
      const loading = ref(true)
      const error = ref(null)
      
      const loadMajorDetail = async () => {
        try {
          loading.value = true
          error.value = null
          
          majorData.value = await DetailMajorController.getCompleteMajorDetail(majorId)
          
          // Cập nhật tiêu đề trang
          document.title = `${majorData.value.major.name} - Thông tin tuyển sinh 2025`
          
          // Khởi tạo các tabs bootstrap sau khi dữ liệu được tải
          setTimeout(() => {
            const triggerEl = document.querySelector('#majorDetailTabs button[data-bs-toggle="tab"]')
            if (triggerEl) {
              const tab = new bootstrap.Tab(triggerEl)
              tab.show()
            }
          }, 100)
          
        } catch (err) {
          console.error('Lỗi khi tải thông tin chi tiết ngành:', err)
          error.value = 'Đã xảy ra lỗi khi tải thông tin chi tiết ngành. Vui lòng thử lại sau.'
        } finally {
          loading.value = false
        }
      }
      
      onMounted(() => {
        loadMajorDetail()
      })
      
      return {
        majorId,
        majorData,
        loading,
        error
      }
    }
  }
  </script>
  
  <style scoped>
  .major-detail-container {
    min-height: 100vh;
    background-color: #f5f5f5;
    margin: 0 5vw;
  }
  
  .breadcrumb-item a {
    color: #0d47a1;
  }
  
  .breadcrumb-item.active {
    color: #6c757d;
    font-weight: 600;
  }
  
  .header-card {
    border: none;
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 0.25rem 0.5rem rgba(0, 0, 0, 0.12);
  }
  
  .major-title {
    color: #0d47a1;
    font-size: 2rem;
    font-weight: 700;
    margin-bottom: 0.75rem;
  }
  
  .major-meta {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-bottom: 0.5rem;
  }
  
  .major-meta .badge {
    padding: 0.65rem 1rem;
    font-size: 0.9rem;
  }
  
  .description {
    color: #495057;
    font-size: 1.05rem;
    line-height: 1.6;
  }
  
  .info-card {
    background-color: #f8f9fa;
    border-radius: 10px;
    padding: 1.25rem;
    box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
    display: flex;
    align-items: center;
    height: 100%;
  }
  
  .info-card-icon {
    width: 50px;
    height: 50px;
    border-radius: 50%;
    background-color: rgba(13, 71, 161, 0.1);
    color: #0d47a1;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
    margin-right: 1rem;
  }
  
  .info-card-content {
    flex: 1;
  }
  
  .info-card-label {
    color: #6c757d;
    font-size: 0.9rem;
    margin-bottom: 0.25rem;
  }
  
  .info-card-value {
    font-size: 1.8rem;
    font-weight: 700;
  }
  
  .content-card {
    border: none;
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 0.25rem 0.5rem rgba(0, 0, 0, 0.12);
  }
  
  .card-header-tabs {
    margin-top: -0.5rem;
    margin-bottom: -0.5rem;
  }
  
  .nav-tabs .nav-link {
    color: #495057;
    background-color: transparent;
    border: none;
    padding: 1rem 1.5rem;
    transition: all 0.2s ease;
  }
  
  .nav-tabs .nav-link.active {
    color: #0d47a1;
    background-color: #ffffff;
    border-bottom: 3px solid #0d47a1;
    font-weight: 600;
  }
  
  .nav-tabs .nav-link:hover:not(.active) {
    background-color: rgba(0, 0, 0, 0.05);
  }
  
  .section-title {
    color: #0d47a1;
    margin-bottom: 1.25rem;
    font-weight: 600;
    position: relative;
    padding-bottom: 0.75rem;
  }
  
  .section-title::after {
    content: '';
    position: absolute;
    left: 0;
    bottom: 0;
    width: 60px;
    height: 3px;
    background-color: #0d47a1;
  }
  
  /* Method cards styling */
  .method-card {
    background-color: #ffffff;
    border-radius: 10px;
    box-shadow: 0 0.25rem 0.5rem rgba(0, 0, 0, 0.08);
    overflow: hidden;
    height: 100%;
    transition: transform 0.3s ease;
  }
  
  .method-card:hover {
    transform: translateY(-5px);
  }
  
  .method-card-header {
    background-color: #f0f7ff;
    padding: 1.25rem;
    position: relative;
    border-bottom: 1px solid #e9ecef;
  }
  
  .method-number {
    position: absolute;
    top: 10px;
    right: 15px;
    width: 30px;
    height: 30px;
    border-radius: 50%;
    background-color: #0d47a1;
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.9rem;
    font-weight: 600;
  }
  
  .method-card-header h5 {
    color: #0d47a1;
    font-weight: 600;
    margin: 0;
    padding-right: 40px;
  }
  
  .method-card-body {
    padding: 1.25rem;
  }
  
  .method-card-body p {
    color: #495057;
    margin-bottom: 1rem;
  }
  
  .method-info {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
  }
  
  .method-info-item {
    background-color: rgba(13, 71, 161, 0.1);
    color: #0d47a1;
    padding: 0.5rem 0.75rem;
    border-radius: 6px;
    font-size: 0.9rem;
  }
  
  /* Group cards styling */
  .method-group-section:not(:first-child) {
    margin-top: 2rem;
    padding-top: 2rem;
    border-top: 1px solid #e9ecef;
  }
  
  .method-group-title {
    color: #495057;
    font-weight: 600;
    margin-bottom: 1rem;
  }
  
  .group-cards, .group-card {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
  }
  
  .group-card {
    background-color: #e8f1ff;
    border-left: 4px solid #0d47a1;
    padding: 1rem;
    border-radius: 8px;
    align-items: center;
    width: 100%;
  }
  
  .group-card i {
    color: #0d47a1;
    font-size: 1.25rem;
    margin-right: 0.75rem;
  }
  
  .group-name {
    font-weight: 500;
    color: #0d47a1;
  }
  
  /* Achievement items styling */
  .achievement-section {
    margin-bottom: 1.5rem;
  }
  
  .achievement-title {
    color: #495057;
    font-weight: 600;
    margin-bottom: 1rem;
  }
  
  .achievement-items {
    display: flex;
    flex-wrap: wrap;
    gap: 0.75rem;
  }
  
  .achievement-item {
    padding: 0.65rem 1rem;
    border-radius: 20px;
    font-size: 0.95rem;
    font-weight: 500;
  }
  
  .achievement-item.subjects {
    background-color: rgba(13, 71, 161, 0.1);
    color: #0d47a1;
    border: 1px solid rgba(13, 71, 161, 0.2);
  }
  
  .achievement-item.fields {
    background-color: rgba(25, 135, 84, 0.1);
    color: #198754;
    border: 1px solid rgba(25, 135, 84, 0.2);
  }
  
  /* Previous scores styling */
  .previous-scores-section:not(:first-child) {
    margin-top: 2rem;
  }
  
  .year-title {
    color: #0d47a1;
    font-weight: 600;
    margin-bottom: 1rem;
  }
  
  .score-value {
    color: #198754;
    font-size: 1.1rem;
  }
  
  /* Responsive adjustments */
  @media (max-width: 992px) {
    .major-title {
      font-size: 1.75rem;
    }
    
    .info-card-value {
      font-size: 1.5rem;
    }
    
    .nav-tabs .nav-link {
      padding: 0.75rem 1rem;
      font-size: 0.9rem;
    }
  }
  
  @media (max-width: 768px) {
    .major-title {
      font-size: 1.5rem;
    }
    
    .description {
      font-size: 1rem;
    }
    
    .info-card {
      padding: 1rem;
    }
    
    .info-card-icon {
      width: 40px;
      height: 40px;
      font-size: 1.25rem;
    }
    
    .method-card-header {
      padding: 1rem;
    }
    
    .nav-tabs .nav-link {
      padding: 0.5rem 0.75rem;
      font-size: 0.85rem;
    }
  }
  
  @media (max-width: 576px) {
    .major-detail-container {
      margin: 0;
    }
    
    .major-title {
      font-size: 1.3rem;
    }
    
    .info-card-label {
      font-size: 0.8rem;
    }
    
    .info-card-value {
      font-size: 1.25rem;
    }
    
    .section-title {
      font-size: 1.25rem;
    }
    
    .method-card-header h5 {
      font-size: 1rem;
    }
    
    .nav-tabs {
      flex-wrap: nowrap;
      overflow-x: auto;
      white-space: nowrap;
      -webkit-overflow-scrolling: touch;
    }
  }
  </style>
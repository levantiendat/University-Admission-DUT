<template>
    <div class="major-list-container">
      <div class="container-fluid py-5">
        <div class="card main-card shadow">
          <div class="card-header bg-primary text-white">
            <div class="d-flex justify-content-center align-items-center">
              <div class="header-icon me-3">
                <i class="bi bi-book-fill"></i>
              </div>
              <h2 class="mb-0">DANH SÁCH NGÀNH TUYỂN SINH NĂM 2025</h2>
            </div>
          </div>
          
          <div class="description-section bg-light p-3 border-bottom">
            <div class="container">
              <p class="description-text mb-0">
                <i class="bi bi-info-circle me-2"></i>
                Danh sách các ngành đào tạo và chỉ tiêu tuyển sinh của Trường Đại học Bách khoa - Đại học Đà Nẵng năm 2025.
                Thí sinh có thể tìm hiểu chi tiết về ngành học, điểm chuẩn các năm trước và các phương thức xét tuyển áp dụng.
              </p>
            </div>
          </div>
          
          <div class="card-body">
            <div v-if="loading" class="text-center py-5">
              <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Đang tải...</span>
              </div>
              <p class="mt-3 fs-5">Đang tải dữ liệu ngành tuyển sinh...</p>
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
                        <option v-for="faculty in faculties" :key="faculty.id" :value="faculty.id">
                          {{ faculty.faculty_code }} - {{ faculty.name }}
                        </option>
                      </select>
                    </div>
                  </div>
                </div>
              </div>
              
              <!-- Bảng danh sách ngành -->
              <div class="table-responsive major-table custom-scroll">
                <table class="table table-hover border">
                  <thead>
                    <tr class="bg-primary text-white">
                      <th scope="col" class="text-center" style="width: 5%">STT</th>
                      <th scope="col" style="width: 12%">Mã ngành</th>
                      <th scope="col" style="width: 25%">Tên ngành</th>
                      <th scope="col" style="width: 25%">Khoa</th>
                      <th scope="col" class="text-center" style="width: 8%">Chỉ tiêu</th>
                      <th scope="col" class="text-center" style="width: 15%">Phương thức xét tuyển</th>
                      <th scope="col" class="text-center" style="width: 10%">Thao tác</th>
                    </tr>
                  </thead>
                  <tbody>
                    <template v-for="(major, index) in filteredMajors" :key="major.id">
                      <tr>
                        <td class="text-center">{{ index + 1 }}</td>
                        <td>{{ major.major_code }}</td>
                        <td class="fw-medium">{{ major.name }}</td>
                        <td>{{ major.faculty_name }}</td>
                        <td class="text-center fw-bold">{{ major.seats }}</td>
                        <td class="text-center">
                          <div class="method-count">
                            <span class="badge bg-info">
                              {{ major.method_count }} phương thức
                            </span>
                          </div>
                        </td>
                        <td class="text-center">
                          <div class="d-flex justify-content-center">
                            <button class="btn btn-sm btn-outline-primary me-2" @click="showMajorQuickView(major.id)">
                              <i class="bi bi-eye"></i> Xem
                            </button>
                            <router-link :to="{ name: 'MajorDetail', params: { id: major.id }}" class="btn btn-sm btn-primary">
                              <i class="bi bi-info-circle"></i> Chi tiết
                            </router-link>
                          </div>
                        </td>
                      </tr>
                    </template>
                    
                    <tr v-if="filteredMajors.length === 0">
                      <td colspan="7" class="text-center py-5">
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
            </div>
          </div>
        </div>
      </div>
      
      <!-- Modal xem nhanh thông tin ngành -->
      <div class="modal fade" id="majorQuickViewModal" tabindex="-1" aria-labelledby="majorModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered modal-xl">
          <div class="modal-content">
            <div class="modal-header bg-primary text-white">
              <h5 class="modal-title" id="majorModalLabel">
                <i class="bi bi-mortarboard-fill me-2"></i>
                {{ selectedMajor ? selectedMajor.name : 'Thông tin ngành' }}
              </h5>
              <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body p-0">
              <div v-if="loadingMajorDetail" class="text-center p-5">
                <div class="spinner-border text-primary" role="status">
                  <span class="visually-hidden">Đang tải...</span>
                </div>
                <p class="mt-3">Đang tải thông tin chi tiết ngành...</p>
              </div>
              
              <div v-else-if="selectedMajor" class="p-4">
                <div class="row mb-4">
                  <div class="col-md-8">
                    <h4 class="major-name mb-2">{{ selectedMajor.name }}</h4>
                    <p class="mb-2">
                      <span class="badge bg-secondary me-2">Mã ngành: {{ selectedMajor.major_code }}</span>
                      <span class="badge bg-info">Khoa: {{ selectedMajor.faculty_name }}</span>
                    </p>
                    <div class="major-description mt-3">
                      <h6 class="text-primary mb-2">Mô tả ngành:</h6>
                      <p>{{ selectedMajor.description || 'Chưa có mô tả cho ngành này.' }}</p>
                    </div>
                  </div>
                  <div class="col-md-4">
                    <div class="detail-card quota mb-3">
                      <div class="detail-card-title">
                        <i class="bi bi-people-fill me-2"></i> Chỉ tiêu 2025
                      </div>
                      <div class="detail-card-value">{{ selectedMajor.seats }}</div>
                    </div>
                    <div class="detail-card methods">
                      <div class="detail-card-title">
                        <i class="bi bi-check2-square me-2"></i> Phương thức xét tuyển
                      </div>
                      <div class="detail-card-value">{{ majorMethods?.length || 0 }}</div>
                    </div>
                  </div>
                </div>
                
                <!-- Phương thức xét tuyển -->
                <div class="quick-view-section">
                  <h5 class="section-heading">
                    <i class="bi bi-list-check me-2"></i>
                    Các phương thức xét tuyển
                  </h5>
                  <div class="method-cards">
                    <div v-for="method in majorMethods" :key="method.admission_methods_id" class="method-card">
                      <div class="method-name">{{ method.name }}</div>
                    </div>
                  </div>
                </div>
                
                <!-- Tổ hợp xét tuyển -->
                <div class="quick-view-section">
                  <h5 class="section-heading">
                    <i class="bi bi-grid-3x3-gap me-2"></i>
                    Tổ hợp xét tuyển
                  </h5>
                  <div class="subject-groups">
                    <div v-for="(groupInfo, idx) in majorSubjectGroups" :key="idx" class="subject-group-section">
                      <h6 class="method-name mb-2">{{ groupInfo.method_name }}</h6>
                      <div class="group-cards">
                        <div v-for="group in groupInfo.groups" :key="group.id" class="group-card">
                          {{ group.name }}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                
                <!-- Điểm chuẩn các năm trước -->
                <div class="quick-view-section">
                  <h5 class="section-heading">
                    <i class="bi bi-bar-chart-line me-2"></i>
                    Điểm chuẩn các năm trước
                  </h5>
                  <div class="previous-scores">
                    <div v-for="(scores, year) in majorPreviousScores" :key="year" class="score-year-section">
                      <h6 class="year-title">Năm {{ year }}</h6>
                      <div class="score-cards">
                        <div v-for="(score, idx) in scores" :key="idx" class="score-card">
                          <div class="method-name">{{ score.method_name }}</div>
                          <div class="score-value">{{ score.score }}</div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                
                <!-- Liên kết xem chi tiết -->
                <div class="text-center mt-4">
                  <router-link :to="{ name: 'MajorDetail', params: { id: selectedMajor.id }}" class="btn btn-primary btn-lg">
                    <i class="bi bi-info-circle-fill me-2"></i> Xem thông tin chi tiết ngành
                  </router-link>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, computed, onMounted } from 'vue'
  import DetailMajorController from '@/controllers/DetailMajorController'
  
  export default {
    name: 'MajorList',
    setup() {
      // States
      const majors = ref([])
      const faculties = ref([])
      const searchQuery = ref('')
      const selectedFaculty = ref('all')
      const loading = ref(true)
      const error = ref(null)
      
      // Quick view state
      const selectedMajor = ref(null)
      const majorMethods = ref([])
      const majorSubjectGroups = ref([])
      const majorPreviousScores = ref({})
      const majorAdmissionDescriptions = ref(null)
      const loadingMajorDetail = ref(false)
      
      // Computed properties
      const filteredMajors = computed(() => {
        let result = majors.value
  
        // Lọc theo khoa nếu đã chọn khoa
        if (selectedFaculty.value !== 'all') {
          result = result.filter(major => major.faculty_id === selectedFaculty.value)
        }
  
        // Lọc theo từ khóa tìm kiếm
        if (searchQuery.value) {
          const query = searchQuery.value.toLowerCase()
          result = result.filter(major => 
            major.major_code.toLowerCase().includes(query) ||
            major.name.toLowerCase().includes(query) ||
            major.faculty_name?.toLowerCase().includes(query)
          )
        }
  
        return result
      })
      
      const totalSeats = computed(() => {
        return majors.value.reduce((sum, major) => sum + major.seats, 0)
      })
      
      // Methods
      const loadData = async () => {
        try {
          loading.value = true
          
          // Lấy danh sách ngành và số phương thức xét tuyển cho mỗi ngành
          const majorsData = await DetailMajorController.getMajors()
          const methodsPromises = majorsData.map(major => 
            DetailMajorController.getMajorAdmissionMethods(major.id)
              .then(methods => ({
                majorId: major.id,
                methodCount: methods.length
              }))
              .catch(() => ({ majorId: major.id, methodCount: 0 }))
          )
          
          const methodsCounts = await Promise.all(methodsPromises)
          
          // Thêm số lượng phương thức xét tuyển vào mỗi ngành
          majorsData.forEach(major => {
            const methodData = methodsCounts.find(m => m.majorId === major.id)
            major.method_count = methodData ? methodData.methodCount : 0
          })
          
          majors.value = majorsData
          faculties.value = await DetailMajorController.getFaculties()
          
        } catch (err) {
          console.error('Lỗi khi tải dữ liệu:', err)
          error.value = 'Đã xảy ra lỗi khi tải dữ liệu. Vui lòng thử lại sau.'
        } finally {
          loading.value = false
        }
      }
      
      const showMajorQuickView = async (majorId) => {
        try {
          loadingMajorDetail.value = true
          
          // Lấy thông tin chi tiết để hiển thị trong modal
          const majorDetail = await DetailMajorController.getMajorDetail(majorId)
          selectedMajor.value = majorDetail
          
          // Lấy các phương thức xét tuyển
          majorMethods.value = await DetailMajorController.getMajorAdmissionMethods(majorId)
          
          // Lấy điểm chuẩn các năm trước
          majorPreviousScores.value = await DetailMajorController.getPreviousAdmissionScores(majorId)
          
          // Lấy tổ hợp thi cho phương thức xét tuyển điểm thi THPT và học bạ
          const thptMethod = majorMethods.value.find(m => m.admission_methods_id === 6)
          const hocbaMethod = majorMethods.value.find(m => m.admission_methods_id === 3)
          
          const subjectGroupsPromises = []
          if (thptMethod) {
            subjectGroupsPromises.push(
              DetailMajorController.getMajorSubjectGroups(majorId, 6)
                .then(groups => ({
                  admission_method_id: 6,
                  method_name: thptMethod.name,
                  groups
                }))
                .catch(() => ({
                  admission_method_id: 6,
                  method_name: thptMethod.name,
                  groups: []
                }))
            )
          }
          
          if (hocbaMethod) {
            subjectGroupsPromises.push(
              DetailMajorController.getMajorSubjectGroups(majorId, 3)
                .then(groups => ({
                  admission_method_id: 3,
                  method_name: hocbaMethod.name,
                  groups
                }))
                .catch(() => ({
                  admission_method_id: 3,
                  method_name: hocbaMethod.name,
                  groups: []
                }))
            )
          }
          
          majorSubjectGroups.value = await Promise.all(subjectGroupsPromises)
          
          // Hiển thị modal
          const modal = new bootstrap.Modal(document.getElementById('majorQuickViewModal'))
          modal.show()
          
        } catch (err) {
          console.error('Lỗi khi lấy thông tin chi tiết ngành:', err)
          error.value = 'Đã xảy ra lỗi khi tải thông tin chi tiết ngành.'
        } finally {
          loadingMajorDetail.value = false
        }
      }
      
      const resetFilters = () => {
        searchQuery.value = ''
        selectedFaculty.value = 'all'
      }
      
      // Mounted hook
      onMounted(() => {
        loadData()
      })
      
      return {
        majors,
        faculties,
        loading,
        error,
        searchQuery,
        selectedFaculty,
        filteredMajors,
        totalSeats,
        resetFilters,
        showMajorQuickView,
        selectedMajor,
        majorMethods,
        majorSubjectGroups,
        majorPreviousScores,
        majorAdmissionDescriptions,
        loadingMajorDetail
      }
    }
  }
  </script>
  
  <style scoped>
  .major-list-container {
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
  
  .major-table {
    border-radius: 10px;
    overflow: hidden;
  }
  
  .custom-scroll {
    overflow-x: auto;
    overflow-y: auto;
    max-height: 70vh;
  }
  
  .method-count .badge {
    font-size: 0.9rem;
    padding: 0.5rem;
  }
  
  /* Modal quick view styles */
  .major-name {
    color: #0d47a1;
    font-weight: 700;
  }
  
  .detail-card {
    background-color: #f8f9fa;
    border-radius: 8px;
    padding: 1.25rem;
    text-align: center;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  }
  
  .detail-card-title {
    color: #495057;
    font-size: 1rem;
    margin-bottom: 0.5rem;
  }
  
  .detail-card-value {
    font-size: 2rem;
    font-weight: 700;
    color: #0d47a1;
  }
  
  .detail-card.quota .detail-card-value {
    color: #28a745;
  }
  
  .quick-view-section {
    margin-top: 2rem;
    padding-top: 1.5rem;
    border-top: 1px solid #e9ecef;
  }
  
  .section-heading {
    color: #0d47a1;
    font-weight: 600;
    margin-bottom: 1rem;
  }
  
  .method-cards {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
    margin-top: 1rem;
  }
  
  .method-card {
    flex: 0 0 calc(33.333% - 1rem);
    background-color: #e8f1ff;
    border-left: 4px solid #0d47a1;
    padding: 1rem;
    border-radius: 8px;
  }
  
  .method-name {
    font-weight: 500;
    color: #0d47a1;
  }
  
  .subject-groups {
    margin-top: 1rem;
  }
  
  .subject-group-section:not(:first-child) {
    margin-top: 1.5rem;
  }
  
  .group-cards {
    display: flex;
    flex-wrap: wrap;
    gap: 0.75rem;
    margin-top: 0.75rem;
  }
  
  .group-card {
    background-color: rgba(13, 71, 161, 0.1);
    color: #0d47a1;
    border: 1px solid rgba(13, 71, 161, 0.2);
    padding: 0.5rem 1rem;
    border-radius: 20px;
    font-size: 0.9rem;
  }
  
  .score-year-section:not(:first-child) {
    margin-top: 1.5rem;
  }
  
  .year-title {
    font-weight: 600;
    color: #495057;
    margin-bottom: 0.75rem;
  }
  
  .score-cards {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
  }
  
  .score-card {
    flex: 0 0 calc(25% - 1rem);
    background-color: #f8f9fa;
    border-radius: 8px;
    padding: 1rem;
    border-left: 4px solid #28a745;
  }
  
  .score-value {
    font-size: 1.5rem;
    font-weight: 700;
    color: #28a745;
    margin-top: 0.5rem;
  }
  
  /* Stats section */
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
  
  /* Responsive adjustments */
  @media (max-width: 992px) {
    .method-card {
      flex: 0 0 calc(50% - 1rem);
    }
    
    .score-card {
      flex: 0 0 calc(50% - 1rem);
    }
  }
  
  @media (max-width: 768px) {
    .card-header h2 {
      font-size: 1.3rem;
    }
    
    .header-icon {
      font-size: 2rem;
    }
    
    .stats-section .card {
      margin-bottom: 1rem;
    }
    
    .method-card {
      flex: 0 0 100%;
    }
    
    .score-card {
      flex: 0 0 100%;
    }
  }
  
  @media (max-width: 576px) {
    .description-text {
      font-size: 0.95rem;
    }
    
    .card-header h2 {
      font-size: 1rem;
    }
    
    .header-icon {
      font-size: 1.5rem;
    }
  }
  </style>
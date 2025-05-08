<template>
  <main class="major-detail-container">
    <div class="container-fluid py-3">
      <div v-if="loading" class="text-center py-3">
        <div class="spinner-border spinner-border-sm text-primary" role="status">
          <span class="visually-hidden">Đang tải...</span>
        </div>
        <p class="mt-2 small">Đang tải thông tin chi tiết ngành...</p>
      </div>
      
      <div v-else-if="error" class="alert alert-danger p-3 text-center" role="alert">
        <i class="bi bi-exclamation-triangle-fill me-2" aria-hidden="true"></i>
        {{ error }}
        <div class="mt-2">
          <router-link to="/major" class="btn btn-primary btn-sm">
            <i class="bi bi-arrow-left me-1" aria-hidden="true"></i> Quay lại danh sách ngành
          </router-link>
        </div>
      </div>
      
      <div v-else-if="majorData">
        <!-- Breadcrumb navigation -->
        <nav aria-label="breadcrumb" class="mb-2">
          <ol class="breadcrumb small">
            <li class="breadcrumb-item">
              <router-link to="/" class="text-decoration-none">
                <i class="bi bi-house-fill" aria-hidden="true"></i> Trang chủ
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
        <section class="card header-card mb-3">
          <div class="card-body p-2 p-md-3">
            <div class="row align-items-center">
              <div class="col-lg-8">
                <h1 class="major-title">{{ majorData.major.name }}</h1>
                <div class="major-meta">
                  <span class="badge bg-primary me-1">Mã: {{ majorData.major.major_code }}</span>
                  <span class="badge bg-info">{{ majorData.major.faculty_name }}</span>
                </div>
                <div class="description mt-2">
                  <p class="small mb-0">{{ majorData.major.description || 'Chưa có mô tả cho ngành này.' }}</p>
                </div>
              </div>
              <div class="col-lg-4 mt-3 mt-lg-0">
                <div class="row g-2">
                  <div class="col-6">
                    <div class="info-card">
                      <div class="info-card-icon" aria-hidden="true">
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
                      <div class="info-card-icon" aria-hidden="true">
                        <i class="bi bi-clipboard2-check-fill"></i>
                      </div>
                      <div class="info-card-content">
                        <div class="info-card-label">Phương thức</div>
                        <div class="info-card-value text-success">{{ majorData.admissionMethods.length }}</div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>
        
        <!-- Main content tabs -->
        <section class="card content-card">
          <div class="card-header p-0">
            <ul class="nav nav-tabs card-header-tabs" id="majorDetailTabs" role="tablist">
              <li class="nav-item" role="presentation">
                <button class="nav-link active" id="admission-methods-tab" data-bs-toggle="tab" data-bs-target="#admission-methods" type="button" role="tab" aria-controls="admission-methods" aria-selected="true">
                  <i class="bi bi-list-check me-1" aria-hidden="true"></i> Phương thức
                </button>
              </li>
              <li class="nav-item" role="presentation">
                <button class="nav-link" id="subject-groups-tab" data-bs-toggle="tab" data-bs-target="#subject-groups" type="button" role="tab" aria-controls="subject-groups" aria-selected="false">
                  <i class="bi bi-grid-3x3-gap me-1" aria-hidden="true"></i> Tổ hợp
                </button>
              </li>
              <li class="nav-item" role="presentation">
                <button class="nav-link" id="achievements-tab" data-bs-toggle="tab" data-bs-target="#achievements" type="button" role="tab" aria-controls="achievements" aria-selected="false">
                  <i class="bi bi-trophy me-1" aria-hidden="true"></i> Thành tích
                </button>
              </li>
              <li class="nav-item" role="presentation">
                <button class="nav-link" id="previous-scores-tab" data-bs-toggle="tab" data-bs-target="#previous-scores" type="button" role="tab" aria-controls="previous-scores" aria-selected="false">
                  <i class="bi bi-bar-chart-line me-1" aria-hidden="true"></i> Điểm chuẩn
                </button>
              </li>
            </ul>
          </div>
          <div class="card-body p-2 p-md-3">
            <div class="tab-content" id="majorDetailTabsContent">
              <!-- Phương thức xét tuyển tab -->
              <div class="tab-pane fade show active" id="admission-methods" role="tabpanel" aria-labelledby="admission-methods-tab">
                <h2 class="section-title">Các phương thức xét tuyển áp dụng</h2>
                <p class="text-muted small mb-2">
                  Ngành {{ majorData.major.name }} áp dụng {{ majorData.admissionMethods.length }} phương thức xét tuyển sau:
                </p>
                
                <div class="row g-2">
                  <div v-for="method in majorData.admissionMethods" :key="method.admission_methods_id" class="col-md-6">
                    <div class="method-card">
                      <div class="method-card-header">
                        <span class="method-number">{{ method.admission_methods_id }}</span>
                        <h3 class="h6 mb-0">{{ method.name }}</h3>
                      </div>
                      <div class="method-card-body">
                        <p class="small mb-1">{{ method.description || 'Không có mô tả chi tiết cho phương thức này.' }}</p>
                        <div class="method-info" v-if="method.min_score || method.max_score">
                          <span class="method-info-item" v-if="method.min_score">
                            <i class="bi bi-arrow-down-square me-1" aria-hidden="true"></i> Tối thiểu: {{ method.min_score }}
                          </span>
                          <span class="method-info-item" v-if="method.max_score">
                            <i class="bi bi-arrow-up-square me-1" aria-hidden="true"></i> Tối đa: {{ method.max_score }}
                          </span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              
              <!-- Tổ hợp xét tuyển tab -->
              <div class="tab-pane fade" id="subject-groups" role="tabpanel" aria-labelledby="subject-groups-tab">
                <h2 class="section-title">Tổ hợp xét tuyển</h2>
                
                <div v-if="majorData.subjectGroups.length === 0" class="alert alert-info py-2 small">
                  <i class="bi bi-info-circle me-1" aria-hidden="true"></i>
                  Ngành này không có tổ hợp xét tuyển nào được áp dụng.
                </div>
                
                <div v-else>
                  <div v-for="(methodGroups, index) in majorData.subjectGroups" :key="index" class="method-group-section">
                    <h3 class="method-group-title h6">
                      <i class="bi bi-journal-check me-1" aria-hidden="true"></i>
                      {{ methodGroups.method_name }}
                    </h3>
                    
                    <div v-if="methodGroups.groups.length === 0" class="alert alert-warning py-2 small">
                      <i class="bi bi-exclamation-triangle me-1" aria-hidden="true"></i>
                      Không có thông tin về tổ hợp xét tuyển cho phương thức này.
                    </div>
                    
                    <div v-else class="row g-2">
                      <div v-for="group in methodGroups.groups" :key="group.id" class="col-6 col-md-4">
                        <div class="group-card">
                          <i class="bi bi-grid-3x3" aria-hidden="true"></i>
                          <div class="group-name">{{ group.name }}</div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              
              <!-- Thành tích xét tuyển tab -->
              <div class="tab-pane fade" id="achievements" role="tabpanel" aria-labelledby="achievements-tab">
                <h2 class="section-title">Thành tích xét tuyển thẳng & xét tuyển riêng</h2>
                
                <div v-if="!majorData.admissionDescriptions || (!majorData.admissionDescriptions.subjects.length && !majorData.admissionDescriptions.fields.length)" class="alert alert-info py-2 small">
                  <i class="bi bi-info-circle me-1" aria-hidden="true"></i>
                  Ngành này không có thông tin về thành tích xét tuyển thẳng và xét tuyển riêng.
                </div>
                
                <div v-else class="row g-2">
                  <div class="col-md-6">
                    <div class="achievement-section">
                      <h3 class="achievement-title h6">
                        <i class="bi bi-book me-1" aria-hidden="true"></i> Môn học đạt giải
                      </h3>
                      
                      <div v-if="majorData.admissionDescriptions.subjects.length === 0" class="alert alert-warning py-2 small">
                        <i class="bi bi-exclamation-triangle me-1" aria-hidden="true"></i>
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
                      <h3 class="achievement-title h6">
                        <i class="bi bi-lightbulb me-1" aria-hidden="true"></i> Lĩnh vực KHKT đạt giải
                      </h3>
                      
                      <div v-if="majorData.admissionDescriptions.fields.length === 0" class="alert alert-warning py-2 small">
                        <i class="bi bi-exclamation-triangle me-1" aria-hidden="true"></i>
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
              
              <!-- Điểm chuẩn các năm tab - Đã tối ưu, nổi bật hơn -->
              <div class="tab-pane fade" id="previous-scores" role="tabpanel" aria-labelledby="previous-scores-tab">
                <h2 class="section-title">
                  <i class="bi bi-award me-2" aria-hidden="true"></i>
                  Điểm chuẩn trúng tuyển các năm trước
                </h2>
                
                <div v-if="!formattedPreviousScores || Object.keys(formattedPreviousScores).length === 0" class="alert alert-info py-2 small">
                  <i class="bi bi-info-circle me-1" aria-hidden="true"></i>
                  Chưa có thông tin điểm chuẩn các năm trước cho ngành này.
                </div>
                
                <div v-else class="previous-score-container">
                  <!-- Banner điểm chuẩn -->
                  <div class="benchmark-banner">
                    <div class="benchmark-header">
                      <i class="bi bi-graph-up-arrow me-2" aria-hidden="true"></i>
                      Điểm chuẩn qua các năm
                    </div>
                  </div>
                  
                  <!-- Bảng điểm chuẩn tổng hợp các năm - thiết kế nổi bật -->
                  <div class="benchmark-table">
                    <div class="table-responsive">
                      <table class="table table-hover table-bordered score-table">
                        <thead>
                          <tr>
                            <th scope="col" class="method-col">Phương thức xét tuyển</th>
                            <th scope="col" class="year-col text-center">
                              <span class="year-label">2023</span>
                            </th>
                            <th scope="col" class="year-col text-center">
                              <span class="year-label">2024</span>
                            </th>
                          </tr>
                        </thead>
                        <tbody>
                          <tr v-for="(method, methodIndex) in uniqueMethods" :key="`method-${methodIndex}`">
                            <td class="method-name">
                              <div class="d-flex align-items-center">
                                <div class="method-icon">
                                  <i :class="getMethodIcon(method)" aria-hidden="true"></i>
                                </div>
                                <span>{{ method }}</span>
                              </div>
                            </td>
                            <td class="text-center score-2023" :class="getScoreClass('2023', method)">
                              {{ getScoreForYearAndMethod('2023', method) }}
                            </td>
                            <td class="text-center score-2024" :class="getScoreClass('2024', method)">
                              {{ getScoreForYearAndMethod('2024', method) }}
                            </td>
                          </tr>
                        </tbody>
                      </table>
                    </div>
                  </div>
                  
                  <div class="benchmark-footer">
                    <div class="info-tip">
                      <i class="bi bi-info-circle-fill me-1" aria-hidden="true"></i>
                      <small>Điểm chuẩn trên thang điểm tương ứng với từng phương thức xét tuyển</small>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>
        
        <!-- Back button -->
        <div class="text-center mt-3">
          <router-link to="/major" class="btn btn-outline-primary btn-sm">
            <i class="bi bi-arrow-left me-1" aria-hidden="true"></i> Quay lại danh sách ngành
          </router-link>
        </div>
      </div>
    </div>
  </main>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
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
    
    // Xử lý dữ liệu điểm chuẩn theo định dạng đúng
    const formattedPreviousScores = computed(() => {
      if (!majorData.value || !majorData.value.previousScores) return {}
      
      // Chuyển đổi và đảm bảo các năm được xử lý dưới dạng chuỗi
      const result = {}
      
      for (const [year, scores] of Object.entries(majorData.value.previousScores)) {
        result[year] = Array.isArray(scores) ? scores : []
      }
      
      return result
    })
    
    // Sắp xếp các năm theo thứ tự giảm dần (mới nhất lên đầu)
    const sortedYears = computed(() => {
      if (!formattedPreviousScores.value) return []
      return Object.keys(formattedPreviousScores.value)
        .map(year => parseInt(year, 10))
        .sort((a, b) => b - a)
        .map(year => year.toString())
    })
    
    const uniqueMethods = computed(() => {
      if (!formattedPreviousScores.value) return []
      
      const methodSet = new Set()
      
      Object.values(formattedPreviousScores.value).forEach(yearScores => {
        yearScores.forEach(score => {
          methodSet.add(score.method_name)
        })
      })
      
      return Array.from(methodSet)
    })
    
    // Lấy điểm theo năm và phương thức
    const getScoreForYearAndMethod = (year, methodName) => {
      if (!formattedPreviousScores.value || !formattedPreviousScores.value[year]) {
        return '-'
      }
      
      const scoreData = formattedPreviousScores.value[year].find(
        score => score.method_name === methodName
      )
      
      return scoreData ? scoreData.score : '-'
    }
    
    // Hàm chọn icon dựa vào tên phương thức
    const getMethodIcon = (methodName) => {
      if (methodName.includes('Xét tuyển thẳng')) return 'bi bi-award'
      if (methodName.includes('Xét học bạ') || methodName.includes('học tập cấp THPT')) return 'bi bi-journal-check'
      if (methodName.includes('thi tốt nghiệp') || methodName.includes('THPT')) return 'bi bi-file-earmark-text'
      if (methodName.includes('đánh giá năng lực') || methodName.includes('ĐGNL')) return 'bi bi-stars'
      if (methodName.includes('tuyển sinh riêng') || methodName.includes('xét tuyển riêng')) return 'bi bi-diagram-3'
      if (methodName.includes('đánh giá tư duy') || methodName.includes('ĐGTD')) return 'bi bi-lightbulb'
      
      // Icon mặc định
      return 'bi bi-bookmark'
    }
    
    // Thêm class cho ô điểm
    const getScoreClass = (year, methodName) => {
      const score = getScoreForYearAndMethod(year, methodName)
      if (score === '-') return '';
      
      // Phân loại các mức điểm chuẩn
      if (parseFloat(score) > 27) return 'score-very-high';
      if (parseFloat(score) > 24) return 'score-high';
      if (parseFloat(score) > 20) return 'score-medium';
      return 'score-normal';
    }
    
    // Viết tắt tên phương thức
    const getShortMethodName = (fullName) => {
      if (!fullName) return ''
      if (fullName.includes('Xét tuyển thẳng')) return 'Xét tuyển thẳng'
      if (fullName.includes('Xét kết quả học tập cấp THPT (học bạ)')) return 'Xét học bạ'
      if (fullName.includes('Xét kết quả thi tốt nghiệp Trung Học Phổ Thông')) return 'Xét điểm thi THPT'
      if (fullName.includes('Xét kết quả thi đánh giá năng lực do ĐHQG TP.HCM tổ chức')) return 'Xét điểm thi ĐGNL'
      if (fullName.includes('Xét tuyển theo phương thức xét tuyển riêng')) return 'Tuyển sinh riêng'
      if (fullName.includes('Xét kết quả thi đánh giá tư duy do Đại Học Bách Khoa Hà Nội tổ chức')) return 'Xét điểm thi ĐGTD'

      // Nếu không khớp với các mẫu trên, lấy các chữ cái đầu tiên
      const words = fullName.split(' ')
      if (words.length <= 2) return fullName

      return words
        .filter(word => word.length > 1)
        .map(word => word.charAt(0))
        .join('')
    }
    
    const loadMajorDetail = async () => {
      try {
        loading.value = true
        error.value = null
        
        majorData.value = await DetailMajorController.getCompleteMajorDetail(majorId)
        console.log("Dữ liệu điểm chuẩn:", majorData.value.previousScores)
        
        // Cập nhật tiêu đề trang
        document.title = `${majorData.value.major.name} - Thông tin tuyển sinh 2025`
        
        // Khởi tạo các tabs bootstrap sau khi dữ liệu được tải
        setTimeout(() => {
          try {
            // Chỉ khởi tạo bootstrap tabs nếu bootstrap tồn tại
            if (window.bootstrap && window.bootstrap.Tab) {
              const triggerEl = document.querySelector('#majorDetailTabs button[data-bs-toggle="tab"]')
              if (triggerEl) {
                const tab = new bootstrap.Tab(triggerEl)
                tab.show()
              }
            }
          } catch (err) {
            console.error('Lỗi khi khởi tạo Bootstrap tabs:', err)
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
      error,
      formattedPreviousScores,
      sortedYears,
      uniqueMethods,
      getShortMethodName,
      getScoreForYearAndMethod,
      getMethodIcon,
      getScoreClass
    }
  }
}
</script>

<style scoped>
.major-detail-container {
  min-height: 100vh;
  background-color: #f5f5f5;
  margin: 0 2vw;
  padding-bottom: 1rem;
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
  border-radius: 0.5rem;
  overflow: hidden;
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.08);
}

.major-title {
  color: #0d47a1;
  font-size: 1.3rem;
  font-weight: 700;
  margin-bottom: 0.35rem;
}

.major-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 0.35rem;
  margin-bottom: 0.25rem;
}

.major-meta .badge {
  padding: 0.25rem 0.5rem;
  font-size: 0.8rem;
}

.description {
  color: #495057;
}

.info-card {
  background-color: #f8f9fa;
  border-radius: 0.5rem;
  padding: 0.75rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  display: flex;
  align-items: center;
  height: 100%;
}

.info-card-icon {
  width: 2rem;
  height: 2rem;
  border-radius: 50%;
  background-color: rgba(13, 71, 161, 0.1);
  color: #0d47a1;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1rem;
  margin-right: 0.5rem;
}

.info-card-content {
  flex: 1;
}

.info-card-label {
  color: #6c757d;
  font-size: 0.75rem;
  margin-bottom: 0.15rem;
}

.info-card-value {
  font-size: 1.2rem;
  font-weight: 700;
}

.content-card {
  border: none;
  border-radius: 0.5rem;
  overflow: hidden;
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.08);
}

.nav-tabs .nav-link {
  color: #495057;
  background-color: transparent;
  border: none;
  padding: 0.5rem 0.75rem;
  transition: all 0.2s ease;
  font-size: 0.85rem;
}

.nav-tabs .nav-link.active {
  color: #0d47a1;
  background-color: #ffffff;
  border-bottom: 2px solid #0d47a1;
  font-weight: 600;
}

.nav-tabs .nav-link:hover:not(.active) {
  background-color: rgba(0, 0, 0, 0.05);
}

.section-title {
  color: #0d47a1;
  margin-bottom: 0.75rem;
  font-weight: 600;
  position: relative;
  padding-bottom: 0.5rem;
  font-size: 1.1rem;
}

.section-title::after {
  content: '';
  position: absolute;
  left: 0;
  bottom: 0;
  width: 40px;
  height: 2px;
  background-color: #0d47a1;
}

/* Method cards styling */
.method-card {
  background-color: #ffffff;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  overflow: hidden;
  height: 100%;
  transition: transform 0.2s ease;
}

.method-card:hover {
  transform: translateY(-3px);
}

.method-card-header {
  background-color: #f0f7ff;
  padding: 0.75rem;
  position: relative;
  border-bottom: 1px solid #e9ecef;
}

.method-number {
  position: absolute;
  top: 8px;
  right: 8px;
  width: 1.5rem;
  height: 1.5rem;
  border-radius: 50%;
  background-color: #0d47a1;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.8rem;
  font-weight: 600;
}

.method-card-header h3 {
  color: #0d47a1;
  font-weight: 600;
  margin: 0;
  padding-right: 2rem;
}

.method-card-body {
  padding: 0.75rem;
}

.method-info {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.method-info-item {
  background-color: rgba(13, 71, 161, 0.1);
  color: #0d47a1;
  padding: 0.25rem 0.5rem;
  border-radius: 0.35rem;
  font-size: 0.8rem;
}

/* Group cards styling */
.method-group-section:not(:first-child) {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #e9ecef;
}

.method-group-title {
  color: #495057;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.group-card {
  background-color: #e8f1ff;
  border-left: 3px solid #0d47a1;
  padding: 0.5rem;
  border-radius: 0.35rem;
  display: flex;
  align-items: center;
  height: 100%;
}

.group-card i {
  color: #0d47a1;
  font-size: 0.9rem;
  margin-right: 0.5rem;
}

.group-name {
  font-weight: 500;
  color: #0d47a1;
  font-size: 0.85rem;
}

/* Achievement items styling */
.achievement-section {
  margin-bottom: 1rem;
}

.achievement-title {
  color: #495057;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.achievement-items {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.achievement-item {
  padding: 0.35rem 0.6rem;
  border-radius: 1rem;
  font-size: 0.8rem;
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

/* Điểm chuẩn các năm - Thiết kế nổi bật */
.previous-score-container {
  background: #ffffff;
  border-radius: 0.5rem;
  overflow: hidden;
  box-shadow: 0 0.25rem 0.75rem rgba(0, 41, 103, 0.08);
  border: 1px solid rgba(13, 71, 161, 0.1);
}

/* Banner */
.benchmark-banner {
  background: linear-gradient(135deg, #0d47a1, #1976d2);
  padding: 0.75rem 1rem;
  color: white;
}

.benchmark-header {
  font-size: 1.1rem;
  font-weight: 600;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
  display: flex;
  align-items: center;
}

/* Table */
.benchmark-table {
  padding: 0.5rem;
}

.score-table {
  margin-bottom: 0;
  border-collapse: separate;
  border-spacing: 0;
  border-radius: 0.5rem;
  overflow: hidden;
}

.score-table thead th {
  background: #e8f0fe;
  color: #0d47a1;
  font-weight: 600;
  border-bottom: 2px solid #1976d2;
  padding: 0.6rem;
  vertical-align: middle;
  position: relative;
}

.score-table .year-col {
  width: 25%;
  background-color: #e3f2fd;
}

.score-table .year-label {
  position: relative;
  font-weight: 700;
}

.score-table .method-col {
  width: 50%;
}

.score-table td {
  padding: 0.6rem;
  vertical-align: middle;
}

.method-name {
  font-weight: 500;
  color: #263238;
  font-size: 0.85rem;
}

.method-icon {
  width: 1.8rem;
  height: 1.8rem;
  background-color: rgba(13, 71, 161, 0.08);
  color: #0d47a1;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  margin-right: 0.5rem;
  font-size: 0.9rem;
}

/* Score cells styling */
.score-table td.score-2023, .score-table td.score-2024 {
  font-weight: 700;
  font-size: 0.95rem;
  position: relative;
}

.score-table td.score-very-high {
  color: #c62828;
  background-color: rgba(198, 40, 40, 0.08);
}

.score-table td.score-high {
  color: #e64a19;
  background-color: rgba(230, 74, 25, 0.08);
}

.score-table td.score-medium {
  color: #0288d1;
  background-color: rgba(2, 136, 209, 0.08);
}

.score-table td.score-normal {
  color: #2e7d32;
  background-color: rgba(46, 125, 50, 0.08);
}

.benchmark-footer {
  background-color: #f5f9ff;
  padding: 0.6rem 1rem;
  border-top: 1px solid #e0e8f5;
}

.info-tip {
  display: flex;
  align-items: center;
  color: #7a8793;
}

.info-tip i {
  color: #1976d2;
  font-size: 0.9rem;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .major-detail-container {
    margin: 0;
  }
  
  .nav-tabs {
    flex-wrap: nowrap;
    overflow-x: auto;
    white-space: nowrap;
    -webkit-overflow-scrolling: touch;
  }
  
  .nav-tabs .nav-link {
    padding: 0.35rem 0.5rem;
    font-size: 0.75rem;
  }
  
  .method-name {
    font-size: 0.8rem;
  }
  
  .method-icon {
    width: 1.5rem;
    height: 1.5rem;
    font-size: 0.8rem;
  }
  
  .score-table td.score-2023, .score-table td.score-2024 {
    font-size: 0.85rem;
  }
}

@media (max-width: 576px) {
  .method-card-header h3 {
    font-size: 0.9rem;
  }
  
  .major-title {
    font-size: 1.1rem;
  }
  
  .info-card-value {
    font-size: 1.1rem;
  }
  
  .section-title {
    font-size: 1rem;
  }
  
  .benchmark-header {
    font-size: 1rem;
  }
}
</style>
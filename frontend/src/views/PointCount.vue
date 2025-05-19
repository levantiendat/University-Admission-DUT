<template>
  <div>
    <!-- Hero Section - More compact like CalculateScoreTHPT -->
    <header class="hero-section py-3 py-md-4 text-center text-white">
      <div class="container">
        <h1 class="fw-bold mb-1">Tính Điểm Xét Tuyển</h1>
        <p>Trường Đại học Bách Khoa - Đại học Đà Nẵng</p>
      </div>
    </header>

    <!-- Main Content: Improved accessibility and mobile responsiveness -->
    <main class="container my-3 my-md-4">
      <div class="card shadow-sm rounded">
        <div class="card-header text-white text-center py-2">
          <h2 class="h5 mb-0">Tính điểm xét tuyển riêng - Trường ĐHBK - ĐHĐN</h2>
        </div>
        <div class="card-body p-2 p-md-3">
          <form @submit.prevent="calculatePoint" id="pointForm">
            <!-- Bước 1: Chọn nhóm xét tuyển -->
            <div class="mb-3">
              <label for="group" class="form-label small mb-1">Chọn nhóm xét tuyển</label>
              <select 
                v-model="form.group" 
                class="form-select form-select-sm" 
                id="group" 
                @change="toggleSections"
                :class="{'is-invalid': errors.group && submitted}"
                aria-describedby="group-feedback">
                <option value="">-- Chọn nhóm --</option>
                <option value="1">Nhóm 1: Giải Khuyến khích Học sinh giỏi / Cuộc thi khoa học kỹ thuật cấp Quốc Gia</option>
                <option value="2">Nhóm 2: Học sinh giỏi cấp tỉnh, thành phố trực thuộc trung ương</option>
                <option value="3">Nhóm 3: Cuộc thi khoa học kỹ thuật cấp tỉnh, thành phố trực thuộc trung ương</option>
              </select>
              <div id="group-feedback" class="invalid-feedback" v-if="errors.group && submitted">
                {{ errors.group }}
              </div>
            </div>

            <!-- Bước 2: Chọn loại thành tích (nếu có) -->
            <div class="mb-3" v-if="showAchievement">
              <label for="achievement" class="form-label small mb-1">Chọn loại thành tích</label>
              <select 
                v-model="form.achievement" 
                class="form-select form-select-sm" 
                id="achievement"
                :class="{'is-invalid': errors.achievement && submitted}"
                aria-describedby="achievement-feedback">
                <option value="">-- Chọn loại giải --</option>
                <option value="I">Giải Nhất</option>
                <option value="II">Giải Nhì</option>
                <option value="III">Giải Ba</option>
                <option value="Khuyến khích">Giải Khuyến khích</option>
              </select>
              <div id="achievement-feedback" class="invalid-feedback" v-if="errors.achievement && submitted">
                {{ errors.achievement }}
              </div>
            </div>

            <!-- Bước 3: Nhập điểm học bạ (nếu có) -->
            <div class="mb-3" v-if="showAchievement">
              <label class="form-label small mb-1">Điểm tổng kết</label>
              <div class="row g-2">
                <div class="col-12 col-sm-4">
                  <div class="input-group input-group-sm">
                    <span class="input-group-text">Lớp 10</span>
                    <input 
                      type="number" 
                      step="0.1" 
                      min="0" 
                      max="10" 
                      class="form-control form-control-sm" 
                      id="score10"
                      v-model.number="form.score10" 
                      @input="validateScore('score10')"
                      :class="{'is-invalid': errors.score10}"
                      aria-describedby="score10-feedback">
                  </div>
                  <div id="score10-feedback" class="invalid-feedback" v-if="errors.score10">
                    {{ errors.score10 }}
                  </div>
                </div>
                <div class="col-12 col-sm-4">
                  <div class="input-group input-group-sm">
                    <span class="input-group-text">Lớp 11</span>
                    <input 
                      type="number" 
                      step="0.1" 
                      min="0" 
                      max="10" 
                      class="form-control form-control-sm" 
                      id="score11"
                      v-model.number="form.score11" 
                      @input="validateScore('score11')"
                      :class="{'is-invalid': errors.score11}"
                      aria-describedby="score11-feedback">
                  </div>
                  <div id="score11-feedback" class="invalid-feedback" v-if="errors.score11">
                    {{ errors.score11 }}
                  </div>
                </div>
                <div class="col-12 col-sm-4">
                  <div class="input-group input-group-sm">
                    <span class="input-group-text">Lớp 12</span>
                    <input 
                      type="number" 
                      step="0.1" 
                      min="0" 
                      max="10" 
                      class="form-control form-control-sm"
                      id="score12" 
                      v-model.number="form.score12" 
                      @input="validateScore('score12')"
                      :class="{'is-invalid': errors.score12}"
                      aria-describedby="score12-feedback">
                  </div>
                  <div id="score12-feedback" class="invalid-feedback" v-if="errors.score12">
                    {{ errors.score12 }}
                  </div>
                </div>
              </div>
              <!-- Thông báo lỗi chung cho điểm số -->
              <div class="alert alert-warning mt-2 py-1 px-2 small" v-if="hasScoreErrors" role="alert">
                <i class="bi bi-exclamation-triangle me-1" aria-hidden="true"></i>
                Vui lòng kiểm tra lại điểm số. Điểm phải nằm trong khoảng từ 0 đến 10 và có tối đa 1 chữ số thập phân.
              </div>
            </div>

            <!-- Bước 4: Chọn trường (xác định khu vực ưu tiên) -->
            <h3 class="section-title h6 mt-3 mb-2">Chọn trường</h3>
            <div class="school-selection-container p-2 p-md-3">
              <div class="row g-2">
                <div class="col-12">
                  <label for="city" class="form-label small mb-1">Tỉnh/Thành phố</label>
                  <select 
                    v-model="form.city_id" 
                    class="form-select form-select-sm" 
                    id="city" 
                    @change="loadDistricts"
                    :class="{'is-invalid': errors.city_id && submitted}"
                    aria-describedby="city-feedback">
                    <option value="">-- Chọn Tỉnh/Thành phố --</option>
                    <option v-for="city in cities" :key="city.id" :value="city.id">
                      {{ city.name }}
                    </option>
                  </select>
                  <div id="city-feedback" class="invalid-feedback" v-if="errors.city_id && submitted">
                    {{ errors.city_id }}
                  </div>
                </div>
                <div class="col-12 col-md-6">
                  <label for="district" class="form-label small mb-1">Quận/Huyện</label>
                  <select 
                    v-model="form.district_id" 
                    class="form-select form-select-sm" 
                    id="district" 
                    @change="loadSchools" 
                    :disabled="!districts.length"
                    :class="{'is-invalid': errors.district_id && submitted}"
                    aria-describedby="district-feedback">
                    <option value="">-- Chọn Quận/Huyện --</option>
                    <option v-for="district in districts" :key="district.id" :value="district.id">
                      {{ district.name }}
                    </option>
                  </select>
                  <div id="district-feedback" class="invalid-feedback" v-if="errors.district_id && submitted">
                    {{ errors.district_id }}
                  </div>
                </div>
                <div class="col-12 col-md-6">
                  <label for="school" class="form-label small mb-1">Trường THPT</label>
                  <select 
                    v-model="form.school_id" 
                    class="form-select form-select-sm" 
                    id="school" 
                    :disabled="!schools.length"
                    :class="{'is-invalid': errors.school_id && submitted}"
                    aria-describedby="school-feedback">
                    <option value="">-- Chọn Trường THPT --</option>
                    <option v-for="school in schools" :key="school.id" :value="school.id" :data-priority="school.priority_area">
                      {{ school.name }}
                    </option>
                  </select>
                  <div id="school-feedback" class="invalid-feedback" v-if="errors.school_id && submitted">
                    {{ errors.school_id }}
                  </div>
                </div>
              </div>
              <div class="mt-2 text-center" v-if="selectedSchoolPriority">
                <p class="small fw-bold mb-0">Khu vực ưu tiên: {{ selectedSchoolPriority }}</p>
              </div>
            </div>

            <!-- Bước 5: Chọn đối tượng ưu tiên -->
            <div class="mb-3 mt-3">
              <h3 class="section-title h6 mb-2">Chọn Ưu tiên đối tượng</h3>
              <select 
                v-model="form.priority_object" 
                class="form-select form-select-sm priority-select" 
                id="priority_object">
                <option value="0">Không có đối tượng ưu tiên</option>
                <option value="ĐT01">ĐT01: Người dân tộc thiểu số tại KV1 (trên 18 tháng)</option>
                <option value="ĐT02">ĐT02: Công nhân trực tiếp sản xuất (5 năm+, 2 năm CSTĐ)</option>
                <option value="ĐT03">ĐT03a: Thương binh, bệnh binh, người hưởng chính sách như thương binh</option>
                <option value="ĐT03">ĐT03b: Quân nhân, CA tại ngũ tại KV1 (12 tháng+)</option>
                <option value="ĐT03">ĐT03c: Quân nhân, CA tại ngũ (18 tháng+)</option>
                <option value="ĐT03">ĐT03d: Quân nhân, CA đã xuất ngũ, hoàn thành nghĩa vụ</option>
                <option value="ĐT04">ĐT04a: Thân nhân liệt sĩ</option>
                <option value="ĐT04">ĐT04b: Con thương, bệnh binh (suy giảm KNL 81%+)</option>
                <option value="ĐT04">ĐT04c: Con người nhiễm chất độc hóa học (suy giảm KNL 81%+)</option>
                <option value="ĐT04">ĐT04d: Con Anh hùng LLVT, Anh hùng Lao động thời kỳ kháng chiến</option>
                <option value="ĐT04">ĐT04đ: Con người hoạt động kháng chiến bị dị dạng do chất độc hóa học</option>
                <option value="ĐT05">ĐT05a: Thanh niên xung phong tập trung được cử đi học</option>
                <option value="ĐT05">ĐT05b: Quân nhân, CA tại ngũ (dưới 12 tháng ở KV1, 18 tháng ở KV khác)</option>
                <option value="ĐT05">ĐT05c: Chỉ huy trưởng, phó BCHQS xã, Dân quân tự vệ (12 tháng+)</option>
                <option value="ĐT06">ĐT06a: Người dân tộc thiểu số ở khu vực khác ngoài KV1</option>
                <option value="ĐT06">ĐT06b: Con thương, bệnh binh (suy giảm KNL dưới 81%)</option>
                <option value="ĐT06">ĐT06c: Con người nhiễm chất độc hóa học (suy giảm KNL dưới 81%)</option>
                <option value="ĐT07">ĐT07a: Người khuyết tật nặng có giấy xác nhận của cơ quan có thẩm quyền</option>
                <option value="ĐT07">ĐT07b: Người lao động ưu tú (thợ giỏi, nghệ nhân, bằng/huy hiệu LĐ sáng tạo)</option>
                <option value="ĐT07">ĐT07c: Giáo viên đã giảng dạy 3 năm+ (dự tuyển ngành đào tạo GV)</option>
                <option value="ĐT07">ĐT07d: Y tá, dược tá, hộ lý, kỹ thuật viên y tế 3 năm+ (tuyển ngành y tế)</option>
              </select>
              <!-- Chi tiết đối tượng ưu tiên -->
              <div v-if="form.priority_object !== '0'" class="mt-2 priority-detail py-2 px-3">
                <div v-if="form.priority_object === 'ĐT01'" class="small">
                  <strong>Đối tượng 01:</strong> Công dân Việt Nam là người dân tộc thiểu số có nơi thường trú trong thời gian học THPT hoặc trung cấp trên 18 tháng tại Khu [...]
                </div>
                <div v-else-if="form.priority_object === 'ĐT02'" class="small">
                  <strong>Đối tượng 02:</strong> Công nhân trực tiếp sản xuất đã làm việc liên tục 5 năm trở lên, trong đó có ít nhất 2 năm là chiến sĩ thi đua được cấp [...]
                </div>
                <div v-else-if="form.priority_object === 'ĐT03'" class="small">
                  <strong>Đối tượng 03:</strong> Thương binh, bệnh binh, người có 'Giấy chứng nhận người được hưởng chính sách như thương binh', Quân nhân tại ngũ với các điều kiện cụ thể [...]
                </div>
                <div v-else-if="form.priority_object === 'ĐT04'" class="small">
                  <strong>Đối tượng 04:</strong> Thân nhân liệt sĩ, con thương binh, bệnh binh suy giảm KNL từ 81% trở lên, con của người hoạt động kháng chiến bị nhiễm chất độc hóa học [...]
                </div>
                <div v-else-if="form.priority_object === 'ĐT05'" class="small">
                  <strong>Đối tượng 05:</strong> Thanh niên xung phong, quân nhân tại ngũ dưới 12 tháng ở KV1 hoặc 18 tháng ở khu vực khác, Chỉ huy trưởng quân sự xã [...]
                </div>
                <div v-else-if="form.priority_object === 'ĐT06'" class="small">
                  <strong>Đối tượng 06:</strong> Người dân tộc thiểu số ở khu vực khác ngoài KV1, con thương binh, bệnh binh suy giảm KNL dưới 81% [...]
                </div>
                <div v-else-if="form.priority_object === 'ĐT07'" class="small">
                  <strong>Đối tượng 07:</strong> Người khuyết tật nặng, người lao động ưu tú, giáo viên đã giảng dạy 3 năm trở lên, y tá, dược tá, hộ lý [...]
                </div>
              </div>
            </div>
            
            <div class="alert alert-danger mt-2 py-1 px-2 small" v-if="hasFormErrors && submitted" role="alert">
              <i class="bi bi-exclamation-circle me-1" aria-hidden="true"></i>
              Vui lòng điền đầy đủ thông tin và sửa các lỗi trước khi tính điểm.
            </div>

            <button type="submit" class="btn btn-calculate btn-sm w-100 mt-3">
              <i class="bi bi-calculator me-1"></i> Tính điểm
            </button>
          </form>
  
          <!-- Loading indicator -->
          <div v-if="loading" class="loading-indicator my-2 text-center">
            <div class="spinner-border spinner-border-sm text-primary" role="status">
              <span class="visually-hidden">Đang tải...</span>
            </div>
            <p class="small mb-0 mt-1">Đang tính toán...</p>
          </div>
          
          <!-- Hiển thị kết quả -->
          <section class="result-container mt-3" v-if="result" aria-labelledby="result-heading">
            <h3 id="result-heading" class="h5 text-center mb-2">Kết quả:</h3>
            <div class="point-summary my-2">
              <div class="row g-2">
                <div class="col-6 col-md-3">
                  <div class="point-card p-2">
                    <div class="point-title small">Điểm thành tích</div>
                    <div class="point-value">{{ result.achievement_points }}</div>
                  </div>
                </div>
                <div class="col-6 col-md-3">
                  <div class="point-card p-2">
                    <div class="point-title small">Điểm học tập</div>
                    <div class="point-value">{{ result.academic_score }}</div>
                  </div>
                </div>
                <div class="col-6 col-md-3">
                  <div class="point-card priority p-2">
                    <div class="point-title small">Điểm ưu tiên</div>
                    <div class="point-value">{{ result.converted_priority }}</div>
                    <div class="point-description small">(Đã quy đổi)</div>
                  </div>
                </div>
                <div class="col-6 col-md-3">
                  <div class="point-card total p-2">
                    <div class="point-title small">Tổng điểm</div>
                    <div class="point-value">{{ result.total_score }}</div>
                  </div>
                </div>
              </div>
            </div>
          </section>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import axios from 'axios'
import config from '@/config/apiConfig';
const BASE_API_URL = config?.BASE_API_URL;
// const BASE_API_URL = 'http://127.0.0.1:8000/api';

export default {
  name: 'PointCount',
  data() {
    return {
      cities: [],
      districts: [],
      schools: [],
      loading: false,
      form: {
        group: '',
        achievement: '',
        score10: null,
        score11: null,
        score12: null,
        city_id: '',
        district_id: '',
        school_id: null,
        priority_area: '',
        priority_object: '0'  // Mặc định là không có đối tượng ưu tiên
      },
      errors: {
        group: '',
        achievement: '',
        score10: '',
        score11: '',
        score12: '',
        city_id: '',
        district_id: '',
        school_id: ''
      },
      result: null,
      showAchievement: false,
      submitted: false
    }
  },
  computed: {
    selectedSchoolPriority() {
      if (this.schools.length && this.form.school_id) {
        const selected = this.schools.find(s => s.id == this.form.school_id)
        return selected ? selected.priority_area : ''
      }
      return ''
    },
    hasScoreErrors() {
      return this.errors.score10 || this.errors.score11 || this.errors.score12
    },
    hasFormErrors() {
      return Object.values(this.errors).some(error => error !== '')
    }
  },
  methods: {
    validateScore(field) {
      this.errors[field] = ''
      
      const score = this.form[field]
      
      if (score === null || score === '') {
        return
      }
      
      if (isNaN(score)) {
        this.errors[field] = 'Điểm phải là số'
        return
      }
      
      if (score < 0 || score > 10) {
        this.errors[field] = 'Điểm phải từ 0-10'
        return
      }
      
      if (score !== Math.floor(score * 10) / 10) {
        this.errors[field] = 'Chỉ cho phép 1 chữ số thập phân'
        return
      }
    },
    
    validateForm() {
      let isValid = true
      this.errors = {
        group: '',
        achievement: '',
        score10: '',
        score11: '',
        score12: '',
        city_id: '',
        district_id: '',
        school_id: ''
      }
      
      if (!this.form.group) {
        this.errors.group = 'Vui lòng chọn nhóm xét tuyển'
        isValid = false
      }
      
      if (this.showAchievement) {
        if (!this.form.achievement) {
          this.errors.achievement = 'Vui lòng chọn loại thành tích'
          isValid = false
        }
        
        ['score10', 'score11', 'score12'].forEach(field => {
          if (this.form[field] === null || this.form[field] === '') {
            this.errors[field] = 'Vui lòng nhập điểm'
            isValid = false
          } else {
            this.validateScore(field)
            if (this.errors[field]) {
              isValid = false
            }
          }
        })
      }
      
      if (!this.form.city_id) {
        this.errors.city_id = 'Vui lòng chọn tỉnh/thành phố'
        isValid = false
      }
      
      if (!this.form.district_id && this.districts.length > 0) {
        this.errors.district_id = 'Vui lòng chọn quận/huyện'
        isValid = false
      }
      
      if (!this.form.school_id && this.schools.length > 0) {
        this.errors.school_id = 'Vui lòng chọn trường THPT'
        isValid = false
      }
      
      return isValid
    },
    
    toggleSections() {
      this.showAchievement = this.form.group === '2' || this.form.group === '3'
      
      if (!this.showAchievement) {
        this.form.achievement = ''
        this.form.score10 = null
        this.form.score11 = null
        this.form.score12 = null
        this.errors.achievement = ''
        this.errors.score10 = ''
        this.errors.score11 = ''
        this.errors.score12 = ''
      }
    },
    
    loadCities() {
      axios.get(`${BASE_API_URL}/priorities/cities`)
        .then(res => {
          this.cities = res.data
        })
        .catch(err => {
          console.error('Lỗi khi tải danh sách tỉnh/thành phố:', err)
        })
    },
    
    loadDistricts() {
      this.form.district_id = ''
      this.form.school_id = null
      this.schools = []
      this.errors.district_id = ''
      this.errors.school_id = ''
      
      if (this.form.city_id) {
        axios.get(`${BASE_API_URL}/priorities/cities/${this.form.city_id}/districts`)
          .then(res => {
            this.districts = res.data
          })
          .catch(err => {
            console.error('Lỗi khi tải danh sách quận/huyện:', err)
          })
      } else {
        this.districts = []
      }
    },
    
    loadSchools() {
      this.form.school_id = null
      this.errors.school_id = ''
      
      if (this.form.district_id) {
        axios.get(`${BASE_API_URL}/priorities/districts/${this.form.district_id}/schools`)
          .then(res => {
            this.schools = res.data
          })
          .catch(err => {
            console.error('Lỗi khi tải danh sách trường:', err)
          })
      } else {
        this.schools = []
      }
    },
    
    async calculatePoint() {
      this.submitted = true
      
      if (!this.validateForm()) {
        this.$nextTick(() => {
          const firstError = document.querySelector('.is-invalid')
          if (firstError) {
            firstError.scrollIntoView({ behavior: 'smooth', block: 'center' })
          }
        })
        return
      }
      
      const selectedSchool = this.schools.find(s => s.id == this.form.school_id)
      if (selectedSchool) {
        this.form.priority_area = selectedSchool.priority_area || ''
      }
      
      this.loading = true
      
      try {
        const response = await axios.post(`${BASE_API_URL}/university-admissions/point-count`, {
          group: this.form.group,
          achievement: this.form.achievement || null,
          score10: this.form.score10,
          score11: this.form.score11,
          score12: this.form.score12,
          school_id: this.form.school_id ? parseInt(this.form.school_id) : null,
          priority_area: this.form.priority_area,
          priority_object: this.form.priority_object || '0'
        })
        
        this.result = response.data
        
        this.$nextTick(() => {
          const resultElement = document.querySelector('.result-container')
          if (resultElement) {
            resultElement.scrollIntoView({ behavior: 'smooth', block: 'start' })
          }
        })
      } catch (error) {
        console.error('Lỗi khi tính điểm:', error)
        alert('Đã xảy ra lỗi khi tính điểm. Vui lòng thử lại sau.')
      } finally {
        this.loading = false
      }
    }
  },
  mounted() {
    this.loadCities()
  }
}
</script>

<style scoped>
/* Hero Section - Simplified like CalculateScoreTHPT */
.hero-section {
  background: linear-gradient(135deg, rgba(14, 76, 146, 0.95), rgba(31, 64, 104, 0.95));
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.15);
}

.hero-section h1 {
  font-size: 1.5rem;
  color: #fff;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
}

.hero-section p {
  color: rgba(255, 255, 255, 0.9);
  font-size: 0.9rem;
}

/* Card Headers */
.card-header {
  background-color: #0e4c92 !important;
  padding: 0.75rem;
}

/* Section titles */
.section-title {
  color: #0e4c92;
  font-weight: 600;
  text-align: center;
  margin-bottom: 0.5rem;
  position: relative;
}

.section-title:after {
  content: "";
  display: block;
  width: 40px;
  height: 2px;
  background: #3a7bd5;
  margin: 0.3rem auto 0;
}

/* School selection container */
.school-selection-container {
  background-color: rgba(208, 225, 249, 0.3);
  border-radius: 0.5rem;
  border: 1px solid #d0e1f9;
}

/* Form controls */
.form-label {
  font-weight: 500;
  color: #4a5568;
  margin-bottom: 0.25rem;
}

.form-select, .form-control {
  font-size: 0.875rem;
}

.form-control {
  border-color: #dce0e5;
}

.input-group-text {
  background-color: #f0f2f5;
  border-color: #dce0e5;
  color: #4a5568;
  font-size: 0.875rem;
}

/* Priority details */
.priority-detail {
  background-color: #f8f9fa;
  border-radius: 0.25rem;
  border: 1px solid #e9ecef;
  color: #495057;
  font-size: 0.8rem;
  line-height: 1.4;
}

/* Calculate Button */
.btn-calculate {
  background: linear-gradient(135deg, #3a7bd5, #0e4c92);
  color: #ffffff;
  font-weight: 600;
  box-shadow: 0 3px 5px rgba(14, 76, 146, 0.2);
  border: none;
  transition: all 0.3s;
}

.btn-calculate:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(14, 76, 146, 0.3);
  background: linear-gradient(135deg, #3a7bd5, #083878);
}

/* Results styling */
.point-card {
  background-color: #f8f9fa;
  border-radius: 0.5rem;
  border: 1px solid #e9ecef;
  text-align: center;
  height: 100%;
}

.point-title {
  color: #4a5568;
  font-weight: 500;
  margin-bottom: 0.25rem;
}

.point-value {
  font-size: 1.25rem;
  font-weight: 700;
  color: #0e4c92;
}

.point-description {
  color: #6c757d;
  font-size: 0.75rem;
}

.point-card.priority {
  background-color: #ebf5ff;
  border-color: #bfdeff;
}

.point-card.total {
  background-color: #e6f4ff;
  border-color: #91caff;
}

.point-card.total .point-value {
  color: #1677ff;
  font-size: 1.5rem;
}

/* Loading indicator */
.loading-indicator {
  text-align: center;
  color: #0e4c92;
  padding: 1rem;
}

/* Responsive tweaks */
@media (max-width: 767px) {
  .card-body {
    padding: 0.75rem;
  }
  
  .point-value {
    font-size: 1.1rem;
  }
  
  .point-card.total .point-value {
    font-size: 1.3rem;
  }
}
</style>
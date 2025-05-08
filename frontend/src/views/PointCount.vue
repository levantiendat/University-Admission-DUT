<template>
  <div>
    <!-- Hero Section: Semantically improved with proper article structure -->
    <header class="hero-section py-4 py-md-5 text-center text-white" aria-labelledby="page-title">
      <div class="container">
        <h1 id="page-title" class="display-4 fw-bold">Tính Điểm Xét Tuyển</h1>
        <p class="lead">Trường Đại học Bách Khoa - Đại học Đà Nẵng</p>
      </div>
    </header>

    <!-- Main Content: Improved accessibility and mobile responsiveness -->
    <main class="container my-4 my-md-5">
      <article class="card shadow rounded">
        <header class="card-header text-white text-center">
          <h2 class="h5 mb-0">Tính điểm xét tuyển riêng - Trường ĐHBK - ĐHĐN</h2>
        </header>
        <div class="card-body px-3 px-md-5 py-4">
          <form @submit.prevent="calculatePoint" id="pointForm">
            <!-- Bước 1: Chọn nhóm xét tuyển -->
            <div class="mb-3">
              <label for="group" class="form-label">Chọn nhóm xét tuyển</label>
              <select 
                v-model="form.group" 
                class="form-select selectpicker" 
                id="group" 
                @change="toggleSections" 
                data-live-search="true" 
                data-width="100%"
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
              <label for="achievement" class="form-label">Chọn loại thành tích</label>
              <select 
                v-model="form.achievement" 
                class="form-select selectpicker" 
                id="achievement" 
                data-live-search="true" 
                data-width="100%"
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
              <fieldset>
                <legend class="form-label">Điểm tổng kết</legend>
                <div class="row g-2">
                  <div class="col-12 col-sm-4">
                    <label for="score10" class="visually-hidden">Điểm lớp 10</label>
                    <input 
                      type="number" 
                      step="0.1" 
                      min="0" 
                      max="10" 
                      class="form-control" 
                      id="score10"
                      v-model.number="form.score10" 
                      placeholder="Lớp 10"
                      @input="validateScore('score10')"
                      :class="{'is-invalid': errors.score10}"
                      aria-describedby="score10-feedback">
                    <div id="score10-feedback" class="invalid-feedback" v-if="errors.score10">
                      {{ errors.score10 }}
                    </div>
                  </div>
                  <div class="col-12 col-sm-4">
                    <label for="score11" class="visually-hidden">Điểm lớp 11</label>
                    <input 
                      type="number" 
                      step="0.1" 
                      min="0" 
                      max="10" 
                      class="form-control" 
                      id="score11"
                      v-model.number="form.score11" 
                      placeholder="Lớp 11"
                      @input="validateScore('score11')"
                      :class="{'is-invalid': errors.score11}"
                      aria-describedby="score11-feedback">
                    <div id="score11-feedback" class="invalid-feedback" v-if="errors.score11">
                      {{ errors.score11 }}
                    </div>
                  </div>
                  <div class="col-12 col-sm-4">
                    <label for="score12" class="visually-hidden">Điểm lớp 12</label>
                    <input 
                      type="number" 
                      step="0.1" 
                      min="0" 
                      max="10" 
                      class="form-control"
                      id="score12" 
                      v-model.number="form.score12" 
                      placeholder="Lớp 12"
                      @input="validateScore('score12')"
                      :class="{'is-invalid': errors.score12}"
                      aria-describedby="score12-feedback">
                    <div id="score12-feedback" class="invalid-feedback" v-if="errors.score12">
                      {{ errors.score12 }}
                    </div>
                  </div>
                </div>
                <!-- Thông báo lỗi chung cho điểm số -->
                <div class="alert alert-warning mt-2" v-if="hasScoreErrors" role="alert">
                  <i class="fas fa-exclamation-triangle me-2" aria-hidden="true"></i>
                  Vui lòng kiểm tra lại điểm số. Điểm phải nằm trong khoảng từ 0 đến 10 và có tối đa 1 chữ số thập phân.
                </div>
              </fieldset>
            </div>

            <!-- Bước 4: Chọn trường (xác định khu vực ưu tiên) -->
            <h3 class="section-title h5 mt-4">Chọn trường</h3>
            <div class="school-selection-container">
              <div class="form-group">
                <label for="city" class="form-label">Chọn Tỉnh/Thành phố</label>
                <select 
                  v-model="form.city_id" 
                  class="form-select selectpicker" 
                  id="city" 
                  @change="loadDistricts" 
                  data-live-search="true" 
                  data-width="100%"
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
              <div class="form-group">
                <label for="district" class="form-label">Chọn Quận/Huyện</label>
                <select 
                  v-model="form.district_id" 
                  class="form-select selectpicker" 
                  id="district" 
                  @change="loadSchools" 
                  :disabled="!districts.length" 
                  data-live-search="true" 
                  data-width="100%"
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
              <div class="form-group">
                <label for="school" class="form-label">Chọn Trường THPT</label>
                <select 
                  v-model="form.school_id" 
                  class="form-select selectpicker" 
                  id="school" 
                  :disabled="!schools.length" 
                  data-live-search="true" 
                  data-width="100%"
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
            <div class="mt-3 text-center" v-if="selectedSchoolPriority">
              <p class="fw-bold">Khu vực ưu tiên: {{ selectedSchoolPriority }}</p>
            </div>

            <!-- Bước 5: Chọn đối tượng ưu tiên -->
            <div class="mb-3 mt-4">
              <label for="priority_object" class="form-label">Chọn Ưu tiên đối tượng</label>
              <select 
                v-model="form.priority_object" 
                class="form-select selectpicker" 
                id="priority_object" 
                data-live-search="true" 
                data-width="100%">
                <option value="0" data-content="Không có đối tượng ưu tiên">Không có đối tượng ưu tiên</option>
                  <option value="ĐT01" data-content="Đối tượng 01:<br>Công dân Việt Nam là người dân tộc thiểu số có nơi thường trú<br>trong thời gian học THPT hoặc trung cấp trên 18 tháng tại Khu vực 1.">
                    Đối tượng 01
                  </option>
                  <option value="ĐT02" data-content="Đối tượng 02:<br>Công nhân trực tiếp sản xuất đã làm việc liên tục 5 năm trở lên,<br>trong đó có ít nhất 2 năm là chiến sĩ thi đua được cấp tỉnh trở lên<br>công nhận và cấp bằng khen.">
                    Đối tượng 02
                  </option>
                  <option value="ĐT03" data-content="Đối tượng 03a:<br>Thương binh, bệnh binh, người có 'Giấy chứng nhận người được hưởng chính sách như thương binh'.">
                    Đối tượng 03a
                  </option>
                  <option value="ĐT03" data-content="Đối tượng 03b:<br>Quân nhân; sĩ quan, hạ sĩ quan, chiến sĩ nghĩa vụ trong Công an nhân dân tại ngũ<br>được cử đi học có thời gian phục vụ từ 12 tháng trở lên tại Khu vực 1.">
                    Đối tượng 03b
                  </option>
                  <option value="ĐT03" data-content="Đối tượng 03c:<br>Quân nhân; sĩ quan, hạ sĩ quan, chiến sĩ nghĩa vụ trong Công an nhân dân tại ngũ<br>được cử đi học có thời gian phục vụ từ 18 tháng trở lên.">
                    Đối tượng 03c
                  </option>
                  <option value="ĐT03" data-content="Đối tượng 03d:<br>Quân nhân; sĩ quan, hạ sĩ quan, chiến sĩ nghĩa vụ trong Công an nhân dân đã xuất ngũ,<br>được công nhận hoàn thành nghĩa vụ phục vụ tại ngũ theo quy định.">
                    Đối tượng 03d
                  </option>
                  <option value="ĐT04" data-content="Đối tượng 04a:<br>Thân nhân liệt sĩ.">
                    Đối tượng 04a
                  </option>
                  <option value="ĐT04" data-content="Đối tượng 04b:<br>Con thương binh, con bệnh binh, con của người được hưởng chính sách như thương binh<br>bị suy giảm khả năng lao động từ 81% trở lên.">
                    Đối tượng 04b
                  </option>
                  <option value="ĐT04" data-content="Đối tượng 04c:<br>Con của người hoạt động kháng chiến bị nhiễm chất độc hóa học<br>bị suy giảm khả năng lao động 81% trở lên.">
                    Đối tượng 04c
                  </option>
                  <option value="ĐT04" data-content="Đối tượng 04d:<br>Con của Anh hùng Lực lượng vũ trang nhân dân; con của Anh hùng Lao động trong thời kỳ kháng chiến.">
                    Đối tượng 04d
                  </option>
                  <option value="ĐT04" data-content="Đối tượng 04đ:<br>Con của người hoạt động kháng chiến bị dị dạng, dị tật do hậu quả của chất độc hóa học<br>đang hưởng trợ cấp hàng tháng.">
                    Đối tượng 04đ
                  </option>
                  <option value="ĐT05" data-content="Đối tượng 05a:<br>Thanh niên xung phong tập trung được cử đi học.">
                    Đối tượng 05a
                  </option>
                  <option value="ĐT05" data-content="Đối tượng 05b:<br>Quân nhân; sĩ quan, hạ sĩ quan, chiến sĩ nghĩa vụ trong Công an nhân dân tại ngũ<br>được cử đi học có thời gian phục vụ dưới 12 tháng ở Khu vực 1 và dưới 18 tháng ở khu vực khác.">
                    Đối tượng 05b
                  </option>
                  <option value="ĐT05" data-content="Đối tượng 05c:<br>Chỉ huy trưởng, Chỉ huy phó ban chỉ huy quân sự xã, phường, thị trấn;<br>Thôn đội trưởng, Trung đội trưởng Dân quân tự vệ nòng cốt, Dân quân tự vệ đã hoàn thành nghĩa vụ tham gia Dân quân tự vệ nòng cốt từ 12 tháng trở lên, dự thi vào ngành Quân sự cơ sở.<br>Thời hạn tối đa được hưởng ưu tiên là 18 tháng kể từ ngày ký quyết định xuất ngũ đến ngày ĐKXT.">
                    Đối tượng 05c
                  </option>
                  <option value="ĐT06" data-content="Đối tượng 06a:<br>Công dân Việt Nam là người dân tộc thiểu số có nơi thường trú ở ngoài khu vực đã quy định<br>thuộc đối tượng 01.">
                    Đối tượng 06a
                  </option>
                  <option value="ĐT06" data-content="Đối tượng 06b:<br>Con thương binh, con bệnh binh, con của người được hưởng chính sách như thương binh<br>bị suy giảm khả năng lao động dưới 81%.">
                    Đối tượng 06b
                  </option>
                  <option value="ĐT06" data-content="Đối tượng 06c:<br>Con của người hoạt động kháng chiến bị nhiễm chất độc hóa học<br>có tỷ lệ suy giảm khả năng lao động dưới 81%.">
                    Đối tượng 06c
                  </option>
                  <option value="ĐT07" data-content="Đối tượng 07a:<br>Người khuyết tật nặng có giấy xác nhận khuyết tật của cơ quan có thẩm quyền cấp theo quy định<br>tại Thông tư liên tịch số 37/2012/TTLT‑BLĐTBXH‑BYT‑BTC‑BGDĐT ngày 28 tháng 12 năm 2012.">
                    Đối tượng 07a
                  </option>
                  <option value="ĐT07" data-content="Đối tượng 07b:<br>Người lao động ưu tú thuộc tất cả thành phần kinh tế từ cấp tỉnh, cấp bộ trở lên được công nhận danh hiệu thợ giỏi, nghệ nhân,<br>được cấp bằng hoặc huy hiệu Lao động sáng tạo.">
                    Đối tượng 07b
                  </option>
                  <option value="ĐT07" data-content="Đối tượng 07c:<br>Giáo viên đã giảng dạy đủ 3 năm trở lên dự tuyển vào các ngành đào tạo giáo viên.">
                    Đối tượng 07c
                  </option>
                  <option value="ĐT07" data-content="Đối tượng 07d:<br>Y tá, dược tá, hộ lý, y sĩ, điều dưỡng viên, hộ sinh viên, kỹ thuật viên, người có bằng trung cấp Dược<br>đã công tác đủ 3 năm trở lên dự tuyển vào đúng ngành tốt nghiệp thuộc lĩnh vực sức khỏe.">
                    Đối tượng 07d
                  </option>
              </select>
            </div>
            <div class="alert alert-danger mt-3" v-if="hasFormErrors && submitted" role="alert">
              <i class="fas fa-exclamation-circle me-2" aria-hidden="true"></i>
              Vui lòng điền đầy đủ thông tin và sửa các lỗi trước khi tính điểm.
            </div>

            <button type="submit" class="btn btn-primary w-100 mt-4">Tính điểm</button>
          </form>
  
          <!-- Hiển thị kết quả -->
          <section class="result-container mt-4" v-if="result" aria-labelledby="result-heading">
            <h3 id="result-heading" class="text-center">Kết quả:</h3>
            <ul class="list-group">
              <li class="list-group-item d-flex flex-column flex-md-row justify-content-between align-items-md-center">
                <span>🎖 Điểm thành tích:</span>
                <strong>{{ result.achievement_points }}</strong>
              </li>
              <li class="list-group-item d-flex flex-column flex-md-row justify-content-between align-items-md-center">
                <span>📚 Điểm học tập:</span>
                <strong>{{ result.academic_score }}</strong>
              </li>
              <li class="list-group-item d-flex flex-column flex-md-row justify-content-between align-items-md-center">
                <span>⭐ Điểm ưu tiên sau quy đổi:</span>
                <strong>{{ result.converted_priority }}</strong>
              </li>
              <li class="list-group-item d-flex flex-column flex-md-row justify-content-between align-items-md-center">
                <span>🏆 Tổng điểm xét tuyển:</span>
                <strong class="fs-5 text-primary">{{ result.total_score }}</strong>
              </li>
            </ul>
          </section>
        </div>
      </article>
    </main>
  </div>
</template>

<script>
// Script section remains the same as original
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
      
      this.$nextTick(() => {
        $('.selectpicker').selectpicker('refresh')
      })
    },
    
    loadCities() {
      axios.get(`${BASE_API_URL}/priorities/cities`)
        .then(res => {
          this.cities = res.data
          this.$nextTick(() => {
            $('.selectpicker').selectpicker('refresh')
          })
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
            this.$nextTick(() => {
              $('.selectpicker').selectpicker('refresh')
            })
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
            this.$nextTick(() => {
              $('.selectpicker').selectpicker('refresh')
            })
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
      }
    }
  },
  mounted() {
    this.loadCities()
    this.$nextTick(() => {
      $('.selectpicker').selectpicker()
    })
  }
}
</script>

<style scoped>
/* Base variables */
:root {
  --primary-color: #0e4c92;
  --primary-dark: #083878;
  --secondary-color: #3a7bd5;
  --accent-color: #d0e1f9;
  --light-bg: #f0f2f5;
  --dark-gray: #4a5568;
  --white: #ffffff;
  --text-color: #333333;
  --success-color: #28a745;
  --danger-color: #dc3545;
  --warning-color: #ffc107;
  --border-radius: 12px;
}

/* Reset and Base Styles */
* {
  box-sizing: border-box;
}

body {
  background-color: var(--light-bg);
  color: var(--text-color);
  font-family: 'Roboto', Arial, sans-serif;
  line-height: 1.6;
}

/* Hero Section */
.hero-section {
  background: linear-gradient(135deg, rgba(14, 76, 146, 0.95), rgba(31, 64, 104, 0.95));
  background-size: cover;
  background-position: center;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
  border-bottom: 5px solid var(--secondary-color);
}

.hero-section h1 {
  color: var(--white);
  font-weight: 800;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.4);
  margin-bottom: 0.5rem;
  letter-spacing: 1px;
  font-size: calc(1.5rem + 1vw); /* Responsive font size */
}

.hero-section p.lead {
  color: var(--white);
  font-size: calc(1rem + 0.25vw);
  max-width: 800px;
  margin: 0 auto;
  opacity: 0.9;
}

/* Card Structure */
.card {
  background-color: var(--white);
  border: none;
  border-radius: var(--border-radius);
  overflow: hidden;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
  margin: 1rem 0;
}

.card-header {
  background-color: var(--primary-color) !important;
  color: var(--white) !important;
  padding: 1rem 1.25rem;
  border: none;
  text-transform: uppercase;
  letter-spacing: 1px;
  text-align: center;
  font-weight: 600;
  font-size: calc(1rem + 0.25vw);
}

.card-body {
  padding: 1.5rem;
}

@media (min-width: 768px) {
  .card-body {
    padding: 2.5rem;
  }
}

/* Section Titles */
.section-title {
  color: var(--primary-color);
  text-align: center;
  margin: 1.5rem 0;
  font-weight: 700;
  position: relative;
}

.section-title:after {
  content: "";
  display: block;
  width: 60px;
  height: 3px;
  background: var(--secondary-color);
  margin: 0.5rem auto 0;
  border-radius: 2px;
}

/* Form Elements */
.form-label {
  font-weight: 600;
  color: var(--primary-color);
  margin-bottom: 0.5rem;
  display: block;
}

.form-select, 
.form-control {
  width: 100%;
  padding: 0.75rem 1rem;
  font-size: 1rem;
  height: auto;
  border-radius: 0.5rem;
  border: 2px solid #dce0e5;
  background-color: var(--white);
  transition: all 0.3s ease;
  margin-bottom: 1rem;
}

@media (min-width: 768px) {
  .form-select, 
  .form-control {
    padding: 1rem 1.25rem;
    font-size: 1.1rem;
  }
}

/* Invalid Feedback */
.is-invalid {
  border-color: var(--danger-color) !important;
}

.invalid-feedback {
  display: none;
  width: 100%;
  margin-top: -0.75rem;
  margin-bottom: 0.5rem;
  font-size: 0.875rem;
  color: var(--danger-color);
}

.is-invalid ~ .invalid-feedback {
  display: block;
}

/* School Selection Container */
.school-selection-container {
  background-color: var(--accent-color);
  border-radius: var(--border-radius);
  padding: 1.5rem;
  margin: 1.5rem 0;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
  border: 2px solid var(--primary-color);
}

@media (min-width: 768px) {
  .school-selection-container {
    padding: 2rem;
  }
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group:last-child {
  margin-bottom: 0;
}

/* Submit Button */
.btn-primary {
  background: linear-gradient(135deg, var(--secondary-color), var(--primary-color));
  color: var(--white);
  font-weight: 700;
  font-size: 1.1rem;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 0.5rem;
  transition: all 0.3s;
  text-transform: uppercase;
  letter-spacing: 1px;
  box-shadow: 0 6px 20px rgba(14, 76, 146, 0.3);
}

@media (min-width: 768px) {
  .btn-primary {
    padding: 1rem 2rem;
    font-size: 1.2rem;
  }
}

.btn-primary:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(14, 76, 146, 0.4);
  background: linear-gradient(135deg, var(--secondary-color), var(--primary-dark));
}

/* Results Container */
.result-container {
  background: linear-gradient(145deg, var(--white), var(--accent-color));
  border-radius: var(--border-radius);
  padding: 1.5rem !important;
  margin: 1.5rem auto;
  box-shadow: 0 8px 25px rgba(14, 76, 146, 0.15);
  border-left: 5px solid var(--primary-color);
}

@media (min-width: 768px) {
  .result-container {
    padding: 2rem !important;
  }
}

.result-container h3 {
  color: var(--primary-color);
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 1.5rem;
  text-transform: uppercase;
}

/* List Results */
.list-group-item {
  background-color: var(--white);
  border-radius: 10px !important;
  padding: 1rem;
  font-size: 1rem;
  border-left: 5px solid var(--secondary-color) !important;
  margin-bottom: 0.75rem;
  transition: transform 0.3s;
}

@media (min-width: 768px) {
  .list-group-item {
    padding: 1.25rem;
    font-size: 1.1rem;
  }
}

.list-group-item strong {
  color: var(--primary-color);
  font-weight: 700;
  display: block;
  margin-top: 0.5rem;
}

@media (min-width: 768px) {
  .list-group-item strong {
    margin-top: 0;
  }
}

.list-group-item:last-child {
  background-color: #eef6ff;
  border-left: 5px solid var(--primary-color) !important;
  margin-top: 0.5rem;
}

/* Alerts */
.alert {
  position: relative;
  padding: 0.75rem 1.25rem;
  margin-bottom: 1rem;
  border: 1px solid transparent;
  border-radius: 0.5rem;
}

.alert-warning {
  color: #856404;
  background-color: #fff3cd;
  border-color: #ffeeba;
}

.alert-danger {
  color: #721c24;
  background-color: #f8d7da;
  border-color: #f5c6cb;
}
</style>
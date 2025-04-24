<template>
  <div>
    <!-- Hero Section -->
    <header class="hero-section py-5 text-center text-white">
      <div class="container">
        <h1 class="display-4 fw-bold">Tính Điểm Xét Tuyển</h1>
        <p class="lead">Trường Đại học Bách Khoa - Đại học Đà Nẵng</p>
      </div>
    </header>

    <!-- Main Content -->
    <div class="container my-5">
      <div class="card shadow rounded">
        <div class="card-header text-white text-center">
          Tính điểm xét tuyển riêng - Trường ĐHBK - ĐHĐN
        </div>
        <div class="card-body">
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
                :class="{'is-invalid': errors.group && submitted}">
                <option value="">-- Chọn nhóm --</option>
                <option value="1">Nhóm 1: Giải Khuyến khích Học sinh giỏi / Cuộc thi khoa học kỹ thuật cấp Quốc Gia</option>
                <option value="2">Nhóm 2: Học sinh giỏi cấp tỉnh, thành phố trực thuộc trung ương</option>
                <option value="3">Nhóm 3: Cuộc thi khoa học kỹ thuật cấp tỉnh, thành phố trực thuộc trung ương</option>
              </select>
              <div class="invalid-feedback" v-if="errors.group && submitted">
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
                :class="{'is-invalid': errors.achievement && submitted}">
                <option value="">-- Chọn loại giải --</option>
                <option value="I">Giải Nhất</option>
                <option value="II">Giải Nhì</option>
                <option value="III">Giải Ba</option>
                <option value="Khuyến khích">Giải Khuyến khích</option>
              </select>
              <div class="invalid-feedback" v-if="errors.achievement && submitted">
                {{ errors.achievement }}
              </div>
            </div>

            <!-- Bước 3: Nhập điểm học bạ (nếu có) -->
            <div class="mb-3" v-if="showAchievement">
              <label class="form-label">Điểm tổng kết</label>
              <div class="row g-2">
                <div class="col-md-4">
                  <input 
                    type="number" 
                    step="0.1" 
                    min="0" 
                    max="10" 
                    class="form-control" 
                    v-model.number="form.score10" 
                    placeholder="Lớp 10"
                    @input="validateScore('score10')"
                    :class="{'is-invalid': errors.score10}">
                  <div class="invalid-feedback" v-if="errors.score10">
                    {{ errors.score10 }}
                  </div>
                </div>
                <div class="col-md-4">
                  <input 
                    type="number" 
                    step="0.1" 
                    min="0" 
                    max="10" 
                    class="form-control" 
                    v-model.number="form.score11" 
                    placeholder="Lớp 11"
                    @input="validateScore('score11')"
                    :class="{'is-invalid': errors.score11}">
                  <div class="invalid-feedback" v-if="errors.score11">
                    {{ errors.score11 }}
                  </div>
                </div>
                <div class="col-md-4">
                  <input 
                    type="number" 
                    step="0.1" 
                    min="0" 
                    max="10" 
                    class="form-control" 
                    v-model.number="form.score12" 
                    placeholder="Lớp 12"
                    @input="validateScore('score12')"
                    :class="{'is-invalid': errors.score12}">
                  <div class="invalid-feedback" v-if="errors.score12">
                    {{ errors.score12 }}
                  </div>
                </div>
              </div>
              <!-- Thông báo lỗi chung cho điểm số -->
              <div class="alert alert-warning mt-2" v-if="hasScoreErrors">
                <i class="fas fa-exclamation-triangle me-2"></i>
                Vui lòng kiểm tra lại điểm số. Điểm phải nằm trong khoảng từ 0 đến 10 và có tối đa 1 chữ số thập phân.
              </div>
            </div>

            <!-- Bước 4: Chọn trường (xác định khu vực ưu tiên) -->
            <h5 class="section-title mt-4">Chọn trường</h5>
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
                  :class="{'is-invalid': errors.city_id && submitted}">
                  <option value="">-- Chọn Tỉnh/Thành phố --</option>
                  <option v-for="city in cities" :key="city.id" :value="city.id">
                    {{ city.name }}
                  </option>
                </select>
                <div class="invalid-feedback" v-if="errors.city_id && submitted">
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
                  :class="{'is-invalid': errors.district_id && submitted}">
                  <option value="">-- Chọn Quận/Huyện --</option>
                  <option v-for="district in districts" :key="district.id" :value="district.id">
                    {{ district.name }}
                  </option>
                </select>
                <div class="invalid-feedback" v-if="errors.district_id && submitted">
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
                  :class="{'is-invalid': errors.school_id && submitted}">
                  <option value="">-- Chọn Trường THPT --</option>
                  <option v-for="school in schools" :key="school.id" :value="school.id" :data-priority="school.priority_area">
                    {{ school.name }}
                  </option>
                </select>
                <div class="invalid-feedback" v-if="errors.school_id && submitted">
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
                  <!-- ... Các option khác ... -->
                </select>
              </div>
              <div class="alert alert-danger mt-3" v-if="hasFormErrors && submitted">
              <i class="fas fa-exclamation-circle me-2"></i>
              Vui lòng điền đầy đủ thông tin và sửa các lỗi trước khi tính điểm.
            </div>

            <button type="submit" class="btn btn-primary w-100">Tính điểm</button>
            </form>
  
            <!-- Hiển thị kết quả -->
            <div class="result-container mt-4" v-if="result">
            <h3 class="text-center">Kết quả:</h3>
            <ul class="list-group">
              <li class="list-group-item">🎖 Điểm thành tích: <strong>{{ result.achievement_points }}</strong></li>
              <li class="list-group-item">📚 Điểm học tập: <strong>{{ result.academic_score }}</strong></li>
              <li class="list-group-item">⭐ Điểm ưu tiên sau quy đổi: <strong>{{ result.converted_priority }}</strong></li>
              <li class="list-group-item">🏆 Tổng điểm xét tuyển: <strong>{{ result.total_score }}</strong></li>
            </ul>
          </div>
          </div>
        </div>
      </div>
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
    // Hàm kiểm tra định dạng điểm số
    validateScore(field) {
      // Reset lỗi
      this.errors[field] = ''
      
      // Lấy giá trị điểm
      const score = this.form[field]
      
      // Bỏ qua nếu field trống
      if (score === null || score === '') {
        return
      }
      
      // Kiểm tra điểm là số hợp lệ
      if (isNaN(score)) {
        this.errors[field] = 'Điểm phải là số'
        return
      }
      
      // Kiểm tra phạm vi điểm
      if (score < 0 || score > 10) {
        this.errors[field] = 'Điểm phải từ 0-10'
        return
      }
      
      // Kiểm tra định dạng thập phân
      // Chỉ cho phép 1 chữ số thập phân (0.1, 8.5, vv..)
      if (score !== Math.floor(score * 10) / 10) {
        this.errors[field] = 'Chỉ cho phép 1 chữ số thập phân'
        return
      }
    },
    
    // Kiểm tra form hợp lệ trước khi tính điểm
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
      
      // Kiểm tra nhóm xét tuyển (bắt buộc)
      if (!this.form.group) {
        this.errors.group = 'Vui lòng chọn nhóm xét tuyển'
        isValid = false
      }
      
      // Kiểm tra thành tích và điểm (nếu nhóm 2 hoặc 3)
      if (this.showAchievement) {
        if (!this.form.achievement) {
          this.errors.achievement = 'Vui lòng chọn loại thành tích'
          isValid = false
        }
        
        // Kiểm tra các trường điểm
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
      
      // Kiểm tra trường học (bắt buộc)
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
      
      // Reset các trường liên quan khi chuyển nhóm
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
      
      // Validate form trước khi gửi
      if (!this.validateForm()) {
        // Cuộn đến thông báo lỗi đầu tiên
        this.$nextTick(() => {
          const firstError = document.querySelector('.is-invalid')
          if (firstError) {
            firstError.scrollIntoView({ behavior: 'smooth', block: 'center' })
          }
        })
        return
      }
      
      // Cập nhật priority_area từ trường đã chọn
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
        
        // Cuộn xuống kết quả
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
/* Thiết lập biến CSS cho màu sắc chính */
:root {
  --primary-color: #0e4c92;        /* Xanh dương đậm */
  --primary-dark: #083878;         /* Xanh dương đậm hơn cho hover */
  --secondary-color: #3a7bd5;      /* Xanh dương sáng hơn */
  --accent-color: #d0e1f9;         /* Xanh dương nhạt */
  --light-bg: #f0f2f5;             /* Xám nhạt */
  --dark-gray: #4a5568;            /* Xám đậm */
  --white: #ffffff;                /* Trắng */
  --text-color: #333333;           /* Màu chữ chính */
  --success-color: #28a745;        /* Màu thành công */
  --danger-color: #dc3545;         /* Màu cảnh báo */
  --warning-color: #ffc107;        /* Màu cảnh báo vàng */
  --border-radius: 12px;           /* Bo góc nhất quán */
}

/* Reset cho toàn bộ trang */
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  background-color: var(--light-bg);
  color: var(--text-color);
  font-family: 'Roboto', Arial, sans-serif;
  line-height: 1.6;
}

/* Hero Section - banner chính */
.hero-section {
  background: linear-gradient(135deg, rgba(14, 76, 146, 0.95), rgba(31, 64, 104, 0.95)), 
              url('https://images.unsplash.com/photo-1523050854058-8df90110c9f1?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80');
  background-size: cover;
  background-position: center;
  padding: 3.5rem 0;
  text-align: center;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
  border-bottom: 5px solid var(--secondary-color);
}

.hero-section h1 {
  color: var(--white);
  font-size: 2.5rem;
  font-weight: 800;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.4);
  margin-bottom: 0.5rem;
  letter-spacing: 1px;
}

.hero-section p.lead {
  color: var(--white);
  font-size: 1.25rem;
  max-width: 800px;
  margin: 0 auto;
  opacity: 0.9;
}

/* Container chính */
.container {
  width: 100%;
  max-width: 1140px;
  margin: 0 auto;
  padding: 0 15px;
}

/* Card chính */
.card {
  background-color: var(--white);
  border: none;
  border-radius: var(--border-radius);
  overflow: hidden;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
  margin: 2rem 0;
}

.card-header {
  background-color: var(--primary-color) !important;
  color: var(--white) !important;
  font-size: 1.3rem;
  font-weight: 600;
  padding: 1.25rem;
  border: none;
  text-transform: uppercase;
  letter-spacing: 1px;
  text-align: center;
}

.card-body {
  padding: 2.5rem;
}

/* Heading trong card */
.section-title {
  color: var(--primary-color);
  font-size: 1.4rem;
  text-align: center;
  margin: 2rem 0 1.5rem;
  font-weight: 700;
  position: relative;
}

.section-title:after {
  content: "";
  display: block;
  width: 80px;
  height: 4px;
  background: var(--secondary-color);
  margin: 0.7rem auto 0;
  border-radius: 2px;
}

/* Form elements - nhất quán và không có thụt lề */
form {
  width: 100%;
  max-width: 100%;
  margin: 0 auto;
}

.form-label {
  font-weight: 600;
  color: var(--primary-color);
  font-size: 1.1rem;
  margin-bottom: 0.7rem;
  display: block;
}

/* Mở rộng kích thước cho nhóm xét tuyển */
.mb-3:first-child .form-select {
  min-height: 60px;
  font-size: 1.1rem;
  padding: 1.2rem 1.5rem;
  border: 2px solid var(--primary-color);
  font-weight: 500;
}

/* Form Select - Mở rộng kích thước */
.form-select, 
.form-control {
  width: 100%;
  padding: 1.2rem 1.5rem;
  font-size: 1.1rem;
  height: auto;
  min-height: 55px;
  border-radius: 8px;
  border: 2px solid #dce0e5;
  background-color: var(--white);
  transition: all 0.3s ease;
  margin-bottom: 1.5rem;
}

/* Style khi có lỗi validation */
.is-invalid {
  border-color: var(--danger-color) !important;
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 12 12' width='12' height='12' fill='none' stroke='%23dc3545'%3e%3ccircle cx='6' cy='6' r='4.5'/%3e%3cpath stroke-linejoin='round' d='M5.8 3.6h.4L6 6.5z'/%3e%3ccircle cx='6' cy='8.2' r='.6' fill='%23dc3545' stroke='none'/%3e%3c/svg%3e");
  background-repeat: no-repeat;
  background-position: right 1rem center;
  background-size: calc(0.75em + 0.375rem) calc(0.75em + 0.375rem);
  padding-right: 2.5rem;
}

.invalid-feedback {
  display: none;
  width: 100%;
  margin-top: -1rem;
  margin-bottom: 0.5rem;
  font-size: 0.875rem;
  color: var(--danger-color);
}

.is-invalid ~ .invalid-feedback {
  display: block;
}

/* Mở rộng dropdown khi mở */
.selectpicker + .dropdown-menu {
  width: 100%;
  max-width: 100%;
  font-size: 1.1rem;
}

.form-select:focus, 
.form-control:focus {
  border-color: var(--secondary-color);
  box-shadow: 0 0 0 3px rgba(58, 123, 213, 0.25);
  outline: none;
}

/* Hiệu ứng cho select */
select {
  cursor: pointer;
  appearance: none;
  -webkit-appearance: none;
  background-image: url("data:image/svg+xml;charset=utf-8,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 16 16'%3E%3Cpath fill='%230e4c92' d='M4 6h8l-4 5z'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 1.5rem center;
  background-size: 18px;
  padding-right: 3rem;
}

/* Container cho form chọn trường - sửa thụt lề và mở rộng */
.school-selection-container {
  background-color: var(--accent-color);
  border-radius: var(--border-radius);
  padding: 2.5rem;
  margin: 2rem 0;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
  width: 100%;
  max-width: 100%;
  border: 2px solid var(--primary-color);
}

.form-group {
  margin-bottom: 2rem;
  width: 100%;
}

.form-group:last-child {
  margin-bottom: 0;
}

/* Sửa Bootstrap Selects - Mở rộng */
.bootstrap-select > .dropdown-toggle {
  width: 100%;
  padding: 1.2rem 1.5rem;
  background-color: var(--white);
  border: 2px solid #dce0e5;
  border-radius: 8px;
  min-height: 55px;
  line-height: 1.5;
  font-size: 1.1rem;
}

/* Đảm bảo dropdown mở ra đủ rộng */
.bootstrap-select .dropdown-menu {
  width: 100%;
  min-width: 100%;
  padding: 0.5rem;
}

/* Style cho dropdown items */
.bootstrap-select .dropdown-menu li a {
  padding: 0.8rem 1.2rem;
  font-size: 1.05rem;
}

/* Nhóm xét tuyển - quan trọng nhất */
#group, #group + .dropdown-toggle, 
#priority_object, #priority_object + .dropdown-toggle {
  border: 2px solid var(--primary-color) !important;
  background-color: rgba(208, 225, 249, 0.2);
  min-height: 60px;
}

/* Tăng kích thước cho các options */
option {
  padding: 10px;
  font-size: 1.1rem;
}

/* Style đặc biệt cho dropdown trong school selection */
.school-selection-container .form-select,
.school-selection-container .bootstrap-select > .dropdown-toggle {
  border: 2px solid var(--secondary-color);
  background-color: var(--white);
  min-height: 58px;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.05);
}

/* Nút tính điểm - cải thiện hiển thị */
.btn-primary {
  background: linear-gradient(135deg, var(--secondary-color), var(--primary-color));
  color: var(--white);
  font-weight: 700;
  font-size: 1.2rem;
  padding: 1.2rem 2.5rem;
  border: none;
  border-radius: 8px;
  width: 100%;
  max-width: 100%;
  margin: 2.5rem auto 1.5rem;
  display: block;
  transition: all 0.3s;
  text-transform: uppercase;
  letter-spacing: 1px;
  box-shadow: 0 6px 20px rgba(14, 76, 146, 0.4);
  position: relative;
  overflow: hidden;
  min-height: 65px;
}

.btn-primary:before {
  content: "";
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
  transition: all 0.6s;
}

.btn-primary:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(14, 76, 146, 0.5);
  background: linear-gradient(135deg, var(--secondary-color), var(--primary-dark));
}

.btn-primary:hover:before {
  left: 100%;
}

.btn-primary:active {
  transform: translateY(1px);
}

/* Results container - cải thiện hiển thị */
.result-container {
  background: linear-gradient(145deg, var(--white), var(--accent-color));
  border-radius: var(--border-radius);
  padding: 2.5rem !important;
  margin: 2.5rem auto;
  max-width: 100%;
  box-shadow: 0 8px 25px rgba(14, 76, 146, 0.15);
  border-left: 5px solid var(--primary-color) !important;
  border-top: 1px solid var(--primary-color) !important;
  border-bottom: 1px solid var(--primary-color) !important;
}

.result-container h3 {
  color: var(--primary-color);
  font-size: 1.8rem;
  font-weight: 700;
  margin-bottom: 2rem;
  text-align: center;
  text-transform: uppercase;
  letter-spacing: 1px;
}

/* Danh sách kết quả */
.list-group {
  gap: 1.2rem;
}

.list-group-item {
  background-color: var(--white);
  border-radius: 10px !important;
  padding: 1.5rem 2rem;
  font-size: 1.15rem;
  border-left: 5px solid var(--secondary-color) !important;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.05);
  transition: transform 0.3s;
  margin-bottom: 1rem;
}

.list-group-item:hover {
  transform: translateX(5px);
}

.list-group-item strong {
  color: var(--primary-color);
  font-size: 1.3rem;
  font-weight: 700;
  margin-left: 1.5rem;
}

/* Hiệu ứng cho phần kết quả cuối */
.list-group-item:last-child {
  background-color: #eef6ff;
  border-left: 5px solid var(--primary-color) !important;
  padding: 1.8rem 2rem;
  margin-top: 0.5rem;
}

.list-group-item:last-child strong {
  color: var(--primary-color);
  font-size: 1.5rem;
}

/* Alert boxes */
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

.alert i {
  margin-right: 0.5rem;
}

/* Điều chỉnh responsive */
@media (max-width: 768px) {
  .card-body {
    padding: 1.5rem;
  }
  
  .result-container {
    padding: 1.5rem !important;
  }

  .list-group-item {
    flex-direction: column;
    align-items: flex-start;
  }

  .list-group-item strong {
    margin-left: 0;
    margin-top: 0.5rem;
  }
  
  .form-select,
  .bootstrap-select > .dropdown-toggle {
    font-size: 1rem;
    padding: 1rem;
  }
  
  /* Điều chỉnh alert trên mobile */
  .alert {
    padding: 0.6rem 1rem;
    font-size: 0.9rem;
  }
}

/* Loại bỏ spinner mặc định của input number */
input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

/* Firefox */
input[type=number] {
  -moz-appearance: textfield;
}
</style>
  
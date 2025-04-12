<template>
    <div>
      <!-- Hero Section: tạo không gian ấn tượng với hình nền liên quan đến du lịch -->
      <header class="hero-section py-5 text-center text-white">
        <div class="container">
          <h1 class="display-4 fw-bold">Tính Điểm Xét Tuyển</h1>
          <p class="lead">Giải pháp tối ưu cho môi trường giáo dục hiện đại kết hợp công nghệ IT và phong cách du lịch</p>
        </div>
      </header>
  
      <!-- Main Content -->
      <div class="container my-5">
        <div class="card shadow rounded">
          <div class="card-header bg-info text-white text-center">
            Tính điểm xét tuyển riêng - Trường ĐHBK - ĐHĐN
          </div>
          <div class="card-body">
            <form @submit.prevent="calculatePoint" id="pointForm">
              <!-- Bước 1: Chọn nhóm xét tuyển -->
              <div class="mb-3">
                <label for="group" class="form-label">Chọn nhóm xét tuyển</label>
                <select v-model="form.group" class="form-select selectpicker" id="group" @change="toggleSections" data-live-search="true">
                  <option value="">-- Chọn nhóm --</option>
                  <option value="1">Nhóm 1: Học sinh giỏi cấp quốc gia</option>
                  <option value="2">Nhóm 2: Học sinh giỏi cấp tỉnh</option>
                  <option value="3">Nhóm 3: Cuộc thi khoa học kỹ thuật cấp tỉnh</option>
                </select>
              </div>
  
              <!-- Bước 2: Chọn loại thành tích (nếu có) -->
              <div class="mb-3" v-if="showAchievement">
                <label for="achievement" class="form-label">Chọn loại thành tích</label>
                <select v-model="form.achievement" class="form-select selectpicker" id="achievement" data-live-search="true">
                  <option value="">-- Chọn loại giải --</option>
                  <option value="I">Giải Nhất</option>
                  <option value="II">Giải Nhì</option>
                  <option value="III">Giải Ba</option>
                  <option value="Khuyến khích">Giải Khuyến khích</option>
                </select>
              </div>
  
              <!-- Bước 3: Nhập điểm học bạ (nếu có) -->
              <div class="mb-3" v-if="showAchievement">
                <label class="form-label">Điểm tổng kết</label>
                <div class="row g-2">
                  <div class="col-md-4">
                    <input type="number" step="0.1" min="0" max="10" class="form-control" v-model.number="form.score10" placeholder="Lớp 10">
                  </div>
                  <div class="col-md-4">
                    <input type="number" step="0.1" min="0" max="10" class="form-control" v-model.number="form.score11" placeholder="Lớp 11">
                  </div>
                  <div class="col-md-4">
                    <input type="number" step="0.1" min="0" max="10" class="form-control" v-model.number="form.score12" placeholder="Lớp 12">
                  </div>
                </div>
              </div>
  
              <!-- Bước 4: Chọn trường (xác định khu vực ưu tiên) -->
              <h5 class="mt-4">Chọn trường</h5>
              <div class="row g-2">
                <div class="col-md-4">
                  <label for="city" class="form-label">Chọn Tỉnh/Thành phố</label>
                  <select v-model="form.city_id" class="form-select selectpicker" id="city" @change="loadDistricts" data-live-search="true">
                    <option value="">-- Chọn Tỉnh/Thành phố --</option>
                    <option v-for="city in cities" :key="city.id" :value="city.id">
                      {{ city.city_name }}
                    </option>
                  </select>
                </div>
                <div class="col-md-4">
                  <label for="district" class="form-label">Chọn Quận/Huyện</label>
                  <select v-model="form.district_id" class="form-select selectpicker" id="district" @change="loadSchools" :disabled="!districts.length" data-live-search="true">
                    <option value="">-- Chọn Quận/Huyện --</option>
                    <option v-for="district in districts" :key="district.id" :value="district.id">
                      {{ district.name }}
                    </option>
                  </select>
                </div>
                <div class="col-md-4">
                  <label for="school" class="form-label">Chọn Trường THPT</label>
                  <select v-model="form.school_id" class="form-select selectpicker" id="school" :disabled="!schools.length" data-live-search="true">
                    <option value="">-- Chọn Trường THPT --</option>
                    <option v-for="school in schools" :key="school.id" :value="school.id" :data-priority="school.priority_area">
                      {{ school.name }}
                    </option>
                  </select>
                </div>
              </div>
              <div class="mt-3" v-if="selectedSchoolPriority">
                <p class="fw-bold">Khu vực ưu tiên: {{ selectedSchoolPriority }}</p>
              </div>
  
              <!-- Bước 5: Chọn đối tượng ưu tiên -->
              <div class="mb-3 mt-4">
                <label for="priority_object" class="form-label">Chọn Ưu tiên đối tượng</label>
                <select v-model="form.priority_object" class="form-select selectpicker" id="priority_object" data-live-search="true" data-width="100%">
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
          score10: 0,
          score11: 0,
          score12: 0,
          city_id: '',
          district_id: '',
          school_id: '',
          priority_object: ''
        },
        result: null,
        showAchievement: false
      }
    },
    computed: {
      selectedSchoolPriority() {
        if (this.schools.length && this.form.school_id) {
          const selected = this.schools.find(s => s.id == this.form.school_id)
          return selected ? selected.priority_area : ''
        }
        return ''
      }
    },
    methods: {
      toggleSections() {
        this.showAchievement = this.form.group === '2' || this.form.group === '3'
        this.$nextTick(() => {
          $('.selectpicker').selectpicker('refresh')
        })
      },
      loadCities() {
        axios.get('http://localhost:8000/point-count')
          .then(res => {
            this.cities = res.data
            this.$nextTick(() => {
              $('.selectpicker').selectpicker('refresh')
            })
          })
          .catch(err => console.error(err))
      },
      loadDistricts() {
        this.form.district_id = ''
        this.schools = []
        if (this.form.city_id) {
          axios.get(`http://localhost:8000/get_districts?city_id=${this.form.city_id}`)
            .then(res => {
              this.districts = res.data
              this.$nextTick(() => {
                $('.selectpicker').selectpicker('refresh')
              })
            })
            .catch(err => console.error(err))
        } else {
          this.districts = []
        }
      },
      loadSchools() {
        this.form.school_id = ''
        if (this.form.district_id) {
          axios.get(`http://localhost:8000/get_schools?district_id=${this.form.district_id}`)
            .then(res => {
              this.schools = res.data
              this.$nextTick(() => {
                $('.selectpicker').selectpicker('refresh')
              })
            })
            .catch(err => console.error(err))
        } else {
          this.schools = []
        }
      },
      calculatePoint() {
        const formData = new FormData()
        for (let key in this.form) {
          formData.append(key, this.form[key])
        }
        axios.post('http://localhost:8000/api/point-count', formData)
          .then(res => {
            this.result = res.data
          })
          .catch(err => console.error(err))
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
  /* Hero Section */
  .hero-section {
    background-color: #343a40; /* màu dự phòng nếu ảnh không load được */
  }
  
  /* Card: thiết kế hiện đại, mềm mại */
  .card {
    border: none;
  }
  .card-header {
    font-size: 1.25rem;
  }
  
  /* Kết quả: tạo border mềm mại và nền sáng */
  .result-container {
    border: 2px solid #17a2b8;
    border-radius: 15px;
    padding: 20px;
    background-color: #f8f9fa;
  }
  .list-group-item {
    font-size: 1.1rem;
  }
  </style>
  
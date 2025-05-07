<template>
  <div>
    <!-- Hero Section -->
    <header class="hero-section py-5 text-center text-white">
      <div class="container">
        <h1 class="display-4 fw-bold">Tính Điểm Xét Tuyển Thi THPT</h1>
        <p class="lead">Trường Đại học Bách Khoa - Đại học Đà Nẵng</p>
      </div>
    </header>

    <!-- Main Content -->
    <div class="container my-5">
      <div class="card shadow rounded">
        <div class="card-header text-white text-center">
          Công cụ tính điểm xét tuyển theo điểm thi tốt nghiệp THPT
        </div>
        <div class="card-body">
          <div v-if="showPriorityStep" class="step-indicator">
            <div class="step active">
              <div class="step-number">1</div>
              <div class="step-title">Nhập điểm</div>
            </div>
            <div class="step-line"></div>
            <div class="step" :class="{ active: showPriorityStep }">
              <div class="step-number">2</div>
              <div class="step-title">Tính điểm ưu tiên</div>
            </div>
          </div>

          <!-- Bước 1: Nhập điểm -->
          <div v-if="!showPriorityStep">
            <form @submit.prevent="calculateInitialScores">
              <!-- Nhập điểm môn thi -->
              <div class="subject-list">
                <h5 class="section-title">Nhập điểm các môn thi</h5>
                <div v-for="(subject, index) in subjectScores" :key="index" class="subject-item">
                  <div class="subject-header">
                    <select class="form-select subject-selector" 
                            v-model="subject.selectedSubject"
                            @change="updateSubjectId(index)">
                      <option value="">-- Chọn môn thi --</option>
                      <option v-for="sub in subjects" 
                              :key="sub.id" 
                              :value="sub">
                        {{ sub.name }}
                      </option>
                    </select>
                    <button type="button" class="btn btn-danger remove-btn" 
                            @click="removeSubject(index)"
                            :disabled="subjectScores.length <= 1">
                      <i class="bi bi-x"></i>
                    </button>
                  </div>
                  
                  <div class="scores-container">
                    <div class="score-input-group exam-score">
                      <label>Điểm thi:</label>
                      <input type="number" 
                             class="form-control" 
                             v-model="subject.scores[0]" 
                             min="0" 
                             max="10" 
                             step="0.05"
                             @blur="formatExamScore(index)"
                             placeholder="Nhập điểm (0-10)">
                      <small class="form-text text-muted">Điểm làm tròn đến 0.05</small>
                    </div>
                  </div>
                </div>
                
                <div class="subject-actions">
                  <button type="button" class="btn btn-primary add-subject-btn" @click="addSubject">
                    <i class="bi bi-plus-circle"></i> Thêm môn thi
                  </button>
                </div>
              </div>
              
              <div v-if="loading" class="loading-indicator">
                <div class="spinner-border text-primary" role="status">
                  <span class="visually-hidden">Loading...</span>
                </div>
                <p>Đang tính toán...</p>
              </div>
              
              <div v-if="error" class="alert alert-danger mt-4">
                <i class="bi bi-exclamation-circle"></i> {{ error }}
              </div>

              <button type="submit" class="btn btn-calculate">
                <i class="bi bi-calculator"></i> Tính điểm
              </button>
            </form>
          </div>
          
          <!-- Bước 2: Chọn tổ hợp và tính điểm ưu tiên -->
          <div v-if="showPriorityStep">
            <form @submit.prevent="calculatePriorityScores">
              <!-- Chọn tổ hợp để tính ưu tiên -->
              <h5 class="section-title">Chọn tổ hợp xét tuyển</h5>
              <div class="combination-selection">
                <div v-for="(combination, index) in initialCombinations" :key="combination.group_id" class="combination-checkbox">
                  <input 
                    type="checkbox" 
                    class="form-check-input" 
                    :id="`combination-${combination.group_id}`" 
                    v-model="selectedCombinationIds" 
                    :value="combination.group_id"
                  >
                  <label class="form-check-label" :for="`combination-${combination.group_id}`">
                    <span class="combination-name">{{ combination.group_name }}</span>
                    <span class="combination-score">Điểm: {{ combination.score }}</span>
                  </label>
                </div>
              </div>
              <div class="alert alert-warning mt-2" v-if="!selectedCombinationIds.length && submitted">
                <i class="bi bi-exclamation-triangle me-2"></i>
                Vui lòng chọn ít nhất một tổ hợp xét tuyển
              </div>
              
              <!-- Chọn trường (xác định khu vực ưu tiên) -->
              <h5 class="section-title mt-4">Chọn trường</h5>
              <div class="school-selection-container">
                <div class="form-group">
                  <label for="city" class="form-label">Chọn Tỉnh/Thành phố</label>
                  <select 
                    v-model="cityId" 
                    class="form-select" 
                    id="city" 
                    @change="loadDistricts">
                    <option value="">-- Chọn Tỉnh/Thành phố --</option>
                    <option v-for="city in cities" :key="city.id" :value="city.id">
                      {{ city.name }}
                    </option>
                  </select>
                </div>
                <div class="form-group">
                  <label for="district" class="form-label">Chọn Quận/Huyện</label>
                  <select 
                    v-model="districtId" 
                    class="form-select" 
                    id="district" 
                    @change="loadSchools" 
                    :disabled="!districts.length">
                    <option value="">-- Chọn Quận/Huyện --</option>
                    <option v-for="district in districts" :key="district.id" :value="district.id">
                      {{ district.name }}
                    </option>
                  </select>
                </div>
                <div class="form-group">
                  <label for="school" class="form-label">Chọn Trường THPT</label>
                  <select 
                    v-model="schoolId" 
                    class="form-select" 
                    id="school" 
                    :disabled="!schools.length">
                    <option value="">-- Chọn Trường THPT --</option>
                    <option v-for="school in schools" :key="school.id" :value="school.id">
                      {{ school.name }}
                    </option>
                  </select>
                </div>
              </div>
              <div class="mt-3 text-center" v-if="selectedSchoolPriority">
                <p class="fw-bold">Khu vực ưu tiên: {{ selectedSchoolPriority }}</p>
              </div>

              <!-- Chọn đối tượng ưu tiên -->
              <div class="mb-3 mt-4">
                <h5 class="section-title">Chọn Ưu tiên đối tượng</h5>
                <select 
                  v-model="priorityObject" 
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
              
              <div class="action-buttons">
                <button type="button" class="btn btn-outline-secondary" @click="goBackToScores">
                  <i class="bi bi-arrow-left"></i> Quay lại
                </button>
                <button type="submit" class="btn btn-calculate">
                  <i class="bi bi-calculator"></i> Tính điểm ưu tiên
                </button>
              </div>
            </form>
          </div>
          
          <!-- Hiển thị kết quả sau bước 1: Tính điểm -->
          <div class="initial-results mt-4" v-if="initialCombinations.length > 0 && !showPriorityStep">
            <h3 class="text-center">Kết quả tính điểm tổ hợp</h3>
            
            <div class="combinations-table">
              <table class="table table-striped">
                <thead>
                  <tr>
                    <th>STT</th>
                    <th>Tổ hợp</th>
                    <th>Môn thi</th>
                    <th>Điểm thi</th>
                    <th>Hệ số</th>
                    <th>Điểm tổ hợp</th>
                  </tr>
                </thead>
                <tbody>
                  <template v-for="(combination, index) in initialCombinations" :key="`combination-${combination.group_id}`">
                    <tr class="combination-row">
                      <td>{{ index + 1 }}</td>
                      <td>{{ combination.group_name }}</td>
                      <td colspan="3"></td>
                      <td class="fw-bold">{{ combination.score }}</td>
                    </tr>
                    <tr v-for="(subject, subIndex) in combination.subjects" :key="`subject-${combination.group_id}-${subIndex}`">
                      <td></td>
                      <td></td>
                      <td>{{ subject.name }}</td>
                      <td>{{ subject.score.toFixed(2) }}</td>
                      <td>{{ subject.coefficient }}</td>
                      <td></td>
                    </tr>
                  </template>
                </tbody>
              </table>
            </div>
            
            <div class="text-center mt-4">
              <button class="btn btn-primary btn-lg" @click="proceedToPriorityStep">
                <i class="bi bi-arrow-right-circle"></i> Tính điểm ưu tiên
              </button>
            </div>
          </div>
          
          <!-- Hiển thị kết quả cuối cùng với điểm ưu tiên -->
          <div class="final-results-container mt-4" v-if="finalResults.length > 0">
            <h3 class="text-center">Kết quả tính điểm xét tuyển</h3>
            
            <template v-for="(result, resultIndex) in finalResults" :key="`result-${resultIndex}`">
              <div class="combination-result">
                <h4 class="combination-name">{{ result.group_name }}</h4>
                
                <!-- Chi tiết điểm từng môn trong tổ hợp -->
                <div class="subject-scores-table">
                  <h5 class="table-title">Điểm các môn thi</h5>
                  <div class="table-responsive">
                    <table class="table table-bordered">
                      <thead>
                        <tr>
                          <th>Môn thi</th>
                          <th>Điểm thi</th>
                          <th>Hệ số</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr v-for="(subject, subjectIndex) in result.subjects" :key="`${resultIndex}-${subjectIndex}`">
                          <td>{{ subject.name }}</td>
                          <td>{{ subject.score.toFixed(2) }}</td>
                          <td>{{ subject.coefficient }}</td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div>
                
                <!-- Điểm tổ hợp và điểm ưu tiên -->
                <div class="point-summary">
                  <div class="row">
                    <div class="col-md-4">
                      <div class="point-card original">
                        <div class="point-title">Điểm tổ hợp gốc</div>
                        <div class="point-value">{{ result.score }}</div>
                        <div class="point-description">(Thang điểm 30)</div>
                      </div>
                    </div>
                    <div class="col-md-4">
                      <div class="point-card priority">
                        <div class="point-title">Điểm ưu tiên</div>
                        <div class="point-value">{{ result.priority_points.convert_priority }}</div>
                        <div class="point-description">(Đã quy đổi)</div>
                      </div>
                    </div>
                    <div class="col-md-4">
                      <div class="point-card total">
                        <div class="point-title">Tổng điểm xét tuyển</div>
                        <div class="point-value">{{ result.priority_points.total_point }}</div>
                        <div class="point-description">(Điểm gốc + ưu tiên)</div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <hr v-if="resultIndex < finalResults.length - 1" class="result-divider">
            </template>
            
            <!-- Reset button for starting over -->
            <div class="text-center mt-4">
              <button class="btn btn-secondary" @click="resetCalculator">
                <i class="bi bi-arrow-counterclockwise"></i> Tính toán lại
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted, watch } from 'vue';
import CalculateScoreController from '@/controllers/CalculateScoreController';

export default {
  name: 'CalculateScoreTHPT',
  setup() {
    // Form state
    const subjects = ref([]);
    const subjectScores = ref([
      {
        selectedSubject: '',
        subject_id: null,
        subject_name: '',
        scores: ['']
      }
    ]);
    
    // School selection
    const cities = ref([]);
    const districts = ref([]);
    const schools = ref([]);
    const cityId = ref('');
    const districtId = ref('');
    const schoolId = ref(null);
    const priorityObject = ref('0');
    
    // Results and state
    const initialCombinations = ref([]);
    const selectedCombinationIds = ref([]);
    const finalResults = ref([]);
    const loading = ref(false);
    const error = ref('');
    const submitted = ref(false);
    const showPriorityStep = ref(false);
    
    // Computed properties
    const selectedSchoolPriority = computed(() => {
      if (schools.value.length && schoolId.value) {
        const selected = schools.value.find(s => s.id == schoolId.value);
        return selected ? selected.priority_area : '';
      }
      return '';
    });
    
    // Methods
    const addSubject = () => {
      subjectScores.value.push({
        selectedSubject: '',
        subject_id: null,
        subject_name: '',
        scores: ['']
      });
    };
    
    const removeSubject = (index) => {
      if (subjectScores.value.length > 1) {
        subjectScores.value.splice(index, 1);
      }
    };
    
    const updateSubjectId = (index) => {
      const selected = subjectScores.value[index].selectedSubject;
      if (selected) {
        subjectScores.value[index].subject_id = selected.id;
        subjectScores.value[index].subject_name = selected.name;
      } else {
        subjectScores.value[index].subject_id = null;
        subjectScores.value[index].subject_name = '';
      }
    };
    
    // Format điểm thi theo yêu cầu (làm tròn đến 0.05, tối đa 2 chữ số thập phân)
    const formatExamScore = (index) => {
      const scoreValue = subjectScores.value[index].scores[0];
      if (scoreValue !== '' && !isNaN(parseFloat(scoreValue))) {
        // Làm tròn đến 0.05 gần nhất
        const roundedValue = Math.round(parseFloat(scoreValue) * 20) / 20;
        // Giới hạn số thập phân tối đa là 2
        subjectScores.value[index].scores[0] = roundedValue.toFixed(2);
      }
    };
    
    const loadCities = async () => {
      try {
        cities.value = await CalculateScoreController.getCities();
      } catch (err) {
        console.error('Error loading cities:', err);
      }
    };
    
    const loadDistricts = async () => {
      districtId.value = '';
      schoolId.value = null;
      schools.value = [];
      
      if (cityId.value) {
        try {
          districts.value = await CalculateScoreController.getDistricts(cityId.value);
        } catch (err) {
          console.error('Error loading districts:', err);
          districts.value = [];
        }
      } else {
        districts.value = [];
      }
    };
    
    const loadSchools = async () => {
      schoolId.value = null;
      
      if (districtId.value) {
        try {
          schools.value = await CalculateScoreController.getSchools(districtId.value);
        } catch (err) {
          console.error('Error loading schools:', err);
          schools.value = [];
        }
      } else {
        schools.value = [];
      }
    };
    
    const loadSubjects = async () => {
      try {
        subjects.value = await CalculateScoreController.getSubjects();
      } catch (err) {
        error.value = 'Không thể tải danh sách môn học. Vui lòng thử lại sau.';
      }
    };
    
    const validateScoreForm = () => {
      error.value = '';
      
      // Check if subjects are selected and have scores
      const invalidSubjects = subjectScores.value.filter(subject => !subject.selectedSubject);
      if (invalidSubjects.length > 0) {
        error.value = 'Vui lòng chọn đầy đủ các môn thi';
        return false;
      }
      
      // Check if all subjects have valid scores
      const invalidScores = subjectScores.value.filter(subject => 
        !subject.scores[0] || subject.scores[0] === '' || isNaN(parseFloat(subject.scores[0]))
      );
      if (invalidScores.length > 0) {
        error.value = 'Vui lòng nhập đầy đủ điểm cho tất cả các môn thi';
        return false;
      }
      
      // Kiểm tra định dạng điểm và làm tròn
      let hasInvalidFormat = false;
      subjectScores.value.forEach((subject, index) => {
        formatExamScore(index);
        const scoreValue = parseFloat(subject.scores[0]);
        if (isNaN(scoreValue) || scoreValue < 0 || scoreValue > 10) {
          hasInvalidFormat = true;
        }
      });
      
      if (hasInvalidFormat) {
        error.value = 'Điểm phải nằm trong khoảng từ 0 đến 10 và được làm tròn đến 0.05';
        return false;
      }
      
      return true;
    };
    
    const validatePriorityForm = () => {
      error.value = '';
      submitted.value = true;
      
      if (selectedCombinationIds.value.length === 0) {
        error.value = 'Vui lòng chọn ít nhất một tổ hợp xét tuyển';
        return false;
      }
      
      return true;
    };
    
    const calculateInitialScores = async () => {
      if (!validateScoreForm()) {
        return;
      }
      
      try {
        loading.value = true;
        error.value = '';
        
        // Format data for API
        const formattedData = subjectScores.value.map(subject => ({
          subject_id: subject.subject_id,
          subject_name: subject.subject_name,
          scores: [parseFloat(subject.scores[0])]
        }));
        
        // Calculate scores
        const scoreResult = await CalculateScoreController.calculateTHPTScores(formattedData);
        
        initialCombinations.value = scoreResult.combinations;
        
        if (initialCombinations.value.length === 0) {
          error.value = 'Không tìm thấy tổ hợp phù hợp với các điểm đã nhập.';
        }
        
      } catch (err) {
        error.value = 'Có lỗi xảy ra khi tính điểm. Vui lòng kiểm tra dữ liệu và thử lại.';
        console.error(err);
      } finally {
        loading.value = false;
      }
    };
    
    const proceedToPriorityStep = () => {
      // Automatically select all combinations initially
      selectedCombinationIds.value = initialCombinations.value.map(comb => comb.group_id);
      showPriorityStep.value = true;
      
      // Refresh bootstrap-select sau khi chuyển bước
      setTimeout(() => {
        $('.selectpicker').selectpicker('refresh');
      }, 100);
    };
    
    const goBackToScores = () => {
      showPriorityStep.value = false;
    };
    
    const calculatePriorityScores = async () => {
      if (!validatePriorityForm()) {
        return;
      }
      
      try {
        loading.value = true;
        error.value = '';
        
        // Filter combinations by selected ids
        const selectedCombinations = initialCombinations.value.filter(
          comb => selectedCombinationIds.value.includes(comb.group_id)
        );
        
        // Calculate priority points for the selected combinations
        finalResults.value = await CalculateScoreController.calculateCombinationPriorityPoints(
          selectedCombinations,
          selectedSchoolPriority.value,
          priorityObject.value,
          schoolId.value
        );
        
      } catch (err) {
        error.value = 'Có lỗi xảy ra khi tính điểm ưu tiên. Vui lòng thử lại.';
        console.error(err);
      } finally {
        loading.value = false;
      }
    };
    
    const resetCalculator = () => {
      // Reset state to initial values
      subjectScores.value = [
        {
          selectedSubject: '',
          subject_id: null,
          subject_name: '',
          scores: ['']
        }
      ];
      initialCombinations.value = [];
      selectedCombinationIds.value = [];
      finalResults.value = [];
      cityId.value = '';
      districtId.value = '';
      schoolId.value = null;
      districts.value = [];
      schools.value = [];
      priorityObject.value = '0';
      error.value = '';
      submitted.value = false;
      showPriorityStep.value = false;
    };
    
    // Init
    onMounted(async () => {
      loading.value = true;
      try {
        await Promise.all([
          loadSubjects(),
          loadCities()
        ]);
        
        // Khởi tạo bootstrap-select
        setTimeout(() => {
          $('.selectpicker').selectpicker();
        }, 300);
        
      } catch (err) {
        error.value = 'Không thể tải dữ liệu ban đầu. Vui lòng tải lại trang.';
      } finally {
        loading.value = false;
      }
    });
    
    return {
      // Form state
      subjects,
      subjectScores,
      
      // School selection
      cities,
      districts,
      schools,
      cityId,
      districtId,
      schoolId,
      priorityObject,
      
      // Results and state
      initialCombinations,
      selectedCombinationIds,
      finalResults,
      loading,
      error,
      submitted,
      showPriorityStep,
      
      // Computed properties
      selectedSchoolPriority,
      
      // Methods
      addSubject,
      removeSubject,
      updateSubjectId,
      formatExamScore,
      loadDistricts,
      loadSchools,
      calculateInitialScores,
      proceedToPriorityStep,
      goBackToScores,
      calculatePriorityScores,
      resetCalculator
    };
  }
}
</script>

<style scoped>
/* Hero Section - banner chính */
.hero-section {
  background: linear-gradient(135deg, rgba(14, 76, 146, 0.95), rgba(31, 64, 104, 0.95)), 
              url('https://images.unsplash.com/photo-1523050854058-8df90110c9f1?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80');
  background-size: cover;
  background-position: center;
  padding: 3.5rem 0;
  text-align: center;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
  border-bottom: 5px solid #3a7bd5;
}

.hero-section h1 {
  color: #ffffff;
  font-size: 2.5rem;
  font-weight: 800;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.4);
  margin-bottom: 0.5rem;
  letter-spacing: 1px;
}

.hero-section p.lead {
  color: #ffffff;
  font-size: 1.25rem;
  max-width: 800px;
  margin: 0 auto;
  opacity: 0.9;
}

/* Card styling */
.card {
  background-color: #ffffff;
  border: none;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
  margin: 2rem 0;
}

.card-header {
  background-color: #0B2942 !important;
  color: #ffffff !important;
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

/* Step indicator */
.step-indicator {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 2rem;
}

.step {
  display: flex;
  flex-direction: column;
  align-items: center;
  opacity: 0.5;
}

.step.active {
  opacity: 1;
}

.step-number {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: #0B2942;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 1.2rem;
  margin-bottom: 0.5rem;
}

.step-title {
  font-weight: 600;
  color: #0B2942;
}

.step-line {
  height: 3px;
  background-color: #0B2942;
  flex-grow: 1;
  margin: 0 1rem;
  position: relative;
  top: -10px;
}

/* Section titles */
.section-title {
  color: #0B2942;
  font-size: 1.4rem;
  text-align: center;
  margin: 1.5rem 0;
  font-weight: 700;
  position: relative;
}

.section-title:after {
  content: "";
  display: block;
  width: 80px;
  height: 4px;
  background: #4da0ff;
  margin: 0.7rem auto 1.5rem;
  border-radius: 2px;
}

/* Subject items */
.subject-item {
  background-color: #f8f9fa;
  border-radius: 8px;
  padding: 1.5rem;
  margin-bottom: 1rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.subject-header {
  display: flex;
  margin-bottom: 1rem;
}

.subject-selector {
  flex-grow: 1;
  margin-right: 1rem;
}

.remove-btn {
  border-radius: 50%;
  width: 38px;
  height: 38px;
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.scores-container {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}

.exam-score {
  flex: 0 0 300px;
}

.score-input-group label {
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
  display: block;
  color: #555;
}

.form-text {
  font-size: 0.8rem;
  margin-top: 0.25rem;
  display: block;
}

.subject-actions {
  margin-top: 1.5rem;
  text-align: center;
}

.add-subject-btn {
  background-color: #3a7bd5;
  border: none;
  border-radius: 8px;
  padding: 0.7rem 1.5rem;
  transition: all 0.3s;
}

.add-subject-btn:hover {
  background-color: #2a6bc9;
  transform: translateY(-2px);
}

/* Form elements */
.form-check-input:checked {
  background-color: #0B2942;
  border-color: #0B2942;
}

.form-check-label {
  font-weight: 500;
  color: #333;
  font-size: 1.1rem;
}

/* School selection container */
.school-selection-container {
  background-color: #f0f8ff;
  border-radius: 12px;
  padding: 2rem;
  margin: 2rem 0;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
  border: 1px solid #d0e1f9;
}

.form-label {
  font-weight: 600;
  color: #0B2942;
  margin-bottom: 0.7rem;
}

.form-select, .form-control {
  border-radius: 8px;
  border: 2px solid #dce0e5;
  padding: 0.8rem 1rem;
  margin-bottom: 1rem;
  transition: all 0.3s;
}

.form-select:focus, .form-control:focus {
  border-color: #3a7bd5;
  box-shadow: 0 0 0 3px rgba(58, 123, 213, 0.25);
}

/* Calculate button */
.btn-calculate {
  background: linear-gradient(135deg, #3a7bd5, #0B2942);
  color: #ffffff;
  font-weight: 700;
  font-size: 1.2rem;
  padding: 1.2rem 2.5rem;
  border: none;
  border-radius: 8px;
  width: 100%;
  max-width: 100%;
  margin: 2rem auto 1rem;
  display: block;
  transition: all 0.3s;
  text-transform: uppercase;
  letter-spacing: 1px;
  box-shadow: 0 6px 20px rgba(14, 76, 146, 0.4);
}

.btn-calculate:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(14, 76, 146, 0.5);
}

.btn-calculate:active {
  transform: translateY(1px);
}

/* Initial results table */
.initial-results {
  background-color: #f0f8ff;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  border: 1px solid #d0e1f9;
}

.initial-results h3 {
  color: #0B2942;
  font-weight: 700;
  margin-bottom: 1.5rem;
}

.combinations-table {
  overflow-x: auto;
}

.combination-row {
  background-color: rgba(14, 76, 146, 0.1);
  font-weight: 600;
}

/* Combination selection */
.combination-selection {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}

.combination-checkbox {
  background-color: #f8f9fa;
  padding: 1rem;
  border-radius: 8px;
  display: flex;
  align-items: flex-start;
  gap: 0.5rem;
  transition: all 0.2s;
  border: 1px solid #eee;
}

.combination-checkbox:hover {
  background-color: #e9f0f8;
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
}

.combination-checkbox label {
  display: flex;
  flex-direction: column;
  cursor: pointer;
  flex-grow: 1;
}

.combination-checkbox .combination-name {
  font-weight: 600;
  color: #0B2942;
}

.combination-checkbox .combination-score {
  font-size: 0.9rem;
  color: #555;
  margin-top: 0.3rem;
}

/* Action buttons */
.action-buttons {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
}

.action-buttons button {
  flex: 1;
  padding: 1rem;
  font-weight: 600;
}

/* Loading indicator */
.loading-indicator {
  text-align: center;
  margin: 2rem 0;
}

.loading-indicator p {
  margin-top: 1rem;
  font-weight: 500;
  color: #0B2942;
}

/* Final results */
.final-results-container {
  background-color: #fff;
  border-radius: 12px;
  padding: 2rem;
  margin-top: 3rem;
  box-shadow: 0 5px 20px rgba(0, 41, 103, 0.1);
  border-top: 5px solid #0B2942;
}

.final-results-container h3 {
  color: #0B2942;
  font-weight: 700;
  margin-bottom: 2rem;
  text-align: center;
}

.combination-result {
  margin-bottom: 2rem;
}

.combination-name {
  background: linear-gradient(135deg, #0B2942, #3a7bd5);
  color: #fff;
  padding: 1rem 1.5rem;
  border-radius: 10px;
  font-weight: 600;
  text-align: center;
  margin-bottom: 1.5rem;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.1);
}

.subject-scores-table {
  background-color: #f8f9fa;
  border-radius: 10px;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
}

.table-title {
  color: #0B2942;
  font-size: 1.1rem;
  margin-bottom: 1rem;
  font-weight: 600;
}

.table {
  margin-bottom: 0;
}

.table th {
  background-color: #d0e1f9;
  color: #0B2942;
  font-weight: 600;
}

.point-summary {
  margin-top: 1.5rem;
}

.point-card {
  background-color: #f8f9fa;
  border-radius: 10px;
  padding: 1.5rem;
  text-align: center;
  height: 100%;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.05);
  transition: transform 0.3s;
}

.point-card:hover {
  transform: translateY(-5px);
}

.point-card.original {
  border-left: 5px solid #3a7bd5;
}

.point-card.priority {
  border-left: 5px solid #28a745;
}

.point-card.total {
  border-left: 5px solid #fd7e14;
  background-color: #fffaf0;
}

.point-title {
  color: #0B2942;
  font-weight: 600;
  font-size: 1.1rem;
  margin-bottom: 0.5rem;
}

.point-value {
  font-size: 2.5rem;
  font-weight: 700;
  color: #0B2942;
}

.point-description {
  color: #6c757d;
  font-size: 0.9rem;
}

.result-divider {
  margin: 2.5rem 0;
  border-top: 2px dashed #d0e1f9;
}

/* Responsive adjustments */
@media (max-width: 992px) {
  .exam-score {
    flex: 0 0 100%;
    max-width: 100%;
  }
}

@media (max-width: 768px) {
  .card-body {
    padding: 1.5rem;
  }
  
  .action-buttons {
    flex-direction: column;
  }
  
  .combination-selection {
    grid-template-columns: 1fr;
  }
  
  .total-score {
    flex-direction: column;
    text-align: center;
  }
  
  .point-card {
    margin-bottom: 1rem;
  }
}

@media (max-width: 576px) {
  .hero-section h1 {
    font-size: 2rem;
  }
  
  .hero-section p.lead {
    font-size: 1rem;
  }
  
  .card-header {
    font-size: 1.1rem;
    padding: 1rem;
  }
  
  .card-body {
    padding: 1rem;
  }
  
  .section-title {
    font-size: 1.2rem;
  }
  
  .btn-calculate {
    font-size: 1rem;
    padding: 1rem;
  }
}
</style>
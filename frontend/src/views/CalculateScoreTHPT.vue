<template>
  <div>
    <!-- Hero Section - Thu gọn -->
    <header class="hero-section py-3 py-md-4 text-center text-white">
      <div class="container">
        <h1 class="fw-bold mb-1">Tính Điểm Xét Tuyển Thi THPT</h1>
        <p>Trường Đại học Bách Khoa - Đại học Đà Nẵng</p>
      </div>
    </header>

    <!-- Thông báo lỗi URL nếu có -->
    <div v-if="urlParseError" class="container mt-2">
      <div class="alert alert-warning py-2 px-3 small">
        <i class="bi bi-exclamation-triangle me-1"></i>
        {{ urlParseError }}
      </div>
    </div>

    <!-- Main Content - Cải thiện cấu trúc -->
    <main class="container my-3 my-md-4">
      <div class="card shadow-sm rounded">
        <div class="card-header text-white text-center py-2">
          <h2 class="h5 mb-0">Công cụ tính điểm xét tuyển theo điểm thi tốt nghiệp THPT</h2>
        </div>
        <div class="card-body p-2 p-md-3">
          <!-- Indicator steps -->
          <div v-if="showPriorityStep" class="step-indicator mb-3">
            <div class="step active">
              <div class="step-number">1</div>
              <div class="step-title small">Nhập điểm</div>
            </div>
            <div class="step-line"></div>
            <div class="step" :class="{ active: showPriorityStep }">
              <div class="step-number">2</div>
              <div class="step-title small">Tính điểm ưu tiên</div>
            </div>
          </div>

          <!-- Bước 1: Nhập điểm - Thiết kế dạng bảng với mỗi môn một hàng -->
          <div v-if="!showPriorityStep">
            <form @submit.prevent="calculateInitialScores">
              <!-- Nhập điểm môn thi - Thiết kế mới dạng bảng -->
              <div class="subject-list">
                <h3 class="section-title h6">Nhập điểm các môn thi</h3>
                
                <div class="table-responsive">
                  <table class="table table-sm table-bordered">
                    <thead class="bg-light">
                      <tr>
                        <th style="width: 60%">Môn thi</th>
                        <th style="width: 30%" class="text-center">Điểm thi</th>
                        <th style="width: 10%" class="text-center">
                          <span class="visually-hidden">Thao tác</span>
                        </th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="(subject, index) in subjectScores" :key="index">
                        <td>
                          <select class="form-select form-select-sm" 
                                v-model="subject.selectedSubject"
                                @change="updateSubjectId(index)"
                                aria-label="Chọn môn thi">
                            <option value="">-- Chọn môn thi --</option>
                            <option v-for="sub in subjects" 
                                  :key="sub.id" 
                                  :value="sub">
                              {{ sub.name }}
                            </option>
                          </select>
                        </td>
                        <td>
                          <div class="input-group input-group-sm">
                            <input type="number" 
                                  class="form-control form-control-sm" 
                                  v-model="subject.scores[0]" 
                                  min="0" 
                                  max="10" 
                                  step="0.05"
                                  @blur="formatExamScore(index)"
                                  placeholder="Nhập điểm (0-10)"
                                  aria-label="Điểm thi">
                          </div>
                          <small class="form-text text-muted small">Làm tròn đến 0.05</small>
                        </td>
                        <td class="text-center align-middle">
                          <button type="button" class="btn btn-sm btn-outline-danger" 
                                @click="removeSubject(index)"
                                :disabled="subjectScores.length <= 1"
                                aria-label="Xóa môn học">
                            <i class="bi bi-x"></i>
                          </button>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
                
                <div class="subject-actions mt-2">
                  <button type="button" class="btn btn-sm btn-outline-primary" @click="addSubject">
                    <i class="bi bi-plus-circle"></i> Thêm môn thi
                  </button>
                </div>
              </div>
              
              <div v-if="loading" class="loading-indicator my-2 text-center">
                <div class="spinner-border spinner-border-sm text-primary" role="status">
                  <span class="visually-hidden">Đang tải...</span>
                </div>
                <p class="small mb-0 mt-1">Đang tính toán...</p>
              </div>
              
              <div v-if="error" class="alert alert-danger mt-2 p-2 small">
                <i class="bi bi-exclamation-circle"></i> {{ error }}
              </div>

              <div class="text-center mt-3">
                <button type="submit" class="btn btn-calculate btn-sm">
                  <i class="bi bi-calculator"></i> Tính điểm
                </button>
              </div>
            </form>
          </div>
          
          <!-- Bước 2: Chọn tổ hợp và tính điểm ưu tiên -->
          <div v-if="showPriorityStep">
            <form @submit.prevent="calculatePriorityScores">
              <!-- Chọn tổ hợp để tính ưu tiên -->
              <h3 class="section-title h6">Chọn tổ hợp xét tuyển</h3>
              <div class="table-responsive">
                <table class="table table-sm table-bordered">
                  <thead class="bg-light">
                    <tr>
                      <th style="width: 5%"></th>
                      <th>Tổ hợp</th>
                      <th style="width: 20%" class="text-end">Điểm</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="(combination, index) in initialCombinations" :key="combination.group_id">
                      <td class="text-center">
                        <input 
                          type="checkbox" 
                          class="form-check-input" 
                          :id="`combination-${combination.group_id}`" 
                          v-model="selectedCombinationIds" 
                          :value="combination.group_id"
                        >
                      </td>
                      <td>
                        <label class="form-check-label small" :for="`combination-${combination.group_id}`">
                          {{ combination.group_name }}
                        </label>
                      </td>
                      <td class="text-end fw-bold">{{ combination.score }}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <div class="alert alert-warning mt-2 p-2 small" v-if="!selectedCombinationIds.length && submitted">
                <i class="bi bi-exclamation-triangle me-1"></i>
                Vui lòng chọn ít nhất một tổ hợp xét tuyển
              </div>
              
              <!-- Chọn trường (xác định khu vực ưu tiên) -->
              <h3 class="section-title h6 mt-3">Chọn trường</h3>
              <div class="school-selection-container p-2 p-md-3">
                <div class="row g-2">
                  <div class="col-12">
                    <label for="city" class="form-label small mb-1">Tỉnh/Thành phố</label>
                    <select 
                      v-model="cityId" 
                      class="form-select form-select-sm" 
                      id="city" 
                      @change="loadDistricts">
                      <option value="">-- Chọn Tỉnh/Thành phố --</option>
                      <option v-for="city in cities" :key="city.id" :value="city.id">
                        {{ city.name }}
                      </option>
                    </select>
                  </div>
                  <div class="col-12 col-md-6">
                    <label for="district" class="form-label small mb-1">Quận/Huyện</label>
                    <select 
                      v-model="districtId" 
                      class="form-select form-select-sm" 
                      id="district" 
                      @change="loadSchools" 
                      :disabled="!districts.length">
                      <option value="">-- Chọn Quận/Huyện --</option>
                      <option v-for="district in districts" :key="district.id" :value="district.id">
                        {{ district.name }}
                      </option>
                    </select>
                  </div>
                  <div class="col-12 col-md-6">
                    <label for="school" class="form-label small mb-1">Trường THPT</label>
                    <select 
                      v-model="schoolId" 
                      class="form-select form-select-sm" 
                      id="school" 
                      :disabled="!schools.length">
                      <option value="">-- Chọn Trường THPT --</option>
                      <option v-for="school in schools" :key="school.id" :value="school.id">
                        {{ school.name }}
                      </option>
                    </select>
                  </div>
                </div>
                <div class="mt-2 text-center" v-if="selectedSchoolPriority">
                  <p class="small fw-bold mb-0">Khu vực ưu tiên: {{ selectedSchoolPriority }}</p>
                </div>
              </div>


              <!-- Chọn đối tượng ưu tiên -->
              <div class="mb-3 mt-3">
                <h3 class="section-title h6">Chọn Ưu tiên đối tượng</h3>
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
              
              <div class="d-flex justify-content-between mt-3">
                <button type="button" class="btn btn-sm btn-outline-secondary" @click="goBackToScores">
                  <i class="bi bi-arrow-left"></i> Quay lại
                </button>
                <button type="submit" class="btn btn-sm btn-calculate">
                  <i class="bi bi-calculator"></i> Tính điểm ưu tiên
                </button>
              </div>
            </form>
          </div>
          
          <!-- Hiển thị kết quả sau bước 1: Tính điểm -->
          <div class="loading-indicator" v-if="loading">
            <div class="spinner-border spinner-border-sm text-primary" role="status">
              <span class="visually-hidden">Đang tải...</span>
            </div>
            <p class="small mb-0 mt-1">Đang tính toán...</p>
          </div>
          
          <div class="initial-results mt-3" v-if="initialCombinations.length > 0 && !showPriorityStep">
            <h3 class="h5 text-center mb-2">Kết quả tính điểm tổ hợp</h3>
            
            <div class="table-responsive">
              <table class="table table-sm table-striped">
                <thead>
                  <tr class="bg-light">
                    <th>STT</th>
                    <th>Tổ hợp</th>
                    <th>Môn thi</th>
                    <th>Điểm</th>
                    <th>Hệ số</th>
                    <th>Điểm tổ hợp</th>
                  </tr>
                </thead>
                <tbody>
                  <template v-for="(combination, index) in initialCombinations" :key="`combination-${combination.group_id}`">
                    <tr class="combination-row table-primary">
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
            
            <!-- Công cụ tạo URL chia sẻ -->
            <div class="url-generator mt-3">
              <hr>
              <h4 class="h6 text-center">Chia sẻ kết quả</h4>
              
              <div class="d-flex justify-content-center">
                <button class="btn btn-sm btn-outline-info me-2" @click="generateShareableUrl">
                  <i class="bi bi-link-45deg"></i> Tạo liên kết chia sẻ
                </button>
                
                <button v-if="shareableUrl" class="btn btn-sm btn-outline-success" @click="copyUrlToClipboard">
                  <i class="bi bi-clipboard"></i> Sao chép liên kết
                </button>
              </div>
              
              <div v-if="shareableUrl" class="mt-2 url-display p-2">
                <small class="text-muted">Liên kết chia sẻ:</small>
                <div class="input-group input-group-sm">
                  <input type="text" class="form-control form-control-sm" readonly v-model="shareableUrl" />
                  <button class="btn btn-sm btn-outline-secondary" @click="copyUrlToClipboard">
                    <i class="bi bi-clipboard"></i>
                  </button>
                </div>
                <small class="text-success" v-if="urlCopied">Đã sao chép vào bộ nhớ tạm!</small>
              </div>
            </div>
            
            <div class="text-center mt-3">
              <button class="btn btn-sm btn-primary" @click="proceedToPriorityStep">
                <i class="bi bi-arrow-right-circle"></i> Tính điểm ưu tiên
              </button>
            </div>
          </div>
          
          <!-- Hiển thị kết quả cuối cùng với điểm ưu tiên -->
          <div class="final-results-container mt-3" v-if="finalResults.length > 0">
            <h3 class="h5 text-center mb-2">Kết quả tính điểm xét tuyển</h3>
            
            <template v-for="(result, resultIndex) in finalResults" :key="`result-${resultIndex}`">
              <div class="combination-result">
                <h4 class="combination-name h6 bg-light p-2">{{ result.group_name }}</h4>
                
                <!-- Chi tiết điểm từng môn trong tổ hợp -->
                <div class="table-responsive">
                  <table class="table table-sm table-bordered">
                    <thead>
                      <tr class="bg-light">
                        <th>Môn thi</th>
                        <th class="text-center">Điểm</th>
                        <th class="text-center">Hệ số</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="(subject, subjectIndex) in result.subjects" :key="`${resultIndex}-${subjectIndex}`">
                        <td>{{ subject.name }}</td>
                        <td class="text-center">{{ subject.score.toFixed(2) }}</td>
                        <td class="text-center">{{ subject.coefficient }}</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
                
                <!-- Điểm tổ hợp và điểm ưu tiên -->
                <div class="point-summary my-2">
                  <div class="row g-2">
                    <div class="col-4">
                      <div class="point-card original p-2">
                        <div class="point-title small">Điểm tổ hợp gốc</div>
                        <div class="point-value">{{ result.score }}</div>
                        <div class="point-description small">(Thang 30)</div>
                      </div>
                    </div>
                    <div class="col-4">
                      <div class="point-card priority p-2">
                        <div class="point-title small">Điểm ưu tiên</div>
                        <div class="point-value">{{ result.priority_points.convert_priority }}</div>
                        <div class="point-description small">(Đã quy đổi)</div>
                      </div>
                    </div>
                    <div class="col-4">
                      <div class="point-card total p-2">
                        <div class="point-title small">Tổng điểm</div>
                        <div class="point-value">{{ result.priority_points.total_point }}</div>
                        <div class="point-description small">(Gốc + ưu tiên)</div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <hr v-if="resultIndex < finalResults.length - 1" class="my-2">
            </template>
            
            <!-- Reset button for starting over -->
            <div class="text-center mt-3">
              <button class="btn btn-sm btn-secondary" @click="resetCalculator">
                <i class="bi bi-arrow-counterclockwise"></i> Tính toán lại
              </button>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
// Script section with updated URL processing
import { ref, reactive, computed, onMounted, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import CalculateScoreController from '@/controllers/CalculateScoreController';

export default {
  name: 'CalculateScoreTHPT',
  setup() {
    const route = useRoute();
    const router = useRouter();
    
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
    
    // URL sharing variables
    const shareableUrl = ref('');
    const urlCopied = ref(false);
    const urlParseError = ref('');
    
    // Computed properties
    const selectedSchoolPriority = computed(() => {
      if (schools.value.length && schoolId.value) {
        const selected = schools.value.find(s => s.id == schoolId.value);
        return selected ? selected.priority_area : '';
      }
      return '';
    });
    
    // Normalize subject name for URL processing
    const normalizeSubjectName = (name) => {
      return name.toLowerCase().trim();
    };
    
    // Find a subject match based on normalized name
    const findSubjectMatch = (normalizedName) => {
      return subjects.value.find(subject => 
        normalizeSubjectName(subject.name) === normalizedName
      );
    };
    
    // Process URL parameters for automatic score calculation
    const processUrlParams = async () => {
      try {
        // Đảm bảo danh sách môn học đã được tải
        if (subjects.value.length === 0) {
          await loadSubjects();
        }
        
        // Kiểm tra xem có query params hay không
        const query = route.query;
        if (!query || Object.keys(query).length === 0) return;
        
        // Xử lý danh sách môn học và điểm từ URL
        const urlSubjects = [];
        const invalidSubjects = [];
        
        for (const key of Object.keys(query)) {
          // Kiểm tra xem key có phải là định dạng s_ID không
          const isSubjectId = key.startsWith('s_');
          let subjectId, matchedSubject;
          
          if (isSubjectId) {
            // Trích xuất ID từ key (s_123 -> 123)
            subjectId = key.substring(2);
            matchedSubject = subjects.value.find(s => s.id.toString() === subjectId);
          } else {
            // Trường hợp URL cũ sử dụng tên môn học
            const normalizedKey = normalizeSubjectName(key);
            matchedSubject = findSubjectMatch(normalizedKey);
          }
          
          if (matchedSubject) {
            // Xử lý điểm
            const score = parseFloat(query[key]);
            
            if (!isNaN(score) && score >= 0 && score <= 10) {
              // Làm tròn đến 0.05
              const roundedScore = Math.round(score * 20) / 20;
              
              urlSubjects.push({
                selectedSubject: matchedSubject,
                subject_id: matchedSubject.id,
                subject_name: matchedSubject.name,
                scores: [roundedScore.toFixed(2)]
              });
            } else {
              invalidSubjects.push(`${matchedSubject.name} (điểm không hợp lệ: ${query[key]})`);
            }
          } else if (!isSubjectId) {
            // Chỉ báo lỗi cho trường hợp không phải định dạng s_ID
            invalidSubjects.push(key);
          }
        }
        
        // Hiển thị thông báo về môn học không hợp lệ
        if (invalidSubjects.length > 0) {
          urlParseError.value = `Một số môn học không được nhận dạng hoặc có điểm không hợp lệ: ${invalidSubjects.join(', ')}`;
        }
        
        // Nếu có ít nhất một môn hợp lệ
        if (urlSubjects.length > 0) {
          subjectScores.value = urlSubjects;
          // Tự động tính điểm
          setTimeout(() => {
            calculateInitialScores();
          }, 500);
        }
        
      } catch (err) {
        console.error('Error processing URL parameters:', err);
        urlParseError.value = 'Có lỗi xảy ra khi xử lý thông tin từ URL.';
      }
    };
    
    // Generate shareable URL
    const generateShareableUrl = () => {
      try {
        // Kiểm tra trước khi tạo URL
        if (!subjectScores.value.length || !subjectScores.value[0].selectedSubject) {
          return alert('Chưa có đủ thông tin điểm để tạo liên kết!');
        }
        
        // Tạo base URL
        const baseUrl = window.location.origin + window.location.pathname;
        
        // Tạo query params
        const params = new URLSearchParams();
        
        // Thêm điểm cho từng môn - SỬ DỤNG ID THẾ CHO TÊN MÔN
        subjectScores.value.forEach(subject => {
          if (subject.selectedSubject && subject.scores[0] !== '') {
            // Sử dụng subject_id thay vì subject_name để tránh vấn đề encoding
            params.append(`s_${subject.subject_id}`, subject.scores[0]);
          }
        });
        
        // Tạo URL đầy đủ
        shareableUrl.value = `${baseUrl}?${params.toString()}`;
        urlCopied.value = false;
      } catch (error) {
        console.error('Error generating URL:', error);
        alert('Có lỗi xảy ra khi tạo liên kết chia sẻ.');
      }
    };
    
    // Copy URL to clipboard
    const copyUrlToClipboard = async () => {
      try {
        await navigator.clipboard.writeText(shareableUrl.value);
        urlCopied.value = true;
        
        // Auto-hide message after 3 seconds
        setTimeout(() => {
          urlCopied.value = false;
        }, 3000);
      } catch (err) {
        console.error('Failed to copy URL:', err);
        alert('Không thể sao chép liên kết. Vui lòng thử lại.');
      }
    };
    
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
    
    // Format exam score to the nearest 0.05
    const formatExamScore = (index) => {
      const scoreValue = subjectScores.value[index].scores[0];
      if (scoreValue !== '' && !isNaN(parseFloat(scoreValue))) {
        // Round to nearest 0.05
        const roundedValue = Math.round(parseFloat(scoreValue) * 20) / 20;
        // Limit to at most 2 decimal places
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
      
      // Check score format and round
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
      
      // Refresh bootstrap-select after step change
      setTimeout(() => {
        if ($('.selectpicker').length) {
          $('.selectpicker').selectpicker('refresh');
        }
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
      shareableUrl.value = '';
      urlParseError.value = '';
    };
    
    // Init
    onMounted(async () => {
      loading.value = true;
      try {
        await Promise.all([
          loadSubjects(),
          loadCities()
        ]);
        
        // Process URL params after subjects are loaded
        await processUrlParams();
        
        // Initialize bootstrap-select if needed
        setTimeout(() => {
          if ($('.selectpicker').length) {
            $('.selectpicker').selectpicker();
          }
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
      
      // URL sharing
      shareableUrl,
      urlCopied,
      urlParseError,
      
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
      resetCalculator,
      generateShareableUrl,
      copyUrlToClipboard
    };
  }
}
</script>

<style scoped>
/* Hero Section - thu gọn */
.hero-section {
  background: linear-gradient(135deg, rgba(14, 76, 146, 0.95), rgba(31, 64, 104, 0.95));
  background-size: cover;
  background-position: center;
  padding: 1.5rem 0;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  border-bottom: 3px solid #3a7bd5;
}

.hero-section h1 {
  color: #ffffff;
  font-size: 1.5rem;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
  margin-bottom: 0.25rem;
  letter-spacing: 0.5px;
}

.hero-section p {
  color: #ffffff;
  font-size: 0.9rem;
  max-width: 800px;
  margin: 0 auto;
  opacity: 0.9;
}

/* Card styling - thu gọn */
.card {
  background-color: #ffffff;
  border: none;
  border-radius: 0.5rem;
  overflow: hidden;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
}

.card-header {
  background-color: #0B2942 !important;
  color: #ffffff !important;
  border: none;
}

/* Section titles - thu gọn */
.section-title {
  color: #0B2942;
  text-align: center;
  margin-bottom: 0.75rem;
  font-weight: 600;
  position: relative;
}

.section-title:after {
  content: "";
  display: block;
  width: 40px;
  height: 2px;
  background: #4da0ff;
  margin: 0.3rem auto 0.5rem;
  border-radius: 1px;
}

/* Step indicator - thu gọn */
.step-indicator {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1rem;
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
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background-color: #0B2942;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 0.8rem;
  margin-bottom: 0.25rem;
}

.step-title {
  font-weight: 600;
  color: #0B2942;
}

.step-line {
  height: 2px;
  background-color: #0B2942;
  flex-grow: 1;
  margin: 0 0.75rem;
  position: relative;
  top: -5px;
}

/* Form controls - thu gọn */
.form-control, .form-select {
  padding: 0.25rem 0.5rem;
  font-size: 0.875rem;
}

.form-control:focus, .form-select:focus {
  box-shadow: 0 0 0 0.15rem rgba(13, 71, 161, 0.25);
}

/* Small text notes */
.form-text {
  font-size: 0.7rem;
  margin-top: 0.1rem;
}

/* Nút tính điểm */
.btn-calculate {
  background: linear-gradient(135deg, #3a7bd5, #0B2942);
  color: #ffffff;
  border: none;
  padding: 0.35rem 1rem;
  transition: all 0.2s;
}

.btn-calculate:hover {
  background: linear-gradient(135deg, #4a8bf5, #1a3952);
  transform: translateY(-1px);
}

/* School selection */
.school-selection-container {
  background-color: #f5f9ff;
  border-radius: 0.5rem;
  border: 1px solid #d0e1f9;
}

/* Table styles */
.table {
  font-size: 0.8rem;
  margin-bottom: 0.5rem;
}

.table td, .table th {
  padding: 0.3rem 0.5rem;
  vertical-align: middle;
}

/* Results */
.initial-results, .final-results-container {
  background-color: #f8f9fa;
  border-radius: 0.5rem;
  padding: 0.75rem;
  border: 1px solid #e9ecef;
}

/* Point cards */
.point-card {
  background-color: #f5f9ff;
  border-radius: 0.5rem;
  text-align: center;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.point-title {
  font-weight: 600;
  color: #495057;
}

.point-value {
  font-size: 1.25rem;
  font-weight: 700;
  color: #0B2942;
  line-height: 1;
  margin: 0.2rem 0;
}

.point-description {
  color: #6c757d;
  font-size: 0.7rem;
}

.point-card.original {
  background-color: #e8f5ff;
}

.point-card.priority {
  background-color: #e1f5ea;
}

.point-card.total {
  background-color: #fff8e1;
}

.point-card.original .point-value {
  color: #0d47a1;
}

.point-card.priority .point-value {
  color: #388e3c;
}

.point-card.total .point-value {
  color: #f57c00;
}

/* URL Display */
.url-display {
  background-color: #f8f9fa;
  border-radius: 0.25rem;
  border: 1px solid #dee2e6;
  margin-top: 0.5rem;
}

/* Accessibility */
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
@media (min-width: 768px) {
  .hero-section h1 {
    font-size: 1.75rem;
  }
  
  .hero-section p {
    font-size: 1rem;
  }
  
  .form-control, .form-select {
    font-size: 0.9rem;
  }
}
</style>
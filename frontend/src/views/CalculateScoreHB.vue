<template>
  <div>
    <!-- Hero Section - Đã thu gọn -->
    <header class="hero-section py-3 py-md-4 text-center text-white">
      <div class="container">
        <h1 class="fw-bold mb-1">Tính Điểm Xét Tuyển Học Bạ</h1>
        <p>Trường Đại học Bách Khoa - Đại học Đà Nẵng</p>
      </div>
    </header>

    <!-- Main Content - Đã thu gọn -->
    <main class="container my-3 my-md-4">
      <div class="card shadow-sm rounded">
        <div class="card-header text-white text-center py-2">
          <h2 class="h5 mb-0">Công cụ tính điểm xét tuyển học bạ THPT</h2>
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

          <!-- Bước 1: Nhập điểm - Thiết kế mới theo dạng hàng -->
          <div v-if="!showPriorityStep">
            <form @submit.prevent="calculateInitialScores">
              <!-- Chọn loại điểm học bạ -->
              <div class="option-selector mb-3">
                <h3 class="section-title h6">Chọn loại điểm học bạ</h3>
                <div class="d-flex justify-content-center">
                  <div class="form-check form-check-inline me-3">
                    <input class="form-check-input" 
                          type="radio" 
                          name="scoreOption" 
                          id="semesterOption" 
                          value="semester" 
                          v-model="scoreOption">
                    <label class="form-check-label small" for="semesterOption">Điểm 6 học kỳ</label>
                  </div>
                  <div class="form-check form-check-inline">
                    <input class="form-check-input" 
                          type="radio" 
                          name="scoreOption" 
                          id="yearOption" 
                          value="year" 
                          v-model="scoreOption">
                    <label class="form-check-label small" for="yearOption">Điểm 3 năm học</label>
                  </div>
                </div>
              </div>

              <!-- Nhập điểm môn học - Thiết kế dạng bảng với một môn trên một hàng -->
              <div class="subject-list">
                <h3 class="section-title h6">Nhập điểm các môn học</h3>
                
                <div class="table-responsive">
                  <table class="table table-sm table-bordered">
                    <thead class="bg-light">
                      <tr>
                        <th style="width: 30%">Môn học</th>
                        <th class="text-center" style="width: 65%">
                          <div class="scores-header-container">
                            <template v-if="scoreOption === 'semester'">
                              <div class="score-header">HK1-Lớp 10</div>
                              <div class="score-header">HK2-Lớp 10</div>
                              <div class="score-header">HK1-Lớp 11</div>
                              <div class="score-header">HK2-Lớp 11</div>
                              <div class="score-header">HK1-Lớp 12</div>
                              <div class="score-header">HK2-Lớp 12</div>
                            </template>
                            <template v-else>
                              <div class="score-header">Lớp 10</div>
                              <div class="score-header">Lớp 11</div>
                              <div class="score-header">Lớp 12</div>
                            </template>
                          </div>
                        </th>
                        <th style="width: 5%" class="text-center">
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
                                aria-label="Chọn môn học">
                            <option value="">-- Chọn môn học --</option>
                            <option v-for="sub in getAvailableSubjectsForRow(index)" 
                                  :key="sub.id" 
                                  :value="sub">
                              {{ sub.name }}
                            </option>
                          </select>
                        </td>
                        <td>
                          <div class="scores-container-wrapper">
                            <div class="scores-container">
                              <template v-if="scoreOption === 'semester'">
                                <div class="score-input-group" v-for="(_, scoreIdx) in 6" :key="`${index}-${scoreIdx}`">
                                  <input type="number" 
                                        class="form-control form-control-sm" 
                                        v-model="subject.scores[scoreIdx]" 
                                        min="0" 
                                        max="10" 
                                        step="0.1"
                                        :aria-label="`Điểm HK${scoreIdx % 2 + 1} lớp ${Math.floor(scoreIdx/2) + 10}`">
                                </div>
                              </template>
                              <template v-else>
                                <div class="score-input-group" v-for="(_, scoreIdx) in 3" :key="`${index}-${scoreIdx}`">
                                  <input type="number" 
                                        class="form-control form-control-sm" 
                                        v-model="subject.scores[scoreIdx]" 
                                        min="0" 
                                        max="10" 
                                        step="0.1"
                                        :aria-label="`Điểm lớp ${scoreIdx + 10}`">
                                </div>
                              </template>
                            </div>
                          </div>
                        </td>
                        <td class="text-center">
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
                    <i class="bi bi-plus-circle"></i> Thêm môn học
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
              <div class="combination-selection">
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
  <div v-if="priorityObject !== '0'" class="mt-2 priority-detail py-2 px-3">
    <div v-if="priorityObject === 'ĐT01'" class="small">
      <strong>Đối tượng 01:</strong> Công dân Việt Nam là người dân tộc thiểu số có nơi thường trú trong thời gian học THPT hoặc trung cấp trên 18 tháng tại Khu vực 1.
    </div>
    <div v-else-if="priorityObject === 'ĐT02'" class="small">
      <strong>Đối tượng 02:</strong> Công nhân trực tiếp sản xuất đã làm việc liên tục 5 năm trở lên, trong đó có ít nhất 2 năm là chiến sĩ thi đua được cấp tỉnh trở lên công nhận và cấp bằng khen.
    </div>
    <div v-else-if="priorityObject === 'ĐT03'" class="small">
      <strong>Đối tượng 03a:</strong> Thương binh, bệnh binh, người có 'Giấy chứng nhận người được hưởng chính sách như thương binh'.<br>
      <strong>Đối tượng 03b:</strong> Quân nhân; sĩ quan, hạ sĩ quan, chiến sĩ nghĩa vụ trong Công an nhân dân tại ngũ được cử đi học có thời gian phục vụ từ 12 tháng trở lên tại Khu vực 1.<br>
      <strong>Đối tượng 03c:</strong> Quân nhân; sĩ quan, hạ sĩ quan, chiến sĩ nghĩa vụ trong Công an nhân dân tại ngũ được cử đi học có thời gian phục vụ từ 18 tháng trở lên.<br>
      <strong>Đối tượng 03d:</strong> Quân nhân; sĩ quan, hạ sĩ quan, chiến sĩ nghĩa vụ trong Công an nhân dân đã xuất ngũ, được công nhận hoàn thành nghĩa vụ phục vụ tại ngũ theo quy định.
    </div>
    <div v-else-if="priorityObject === 'ĐT04'" class="small">
      <strong>Đối tượng 04a:</strong> Thân nhân liệt sĩ.<br>
      <strong>Đối tượng 04b:</strong> Con thương binh, con bệnh binh, con của người được hưởng chính sách như thương binh bị suy giảm khả năng lao động từ 81% trở lên.<br>
      <strong>Đối tượng 04c:</strong> Con của người hoạt động kháng chiến bị nhiễm chất độc hóa học bị suy giảm khả năng lao động 81% trở lên.<br>
      <strong>Đối tượng 04d:</strong> Con của Anh hùng Lực lượng vũ trang nhân dân; con của Anh hùng Lao động trong thời kỳ kháng chiến.<br>
      <strong>Đối tượng 04đ:</strong> Con của người hoạt động kháng chiến bị dị dạng, dị tật do hậu quả của chất độc hóa học đang hưởng trợ cấp hàng tháng.
    </div>
    <div v-else-if="priorityObject === 'ĐT05'" class="small">
      <strong>Đối tượng 05a:</strong> Thanh niên xung phong tập trung được cử đi học.<br>
      <strong>Đối tượng 05b:</strong> Quân nhân; sĩ quan, hạ sĩ quan, chiến sĩ nghĩa vụ trong Công an nhân dân tại ngũ được cử đi học có thời gian phục vụ dưới 12 tháng ở Khu vực 1 và dưới 18 tháng ở khu vực khác.<br>
      <strong>Đối tượng 05c:</strong> Chỉ huy trưởng, Chỉ huy phó ban chỉ huy quân sự xã, phường, thị trấn; Thôn đội trưởng, Trung đội trưởng Dân quân tự vệ nòng cốt, Dân quân tự vệ đã hoàn thành nghĩa vụ tham gia Dân quân tự vệ nòng cốt từ 12 tháng trở lên, dự thi vào ngành Quân sự cơ sở.
    </div>
    <div v-else-if="priorityObject === 'ĐT06'" class="small">
      <strong>Đối tượng 06a:</strong> Công dân Việt Nam là người dân tộc thiểu số có nơi thường trú ở ngoài khu vực đã quy định thuộc đối tượng 01.<br>
      <strong>Đối tượng 06b:</strong> Con thương binh, con bệnh binh, con của người được hưởng chính sách như thương binh bị suy giảm khả năng lao động dưới 81%.<br>
      <strong>Đối tượng 06c:</strong> Con của người hoạt động kháng chiến bị nhiễm chất độc hóa học có tỷ lệ suy giảm khả năng lao động dưới 81%.
    </div>
    <div v-else-if="priorityObject === 'ĐT07'" class="small">
      <strong>Đối tượng 07a:</strong> Người khuyết tật nặng có giấy xác nhận khuyết tật của cơ quan có thẩm quyền cấp theo quy định tại Thông tư liên tịch số 37/2012/TTLT‑BLĐTBXH‑BYT‑BTC‑BGDĐT ngày 28 tháng 12 năm 2012.<br>
      <strong>Đối tượng 07b:</strong> Người lao động ưu tú thuộc tất cả thành phần kinh tế từ cấp tỉnh, cấp bộ trở lên được công nhận danh hiệu thợ giỏi, nghệ nhân, được cấp bằng hoặc huy hiệu Lao động sáng tạo.<br>
      <strong>Đối tượng 07c:</strong> Giáo viên đã giảng dạy đủ 3 năm trở lên dự tuyển vào các ngành đào tạo giáo viên.<br>
      <strong>Đối tượng 07d:</strong> Y tá, dược tá, hộ lý, y sĩ, điều dưỡng viên, hộ sinh viên, kỹ thuật viên, người có bằng trung cấp Dược đã công tác đủ 3 năm trở lên dự tuyển vào đúng ngành tốt nghiệp thuộc lĩnh vực sức khỏe.
    </div>
  </div>
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
          <div class="initial-results mt-3" v-if="initialCombinations.length > 0 && !showPriorityStep">
            <h3 class="h5 text-center mb-2">Kết quả tính điểm tổ hợp</h3>
            
            <div class="table-responsive">
              <table class="table table-sm table-striped">
                <thead>
                  <tr class="bg-light">
                    <th>STT</th>
                    <th>Tổ hợp</th>
                    <th>Môn học</th>
                    <th>Điểm TB</th>
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
                        <th>Môn học</th>
                        <th class="text-center">Điểm TB</th>
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
              <!-- Thêm nút gợi ý ngành học dựa trên kết quả -->
                <div class="suggestion-actions mt-2 text-center">
                  <button 
                    class="btn btn-sm btn-outline-info" 
                    @click="getMajorSuggestions(result)"
                    :disabled="suggestionsLoading === result.group_id"
                  >
                    <i class="bi bi-lightbulb"></i> 
                    <span v-if="suggestionsLoading !== result.group_id">Gợi ý ngành học phù hợp</span>
                    <span v-else>Đang tải gợi ý...</span>
                  </button>
                </div>

                <!-- Hiển thị kết quả gợi ý nếu có -->
                <div v-if="suggestions[result.group_id]" class="suggestions-container mt-3">
                  <div class="card">
                    <div class="card-header bg-info bg-opacity-10 py-2">
                      <h5 class="card-title mb-0 h6">
                        <i class="bi bi-lightbulb-fill text-warning me-1"></i>
                        Gợi ý ngành học phù hợp với {{ result.group_name }} - Điểm {{ result.priority_points.total_point }}
                      </h5>
                    </div>
                    <div class="card-body p-2">
                      <div v-for="(category, catIndex) in suggestions[result.group_id]" :key="`cat-${result.group_id}-${catIndex}`" class="suggestion-category mb-3">
                        <div class="category-title fw-bold mb-2" v-html="category.title"></div>
                        
                        <div class="table-responsive">
                          <table class="table table-sm table-hover">
                            <thead>
                              <tr class="bg-light">
                                <th style="width: 5%">STT</th>
                                <th>Tên ngành</th>
                                <th style="width: 20%" class="text-center">Chi tiết</th>
                              </tr>
                            </thead>
                            <tbody>
                              <tr v-for="(major, majorIdx) in category.majors" :key="`major-${result.group_id}-${catIndex}-${majorIdx}`">
                                <td>{{ majorIdx + 1 }}</td>
                                <td>{{ major.name }}</td>
                                <td class="text-center">
                                  <a :href="major.link" target="_blank" class="btn btn-sm btn-link">Tại đây</a>
                                </td>
                              </tr>
                            </tbody>
                          </table>
                        </div>
                      </div>
                      
                      <div class="suggestion-footer text-muted small fst-italic" v-if="suggestions[result.group_id].length > 0">
                        <p v-html="suggestions[result.group_id][suggestions[result.group_id].length - 1]?.note"></p>
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
// Cập nhật phần script, giữ nguyên phần template và style
import { ref, reactive, computed, onMounted, watch } from 'vue';
import CalculateScoreController from '@/controllers/CalculateScoreController';
import ChatRasaController from '@/controllers/ChatRasaController';

export default {
  name: 'CalculateScoreHB',
  setup() {
    // Form state
    const scoreOption = ref('semester');
    const allSubjects = ref([]); // Danh sách tất cả các môn học từ API
    const subjects = ref([]); // Danh sách môn học có thể chọn
    const subjectScores = ref([
      {
        selectedSubject: '',
        subject_id: null,
        subject_name: '',
        scores: scoreOption.value === 'semester' ? ['', '', '', '', '', ''] : ['', '', '']
      }
    ]);
    
    // School selection và các state khác - giữ nguyên như code gốc
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

    // Gợi ý ngành học
    const suggestions = ref({}); // Lưu trữ gợi ý cho từng tổ hợp: { group_id: [{title, majors}] }
    const suggestionsLoading = ref(null); // ID của tổ hợp đang tải gợi ý
    
    // Computed property cho danh sách môn học có thể chọn
    const availableSubjects = computed(() => {
      // Lấy danh sách ID các môn học đã chọn
      const selectedSubjectIds = subjectScores.value
        .filter(item => item.selectedSubject && item.subject_id)
        .map(item => item.subject_id);
      
      // Trả về danh sách các môn học chưa được chọn
      return allSubjects.value.filter(subject => !selectedSubjectIds.includes(subject.id));
    });
    
    // Computed properties
    const selectedSchoolPriority = computed(() => {
      if (schools.value.length && schoolId.value) {
        const selected = schools.value.find(s => s.id == schoolId.value);
        return selected ? selected.priority_area : '';
      }
      return '';
    });
    
    // Watch for changes in score option
    watch(scoreOption, (newOption) => {
      subjectScores.value.forEach(subject => {
        subject.scores = newOption === 'semester' ? ['', '', '', '', '', ''] : ['', '', ''];
      });
    });
    
    // Methods
    const addSubject = () => {
      subjectScores.value.push({
        selectedSubject: '',
        subject_id: null,
        subject_name: '',
        scores: scoreOption.value === 'semester' ? ['', '', '', '', '', ''] : ['', '', '']
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
    
    const getAvailableSubjectsForRow = (currentIndex) => {
      // Lấy danh sách ID các môn học đã chọn, ngoại trừ môn đã chọn tại row hiện tại
      const selectedSubjectIds = subjectScores.value
        .filter((item, idx) => idx !== currentIndex && item.selectedSubject && item.subject_id)
        .map(item => item.subject_id);
      
      // Trả về danh sách các môn học chưa được chọn + môn học đang chọn tại row hiện tại
      const currentSubjectId = subjectScores.value[currentIndex].subject_id;
      
      if (currentSubjectId) {
        // Nếu row hiện tại đã chọn môn, thêm môn này vào danh sách có thể chọn
        const currentSelectedSubject = allSubjects.value.find(s => s.id === currentSubjectId);
        return allSubjects.value.filter(subject => 
          !selectedSubjectIds.includes(subject.id) || subject.id === currentSubjectId
        );
      } else {
        // Nếu row hiện tại chưa chọn môn, chỉ hiển thị các môn chưa được chọn
        return allSubjects.value.filter(subject => !selectedSubjectIds.includes(subject.id));
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
        allSubjects.value = await CalculateScoreController.getSubjects();
      } catch (err) {
        error.value = 'Không thể tải danh sách môn học. Vui lòng thử lại sau.';
      }
    };
    
    const validateScoreForm = () => {
      error.value = '';
      
      // Check if subjects are selected and have scores
      const invalidSubjects = subjectScores.value.filter(subject => !subject.selectedSubject);
      if (invalidSubjects.length > 0) {
        error.value = 'Vui lòng chọn đầy đủ các môn học';
        return false;
      }
      
      return true;
    };
    
    // Các methods còn lại giữ nguyên như code gốc
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
          scores: subject.scores.map(score => score === '' ? 0 : parseFloat(score))
        }));
        
        // Calculate scores
        const scoreResult = await CalculateScoreController.calculateHBScores(
          formattedData, 
          scoreOption.value
        );
        
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
          scores: scoreOption.value === 'semester' ? ['', '', '', '', '', ''] : ['', '', '']
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
      suggestions.value = {};
    };
    
    const getMajorSuggestions = async (result) => {
      const groupId = result.group_id;
      
      if (suggestionsLoading.value === groupId) {
        return; // Already loading suggestions for this combination
      }
      
      try {
        suggestionsLoading.value = groupId;
        
        // Get subject names
        const subjectNames = result.subjects.map(s => s.name);
        const score = result.priority_points.total_point;
        const method_key = false;
        
        // Use the specialized function for getting suggestions
        const processedSuggestions = await ChatRasaController.getMajorSuggestions(subjectNames, score, method_key);
        
        // Check if we got valid suggestions
        if (processedSuggestions && processedSuggestions.length > 0) {
          suggestions.value = {
            ...suggestions.value,
            [groupId]: processedSuggestions
          };
        } else {
          throw new Error('Không nhận được gợi ý phù hợp');
        }
        
      } catch (err) {
        console.error('Error getting major suggestions:', err);
        alert('Có lỗi xảy ra khi lấy gợi ý ngành học: ' + (err.message || 'Vui lòng thử lại sau.'));
      } finally {
        suggestionsLoading.value = null;
      }
    };
    // Init
    onMounted(async () => {
      loading.value = true;
      try {
        await Promise.all([
          loadSubjects(),
          loadCities()
        ]);
        
        // Khởi tạo bootstrap-select nếu cần
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
      scoreOption,
      allSubjects, // Thêm allSubjects vào return
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
      availableSubjects, // Thêm computed property

      // Suggestions
      suggestions,
      suggestionsLoading,
      
      // Methods
      addSubject,
      removeSubject,
      updateSubjectId,
      getAvailableSubjectsForRow, // Thêm method mới
      loadDistricts,
      loadSchools,
      calculateInitialScores,
      proceedToPriorityStep,
      goBackToScores,
      calculatePriorityScores,
      resetCalculator,

      getAvailableSubjectsForRow, // Thêm hàm lấy danh sách môn học khả dụng
      getMajorSuggestions // Thêm hàm lấy gợi ý ngành học
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

/* Nhập điểm môn học - thiết kế mới */
.scores-header-container {
  display: flex;
  overflow-x: auto;
  padding-bottom: 2px;
}

.score-header {
  flex: 0 0 80px;
  font-size: 0.75rem;
  font-weight: bold;
  text-align: center;
  padding: 0 0.25rem;
}

.scores-container-wrapper {
  overflow-x: auto;
  padding-bottom: 2px;
}

.scores-container {
  display: flex;
  min-width: max-content;
}

.score-input-group {
  flex: 0 0 80px;
  padding: 0 0.25rem;
}

/* Form controls - thu gọn */
.form-control, .form-select {
  padding: 0.25rem 0.5rem;
  font-size: 0.875rem;
}

.form-control:focus, .form-select:focus {
  box-shadow: 0 0 0 0.15rem rgba(13, 71, 161, 0.25);
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

/* Combination selector */
.combination-selection {
  margin-bottom: 1rem;
}

.combination-name {
  font-weight: 600;
  color: #0B2942;
  font-size: 0.9rem;
  margin-bottom: 0.25rem;
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

/* Table adjustments */
.table {
  font-size: 0.8rem;
  margin-bottom: 0.5rem;
}

.table td, .table th {
  padding: 0.3rem 0.5rem;
  vertical-align: middle;
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

.priority-select {
  font-size: 0.85rem;
}

.priority-detail {
  background-color: #f8f9fa;
  border-radius: 0.25rem;
  border: 1px solid #e9ecef;
  color: #495057;
  margin-top: 0.5rem;
  font-size: 0.8rem;
  line-height: 1.4;
}

.suggestions-container {
  margin-top: 15px;
}

.suggestions-container .card-header {
  background-color: #0B2942 !important;
  color: #ffffff !important;
  border: none;
}

.suggestion-category {
  margin-bottom: 15px;
}

.category-title {
  color: #0b5394;
  padding-bottom: 5px;
  border-bottom: 1px solid #e0e0e0;
}

.suggestion-footer {
  margin-top: 15px;
  padding-top: 10px;
  border-top: 1px solid #e0e0e0;
}

.suggestion-actions {
  margin-top: 10px;
}

/* Thêm thiết kế responsive cho phần gợi ý */
@media (max-width: 768px) {
  .suggestion-category {
    margin-bottom: 10px;
  }
}

/* Nút gợi ý */
.btn-outline-info {
  color: #0dcaf0;
  border-color: #0dcaf0;
}

.btn-outline-info:hover, .btn-outline-info:focus {
  background-color: #0dcaf0;
  color: white;
}

/* Bảng gợi ý */
.suggestion-category .table-hover tbody tr:hover {
  background-color: rgba(13, 202, 240, 0.05);
}

.suggestion-category .table-sm {
  font-size: 0.9rem;
}

.suggestion-category .table-sm th {
  font-weight: 600;
  background-color: rgba(11, 83, 148, 0.05);
}

/* Link chi tiết ngành */
.suggestion-category .btn-link {
  color: #0b5394;
  text-decoration: none;
  padding: 0.1rem 0.5rem;
}

.suggestion-category .btn-link:hover {
  text-decoration: underline;
  background-color: rgba(11, 83, 148, 0.05);
  border-radius: 0.25rem;
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
  
  .point-value {
    font-size: 1.5rem;
  }
}
</style>
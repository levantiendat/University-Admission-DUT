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
                            <option v-for="sub in getAvailableSubjectsForRow(index)" 
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
                                  step="0.01"
                                  @blur="formatExamScore(index)"
                                  placeholder="Nhập điểm (0-10)"
                                  aria-label="Điểm thi">
                          </div>
                          <small class="form-text text-muted small">Làm tròn đến 0.01</small>
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

              <!-- Điểm cộng -->
              <div class="mb-3 mt-3">
                <h3 class="section-title h6 mb-2">Điểm cộng (nếu có)</h3>
                
                <!-- Chọn loại điểm cộng thứ nhất -->
                <div class="mb-3">
                  <label for="bonusType1" class="form-label small mb-1">Loại điểm cộng 1</label>
                  <select 
                    v-model="form.bonusType1" 
                    class="form-select form-select-sm" 
                    id="bonusType1"
                    @change="onBonusType1Change">
                    <option value="">Không có điểm cộng</option>
                    <option value="language">Chứng chỉ ngoại ngữ</option>
                    <option value="direct">Thí sinh xét tuyển thẳng, ưu tiên xét tuyển không sử dụng quyền tuyển thẳng</option>
                  </select>
                </div>

                <!-- Chứng chỉ ngoại ngữ (loại 1) -->
                <div class="mb-3" v-if="form.bonusType1 === 'language'">
                  <div class="row g-2">
                    <div class="col-12 col-md-6">
                      <label for="certificateType1" class="form-label small mb-1">Loại chứng chỉ</label>
                      <select 
                        v-model="form.certificateType1" 
                        class="form-select form-select-sm" 
                        id="certificateType1"
                        @change="onCertificateTypeChange(1)">
                        <option value="">-- Chọn loại chứng chỉ --</option>
                        <option value="KNLNN">KNLNN Việt Nam</option>
                        <option value="Aptis">Khung tham chiếu châu Âu Aptis ESOL</option>
                        <option value="IELTS">IELTS Academic</option>
                        <option value="VSEP">VSEP</option>
                        <option value="PEIC">PEIC</option>
                        <option value="PTE">PTE Academic</option>
                        <option value="Linguaskill">Linguaskill</option>
                        <option value="Cambridge">Cambridge Assessment English</option>
                        <option value="CET">Cambridge English Test</option>
                        <option value="TOEIC">TOEIC</option>
                        <option value="TOEFL">TOEFL iBT</option>
                        <option value="JLPT">JLPT</option>
                      </select>
                    </div>
                    <div class="col-12 col-md-6">
                      <label for="certificateLevel1" class="form-label small mb-1">Trình độ/Điểm số</label>
                      <select v-if="!isTOEIC1 && showTextSelect1" v-model="form.certificateLevel1" class="form-select form-select-sm" id="certificateLevel1">
                        <option value="">-- Chọn trình độ --</option>
                        <option v-for="level in certificateLevels1" :key="level" :value="level">{{ level }}</option>
                      </select>
                      <input v-else-if="!isTOEIC1 && !showTextSelect1" type="number" v-model.number="form.certificateLevel1" class="form-control form-control-sm" id="certificateLevel1" step="0.1" min="0" :max="maxCertificateScore1">
                      
                      <!-- TOEIC specific inputs (4 skills) -->
                      <div v-if="isTOEIC1" class="mt-2">
                        <div class="row g-1 mb-1">
                          <div class="col-6">
                            <div class="input-group input-group-sm">
                              <span class="input-group-text">Nghe</span>
                              <input type="number" v-model.number="form.toeic1.listen" class="form-control form-control-sm" min="0" max="495">
                            </div>
                          </div>
                          <div class="col-6">
                            <div class="input-group input-group-sm">
                              <span class="input-group-text">Đọc</span>
                              <input type="number" v-model.number="form.toeic1.read" class="form-control form-control-sm" min="0" max="495">
                            </div>
                          </div>
                        </div>
                        <div class="row g-1">
                          <div class="col-6">
                            <div class="input-group input-group-sm">
                              <span class="input-group-text">Nói</span>
                              <input type="number" v-model.number="form.toeic1.speak" class="form-control form-control-sm" min="0" max="200">
                            </div>
                          </div>
                          <div class="col-6">
                            <div class="input-group input-group-sm">
                              <span class="input-group-text">Viết</span>
                              <input type="number" v-model.number="form.toeic1.write" class="form-control form-control-sm" min="0" max="200">
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Thí sinh xét tuyển thẳng (loại 1) -->
                <div class="mb-3" v-if="form.bonusType1 === 'direct'">
                  <label for="directAdmissionType1" class="form-label small mb-1">Loại thành tích</label>
                  <select 
                    v-model="form.directAdmissionType1" 
                    class="form-select form-select-sm" 
                    id="directAdmissionType1">
                    <option value="">-- Chọn loại thành tích --</option>
                    <option value="hero">Anh hùng lực lượng lao động, Anh hùng lực lượng vũ trang nhân dân, Chiến sĩ thi đua toàn quốc</option>
                    <option value="national_first">Giải nhất chọn HSG, thi KHKT cấp quốc gia, quốc tế</option>
                    <option value="national_second">Giải nhì chọn HSG, thi KHKT cấp quốc gia, quốc tế</option>
                    <option value="national_third">Giải ba chọn HSG, thi KHKT cấp quốc gia, quốc tế</option>
                  </select>
                </div>

                <!-- Chọn loại điểm cộng thứ hai -->
                <div class="mb-3">
                  <label for="bonusType2" class="form-label small mb-1">Loại điểm cộng 2</label>
                  <select 
                    v-model="form.bonusType2" 
                    class="form-select form-select-sm" 
                    id="bonusType2"
                    @change="onBonusType2Change">
                    <option value="">Không có điểm cộng</option>
                    <option value="language" v-if="form.bonusType1 !== 'language'">Chứng chỉ ngoại ngữ</option>
                    <option value="direct" v-if="form.bonusType1 !== 'direct'">Thí sinh xét tuyển thẳng, ưu tiên xét tuyển không sử dụng quyền tuyển thẳng</option>
                  </select>
                </div>

                <!-- Chứng chỉ ngoại ngữ (loại 2) -->
                <div class="mb-3" v-if="form.bonusType2 === 'language'">
                  <div class="row g-2">
                    <div class="col-12 col-md-6">
                      <label for="certificateType2" class="form-label small mb-1">Loại chứng chỉ</label>
                      <select 
                        v-model="form.certificateType2" 
                        class="form-select form-select-sm" 
                        id="certificateType2"
                        @change="onCertificateTypeChange(2)">
                        <option value="">-- Chọn loại chứng chỉ --</option>
                        <option value="KNLNN">KNLNN Việt Nam</option>
                        <option value="Aptis">Khung tham chiếu châu Âu Aptis ESOL</option>
                        <option value="IELTS">IELTS Academic</option>
                        <option value="VSEP">VSEP</option>
                        <option value="PEIC">PEIC</option>
                        <option value="PTE">PTE Academic</option>
                        <option value="Linguaskill">Linguaskill</option>
                        <option value="Cambridge">Cambridge Assessment English</option>
                        <option value="CET">Cambridge English Test</option>
                        <option value="TOEIC">TOEIC</option>
                        <option value="TOEFL">TOEFL iBT</option>
                        <option value="JLPT">JLPT</option>
                      </select>
                    </div>
                    <div class="col-12 col-md-6">
                      <label for="certificateLevel2" class="form-label small mb-1">Trình độ/Điểm số</label>
                      <select v-if="!isTOEIC2 && showTextSelect2" v-model="form.certificateLevel2" class="form-select form-select-sm" id="certificateLevel2">
                        <option value="">-- Chọn trình độ --</option>
                        <option v-for="level in certificateLevels2" :key="level" :value="level">{{ level }}</option>
                      </select>
                      <input v-else-if="!isTOEIC2 && !showTextSelect2" type="number" v-model.number="form.certificateLevel2" class="form-control form-control-sm" id="certificateLevel2" step="0.1" min="0" :max="maxCertificateScore2">
                      
                      <!-- TOEIC specific inputs (4 skills) -->
                      <div v-if="isTOEIC2" class="mt-2">
                        <div class="row g-1 mb-1">
                          <div class="col-6">
                            <div class="input-group input-group-sm">
                              <span class="input-group-text">Nghe</span>
                              <input type="number" v-model.number="form.toeic2.listen" class="form-control form-control-sm" min="0" max="495">
                            </div>
                          </div>
                          <div class="col-6">
                            <div class="input-group input-group-sm">
                              <span class="input-group-text">Đọc</span>
                              <input type="number" v-model.number="form.toeic2.read" class="form-control form-control-sm" min="0" max="495">
                            </div>
                          </div>
                        </div>
                        <div class="row g-1">
                          <div class="col-6">
                            <div class="input-group input-group-sm">
                              <span class="input-group-text">Nói</span>
                              <input type="number" v-model.number="form.toeic2.speak" class="form-control form-control-sm" min="0" max="200">
                            </div>
                          </div>
                          <div class="col-6">
                            <div class="input-group input-group-sm">
                              <span class="input-group-text">Viết</span>
                              <input type="number" v-model.number="form.toeic2.write" class="form-control form-control-sm" min="0" max="200">
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Thí sinh xét tuyển thẳng (loại 2) -->
                <div class="mb-3" v-if="form.bonusType2 === 'direct'">
                  <label for="directAdmissionType2" class="form-label small mb-1">Loại thành tích</label>
                  <select 
                    v-model="form.directAdmissionType2" 
                    class="form-select form-select-sm" 
                    id="directAdmissionType2">
                    <option value="">-- Chọn loại thành tích --</option>
                    <option value="hero">Anh hùng lực lượng lao động, Anh hùng lực lượng vũ trang nhân dân, Chiến sĩ thi đua toàn quốc</option>
                    <option value="national_first">Giải nhất chọn HSG, thi KHKT cấp quốc gia, quốc tế</option>
                    <option value="national_second">Giải nhì chọn HSG, thi KHKT cấp quốc gia, quốc tế</option>
                    <option value="national_third">Giải ba chọn HSG, thi KHKT cấp quốc gia, quốc tế</option>
                  </select>
                </div>

                <!-- Hiển thị tổng điểm cộng -->
                <div class="mt-3 mb-2 p-2 bg-light rounded" v-if="calculatedBonusScore > 0">
                  <div class="d-flex justify-content-between align-items-center">
                    <div class="fw-bold">Tổng điểm cộng:</div>
                    <div class="fw-bold text-primary">{{ calculatedBonusScore }}</div>
                  </div>
                </div>
              </div>
              
              <!-- Chọn trường (xác định khu vực ưu tiên) -->
              <h3 class="section-title h6 mt-3 mb-2">Chọn trường</h3>
              <div class="school-selection-container p-2 p-md-3">
                <div class="row g-2">
                  <div class="col-12">
                    <label for="city" class="form-label small mb-1">Tỉnh/Thành phố</label>
                    <select 
                      v-model="cityId" 
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
                      v-model="districtId" 
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
                      v-model="schoolId" 
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


              <!-- Chọn đối tượng ưu tiên -->
              <div class="mb-3 mt-3">
                <h3 class="section-title h6 mb-2">Chọn Ưu tiên đối tượng</h3>
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
                    <strong>Đối tượng 01:</strong> Công dân Việt Nam là người dân tộc thiểu số có nơi thường trú trong thời gian học THPT hoặc trung cấp trên 18 thán[...]
                  </div>
                  <div v-else-if="priorityObject === 'ĐT02'" class="small">
                    <strong>Đối tượng 02:</strong> Công nhân trực tiếp sản xuất đã làm việc liên tục 5 năm trở lên, trong đó có ít nhất 2 năm là chiến sĩ thi đua [...]
                  </div>
                  <div v-else-if="priorityObject === 'ĐT03'" class="small">
                    <strong>Đối tượng 03:</strong> Thương binh, bệnh binh, người có 'Giấy chứng nhận người được hưởng chính sách như thương binh', Quân nhân tại ng[...]
                  </div>
                  <div v-else-if="priorityObject === 'ĐT04'" class="small">
                    <strong>Đối tượng 04:</strong> Thân nhân liệt sĩ, con thương binh, bệnh binh suy giảm KNL từ 81% trở lên, con của người hoạt động kháng chiến bị [...]
                  </div>
                  <div v-else-if="priorityObject === 'ĐT05'" class="small">
                    <strong>Đối tượng 05:</strong> Thanh niên xung phong, quân nhân tại ngũ dưới 12 tháng ở KV1 hoặc 18 tháng ở khu vực khác, Chỉ huy trưởng quân sự xã[...]
                  </div>
                  <div v-else-if="priorityObject === 'ĐT06'" class="small">
                    <strong>Đối tượng 06:</strong> Người dân tộc thiểu số ở khu vực khác ngoài KV1, con thương binh, bệnh binh suy giảm KNL dưới 81% [...]
                  </div>
                  <div v-else-if="priorityObject === 'ĐT07'" class="small">
                    <strong>Đối tượng 07:</strong> Người khuyết tật nặng, người lao động ưu tú, giáo viên đã giảng dạy 3 năm trở lên, y tá, dược tá, hộ lý [...[...]
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
                  <table class="table table-sm table-striped table-bordered">
                    <thead class="bg-light">
                      <tr>
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
                
                <!-- Điểm tổ hợp và điểm ưu tiên - Đã cải thiện thiết kế -->
                <div class="point-summary my-3">
                  <div class="row g-2">
                    <div class="col-12 col-md-3">
                      <div class="point-card original p-2">
                        <div class="point-title small">Điểm tổ hợp gốc</div>
                        <div class="point-value">{{ result.priority_points.origin_point || result.score }}</div>
                        <div class="point-description small">(Thang 30)</div>
                      </div>
                    </div>
                    <div class="col-12 col-md-3">
                      <div class="point-card bonus p-2">
                        <div class="point-title small">Điểm cộng</div>
                        <div class="point-value">{{ result.priority_points.bonus_score || 0 }}</div>
                      </div>
                    </div>
                    <div class="col-12 col-md-3">
                      <div class="point-card priority p-2">
                        <div class="point-title small">Điểm ưu tiên</div>
                        <div class="point-value">{{ result.priority_points.convert_priority }}</div>
                        <div class="point-description small">(Đã quy đổi)</div>
                      </div>
                    </div>
                    <div class="col-12 col-md-3">
                      <div class="point-card total p-2">
                        <div class="point-title small">Tổng điểm</div>
                        <div class="point-value">{{ result.priority_points.total_point }}</div>
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
                      <!-- Hiển thị danh mục đầu tiên nếu có (giới thiệu) -->
                      <div v-for="(category, catIndex) in suggestions[result.group_id]" :key="`cat-${result.group_id}-${catIndex}`" class="suggestion-category mb-3">
                        <!-- Hiển thị danh mục giới thiệu nếu có và không phải danh mục gộp -->
                        <div v-if="!category.isCombined" class="category-title fw-bold mb-2" v-html="category.title"></div>
                        
                        <!-- Hiển thị danh sách ngành cho danh mục giới thiệu -->
                        <div v-if="!category.isCombined && category.majors" class="table-responsive">
                          <table class="table table-sm table-hover">
                            <thead>
                              <tr class="bg-light">
                                <th style="width: 5%">STT</th>
                                <th>Tên ngành</th>
                                <th style="width: 20%" class="text-center">Chi tiết</th>
                              </tr>
                            </thead>
                            <tbody>
                              <tr v-for="(major, majorIdx) in category.majors" :key="`major-intro-${result.group_id}-${catIndex}-${majorIdx}`">
                                <td>{{ majorIdx + 1 }}</td>
                                <td>{{ major.name }}</td>
                                <td class="text-center">
                                  <a :href="major.link" target="_blank" class="btn btn-sm btn-link">Tại đây</a>
                                </td>
                              </tr>
                            </tbody>
                          </table>
                        </div>
                        
                        <!-- Hiển thị bảng gộp cho các ngành có mức độ an toàn -->
                        <div v-if="category.isCombined" class="table-responsive">
                          <div class="category-title fw-bold mb-2">{{ category.title }}</div>
                          <table class="table table-sm table-hover major-suggestion-table">
                            <thead>
                              <tr class="bg-light">
                                <th style="width: 5%">STT</th>
                                <th>Tên ngành</th>
                                <th style="width: 20%" class="text-center">Mức độ an toàn</th>
                                <th style="width: 15%" class="text-center">Chi tiết</th>
                              </tr>
                            </thead>
                            <tbody>
                              <tr v-for="(major, majorIdx) in category.majors" :key="`major-combined-${result.group_id}-${catIndex}-${majorIdx}`">
                                <td>{{ majorIdx + 1 }}</td>
                                <td>{{ major.name }}</td>
                                <td class="text-center">
                                  <span v-if="major.safetyLevel === 'high'" class="safety-level-high safety-text">
                                    Rất an toàn
                                  </span>
                                  <span v-else-if="major.safetyLevel === 'medium'" class="safety-level-medium safety-text">
                                    Khá an toàn
                                  </span>
                                  <span v-else-if="major.safetyLevel === 'low'" class="safety-level-low safety-text">
                                    Chưa an toàn
                                  </span>
                                </td>
                                <td class="text-center">
                                  <a :href="major.link" target="_blank" class="btn btn-sm btn-link">Tại đây</a>
                                </td>
                              </tr>
                            </tbody>
                          </table>
                        </div>
                        
                        <!-- Hiển thị ghi chú nếu có -->
                        <div v-if="category.isNote" class="suggestion-footer text-muted small fst-italic">
                          <p v-html="category.note"></p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <hr v-if="resultIndex < finalResults.length - 1" class="my-3">
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
import { ref, reactive, computed, onMounted, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import CalculateScoreController from '@/controllers/CalculateScoreController';
import ChatRasaController from '@/controllers/ChatRasaController';
import { calculateLanguageCertificatePoints, calculateDirectAdmissionPoints } from '@/controllers/bonuspoint';

export default {
  name: 'CalculateScoreTHPT',
  setup() {
    const route = useRoute();
    const router = useRouter();
    
    // Form state
    const allSubjects = ref([]); // Danh sách tất cả các môn học từ API
    const subjects = ref([]); // Giữ để tương thích với code cũ
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
    const errors = ref({
      city_id: '',
      district_id: '',
      school_id: ''
    });
    const submitted = ref(false);
    const showPriorityStep = ref(false);
    
    // URL sharing variables
    const shareableUrl = ref('');
    const urlCopied = ref(false);
    const urlParseError = ref('');
    
    // Gợi ý ngành học
    const suggestions = ref({}); // Lưu trữ gợi ý cho từng tổ hợp: { group_id: [{title, majors}] }
    const suggestionsLoading = ref(null); // ID của tổ hợp đang tải gợi ý
    
    // Bonus score data
    const form = reactive({
      bonusType1: '',
      certificateType1: '',
      certificateLevel1: '',
      toeic1: {
        listen: null,
        read: null,
        speak: null,
        write: null
      },
      directAdmissionType1: '',
      bonusType2: '',
      certificateType2: '',
      certificateLevel2: '',
      toeic2: {
        listen: null,
        read: null,
        speak: null,
        write: null
      },
      directAdmissionType2: ''
    });
    
    // Certificate fields
    const certificateLevels1 = ref([]);
    const certificateLevels2 = ref([]);
    const showTextSelect1 = ref(true);
    const showTextSelect2 = ref(true);
    const maxCertificateScore1 = ref(10);
    const maxCertificateScore2 = ref(10);
    const isTOEIC1 = ref(false);
    const isTOEIC2 = ref(false);
    
    // Computed properties
    const selectedSchoolPriority = computed(() => {
      if (schools.value.length && schoolId.value) {
        const selected = schools.value.find(s => s.id == schoolId.value);
        return selected ? selected.priority_area : '';
      }
      return '';
    });
    
    // Computed property for bonus score calculation
    const calculatedBonusScore = computed(() => {
      let totalBonus = 0;
      
      // Calculate bonus from first bonus type
      if (form.bonusType1 === 'language' && form.certificateType1) {
        if (form.certificateType1 === 'TOEIC') {
          // For TOEIC, check if at least one skill has valid score
          const { listen, read, speak, write } = form.toeic1;
          if (listen > 0 || read > 0 || speak > 0 || write > 0) {
            totalBonus += calculateLanguageCertificatePoints(form.certificateType1, form.toeic1);
          }
        } else if (form.certificateLevel1) {
          totalBonus += calculateLanguageCertificatePoints(form.certificateType1, form.certificateLevel1);
        }
      } else if (form.bonusType1 === 'direct' && form.directAdmissionType1) {
        totalBonus += calculateDirectAdmissionPoints(form.directAdmissionType1);
      }
      
      // Calculate bonus from second bonus type
      if (form.bonusType2 === 'language' && form.certificateType2) {
        if (form.certificateType2 === 'TOEIC') {
          // For TOEIC, check if at least one skill has valid score
          const { listen, read, speak, write } = form.toeic2;
          if (listen > 0 || read > 0 || speak > 0 || write > 0) {
            totalBonus += calculateLanguageCertificatePoints(form.certificateType2, form.toeic2);
          }
        } else if (form.certificateLevel2) {
          totalBonus += calculateLanguageCertificatePoints(form.certificateType2, form.certificateLevel2);
        }
      } else if (form.bonusType2 === 'direct' && form.directAdmissionType2) {
        totalBonus += calculateDirectAdmissionPoints(form.directAdmissionType2);
      }
      
      return totalBonus;
    });
    
    // Phương thức để lấy danh sách môn học có thể chọn cho một dòng cụ thể
    const getAvailableSubjectsForRow = (currentIndex) => {
      // Lấy danh sách ID các môn học đã chọn, ngoại trừ môn đã chọn tại row hiện tại
      const selectedSubjectIds = subjectScores.value
        .filter((item, idx) => idx !== currentIndex && item.selectedSubject && item.subject_id)
        .map(item => item.subject_id);
      
      // Trả về danh sách các môn học chưa được chọn + môn học đang chọn tại row hiện tại
      const currentSubjectId = subjectScores.value[currentIndex].subject_id;
      
      if (currentSubjectId) {
        // Nếu row hiện tại đã chọn môn, thêm môn này vào danh sách có thể chọn
        return allSubjects.value.filter(subject => 
          !selectedSubjectIds.includes(subject.id) || subject.id === currentSubjectId
        );
      } else {
        // Nếu row hiện tại chưa chọn môn, chỉ hiển thị các môn chưa được chọn
        return allSubjects.value.filter(subject => !selectedSubjectIds.includes(subject.id));
      }
    };
    
    // Bonus score methods
    const onBonusType1Change = () => {
      form.certificateType1 = '';
      form.certificateLevel1 = '';
      form.directAdmissionType1 = '';
      certificateLevels1.value = [];
      showTextSelect1.value = true;
      maxCertificateScore1.value = 10;
      isTOEIC1.value = false;
      form.toeic1 = {
        listen: null,
        read: null,
        speak: null,
        write: null
      };
    };
    
    const onBonusType2Change = () => {
      form.certificateType2 = '';
      form.certificateLevel2 = '';
      form.directAdmissionType2 = '';
      certificateLevels2.value = [];
      showTextSelect2.value = true;
      maxCertificateScore2.value = 10;
      isTOEIC2.value = false;
      form.toeic2 = {
        listen: null,
        read: null,
        speak: null,
        write: null
      };
    };
    
    const onCertificateTypeChange = (bonusNumber) => {
      const certType = bonusNumber === 1 ? form.certificateType1 : form.certificateType2;
      
      if (bonusNumber === 1) {
        form.certificateLevel1 = '';
        isTOEIC1.value = certType === 'TOEIC';
      } else {
        form.certificateLevel2 = '';
        isTOEIC2.value = certType === 'TOEIC';
      }
      
      // Set levels based on certificate type
      let levels = [];
      let showTextSelect = true;
      let maxScore = 10;
      
      switch (certType) {
        case 'KNLNN':
          levels = ['Bậc 3', 'Bậc 4', 'Bậc 5', 'Bậc 6'];
          break;
        case 'Aptis':
          levels = ['B1', 'B2', 'C1', 'C2'];
          break;
        case 'IELTS':
          showTextSelect = false;
          maxScore = 9.0;
          break;
        case 'VSEP':
          showTextSelect = false;
          maxScore = 10.0;
          break;
        case 'PEIC':
          levels = ['Level 2', 'Level 3', 'Level 4', 'Level 5'];
          break;
        case 'PTE':
          showTextSelect = false;
          maxScore = 90;
          break;
        case 'Linguaskill':
          showTextSelect = false;
          maxScore = 200;
          break;
        case 'Cambridge':
          levels = ['B1 Preliminary', 'B1 Business Preliminary', 'B2 First', 'B2 Business Vantage', 'C1 Advanced', 'C1 Business Higher', 'C2 Proficiency'];
          break;
        case 'CET':
          levels = ['PTE', 'FCE', 'CAE', 'CPE'];
          showTextSelect = true;
          break;
        case 'JLPT':
          levels = ['N4', 'N3', 'N2', 'N1'];
          showTextSelect = true;
          break;
        case 'TOEFL':
          showTextSelect = false;
          maxScore = 120;
          break;
      }
      
      if (bonusNumber === 1) {
        certificateLevels1.value = levels;
        showTextSelect1.value = showTextSelect && levels.length > 0;
        maxCertificateScore1.value = maxScore;
      } else {
        certificateLevels2.value = levels;
        showTextSelect2.value = showTextSelect && levels.length > 0;
        maxCertificateScore2.value = maxScore;
      }
    };
    
    // Normalize subject name for URL processing
    const normalizeSubjectName = (name) => {
      return name.toLowerCase().trim();
    };
    
    // Find a subject match based on normalized name
    const findSubjectMatch = (normalizedName) => {
      return allSubjects.value.find(subject => 
        normalizeSubjectName(subject.name) === normalizedName
      );
    };
    
    // Process URL parameters for automatic score calculation
    const processUrlParams = async () => {
      try {
        // Đảm bảo danh sách môn học đã được tải
        if (allSubjects.value.length === 0) {
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
            matchedSubject = allSubjects.value.find(s => s.id.toString() === subjectId);
          } else {
            // Trường hợp URL cũ sử dụng tên môn học
            const normalizedKey = normalizeSubjectName(key);
            matchedSubject = findSubjectMatch(normalizedKey);
          }
          
          if (matchedSubject) {
            // Xử lý điểm
            const score = parseFloat(query[key]);
            
            if (!isNaN(score) && score >= 0 && score <= 10) {
              // Làm tròn đến 0.01
              const roundedScore = Math.round(score * 100) / 100;
              
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
    
    // Format exam score to the nearest 0.01
    const formatExamScore = (index) => {
      const scoreValue = subjectScores.value[index].scores[0];
      if (scoreValue !== '' && !isNaN(parseFloat(scoreValue))) {
        // Round to nearest 0.01
        const roundedValue = Math.round(parseFloat(scoreValue) * 100) / 100;
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
      errors.value.district_id = '';
      errors.value.school_id = '';
      
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
      errors.value.school_id = '';
      
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
        const subjectsData = await CalculateScoreController.getSubjects();
        allSubjects.value = subjectsData;
        subjects.value = subjectsData; // Giữ để tương thích với code cũ
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
        error.value = 'Điểm phải nằm trong khoảng từ 0 đến 10 và được làm tròn đến 0.01';
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
        if (window.$ && $('.selectpicker').length) {
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
        
        // Get bonus score
        const bonusScore = calculatedBonusScore.value;
        
        // Calculate priority points for the selected combinations
        finalResults.value = await CalculateScoreController.calculateCombinationPriorityPoints(
          selectedCombinations,
          selectedSchoolPriority.value,
          priorityObject.value,
          bonusScore,
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
      urlCopied.value = false;
      urlParseError.value = '';
      suggestions.value = {};
      
      // Reset bonus score form
      form.bonusType1 = '';
      form.certificateType1 = '';
      form.certificateLevel1 = '';
      form.toeic1 = { listen: null, read: null, speak: null, write: null };
      form.directAdmissionType1 = '';
      form.bonusType2 = '';
      form.certificateType2 = '';
      form.certificateLevel2 = '';
      form.toeic2 = { listen: null, read: null, speak: null, write: null };
      form.directAdmissionType2 = '';
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
        
        // Use the specialized function for getting suggestions
        const processedSuggestions = await ChatRasaController.getMajorSuggestions(subjectNames, score);
        
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
        
        // Process URL params if any
        await processUrlParams();
        
        // Khởi tạo bootstrap-select nếu cần
        setTimeout(() => {
          if (window.$ && $('.selectpicker').length) {
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
      allSubjects,
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
      errors,
      submitted,
      showPriorityStep,
      
      // URL sharing variables
      shareableUrl,
      urlCopied,
      urlParseError,
      
      // Suggestions
      suggestions,
      suggestionsLoading,
      
      // Form for bonus points
      form,
      certificateLevels1,
      certificateLevels2,
      showTextSelect1,
      showTextSelect2,
      maxCertificateScore1,
      maxCertificateScore2,
      isTOEIC1,
      isTOEIC2,
      
      // Computed properties
      selectedSchoolPriority,
      calculatedBonusScore,
      
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
      getAvailableSubjectsForRow,
      generateShareableUrl,
      copyUrlToClipboard,
      getMajorSuggestions,
      
      // Bonus score methods
      onBonusType1Change,
      onBonusType2Change,
      onCertificateTypeChange
    };
  }
};
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

/* Step indicator */
.step-indicator {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1.5rem;
}

.step {
  display: flex;
  flex-direction: column;
  align-items: center;
  opacity: 0.5;
  transition: all 0.3s ease;
}

.step.active {
  opacity: 1;
}

.step-number {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background-color: #dee2e6;
  color: #495057;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 0.875rem;
  margin-bottom: 0.25rem;
  transition: all 0.3s ease;
}

.step.active .step-number {
  background-color: #0e4c92;
  color: #fff;
}

.step-title {
  color: #6c757d;
  transition: all 0.3s ease;
}

.step.active .step-title {
  color: #0e4c92;
  font-weight: 500;
}

.step-line {
  flex-grow: 1;
  height: 2px;
  background-color: #dee2e6;
  margin: 0 1rem;
  margin-bottom: 1.5rem;
  max-width: 100px;
}

/* Section titles */
.section-title {
  color: #0e4c92;
  font-weight: 600;
  text-align: center;
  margin-bottom: 0.75rem;
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

/* Subject list table */
.subject-list table {
  border-collapse: collapse;
}

.subject-list thead th {
  background-color: #f8f9fa;
  font-weight: 600;
  font-size: 0.875rem;
  color: #495057;
  border-bottom: 2px solid #dee2e6;
}

/* School selection container */
.school-selection-container {
  background-color: rgba(208, 225, 249, 0.2);
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
.initial-results table, .final-results-container table {
  border-collapse: collapse;
}

.combination-row {
  background-color: #e6f0ff !important;
  font-weight: 500;
}

/* Point cards */
.point-summary {
  margin: 1rem 0;
}

.point-card {
  background-color: #f8f9fa;
  border-radius: 0.5rem;
  border: 1px solid #e9ecef;
  text-align: center;
  height: 100%;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
  transition: all 0.2s;
}

.point-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
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

.point-card.original {
  background-color: #f8f9fa;
  border-color: #dee2e6;
}

.point-card.bonus {
  background-color: #e2f8ee;
  border-color: #b3e6d5;
}

.point-card.bonus .point-value {
  color: #0d8055;
}

.point-card.priority {
  background-color: #ebf5ff;
  border-color: #bfdeff;
}

.point-card.priority .point-value {
  color: #0074cc;
}

.point-card.total {
  background-color: #e6f4ff;
  border-color: #91caff;
}

.point-card.total .point-value {
  color: #1677ff;
  font-size: 1.5rem;
}

/* URL generator */
.url-display {
  background-color: #f8f9fa;
  border: 1px solid #dee2e6;
  border-radius: 0.375rem;
}

/* Loading indicator */
.loading-indicator {
  text-align: center;
  color: #0e4c92;
  padding: 1rem;
}

/* Safety levels for suggestions */
.safety-level-high {
  background: linear-gradient(135deg, #198754, #25b070);
  color: white;
  font-weight: bold;
  padding: 0.25rem 0.75rem;
  border-radius: 0.75rem;
  box-shadow: 0 2px 4px rgba(25, 135, 84, 0.3);
  transition: all 0.2s ease;
  display: inline-block;
  text-shadow: 0px 1px 1px rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.15);
}

.safety-level-high:hover {
  transform: translateY(-1px);
  box-shadow: 0 3px 6px rgba(25, 135, 84, 0.4);
}

.safety-level-medium {
  background: linear-gradient(135deg, #0d6efd, #4d94ff);
  color: white;
  font-weight: bold;
  padding: 0.25rem 0.75rem;
  border-radius: 0.75rem;
  box-shadow: 0 2px 4px rgba(13, 110, 253, 0.3);
  transition: all 0.2s ease;
  display: inline-block;
  text-shadow: 0px 1px 1px rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.15);
}

.safety-level-medium:hover {
  transform: translateY(-1px);
  box-shadow: 0 3px 6px rgba(13, 110, 253, 0.4);
}

.safety-level-low {
  background: linear-gradient(135deg, #ffc107, #ffda73);
  color: #212529;
  font-weight: bold;
  padding: 0.25rem 0.75rem;
  border-radius: 0.75rem;
  box-shadow: 0 2px 4px rgba(255, 193, 7, 0.3);
  transition: all 0.2s ease;
  display: inline-block;
  text-shadow: 0px 1px 1px rgba(255, 255, 255, 0.3);
  border: 1px solid rgba(0, 0, 0, 0.05);
}

.safety-level-low:hover {
  transform: translateY(-1px);
  box-shadow: 0 3px 6px rgba(255, 193, 7, 0.4);
}

/* Subject selection */
.subject-actions {
  display: flex;
  justify-content: center;
}

/* Suggestion section */
.suggestions-container .card-header {
  border-bottom: 1px solid rgba(0,0,0,0.08);
}

.suggestion-category:not(:last-child) {
  border-bottom: 1px dashed #dee2e6;
  padding-bottom: 1rem;
}

.category-title {
  color: #1a3f6e;
}

.suggestion-footer {
  background-color: #f8f9fa;
  padding: 0.5rem;
  border-radius: 0.25rem;
  margin-top: 0.5rem;
}

/* Combination name header */
.combination-name {
  border-radius: 0.25rem;
  background-color: #f0f7ff !important;
  color: #1a3f6e;
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
  
  .step-line {
    margin: 0 0.5rem;
    margin-bottom: 1.5rem;
    max-width: 50px;
  }
}
</style>
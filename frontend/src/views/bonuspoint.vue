<template>
  <div class="bonuspoint-container">
    <div class="container-fluid py-2 py-md-3">
      <article class="card main-card shadow-sm">
        <!-- Header Section -->
        <header class="card-header bg-primary text-white" aria-labelledby="bonuspoint-title">
          <div class="d-flex justify-content-center align-items-center">
            <div class="header-icon me-2" aria-hidden="true">
              <i class="bi bi-award"></i>
            </div>
            <h1 id="bonuspoint-title" class="mb-0 fs-5">ĐIỂM CỘNG (ĐIỂM THƯỞNG) XÉT TUYỂN ĐẠI HỌC</h1>
          </div>
        </header>
        
        <!-- Description Section -->
        <div class="description-section bg-light p-2 border-bottom">
          <div class="container">
            <p class="description-text mb-1">
              <strong>Trường Đại học Bách khoa, Đại học Đà Nẵng cộng điểm vào các phương thức đối với thí sinh có chứng chỉ ngoại ngữ hoặc có quyền xét tuyển thẳng và ưu tiên xét tuyển mà không sử dụng.</strong>
            </p>
            
            <div class="announcement-content">
              <!-- Accordion for collapsible content -->
              <div class="accordion accordion-flush" id="announcementAccordion">
                <div class="accordion-item">
                  <h2 class="accordion-header">
                    <button class="accordion-button collapsed p-2 fs-7" type="button" data-bs-toggle="collapse" data-bs-target="#section1" aria-expanded="false" aria-controls="section1">
                      <strong>Quy định về điểm thưởng xét tuyển</strong>
                    </button>
                  </h2>
                  <div id="section1" class="accordion-collapse collapse" data-bs-parent="#announcementAccordion">
                    <div class="accordion-body p-2 fs-7">
                      <p class="mb-1">Điểm thưởng là tổng điểm cộng của điểm cộng chứng chỉ ngoại ngữ cao nhất và điểm cộng đối tượng tuyển thẳng cao nhất, tối đa là 3.0 điểm.</p>
                      <p class="mb-1">Sau khi cộng với điểm xét tuyển (chưa bao gồm điểm ưu tiên), nếu tổng điểm vượt quá 30 điểm thì điểm xét tuyển tối đa là 30 điểm.</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Main Content Section -->
        <div class="card-body py-2">
          <!-- Foreign Language Certificates Table -->
          <section class="table-section mb-4" aria-labelledby="language-certificate-heading">
            <h2 id="language-certificate-heading" class="section-title mb-3">
              <i class="bi bi-translate me-2" aria-hidden="true"></i>
              Bảng điểm thưởng chứng chỉ ngoại ngữ
            </h2>
            
            <div class="table-responsive">
              <table class="table table-bordered border-primary table-hover table-sm">
                <caption class="caption-top text-center small fst-italic text-muted">Điểm thưởng dựa trên loại chứng chỉ và trình độ/điểm số đạt được</caption>
                <thead>
                  <tr class="bg-primary text-white">
                    <th scope="col" rowspan="2" class="align-middle text-center" style="width: 15%">Loại chứng chỉ</th>
                    <th scope="col" rowspan="2" class="align-middle text-center" style="width: 5%">Kỹ năng</th>
                    <th scope="col" colspan="4" class="text-center" style="width: 80%">Mức điểm thưởng</th>
                  </tr>
                  <tr class="bg-primary text-white">
                    <th scope="col" class="text-center" style="width: 20%">0.25</th>
                    <th scope="col" class="text-center" style="width: 20%">0.50</th>
                    <th scope="col" class="text-center" style="width: 20%">0.75</th>
                    <th scope="col" class="text-center" style="width: 20%">1.00</th>
                  </tr>
                </thead>
                <tbody>
                  <!-- KNLNN -->
                  <tr>
                    <td>KNLNN Việt Nam</td>
                    <td class="text-center"></td>
                    <td class="text-center">Bậc 3</td>
                    <td class="text-center">Bậc 4</td>
                    <td class="text-center">Bậc 5</td>
                    <td class="text-center">Bậc 6</td>
                  </tr>
                  
                  <!-- Aptis -->
                  <tr>
                    <td>Khung tham chiếu châu Âu Aptis ESOL</td>
                    <td class="text-center"></td>
                    <td class="text-center">B1</td>
                    <td class="text-center">B2</td>
                    <td class="text-center">C1</td>
                    <td class="text-center">C2</td>
                  </tr>
                  
                  <!-- IELTS -->
                  <tr>
                    <td>IELTS Academic</td>
                    <td class="text-center"></td>
                    <td class="text-center">5.0</td>
                    <td class="text-center">5.5-6.5</td>
                    <td class="text-center">7.0-8.0</td>
                    <td class="text-center">8.5-9.0</td>
                  </tr>
                  
                  <!-- VSEP -->
                  <tr>
                    <td>VSEP</td>
                    <td class="text-center"></td>
                    <td class="text-center">5.5</td>
                    <td class="text-center">6.0-8.0</td>
                    <td class="text-center">8.5-10.0</td>
                    <td class="text-center">-</td>
                  </tr>
                  
                  <!-- PEIC -->
                  <tr>
                    <td>PEIC</td>
                    <td class="text-center"></td>
                    <td class="text-center">Level 2</td>
                    <td class="text-center">Level 3</td>
                    <td class="text-center">Level 4</td>
                    <td class="text-center">Level 5</td>
                  </tr>
                  
                  <!-- PTE Academic -->
                  <tr>
                    <td>PTE Academic</td>
                    <td class="text-center"></td>
                    <td class="text-center">45-58</td>
                    <td class="text-center">59-75</td>
                    <td class="text-center">76-84</td>
                    <td class="text-center">≥85</td>
                  </tr>
                  
                  <!-- Linguaskill -->
                  <tr>
                    <td>Linguaskill</td>
                    <td class="text-center"></td>
                    <td class="text-center">140-159</td>
                    <td class="text-center">160-179</td>
                    <td class="text-center">≥180</td>
                    <td class="text-center">-</td>
                  </tr>
                  
                  <!-- Cambridge Assessment English -->
                  <tr>
                    <td>Cambridge Assessment English</td>
                    <td class="text-center"></td>
                    <td class="text-center">B1 Preliminary/<br>B1 Business Preliminary</td>
                    <td class="text-center">B2 First/<br>B2 Business Vantage</td>
                    <td class="text-center">C1 Advanced/<br>C1 Business Higher</td>
                    <td class="text-center">C2 Proficiency</td>
                  </tr>
                  
                  <!-- Cambridge English Test -->
                  <tr>
                    <td>Cambridge English Test</td>
                    <td class="text-center"></td>
                    <td class="text-center">PTE<br>(140-159)</td>
                    <td class="text-center">FCE<br>(160-179)</td>
                    <td class="text-center">CAE<br>(180-199)</td>
                    <td class="text-center">CPE<br>(200-230)</td>
                  </tr>
                  
                  <!-- TOEFL -->
                  <tr>
                    <td>TOEFL iBT</td>
                    <td class="text-center"></td>
                    <td class="text-center">30-45</td>
                    <td class="text-center">46-93</td>
                    <td class="text-center">94-114</td>
                    <td class="text-center">≥115</td>
                  </tr>
                  
                  <!-- TOEIC -->
                  <tr>
                    <td rowspan="5">TOEIC</td>
                    
                  </tr>
                  <tr>
                    <td class="text-center">Nghe</td>
                    <td class="text-center">275-395</td>
                    <td class="text-center">400-485</td>
                    <td class="text-center">≥490</td>
                    <td class="text-center"></td>
                  </tr>
                  <tr>
                    <td class="text-center">Đọc</td>
                    <td class="text-center">275-380</td>
                    <td class="text-center">385-450</td>
                    <td class="text-center">≥455</td>
                    <td class="text-center"></td>
                  </tr>
                  <tr>
                    <td class="text-center">Nói</td>
                    <td class="text-center">120-150</td>
                    <td class="text-center">160-170</td>
                    <td class="text-center">≥180</td>
                    <td class="text-center"></td>
                  </tr>
                  <tr>
                    <td class="text-center">Viết</td>
                    <td class="text-center">120-140</td>
                    <td class="text-center">150-170</td>
                    <td class="text-center">≥180</td>
                    <td class="text-center"></td>
                  </tr>
                </tbody>
              </table>
            </div>
          </section>
          
          <!-- Direct Admission Achievements Table -->
          <section class="table-section mb-4" aria-labelledby="direct-admission-heading">
            <h2 id="direct-admission-heading" class="section-title mb-3">
              <i class="bi bi-trophy me-2" aria-hidden="true"></i>
              Bảng điểm thưởng xét tuyển thẳng không sử dụng quyền tuyển thẳng
            </h2>
            
            <div class="table-responsive">
              <table class="table table-bordered border-primary table-hover table-sm">
                <thead>
                  <tr class="bg-primary text-white">
                    <th scope="col" class="text-center" style="width: 5%">STT</th>
                    <th scope="col" style="width: 50%">Thành tích</th>
                    <th scope="col" class="text-center" style="width: 20%">Điểm thưởng</th>
                    <th scope="col" style="width: 25%">Ghi chú</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td class="text-center">1</td>
                    <td>Anh hùng lực lượng lao động, Anh hùng lực lượng vũ trang nhân dân, Chiến sĩ thi đua toàn quốc</td>
                    <td class="text-center font-weight-bold text-primary">2.0</td>
                    <td rowspan="4">Không sử dụng quyền xét tuyển thẳng</td>
                  </tr>
                  <tr>
                    <td class="text-center">2</td>
                    <td>Giải nhất HSG hoặc KHKT cấp quốc gia, quốc tế</td>
                    <td class="text-center font-weight-bold text-primary">2.0</td>
                  </tr>
                  <tr>
                    <td class="text-center">3</td>
                    <td>Giải nhì HSG hoặc KHKT cấp quốc gia, quốc tế</td>
                    <td class="text-center font-weight-bold text-primary">1.5</td>
                  </tr>
                  <tr>
                    <td class="text-center">4</td>
                    <td>Giải ba HSG hoặc KHKT cấp quốc gia, quốc tế</td>
                    <td class="text-center font-weight-bold text-primary">1.0</td>
                  </tr>
                </tbody>
              </table>
            </div>
            
            <div class="notes mt-2 p-2 bg-light rounded">
              <p class="small mb-0"><strong>Lưu ý:</strong> Điểm thưởng là tổng điểm cộng của điểm cộng chứng chỉ ngoại ngữ cao nhất và điểm cộng đối tượng tuyển thẳng cao nhất, tối đa là 3.0 điểm. Sau khi cộng với điểm xét tuyển (chưa bao gồm điểm ưu tiên), nếu tổng điểm vượt quá 30 điểm thì điểm xét tuyển tối đa là 30 điểm.</p>
            </div>
          </section>
          
          <!-- Calculator Section -->
          <section class="calculator-section" aria-labelledby="calculator-heading">
            <h2 id="calculator-heading" class="section-title mb-3">
              <i class="bi bi-calculator me-2" aria-hidden="true"></i>
              Tra cứu điểm thưởng
            </h2>
            
            <!-- Tab navigation for calculator types -->
            <ul class="nav nav-tabs" id="calculatorTabs" role="tablist">
              <li class="nav-item" role="presentation">
                <button class="nav-link active" 
                  id="language-tab" 
                  data-bs-toggle="tab" 
                  data-bs-target="#language-calculator" 
                  type="button" 
                  role="tab" 
                  aria-controls="language-calculator" 
                  aria-selected="true">
                  Chứng chỉ ngoại ngữ
                </button>
              </li>
              <li class="nav-item" role="presentation">
                <button class="nav-link" 
                  id="direct-admission-tab" 
                  data-bs-toggle="tab" 
                  data-bs-target="#direct-admission-calculator" 
                  type="button" 
                  role="tab" 
                  aria-controls="direct-admission-calculator" 
                  aria-selected="false">
                  Xét tuyển thẳng
                </button>
              </li>
            </ul>
            
            <!-- Tab content -->
            <div class="tab-content p-3 border border-top-0 rounded-bottom mb-3" id="calculatorTabContent">
              <!-- Foreign Language Certificate Calculator -->
              <div class="tab-pane fade show active" id="language-calculator" role="tabpanel" aria-labelledby="language-tab">
                <div class="row g-3">
                  <div class="col-md-6">
                    <label for="certificateType" class="form-label">Loại chứng chỉ</label>
                    <select 
                      v-model="form.certificateType" 
                      class="form-select" 
                      id="certificateType"
                      @change="onCertificateTypeChange">
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
                    </select>
                  </div>
                  
                  <div v-if="form.certificateType" class="col-md-6">
                    <!-- Standard input for level selection - for non-TOEIC certificates -->
                    <template v-if="form.certificateType !== 'TOEIC'">
                      <label for="certificateLevel" class="form-label">Trình độ/Điểm số</label>
                      <div class="input-group">
                        <select v-if="showTextSelect" v-model="form.certificateLevel" class="form-select" id="certificateLevel">
                          <option value="">-- Chọn trình độ --</option>
                          <option v-for="level in certificateLevels" :key="level" :value="level">{{ level }}</option>
                        </select>
                        <input v-else type="number" v-model.number="form.certificateLevel" class="form-control" id="certificateLevel" step="0.1" min="0" :max="maxCertificateScore">
                      </div>
                    </template>
                    
                    <!-- TOEIC specific inputs (4 skills) -->
                    <template v-else>
                      <label class="form-label">Điểm TOEIC (4 kỹ năng)</label>
                      <div class="row g-2 mb-2">
                        <div class="col-6">
                          <div class="input-group input-group-sm">
                            <span class="input-group-text">Nghe</span>
                            <input type="number" v-model.number="form.toeic.listen" class="form-control" min="0" max="495">
                          </div>
                        </div>
                        <div class="col-6">
                          <div class="input-group input-group-sm">
                            <span class="input-group-text">Đọc</span>
                            <input type="number" v-model.number="form.toeic.read" class="form-control" min="0" max="495">
                          </div>
                        </div>
                      </div>
                      <div class="row g-2">
                        <div class="col-6">
                          <div class="input-group input-group-sm">
                            <span class="input-group-text">Nói</span>
                            <input type="number" v-model.number="form.toeic.speak" class="form-control" min="0" max="200">
                          </div>
                        </div>
                        <div class="col-6">
                          <div class="input-group input-group-sm">
                            <span class="input-group-text">Viết</span>
                            <input type="number" v-model.number="form.toeic.write" class="form-control" min="0" max="200">
                          </div>
                        </div>
                      </div>
                    </template>
                  </div>
                  
                  <div class="col-12">
                    <button class="btn btn-primary" 
                      @click="calculateLanguageBonus" 
                      :disabled="!canCalculateLanguage">
                      Tính điểm thưởng
                    </button>
                  </div>
                </div>
                
                <!-- Result display for language certificate -->
                <div v-if="languageResult !== null" class="result-display mt-3 p-3 border rounded bg-light">
                  <h3 class="h6 mb-2">Kết quả tính toán</h3>
                  <div class="d-flex justify-content-between align-items-center">
                    <p class="mb-0"><strong>Điểm thưởng:</strong></p>
                    <p class="mb-0 display-6">{{ languageResult }}</p>
                  </div>
                  <p class="small text-muted mt-2 mb-0">Thí sinh được cộng {{ languageResult }} điểm vào tổng điểm xét tuyển.</p>
                </div>
              </div>
              
              <!-- Direct Admission Achievement Calculator -->
              <div class="tab-pane fade" id="direct-admission-calculator" role="tabpanel" aria-labelledby="direct-admission-tab">
                <div class="row g-3">
                  <div class="col-12">
                    <label for="directAdmissionType" class="form-label">Loại thành tích</label>
                    <select 
                      v-model="form.directAdmissionType" 
                      class="form-select" 
                      id="directAdmissionType">
                      <option value="">-- Chọn loại thành tích --</option>
                      <option value="hero">Anh hùng lực lượng lao động, Anh hùng lực lượng vũ trang nhân dân, Chiến sĩ thi đua toàn quốc</option>
                      <option value="national_first">Giải nhất chọn HSG, thi KHKT cấp quốc gia, quốc tế</option>
                      <option value="national_second">Giải nhì chọn HSG, thi KHKT cấp quốc gia, quốc tế</option>
                      <option value="national_third">Giải ba chọn HSG, thi KHKT cấp quốc gia, quốc tế</option>
                    </select>
                  </div>
                  
                  <div class="col-12">
                    <button class="btn btn-primary" 
                      @click="calculateDirectAdmissionBonus" 
                      :disabled="!form.directAdmissionType">
                      Tính điểm thưởng
                    </button>
                  </div>
                </div>
                
                <!-- Result display for direct admission -->
                <div v-if="directAdmissionResult !== null" class="result-display mt-3 p-3 border rounded bg-light">
                  <h3 class="h6 mb-2">Kết quả tính toán</h3>
                  <div class="d-flex justify-content-between align-items-center">
                    <p class="mb-0"><strong>Điểm thưởng:</strong></p>
                    <p class="mb-0 display-6">{{ directAdmissionResult }}</p>
                  </div>
                  <p class="small text-muted mt-2 mb-0">Thí sinh được cộng {{ directAdmissionResult }} điểm vào tổng điểm xét tuyển.</p>
                </div>
              </div>
            </div>
            
            <!-- Compare results (when both calculations are available) -->
            <div v-if="languageResult !== null && directAdmissionResult !== null" class="compare-section mt-3 p-3 border rounded bg-primary bg-opacity-10">
              <h3 class="h5 mb-3">Tổng điểm thưởng</h3>
              
              <div class="table-responsive">
                <table class="table table-bordered table-sm">
                  <thead class="bg-primary text-white">
                    <tr>
                      <th>Loại điểm thưởng</th>
                      <th class="text-center">Điểm</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td>Chứng chỉ ngoại ngữ</td>
                      <td class="text-center">{{ languageResult }}</td>
                    </tr>
                    <tr>
                      <td>Xét tuyển thẳng</td>
                      <td class="text-center">{{ directAdmissionResult }}</td>
                    </tr>
                    <tr class="fw-bold bg-light">
                      <td>Tổng điểm thưởng</td>
                      <td class="text-center">{{ Math.min(languageResult + directAdmissionResult, 3.0) }}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
              
              <p class="small text-muted mt-1 mb-0">
                Điểm thưởng tối đa không vượt quá 3.0 điểm. Sau khi cộng với điểm xét tuyển (chưa bao gồm điểm ưu tiên), nếu tổng điểm vượt quá 30 điểm thì điểm xét tuyển tối đa là 30 điểm.
              </p>
            </div>
          </section>
          
          <!-- Contact Information -->
          <section class="contact-section mt-4" aria-labelledby="contact-heading">
            <div class="card bg-light">
              <div class="card-body p-2">
                <h2 id="contact-heading" class="card-title fs-6 mb-2">
                  <i class="bi bi-info-circle me-2" aria-hidden="true"></i>
                  Thông tin liên hệ
                </h2>
                <div class="mt-1">
                  <ul class="contact-list">
                    <li>Muốn biết thêm chi tiết, thí sinh vui lòng truy cập trang Tuyển sinh của Trường Đại học Bách khoa tại địa chỉ: <a href="https://tuyensinh.dut.udn.vn" target="_blank">https://tuyensinh.dut.udn.vn</a></li>
                    <li>Hotline: <a href="tel:0888477377">0888 477 377</a>; <a href="tel:0888477533">0888 477 533</a></li>
                    <li>Email: <a href="mailto:tuyensinhbkdn@dut.udn.vn">tuyensinhbkdn@dut.udn.vn</a></li>
                    <li>Fanpage: <a href="https://www.facebook.com/DUTpage" target="_blank" rel="noopener noreferrer">https://www.facebook.com/DUTpage</a></li>
                  </ul>
                </div>
              </div>
            </div>
          </section>
        </div>
      </article>
    </div>
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted } from 'vue';
import { calculateLanguageCertificatePoints, calculateDirectAdmissionPoints } from '@/controllers/bonuspoint';

export default {
  name: 'BonusPointView',
  setup() {
    // Form state
    const form = reactive({
      certificateType: '',
      certificateLevel: '',
      toeic: {
        listen: null,
        read: null,
        speak: null,
        write: null
      },
      directAdmissionType: ''
    });
    
    // Results
    const languageResult = ref(null);
    const directAdmissionResult = ref(null);
    
    // Certificate fields
    const certificateLevels = ref([]);
    const showTextSelect = ref(true);
    const maxCertificateScore = ref(10);
    
    // Computed properties
    const canCalculateLanguage = computed(() => {
      if (!form.certificateType) return false;
      
      if (form.certificateType === 'TOEIC') {
        // For TOEIC, check if at least one skill has valid score
        const { listen, read, speak, write } = form.toeic;
        return listen > 0 || read > 0 || speak > 0 || write > 0;
      } else {
        // For other certificates, check if level is provided
        return !!form.certificateLevel;
      }
    });
    
    // Methods
    const onCertificateTypeChange = () => {
      form.certificateLevel = '';
      const certType = form.certificateType;
      
      // Set levels based on certificate type
      let levels = [];
      let showSelectMode = true;
      let maxScore = 10;
      
      switch (certType) {
        case 'KNLNN':
          levels = ['Bậc 3', 'Bậc 4', 'Bậc 5', 'Bậc 6'];
          break;
        case 'Aptis':
          levels = ['B1', 'B2', 'C1', 'C2'];
          break;
        case 'IELTS':
          showSelectMode = false;
          maxScore = 9.0;
          break;
        case 'VSEP':
          showSelectMode = false;
          maxScore = 10.0;
          break;
        case 'PEIC':
          levels = ['Level 2', 'Level 3', 'Level 4', 'Level 5'];
          break;
        case 'PTE':
          showSelectMode = false;
          maxScore = 90;
          break;
        case 'Linguaskill':
          showSelectMode = false;
          maxScore = 200;
          break;
        case 'Cambridge':
          levels = ['B1 Preliminary', 'B1 Business Preliminary', 'B2 First', 'B2 Business Vantage', 'C1 Advanced', 'C1 Business Higher', 'C2 Proficiency'];
          break;
        case 'CET':
          levels = ['PTE(140-159)', 'FCE(160-179)', 'CAE(180-199)', 'CPE(200-230)'];
          showSelectMode = true;
          break;
        case 'TOEFL':
          showSelectMode = false;
          maxScore = 120;
          break;
        case 'TOEIC':
          // Reset TOEIC specific fields
          form.toeic = {
            listen: null,
            read: null,
            speak: null,
            write: null
          };
          break;
      }
      
      certificateLevels.value = levels;
      showTextSelect.value = showSelectMode && levels.length > 0;
      maxCertificateScore.value = maxScore;
    };
    
    const calculateLanguageBonus = () => {
      try {
        let result;
        
        // Calculate based on certificate type
        if (form.certificateType === 'TOEIC') {
          result = calculateLanguageCertificatePoints(form.certificateType, form.toeic);
        } else {
          result = calculateLanguageCertificatePoints(form.certificateType, form.certificateLevel);
        }
        
        languageResult.value = result;
      } catch (error) {
        console.error('Error calculating language bonus:', error);
        languageResult.value = 0;
      }
    };
    
    const calculateDirectAdmissionBonus = () => {
      try {
        const result = calculateDirectAdmissionPoints(form.directAdmissionType);
        directAdmissionResult.value = result;
      } catch (error) {
        console.error('Error calculating direct admission bonus:', error);
        directAdmissionResult.value = 0;
      }
    };
    
    const initializeTooltips = () => {
      // Initialize Bootstrap tooltips if needed
      if (typeof bootstrap !== 'undefined') {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
          return new bootstrap.Tooltip(tooltipTriggerEl);
        });
      }
    };
    
    // Initialize tooltips after component is mounted
    onMounted(() => {
      initializeTooltips();
    });
    
    return {
      form,
      languageResult,
      directAdmissionResult,
      certificateLevels,
      showTextSelect,
      maxCertificateScore,
      canCalculateLanguage,
      onCertificateTypeChange,
      calculateLanguageBonus,
      calculateDirectAdmissionBonus
    };
  }
}
</script>

<style scoped>
/* Base Container */
.bonuspoint-container {
  min-height: 100vh;
  background-color: #f5f5f5;
  margin: 0;
  padding: 0 5px;
}

@media (min-width: 768px) {
  .bonuspoint-container {
    margin: 0 2vw;
    padding: 0;
  }
}

/* Main Card */
.main-card {
  border: none;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.1) !important;
}

/* Header */
.card-header {
  background-color: #0d47a1 !important;
  padding: 0.6rem;
}

.header-icon {
  font-size: 1.3rem;
}

/* Description Section */
.description-section {
  background-color: #e8f1ff !important;
  border-bottom: 1px solid #dee2e6;
}

.description-text {
  font-size: 0.85rem;
  line-height: 1.3;
  color: #495057;
}

/* Section Titles */
.section-title {
  color: #0d47a1;
  font-size: 1.2rem;
  font-weight: 600;
  border-bottom: 2px solid #e8f1ff;
  padding-bottom: 0.5rem;
}

/* Tables */
.table {
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
}

.table th {
  background-color: #0d47a1;
  color: white;
  vertical-align: middle;
}

.table thead th {
  font-weight: 600;
}

.table tbody td {
  vertical-align: middle;
}

.table-bordered {
  border-color: #dee2e6;
}

.table caption {
  padding: 0.3rem;
  margin-bottom: 0.3rem;
}

/* Calculator Section */
.calculator-section {
  background-color: #f8f9fa;
  padding: 1rem;
  border-radius: 8px;
  border: 1px solid #e9ecef;
}

.nav-tabs .nav-link {
  color: #495057;
  font-size: 0.9rem;
}

.nav-tabs .nav-link.active {
  color: #0d47a1;
  font-weight: 600;
}

.form-label {
  font-weight: 500;
  color: #495057;
  margin-bottom: 0.3rem;
  font-size: 0.9rem;
}

.btn-primary {
  background-color: #0d47a1;
  border-color: #0d47a1;
}

.btn-primary:hover {
  background-color: #0a3987;
  border-color: #0a3987;
}

/* Result Display */
.result-display {
  background-color: #f0f7ff !important;
}

.result-display .display-6 {
  font-weight: 700;
  color: #0d47a1;
}

/* Compare Section */
.compare-section {
  border-color: #0d47a1 !important;
}

/* Contact Section */
.contact-section .card {
  border: none;
  border-radius: 6px;
}

.contact-list {
  padding-left: 1rem;
  margin-bottom: 0;
  font-size: 0.8rem;
}

.contact-list li {
  margin-bottom: 0.4rem;
}

.contact-list a {
  color: #0d47a1;
  text-decoration: none;
}

.contact-list a:hover {
  text-decoration: underline;
}

/* Accordion */
.accordion-button {
  font-size: 0.85rem;
}

.accordion-button:not(.collapsed) {
  background-color: rgba(13, 71, 161, 0.1);
  color: #0d47a1;
}

.accordion-button:focus {
  box-shadow: 0 0 0 0.25rem rgba(13, 71, 161, 0.25);
}

/* Font sizes */
.fs-7 {
  font-size: 0.75rem !important;
}

/* Responsive adjustments */
@media (max-width: 576px) {
  .header-icon {
    font-size: 1.1rem;
  }
  
  #bonuspoint-title {
    font-size: 0.95rem !important;
  }
  
  .description-text, 
  .accordion-button,
  .contact-list {
    font-size: 0.75rem;
  }
  
  .section-title {
    font-size: 1rem;
  }
  
  .table {
    font-size: 0.8rem;
  }
}
</style>
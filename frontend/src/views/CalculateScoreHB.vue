<template>
    <div class="calculate-score-container">
      <div class="header-section">
        <h1 class="main-title">Công cụ tính điểm xét tuyển học bạ</h1>
        <div class="header-description">
          <p>Công cụ này giúp bạn tính toán điểm xét tuyển dựa trên kết quả học tập ở trường THPT.</p>
          <p>Nhập thông tin điểm số các môn học của bạn để nhận kết quả tính toán cho tất cả tổ hợp môn học.</p>
        </div>
      </div>
      
      <div class="score-calculator-card">
        <div class="option-selector">
          <div class="form-check form-check-inline">
            <input class="form-check-input" 
                   type="radio" 
                   name="scoreOption" 
                   id="semesterOption" 
                   value="semester" 
                   v-model="scoreOption">
            <label class="form-check-label" for="semesterOption">Điểm 6 học kỳ</label>
          </div>
          <div class="form-check form-check-inline">
            <input class="form-check-input" 
                   type="radio" 
                   name="scoreOption" 
                   id="yearOption" 
                   value="year" 
                   v-model="scoreOption">
            <label class="form-check-label" for="yearOption">Điểm 3 năm học</label>
          </div>
        </div>
        
        <div class="subject-list">
          <div v-for="(subject, index) in subjectScores" :key="index" class="subject-item">
            <div class="subject-header">
              <select class="form-select subject-selector" 
                      v-model="subject.selectedSubject"
                      @change="updateSubjectId(index)">
                <option value="">Chọn môn học</option>
                <option v-for="sub in subjects" 
                        :key="sub.id" 
                        :value="sub">
                  {{ sub.name }}
                </option>
              </select>
              <button class="btn btn-danger remove-btn" 
                      @click="removeSubject(index)"
                      :disabled="subjectScores.length <= 1">
                <i class="bi bi-x"></i>
              </button>
            </div>
            
            <div class="scores-container">
              <template v-if="scoreOption === 'semester'">
                <div class="score-input-group">
                  <label>HK1 - Lớp 10:</label>
                  <input type="number" 
                         class="form-control" 
                         v-model="subject.scores[0]" 
                         min="0" 
                         max="10" 
                         step="0.01">
                </div>
                <div class="score-input-group">
                  <label>HK2 - Lớp 10:</label>
                  <input type="number" 
                         class="form-control" 
                         v-model="subject.scores[1]" 
                         min="0" 
                         max="10" 
                         step="0.01">
                </div>
                <div class="score-input-group">
                  <label>HK1 - Lớp 11:</label>
                  <input type="number" 
                         class="form-control" 
                         v-model="subject.scores[2]" 
                         min="0" 
                         max="10" 
                         step="0.01">
                </div>
                <div class="score-input-group">
                  <label>HK2 - Lớp 11:</label>
                  <input type="number" 
                         class="form-control" 
                         v-model="subject.scores[3]" 
                         min="0" 
                         max="10" 
                         step="0.01">
                </div>
                <div class="score-input-group">
                  <label>HK1 - Lớp 12:</label>
                  <input type="number" 
                         class="form-control" 
                         v-model="subject.scores[4]" 
                         min="0" 
                         max="10" 
                         step="0.01">
                </div>
                <div class="score-input-group">
                  <label>HK2 - Lớp 12:</label>
                  <input type="number" 
                         class="form-control" 
                         v-model="subject.scores[5]" 
                         min="0" 
                         max="10" 
                         step="0.01">
                </div>
              </template>
              
              <template v-else>
                <div class="score-input-group year-score">
                  <label>Lớp 10:</label>
                  <input type="number" 
                         class="form-control" 
                         v-model="subject.scores[0]" 
                         min="0" 
                         max="10" 
                         step="0.01">
                </div>
                <div class="score-input-group year-score">
                  <label>Lớp 11:</label>
                  <input type="number" 
                         class="form-control" 
                         v-model="subject.scores[1]" 
                         min="0" 
                         max="10" 
                         step="0.01">
                </div>
                <div class="score-input-group year-score">
                  <label>Lớp 12:</label>
                  <input type="number" 
                         class="form-control" 
                         v-model="subject.scores[2]" 
                         min="0" 
                         max="10" 
                         step="0.01">
                </div>
              </template>
            </div>
          </div>
          
          <div class="subject-actions">
            <button class="btn btn-primary" @click="addSubject">
              <i class="bi bi-plus-circle"></i> Thêm môn học
            </button>
          </div>
        </div>
        
        <div class="calculation-actions">
          <button class="btn btn-calculate" @click="calculateScores">
            <i class="bi bi-calculator"></i> Tính điểm
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
      
      <div v-if="results.length > 0" class="results-section">
        <h2 class="results-title">Kết quả tính toán</h2>
        <div class="results-description">
          <p>Dưới đây là điểm của bạn theo từng tổ hợp môn học, sắp xếp theo thứ tự điểm cao xuống thấp.</p>
        </div>
        
        <div class="results-table">
          <table class="table table-striped table-hover">
            <thead>
              <tr>
                <th>STT</th>
                <th>Mã tổ hợp</th>
                <th>Tên tổ hợp</th>
                <th>Môn học</th>
                <th>Điểm trung bình</th>
                <th>Hệ số</th>
                <th>Điểm tổ hợp</th>
              </tr>
            </thead>
            <tbody>
              <template v-for="(result, resultIndex) in results" :key="resultIndex">
                <tr class="combination-row">
                  <td>{{ resultIndex + 1 }}</td>
                  <td>{{ result.group_id }}</td>
                  <td>{{ result.group_name }}</td>
                  <td colspan="3"></td>
                  <td class="combination-score">{{ result.score }}</td>
                </tr>
                <tr v-for="(subject, subjectIndex) in result.subjects" :key="`${resultIndex}-${subjectIndex}`">
                  <td></td>
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
      </div>
    </div>
  </template>
  
  <script>
  import { ref, onMounted, reactive } from 'vue'
  import CalculateScoreController from '@/controllers/CalculateScoreController'
  
  export default {
    name: 'CalculateScoreHB',
    setup() {
      const subjects = ref([])
      const scoreOption = ref('semester')
      const subjectScores = ref([
        {
          selectedSubject: '',
          subject_id: null,
          subject_name: '',
          scores: ['', '', '', '', '', '']
        }
      ])
      
      const loading = ref(false)
      const error = ref('')
      const results = ref([])
      
      onMounted(async () => {
        try {
          loading.value = true
          const data = await CalculateScoreController.getSubjects()
          subjects.value = data
        } catch (err) {
          error.value = 'Không thể tải danh sách môn học. Vui lòng thử lại sau.'
          console.error(err)
        } finally {
          loading.value = false
        }
      })
      
      const updateSubjectId = (index) => {
        const selected = subjectScores.value[index].selectedSubject
        if (selected) {
          subjectScores.value[index].subject_id = selected.id
          subjectScores.value[index].subject_name = selected.name
        } else {
          subjectScores.value[index].subject_id = null
          subjectScores.value[index].subject_name = ''
        }
      }
      
      const addSubject = () => {
        subjectScores.value.push({
          selectedSubject: '',
          subject_id: null,
          subject_name: '',
          scores: scoreOption.value === 'semester' ? ['', '', '', '', '', ''] : ['', '', '']
        })
      }
      
      const removeSubject = (index) => {
        if (subjectScores.value.length > 1) {
          subjectScores.value.splice(index, 1)
        }
      }
      
      const calculateScores = async () => {
        try {
          error.value = ''
          results.value = []
          
          // Validation
          const invalidSubjects = subjectScores.value.filter(subject => !subject.selectedSubject)
          if (invalidSubjects.length > 0) {
            error.value = 'Vui lòng chọn môn học cho tất cả các dòng.'
            return
          }
          
          loading.value = true
          
          // Format data for API
          const formattedData = subjectScores.value.map(subject => ({
            subject_id: subject.subject_id,
            subject_name: subject.subject_name,
            scores: subject.scores.map(score => score === '' ? 0 : parseFloat(score))
          }))
          
          const response = await CalculateScoreController.calculateHBScores(
            formattedData, 
            scoreOption.value
          )
          
          results.value = response.combinations
          
          if (results.value.length === 0) {
            error.value = 'Không tìm thấy tổ hợp phù hợp với các điểm đã nhập.'
          }
        } catch (err) {
          error.value = 'Có lỗi xảy ra khi tính điểm. Vui lòng kiểm tra dữ liệu và thử lại.'
          console.error(err)
        } finally {
          loading.value = false
        }
      }
      
      return {
        subjects,
        scoreOption,
        subjectScores,
        loading,
        error,
        results,
        updateSubjectId,
        addSubject,
        removeSubject,
        calculateScores
      }
    }
  }
  </script>
  
  <style scoped>
  .calculate-score-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem 1rem;
    background-color: white;
  }
  
  .header-section {
    text-align: center;
    margin-bottom: 2rem;
  }
  
  .main-title {
    color: #0B2942;
    font-weight: bold;
    margin-bottom: 1rem;
  }
  
  .header-description {
    color: #666;
    max-width: 800px;
    margin: 0 auto;
  }
  
  .score-calculator-card {
    background-color: white;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    padding: 2rem;
    margin-bottom: 2rem;
  }
  
  .option-selector {
    display: flex;
    justify-content: center;
    margin-bottom: 2rem;
  }
  
  .form-check-inline {
    margin-right: 2rem;
  }
  
  .subject-list {
    margin-bottom: 1.5rem;
  }
  
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
  
  .score-input-group {
    flex: 0 0 calc(16.666% - 1rem);
  }
  
  .year-score {
    flex: 0 0 calc(33.333% - 1rem);
  }
  
  .score-input-group label {
    font-size: 0.9rem;
    margin-bottom: 0.5rem;
    display: block;
    color: #555;
  }
  
  .subject-actions {
    margin-top: 1.5rem;
    text-align: center;
  }
  
  .calculation-actions {
    text-align: center;
    margin-top: 2rem;
  }
  
  .btn-calculate {
    background-color: #0B2942;
    color: white;
    padding: 0.75rem 2rem;
    font-size: 1.1rem;
    border-radius: 30px;
    transition: all 0.3s;
    border: none;
  }
  
  .btn-calculate:hover {
    background-color: #164675;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(11, 41, 66, 0.2);
  }
  
  .results-section {
    margin-top: 3rem;
  }
  
  .results-title {
    color: #0B2942;
    text-align: center;
    margin-bottom: 1rem;
  }
  
  .results-description {
    text-align: center;
    color: #666;
    margin-bottom: 2rem;
  }
  
  .results-table {
    overflow-x: auto;
  }
  
  .combination-row {
    background-color: #ebf5ff !important;
    font-weight: bold;
  }
  
  .combination-score {
    font-size: 1.1rem;
    font-weight: bold;
    color: #0B2942;
  }
  
  .loading-indicator {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin: 2rem 0;
  }
  
  @media (max-width: 992px) {
    .score-input-group {
      flex: 0 0 calc(33.333% - 1rem);
    }
  }
  
  @media (max-width: 768px) {
    .score-input-group {
      flex: 0 0 calc(50% - 1rem);
    }
  }
  
  @media (max-width: 576px) {
    .score-input-group {
      flex: 0 0 100%;
    }
  }
  </style>
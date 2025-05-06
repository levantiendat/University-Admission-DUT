<template>
    <div class="calculate-score-container">
      <div class="header-section">
        <h1 class="main-title">Công cụ tính điểm xét tuyển thi THPT</h1>
        <div class="header-description">
          <p>Công cụ này giúp bạn tính toán điểm xét tuyển dựa trên kết quả kỳ thi tốt nghiệp THPT.</p>
          <p>Nhập thông tin điểm số các môn thi của bạn để nhận kết quả tính toán cho tất cả tổ hợp môn xét tuyển.</p>
        </div>
      </div>
      
      <div class="score-calculator-card">
        <div class="subject-list">
          <div v-for="(subject, index) in subjectScores" :key="index" class="subject-item">
            <div class="subject-header">
              <select class="form-select subject-selector" 
                      v-model="subject.selectedSubject"
                      @change="updateSubjectId(index)">
                <option value="">Chọn môn thi</option>
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
              <div class="score-input-group exam-score">
                <label>Điểm thi:</label>
                <input type="number" 
                       class="form-control" 
                       v-model="subject.scores[0]" 
                       min="0" 
                       max="10" 
                       step="0.01">
              </div>
            </div>
          </div>
          
          <div class="subject-actions">
            <button class="btn btn-primary" @click="addSubject">
              <i class="bi bi-plus-circle"></i> Thêm môn thi
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
          <p>Dưới đây là điểm của bạn theo từng tổ hợp môn thi, sắp xếp theo thứ tự điểm cao xuống thấp.</p>
        </div>
        
        <div class="results-table">
          <table class="table table-striped table-hover">
            <thead>
              <tr>
                <th>STT</th>
                <th>Mã tổ hợp</th>
                <th>Tên tổ hợp</th>
                <th>Môn thi</th>
                <th>Điểm thi</th>
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
  import { ref, onMounted } from 'vue'
  import CalculateScoreController from '@/controllers/CalculateScoreController'
  
  export default {
    name: 'CalculateScoreTHPT',
    setup() {
      const subjects = ref([])
      const subjectScores = ref([
        {
          selectedSubject: '',
          subject_id: null,
          subject_name: '',
          scores: ['']
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
          scores: ['']
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
            error.value = 'Vui lòng chọn môn thi cho tất cả các dòng.'
            return
          }
          
          // Check for missing scores
          const invalidScores = subjectScores.value.filter(subject => 
            !subject.scores[0] || subject.scores[0] === '' || isNaN(parseFloat(subject.scores[0]))
          )
          if (invalidScores.length > 0) {
            error.value = 'Vui lòng nhập điểm thi cho tất cả các môn đã chọn.'
            return
          }
          
          loading.value = true
          
          // Format data for API
          const formattedData = subjectScores.value.map(subject => ({
            subject_id: subject.subject_id,
            subject_name: subject.subject_name,
            scores: [parseFloat(subject.scores[0])]
          }))
          
          const response = await CalculateScoreController.calculateTHPTScores(formattedData)
          
          results.value = response.combinations
          
          if (results.value.length === 0) {
            error.value = 'Không tìm thấy tổ hợp phù hợp với các điểm đã nhập. Vui lòng kiểm tra lại điểm các môn thi.'
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
  
  .exam-score {
    flex: 0 0 300px;
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
  
  @media (max-width: 768px) {
    .exam-score {
      flex: 0 0 100%;
    }
  }
  </style>
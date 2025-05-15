<template>
  <div>
    <!-- Hero Section -->
    <header class="hero-section py-3 py-md-4 text-center text-white">
      <div class="container">
        <h1 class="fw-bold mb-1">Quy Đổi Điểm Tương Đương</h1>
        <p>Trường Đại học Bách Khoa - Đại học Đà Nẵng</p>
      </div>
    </header>

    <!-- Main Content -->
    <main class="container my-3 my-md-4">
      <div class="card shadow-sm rounded">
        <div class="card-header text-white text-center py-2">
          <h2 class="h5 mb-0">Công cụ quy đổi điểm giữa các phương thức xét tuyển</h2>
        </div>
        <div class="card-body p-2 p-md-3">
          <div class="alert alert-info small py-2" role="alert">
            <i class="bi bi-info-circle me-1"></i>
            <strong>Lưu ý:</strong> Điểm quy đổi chỉ mang tính chất tham khảo.
          </div>
          
          <!-- Score Conversion Form -->
          <form @submit.prevent="convertScore">
            <!-- Admission Method Selection -->
            <div class="mb-3">
              <label for="admissionMethod" class="form-label">Phương thức xét tuyển</label>
              <select
                id="admissionMethod"
                class="form-select"
                v-model="selectedAdmissionMethod"
                @change="loadConversionTable"
                required
              >
                <option value="">-- Chọn phương thức xét tuyển --</option>
                <option v-for="method in admissionMethods" :key="method.id" :value="method.id">
                  {{ method.name }}
                </option>
              </select>
            </div>

            <!-- Score Input -->
            <div class="mb-3">
              <label for="originalScore" class="form-label">Điểm đầu vào</label>
              <input
                type="number"
                class="form-control"
                id="originalScore"
                v-model="originalScore"
                placeholder="Nhập điểm cần quy đổi"
                min="0"
                step="0.01"
                required
              />
              <div class="form-text small" v-if="selectedAdmissionMethod && currentMethod">
                Thang điểm: {{ currentMethod.min_score }} - {{ currentMethod.max_score }}
              </div>
            </div>

            <!-- Submit Button -->
            <div class="text-center">
              <button type="submit" class="btn btn-convert" :disabled="loading">
                <i class="bi bi-calculator me-1"></i>
                {{ loading ? 'Đang tính...' : 'Quy đổi điểm' }}
              </button>
            </div>
          </form>

          <!-- Conversion Table for Selected Method -->
          <div v-if="selectedAdmissionMethod && conversionTable.length" class="mt-4 conversion-table-container">
            <h3 class="h6 fw-bold mb-2 text-center">Bảng quy đổi điểm</h3>
            <div class="table-responsive">
              <table class="table table-hover conversion-table">
                <thead>
                  <tr>
                    <th scope="col">Điểm đầu vào</th>
                    <th scope="col">Điểm quy đổi</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(range, index) in conversionTable" :key="index">
                    <td>{{ range.origin_min }} - {{ range.origin_max }}</td>
                    <td>{{ range.convert_score_min }} - {{ range.convert_score_max }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- Conversion Result -->
          <div v-if="conversionResult" class="mt-4">
            <div class="conversion-result" :class="conversionResult.success ? 'success-result' : 'failure-result'">
              <div class="result-header">
                <i class="bi" :class="conversionResult.success ? 'bi-check-circle' : 'bi-x-circle'"></i>
                {{ conversionResult.message }}
              </div>
              
              <div class="result-body">
                <!-- Method Info -->
                <div class="result-item">
                  <div class="result-label">Phương thức xét tuyển:</div>
                  <div class="result-value">{{ conversionResult.admission_method?.name }}</div>
                </div>
                
                <!-- Original Score -->
                <div class="result-item">
                  <div class="result-label">Điểm đầu vào:</div>
                  <div class="result-value">{{ conversionResult.origin_score }}</div>
                </div>
                
                <!-- Converted Score - Highlighted -->
                <div class="result-item converted-score" v-if="conversionResult.success">
                  <div class="result-label">Điểm quy đổi:</div>
                  <div class="result-value-highlight">{{ conversionResult.converted_score }}</div>
                </div>
                
                <!-- Conversion Range -->
                <div class="result-item" v-if="conversionResult.success && conversionResult.convert_range">
                  <div class="result-label">Khoảng quy đổi:</div>
                  <div class="result-value">
                    {{ conversionResult.convert_range.origin_min }} - 
                    {{ conversionResult.convert_range.origin_max }} 
                    <i class="bi bi-arrow-right mx-2"></i>
                    {{ conversionResult.convert_range.convert_score_min }} - 
                    {{ conversionResult.convert_range.convert_score_max }}
                  </div>
                </div>
                
                <!-- Formula -->
                <div class="result-item" v-if="conversionResult.success && conversionResult.formula">
                  <div class="result-label">Công thức:</div>
                  <div class="result-value formula">{{ conversionResult.formula }}</div>
                </div>
                
                <!-- Calculation Details -->
                <div class="result-item" v-if="conversionResult.success && conversionResult.calculation_detail">
                  <div class="result-label">Chi tiết tính toán:</div>
                  <div class="result-value calculation-detail">{{ conversionResult.calculation_detail }}</div>
                </div>
                
                <!-- Calculate Priority Points Option -->
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import ConvertPointController from '@/controllers/ConvertPointController'

export default {
  name: 'ConvertPointView',
  setup() {
    // State variables
    const admissionMethods = ref([])
    const selectedAdmissionMethod = ref('')
    const originalScore = ref('')
    const conversionTable = ref([])
    const conversionResult = ref(null)
    const loading = ref(false)
    const error = ref('')

    // Computed properties
    const currentMethod = computed(() => {
      if (!selectedAdmissionMethod.value) return null
      return admissionMethods.value.find(method => method.id === selectedAdmissionMethod.value)
    })

    // Load admission methods with conversion tables
    const loadAdmissionMethods = async () => {
      try {
        loading.value = true
        admissionMethods.value = await ConvertPointController.getAdmissionMethodsWithConversion()
      } catch (err) {
        error.value = 'Không thể tải danh sách phương thức xét tuyển'
        console.error(err)
      } finally {
        loading.value = false
      }
    }

    // Load conversion table for selected method
    const loadConversionTable = async () => {
      if (!selectedAdmissionMethod.value) {
        conversionTable.value = []
        return
      }
      
      try {
        loading.value = true
        conversionTable.value = await ConvertPointController.getConversionTable(selectedAdmissionMethod.value)
        // Reset conversion result when method changes
        conversionResult.value = null
      } catch (err) {
        error.value = 'Không thể tải bảng quy đổi điểm'
        console.error(err)
      } finally {
        loading.value = false
      }
    }

    // Convert score
    const convertScore = async () => {
      if (!selectedAdmissionMethod.value || !originalScore.value) {
        error.value = 'Vui lòng chọn phương thức xét tuyển và nhập điểm'
        return
      }
      
      try {
        loading.value = true
        conversionResult.value = await ConvertPointController.convertScore(
          selectedAdmissionMethod.value, 
          parseFloat(originalScore.value)
        )
      } catch (err) {
        error.value = 'Không thể thực hiện quy đổi điểm'
        console.error(err)
      } finally {
        loading.value = false
      }
    }

    // Initialize component
    onMounted(async () => {
      await loadAdmissionMethods()
    })

    return {
      admissionMethods,
      selectedAdmissionMethod,
      originalScore,
      conversionTable,
      conversionResult,
      loading,
      error,
      currentMethod,
      loadConversionTable,
      convertScore
    }
  }
}
</script>

<style scoped>
/* Hero Section */
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

/* Card styling */
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

/* Form controls */
.form-label {
  font-weight: 600;
  color: #0B2942;
  font-size: 0.9rem;
}

.form-control:focus, .form-select:focus {
  box-shadow: 0 0 0 0.15rem rgba(13, 71, 161, 0.25);
  border-color: #1a73e8;
}

/* Button styling */
.btn-convert {
  background: linear-gradient(135deg, #3a7bd5, #0B2942);
  color: #ffffff;
  border: none;
  padding: 0.5rem 1.5rem;
  transition: all 0.2s;
  font-weight: 600;
  border-radius: 4px;
}

.btn-convert:hover, .btn-convert:focus {
  background: linear-gradient(135deg, #4a8bf5, #1a3952);
  color: #ffffff;
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

/* Enhanced Conversion Table Styling */
.conversion-table-container {
  background-color: #f8fbff;
  border-radius: 8px;
  padding: 15px;
  border: 1px solid #d0e1f9;
}

.conversion-table {
  margin-bottom: 0;
}

.conversion-table thead {
  background: linear-gradient(135deg, #0B2942, #1a73e8);
  color: white;
}

.conversion-table th {
  padding: 10px 15px;
  border-bottom: none;
  font-weight: 600;
  text-align: center;
}

.conversion-table td {
  padding: 8px 15px;
  text-align: center;
  border-color: #d0e1f9;
  font-weight: 500;
}

.conversion-table tr:hover {
  background-color: rgba(13, 71, 161, 0.05);
}

/* Enhanced Result Display */
.conversion-result {
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.1);
}

.result-header {
  padding: 12px 15px;
  font-weight: 600;
  font-size: 1rem;
  display: flex;
  align-items: center;
}

.result-header i {
  margin-right: 10px;
  font-size: 1.2rem;
}

.success-result .result-header {
  background: linear-gradient(135deg, #0B2942, #1a73e8);
  color: white;
}

.failure-result .result-header {
  background: linear-gradient(135deg, #d32f2f, #f44336);
  color: white;
}

.result-body {
  padding: 15px 20px;
  background-color: #f8fbff;
  border: 1px solid;
  border-top: none;
}

.success-result .result-body {
  border-color: #d0e1f9;
}

.failure-result .result-body {
  border-color: #ffcdd2;
}

.result-item {
  margin-bottom: 15px;
  display: flex;
  flex-direction: column;
}

.result-label {
  font-weight: 600;
  color: #0B2942;
  margin-bottom: 5px;
  font-size: 0.9rem;
}

.result-value {
  padding: 8px 12px;
  background-color: white;
  border-radius: 4px;
  border: 1px solid #d0e1f9;
}

/* Highlight for converted score */
.converted-score {
  margin-top: 20px;
  margin-bottom: 20px;
  padding: 10px;
  background-color: rgba(13, 71, 161, 0.05);
  border-radius: 8px;
  border-left: 4px solid #1a73e8;
}

.result-value-highlight {
  font-size: 1.8rem;
  font-weight: 700;
  color: #1a73e8;
  text-align: center;
  padding: 15px;
  background-color: white;
  border-radius: 4px;
  border: 2px solid #1a73e8;
  box-shadow: 0 3px 6px rgba(26, 115, 232, 0.1);
}

.formula {
  font-family: monospace;
  font-size: 0.95rem;
  background-color: #f0f4fa;
  padding: 10px 15px;
}

.calculation-detail {
  font-size: 0.9rem;
  color: #555;
  font-style: italic;
}

/* Priority button */
.priority-calculation {
  margin-top: 20px;
  text-align: center;
}

.btn-priority {
  background-color: #0B2942;
  color: white;
  padding: 10px 20px;
  border-radius: 4px;
  font-weight: 600;
  transition: all 0.2s;
  border: none;
  display: inline-block;
}

.btn-priority:hover {
  background-color: #1a3952;
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .card-body {
    padding: 1rem;
  }
  
  .result-item {
    flex-direction: column;
  }
  
  .result-label {
    margin-bottom: 5px;
  }
  
  .result-value-highlight {
    font-size: 1.5rem;
    padding: 10px;
  }
}
</style>
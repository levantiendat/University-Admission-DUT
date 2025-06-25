<template>
  <div class="admin-admission-method-majors">
    <div class="admin-page-header d-flex justify-content-between align-items-center">
      <div>
        <div class="d-flex align-items-center">
          <router-link :to="`/admins/admission-methods/${admissionMethodId}`" class="btn-back">
            <i class="bi bi-arrow-left"></i>
          </router-link>
          <div>
            <h2 class="admin-page-title">Quản lý ngành áp dụng</h2>
            <p class="admin-page-description">
              Danh sách các ngành áp dụng phương thức xét tuyển:
              <strong>{{ methodName }}</strong>
            </p>
          </div>
        </div>
      </div>
      <button class="btn-create" @click="showAddMajorModal">
        <i class="bi bi-plus-circle me-2"></i>Thêm ngành áp dụng
      </button>
    </div>

    <!-- Search and Filter -->
    <div class="admin-card mb-4">
      <div class="row align-items-center">
        <div class="col-md-12">
          <div class="search-box">
            <i class="bi bi-search search-icon"></i>
            <input
              type="text"
              v-model="searchQuery"
              class="search-input"
              placeholder="Tìm kiếm ngành theo tên hoặc mã ngành..."
              @input="filterMajors"
            >
          </div>
        </div>
      </div>
    </div>

    <!-- Loading Indicator -->
    <div v-if="loading" class="loading-container">
      <div class="spinner">
        <div class="bounce1"></div>
        <div class="bounce2"></div>
        <div class="bounce3"></div>
      </div>
      <p class="loading-text">Đang tải danh sách ngành áp dụng...</p>
    </div>

    <!-- Error Message -->
    <div v-else-if="error" class="error-message">
      <i class="bi bi-exclamation-triangle-fill error-icon"></i>
      <span>{{ error }}</span>
    </div>

    <!-- Majors Table -->
    <div v-else class="admin-card">
      <div class="table-responsive">
        <table class="data-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Mã ngành</th>
              <th>Tên ngành</th>
              <th>Khoa</th>
              <th>Chỉ tiêu riêng</th>
              <th>Điểm sàn</th>
              <th>Môn nền tảng</th>
              <th>Điểm sàn môn</th>
              <th>Thao tác</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="major in filteredMajors" :key="major.id" class="data-row">
              <td><span class="id-badge">#{{ major.major_id }}</span></td>
              <td><span class="code-badge">{{ major.major_code }}</span></td>
              <td><span class="name-text">{{ major.major_name }}</span></td>
              <td>
                <router-link :to="`/admins/faculties/${major.falculty_id}`" class="faculty-link">
                  {{ major.faculty_name }}
                </router-link>
              </td>
              <td><span class="quota-badge">{{ major.quota || 'Không' }}</span></td>
              <td><span class="score-badge">{{ major.minimum_score || 'Không' }}</span></td>
              <td>
                <span v-if="major.foundation_subject_id" class="subject-badge">
                  {{ getSubjectName(major.foundation_subject_id) }}
                </span>
                <span v-else class="none-badge">Không có</span>
              </td>
              <td>
                <span v-if="major.subject_minimum_score" class="subscore-badge">
                  {{ major.subject_minimum_score }}
                </span>
                <span v-else class="none-badge">Không có</span>
              </td>
              <td>
                <div class="action-buttons">
                  <button 
                    class="btn-action edit"
                    @click="showEditMajorModal(major)"
                    title="Chỉnh sửa thông tin"
                  >
                    <i class="bi bi-pencil"></i>
                  </button>
                  <button
                    class="btn-action delete"
                    @click="confirmRemoveMajor(major)"
                    title="Xóa ngành khỏi phương thức tuyển sinh"
                  >
                    <i class="bi bi-x-circle"></i>
                  </button>
                </div>
              </td>
            </tr>

            <!-- Empty State -->
            <tr v-if="filteredMajors.length === 0">
              <td colspan="9">
                <div class="empty-state">
                  <i class="bi bi-clipboard-x empty-icon"></i>
                  <h4>Không tìm thấy ngành áp dụng</h4>
                  <p v-if="searchQuery">Thử thay đổi từ khóa tìm kiếm</p>
                  <p v-else>Chưa có ngành nào áp dụng phương thức tuyển sinh này</p>
                  <button @click="showAddMajorModal" class="btn-create-empty">
                    <i class="bi bi-plus-circle me-2"></i>Thêm ngành áp dụng
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Add/Edit Major Modal -->
    <div v-if="showModal" class="modal-overlay" @click="cancelModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h4 class="modal-title">{{ isEdit ? 'Cập nhật thông tin ngành áp dụng' : 'Thêm ngành áp dụng' }}</h4>
          <button type="button" class="btn-close" @click="cancelModal"></button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="saveAdmissionMethodMajor">
            <div class="form-group">
              <label for="major-select">Chọn ngành <span class="required">*</span></label>
              <select
                id="major-select"
                v-model="formData.major_id"
                class="form-control"
                :disabled="isEdit"
                :class="{ 'is-invalid': formErrors.major_id }"
              >
                <option value="" disabled selected>Chọn ngành áp dụng</option>
                <template v-if="isEdit">
                  <option v-for="major in listMajors" :key="major.id" :value="major.id">
                    {{ major.major_code }} - {{ major.name }}
                  </option>
                </template>
                <template v-else>
                  <option v-for="major in availableMajors" :key="major.id" :value="major.id">
                    {{ major.major_code }} - {{ major.name }}
                  </option>
                </template>
              </select>
              <div v-if="formErrors.major_id" class="invalid-feedback">{{ formErrors.major_id }}</div>
            </div>

            <div class="form-group">
              <label for="quota">Chỉ tiêu riêng của phương thức</label>
              <input
                type="number"
                id="quota"
                v-model="formData.quota"
                class="form-control"
                placeholder="Để trống nếu không giới hạn"
                min="1"
                :class="{ 'is-invalid': formErrors.quota }"
              >
              <div v-if="formErrors.quota" class="invalid-feedback">{{ formErrors.quota }}</div>
              <small class="form-text text-muted">Số lượng chỉ tiêu dành riêng cho phương thức tuyển sinh này.</small>
            </div>

            <div class="form-group">
              <label for="minimum_score">Điểm sàn</label>
              <input
                type="number"
                id="minimum_score"
                v-model="formData.minimum_score"
                class="form-control"
                placeholder="Để trống nếu không giới hạn"
                step="0.01"
                min="0"
                :class="{ 'is-invalid': formErrors.minimum_score }"
              >
              <div v-if="formErrors.minimum_score" class="invalid-feedback">{{ formErrors.minimum_score }}</div>
              <small class="form-text text-muted">Điểm sàn tối thiểu để xét tuyển ngành này.</small>
            </div>

            <div class="form-group">
              <label for="foundation_subject">Môn nền tảng</label>
              <select
                id="foundation_subject"
                v-model="formData.foundation_subject_id"
                class="form-control"
                :class="{ 'is-invalid': formErrors.foundation_subject_id }"
              >
                <option value="">Không có</option>
                <option v-for="subject in subjects" :key="subject.id" :value="subject.id">
                  {{ subject.name }}
                </option>
              </select>
              <div v-if="formErrors.foundation_subject_id" class="invalid-feedback">{{ formErrors.foundation_subject_id }}</div>
              <small class="form-text text-muted">Môn học được coi là nền tảng cho ngành này.</small>
            </div>

            <div class="form-group" v-if="formData.foundation_subject_id">
              <label for="subject_minimum_score">Điểm sàn môn nền tảng </label>
              <input
                type="number"
                id="subject_minimum_score"
                v-model="formData.subject_minimum_score"
                class="form-control"
                step="0.01"
                min="0"
                :class="{ 'is-invalid': formErrors.subject_minimum_score }"
              >
              <div v-if="formErrors.subject_minimum_score" class="invalid-feedback">{{ formErrors.subject_minimum_score }}</div>
              <small class="form-text text-muted">Điểm tối thiểu của môn nền tảng để xét tuyển.</small>
            </div>

            <div v-if="formError" class="alert alert-danger">{{ formError }}</div>
          </form>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn-cancel" @click="cancelModal">Hủy</button>
          <button
            type="button"
            class="btn-add"
            @click="saveAdmissionMethodMajor"
            :disabled="isSaving"
          >
            <span v-if="isSaving">Đang lưu...</span>
            <span v-else>{{ isEdit ? 'Cập nhật' : 'Thêm ngành' }}</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Remove Confirmation Modal -->
    <div v-if="showRemoveModal" class="modal-overlay" @click="cancelRemoveMajor">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h4 class="modal-title">Xác nhận xóa</h4>
          <button type="button" class="btn-close" @click="cancelRemoveMajor"></button>
        </div>
        <div class="modal-body">
          <p>Bạn có chắc chắn muốn xóa ngành <strong>{{ majorToRemove?.major_name }}</strong> khỏi phương thức tuyển sinh này?</p>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn-cancel" @click="cancelRemoveMajor">Hủy</button>
          <button type="button" class="btn-delete" @click="removeMajorFromMethod" :disabled="isRemoving">
            <span v-if="isRemoving">Đang xóa...</span>
            <span v-else>Xác nhận xóa</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import AdmissionMethodController from '@/controllers/admins/AdmissionMethodController'
import AdmissionMethodMajorController from '@/controllers/admins/AdmissionMethodMajorController'
import MajorController from '@/controllers/admins/MajorController'
import SubjectController from '@/controllers/admins/SubjectController'

export default {
  name: 'AdminAdmissionMethodMajors',
  props: {
    admissionMethodId: {
      type: [String, Number],
      required: true
    }
  },
  setup(props) {
    const majors = ref([])
    const filteredMajors = ref([])
    const availableMajors = ref([])
    const listMajors = ref([])
    const subjects = ref([])
    const methodName = ref('')
    const loading = ref(true)
    const error = ref(null)
    const searchQuery = ref('')
    
    // Form state
    const showModal = ref(false)
    const isEdit = ref(false)
    const formData = reactive({
      major_id: '',
      admission_methods_id: props.admissionMethodId,
      quota: '',
      minimum_score: '',
      foundation_subject_id: '',
      subject_minimum_score: ''
    })
    const formErrors = reactive({
      major_id: '',
      quota: '',
      minimum_score: '',
      foundation_subject_id: '',
      subject_minimum_score: ''
    })
    const formError = ref('')
    const isSaving = ref(false)
    const selectedRelationId = ref(null)
    
    // Remove major modal state
    const showRemoveModal = ref(false)
    const majorToRemove = ref(null)
    const isRemoving = ref(false)

    // Filter majors based on search query
    const filterMajors = () => {
      if (!majors.value.length) return
      
      filteredMajors.value = majors.value.filter(major => {
        const matchesQuery = !searchQuery.value || 
          major.major_name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
          major.major_code.toLowerCase().includes(searchQuery.value.toLowerCase())
        
        return matchesQuery
      })
    }

    // Load method details and majors
    const loadData = async () => {
      try {
        loading.value = true
        error.value = null
        
        // Get method name
        const method = await AdmissionMethodController.getAdmissionMethodById(props.admissionMethodId)
        methodName.value = method.name
        
        // Get majors using this method
        const majorsData = await AdmissionMethodMajorController.getMajorsByAdmissionMethod(props.admissionMethodId)
        majors.value = majorsData
        filteredMajors.value = [...majorsData]
        console.log('Loaded majors:', majors.value) // Debug: log loaded majors
        // Get available majors (all majors not using this method)
        await loadAvailableMajors()

        // Load subjects
        await loadSubjects()
      } catch (err) {
        error.value = `Không thể tải danh sách ngành: ${err.message}`
      } finally {
        loading.value = false
      }
    }
    
    // Load majors available to add
    const loadAvailableMajors = async () => {
      try {
        // Get all majors
        const allMajors = await MajorController.getAllMajors()
        
        // Filter out majors that already use this method
        const currentMajorIds = majors.value.map(m => m.major_id)
        availableMajors.value = allMajors.filter(major => !currentMajorIds.includes(major.id))
        listMajors.value = allMajors
      } catch (err) {
        console.error('Error loading available majors:', err)
        availableMajors.value = []
      }
    }

    // Load all subjects
    const loadSubjects = async () => {
      try {
        subjects.value = await SubjectController.getAllSubjects()
      } catch (err) {
        console.error('Error loading subjects:', err)
        subjects.value = []
      }
    }
    
    // Get subject name by ID
    const getSubjectName = (subjectId) => {
      const subject = subjects.value.find(s => s.id === subjectId)
      return subject ? subject.name : 'N/A'
    }
    
    // Reset form data
    const resetForm = () => {
      formData.major_id = ''
      formData.admission_methods_id = props.admissionMethodId
      formData.quota = ''
      formData.minimum_score = ''
      formData.foundation_subject_id = ''
      formData.subject_minimum_score = ''

      // Clear errors
      Object.keys(formErrors).forEach(key => {
        formErrors[key] = ''
      })
      formError.value = ''
    }
    
    // Show add major modal
    const showAddMajorModal = () => {
      resetForm()
      isEdit.value = false
      showModal.value = true
    }
    
    // Show edit major modal
    const showEditMajorModal = (major) => {
      resetForm()
      isEdit.value = true
      
      formData.major_id = major.major_id
      formData.quota = major.quota !== null ? major.quota : ''
      formData.minimum_score = major.minimum_score !== null ? major.minimum_score : ''
      formData.foundation_subject_id = major.foundation_subject_id || ''
      formData.subject_minimum_score = major.subject_minimum_score !== null ? major.subject_minimum_score : ''
      
      selectedRelationId.value = major.id
      showModal.value = true
    }
    
    // Cancel modal
    const cancelModal = () => {
      showModal.value = false
      resetForm()
    }
    
    // Validate form data
    const validateForm = () => {
  let isValid = true;
  
  // Clear errors
  Object.keys(formErrors).forEach(key => {
    formErrors[key] = '';
  });
  formError.value = '';
  
  // Validate major selection
  if (!formData.major_id) {
    formErrors.major_id = 'Vui lòng chọn ngành';
    isValid = false;
  }
  
  // Kiểm tra giá trị quota (chỉ kiểm tra khi không phải chuỗi rỗng)
  if (formData.quota !== '' && formData.quota !== null && formData.quota !== undefined) {
    const quotaValue = parseInt(formData.quota);
    if (isNaN(quotaValue) || quotaValue <= 0) {
      formErrors.quota = 'Chỉ tiêu phải là số nguyên dương';
      isValid = false;
    }
  }
  
  // Kiểm tra giá trị minimum_score (chỉ kiểm tra khi không phải chuỗi rỗng)
  if (formData.minimum_score !== '' && formData.minimum_score !== null && formData.minimum_score !== undefined) {
    const minScoreValue = parseFloat(formData.minimum_score);
    if (isNaN(minScoreValue) || minScoreValue < 0) {
      formErrors.minimum_score = 'Điểm sàn phải là số không âm';
      isValid = false;
    }
  }
  
  // Xử lý môn nền tảng và điểm sàn môn nền tảng
  const hasFoundationSubject = formData.foundation_subject_id !== '' && 
                               formData.foundation_subject_id !== null && 
                               formData.foundation_subject_id !== undefined;
                               
  const hasSubjectMinScore = formData.subject_minimum_score !== '' && 
                             formData.subject_minimum_score !== null && 
                             formData.subject_minimum_score !== undefined;
  
  // Validate mối quan hệ giữa môn nền tảng và điểm sàn môn nền tảng
  
  if (!hasFoundationSubject && hasSubjectMinScore) {
    formErrors.foundation_subject_id = 'Vui lòng chọn môn nền tảng';
    isValid = false;
  }
  
  // Kiểm tra giá trị điểm sàn môn nền tảng (chỉ kiểm tra khi không phải chuỗi rỗng)
  if (hasSubjectMinScore) {
    const subjectMinScoreValue = parseFloat(formData.subject_minimum_score);
    if (isNaN(subjectMinScoreValue) || subjectMinScoreValue < 0) {
      formErrors.subject_minimum_score = 'Điểm sàn môn nền tảng phải là số không âm';
      isValid = false;
    }
  }
  
  console.log('Form validation result:', isValid, formErrors); // Debug: log kết quả validate
  return isValid;
}
    
    // Save admission method-major relationship
    // Save admission method-major relationship
const saveAdmissionMethodMajor = async () => {
  if (!validateForm()) {
    return;
  }
  
  try {
    isSaving.value = true;
    
    // Tạo đối tượng dữ liệu mới
    const data = {
      major_id: formData.major_id,
      admission_methods_id: props.admissionMethodId
    };
    
    // Chỉ thêm các trường có giá trị hoặc chuỗi rỗng (để chuyển thành null)
    // Điều này tránh việc gửi undefined
    if (formData.quota !== undefined) data.quota = formData.quota;
    if (formData.minimum_score !== undefined) data.minimum_score = formData.minimum_score;
    if (formData.foundation_subject_id !== undefined) data.foundation_subject_id = formData.foundation_subject_id;
    if (formData.subject_minimum_score !== undefined) data.subject_minimum_score = formData.subject_minimum_score;
    
    console.log('Data being sent:', data); // Debug: log dữ liệu trước khi gửi
    
    if (isEdit.value) {
      // Update existing relationship
      await AdmissionMethodMajorController.updateAdmissionMethodMajor(selectedRelationId.value, data);
    } else {
      // Create new relationship
      await AdmissionMethodMajorController.createAdmissionMethodMajor(data);
    }
    
    // Reload data
    await loadData();
    
    // Close modal and show success message
    showModal.value = false;
    alert(isEdit.value ? 'Cập nhật thông tin thành công' : 'Thêm ngành áp dụng thành công');
  } catch (err) {
    console.error('Error saving:', err); // Debug: log lỗi chi tiết
    formError.value = err.message;
  } finally {
    isSaving.value = false;
  }
}
    
    // Show remove confirmation modal
    const confirmRemoveMajor = (major) => {
      majorToRemove.value = major
      showRemoveModal.value = true
    }
    
    // Cancel remove major
    const cancelRemoveMajor = () => {
      showRemoveModal.value = false
      majorToRemove.value = null
    }
    
    // Remove major from method
    const removeMajorFromMethod = async () => {
      if (!majorToRemove.value) return
      
      try {
        isRemoving.value = true
        
        await AdmissionMethodMajorController.deleteAdmissionMethodMajor(majorToRemove.value.id)
        
        // Remove from lists
        majors.value = majors.value.filter(m => m.id !== majorToRemove.value.id)
        filterMajors()
        
        // Close modal
        showRemoveModal.value = false
        majorToRemove.value = null
        
        // Reload available majors
        await loadAvailableMajors()
        
        alert('Xóa ngành khỏi phương thức tuyển sinh thành công')
      } catch (err) {
        alert(`Lỗi: ${err.message}`)
      } finally {
        isRemoving.value = false
      }
    }

    onMounted(() => {
      loadData()
    })

    return {
      majors,
      filteredMajors,
      availableMajors,
      subjects,
      methodName,
      loading,
      error,
      searchQuery,
      formData,
      formErrors,
      formError,
      showModal,
      isEdit,
      isSaving,
      selectedRelationId,
      showRemoveModal,
      majorToRemove,
      isRemoving,
      filterMajors,
      getSubjectName,
      showAddMajorModal,
      showEditMajorModal,
      cancelModal,
      saveAdmissionMethodMajor,
      confirmRemoveMajor,
      cancelRemoveMajor,
      removeMajorFromMethod,
      listMajors
    }
  }
}
</script>

<style scoped>
.admin-admission-method-majors {
  width: 100%;
}

.admin-page-header {
  margin-bottom: 2rem;
}

.admin-page-title {
  font-size: 1.75rem;
  font-weight: 600;
  color: #0B2942;
  margin-bottom: 0.5rem;
}

.admin-page-description {
  color: #6c757d;
  font-size: 0.95rem;
}

.admin-card {
  background-color: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
  padding: 1.5rem;
  margin-bottom: 1.5rem;
  transition: all 0.3s ease;
}

.admin-card:hover {
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
}

.btn-back {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: #f8f9fa;
  color: #0B2942;
  text-decoration: none;
  margin-right: 1rem;
  transition: all 0.2s ease;
}

.btn-back:hover {
  background-color: #e9ecef;
  transform: translateX(-2px);
}

.btn-create {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background-color: #0B2942;
  color: #fff;
  font-weight: 500;
  padding: 0.75rem 1.25rem;
  border-radius: 8px;
  text-decoration: none;
  transition: all 0.3s;
  border: none;
  cursor: pointer;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.btn-create:hover, .btn-create:focus {
  background-color: #4da0ff;
  color: #fff;
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

/* Search Box */
.search-box {
  position: relative;
}

.search-icon {
  position: absolute;
  left: 15px;
  top: 50%;
  transform: translateY(-50%);
  color: #95a5a6;
}

.search-input {
  width: 100%;
  padding: 0.75rem 0.75rem 0.75rem 40px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  font-size: 0.95rem;
  transition: all 0.3s;
}

.search-input:focus {
  outline: none;
  border-color: #4da0ff;
  box-shadow: 0 0 0 3px rgba(77, 160, 255, 0.25);
}

/* Loading Animation */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem 0;
}

.spinner {
  margin: 0 auto;
  width: 70px;
  text-align: center;
}

.spinner > div {
  width: 18px;
  height: 18px;
  background-color: #0B2942;
  border-radius: 100%;
  display: inline-block;
  animation: sk-bouncedelay 1.4s infinite ease-in-out both;
  margin: 0 3px;
}

.spinner .bounce1 {
  animation-delay: -0.32s;
}

.spinner .bounce2 {
  animation-delay: -0.16s;
}

@keyframes sk-bouncedelay {
  0%, 80%, 100% { transform: scale(0); }
  40% { transform: scale(1.0); }
}

.loading-text {
  margin-top: 1rem;
  color: #6c757d;
  font-size: 1rem;
}

/* Error Message */
.error-message {
  background-color: #f8d7da;
  color: #721c24;
  padding: 1rem;
  border-radius: 8px;
  display: flex;
  align-items: center;
  margin-bottom: 1.5rem;
}

.error-icon {
  font-size: 1.25rem;
  margin-right: 0.75rem;
}

/* Table Styling */
.data-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
}

.data-table th {
  background-color: #f8f9fa;
  color: #0B2942;
  font-weight: 600;
  padding: 1rem;
  text-align: left;
  border-bottom: 2px solid #dee2e6;
  position: sticky;
  top: 0;
  z-index: 10;
}

.data-table td {
  padding: 1rem;
  vertical-align: middle;
  border-bottom: 1px solid #edf2f7;
}

.data-row {
  transition: background-color 0.3s;
}

.data-row:hover {
  background-color: rgba(77, 160, 255, 0.05);
}

.id-badge {
  font-weight: 600;
  color: #6c757d;
}

.code-badge {
  display: inline-block;
  padding: 0.35rem 0.75rem;
  border-radius: 50px;
  font-size: 0.85rem;
  font-weight: 500;
  background-color: #e3f2fd;
  color: #0d6efd;
}

.name-text {
  font-weight: 500;
  color: #0B2942;
}

.faculty-link {
  color: #4da0ff;
  text-decoration: none;
  transition: all 0.3s;
}

.faculty-link:hover {
  text-decoration: underline;
}

.quota-badge {
  display: inline-block;
  padding: 0.35rem 0.75rem;
  border-radius: 50px;
  font-size: 0.85rem;
  font-weight: 500;
  background-color: #e3faeb;
  color: #198754;
}

.score-badge {
  display: inline-block;
  padding: 0.35rem 0.75rem;
  border-radius: 50px;
  font-size: 0.85rem;
  font-weight: 500;
  background-color: #fff3cd;
  color: #856404;
}

.subject-badge {
  display: inline-block;
  padding: 0.35rem 0.75rem;
  border-radius: 50px;
  font-size: 0.85rem;
  font-weight: 500;
  background-color: #f5e6ff;
  color: #6f42c1;
}

.subscore-badge {
  display: inline-block;
  padding: 0.35rem 0.75rem;
  border-radius: 50px;
  font-size: 0.85rem;
  font-weight: 500;
  background-color: #d1ecf1;
  color: #0c5460;
}

.none-badge {
  display: inline-block;
  padding: 0.35rem 0.75rem;
  border-radius: 50px;
  font-size: 0.85rem;
  font-weight: 500;
  background-color: #f8f9fa;
  color: #6c757d;
}

.action-buttons {
  display: flex;
  gap: 0.5rem;
}

.btn-action {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border-radius: 8px;
  border: none;
  background-color: transparent;
  transition: all 0.3s ease;
}

.btn-action.view {
  color: #17a2b8;
}

.btn-action.edit {
  color: #0d6efd;
}

.btn-action.delete {
  color: #dc3545;
}

.btn-action:hover {
  background-color: #f8f9fa;
  transform: translateY(-2px);
}

.btn-action.view:hover {
  color: #17a2b8;
  background-color: rgba(23, 162, 184, 0.1);
}

.btn-action.edit:hover {
  color: #0d6efd;
  background-color: rgba(13, 110, 253, 0.1);
}

.btn-action.delete:hover {
  color: #dc3545;
  background-color: rgba(220, 53, 69, 0.1);
}

/* Empty State */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem 0;
  text-align: center;
}

.empty-icon {
  font-size: 3rem;
  color: #6c757d;
  margin-bottom: 1rem;
}

.empty-state h4 {
  font-size: 1.25rem;
  color: #0B2942;
  margin-bottom: 0.5rem;
}

.empty-state p {
  color: #6c757d;
  margin-bottom: 1.5rem;
}

.btn-create-empty {
  display: inline-flex;
  align-items: center;
  background-color: #0B2942;
  color: #fff;
  padding: 0.75rem 1.25rem;
  border-radius: 8px;
  text-decoration: none;
  border: none;
  transition: all 0.3s;
}

.btn-create-empty:hover {
  background-color: #4da0ff;
  color: #fff;
}

/* Modal Styling */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1050;
}

.modal-content {
  background-color: #fff;
  border-radius: 12px;
  width: 90%;
  max-width: 500px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
  overflow: hidden;
}

.modal-header {
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #e9ecef;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.modal-title {
  font-size: 1.25rem;
  color: #0B2942;
  margin: 0;
}

.btn-close {
  background: transparent;
  border: none;
  font-size: 1.5rem;
  line-height: 1;
  color: #6c757d;
  cursor: pointer;
}

.modal-body {
  padding: 1.5rem;
}

.modal-footer {
  padding: 1rem 1.5rem;
  border-top: 1px solid #e9ecef;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 0.5rem;
}

.form-group {
  margin-bottom: 1.25rem;
}

.form-group label {
  display: block;
  font-weight: 500;
  margin-bottom: 0.5rem;
  color: #0B2942;
}

.required {
  color: #dc3545;
}

.form-control {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  font-size: 0.95rem;
  transition: all 0.3s;
}

.form-control:focus {
  outline: none;
  border-color: #4da0ff;
  box-shadow: 0 0 0 3px rgba(77, 160, 255, 0.25);
}

.form-control.is-invalid {
  border-color: #dc3545;
}

.invalid-feedback {
  color: #dc3545;
  font-size: 0.875em;
  margin-top: 0.25rem;
}

.form-text {
  color: #6c757d;
  font-size: 0.875em;
  margin-top: 0.25rem;
}

.text-info {
  color: #17a2b8;
  margin-top: 1rem;
}

.alert {
  padding: 1rem;
  margin: 1rem 0;
  border-radius: 8px;
}

.alert-danger {
  background-color: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c2c7;
}

.btn-cancel {
  padding: 0.5rem 1rem;
  background-color: #f8f9fa;
  color: #6c757d;
  border: 1px solid #e0e0e0;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-cancel:hover {
  background-color: #e9ecef;
  color: #0B2942;
}

.btn-add {
  padding: 0.5rem 1rem;
  background-color: #0B2942;
  color: #fff;
  border: none;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-add:hover:not(:disabled) {
  background-color: #4da0ff;
}

.btn-add:disabled {
  background-color: #e9ecef;
  color: #6c757d;
  cursor: not-allowed;
}

.btn-delete {
  padding: 0.5rem 1rem;
  background-color: #dc3545;
  color: #fff;
  border: none;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-delete:hover:not(:disabled) {
  background-color: #c82333;
}

.btn-delete:disabled {
  background-color: #e9ecef;
  color: #6c757d;
  cursor: not-allowed;
}

@media (max-width: 768px) {
  .admin-page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  
  .btn-create {
    width: 100%;
  }
}
</style>
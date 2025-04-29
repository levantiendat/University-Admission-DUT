<template>
  <div class="admin-subject-group-create">
    <div class="admin-page-header">
      <div class="d-flex align-items-center">
        <router-link to="/admins/subject-groups" class="btn-back">
          <i class="bi bi-arrow-left"></i>
        </router-link>
        <div>
          <h2 class="admin-page-title">Tạo tổ hợp môn thi mới</h2>
          <p class="admin-page-description">Thêm tổ hợp môn thi mới vào hệ thống</p>
        </div>
      </div>
    </div>

    <div class="admin-card mb-4">
      <!-- Thông tin cơ bản của tổ hợp -->
      <h3 class="section-title">Thông tin cơ bản</h3>
      <form class="create-form">
        <div class="form-group">
          <label for="name">Tên tổ hợp môn thi <span class="required">*</span></label>
          <input 
            type="text" 
            id="name" 
            v-model="formData.name" 
            class="form-control" 
            required
            :class="{ 'is-invalid': errors.name }"
            placeholder="Ví dụ: Toán + Lý + Hóa, Văn + Sử + Địa..."
          >
          <div v-if="errors.name" class="invalid-feedback">{{ errors.name }}</div>
        </div>
      </form>
      
      <!-- Thêm môn học vào tổ hợp -->
      <h3 class="section-title mt-4">Thêm môn thi vào tổ hợp</h3>
      
      <div class="selected-subjects mb-4">
        <div class="row">
          <div v-for="(subject, index) in selectedSubjects" :key="index" class="col-md-4 mb-3">
            <div class="subject-item">
              <div class="subject-info">
                <span class="subject-name">{{ subject.name }}</span>
                <span class="coefficient-badge">Hệ số: {{ subject.coefficient }}</span>
              </div>
              <div class="subject-actions">
                <button class="btn-edit-subject" @click="editSubject(index)" title="Sửa hệ số">
                  <i class="bi bi-pencil"></i>
                </button>
                <button class="btn-remove-subject" @click="removeSubject(index)" title="Xóa môn thi">
                  <i class="bi bi-x"></i>
                </button>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Empty state for selected subjects -->
        <div v-if="selectedSubjects.length === 0" class="empty-subjects">
          <p><i class="bi bi-info-circle me-2"></i>Chưa có môn thi nào được thêm vào tổ hợp</p>
        </div>
      </div>
      
      <!-- Form thêm môn học -->
      <div class="add-subject-form">
        <div class="row">
          <div class="col-md-5">
            <div class="form-group">
              <label for="subject-select">Chọn môn thi</label>
              <select 
                id="subject-select" 
                v-model="currentSubject.id" 
                class="form-control"
                :disabled="availableSubjects.length === 0"
              >
                <option value="" disabled selected>Chọn môn thi</option>
                <option v-for="subject in availableSubjects" :key="subject.id" :value="subject.id">
                  {{ subject.name }}
                </option>
              </select>
            </div>
          </div>
          <div class="col-md-3">
            <div class="form-group">
              <label for="coefficient">Hệ số</label>
              <input 
                type="number" 
                id="coefficient" 
                v-model="currentSubject.coefficient" 
                class="form-control" 
                min="0.1" 
                step="0.1"
                placeholder="Mặc định: 1.0"
                :disabled="!currentSubject.id"
              >
            </div>
          </div>
          <div class="col-md-4">
            <div class="form-group d-flex align-items-end h-100">
              <button 
                type="button" 
                class="btn-add-subject" 
                @click="addSubjectToList" 
                :disabled="!currentSubject.id"
              >
                <i class="bi bi-plus-circle me-2"></i>Thêm môn thi
              </button>
            </div>
          </div>
        </div>
        
        <p class="text-info" v-if="availableSubjects.length === 0">
          <i class="bi bi-info-circle me-1"></i>
          Tất cả môn thi đã được thêm vào tổ hợp này hoặc chưa có môn thi nào trong hệ thống.
          <router-link to="/admins/subjects/create" class="create-subject-link">Tạo môn thi mới</router-link>
        </p>
      </div>

      <div v-if="errorMessage" class="alert alert-danger mt-3">{{ errorMessage }}</div>

      <div class="form-actions mt-4">
        <button type="button" class="btn-create" :disabled="isCreating || selectedSubjects.length === 0" @click="createSubjectGroup">
          <i class="bi bi-plus-circle me-2"></i>
          {{ isCreating ? 'Đang tạo...' : 'Tạo tổ hợp' }}
        </button>
        <button type="button" class="btn-reset" @click="resetForm">
          <i class="bi bi-arrow-repeat me-2"></i>
          Nhập lại
        </button>
      </div>
    </div>
    
    <!-- Edit Subject Modal -->
    <div v-if="showEditModal" class="modal-overlay" @click="cancelEdit">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h4 class="modal-title">Sửa hệ số môn thi</h4>
          <button type="button" class="btn-close" @click="cancelEdit"></button>
        </div>
        <div class="modal-body">
          <div class="subject-edit-info">
            <strong>Môn thi:</strong> {{ getSubjectName(editSubjectData.id) }}
          </div>

          <div class="form-group">
            <label for="edit-coefficient">Hệ số <span class="required">*</span></label>
            <input 
              type="number" 
              id="edit-coefficient" 
              v-model="editSubjectData.coefficient" 
              class="form-control" 
              min="0.1" 
              step="0.1"
              required
              :class="{ 'is-invalid': editError }"
            >
            <div v-if="editError" class="invalid-feedback">{{ editError }}</div>
            <small class="form-text text-muted">Hệ số quy định trọng số của môn thi này trong tổ hợp.</small>
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn-cancel" @click="cancelEdit">Hủy</button>
          <button type="button" class="btn-save" @click="saveEdit">
            Lưu thay đổi
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { reactive, ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import SubjectGroupController from '@/controllers/admins/SubjectGroupController'
import SubjectController from '@/controllers/admins/SubjectController'
import SubjectGroupDetailController from '@/controllers/admins/SubjectGroupDetailController'

export default {
  name: 'AdminSubjectGroupCreate',
  setup() {
    const router = useRouter()
    const formData = reactive({
      name: ''
    })
    
    const allSubjects = ref([])
    const selectedSubjects = ref([])
    const currentSubject = reactive({
      id: '',
      name: '',
      coefficient: 1
    })
    
    // Computed property: available subjects (not yet in the list)
    const availableSubjects = computed(() => {
      const selectedIds = selectedSubjects.value.map(s => s.id)
      return allSubjects.value.filter(subject => !selectedIds.includes(subject.id))
    })
    
    const isCreating = ref(false)
    const errorMessage = ref('')
    const errors = reactive({
      name: ''
    })
    
    // Edit subject modal state
    const showEditModal = ref(false)
    const editSubjectData = reactive({
      id: null,
      name: '',
      coefficient: 1,
      index: -1
    })
    const editError = ref('')

    // Reset form
    const resetForm = () => {
      formData.name = ''
      selectedSubjects.value = []
      currentSubject.id = ''
      currentSubject.name = ''
      currentSubject.coefficient = 1
      
      // Clear errors
      errors.name = ''
      errorMessage.value = ''
    }

    // Validate form
    const validateForm = () => {
      let isValid = true
      
      // Clear previous errors
      errors.name = ''
      errorMessage.value = ''
      
      // Name validation
      if (!formData.name.trim()) {
        errors.name = 'Tên tổ hợp môn thi không được để trống'
        isValid = false
      }
      
      // Check if at least one subject is selected
      if (selectedSubjects.value.length === 0) {
        errorMessage.value = 'Vui lòng thêm ít nhất một môn thi vào tổ hợp'
        isValid = false
      }
      
      return isValid
    }
    
    // Get subject name by id
    const getSubjectName = (subjectId) => {
      const subject = allSubjects.value.find(s => s.id === subjectId)
      return subject ? subject.name : 'Không xác định'
    }
    
    // Add subject to list
    const addSubjectToList = () => {
      if (!currentSubject.id) return
      
      const coefficient = parseFloat(currentSubject.coefficient) || 1
      if (coefficient <= 0) {
        alert('Hệ số phải là số dương')
        return
      }
      
      const subject = allSubjects.value.find(s => s.id === currentSubject.id)
      if (!subject) return
      
      selectedSubjects.value.push({
        id: subject.id,
        name: subject.name,
        coefficient: coefficient
      })
      
      // Reset current subject
      currentSubject.id = ''
      currentSubject.name = ''
      currentSubject.coefficient = 1
    }
    
    // Remove subject from list
    const removeSubject = (index) => {
      selectedSubjects.value.splice(index, 1)
    }
    
    // Edit subject
    const editSubject = (index) => {
      const subject = selectedSubjects.value[index]
      
      editSubjectData.id = subject.id
      editSubjectData.name = subject.name
      editSubjectData.coefficient = subject.coefficient
      editSubjectData.index = index
      
      showEditModal.value = true
    }
    
    // Save edit
    const saveEdit = () => {
      const coefficient = parseFloat(editSubjectData.coefficient)
      
      if (isNaN(coefficient) || coefficient <= 0) {
        editError.value = 'Hệ số phải là số dương'
        return
      }
      
      const index = editSubjectData.index
      if (index >= 0 && index < selectedSubjects.value.length) {
        selectedSubjects.value[index].coefficient = coefficient
      }
      
      showEditModal.value = false
    }
    
    // Cancel edit
    const cancelEdit = () => {
      showEditModal.value = false
      editError.value = ''
    }

    // Create subject group
    const createSubjectGroup = async () => {
      try {
        // Validate form
        if (!validateForm()) {
          return
        }
        
        isCreating.value = true
        errorMessage.value = ''
        
        // Create subject group first
        const newGroup = await SubjectGroupController.createSubjectGroup({
          name: formData.name.trim()
        })
        
        // Then add subjects with their coefficients
        const promises = selectedSubjects.value.map(subject => {
          return SubjectGroupDetailController.createSubjectGroupDetail({
            group_id: newGroup.id,
            subject_id: subject.id,
            coefficient: parseFloat(subject.coefficient) || 1
          })
        })
        
        await Promise.all(promises)
        
        alert('Tạo tổ hợp môn thi mới thành công')
        router.push(`/admins/subject-groups/${newGroup.id}`)
      } catch (err) {
        errorMessage.value = `Không thể tạo tổ hợp môn thi: ${err.message}`
      } finally {
        isCreating.value = false
      }
    }
    
    // Load all subjects
    const loadSubjects = async () => {
      try {
        const subjects = await SubjectController.getAllSubjects()
        allSubjects.value = subjects
      } catch (err) {
        console.error('Error loading subjects:', err)
        errorMessage.value = 'Không thể tải danh sách môn thi. Vui lòng thử lại sau.'
      }
    }

    onMounted(() => {
      loadSubjects()
    })

    return {
      formData,
      isCreating,
      errorMessage,
      errors,
      allSubjects,
      selectedSubjects,
      currentSubject,
      availableSubjects,
      showEditModal,
      editSubjectData,
      editError,
      resetForm,
      createSubjectGroup,
      getSubjectName,
      addSubjectToList,
      removeSubject,
      editSubject,
      saveEdit,
      cancelEdit
    }
  }
}
</script>

<style scoped>
.admin-subject-group-create {
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

.admin-card {
  background-color: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
  padding: 2rem;
  transition: all 0.3s ease;
}

.admin-card:hover {
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
}

.section-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #0B2942;
  margin-bottom: 1.5rem;
}

/* Form Styling */
.create-form {
  width: 100%;
  max-width: 700px;
}

.form-group {
  margin-bottom: 1.5rem;
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
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 12 12' width='12' height='12' fill='none' stroke='%23dc3545'%3e%3ccircle cx='6' cy='6' r='4.5'/%3e%3cpath stroke-linejoin='round' d='M5.8 3.6h.4L6 6.5z'/%3e%3ccircle cx='6' cy='8.2' r='.6' fill='%23dc3545' stroke='none'/%3e%3c/svg%3e");
  background-repeat: no-repeat;
  background-position: right calc(0.375em + 0.1875rem) center;
  background-size: calc(0.75em + 0.375rem) calc(0.75em + 0.375rem);
}

.form-control:disabled {
  background-color: #f8f9fa;
  cursor: not-allowed;
}

.invalid-feedback {
  color: #dc3545;
  font-size: 0.875em;
  margin-top: 0.25rem;
}

/* Selected Subjects Styling */
.selected-subjects {
  margin-top: 1.5rem;
  margin-bottom: 1.5rem;
}

.subject-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #f8f9fa;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 0.75rem 1rem;
  transition: all 0.3s ease;
}

.subject-item:hover {
  background-color: #e9ecef;
  border-color: #ced4da;
}

.subject-info {
  display: flex;
  flex-direction: column;
}

.subject-name {
  font-weight: 500;
  color: #0B2942;
  margin-bottom: 0.25rem;
}

.coefficient-badge {
  display: inline-block;
  font-size: 0.8rem;
  padding: 0.2rem 0.5rem;
  border-radius: 50px;
  background-color: #e3f2fd;
  color: #0d6efd;
}

.subject-actions {
  display: flex;
  gap: 0.5rem;
}

.btn-edit-subject, .btn-remove-subject {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 30px;
  height: 30px;
  border-radius: 6px;
  border: none;
  background-color: transparent;
  transition: all 0.3s ease;
}

.btn-edit-subject {
  color: #0B2942;
}

.btn-remove-subject {
  color: #dc3545;
}

.btn-edit-subject:hover, .btn-remove-subject:hover {
  background-color: #fff;
}

.btn-edit-subject:hover {
  color: #4da0ff;
}

.btn-remove-subject:hover {
  color: #c82333;
}

/* Empty subjects state */
.empty-subjects {
  text-align: center;
  padding: 1.5rem;
  background-color: #f8f9fa;
  border: 1px dashed #ced4da;
  border-radius: 8px;
}

.empty-subjects p {
  color: #6c757d;
  margin: 0;
}

/* Add Subject Form */
.add-subject-form {
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid #e9ecef;
}

.btn-add-subject {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.75rem 1rem;
  background-color: #0B2942;
  color: #fff;
  border: none;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
  width: 100%;
}

.btn-add-subject:hover:not(:disabled) {
  background-color: #4da0ff;
}

.btn-add-subject:disabled {
  background-color: #e9ecef;
  color: #6c757d;
  cursor: not-allowed;
}

.text-info {
  color: #0d6efd;
  margin: 1rem 0;
}

.create-subject-link {
  color: #0d6efd;
  font-weight: 500;
  text-decoration: none;
  margin-left: 0.5rem;
}

.create-subject-link:hover {
  text-decoration: underline;
}

.form-actions {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
}

.btn-create {
  padding: 0.75rem 1.5rem;
  background-color: #0B2942;
  border: none;
  border-radius: 8px;
  color: #fff;
  font-weight: 500;
  transition: all 0.3s;
  display: inline-flex;
  align-items: center;
}

.btn-create:hover:not(:disabled) {
  background-color: #4da0ff;
}

.btn-create:disabled {
  background-color: #e9ecef;
  color: #6c757d;
  cursor: not-allowed;
}

.btn-reset {
  padding: 0.75rem 1.5rem;
  background-color: #f8f9fa;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  color: #6c757d;
  font-weight: 500;
  transition: all 0.3s;
  display: inline-flex;
  align-items: center;
}

.btn-reset:hover {
  background-color: #e9ecef;
  color: #0B2942;
}

/* Alert */
.alert {
  padding: 1rem;
  margin-bottom: 1rem;
  border-radius: 8px;
}

.alert-danger {
  background-color: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c2c7;
}

.alert-info {
  background-color: #e3f2fd;
  color: #084298;
  border: 1px solid #b6d4fe;
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

.subject-edit-info {
  margin-bottom: 1.5rem;
  color: #0B2942;
  font-size: 1rem;
}

.modal-footer {
  padding: 1rem 1.5rem;
  border-top: 1px solid #e9ecef;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 0.5rem;
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

.btn-save {
  padding: 0.5rem 1rem;
  background-color: #0B2942;
  color: #fff;
  border: none;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-save:hover {
  background-color: #4da0ff;
}

.form-text {
  font-size: 0.85rem;
  margin-top: 0.25rem;
}

.text-muted {
  color: #6c757d;
}

@media (max-width: 768px) {
  .form-actions {
    flex-direction: column;
  }
  
  .btn-create, .btn-reset {
    width: 100%;
  }
}
</style>
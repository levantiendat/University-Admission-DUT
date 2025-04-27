<template>
    <div class="admin-subject-group-detail">
      <div class="admin-page-header">
        <div class="d-flex align-items-center">
          <router-link to="/admins/subject-groups" class="btn-back">
            <i class="bi bi-arrow-left"></i>
          </router-link>
          <div>
            <h2 class="admin-page-title">Chi tiết tổ hợp môn thi</h2>
            <p class="admin-page-description">Quản lý thông tin tổ hợp và các môn thi trong tổ hợp</p>
          </div>
        </div>
      </div>
  
      <!-- Loading State -->
      <div v-if="loading" class="loading-container">
        <div class="spinner">
          <div class="bounce1"></div>
          <div class="bounce2"></div>
          <div class="bounce3"></div>
        </div>
        <p class="loading-text">Đang tải thông tin tổ hợp môn thi...</p>
      </div>
  
      <!-- Error State -->
      <div v-else-if="error" class="error-message">
        <i class="bi bi-exclamation-triangle-fill error-icon"></i>
        <span>{{ error }}</span>
      </div>
  
      <div v-else>
        <!-- Basic Info Card -->
        <div class="admin-card mb-4">
          <div class="row">
            <div class="col-md-6">
              <div class="group-info">
                <h3 class="group-name">{{ group.name }}</h3>
                <div class="group-meta">
                  <div class="group-meta-item">
                    <span class="meta-label">ID:</span>
                    <span class="meta-value">#{{ group.id }}</span>
                  </div>
                  <div class="group-meta-item">
                    <span class="meta-label">Ngày tạo:</span>
                    <span class="meta-value">{{ formatDate(group.created_at) }}</span>
                  </div>
                  <div class="group-meta-item">
                    <span class="meta-label">Cập nhật:</span>
                    <span class="meta-value">{{ formatDate(group.updated_at) }}</span>
                  </div>
                </div>
              </div>
            </div>
  
            <div class="col-md-6">
              <div class="group-actions">
                <button class="btn-edit" @click="showEditModal = true">
                  <i class="bi bi-pencil me-2"></i>Đổi tên tổ hợp
                </button>
                <button class="btn-delete" @click="confirmDeleteGroup">
                  <i class="bi bi-trash me-2"></i>Xóa tổ hợp
                </button>
              </div>
            </div>
          </div>
        </div>
  
        <!-- Subject List Card -->
        <div class="admin-card mb-4">
          <div class="card-header d-flex justify-content-between align-items-center">
            <h3 class="section-title mb-0">Các môn thi trong tổ hợp</h3>
            <button class="btn-add-subject" @click="showAddSubjectModal = true">
              <i class="bi bi-plus-circle me-2"></i>Thêm môn thi
            </button>
          </div>
  
          <div class="table-responsive" v-if="groupSubjects.length > 0">
            <table class="data-table">
              <thead>
                <tr>
                  <th>STT</th>
                  <th>Môn thi</th>
                  <th>Hệ số</th>
                  <th>Thao tác</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(detail, index) in groupSubjects" :key="detail.id" class="data-row">
                  <td>{{ index + 1 }}</td>
                  <td>{{ getSubjectName(detail.subject_id) }}</td>
                  <td>
                    <span class="coefficient-badge">{{ detail.coefficient }}</span>
                  </td>
                  <td>
                    <div class="action-buttons">
                      <button 
                        class="btn-action edit"
                        @click="openEditSubjectModal(detail)"
                        title="Sửa hệ số"
                      >
                        <i class="bi bi-pencil-square"></i>
                      </button>
                      <button 
                        class="btn-action delete"
                        @click="confirmDeleteSubject(detail)"
                        title="Xóa môn thi khỏi tổ hợp"
                      >
                        <i class="bi bi-trash"></i>
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
  
          <!-- Empty State for Subjects -->
          <div v-else class="empty-state">
            <i class="bi bi-journal-x empty-icon"></i>
            <h4>Chưa có môn thi nào trong tổ hợp này</h4>
            <p>Hãy thêm các môn thi vào tổ hợp</p>
            <button @click="showAddSubjectModal = true" class="btn-add-empty">
              <i class="bi bi-plus-circle me-2"></i>Thêm môn thi
            </button>
          </div>
        </div>
  
        <!-- Applied Majors List -->
        <div class="admin-card">
  <div class="card-header d-flex justify-content-between align-items-center">
    <h3 class="section-title mb-0">Các ngành áp dụng tổ hợp này</h3>
    <button class="btn-add-major" @click="showAddMajorModal = true">
      <i class="bi bi-plus-circle me-2"></i>Thêm ngành áp dụng
    </button>
  </div>

  <div v-if="loadingMajors" class="text-center py-4">
    <div class="spinner">
      <div class="bounce1"></div>
      <div class="bounce2"></div>
      <div class="bounce3"></div>
    </div>
    <p class="loading-text">Đang tải danh sách ngành...</p>
  </div>

  <div v-else-if="majorsError" class="alert alert-danger mx-3 my-3">
    {{ majorsError }}
  </div>

  <div class="table-responsive" v-else-if="groupMajors.length > 0">
    <table class="data-table">
      <thead>
        <tr>
          <th>Ngành</th>
          <th>Phương thức tuyển sinh</th>
          <th>Thao tác</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="majorRelation in groupMajors" :key="majorRelation.id" class="data-row">
          <td>
            <span class="major-name">{{ majorRelation.major.name }}</span>
          </td>
          <td>
            <span class="method-name">{{ majorRelation.admission_method.name }}</span>
          </td>
          <td>
            <div class="action-buttons">
              <router-link :to="`/admins/majors/${majorRelation.major.id}`" class="btn-action view" title="Xem chi tiết ngành">
                <i class="bi bi-eye"></i>
              </router-link>
              <button 
                class="btn-action delete"
                @click="confirmRemoveMajor(majorRelation)"
                title="Xóa ngành khỏi tổ hợp"
              >
                <i class="bi bi-trash"></i>
              </button>
            </div>
          </td>
        </tr>
      </tbody>
    </table>
  </div>

  <!-- Empty State for Majors -->
  <div v-else class="empty-state">
    <i class="bi bi-building empty-icon"></i>
    <h4>Chưa có ngành nào áp dụng tổ hợp này</h4>
    <p>Hãy thêm ngành vào tổ hợp này</p>
    <button @click="showAddMajorModal = true" class="btn-add-empty">
      <i class="bi bi-plus-circle me-2"></i>Thêm ngành áp dụng
    </button>
  </div>
</div>

<!-- Add these new modals to the component -->

<!-- Add Major Modal -->
<div v-if="showAddMajorModal" class="modal-overlay" @click="cancelAddMajor">
  <div class="modal-content" @click.stop>
    <div class="modal-header">
      <h4 class="modal-title">Thêm ngành áp dụng tổ hợp</h4>
      <button type="button" class="btn-close" @click="cancelAddMajor"></button>
    </div>
    <div class="modal-body">
      <div class="form-group">
        <label for="admission-method-major-select">Chọn phương thức tuyển sinh-ngành <span class="required">*</span></label>
        <select 
          id="admission-method-major-select" 
          v-model="addMajorData.admission_method_major_id" 
          class="form-control" 
          :class="{ 'is-invalid': addMajorErrors.admission_method_major_id }"
        >
          <option value="" disabled selected>Chọn phương thức tuyển sinh-ngành</option>
          <option v-for="relation in availableAdmissionMethodMajors" :key="relation.id" :value="relation.id">
            {{ relation.major_name }} - {{ getAdmissionMethodName(relation.admission_method_id) }}
          </option>
        </select>
        <div v-if="addMajorErrors.admission_method_major_id" class="invalid-feedback">{{ addMajorErrors.admission_method_major_id }}</div>
      </div>
      
      <div v-if="addMajorError" class="alert alert-danger">{{ addMajorError }}</div>
      
      <p class="text-info" v-if="availableAdmissionMethodMajors.length === 0">
        <i class="bi bi-info-circle me-1"></i>
        Tất cả ngành đã được thêm vào tổ hợp này hoặc chưa có ngành nào có phương thức tuyển sinh phù hợp.
      </p>
    </div>
    <div class="modal-footer">
      <button type="button" class="btn-cancel" @click="cancelAddMajor">Hủy</button>
      <button 
        type="button" 
        class="btn-add" 
        @click="addMajorToSubjectGroup" 
        :disabled="isAddingMajor || !addMajorData.admission_method_major_id"
      >
        <span v-if="isAddingMajor">Đang thêm...</span>
        <span v-else>Thêm ngành</span>
      </button>
    </div>
  </div>
</div>

<!-- Remove Major Confirmation Modal -->
<div v-if="showRemoveMajorModal" class="modal-overlay" @click="cancelRemoveMajor">
  <div class="modal-content" @click.stop>
    <div class="modal-header">
      <h4 class="modal-title">Xác nhận xóa ngành</h4>
      <button type="button" class="btn-close" @click="cancelRemoveMajor"></button>
    </div>
    <div class="modal-body">
      <p>Bạn có chắc chắn muốn xóa ngành <strong>{{ majorToRemove?.major?.name }}</strong> khỏi tổ hợp này?</p>
    </div>
    <div class="modal-footer">
      <button type="button" class="btn-cancel" @click="cancelRemoveMajor">Hủy</button>
      <button 
        type="button" 
        class="btn-delete" 
        @click="removeMajorFromSubjectGroup" 
        :disabled="isRemovingMajor"
      >
        <span v-if="isRemovingMajor">Đang xóa...</span>
        <span v-else>Xác nhận xóa</span>
      </button>
    </div>
  </div>
</div>
      </div>
  
      <!-- Edit Group Name Modal -->
      <div v-if="showEditModal" class="modal-overlay" @click="showEditModal = false">
        <div class="modal-content" @click.stop>
          <div class="modal-header">
            <h4 class="modal-title">Đổi tên tổ hợp môn thi</h4>
            <button type="button" class="btn-close" @click="showEditModal = false"></button>
          </div>
          <div class="modal-body">
            <div class="form-group">
              <label for="group-name">Tên tổ hợp môn thi <span class="required">*</span></label>
              <input 
                type="text" 
                id="group-name" 
                v-model="editGroupData.name" 
                class="form-control" 
                required
                :class="{ 'is-invalid': editError }"
              >
              <div v-if="editError" class="invalid-feedback">{{ editError }}</div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn-cancel" @click="showEditModal = false">Hủy</button>
            <button type="button" class="btn-save" @click="updateGroupName" :disabled="isUpdating">
              <span v-if="isUpdating">Đang lưu...</span>
              <span v-else>Lưu thay đổi</span>
            </button>
          </div>
        </div>
      </div>
  
      <!-- Add Subject Modal -->
      <div v-if="showAddSubjectModal" class="modal-overlay" @click="cancelAddSubject">
        <div class="modal-content" @click.stop>
          <div class="modal-header">
            <h4 class="modal-title">Thêm môn thi vào tổ hợp</h4>
            <button type="button" class="btn-close" @click="cancelAddSubject"></button>
          </div>
          <div class="modal-body">
            <div class="form-group">
              <label for="subject-select">Chọn môn thi <span class="required">*</span></label>
              <select 
                id="subject-select" 
                v-model="addSubjectData.subject_id" 
                class="form-control" 
                :class="{ 'is-invalid': addSubjectErrors.subject_id }"
              >
                <option value="" disabled selected>Chọn môn thi</option>
                <option v-for="subject in availableSubjects" :key="subject.id" :value="subject.id">
                  {{ subject.name }}
                </option>
              </select>
              <div v-if="addSubjectErrors.subject_id" class="invalid-feedback">{{ addSubjectErrors.subject_id }}</div>
            </div>
  
            <div class="form-group">
              <label for="coefficient">Hệ số</label>
              <input 
                type="number" 
                id="coefficient" 
                v-model="addSubjectData.coefficient" 
                class="form-control" 
                min="0.1" 
                step="0.1"
                :class="{ 'is-invalid': addSubjectErrors.coefficient }"
                placeholder="Mặc định: 1.0"
              >
              <div v-if="addSubjectErrors.coefficient" class="invalid-feedback">{{ addSubjectErrors.coefficient }}</div>
              <small class="form-text text-muted">Hệ số quy định trọng số của môn thi này trong tổ hợp.</small>
            </div>
            
            <div v-if="addSubjectError" class="alert alert-danger">{{ addSubjectError }}</div>
            
            <p class="text-info" v-if="availableSubjects.length === 0">
              <i class="bi bi-info-circle me-1"></i>
              Tất cả môn thi đã được thêm vào tổ hợp này hoặc chưa có môn thi nào trong hệ thống.
            </p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn-cancel" @click="cancelAddSubject">Hủy</button>
            <button 
              type="button" 
              class="btn-add" 
              @click="addSubjectToGroup" 
              :disabled="isAddingSubject || !addSubjectData.subject_id"
            >
              <span v-if="isAddingSubject">Đang thêm...</span>
              <span v-else>Thêm môn thi</span>
            </button>
          </div>
        </div>
      </div>
  
      <!-- Edit Subject Modal -->
      <div v-if="showEditSubjectModal" class="modal-overlay" @click="cancelEditSubject">
        <div class="modal-content" @click.stop>
          <div class="modal-header">
            <h4 class="modal-title">Sửa hệ số môn thi</h4>
            <button type="button" class="btn-close" @click="cancelEditSubject"></button>
          </div>
          <div class="modal-body">
            <div class="subject-edit-info">
              <strong>Môn thi:</strong> {{ getSubjectName(editSubjectData.subject_id) }}
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
                :class="{ 'is-invalid': editSubjectError }"
              >
              <div v-if="editSubjectError" class="invalid-feedback">{{ editSubjectError }}</div>
              <small class="form-text text-muted">Hệ số quy định trọng số của môn thi này trong tổ hợp.</small>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn-cancel" @click="cancelEditSubject">Hủy</button>
            <button 
              type="button" 
              class="btn-save" 
              @click="updateSubjectCoefficient" 
              :disabled="isEditingSubject"
            >
              <span v-if="isEditingSubject">Đang lưu...</span>
              <span v-else>Lưu thay đổi</span>
            </button>
          </div>
        </div>
      </div>
  
      <!-- Delete Subject Confirmation Modal -->
      <div v-if="showDeleteSubjectModal" class="modal-overlay" @click="cancelDeleteSubject">
        <div class="modal-content" @click.stop>
          <div class="modal-header">
            <h4 class="modal-title">Xác nhận xóa môn thi</h4>
            <button type="button" class="btn-close" @click="cancelDeleteSubject"></button>
          </div>
          <div class="modal-body">
            <p>Bạn có chắc chắn muốn xóa môn thi <strong>{{ getSubjectName(subjectToDelete?.subject_id) }}</strong> khỏi tổ hợp này?</p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn-cancel" @click="cancelDeleteSubject">Hủy</button>
            <button 
              type="button" 
              class="btn-delete" 
              @click="deleteSubjectFromGroup" 
              :disabled="isDeletingSubject"
            >
              <span v-if="isDeletingSubject">Đang xóa...</span>
              <span v-else>Xác nhận xóa</span>
            </button>
          </div>
        </div>
      </div>
  
      <!-- Delete Group Confirmation Modal -->
      <div v-if="showDeleteGroupModal" class="modal-overlay" @click="cancelDeleteGroup">
        <div class="modal-content" @click.stop>
          <div class="modal-header">
            <h4 class="modal-title">Xác nhận xóa tổ hợp</h4>
            <button type="button" class="btn-close" @click="cancelDeleteGroup"></button>
          </div>
          <div class="modal-body">
            <p>Bạn có chắc chắn muốn xóa tổ hợp môn thi <strong>{{ group.name }}</strong>?</p>
            <p class="text-danger">
              <i class="bi bi-exclamation-triangle me-2"></i>
              Thao tác này sẽ xóa tổ hợp môn thi và tất cả liên kết của nó với các ngành, và không thể khôi phục lại!
            </p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn-cancel" @click="cancelDeleteGroup">Hủy</button>
            <button 
              type="button" 
              class="btn-delete" 
              @click="deleteGroup" 
              :disabled="isDeletingGroup"
            >
              <span v-if="isDeletingGroup">Đang xóa...</span>
              <span v-else>Xác nhận xóa</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, reactive, onMounted } from 'vue'
  import { useRouter } from 'vue-router'
  import SubjectGroupController from '@/controllers/admins/SubjectGroupController'
  import SubjectController from '@/controllers/admins/SubjectController'
  import SubjectGroupDetailController from '@/controllers/admins/SubjectGroupDetailController'
  import AdmissionMethodMajorController from '@/controllers/admins/AdmissionMethodMajorController'
  import AdmissionMethodController from '@/controllers/admins/AdmissionMethodController'
  import SubjectGroupMajorController from '@/controllers/admins/SubjectGroupMajorController'
  
  export default {
    name: 'AdminSubjectGroupDetail',
    props: {
      groupId: {
        type: [String, Number],
        required: true
      }
    },
    setup(props) {
      const router = useRouter()
      const group = ref({})
      const groupSubjects = ref([])
      const allSubjects = ref([])
      const loading = ref(true)
      const error = ref(null)
      const groupMajors = ref([])
      const loadingMajors = ref(false)
      const majorsError = ref(null)
      
      // Edit group modal state
      const showEditModal = ref(false)
      const editGroupData = reactive({
        name: ''
      })
      const editError = ref('')
      const isUpdating = ref(false)
  
      // Add subject modal state
      const showAddSubjectModal = ref(false)
      const addSubjectData = reactive({
        group_id: parseInt(props.groupId),
        subject_id: '',
        coefficient: 1
      })
      const addSubjectError = ref('')
      const addSubjectErrors = reactive({
        subject_id: '',
        coefficient: ''
      })
      const isAddingSubject = ref(false)
  
      // Edit subject modal state
      const showEditSubjectModal = ref(false)
      const editSubjectData = reactive({
        id: null,
        subject_id: null,
        coefficient: null
      })
      const editSubjectError = ref('')
      const isEditingSubject = ref(false)
  
      // Delete subject modal state
      const showDeleteSubjectModal = ref(false)
      const subjectToDelete = ref(null)
      const isDeletingSubject = ref(false)
  
      // Delete group modal state
      const showDeleteGroupModal = ref(false)
      const isDeletingGroup = ref(false)
  
      // Computed property: available subjects (not yet in the group)
      const availableSubjects = ref([])

      // Add Major modal state
      const showAddMajorModal = ref(false)
      const addMajorData = reactive({
        group_id: parseInt(props.groupId),
        admission_method_major_id: ''
    })
    const addMajorError = ref('')
    const addMajorErrors = reactive({
        admission_method_major_id: ''
    })
    const isAddingMajor = ref(false)

    // Remove Major modal state
    const showRemoveMajorModal = ref(false)
    const majorToRemove = ref(null)
    const isRemovingMajor = ref(false)

    // Available admission method majors (not yet linked to this group)
    const availableAdmissionMethodMajors = ref([])
    const admissionMethods = ref([])
      
      // Update available subjects
      const updateAvailableSubjects = () => {
        const usedSubjectIds = groupSubjects.value.map(gs => gs.subject_id)
        availableSubjects.value = allSubjects.value.filter(subject => {
          return !usedSubjectIds.includes(subject.id)
        })
      }
  
      // Get subject name by id
      const getSubjectName = (subjectId) => {
        const subject = allSubjects.value.find(s => s.id === subjectId)
        return subject ? subject.name : 'Không xác định'
      }
  
      // Format date
      const formatDate = (dateString) => {
        if (!dateString) return 'N/A'
        
        const date = new Date(dateString)
        return new Intl.DateTimeFormat('vi-VN', { 
          day: '2-digit', 
          month: '2-digit', 
          year: 'numeric',
          hour: '2-digit',
          minute: '2-digit'
        }).format(date)
      }

      const getAdmissionMethodName = (methodId) => {
        const method = admissionMethods.value.find(m => m.id === methodId)
        return method ? method.name : 'Không xác định'
        }
  
      // Fetch data
      const fetchData = async () => {
  try {
    loading.value = true
    error.value = null

    // Load all subjects for reference
    const subjectsData = await SubjectController.getAllSubjects()
    allSubjects.value = subjectsData
    
    // Load group data
    const groupData = await SubjectGroupController.getSubjectGroupById(props.groupId)
    group.value = groupData
    editGroupData.name = groupData.name
    
    // Load group subjects
    const groupSubjectsData = await SubjectGroupDetailController.getSubjectGroupDetailsByGroup(props.groupId)
    groupSubjects.value = groupSubjectsData
    
    // Update available subjects
    updateAvailableSubjects()
    
    // Load majors that apply this subject group
    loadMajors()
    
    // Load admission methods for reference
    try {
      const methodsData = await AdmissionMethodController.getAllAdmissionMethods()
      admissionMethods.value = methodsData
    } catch (err) {
      console.error('Error loading admission methods:', err)
    }
    
  } catch (err) {
    error.value = `Không thể tải thông tin tổ hợp: ${err.message}`
  } finally {
    loading.value = false
  }
}
  
      // Update group name
      const updateGroupName = async () => {
        if (!editGroupData.name.trim()) {
          editError.value = 'Tên tổ hợp không được để trống'
          return
        }
        
        try {
          isUpdating.value = true
          editError.value = ''
          
          await SubjectGroupController.updateSubjectGroup(props.groupId, {
            name: editGroupData.name.trim()
          })
          
          // Update local data
          group.value.name = editGroupData.name.trim()
          
          // Close modal
          showEditModal.value = false
          
          alert('Cập nhật tên tổ hợp thành công')
        } catch (err) {
          editError.value = `Không thể cập nhật tên tổ hợp: ${err.message}`
        } finally {
          isUpdating.value = false
        }
      }
  
      // Add subject to group
      const addSubjectToGroup = async () => {
        // Validate
        let isValid = true
        addSubjectErrors.subject_id = ''
        addSubjectErrors.coefficient = ''
        addSubjectError.value = ''
        
        if (!addSubjectData.subject_id) {
          addSubjectErrors.subject_id = 'Vui lòng chọn môn thi'
          isValid = false
        }
        
        if (addSubjectData.coefficient && (isNaN(parseFloat(addSubjectData.coefficient)) || parseFloat(addSubjectData.coefficient) <= 0)) {
          addSubjectErrors.coefficient = 'Hệ số phải là số dương'
          isValid = false
        }
        
        if (!isValid) return
        
        try {
          isAddingSubject.value = true
          
          const data = {
            group_id: parseInt(props.groupId),
            subject_id: parseInt(addSubjectData.subject_id),
            coefficient: parseFloat(addSubjectData.coefficient) || 1
          }
          
          await SubjectGroupDetailController.createSubjectGroupDetail(data)
          
          // Reload group subjects
          const groupSubjectsData = await SubjectGroupDetailController.getSubjectGroupDetailsByGroup(props.groupId)
          groupSubjects.value = groupSubjectsData
          
          // Update available subjects
          updateAvailableSubjects()
          
          // Reset form and close modal
          addSubjectData.subject_id = ''
          addSubjectData.coefficient = 1
          showAddSubjectModal.value = false
          
          alert('Thêm môn thi vào tổ hợp thành công')
        } catch (err) {
          addSubjectError.value = `Không thể thêm môn thi: ${err.message}`
        } finally {
          isAddingSubject.value = false
        }
      }
  
      // Cancel add subject
      const cancelAddSubject = () => {
        showAddSubjectModal.value = false
        addSubjectData.subject_id = ''
        addSubjectData.coefficient = 1
        addSubjectError.value = ''
        addSubjectErrors.subject_id = ''
        addSubjectErrors.coefficient = ''
      }
  
      // Open edit subject modal
      const openEditSubjectModal = (detail) => {
        editSubjectData.id = detail.id
        editSubjectData.subject_id = detail.subject_id
        editSubjectData.coefficient = detail.coefficient
        editSubjectError.value = ''
        showEditSubjectModal.value = true
      }
  
      // Cancel edit subject
      const cancelEditSubject = () => {
        showEditSubjectModal.value = false
        editSubjectError.value = ''
      }
  
      // Update subject coefficient
      const updateSubjectCoefficient = async () => {
        if (isNaN(parseFloat(editSubjectData.coefficient)) || parseFloat(editSubjectData.coefficient) <= 0) {
          editSubjectError.value = 'Hệ số phải là số dương'
          return
        }
        
        try {
          isEditingSubject.value = true
          
          await SubjectGroupDetailController.updateSubjectGroupDetail(editSubjectData.id, {
            coefficient: parseFloat(editSubjectData.coefficient)
          })
          
          // Update local data
          const index = groupSubjects.value.findIndex(gs => gs.id === editSubjectData.id)
          if (index !== -1) {
            groupSubjects.value[index].coefficient = parseFloat(editSubjectData.coefficient)
          }
          
          // Close modal
          showEditSubjectModal.value = false
          
          alert('Cập nhật hệ số thành công')
        } catch (err) {
          editSubjectError.value = `Không thể cập nhật hệ số: ${err.message}`
        } finally {
          isEditingSubject.value = false
        }
      }
  
      // Confirm delete subject
      const confirmDeleteSubject = (detail) => {
        subjectToDelete.value = detail
        showDeleteSubjectModal.value = true
      }
  
      // Cancel delete subject
      const cancelDeleteSubject = () => {
        showDeleteSubjectModal.value = false
        subjectToDelete.value = null
      }
  
      // Delete subject from group
      const deleteSubjectFromGroup = async () => {
        if (!subjectToDelete.value) return
        
        try {
          isDeletingSubject.value = true
          
          await SubjectGroupDetailController.deleteSubjectGroupDetail(subjectToDelete.value.id)
          
          // Remove from list
          groupSubjects.value = groupSubjects.value.filter(gs => gs.id !== subjectToDelete.value.id)
          
          // Update available subjects
          updateAvailableSubjects()
          
          // Close modal
          showDeleteSubjectModal.value = false
          subjectToDelete.value = null
          
          alert('Xóa môn thi khỏi tổ hợp thành công')
        } catch (err) {
          alert(`Lỗi: ${err.message}`)
        } finally {
          isDeletingSubject.value = false
        }
      }
  
      // Confirm delete group
      const confirmDeleteGroup = () => {
        showDeleteGroupModal.value = true
      }
  
      // Cancel delete group
      const cancelDeleteGroup = () => {
        showDeleteGroupModal.value = false
      }
  
      // Delete group
      const deleteGroup = async () => {
        try {
          isDeletingGroup.value = true
          
          await SubjectGroupController.deleteSubjectGroup(props.groupId)
          
          alert('Xóa tổ hợp môn thi thành công')
          router.push('/admins/subject-groups')
        } catch (err) {
          alert(`Lỗi: ${err.message}`)
        } finally {
          isDeletingGroup.value = false
          showDeleteGroupModal.value = false
        }
      }

      // Add a function to load majors
const loadMajors = async () => {
  try {
    loadingMajors.value = true
    majorsError.value = null
    
    // Get majors that use this subject group
    const majorsData = await SubjectGroupMajorController.getMajorsBySubjectGroup(props.groupId)
    groupMajors.value = majorsData
    
    // Load available admission method majors that can be added
    loadAvailableAdmissionMethodMajors()
  } catch (err) {
    majorsError.value = `Không thể tải danh sách ngành: ${err.message}`
  } finally {
    loadingMajors.value = false
  }
}

// Load available admission method majors
const loadAvailableAdmissionMethodMajors = async () => {
  try {
    // Get all admission method majors
    const allMethodMajors = await AdmissionMethodMajorController.getAllAdmissionMethodMajors()
    
    // Filter out ones already linked to this group
    const linkedIds = groupMajors.value.map(m => m.id)
    availableAdmissionMethodMajors.value = allMethodMajors.filter(amm => !linkedIds.includes(amm.id))
  } catch (err) {
    console.error('Error loading available admission method majors:', err)
    availableAdmissionMethodMajors.value = []
  }
}

// Cancel add major
const cancelAddMajor = () => {
  showAddMajorModal.value = false
  addMajorData.admission_method_major_id = ''
  addMajorError.value = ''
  addMajorErrors.admission_method_major_id = ''
}

// Add major to subject group
const addMajorToSubjectGroup = async () => {
  // Validate
  if (!addMajorData.admission_method_major_id) {
    addMajorErrors.admission_method_major_id = 'Vui lòng chọn phương thức tuyển sinh-ngành'
    return
  }
  
  try {
    isAddingMajor.value = true
    
    const data = {
      group_id: parseInt(props.groupId),
      admission_method_major_id: parseInt(addMajorData.admission_method_major_id)
    }
    
    await SubjectGroupMajorController.createSubjectGroupMajor(data)
    
    // Reload majors
    await loadMajors()
    
    // Reset form and close modal
    addMajorData.admission_method_major_id = ''
    showAddMajorModal.value = false
    
    alert('Thêm ngành áp dụng tổ hợp thành công')
  } catch (err) {
    addMajorError.value = `Không thể thêm ngành: ${err.message}`
  } finally {
    isAddingMajor.value = false
  }
}

// Confirm remove major
const confirmRemoveMajor = (majorRelation) => {
  majorToRemove.value = majorRelation
  showRemoveMajorModal.value = true
}

// Cancel remove major
const cancelRemoveMajor = () => {
  showRemoveMajorModal.value = false
  majorToRemove.value = null
}

// Remove major from subject group
const removeMajorFromSubjectGroup = async () => {
  if (!majorToRemove.value) return
  
  try {
    isRemovingMajor.value = true
    
    await SubjectGroupMajorController.deleteSubjectGroupMajor(majorToRemove.value.id)
    
    // Reload majors
    await loadMajors()
    
    // Close modal
    showRemoveMajorModal.value = false
    majorToRemove.value = null
    
    alert('Xóa ngành khỏi tổ hợp thành công')
  } catch (err) {
    alert(`Lỗi: ${err.message}`)
  } finally {
    isRemovingMajor.value = false
  }
}

      
  
      onMounted(() => {
        fetchData()
      })
  
      return {
        group,
        groupSubjects,
        allSubjects,
        availableSubjects,
        loading,
        error,
        showEditModal,
        editGroupData,
        editError,
        isUpdating,
        showAddSubjectModal,
        addSubjectData,
        addSubjectError,
        addSubjectErrors,
        isAddingSubject,
        showEditSubjectModal,
        editSubjectData,
        editSubjectError,
        isEditingSubject,
        showDeleteSubjectModal,
        subjectToDelete,
        isDeletingSubject,
        showDeleteGroupModal,
        isDeletingGroup,
        formatDate,
        getSubjectName,
        updateGroupName,
        addSubjectToGroup,
        cancelAddSubject,
        openEditSubjectModal,
        cancelEditSubject,
        updateSubjectCoefficient,
        confirmDeleteSubject,
        cancelDeleteSubject,
        deleteSubjectFromGroup,
        confirmDeleteGroup,
        cancelDeleteGroup,
        deleteGroup,
        groupMajors,
  loadingMajors,
  majorsError,
  showAddMajorModal,
  addMajorData,
  addMajorError,
  addMajorErrors,
  isAddingMajor,
  showRemoveMajorModal,
  majorToRemove,
  isRemovingMajor,
  availableAdmissionMethodMajors,
  admissionMethods,
  
  // New functions
  getAdmissionMethodName,
  loadMajors,
  loadAvailableAdmissionMethodMajors,
  cancelAddMajor,
  addMajorToSubjectGroup,
  confirmRemoveMajor,
  cancelRemoveMajor,
  removeMajorFromSubjectGroup
      }
    }
  }
  </script>
  
  <style scoped>
  .admin-subject-group-detail {
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
    padding: 1.5rem;
    transition: all 0.3s ease;
  }
  
  .admin-card:hover {
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
  }
  
  .card-header {
    padding-bottom: 1rem;
    margin-bottom: 1rem;
    border-bottom: 1px solid #e9ecef;
  }
  
  /* Group Info Styling */
  .group-name {
    font-size: 1.5rem;
    font-weight: 600;
    color: #0B2942;
    margin-bottom: 1rem;
  }
  
  .group-meta {
    margin-bottom: 1rem;
  }
  
  .group-meta-item {
    display: flex;
    justify-content: flex-start;
    margin-bottom: 0.5rem;
  }
  
  .meta-label {
    font-weight: 500;
    color: #6c757d;
    width: 100px;
  }
  
  .meta-value {
    color: #0B2942;
    font-weight: 500;
  }
  
  .group-actions {
    display: flex;
    gap: 1rem;
    justify-content: flex-end;
    margin-top: 1rem;
  }
  
  .btn-edit {
    display: inline-flex;
    align-items: center;
    padding: 0.6rem 1rem;
    background-color: #0B2942;
    color: #fff;
    border: none;
    border-radius: 8px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s;
  }
  
  .btn-edit:hover {
    background-color: #4da0ff;
  }
  
  .btn-delete {
    display: inline-flex;
    align-items: center;
    padding: 0.6rem 1rem;
    background-color: #fff;
    color: #dc3545;
    border: 1px solid #dc3545;
    border-radius: 8px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s;
  }
  
  .btn-delete:hover {
    background-color: #dc3545;
    color: #fff;
  }
  
  .section-title {
    font-size: 1.25rem;
    font-weight: 600;
    color: #0B2942;
  }
  
  .btn-add-subject {
    display: inline-flex;
    align-items: center;
    padding: 0.6rem 1rem;
    background-color: #0B2942;
    color: #fff;
    border: none;
    border-radius: 8px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s;
  }
  
  .btn-add-subject:hover {
    background-color: #4da0ff;
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
  
  .coefficient-badge {
    display: inline-block;
    padding: 0.35rem 0.75rem;
    border-radius: 50px;
    font-size: 0.9rem;
    font-weight: 500;
    background-color: #e3f2fd;
    color: #0d6efd;
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
  
  .btn-action.edit {
    color: #0B2942;
  }
  
  .btn-action.delete {
    color: #dc3545;
  }
  
  .btn-action:hover {
    background-color: #f8f9fa;
    transform: translateY(-2px);
  }
  
  .btn-action.edit:hover {
    color: #0B2942;
    background-color: rgba(11, 41, 66, 0.1);
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
  
  .btn-add-empty {
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
  
  .btn-add-empty:hover {
    background-color: #4da0ff;
    color: #fff;
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
  
  .form-text {
    font-size: 0.85rem;
    margin-top: 0.25rem;
  }
  
  .text-muted {
    color: #6c757d;
  }
  
  .text-info {
    color: #0d6efd;
  }
  
  .invalid-feedback {
    color: #dc3545;
    font-size: 0.875em;
    margin-top: 0.25rem;
  }
  
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
  
  .btn-save, .btn-add {
    padding: 0.5rem 1rem;
    background-color: #0B2942;
    color: #fff;
    border: none;
    border-radius: 6px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s;
  }
  
  .btn-save:hover:not(:disabled), .btn-add:hover:not(:disabled) {
    background-color: #4da0ff;
  }
  
  .btn-save:disabled, .btn-add:disabled {
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
  
  .text-danger {
    color: #dc3545;
  }
  
  @media (max-width: 768px) {
    .group-actions {
      flex-direction: column;
      align-items: stretch;
    }
  
    .btn-edit, .btn-delete {
      width: 100%;
      justify-content: center;
    }
  
    .card-header {
      flex-direction: column;
      gap: 1rem;
    }
  
    .btn-add-subject {
      width: 100%;
      justify-content: center;
    }
  }
  </style>
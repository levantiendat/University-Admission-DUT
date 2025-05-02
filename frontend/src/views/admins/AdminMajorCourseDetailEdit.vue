<template>
    <div class="admin-major-course-detail-edit">
      <div class="admin-page-header">
        <div class="d-flex align-items-center">
          <router-link :to="`/admins/major-courses/${majorCourseId}`" class="btn-back">
            <i class="bi bi-arrow-left"></i>
          </router-link>
          <div>
            <h2 class="admin-page-title">Quản lý mối quan hệ học phần</h2>
            <p class="admin-page-description">Thiết lập các mối quan hệ giữa các học phần trong khung chương trình</p>
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
        <p class="loading-text">Đang tải thông tin học phần...</p>
      </div>
  
      <!-- Error State -->
      <div v-else-if="error" class="error-message">
        <i class="bi bi-exclamation-triangle-fill error-icon"></i>
        <span>{{ error }}</span>
      </div>
  
      <div v-else class="content-container">
        <!-- Course Detail Info Card -->
        <div class="admin-card info-card mb-4">
          <div class="info-header">
            <h3 class="course-name">{{ getCourseById(courseDetail.course_id)?.name }}</h3>
            <div class="course-code">{{ getCourseById(courseDetail.course_id)?.course_code }}</div>
            <div class="course-meta">
              <span class="semester-badge">Học kỳ {{ courseDetail.semester }}</span>
              <span 
                v-if="courseDetail.elective_course" 
                class="type-badge elective"
                title="Tự chọn"
              >
                Tự chọn
              </span>
              <span 
                v-if="courseDetail.pre_capstone" 
                class="type-badge pre-capstone"
                title="Tiền đồ án"
              >
                Tiền đồ án
              </span>
              <span 
                v-if="courseDetail.mandatory_capstone" 
                class="type-badge capstone"
                title="Đồ án bắt buộc"
              >
                Đồ án bắt buộc
              </span>
            </div>
          </div>
  
          <div class="info-meta">
            <div class="info-item">
              <span class="info-label">ID học phần:</span>
              <span class="info-value">#{{ courseDetail.id }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">Thuộc khung chương trình:</span>
              <span class="info-value">#{{ courseDetail.major_course_id }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">Số tín chỉ:</span>
              <span class="info-value">{{ getCourseById(courseDetail.course_id)?.credits }}</span>
            </div>
          </div>
  
          <div class="info-actions">
            <button 
              class="btn-edit"
              @click="showEditModal = true"
            >
              <i class="bi bi-pencil-square me-2"></i>
              Sửa thông tin học phần
            </button>
          </div>
        </div>
  
        <!-- Relationship Management -->
        <div class="row">
          <!-- Prior Courses -->
          <div class="col-md-4">
            <div class="admin-card relationship-card">
              <div class="d-flex justify-content-between align-items-center mb-3">
                <h4 class="relationship-title">
                  <i class="bi bi-box-arrow-in-up-right me-2"></i>
                  Học phần học trước
                </h4>
                <button class="btn-add-relationship" @click="showPriorCourseModal = true">
                  <i class="bi bi-plus-circle"></i>
                </button>
              </div>
              <p class="relationship-desc">Các học phần cần học trước khi đăng ký học phần này</p>
  
              <!-- Prior Courses List -->
              <div v-if="loadingRelationships" class="loading-container py-3">
                <div class="spinner">
                  <div class="bounce1"></div>
                  <div class="bounce2"></div>
                  <div class="bounce3"></div>
                </div>
              </div>
              <div v-else-if="courseDetail.prior_courses && courseDetail.prior_courses.length > 0" class="relationship-list">
                <div v-for="priorId in courseDetail.prior_courses" :key="`prior-${priorId}`" class="relationship-item">
                  <div class="course-relation-info">
                    <span class="course-code">{{ getCourseFromDetailId(priorId)?.course_code }}</span>
                    <span class="course-name">{{ getCourseFromDetailId(priorId)?.name }}</span>
                    <span class="semester-info">Học kỳ {{ getDetailById(priorId)?.semester }}</span>
                  </div>
                  <button class="btn-remove" @click="confirmRemovePriorCourse(priorId)" title="Xóa mối quan hệ">
                    <i class="bi bi-x-circle"></i>
                  </button>
                </div>
              </div>
              <div v-else class="empty-relationship">
                <i class="bi bi-inbox empty-icon"></i>
                <p>Chưa có học phần học trước</p>
              </div>
            </div>
          </div>
  
          <!-- Prerequisites -->
          <div class="col-md-4">
            <div class="admin-card relationship-card">
              <div class="d-flex justify-content-between align-items-center mb-3">
                <h4 class="relationship-title">
                  <i class="bi bi-arrow-left-circle me-2"></i>
                  Học phần tiên quyết
                </h4>
                <button class="btn-add-relationship" @click="showPrerequisiteModal = true">
                  <i class="bi bi-plus-circle"></i>
                </button>
              </div>
              <p class="relationship-desc">Các học phần cần đạt điểm hoàn thành trước khi đăng ký học phần này</p>
  
              <!-- Prerequisites List -->
              <div v-if="loadingRelationships" class="loading-container py-3">
                <div class="spinner">
                  <div class="bounce1"></div>
                  <div class="bounce2"></div>
                  <div class="bounce3"></div>
                </div>
              </div>
              <div v-else-if="courseDetail.prerequisites && courseDetail.prerequisites.length > 0" class="relationship-list">
                <div v-for="prerequisiteId in courseDetail.prerequisites" :key="`prerequisite-${prerequisiteId}`" class="relationship-item">
                  <div class="course-relation-info">
                    <span class="course-code">{{ getCourseFromDetailId(prerequisiteId)?.course_code }}</span>
                    <span class="course-name">{{ getCourseFromDetailId(prerequisiteId)?.name }}</span>
                    <span class="semester-info">Học kỳ {{ getDetailById(prerequisiteId)?.semester }}</span>
                  </div>
                  <button class="btn-remove" @click="confirmRemovePrerequisite(prerequisiteId)" title="Xóa mối quan hệ">
                    <i class="bi bi-x-circle"></i>
                  </button>
                </div>
              </div>
              <div v-else class="empty-relationship">
                <i class="bi bi-inbox empty-icon"></i>
                <p>Chưa có học phần tiên quyết</p>
              </div>
            </div>
          </div>
  
          <!-- Corequisites -->
          <div class="col-md-4">
            <div class="admin-card relationship-card">
              <div class="d-flex justify-content-between align-items-center mb-3">
                <h4 class="relationship-title">
                  <i class="bi bi-arrows-angle-expand me-2"></i>
                  Học phần song hành
                </h4>
                <button class="btn-add-relationship" @click="showCorequisiteModal = true">
                  <i class="bi bi-plus-circle"></i>
                </button>
              </div>
              <p class="relationship-desc">Các học phần cần đăng ký học cùng lúc (hoặc đã học trước) với học phần này</p>
  
              <!-- Corequisites List -->
              <div v-if="loadingRelationships" class="loading-container py-3">
                <div class="spinner">
                  <div class="bounce1"></div>
                  <div class="bounce2"></div>
                  <div class="bounce3"></div>
                </div>
              </div>
              <div v-else-if="courseDetail.corequisites && courseDetail.corequisites.length > 0" class="relationship-list">
                <div v-for="corequisiteId in courseDetail.corequisites" :key="`corequisite-${corequisiteId}`" class="relationship-item">
                  <div class="course-relation-info">
                    <span class="course-code">{{ getCourseFromDetailId(corequisiteId)?.course_code }}</span>
                    <span class="course-name">{{ getCourseFromDetailId(corequisiteId)?.name }}</span>
                    <span class="semester-info">Học kỳ {{ getDetailById(corequisiteId)?.semester }}</span>
                  </div>
                  <button class="btn-remove" @click="confirmRemoveCorequisite(corequisiteId)" title="Xóa mối quan hệ">
                    <i class="bi bi-x-circle"></i>
                  </button>
                </div>
              </div>
              <div v-else class="empty-relationship">
                <i class="bi bi-inbox empty-icon"></i>
                <p>Chưa có học phần song hành</p>
              </div>
            </div>
          </div>
        </div>
      </div>
  
      <!-- Edit Course Detail Modal -->
      <div v-if="showEditModal" class="modal-overlay" @click="cancelEdit">
        <div class="modal-content" @click.stop>
          <div class="modal-header">
            <h4 class="modal-title">Chỉnh sửa thông tin học phần</h4>
            <button type="button" class="btn-close" @click="cancelEdit"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="updateCourseDetail">
              <div class="row">
                <div class="col-md-6">
                  <div class="form-group">
                    <label for="course-code">Mã học phần</label>
                    <input 
                      type="text" 
                      id="course-code" 
                      class="form-control" 
                      :value="getCourseById(courseDetail.course_id)?.course_code" 
                      disabled
                    >
                  </div>
                </div>
                <div class="col-md-6">
                  <div class="form-group">
                    <label for="semester">Học kỳ <span class="required">*</span></label>
                    <select 
                      id="semester" 
                      v-model="editData.semester" 
                      class="form-select" 
                      required
                      :class="{ 'is-invalid': editErrors.semester }"
                    >
                      <option v-for="i in 10" :key="i" :value="i">Học kỳ {{ i }}</option>
                    </select>
                    <div v-if="editErrors.semester" class="invalid-feedback">{{ editErrors.semester }}</div>
                  </div>
                </div>
              </div>
  
              <div class="course-options">
                <div class="form-check">
                  <input 
                    type="checkbox" 
                    id="edit-elective-course" 
                    v-model="editData.elective_course" 
                    class="form-check-input"
                  >
                  <label for="edit-elective-course" class="form-check-label">Học phần tự chọn</label>
                </div>
  
                <div class="form-check">
                  <input 
                    type="checkbox" 
                    id="edit-pre-capstone" 
                    v-model="editData.pre_capstone" 
                    class="form-check-input"
                  >
                  <label for="edit-pre-capstone" class="form-check-label">Học trước đồ án</label>
                </div>
  
                <div class="form-check">
                  <input 
                    type="checkbox" 
                    id="edit-mandatory-capstone" 
                    v-model="editData.mandatory_capstone" 
                    class="form-check-input"
                  >
                  <label for="edit-mandatory-capstone" class="form-check-label">Tiên quyết đồ án</label>
                </div>
              </div>
  
              <div v-if="editError" class="alert alert-danger mt-3">
                {{ editError }}
              </div>
  
              <div class="modal-footer">
                <button type="button" class="btn-cancel" @click="cancelEdit">Hủy</button>
                <button type="submit" class="btn-save" :disabled="isUpdating">
                  {{ isUpdating ? 'Đang lưu...' : 'Lưu thay đổi' }}
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
  
      <!-- Add Prior Course Modal -->
      <div v-if="showPriorCourseModal" class="modal-overlay" @click="cancelAddRelationship('prior')">
        <div class="modal-content" @click.stop>
          <div class="modal-header">
            <h4 class="modal-title">Thêm học phần học trước</h4>
            <button type="button" class="btn-close" @click="cancelAddRelationship('prior')"></button>
          </div>
          <div class="modal-body">
            <p class="mb-4">Chọn học phần cần học trước khi đăng ký học phần {{ getCourseById(courseDetail.course_id)?.name }}</p>
            
            <div class="form-group mb-4">
              <div class="search-box">
                <i class="bi bi-search search-icon"></i>
                <input 
                  type="text" 
                  v-model="searchQuery" 
                  class="search-input" 
                  placeholder="Tìm kiếm học phần..." 
                >
              </div>
            </div>
  
            <div class="available-courses">
              <div v-if="filteredAvailableCourses.length === 0" class="empty-state">
                <p>Không tìm thấy học phần phù hợp</p>
              </div>
              <div v-else v-for="detail in filteredAvailableCourses" :key="detail.id" class="course-option">
                <div class="course-option-info">
                  <div class="course-code">{{ getCourseById(detail.course_id)?.course_code }}</div>
                  <div class="course-name">{{ getCourseById(detail.course_id)?.name }}</div>
                  <div class="semester-info">Học kỳ {{ detail.semester }}</div>
                </div>
                <button 
                  class="btn-add-action"
                  @click="addPriorCourse(detail.id)"
                  :disabled="isAdding"
                >
                  <i class="bi bi-plus-circle"></i>
                </button>
              </div>
            </div>
  
            <div v-if="relationshipError" class="alert alert-danger mt-3">
              {{ relationshipError }}
            </div>
  
            <div class="modal-footer">
              <button type="button" class="btn-cancel" @click="cancelAddRelationship('prior')">Đóng</button>
            </div>
          </div>
        </div>
      </div>
  
      <!-- Add Prerequisite Modal -->
      <div v-if="showPrerequisiteModal" class="modal-overlay" @click="cancelAddRelationship('prerequisite')">
        <div class="modal-content" @click.stop>
          <div class="modal-header">
            <h4 class="modal-title">Thêm học phần tiên quyết</h4>
            <button type="button" class="btn-close" @click="cancelAddRelationship('prerequisite')"></button>
          </div>
          <div class="modal-body">
            <p class="mb-4">Chọn học phần cần đạt điểm hoàn thành trước khi đăng ký học phần {{ getCourseById(courseDetail.course_id)?.name }}</p>
            
            <div class="form-group mb-4">
              <div class="search-box">
                <i class="bi bi-search search-icon"></i>
                <input 
                  type="text" 
                  v-model="searchQuery" 
                  class="search-input" 
                  placeholder="Tìm kiếm học phần..." 
                >
              </div>
            </div>
  
            <div class="available-courses">
              <div v-if="filteredAvailableCourses.length === 0" class="empty-state">
                <p>Không tìm thấy học phần phù hợp</p>
              </div>
              <div v-else v-for="detail in filteredAvailableCourses" :key="detail.id" class="course-option">
                <div class="course-option-info">
                  <div class="course-code">{{ getCourseById(detail.course_id)?.course_code }}</div>
                  <div class="course-name">{{ getCourseById(detail.course_id)?.name }}</div>
                  <div class="semester-info">Học kỳ {{ detail.semester }}</div>
                </div>
                <button 
                  class="btn-add-action"
                  @click="addPrerequisite(detail.id)"
                  :disabled="isAdding"
                >
                  <i class="bi bi-plus-circle"></i>
                </button>
              </div>
            </div>
  
            <div v-if="relationshipError" class="alert alert-danger mt-3">
              {{ relationshipError }}
            </div>
  
            <div class="modal-footer">
              <button type="button" class="btn-cancel" @click="cancelAddRelationship('prerequisite')">Đóng</button>
            </div>
          </div>
        </div>
      </div>
  
      <!-- Add Corequisite Modal -->
      <div v-if="showCorequisiteModal" class="modal-overlay" @click="cancelAddRelationship('corequisite')">
        <div class="modal-content" @click.stop>
          <div class="modal-header">
            <h4 class="modal-title">Thêm học phần song hành</h4>
            <button type="button" class="btn-close" @click="cancelAddRelationship('corequisite')"></button>
          </div>
          <div class="modal-body">
            <p class="mb-4">Chọn học phần cần đăng ký cùng lúc với học phần {{ getCourseById(courseDetail.course_id)?.name }}</p>
            
            <div class="form-group mb-4">
              <div class="search-box">
                <i class="bi bi-search search-icon"></i>
                <input 
                  type="text" 
                  v-model="searchQuery" 
                  class="search-input" 
                  placeholder="Tìm kiếm học phần..." 
                >
              </div>
            </div>
  
            <div class="available-courses">
              <div v-if="filteredAvailableCourses.length === 0" class="empty-state">
                <p>Không tìm thấy học phần phù hợp</p>
              </div>
              <div v-else v-for="detail in filteredAvailableCourses" :key="detail.id" class="course-option">
                <div class="course-option-info">
                  <div class="course-code">{{ getCourseById(detail.course_id)?.course_code }}</div>
                  <div class="course-name">{{ getCourseById(detail.course_id)?.name }}</div>
                  <div class="semester-info">Học kỳ {{ detail.semester }}</div>
                </div>
                <button 
                  class="btn-add-action"
                  @click="addCorequisite(detail.id)"
                  :disabled="isAdding"
                >
                  <i class="bi bi-plus-circle"></i>
                </button>
              </div>
            </div>
  
            <div v-if="relationshipError" class="alert alert-danger mt-3">
              {{ relationshipError }}
            </div>
  
            <div class="modal-footer">
              <button type="button" class="btn-cancel" @click="cancelAddRelationship('corequisite')">Đóng</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  <script>
  import { ref, reactive, computed, onMounted, watch } from 'vue'
  import { useRouter } from 'vue-router'
  import MajorCourseController from '@/controllers/admins/MajorCourseController'
  import CourseController from '@/controllers/admins/CourseController'
  
  export default {
    name: 'AdminMajorCourseDetailEdit',
    props: {
      detailId: {
        type: [String, Number],
        required: true
      }
    },
    setup(props) {
      const router = useRouter()
      
      // Basic state
      const courseDetail = ref({})
      const allCourseDetails = ref([])
      const allCourses = ref([])
      const loading = ref(true)
      const error = ref(null)
      const majorCourseId = ref(null)
      
      // Edit modal state
      const showEditModal = ref(false)
      const isUpdating = ref(false)
      const editError = ref(null)
      const editData = reactive({
        semester: '',
        elective_course: false,
        pre_capstone: false,
        mandatory_capstone: false
      })
      const editErrors = reactive({
        semester: ''
      })
      
      // Relationship management state
      const loadingRelationships = ref(false)
      const showPriorCourseModal = ref(false)
      const showPrerequisiteModal = ref(false)
      const showCorequisiteModal = ref(false)
      const relationshipError = ref(null)
      const isAdding = ref(false)
      const searchQuery = ref('')
      
      // Current modal type
      const currentRelationshipType = ref('') // 'prior', 'prerequisite', or 'corequisite'
      
      // Filtered available courses for adding
      const filteredAvailableCourses = computed(() => {
        let courses = allCourseDetails.value.filter(detail => {
          // Can't add self
          if (detail.id === parseInt(props.detailId)) {
            return false
          }
          
          // Must be in the same major course
          if (detail.major_course_id !== courseDetail.value.major_course_id) {
            return false
          }
          
          // Filter based on relationship type
          if (currentRelationshipType.value === 'prior') {
            // For prior course, exclude those already set as prior
            if (courseDetail.value.prior_courses?.includes(detail.id)) {
              return false
            }
          } else if (currentRelationshipType.value === 'prerequisite') {
            // For prerequisite, exclude those already set as prerequisite
            if (courseDetail.value.prerequisites?.includes(detail.id)) {
              return false
            }
          } else if (currentRelationshipType.value === 'corequisite') {
            // For corequisite, exclude those already set as corequisite
            if (courseDetail.value.corequisites?.includes(detail.id)) {
              return false
            }
          }
          
          // Apply search filter if any
          if (searchQuery.value) {
            const course = getCourseById(detail.course_id)
            if (!course) return false
            
            const search = searchQuery.value.toLowerCase()
            return (
              course.name.toLowerCase().includes(search) ||
              course.course_code.toLowerCase().includes(search)
            )
          }
          
          return true
        })
        
        // Sort by semester and then by course code
        courses.sort((a, b) => {
          if (a.semester === b.semester) {
            const courseA = getCourseById(a.course_id)
            const courseB = getCourseById(b.course_id)
            if (courseA && courseB) {
              return courseA.course_code.localeCompare(courseB.course_code)
            }
            return 0
          }
          return a.semester - b.semester
        })
        
        return courses
      })
      
      // Get course by ID
      const getCourseById = (courseId) => {
        return allCourses.value.find(c => c.id === courseId)
      }
      
      // Get course from detail ID
      const getCourseFromDetailId = (detailId) => {
        const detail = allCourseDetails.value.find(d => d.id === detailId)
        if (!detail) return null
        return getCourseById(detail.course_id)
      }
      
      // Get course detail by ID
      const getDetailById = (detailId) => {
        return allCourseDetails.value.find(d => d.id === detailId)
      }
      
      // Fetch course detail data
      const fetchCourseDetail = async () => {
        try {
          loading.value = true
          error.value = null
          
          // Get the detail data
          const detailData = await MajorCourseController.getMajorCourseDetail(props.detailId)
          courseDetail.value = detailData
          majorCourseId.value = detailData.major_course_id
          
          // Setup edit data
          editData.semester = detailData.semester
          editData.elective_course = detailData.elective_course
          editData.pre_capstone = detailData.pre_capstone
          editData.mandatory_capstone = detailData.mandatory_capstone
          
          // Fetch all courses and course details for the major course
          const [coursesResponse, allCoursesData] = await Promise.all([
            MajorCourseController.getMajorCourseDetailsById(detailData.major_course_id),
            CourseController.getAllCourses()
          ])
          
          allCourses.value = allCoursesData
          allCourseDetails.value = coursesResponse.major_course_details || []
          
          // Fetch relationships
          await updateRelationships()
          
        } catch (err) {
          error.value = `Không thể tải thông tin học phần: ${err.message}`
        } finally {
          loading.value = false
        }
      }
      
      // Update relationships with API data
      const updateRelationships = async () => {
        try {
          loadingRelationships.value = true
          
          // Fetch relationships data
          const [prerequisites, priorCourses, corequisites] = await Promise.all([
            MajorCourseController.getAllPrerequisites(),
            MajorCourseController.getAllPriorCourses(),
            MajorCourseController.getAllCorequisites()
          ])
          
          // Update the courseDetail with current relationships
          const currentPrerequisites = prerequisites
            .filter(p => p.major_course_detail_id === parseInt(props.detailId))
            .map(p => p.prerequisite_major_course_detail_id)
          
          const currentPriorCourses = priorCourses
            .filter(p => p.major_course_detail_id === parseInt(props.detailId))
            .map(p => p.prior_course_detail_id)
          
          const currentCorequisites = corequisites
            .filter(c => c.major_course_detail_id === parseInt(props.detailId))
            .map(c => c.corequisite_major_course_detail_id)
          
          courseDetail.value = {
            ...courseDetail.value,
            prerequisites: currentPrerequisites,
            prior_courses: currentPriorCourses,
            corequisites: currentCorequisites
          }
        } catch (err) {
          console.error('Error updating relationships:', err)
        } finally {
          loadingRelationships.value = false
        }
      }
      
      // Cancel edit modal
      const cancelEdit = () => {
        showEditModal.value = false
        // Reset to original values
        editData.semester = courseDetail.value.semester
        editData.elective_course = courseDetail.value.elective_course
        editData.pre_capstone = courseDetail.value.pre_capstone
        editData.mandatory_capstone = courseDetail.value.mandatory_capstone
        
        // Clear errors
        editError.value = null
        editErrors.semester = ''
      }
      
      // Validate edit form
      const validateEditForm = () => {
        let isValid = true
        
        editError.value = null
        editErrors.semester = ''
        
        if (!editData.semester || isNaN(parseInt(editData.semester)) || parseInt(editData.semester) < 1) {
          editErrors.semester = 'Vui lòng chọn học kỳ hợp lệ'
          isValid = false
        }
        
        return isValid
      }
      
      // Update course detail
      const updateCourseDetail = async () => {
        try {
          if (!validateEditForm()) {
            return
          }
          
          isUpdating.value = true
          
          const updateData = {
            semester: parseInt(editData.semester),
            elective_course: editData.elective_course,
            pre_capstone: editData.pre_capstone,
            mandatory_capstone: editData.mandatory_capstone
          }
          
          await MajorCourseController.updateMajorCourseDetail(props.detailId, updateData)
          
          // Update local state
          courseDetail.value = {
            ...courseDetail.value,
            ...updateData
          }
          
          // Update in allCourseDetails
          const index = allCourseDetails.value.findIndex(d => d.id === parseInt(props.detailId))
          if (index !== -1) {
            allCourseDetails.value[index] = {
              ...allCourseDetails.value[index],
              ...updateData
            }
          }
          
          showEditModal.value = false
          alert('Cập nhật thông tin học phần thành công')
        } catch (err) {
          editError.value = `Không thể cập nhật thông tin học phần: ${err.message}`
        } finally {
          isUpdating.value = false
        }
      }
      
      // Handle relationship modal open
      const openRelationshipModal = (type) => {
        currentRelationshipType.value = type
        relationshipError.value = null
        searchQuery.value = ''
        
        if (type === 'prior') {
          showPriorCourseModal.value = true
        } else if (type === 'prerequisite') {
          showPrerequisiteModal.value = true
        } else if (type === 'corequisite') {
          showCorequisiteModal.value = true
        }
      }
      
      // Handle relationship modal close
      const cancelAddRelationship = (type) => {
        if (type === 'prior') {
          showPriorCourseModal.value = false
        } else if (type === 'prerequisite') {
          showPrerequisiteModal.value = false
        } else if (type === 'corequisite') {
          showCorequisiteModal.value = false
        }
        
        relationshipError.value = null
        currentRelationshipType.value = ''
      }
      
      // Add prior course relationship
      const addPriorCourse = async (priorDetailId) => {
        try {
          isAdding.value = true
          relationshipError.value = null
          
          await MajorCourseController.addPriorCourse(props.detailId, priorDetailId)
          
          // Update local state
          if (!courseDetail.value.prior_courses) {
            courseDetail.value.prior_courses = []
          }
          courseDetail.value.prior_courses.push(priorDetailId)
          
          alert('Thêm học phần học trước thành công')
        } catch (err) {
          relationshipError.value = `Không thể thêm học phần học trước: ${err.message}`
        } finally {
          isAdding.value = false
        }
      }
      
      // Add prerequisite relationship
      const addPrerequisite = async (prerequisiteDetailId) => {
        try {
          isAdding.value = true
          relationshipError.value = null
          
          await MajorCourseController.addPrerequisite(props.detailId, prerequisiteDetailId)
          
          // Update local state
          if (!courseDetail.value.prerequisites) {
            courseDetail.value.prerequisites = []
          }
          courseDetail.value.prerequisites.push(prerequisiteDetailId)
          
          alert('Thêm học phần tiên quyết thành công')
        } catch (err) {
          relationshipError.value = `Không thể thêm học phần tiên quyết: ${err.message}`
        } finally {
          isAdding.value = false
        }
      }
      
      // Add corequisite relationship
      const addCorequisite = async (corequisiteDetailId) => {
        try {
          isAdding.value = true
          relationshipError.value = null
          
          await MajorCourseController.addCorequisite(props.detailId, corequisiteDetailId)
          
          // Update local state
          if (!courseDetail.value.corequisites) {
            courseDetail.value.corequisites = []
          }
          courseDetail.value.corequisites.push(corequisiteDetailId)
          
          alert('Thêm học phần song hành thành công')
        } catch (err) {
          relationshipError.value = `Không thể thêm học phần song hành: ${err.message}`
        } finally {
          isAdding.value = false
        }
      }
      
      // Confirm remove prior course
      const confirmRemovePriorCourse = async (priorId) => {
        try {
          // Get the relationship ID
          const priorCourses = await MajorCourseController.getAllPriorCourses()
          const relationship = priorCourses.find(
            p => p.major_course_detail_id === parseInt(props.detailId) && 
                 p.prior_course_detail_id === priorId
          )
          
          if (!relationship) {
            throw new Error('Không tìm thấy mối quan hệ này')
          }
          
          if (confirm('Bạn có chắc chắn muốn xóa mối quan hệ học trước này?')) {
            await MajorCourseController.removePriorCourse(relationship.id)
            
            // Update local state
            courseDetail.value.prior_courses = courseDetail.value.prior_courses.filter(id => id !== priorId)
            
            alert('Đã xóa mối quan hệ học trước')
          }
        } catch (err) {
          alert(`Lỗi: ${err.message}`)
        }
      }
      
      // Confirm remove prerequisite
      const confirmRemovePrerequisite = async (prerequisiteId) => {
        try {
          // Get the relationship ID
          const prerequisites = await MajorCourseController.getAllPrerequisites()
          const relationship = prerequisites.find(
            p => p.major_course_detail_id === parseInt(props.detailId) && 
                 p.prerequisite_major_course_detail_id === prerequisiteId
          )
          
          if (!relationship) {
            throw new Error('Không tìm thấy mối quan hệ này')
          }
          
          if (confirm('Bạn có chắc chắn muốn xóa mối quan hệ tiên quyết này?')) {
            await MajorCourseController.removePrerequisite(relationship.id)
            
            // Update local state
            courseDetail.value.prerequisites = courseDetail.value.prerequisites.filter(id => id !== prerequisiteId)
            
            alert('Đã xóa mối quan hệ tiên quyết')
          }
        } catch (err) {
          alert(`Lỗi: ${err.message}`)
        }
      }
      
      // Confirm remove corequisite
      const confirmRemoveCorequisite = async (corequisiteId) => {
        try {
          // Get the relationship ID
          const corequisites = await MajorCourseController.getAllCorequisites()
          const relationship = corequisites.find(
            c => c.major_course_detail_id === parseInt(props.detailId) && 
                 c.corequisite_major_course_detail_id === corequisiteId
          )
          
          if (!relationship) {
            throw new Error('Không tìm thấy mối quan hệ này')
          }
          
          if (confirm('Bạn có chắc chắn muốn xóa mối quan hệ song hành này?')) {
            await MajorCourseController.removeCorequisite(relationship.id)
            
            // Update local state
            courseDetail.value.corequisites = courseDetail.value.corequisites.filter(id => id !== corequisiteId)
            
            alert('Đã xóa mối quan hệ song hành')
          }
        } catch (err) {
          alert(`Lỗi: ${err.message}`)
        }
      }
      
      // Watch for relationship modal changes to update filtered courses
      watch([showPriorCourseModal, showPrerequisiteModal, showCorequisiteModal], ([prior, prerequisite, corequisite]) => {
        if (prior) {
          currentRelationshipType.value = 'prior'
        } else if (prerequisite) {
          currentRelationshipType.value = 'prerequisite'
        } else if (corequisite) {
          currentRelationshipType.value = 'corequisite'
        } else {
          currentRelationshipType.value = ''
        }
      })
      
      onMounted(() => {
        fetchCourseDetail()
      })
  
      return {
        courseDetail,
        allCourseDetails,
        allCourses,
        loading,
        error,
        majorCourseId,
        showEditModal,
        isUpdating,
        editError,
        editData,
        editErrors,
        loadingRelationships,
        showPriorCourseModal,
        showPrerequisiteModal,
        showCorequisiteModal,
        relationshipError,
        isAdding,
        searchQuery,
        currentRelationshipType,
        filteredAvailableCourses,
        getCourseById,
        getCourseFromDetailId,
        getDetailById,
        cancelEdit,
        updateCourseDetail,
        openRelationshipModal,
        cancelAddRelationship,
        addPriorCourse,
        addPrerequisite,
        addCorequisite,
        confirmRemovePriorCourse,
        confirmRemovePrerequisite,
        confirmRemoveCorequisite
      }
    }
  }
  </script>
  
  <style scoped>
  .admin-major-course-detail-edit {
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
  
  .content-container {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
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
  
  /* Info Card Styling */
  .info-card {
    display: flex;
    flex-direction: column;
    position: relative;
  }
  
  .info-header {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    padding-bottom: 1.5rem;
    border-bottom: 1px solid #e9ecef;
    margin-bottom: 1.5rem;
  }
  
  .info-header .course-name {
    font-size: 1.3rem;
    font-weight: 600;
    color: #0B2942;
    margin-bottom: 0.5rem;
  }
  
  .info-header .course-code {
    font-weight: 500;
    color: #6c757d;
    font-size: 1rem;
    margin-bottom: 1rem;
  }
  
  .course-meta {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 0.5rem;
  }
  
  .semester-badge {
    display: inline-block;
    padding: 0.35rem 0.75rem;
    border-radius: 50px;
    font-size: 0.85rem;
    font-weight: 500;
    background-color: #f1f8ff;
    color: #1a73e8;
  }
  
  .type-badge {
    display: inline-block;
    padding: 0.35rem 0.75rem;
    border-radius: 50px;
    font-size: 0.85rem;
    font-weight: 500;
  }
  
  .type-badge.elective {
    background-color: #e3f2fd;
    color: #0d6efd;
  }
  
  .type-badge.pre-capstone {
    background-color: #fff3cd;
    color: #ffc107;
  }
  
  .type-badge.capstone {
    background-color: #d1e7dd;
    color: #198754;
  }
  
  .info-meta {
    margin-bottom: 1.5rem;
  }
  
  .info-item {
    display: flex;
    justify-content: space-between;
    padding: 0.75rem 0;
    border-bottom: 1px solid #f1f1f1;
  }
  
  .info-item:last-child {
    border-bottom: none;
  }
  
  .info-label {
    color: #6c757d;
    font-weight: 500;
  }
  
  .info-value {
    color: #0B2942;
    font-weight: 500;
  }
  
  .info-actions {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    margin-top: auto;
  }
  
  .btn-edit {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 0.75rem 1rem;
    background-color: #0B2942;
    color: #fff;
    border: none;
    border-radius: 8px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s ease;
  }
  
  .btn-edit:hover {
    background-color: #4da0ff;
    transform: translateY(-2px);
  }
  
  /* Relationship card styling */
  .relationship-card {
    height: 100%;
    display: flex;
    flex-direction: column;
  }
  
  .relationship-title {
    font-size: 1.1rem;
    font-weight: 600;
    color: #0B2942;
    margin: 0;
    display: flex;
    align-items: center;
  }
  
  .relationship-desc {
    font-size: 0.9rem;
    color: #6c757d;
    margin-bottom: 1.5rem;
  }
  
  .btn-add-relationship {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 36px;
    height: 36px;
    border-radius: 50%;
    border: none;
    background-color: #f8f9fa;
    color: #0B2942;
    cursor: pointer;
    transition: all 0.2s ease;
  }
  
  .btn-add-relationship:hover {
    background-color: #0B2942;
    color: #fff;
    transform: rotate(90deg);
  }
  
  .relationship-list {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    flex: 1;
  }
  
  .relationship-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem;
    border-radius: 8px;
    background-color: #f8f9fa;
    transition: all 0.2s ease;
  }
  
  .relationship-item:hover {
    background-color: #f1f8ff;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  }
  
  .course-relation-info {
    display: flex;
    flex-direction: column;
  }
  
  .course-relation-info .course-code {
    font-weight: 600;
    font-size: 0.9rem;
    color: #0B2942;
    margin-bottom: 0.25rem;
  }
  
  .course-relation-info .course-name {
    font-size: 0.95rem;
    font-weight: 500;
    color: #0B2942;
    margin-bottom: 0.25rem;
  }
  
  .course-relation-info .semester-info {
    font-size: 0.8rem;
    color: #6c757d;
  }
  
  .btn-remove {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 32px;
    height: 32px;
    border-radius: 50%;
    border: none;
    background-color: transparent;
    color: #dc3545;
    cursor: pointer;
    transition: all 0.2s ease;
  }
  
  .btn-remove:hover {
    background-color: rgba(220, 53, 69, 0.1);
    transform: scale(1.1);
  }
  
  .empty-relationship {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 2rem 0;
    text-align: center;
  }
  
  .empty-icon {
    font-size: 2rem;
    color: #6c757d;
    margin-bottom: 1rem;
  }
  
  .empty-relationship p {
    color: #6c757d;
    margin: 0;
    font-style: italic;
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
  
  /* Form styling */
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
  
  .form-control, .form-select {
    width: 100%;
    padding: 0.75rem;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    font-size: 0.95rem;
    transition: all 0.3s;
  }
  
  .form-control:focus, .form-select:focus {
    outline: none;
    border-color: #4da0ff;
    box-shadow: 0 0 0 3px rgba(77, 160, 255, 0.25);
  }
  
  .form-control:disabled, .form-select:disabled {
    background-color: #f8f9fa;
    cursor: not-allowed;
  }
  
  .form-control.is-invalid, .form-select.is-invalid {
    border-color: #dc3545;
  }
  
  .invalid-feedback {
    color: #dc3545;
    font-size: 0.875em;
    margin-top: 0.25rem;
  }
  
  /* Course options in edit modal */
  .course-options {
    padding: 1rem 0;
    display: flex;
    gap: 1.5rem;
    flex-wrap: wrap;
  }
  
  .form-check {
    display: flex;
    align-items: center;
  }
  
  .form-check-input {
    margin-right: 0.5rem;
  }
  
  .form-check-label {
    font-weight: 500;
    color: #0B2942;
  }
  
  /* Search box */
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
  
  /* Available courses list in modals */
  .available-courses {
    max-height: 300px;
    overflow-y: auto;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    margin-top: 0.5rem;
  }
  
  .course-option {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.75rem 1rem;
    border-bottom: 1px solid #e0e0e0;
    transition: background-color 0.2s ease;
  }
  
  .course-option:last-child {
    border-bottom: none;
  }
  
  .course-option:hover {
    background-color: #f8f9fa;
  }
  
  .course-option-info {
    display: flex;
    flex-direction: column;
  }
  
  .course-option-info .course-code {
    font-weight: 600;
    font-size: 0.9rem;
    color: #0B2942;
    margin-bottom: 0.25rem;
  }
  
  .course-option-info .course-name {
    font-size: 0.95rem;
    font-weight: 500;
    color: #0B2942;
    margin-bottom: 0.25rem;
  }
  
  .course-option-info .semester-info {
    font-size: 0.8rem;
    color: #6c757d;
  }
  
  .btn-add-action {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 36px;
    height: 36px;
    border-radius: 50%;
    border: none;
    background-color: #f8f9fa;
    color: #0B2942;
    cursor: pointer;
    transition: all 0.2s ease;
  }
  
  .btn-add-action:hover:not(:disabled) {
    background-color: #0B2942;
    color: #fff;
  }
  
  .btn-add-action:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
  
  .btn-save {
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
  
  .btn-save:hover:not(:disabled) {
    background-color: #4da0ff;
  }
  
  .btn-save:disabled {
    background-color: #e9ecef;
    color: #6c757d;
    cursor: not-allowed;
  }
  
  .btn-cancel {
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
  
  .btn-cancel:hover {
    background-color: #e9ecef;
    color: #0B2942;
  }
  
  .empty-state {
    padding: 2rem;
    text-align: center;
    color: #6c757d;
    font-style: italic;
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
  
  .alert-warning {
    background-color: #fff3cd;
    color: #664d03;
    border: 1px solid #ffecb5;
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
  
  /* Responsive adjustments */
  @media (max-width: 768px) {
    .course-options {
      flex-direction: column;
      gap: 0.75rem;
    }
    
    .modal-footer {
      flex-direction: column-reverse;
    }
    
    .btn-save, .btn-cancel {
      width: 100%;
    }
    
    .btn-add-relationship {
      width: 32px;
      height: 32px;
    }
  }
  </style>
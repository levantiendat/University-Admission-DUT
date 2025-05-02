<template>
  <div class="admin-major-course-detail">
    <div class="admin-page-header">
      <div class="d-flex align-items-center">
        <router-link to="/admins/major-courses" class="btn-back">
          <i class="bi bi-arrow-left"></i>
        </router-link>
        <div>
          <h2 class="admin-page-title">Chi tiết khung chương trình đào tạo</h2>
          <p class="admin-page-description">Xem và chỉnh sửa thông tin khung chương trình</p>
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
      <p class="loading-text">Đang tải thông tin khung chương trình...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="error-message">
      <i class="bi bi-exclamation-triangle-fill error-icon"></i>
      <span>{{ error }}</span>
    </div>

    <div v-else class="content-container">
      <div class="row mb-4">
        <!-- Major Course Info Card -->
        <div class="col-md-4 mb-4">
          <div class="admin-card info-card">
            <div class="info-header">
              <div 
                class="course-badge"
                :class="{
                  'bachelor': majorCourse.type === 'Cử nhân',
                  'engineer': majorCourse.type === 'Kỹ sư',
                  'architect': majorCourse.type === 'Kiến trúc sư'
                }"
              >
                <i class="bi bi-mortarboard-fill"></i>
              </div>
              <h3 class="major-name">{{ getMajorName(majorCourse.major_id) }}</h3>
              <div class="course-type">
                <span 
                  class="type-badge" 
                  :class="{
                    'bachelor': majorCourse.type === 'Cử nhân',
                    'engineer': majorCourse.type === 'Kỹ sư',
                    'architect': majorCourse.type === 'Kiến trúc sư'
                  }"
                >
                  {{ majorCourse.type }} ({{ majorCourse.year }})
                </span>
              </div>
            </div>
            
            <div class="info-meta">
              <div class="info-item">
                <span class="info-label">ID:</span>
                <span class="info-value">#{{ majorCourse.id }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">Năm:</span>
                <span class="info-value">{{ majorCourse.year }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">Ngày tạo:</span>
                <span class="info-value">{{ formatDate(majorCourse.created_at) }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">Cập nhật:</span>
                <span class="info-value">{{ formatDate(majorCourse.updated_at) }}</span>
              </div>
            </div>

            <div class="info-actions">
              <button 
                class="btn-delete"
                @click="confirmDelete"
              >
                <i class="bi bi-trash me-2"></i>
                Xóa khung chương trình
              </button>
            </div>
          </div>
        </div>

        <!-- Edit Form -->
        <div class="col-md-8 mb-4">
          <div class="admin-card">
            <h3 class="section-title">Chỉnh sửa thông tin</h3>

            <form @submit.prevent="updateMajorCourse" class="edit-form">
              <div class="form-group">
                <label for="major-id">Ngành học</label>
                <select 
                  id="major-id" 
                  v-model="formData.major_id" 
                  class="form-select" 
                  disabled
                >
                  <option v-for="major in majors" :key="major.id" :value="major.id">
                    {{ major.name }}
                  </option>
                </select>
                <small class="form-text text-muted">Không thể thay đổi ngành học</small>
              </div>

              <div class="row">
                <div class="col-md-6">
                  <div class="form-group">
                    <label for="year">Năm <span class="required">*</span></label>
                    <select 
                      id="year" 
                      v-model="formData.year" 
                      class="form-select" 
                      required
                      :class="{ 'is-invalid': errors.year }"
                    >
                      <option v-for="year in availableYears" :key="year" :value="year">
                        {{ year }}
                      </option>
                    </select>
                    <div v-if="errors.year" class="invalid-feedback">{{ errors.year }}</div>
                  </div>
                </div>

                <div class="col-md-6">
                  <div class="form-group">
                    <label for="type">Loại chương trình đào tạo <span class="required">*</span></label>
                    <select 
                      id="type" 
                      v-model="formData.type" 
                      class="form-select" 
                      required
                      :class="{ 'is-invalid': errors.type }"
                    >
                      <option value="Cử nhân">Cử nhân</option>
                      <option value="Kỹ sư">Kỹ sư</option>
                      <option value="Kiến trúc sư">Kiến trúc sư</option>
                    </select>
                    <div v-if="errors.type" class="invalid-feedback">{{ errors.type }}</div>
                  </div>
                </div>
              </div>

              <div class="alert alert-warning" v-if="isDuplicate">
                <i class="bi bi-exclamation-triangle-fill me-2"></i>
                <strong>Cảnh báo:</strong> Đã tồn tại khung chương trình {{ formData.type }} cho ngành này trong năm {{ formData.year }}. Vui lòng kiểm tra lại.
              </div>

              <div v-if="updateError" class="alert alert-danger">{{ updateError }}</div>

              <div class="form-actions">
                <button type="submit" class="btn-save" :disabled="isUpdating || isDuplicate">
                  <i class="bi bi-check-circle me-2"></i>
                  {{ isUpdating ? 'Đang lưu...' : 'Lưu thay đổi' }}
                </button>
                <button type="button" class="btn-cancel" @click="resetForm">
                  <i class="bi bi-x-circle me-2"></i>
                  Hủy thay đổi
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>

      <!-- Course Details Management Section -->
      <div class="admin-card">
        <div class="d-flex justify-content-between align-items-center mb-4">
          <h3 class="section-title mb-0">Học phần trong chương trình đào tạo</h3>
          <button class="btn-add" @click="showAddCourseModal = true">
            <i class="bi bi-plus-circle me-2"></i>Thêm học phần mới
          </button>
        </div>

        <!-- Course details filters -->
        <div class="row mb-4">
          <div class="col-md-3 mb-3">
            <div class="form-group">
              <label for="filter-semester">Học kỳ</label>
              <select id="filter-semester" v-model="courseFilters.semester" class="form-select" @change="filterCourses">
                <option value="">Tất cả học kỳ</option>
                <option v-for="semester in availableSemesters" :key="semester" :value="semester">
                  Học kỳ {{ semester }}
                </option>
              </select>
            </div>
          </div>
          <div class="col-md-3 mb-3">
            <div class="form-group">
              <label for="filter-type">Loại học phần</label>
              <select id="filter-type" v-model="courseFilters.type" class="form-select" @change="filterCourses">
                <option value="">Tất cả loại</option>
                <option value="regular">Bắt buộc</option>
                <option value="elective">Tự chọn</option>
                <option value="pre_capstone">Tiền đồ án</option>
                <option value="mandatory_capstone">Đồ án bắt buộc</option>
              </select>
            </div>
          </div>
          <div class="col-md-6 mb-3">
            <div class="form-group">
              <label for="search-course">Tìm kiếm học phần</label>
              <div class="search-box">
                <i class="bi bi-search search-icon"></i>
                <input 
                  type="text" 
                  id="search-course" 
                  v-model="courseFilters.search" 
                  class="search-input" 
                  placeholder="Tìm theo mã hoặc tên học phần..." 
                  @input="filterCourses"
                >
              </div>
            </div>
          </div>
        </div>

        <!-- Loading details state -->
        <div v-if="loadingDetails" class="loading-container">
          <div class="spinner">
            <div class="bounce1"></div>
            <div class="bounce2"></div>
            <div class="bounce3"></div>
          </div>
          <p class="loading-text">Đang tải danh sách học phần...</p>
        </div>

        <!-- Error state for details -->
        <div v-else-if="detailsError" class="error-message">
          <i class="bi bi-exclamation-triangle-fill error-icon"></i>
          <span>{{ detailsError }}</span>
        </div>

        <!-- Course details table -->
        <div v-else-if="filteredCourseDetails.length" class="table-responsive">
          <table class="data-table">
            <thead>
              <tr>
                <th width="10%">Mã học phần</th>
                <th width="35%">Tên học phần</th>
                <th width="10%">Tín chỉ</th>
                <th width="10%">Học kỳ</th>
                <th width="20%">Loại</th>
                <th width="15%">Thao tác</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="detail in filteredCourseDetails" :key="detail.id" class="data-row">
                <td>
                  <span class="course-code">{{ getCourseById(detail.course_id)?.course_code }}</span>
                </td>
                <td>
                  <span class="course-name">{{ getCourseById(detail.course_id)?.name }}</span>
                </td>
                <td>
                  <span class="credits-badge">{{ getCourseById(detail.course_id)?.credits }}</span>
                </td>
                <td>
                  <span class="semester-badge">{{ detail.semester }}</span>
                </td>
                <td>
                  <div class="course-types">
                    <span v-if="detail.elective_course" class="type-pill elective" title="Tự chọn">TC</span>
                    <span v-if="detail.pre_capstone" class="type-pill pre-capstone" title="Học trước đồ án">HT DA</span>
                    <span v-if="detail.mandatory_capstone" class="type-pill capstone" title="Tiên quyết đồ án">TQ ĐA</span>
                    <span v-if="!detail.elective_course && !detail.pre_capstone && !detail.mandatory_capstone" class="type-pill regular" title="Học phần thường">T</span>
                  </div>
                </td>
                <td>
                  <div class="action-buttons">
                    <router-link 
                      :to="`/admins/major-courses/details/${detail.id}`" 
                      class="btn-action edit" 
                      title="Sửa thông tin học phần"
                    >
                      <i class="bi bi-pencil-square"></i>
                    </router-link>
                    <button 
                      class="btn-action relationships" 
                      title="Xem mối quan hệ"
                      @click="viewRelationships(detail)"
                    >
                      <i class="bi bi-diagram-3"></i>
                    </button>
                    <button 
                      class="btn-action delete"
                      @click="confirmDeleteDetail(detail)"
                      title="Xóa học phần khỏi chương trình"
                    >
                      <i class="bi bi-trash"></i>
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Empty state for course details -->
        <div v-else class="empty-state">
          <i class="bi bi-journal-x empty-icon"></i>
          <h4>Không tìm thấy học phần nào</h4>
          <p v-if="hasCourseFilters">Thử thay đổi bộ lọc hoặc tìm kiếm</p>
          <p v-else>Khung chương trình này chưa có học phần nào</p>
          <button class="btn-create-empty" @click="showAddCourseModal = true">
            <i class="bi bi-plus-circle me-2"></i>Thêm học phần mới
          </button>
        </div>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div v-if="showDeleteModal" class="modal-overlay" @click="cancelDelete">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h4 class="modal-title">Xác nhận xóa khung chương trình</h4>
          <button type="button" class="btn-close" @click="cancelDelete"></button>
        </div>
        <div class="modal-body">
          <p>Bạn có chắc chắn muốn xóa khung chương trình <strong>{{ majorCourse.type }}</strong> của ngành <strong>{{ getMajorName(majorCourse.major_id) }}</strong> năm <strong>{{ majorCourse.year }}</strong>?</p>
          <p class="text-danger">
            <i class="bi bi-exclamation-triangle me-2"></i>
            Thao tác này không thể khôi phục lại!
          </p>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn-cancel" @click="cancelDelete">Hủy</button>
          <button type="button" class="btn-delete" @click="deleteMajorCourse" :disabled="isDeleting">
            <span v-if="isDeleting">Đang xóa...</span>
            <span v-else>Xác nhận xóa</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Delete Course Detail Confirmation Modal -->
    <div v-if="showDeleteDetailModal" class="modal-overlay" @click="cancelDeleteDetail">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h4 class="modal-title">Xác nhận xóa học phần</h4>
          <button type="button" class="btn-close" @click="cancelDeleteDetail"></button>
        </div>
        <div class="modal-body">
          <p>Bạn có chắc chắn muốn xóa học phần <strong>{{ getCourseById(courseDetailToDelete?.course_id)?.name }}</strong> khỏi khung chương trình này?</p>
          <p class="text-danger">
            <i class="bi bi-exclamation-triangle me-2"></i>
            Thao tác này sẽ xóa cả các mối quan hệ của học phần này!
          </p>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn-cancel" @click="cancelDeleteDetail">Hủy</button>
          <button type="button" class="btn-delete" @click="deleteCourseDetail" :disabled="isDeletingDetail">
            <span v-if="isDeletingDetail">Đang xóa...</span>
            <span v-else>Xác nhận xóa</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Add Course Modal -->
    <div v-if="showAddCourseModal" class="modal-overlay" @click="cancelAddCourse">
      <div class="modal-content modal-lg" @click.stop>
        <div class="modal-header">
          <h4 class="modal-title">Thêm học phần mới</h4>
          <button type="button" class="btn-close" @click="cancelAddCourse"></button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="addCourseDetail">
            <div class="row">
              <div class="col-md-8 mb-3">
                <div class="form-group">
                  <label for="course-id">Học phần <span class="required">*</span></label>
                  <select 
                    id="course-id" 
                    v-model="newCourseDetail.course_id" 
                    class="form-select" 
                    required
                    :class="{ 'is-invalid': newCourseErrors.course_id }"
                  >
                    <option value="" disabled selected>Chọn học phần</option>
                    <option v-for="course in availableCourses" :key="course.id" :value="course.id">
                      {{ course.course_code }} - {{ course.name }} ({{ course.credits }} TC)
                    </option>
                  </select>
                  <div v-if="newCourseErrors.course_id" class="invalid-feedback">{{ newCourseErrors.course_id }}</div>
                </div>
              </div>
              <div class="col-md-4 mb-3">
                <div class="form-group">
                  <label for="semester">Học kỳ <span class="required">*</span></label>
                  <select 
                    id="semester" 
                    v-model="newCourseDetail.semester" 
                    class="form-select" 
                    required
                    :class="{ 'is-invalid': newCourseErrors.semester }"
                  >
                    <option value="" disabled selected>Chọn học kỳ</option>
                    <option v-for="i in 10" :key="i" :value="i">Học kỳ {{ i }}</option>
                  </select>
                  <div v-if="newCourseErrors.semester" class="invalid-feedback">{{ newCourseErrors.semester }}</div>
                </div>
              </div>
            </div>

            <div class="course-options">
              <div class="form-check">
                <input 
                  type="checkbox" 
                  id="elective-course" 
                  v-model="newCourseDetail.elective_course" 
                  class="form-check-input"
                >
                <label for="elective-course" class="form-check-label">Học phần tự chọn</label>
              </div>

              <div class="form-check">
                <input 
                  type="checkbox" 
                  id="pre-capstone" 
                  v-model="newCourseDetail.pre_capstone" 
                  class="form-check-input"
                >
                <label for="pre-capstone" class="form-check-label">Học trước đồ án</label>
              </div>

              <div class="form-check">
                <input 
                  type="checkbox" 
                  id="mandatory-capstone" 
                  v-model="newCourseDetail.mandatory_capstone" 
                  class="form-check-input"
                >
                <label for="mandatory-capstone" class="form-check-label">Tiên quyết đồ án</label>
              </div>
            </div>

            <div v-if="addCourseError" class="alert alert-danger mt-3">
              {{ addCourseError }}
            </div>

            <div class="modal-footer">
              <button type="button" class="btn-cancel" @click="cancelAddCourse">Hủy</button>
              <button type="submit" class="btn-add" :disabled="isAddingCourse">
                {{ isAddingCourse ? 'Đang thêm...' : 'Thêm học phần' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- View Relationships Modal -->
    <div v-if="showRelationshipsModal" class="modal-overlay" @click="closeRelationships">
  <div class="modal-content modal-md" @click.stop>
    <div class="modal-header">
      <h4 class="modal-title">Mối quan hệ học phần</h4>
      <button type="button" class="btn-close" @click="closeRelationships"></button>
    </div>
    <div class="modal-body">
      <div class="course-info mb-3">
        <h5 class="course-name">{{ getCourseById(selectedDetail?.course_id)?.name }}</h5>
        <p class="course-code">({{ getCourseById(selectedDetail?.course_id)?.course_code }})</p>
        <div class="course-meta">
          <span class="semester-badge">Học kỳ {{ selectedDetail?.semester }}</span>
          <span v-if="selectedDetail?.elective_course" class="type-pill elective">Tự chọn</span>
        </div>
      </div>

      <div class="relationships-container">
        <!-- Prior courses -->
        <div class="relationship-section">
          <h6 class="relationship-title"><i class="bi bi-box-arrow-in-up-right me-1"></i>Học phần học trước</h6>
          <div v-if="selectedDetail?.prior_courses?.length" class="relationship-list compact">
            <div v-for="priorId in selectedDetail.prior_courses" :key="`prior-${priorId}`" class="relationship-item">
              <div class="course-relation-info">
                <div class="d-flex align-items-center">
                  <span class="course-code me-2">{{ getCourseFromDetailId(priorId)?.course_code }}</span>
                  <span class="course-name">{{ getCourseFromDetailId(priorId)?.name }}</span>
                </div>
              </div>
              <button class="btn-remove-sm" @click="confirmRemovePriorCourse(priorId)" title="Xóa mối quan hệ">
                <i class="bi bi-x"></i>
              </button>
            </div>
          </div>
          <div v-else class="empty-relationship">Không có học phần học trước</div>
        </div>

        <!-- Prerequisites -->
        <div class="relationship-section">
          <h6 class="relationship-title"><i class="bi bi-arrow-left-circle me-1"></i>Học phần tiên quyết</h6>
          <div v-if="selectedDetail?.prerequisites?.length" class="relationship-list compact">
            <div v-for="prerequisiteId in selectedDetail.prerequisites" :key="`prerequisite-${prerequisiteId}`" class="relationship-item">
              <div class="course-relation-info">
                <div class="d-flex align-items-center">
                  <span class="course-code me-2">{{ getCourseFromDetailId(prerequisiteId)?.course_code }}</span>
                  <span class="course-name">{{ getCourseFromDetailId(prerequisiteId)?.name }}</span>
                </div>
              </div>
              <button class="btn-remove-sm" @click="confirmRemovePrerequisite(prerequisiteId)" title="Xóa mối quan hệ">
                <i class="bi bi-x"></i>
              </button>
            </div>
          </div>
          <div v-else class="empty-relationship">Không có học phần tiên quyết</div>
        </div>

        <!-- Corequisites -->
        <div class="relationship-section">
          <h6 class="relationship-title"><i class="bi bi-arrows-angle-expand me-1"></i>Học phần song hành</h6>
          <div v-if="selectedDetail?.corequisites?.length" class="relationship-list compact">
            <div v-for="corequisiteId in selectedDetail.corequisites" :key="`corequisite-${corequisiteId}`" class="relationship-item">
              <div class="course-relation-info">
                <div class="d-flex align-items-center">
                  <span class="course-code me-2">{{ getCourseFromDetailId(corequisiteId)?.course_code }}</span>
                  <span class="course-name">{{ getCourseFromDetailId(corequisiteId)?.name }}</span>
                </div>
              </div>
              <button class="btn-remove-sm" @click="confirmRemoveCorequisite(corequisiteId)" title="Xóa mối quan hệ">
                <i class="bi bi-x"></i>
              </button>
            </div>
          </div>
          <div v-else class="empty-relationship">Không có học phần song hành</div>
        </div>
      </div>
      
      <router-link :to="`/admins/major-courses/details/${selectedDetail?.id}`" class="btn-edit-relationships">
        <i class="bi bi-gear me-2"></i>Quản lý chi tiết mối quan hệ
      </router-link>
    </div>
  </div>
</div>
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import MajorCourseController from '@/controllers/admins/MajorCourseController'
import MajorController from '@/controllers/admins/MajorController'
import CourseController from '@/controllers/admins/CourseController'

export default {
  name: 'AdminMajorCourseDetail',
  props: {
    majorCourseId: {
      type: [String, Number],
      required: true
    }
  },
  setup(props) {
    const router = useRouter()
    const majorCourse = ref({})
    const formData = reactive({
      major_id: '',
      year: '',
      type: ''
    })
    
    const existingMajorCourses = ref([])
    const majors = ref([])
    
    const loading = ref(true)
    const error = ref(null)
    const updateError = ref(null)
    const isUpdating = ref(false)
    const errors = reactive({
      year: '',
      type: ''
    })
    
    // Delete modal state
    const showDeleteModal = ref(false)
    const isDeleting = ref(false)
    
    // Course details state
    const courseDetails = ref([])
    const allCourses = ref([])
    const filteredCourseDetails = ref([])
    const loadingDetails = ref(false)
    const detailsError = ref(null)
    
    // Course detail delete state
    const showDeleteDetailModal = ref(false)
    const courseDetailToDelete = ref(null)
    const isDeletingDetail = ref(false)
    
    // Course detail add state
    const showAddCourseModal = ref(false)
    const isAddingCourse = ref(false)
    const addCourseError = ref(null)
    const newCourseDetail = reactive({
      course_id: '',
      semester: '',
      elective_course: false,
      pre_capstone: false,
      mandatory_capstone: false
    })
    const newCourseErrors = reactive({
      course_id: '',
      semester: ''
    })
    
    // Relationships modal state
    const showRelationshipsModal = ref(false)
    const selectedDetail = ref(null)
    
    // Filters for course details
    const courseFilters = reactive({
      semester: '',
      type: '',
      search: ''
    })
    
    // Generate a list of years (current year - 5 to current year + 5)
    const availableYears = computed(() => {
      const currentYear = new Date().getFullYear()
      const years = []
      for (let i = -5; i <= 5; i++) {
        years.push(currentYear + i)
      }
      return years.sort((a, b) => b - a) // Sort years in descending order
    })
    
    // Available semesters from course details
    const availableSemesters = computed(() => {
      const semesters = [...new Set(courseDetails.value.map(d => d.semester))].sort((a, b) => a - b)
      return semesters
    })
    
    // Available courses for adding (exclude already added courses)
    const availableCourses = computed(() => {
      const existingCourseIds = courseDetails.value.map(d => d.course_id)
      return allCourses.value.filter(c => !existingCourseIds.includes(c.id))
    })
    
    // Check if there's a duplicate entry
    const isDuplicate = computed(() => {
      if (!formData.major_id || !formData.year || !formData.type) {
        return false
      }
      
      // Check if values changed from original
      if (
        parseInt(formData.year) === majorCourse.value.year &&
        formData.type === majorCourse.value.type
      ) {
        return false // Not changed, so no duplicate
      }
      
      return existingMajorCourses.value.some(course => 
        parseInt(course.major_id) === parseInt(formData.major_id) &&
        parseInt(course.year) === parseInt(formData.year) &&
        course.type === formData.type &&
        course.id !== parseInt(props.majorCourseId) // Exclude current course
      )
    })
    
    // Check if any course filters are applied
    const hasCourseFilters = computed(() => {
      return courseFilters.semester || courseFilters.type || courseFilters.search
    })
    
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
    
    // Get major name by ID
    const getMajorName = (majorId) => {
      const major = majors.value.find(m => m.id === majorId)
      return major ? major.name : 'Không xác định'
    }
    
    // Get course by ID
    const getCourseById = (courseId) => {
      return allCourses.value.find(c => c.id === courseId)
    }
    
    // Get course from a detail ID
    const getCourseFromDetailId = (detailId) => {
      const detail = courseDetails.value.find(d => d.id === detailId)
      if (!detail) return null
      return getCourseById(detail.course_id)
    }
    
    // Filter courses based on applied filters
    const filterCourses = () => {
      filteredCourseDetails.value = courseDetails.value.filter(detail => {
        const course = getCourseById(detail.course_id)
        if (!course) return false
        
        // Apply semester filter
        if (courseFilters.semester && detail.semester !== parseInt(courseFilters.semester)) {
          return false
        }
        
        // Apply type filter
        if (courseFilters.type) {
          switch (courseFilters.type) {
            case 'regular':
              if (detail.elective_course || detail.pre_capstone || detail.mandatory_capstone) {
                return false
              }
              break
            case 'elective':
              if (!detail.elective_course) {
                return false
              }
              break
            case 'pre_capstone':
              if (!detail.pre_capstone) {
                return false
              }
              break
            case 'mandatory_capstone':
              if (!detail.mandatory_capstone) {
                return false
              }
              break
          }
        }
        
        // Apply search filter
        if (courseFilters.search) {
          const search = courseFilters.search.toLowerCase()
          return (
            course.name.toLowerCase().includes(search) ||
            course.course_code.toLowerCase().includes(search)
          )
        }
        
        return true
      })
    }
    
    // Fetch major course details
    const fetchMajorCourseDetails = async () => {
      try {
        loading.value = true
        error.value = null
        
        // Load all data in parallel
        const [courseData, coursesData, majorsData] = await Promise.all([
          MajorCourseController.getMajorCourseById(props.majorCourseId),
          MajorCourseController.getAllMajorCourses(),
          MajorController.getAllMajors()
        ])
        
        majorCourse.value = courseData
        existingMajorCourses.value = coursesData
        majors.value = majorsData
        
        // Set form data
        formData.major_id = courseData.major_id
        formData.year = courseData.year
        formData.type = courseData.type
        
        // Fetch course details and all courses
        await fetchCourseDetails()
      } catch (err) {
        error.value = `Không thể tải thông tin khung chương trình: ${err.message}`
      } finally {
        loading.value = false
      }
    }
    
    // Fetch course details for this major course
    const fetchCourseDetails = async () => {
      try {
        loadingDetails.value = true
        detailsError.value = null
        
        const [coursesResponse, allCoursesData] = await Promise.all([
          MajorCourseController.getMajorCourseDetailsById(props.majorCourseId),
          CourseController.getAllCourses()
        ])
        
        allCourses.value = allCoursesData
        courseDetails.value = coursesResponse.major_course_details || []
        
        // Apply initial filtering
        filterCourses()
      } catch (err) {
        detailsError.value = `Không thể tải danh sách học phần: ${err.message}`
      } finally {
        loadingDetails.value = false
      }
    }
    
    // Reset form
    const resetForm = () => {
      // Reset to original values
      formData.year = majorCourse.value.year
      formData.type = majorCourse.value.type
      
      // Clear errors
      Object.keys(errors).forEach(key => {
        errors[key] = ''
      })
      updateError.value = null
    }
    
    // Validate form
    const validateForm = () => {
      let isValid = true
      
      // Clear previous errors
      Object.keys(errors).forEach(key => {
        errors[key] = ''
      })
      updateError.value = null
      
      if (!formData.year) {
        errors.year = 'Vui lòng chọn năm'
        isValid = false
      }
      
      if (!formData.type) {
        errors.type = 'Vui lòng chọn loại chương trình đào tạo'
        isValid = false
      }
      
      if (isDuplicate.value) {
        updateError.value = 'Đã tồn tại khung chương trình này'
        isValid = false
      }
      
      return isValid
    }
    
    // Update major course
    const updateMajorCourse = async () => {
      try {
        // Validate form
        if (!validateForm()) {
          return
        }
        
        isUpdating.value = true
        
        const updatedData = {
          year: parseInt(formData.year),
          type: formData.type
        }
        
        await MajorCourseController.updateMajorCourse(props.majorCourseId, updatedData)
        
        // Update local state
        Object.assign(majorCourse.value, updatedData, { updated_at: new Date().toISOString() })
        
        alert('Cập nhật khung chương trình thành công')
      } catch (err) {
        updateError.value = `Không thể cập nhật khung chương trình: ${err.message}`
      } finally {
        isUpdating.value = false
      }
    }
    
    // Confirm delete
    const confirmDelete = () => {
      showDeleteModal.value = true
    }
    
    // Cancel delete
    const cancelDelete = () => {
      showDeleteModal.value = false
    }
    
    // Delete major course
    const deleteMajorCourse = async () => {
      try {
        isDeleting.value = true
        
        await MajorCourseController.deleteMajorCourse(props.majorCourseId)
        
        alert('Xóa khung chương trình thành công')
        router.push('/admins/major-courses')
      } catch (err) {
        alert(`Lỗi: ${err.message}`)
      } finally {
        isDeleting.value = false
        showDeleteModal.value = false
      }
    }
    
    // Confirm delete course detail
    const confirmDeleteDetail = (detail) => {
      courseDetailToDelete.value = detail
      showDeleteDetailModal.value = true
    }
    
    // Cancel delete detail
    const cancelDeleteDetail = () => {
      courseDetailToDelete.value = null
      showDeleteDetailModal.value = false
    }
    
    // Delete course detail
    const deleteCourseDetail = async () => {
      if (!courseDetailToDelete.value) return
      
      try {
        isDeletingDetail.value = true
        
        await MajorCourseController.deleteMajorCourseDetail(courseDetailToDelete.value.id)
        
        // Remove from lists and update filtered list
        courseDetails.value = courseDetails.value.filter(d => d.id !== courseDetailToDelete.value.id)
        filterCourses()
        
        alert('Đã xóa học phần khỏi khung chương trình')
      } catch (err) {
        alert(`Lỗi: ${err.message}`)
      } finally {
        isDeletingDetail.value = false
        cancelDeleteDetail()
      }
    }
    
    // Cancel adding a course
    const cancelAddCourse = () => {
      showAddCourseModal.value = false
      // Reset form
      newCourseDetail.course_id = ''
      newCourseDetail.semester = ''
      newCourseDetail.elective_course = false
      newCourseDetail.pre_capstone = false
      newCourseDetail.mandatory_capstone = false
      
      // Clear errors
      Object.keys(newCourseErrors).forEach(key => {
        newCourseErrors[key] = ''
      })
      addCourseError.value = null
    }
    
    // Validate new course detail
    const validateNewCourse = () => {
      let isValid = true
      
      // Clear errors
      Object.keys(newCourseErrors).forEach(key => {
        newCourseErrors[key] = ''
      })
      addCourseError.value = null
      
      if (!newCourseDetail.course_id) {
        newCourseErrors.course_id = 'Vui lòng chọn học phần'
        isValid = false
      }
      
      if (!newCourseDetail.semester) {
        newCourseErrors.semester = 'Vui lòng chọn học kỳ'
        isValid = false
      } else if (isNaN(parseInt(newCourseDetail.semester)) || parseInt(newCourseDetail.semester) < 1) {
        newCourseErrors.semester = 'Học kỳ không hợp lệ'
        isValid = false
      }
      
      // Check if course is already in this major course
      const existingCourse = courseDetails.value.find(d => d.course_id === parseInt(newCourseDetail.course_id))
      if (existingCourse) {
        addCourseError.value = 'Học phần này đã có trong khung chương trình'
        isValid = false
      }
      
      return isValid
    }
    
    // Add new course detail
    const addCourseDetail = async () => {
      try {
        // Validate
        if (!validateNewCourse()) {
          return
        }
        
        isAddingCourse.value = true
        
        const data = {
          major_course_id: parseInt(props.majorCourseId),
          course_id: parseInt(newCourseDetail.course_id),
          semester: parseInt(newCourseDetail.semester),
          elective_course: newCourseDetail.elective_course,
          pre_capstone: newCourseDetail.pre_capstone,
          mandatory_capstone: newCourseDetail.mandatory_capstone
        }
        
        const result = await MajorCourseController.createMajorCourseDetail(data)
        
        // Add to the list and update filtered list
        courseDetails.value.push(result)
        filterCourses()
        
        // Close modal and reset
        cancelAddCourse()
        
        alert('Thêm học phần thành công')
      } catch (err) {
        addCourseError.value = `Không thể thêm học phần: ${err.message}`
      } finally {
        isAddingCourse.value = false
      }
    }
    
    // View relationships of a course detail
    const viewRelationships = (detail) => {
      selectedDetail.value = detail
      showRelationshipsModal.value = true
    }
    
    // Close relationships modal
    const closeRelationships = () => {
      selectedDetail.value = null
      showRelationshipsModal.value = false
    }
    
    // Confirm remove prior course
    const confirmRemovePriorCourse = async (priorId) => {
      if (!selectedDetail.value) return
      
      try {
        // Get the relationship ID
        const priorCourses = await MajorCourseController.getAllPriorCourses()
        const relationship = priorCourses.find(
          p => p.major_course_detail_id === selectedDetail.value.id && 
               p.prior_course_detail_id === priorId
        )
        
        if (!relationship) {
          throw new Error('Không tìm thấy mối quan hệ này')
        }
        
        if (confirm('Bạn có chắc chắn muốn xóa mối quan hệ học trước này?')) {
          await MajorCourseController.removePriorCourse(relationship.id)
          
          // Update the selected detail
          selectedDetail.value.prior_courses = selectedDetail.value.prior_courses.filter(id => id !== priorId)
          
          // Update in course details list
          const index = courseDetails.value.findIndex(d => d.id === selectedDetail.value.id)
          if (index !== -1) {
            courseDetails.value[index] = { ...selectedDetail.value }
          }
          
          alert('Đã xóa mối quan hệ học trước')
        }
      } catch (err) {
        alert(`Lỗi: ${err.message}`)
      }
    }
    
    // Confirm remove prerequisite
    const confirmRemovePrerequisite = async (prerequisiteId) => {
      if (!selectedDetail.value) return
      
      try {
        // Get the relationship ID
        const prerequisites = await MajorCourseController.getAllPrerequisites()
        const relationship = prerequisites.find(
          p => p.major_course_detail_id === selectedDetail.value.id && 
               p.prerequisite_major_course_detail_id === prerequisiteId
        )
        
        if (!relationship) {
          throw new Error('Không tìm thấy mối quan hệ này')
        }
        
        if (confirm('Bạn có chắc chắn muốn xóa mối quan hệ tiên quyết này?')) {
          await MajorCourseController.removePrerequisite(relationship.id)
          
          // Update the selected detail
          selectedDetail.value.prerequisites = selectedDetail.value.prerequisites.filter(id => id !== prerequisiteId)
          
          // Update in course details list
          const index = courseDetails.value.findIndex(d => d.id === selectedDetail.value.id)
          if (index !== -1) {
            courseDetails.value[index] = { ...selectedDetail.value }
          }
          
          alert('Đã xóa mối quan hệ tiên quyết')
        }
      } catch (err) {
        alert(`Lỗi: ${err.message}`)
      }
    }
    
    // Confirm remove corequisite
    const confirmRemoveCorequisite = async (corequisiteId) => {
      if (!selectedDetail.value) return
      
      try {
        // Get the relationship ID
        const corequisites = await MajorCourseController.getAllCorequisites()
        const relationship = corequisites.find(
          c => c.major_course_detail_id === selectedDetail.value.id && 
               c.corequisite_major_course_detail_id === corequisiteId
        )
        
        if (!relationship) {
          throw new Error('Không tìm thấy mối quan hệ này')
        }
        
        if (confirm('Bạn có chắc chắn muốn xóa mối quan hệ song hành này?')) {
          await MajorCourseController.removeCorequisite(relationship.id)
          
          // Update the selected detail
          selectedDetail.value.corequisites = selectedDetail.value.corequisites.filter(id => id !== corequisiteId)
          
          // Update in course details list
          const index = courseDetails.value.findIndex(d => d.id === selectedDetail.value.id)
          if (index !== -1) {
            courseDetails.value[index] = { ...selectedDetail.value }
          }
          
          alert('Đã xóa mối quan hệ song hành')
        }
      } catch (err) {
        alert(`Lỗi: ${err.message}`)
      }
    }

    onMounted(() => {
      fetchMajorCourseDetails()
    })

    return {
      majorCourse,
      formData,
      majors,
      loading,
      error,
      updateError,
      isUpdating,
      errors,
      showDeleteModal,
      isDeleting,
      availableYears,
      isDuplicate,
      courseDetails,
      allCourses,
      filteredCourseDetails,
      loadingDetails,
      detailsError,
      showDeleteDetailModal,
      courseDetailToDelete,
      isDeletingDetail,
      showAddCourseModal,
      isAddingCourse,
      addCourseError,
      newCourseDetail,
      newCourseErrors,
      showRelationshipsModal,
      selectedDetail,
      courseFilters,
      availableSemesters,
      availableCourses,
      hasCourseFilters,
      formatDate,
      getMajorName,
      getCourseById,
      getCourseFromDetailId,
      filterCourses,
      resetForm,
      updateMajorCourse,
      confirmDelete,
      cancelDelete,
      deleteMajorCourse,
      confirmDeleteDetail,
      cancelDeleteDetail,
      deleteCourseDetail,
      cancelAddCourse,
      addCourseDetail,
      viewRelationships,
      closeRelationships,
      confirmRemovePriorCourse,
      confirmRemovePrerequisite,
      confirmRemoveCorequisite
    }
  }
}
</script>

<style scoped>
.admin-major-course-detail {
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
  height: 100%;
  transition: all 0.3s ease;
}

.admin-card:hover {
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
}

/* Info Card Styling */
.info-card {
  display: flex;
  flex-direction: column;
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

.course-badge {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1rem;
  font-size: 2.5rem;
}

.course-badge.bachelor {
  background-color: #e3f2fd;
  color: #0d6efd;
}

.course-badge.engineer {
  background-color: #e8f5e9;
  color: #28a745;
}

.course-badge.architect {
  background-color: #fff8e1;
  color: #ffc107;
}

.major-name {
  font-size: 1.3rem;
  font-weight: 600;
  color: #0B2942;
  margin-bottom: 1rem;
}

.course-type {
  margin-bottom: 0.5rem;
}

.type-badge {
  display: inline-block;
  padding: 0.35rem 0.75rem;
  border-radius: 50px;
  font-size: 0.85rem;
  font-weight: 500;
}

.type-badge.bachelor {
  background-color: #e3f2fd;
  color: #0d6efd;
}

.type-badge.engineer {
  background-color: #e8f5e9;
  color: #28a745;
}

.type-badge.architect {
  background-color: #fff8e1;
  color: #ffc107;
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

.btn-delete {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0.75rem 1rem;
  background-color: #f8f9fa;
  border: 1px solid #dc3545;
  color: #dc3545;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-delete:hover {
  background-color: #dc3545;
  color: white;
}

.btn-add {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.75rem 1.25rem;
  background-color: #0B2942;
  color: #fff;
  font-weight: 500;
  border-radius: 8px;
  text-decoration: none;
  transition: all 0.3s;
  border: none;
  cursor: pointer;
}

.btn-add:hover:not(:disabled) {
  background-color: #4da0ff;
  transform: translateY(-2px);
}

.btn-add:disabled {
  background-color: #e9ecef;
  color: #6c757d;
  cursor: not-allowed;
}

/* Form Styling */
.section-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #0B2942;
  margin-bottom: 1.5rem;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid #e9ecef;
}

.edit-form {
  width: 100%;
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

.form-text {
  font-size: 0.85rem;
  margin-top: 0.25rem;
}

.text-muted {
  color: #6c757d;
}

.form-actions {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
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

/* Search and filter */
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

/* Course details table */
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

.course-code {
  font-weight: 600;
  color: #0B2942;
}

.course-name {
  font-weight: 500;
  color: #0B2942;
}

.credits-badge {
  display: inline-block;
  padding: 0.35rem 0.65rem;
  border-radius: 50px;
  font-size: 0.85rem;
  font-weight: 500;
  background-color: #e9f5ff;
  color: #0B2942;
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

.course-types {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.type-pill {
  display: inline-block;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 600;
  text-align: center;
}

.type-pill.regular {
  background-color: #e9ecef;
  color: #495057;
}

.type-pill.elective {
  background-color: #e3f2fd;
  color: #0d6efd;
}

.type-pill.pre-capstone {
  background-color: #fff3cd;
  color: #ffc107;
}

.type-pill.capstone {
  background-color: #d1e7dd;
  color: #198754;
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
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-action.edit {
  color: #0B2942;
}

.btn-action.relationships {
  color: #0d6efd;
}

.btn-action.delete {
  color: #dc3545;
}

.btn-action:hover {
  background-color: #f8f9fa;
  transform: translateY(-2px);
}

.btn-action.edit:hover {
  background-color: rgba(11, 41, 66, 0.1);
}

.btn-action.relationships:hover {
  background-color: rgba(13, 110, 253, 0.1);
}

.btn-action.delete:hover {
  background-color: rgba(220, 53, 69, 0.1);
}

/* Empty state */
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
  margin-bottom: 1.5rem;
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
  transition: all 0.3s;
  border: none;
  cursor: pointer;
}

.btn-create-empty:hover {
  background-color: #4da0ff;
  color: #fff;
}

/* Relationships modal - PHẦN CẬP NHẬT */
.modal-content.modal-md {
  max-width: 500px;
}

.course-info {
  padding-bottom: 0.75rem;
  border-bottom: 1px solid #e9ecef;
  text-align: center;
}

.course-info .course-name {
  font-size: 1.1rem;
  font-weight: 600;
  color: #0B2942;
  margin-bottom: 0;
}

.course-info .course-code {
  color: #6c757d;
  margin: 0.1rem 0 0.5rem 0;
  font-size: 0.9rem;
}

.course-info .course-meta {
  display: flex;
  justify-content: center;
  gap: 0.5rem;
}

.relationships-container {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin: 0.75rem 0;
}

.relationship-section {
  border: 1px solid #e9ecef;
  border-radius: 6px;
  overflow: hidden;
}

.relationship-title {
  margin: 0;
  padding: 0.5rem 0.75rem;
  background-color: #f8f9fa;
  color: #0B2942;
  font-size: 0.9rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  border-bottom: 1px solid #e9ecef;
}

.relationship-list.compact {
  max-height: 120px;
  overflow-y: auto;
  padding: 0.25rem;
}

.relationship-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.35rem 0.6rem;
  border-bottom: 1px solid #f1f1f1;
  margin-bottom: 0.25rem;
  border-radius: 4px;
  background-color: #f9f9f9;
}

.relationship-item:last-child {
  margin-bottom: 0;
}

.relationship-item:hover {
  background-color: #f3f8ff;
}

.course-relation-info {
  flex: 1;
  min-width: 0;
}

.course-relation-info .course-code {
  font-size: 0.75rem;
  font-weight: 600;
  color: #0B2942;
}

.course-relation-info .course-name {
  font-size: 0.85rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 300px;
  font-weight: 500;
}

.btn-remove-sm {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 22px;
  height: 22px;
  border-radius: 50%;
  border: none;
  background-color: #f1f1f1;
  color: #dc3545;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 0.8rem;
  padding: 0;
  margin-left: 0.5rem;
}

.btn-remove-sm:hover {
  background-color: #dc3545;
  color: white;
}

.empty-relationship {
  padding: 0.6rem;
  text-align: center;
  color: #6c757d;
  font-style: italic;
  font-size: 0.85rem;
}

.btn-edit-relationships {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0.6rem 1rem;
  background-color: #0B2942;
  color: #fff;
  font-weight: 500;
  font-size: 0.9rem;
  border-radius: 6px;
  text-decoration: none;
  transition: all 0.3s ease;
  width: 100%;
  margin-top: 0.5rem;
}

.btn-edit-relationships:hover {
  background-color: #4da0ff;
  color: #fff;
}

/* Course options in add modal */
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

.modal-content.modal-lg {
  max-width: 700px;
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

.text-danger {
  color: #dc3545;
}

@media (max-width: 768px) {
  .form-actions {
    flex-direction: column;
  }
  
  .btn-save, .btn-cancel {
    width: 100%;
  }
  
  .course-options {
    flex-direction: column;
    gap: 0.75rem;
  }
  
  .course-relation-info .course-name {
    max-width: 200px;
  }
}
</style>
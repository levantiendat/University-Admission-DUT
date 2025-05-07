<template>
    <div class="modal fade" id="majorQuickViewModal" tabindex="-1" aria-labelledby="majorModalLabel" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered modal-lg">
        <div class="modal-content">
          <div class="modal-header bg-primary text-white">
            <h5 class="modal-title" id="majorModalLabel">
              <i class="bi bi-mortarboard-fill me-2"></i>
              {{ major ? major.name : 'Thông tin ngành' }}
            </h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body p-0">
            <div v-if="loading" class="text-center p-5">
              <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Đang tải...</span>
              </div>
              <p class="mt-3">Đang tải thông tin chi tiết ngành...</p>
            </div>
            
            <div v-else-if="major" class="p-4">
              <div class="row mb-4">
                <div class="col-md-8">
                  <h4 class="major-name mb-2">{{ major.name }}</h4>
                  <p class="mb-2">
                    <span class="badge bg-secondary me-2">Mã ngành: {{ major.major_code }}</span>
                    <span class="badge bg-info">Khoa: {{ major.faculty_name }}</span>
                  </p>
                  <div class="major-description mt-3">
                    <h6 class="text-primary mb-2">Mô tả ngành:</h6>
                    <p>{{ major.description || 'Chưa có mô tả cho ngành này.' }}</p>
                  </div>
                </div>
                <div class="col-md-4">
                  <div class="detail-card quota mb-3">
                    <div class="detail-card-title">
                      <i class="bi bi-people-fill me-2"></i> Chỉ tiêu 2025
                    </div>
                    <div class="detail-card-value">{{ major.seats }}</div>
                  </div>
                  <div class="detail-card methods">
                    <div class="detail-card-title">
                      <i class="bi bi-check2-square me-2"></i> Phương thức xét tuyển
                    </div>
                    <div class="detail-card-value">{{ admissionMethods.length }}</div>
                  </div>
                </div>
              </div>
              
              <div class="text-center mt-4">
                <router-link :to="{ name: 'MajorDetail', params: { id: major.id }}" class="btn btn-primary btn-lg">
                  <i class="bi bi-info-circle-fill me-2"></i> Xem thông tin chi tiết ngành
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, watch } from 'vue'
  import DetailMajorController from '@/controllers/DetailMajorController'
  
  export default {
    name: 'MajorQuickView',
    props: {
      majorId: {
        type: [Number, String],
        default: null
      },
      show: {
        type: Boolean,
        default: false
      }
    },
    
    setup(props) {
      const major = ref(null)
      const admissionMethods = ref([])
      const loading = ref(false)
      const error = ref(null)
      
      const loadMajorDetail = async (id) => {
        if (!id) return
        
        try {
          loading.value = true
          error.value = null
          
          // Lấy thông tin chi tiết về ngành
          major.value = await DetailMajorController.getMajorDetail(id)
          
          // Lấy các phương thức xét tuyển
          admissionMethods.value = await DetailMajorController.getMajorAdmissionMethods(id)
          
        } catch (err) {
          console.error('Lỗi khi tải thông tin chi tiết ngành:', err)
          error.value = 'Đã xảy ra lỗi khi tải thông tin chi tiết ngành.'
        } finally {
          loading.value = false
        }
      }
      
      // Watch for changes in props.majorId
      watch(() => props.majorId, (newId) => {
        if (newId) {
          loadMajorDetail(newId)
        }
      })
      
      // Watch for changes in props.show
      watch(() => props.show, (newValue) => {
        if (newValue && props.majorId) {
          const modalElement = document.getElementById('majorQuickViewModal')
          if (modalElement) {
            const modal = new bootstrap.Modal(modalElement)
            modal.show()
          }
        }
      })
      
      return {
        major,
        admissionMethods,
        loading,
        error
      }
    }
  }
  </script>
  
  <style scoped>
  .major-name {
    color: #0d47a1;
    font-weight: 700;
  }
  
  .detail-card {
    background-color: #f8f9fa;
    border-radius: 8px;
    padding: 1.25rem;
    text-align: center;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  }
  
  .detail-card-title {
    color: #495057;
    font-size: 1rem;
    margin-bottom: 0.5rem;
  }
  
  .detail-card-value {
    font-size: 2rem;
    font-weight: 700;
    color: #0d47a1;
  }
  
  .detail-card.quota .detail-card-value {
    color: #28a745;
  }
  
  .major-description {
    color: #495057;
  }
  
  @media (max-width: 768px) {
    .detail-card {
      padding: 1rem;
    }
    
    .detail-card-value {
      font-size: 1.5rem;
    }
    
    .major-name {
      font-size: 1.3rem;
    }
  }
  </style>
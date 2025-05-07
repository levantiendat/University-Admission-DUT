import DetailMajorService from '@/models/DetailMajorServices'

const DetailMajorController = {
  /**
   * Lấy danh sách tất cả các khoa
   * @returns {Promise<Array>} - Danh sách khoa
   */
  async getFaculties() {
    try {
      return await DetailMajorService.getFaculties()
    } catch (error) {
      throw error
    }
  },
  
  /**
   * Lấy danh sách tất cả các ngành
   * @returns {Promise<Array>} - Danh sách ngành
   */
  async getMajors() {
    try {
      const majors = await DetailMajorService.getMajors()
      const faculties = await this.getFaculties()
      
      // Thêm thông tin khoa vào mỗi ngành
      return majors.map(major => {
        const faculty = faculties.find(f => f.id === major.faculty_id)
        return {
          ...major,
          faculty_name: faculty ? faculty.name : 'Chưa xác định',
          faculty_code: faculty ? faculty.faculty_code : ''
        }
      })
    } catch (error) {
      throw error
    }
  },
  
  /**
   * Lấy thông tin chi tiết ngành kèm thông tin khoa
   * @param {number} majorId - ID của ngành
   * @returns {Promise<Object>} - Thông tin chi tiết ngành
   */
  async getMajorDetail(majorId) {
    try {
      const major = await DetailMajorService.getMajorById(majorId)
      const faculties = await this.getFaculties()
      const faculty = faculties.find(f => f.id === major.faculty_id)
      
      return {
        ...major,
        faculty_name: faculty ? faculty.name : 'Chưa xác định',
        faculty_code: faculty ? faculty.faculty_code : ''
      }
    } catch (error) {
      throw error
    }
  },
  
  /**
   * Lấy tất cả các phương thức xét tuyển áp dụng cho một ngành
   * @param {number} majorId - ID của ngành
   * @returns {Promise<Array>} - Danh sách phương thức xét tuyển với thông tin chi tiết
   */
  async getMajorAdmissionMethods(majorId) {
    try {
      const majorAdmissionMethods = await DetailMajorService.getMajorAdmissionMethods(majorId)
      const allAdmissionMethods = await DetailMajorService.getAdmissionMethods()
      
      // Kết hợp dữ liệu để lấy thông tin đầy đủ về các phương thức xét tuyển áp dụng
      return majorAdmissionMethods.map(method => {
        const fullInfo = allAdmissionMethods.find(m => m.id === method.admission_methods_id)
        return {
          ...method,
          name: fullInfo ? fullInfo.name : '',
          description: fullInfo ? fullInfo.description : '',
          min_score: fullInfo ? fullInfo.min_score : 0,
          max_score: fullInfo ? fullInfo.max_score : 0
        }
      })
    } catch (error) {
      throw error
    }
  },
  
  /**
   * Lấy tổ hợp thi áp dụng cho một ngành theo phương thức xét tuyển
   * @param {number} majorId - ID của ngành
   * @param {number} admissionMethodId - ID của phương thức xét tuyển
   * @returns {Promise<Array>} - Danh sách tổ hợp thi với thông tin chi tiết
   */
  async getMajorSubjectGroups(majorId, admissionMethodId) {
    try {
      const majorSubjectGroups = await DetailMajorService.getMajorSubjectGroups(majorId, admissionMethodId)
      const allSubjectGroups = await DetailMajorService.getSubjectGroups()
      
      // Kết hợp dữ liệu để lấy thông tin đầy đủ về các tổ hợp thi
      return majorSubjectGroups.map(group => {
        const fullInfo = allSubjectGroups.find(g => g.id === group.group_id)
        return {
          ...group,
          name: fullInfo ? fullInfo.name : 'Không xác định'
        }
      })
    } catch (error) {
      throw error
    }
  },
  
  /**
   * Lấy thành tích áp dụng cho xét tuyển thẳng và xét tuyển riêng
   * @param {number} majorId - ID của ngành
   * @returns {Promise<Object>} - Danh sách thành tích phân loại theo môn học và lĩnh vực KHKT
   */
  async getMajorAdmissionDescriptions(majorId) {
    try {
      const descriptions = await DetailMajorService.getMajorAdmissionDescriptions(majorId)
      
      // Phân loại thành môn học và lĩnh vực KHKT như trong XTRView
      const exactSubjects = ['Toán', 'Vật Lý', 'Hóa Học', 'Sinh Học', 'Tin Học', 'Ngữ Văn', 'Tiếng Anh']
      
      // Phân loại thành môn học và lĩnh vực
      const subjects = descriptions.filter(desc => 
        exactSubjects.includes(desc.field_or_subject_name)
      )
      
      const fields = descriptions.filter(desc => 
        !exactSubjects.includes(desc.field_or_subject_name)
      )
      
      return {
        subjects,
        fields
      }
    } catch (error) {
      throw error
    }
  },
  
  /**
   * Lấy điểm chuẩn các năm trước của một ngành
   * @param {number} majorId - ID của ngành
   * @returns {Promise<Object>} - Điểm chuẩn theo năm và phương thức xét tuyển
   */
  async getPreviousAdmissionScores(majorId) {
    try {
      const scores = await DetailMajorService.getPreviousAdmissionScores(majorId)
      const allAdmissionMethods = await DetailMajorService.getAdmissionMethods()
      
      // Thêm thông tin phương thức xét tuyển vào mỗi điểm chuẩn
      const enhancedScores = scores.map(score => {
        const method = allAdmissionMethods.find(m => m.id === score.admission_methods_id)
        return {
          ...score,
          method_name: method ? method.name : 'Không xác định'
        }
      })
      
      // Nhóm điểm chuẩn theo năm
      const groupedByYear = {}
      enhancedScores.forEach(score => {
        if (!groupedByYear[score.year]) {
          groupedByYear[score.year] = []
        }
        groupedByYear[score.year].push(score)
      })
      
      return groupedByYear
    } catch (error) {
      throw error
    }
  },
  
  /**
   * Lấy toàn bộ dữ liệu chi tiết của một ngành cho trang chi tiết
   * @param {number} majorId - ID của ngành
   * @returns {Promise<Object>} - Tất cả thông tin chi tiết của ngành
   */
  async getCompleteMajorDetail(majorId) {
    try {
      const majorDetail = await this.getMajorDetail(majorId)
      const admissionMethods = await this.getMajorAdmissionMethods(majorId)
      const previousScores = await this.getPreviousAdmissionScores(majorId)
      const admissionDescriptions = await this.getMajorAdmissionDescriptions(majorId)
      
      // Lấy tổ hợp thi cho các phương thức xét tuyển theo điểm thi THPT và xét học bạ
      const subjectGroupsPromises = admissionMethods
        .filter(method => [3, 6].includes(method.admission_methods_id))
        .map(method => this.getMajorSubjectGroups(majorId, method.admission_methods_id)
          .then(groups => ({
            admission_method_id: method.admission_methods_id,
            method_name: method.name,
            groups
          }))
        )
      
      const subjectGroups = await Promise.all(subjectGroupsPromises)
      
      return {
        major: majorDetail,
        admissionMethods,
        previousScores,
        admissionDescriptions,
        subjectGroups
      }
    } catch (error) {
      throw error
    }
  }
}

export default DetailMajorController
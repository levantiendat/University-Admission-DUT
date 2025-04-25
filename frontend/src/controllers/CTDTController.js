import CTDTService from '@/models/CTDTService'

export default {
  /**
   * Lấy thông tin khoa theo ID
   * @param {number} facultyId - ID của khoa
   * @returns {Promise} - Promise trả về thông tin khoa
   */
  async getFacultyById(facultyId) {
    try {
      const response = await CTDTService.getFacultyById(facultyId)
      return response.data
    } catch (error) {
      console.error('Lỗi khi lấy thông tin khoa:', error)
      throw error
    }
  },

  /**
   * Lấy danh sách ngành theo khoa
   * @param {number} facultyId - ID của khoa
   * @returns {Promise} - Promise trả về danh sách ngành
   */
  async getMajorsByFaculty(facultyId) {
    try {
      const response = await CTDTService.getMajorsByFaculty(facultyId)
      return response.data
    } catch (error) {
      console.error('Lỗi khi lấy danh sách ngành:', error)
      throw error
    }
  },

  /**
   * Lấy danh sách chương trình đào tạo theo ngành
   * @param {number} majorId - ID của ngành
   * @returns {Promise} - Promise trả về danh sách chương trình đào tạo
   */
  async getMajorCoursesByMajorId(majorId) {
    try {
      const response = await CTDTService.getMajorCoursesByMajorId(majorId)
      return response.data
    } catch (error) {
      console.error('Lỗi khi lấy danh sách chương trình đào tạo:', error)
      throw error
    }
  },

  /**
   * Lấy và xử lý chi tiết chương trình đào tạo
   * @param {number} majorCourseId - ID của chương trình đào tạo
   * @returns {Promise} - Promise trả về chi tiết chương trình đào tạo đã được xử lý
   */
  async getMajorCourseDetailsByMajorCourseId(majorCourseId) {
    try {
      const response = await CTDTService.getMajorCourseDetailsByMajorCourseId(majorCourseId)
      const data = response.data
      
      // Tạo map từ course_id sang thông tin khóa học
      const courseMap = {}
      data.courses.forEach(course => {
        courseMap[course.id] = course
      })
      
      // Tạo map từ major_course_detail.id sang thông tin chi tiết
      const detailMap = {}
      data.major_course_details.forEach(detail => {
        detailMap[detail.id] = detail
      })
      
      // Gắn thông tin khóa học vào major_course_details
      const enrichedDetails = data.major_course_details.map(detail => {
        const course = courseMap[detail.course_id]
        
        // Xử lý học phần cần học trước
        const priorCourses = detail.prior_courses.map(id => {
          const priorDetail = detailMap[id]
          if (priorDetail && courseMap[priorDetail.course_id]) {
            const priorCourse = courseMap[priorDetail.course_id]
            return {
              code: priorCourse.course_code,
              name: priorCourse.name
            }
          }
          return null
        }).filter(Boolean)
        
        // Xử lý học phần tiên quyết
        const prerequisites = detail.prerequisites.map(id => {
          const prereqDetail = detailMap[id]
          if (prereqDetail && courseMap[prereqDetail.course_id]) {
            const prereqCourse = courseMap[prereqDetail.course_id]
            return {
              code: prereqCourse.course_code,
              name: prereqCourse.name
            }
          }
          return null
        }).filter(Boolean)
        
        // Xử lý học phần song hành
        const corequisites = detail.corequisites.map(id => {
          const coreqDetail = detailMap[id]
          if (coreqDetail && courseMap[coreqDetail.course_id]) {
            const coreqCourse = courseMap[coreqDetail.course_id]
            return {
              code: coreqCourse.course_code,
              name: coreqCourse.name
            }
          }
          return null
        }).filter(Boolean)
        
        return {
          ...detail,
          course: course,
          priorCourses,
          prerequisites,
          corequisites
        }
      })
      
      // Sắp xếp theo học kỳ
      enrichedDetails.sort((a, b) => {
        return a.semester - b.semester
      })
      
      return enrichedDetails
    } catch (error) {
      console.error('Lỗi khi lấy chi tiết chương trình đào tạo:', error)
      throw error
    }
  }
}
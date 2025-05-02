import MajorCourseDetailServices from '../../models/admins/MajorCourseDetailServices';

export default {
  /**
   * Lấy tất cả chi tiết khung chương trình đào tạo
   */
  async getAllMajorCourseDetails() {
    try {
      return await MajorCourseDetailServices.getAllMajorCourseDetails();
    } catch (error) {
      throw new Error(`Không thể lấy danh sách chi tiết khung chương trình: ${error.message}`);
    }
  },

  /**
   * Lấy chi tiết khung chương trình đào tạo theo ID khung chương trình
   * @param {number} majorCourseId - ID của khung chương trình đào tạo
   */
  async getMajorCourseDetailsByMajorCourseId(majorCourseId) {
    try {
      return await MajorCourseDetailServices.getMajorCourseDetailsByMajorCourseId(majorCourseId);
    } catch (error) {
      throw new Error(`Không thể lấy chi tiết khung chương trình: ${error.message}`);
    }
  },

  /**
   * Lấy chi tiết một học phần trong khung chương trình đào tạo
   * @param {number} id - ID của chi tiết học phần
   */
  async getMajorCourseDetailById(id) {
    try {
      return await MajorCourseDetailServices.getMajorCourseDetail(id);
    } catch (error) {
      throw new Error(`Không thể lấy chi tiết học phần: ${error.message}`);
    }
  },

  /**
   * Tạo chi tiết học phần mới trong khung chương trình đào tạo
   * @param {Object} data - Dữ liệu chi tiết học phần
   */
  async createMajorCourseDetail(data) {
    try {
      // Validate input
      if (!data.major_course_id) {
        throw new Error('Vui lòng chọn khung chương trình');
      }

      if (!data.course_id) {
        throw new Error('Vui lòng chọn học phần');
      }

      if (data.semester === undefined || data.semester === null || isNaN(parseInt(data.semester)) || parseInt(data.semester) < 1) {
        throw new Error('Học kỳ không hợp lệ (phải >=1)');
      }

      if (data.elective_course === undefined) {
        data.elective_course = false;
      }

      if (data.pre_capstone === undefined) {
        data.pre_capstone = false;
      }

      if (data.mandatory_capstone === undefined) {
        data.mandatory_capstone = false;
      }

      // Format data
      const formattedData = {
        major_course_id: parseInt(data.major_course_id),
        course_id: parseInt(data.course_id),
        semester: parseInt(data.semester),
        elective_course: Boolean(data.elective_course),
        pre_capstone: Boolean(data.pre_capstone),
        mandatory_capstone: Boolean(data.mandatory_capstone)
      };

      return await MajorCourseDetailServices.createMajorCourseDetail(formattedData);
    } catch (error) {
      throw new Error(`Không thể tạo chi tiết học phần mới: ${error.message}`);
    }
  },

  /**
   * Cập nhật chi tiết học phần trong khung chương trình đào tạo
   * @param {number} id - ID của chi tiết học phần
   * @param {Object} data - Dữ liệu cập nhật
   */
  async updateMajorCourseDetail(id, data) {
    try {
      // Validate input
      if (data.semester !== undefined) {
        if (isNaN(parseInt(data.semester)) || parseInt(data.semester) < 1) {
          throw new Error('Học kỳ không hợp lệ (phải >=1)');
        }
      }

      // Format data
      const formattedData = { ...data };
      if (formattedData.major_course_id !== undefined) formattedData.major_course_id = parseInt(formattedData.major_course_id);
      if (formattedData.course_id !== undefined) formattedData.course_id = parseInt(formattedData.course_id);
      if (formattedData.semester !== undefined) formattedData.semester = parseInt(formattedData.semester);
      if (formattedData.elective_course !== undefined) formattedData.elective_course = Boolean(formattedData.elective_course);
      if (formattedData.pre_capstone !== undefined) formattedData.pre_capstone = Boolean(formattedData.pre_capstone);
      if (formattedData.mandatory_capstone !== undefined) formattedData.mandatory_capstone = Boolean(formattedData.mandatory_capstone);

      return await MajorCourseDetailServices.updateMajorCourseDetail(id, formattedData);
    } catch (error) {
      throw new Error(`Không thể cập nhật chi tiết học phần: ${error.message}`);
    }
  },

  /**
   * Xóa chi tiết học phần trong khung chương trình đào tạo
   * @param {number} id - ID của chi tiết học phần
   */
  async deleteMajorCourseDetail(id) {
    try {
      return await MajorCourseDetailServices.deleteMajorCourseDetail(id);
    } catch (error) {
      throw new Error(`Không thể xóa chi tiết học phần: ${error.message}`);
    }
  },

  /**
   * Tạo mới mối quan hệ học trước
   * @param {number} majorCourseDetailId - ID chi tiết học phần
   * @param {number} priorCourseDetailId - ID chi tiết học phần học trước
   */
  async createCoursePriorCourse(majorCourseDetailId, priorCourseDetailId) {
    try {
      const data = {
        major_course_detail_id: parseInt(majorCourseDetailId),
        prior_course_detail_id: parseInt(priorCourseDetailId)
      };

      return await MajorCourseDetailServices.createCoursePriorCourse(data);
    } catch (error) {
      throw new Error(`Không thể tạo mối quan hệ học trước: ${error.message}`);
    }
  },

  /**
   * Xóa mối quan hệ học trước
   * @param {number} id - ID của mối quan hệ học trước
   */
  async deleteCoursePriorCourse(id) {
    try {
      return await MajorCourseDetailServices.deleteCoursePriorCourse(id);
    } catch (error) {
      throw new Error(`Không thể xóa mối quan hệ học trước: ${error.message}`);
    }
  },

  /**
   * Tạo mới mối quan hệ học tiên quyết
   * @param {number} majorCourseDetailId - ID chi tiết học phần
   * @param {number} prerequisiteMajorCourseDetailId - ID chi tiết học phần tiên quyết
   */
  async createCoursePrerequisite(majorCourseDetailId, prerequisiteMajorCourseDetailId) {
    try {
      const data = {
        major_course_detail_id: parseInt(majorCourseDetailId),
        prerequisite_major_course_detail_id: parseInt(prerequisiteMajorCourseDetailId)
      };

      return await MajorCourseDetailServices.createCoursePrerequisite(data);
    } catch (error) {
      throw new Error(`Không thể tạo mối quan hệ học tiên quyết: ${error.message}`);
    }
  },

  /**
   * Xóa mối quan hệ học tiên quyết
   * @param {number} id - ID của mối quan hệ học tiên quyết
   */
  async deleteCoursePrerequisite(id) {
    try {
      return await MajorCourseDetailServices.deleteCoursePrerequisite(id);
    } catch (error) {
      throw new Error(`Không thể xóa mối quan hệ học tiên quyết: ${error.message}`);
    }
  },

  /**
   * Tạo mới mối quan hệ học song hành
   * @param {number} majorCourseDetailId - ID chi tiết học phần
   * @param {number} corequisiteMajorCourseDetailId - ID chi tiết học phần song hành
   */
  async createCourseCorequisite(majorCourseDetailId, corequisiteMajorCourseDetailId) {
    try {
      const data = {
        major_course_detail_id: parseInt(majorCourseDetailId),
        corequisite_major_course_detail_id: parseInt(corequisiteMajorCourseDetailId)
      };

      return await MajorCourseDetailServices.createCourseCorequisite(data);
    } catch (error) {
      throw new Error(`Không thể tạo mối quan hệ học song hành: ${error.message}`);
    }
  },

  /**
   * Xóa mối quan hệ học song hành
   * @param {number} id - ID của mối quan hệ học song hành
   */
  async deleteCourseCorequisite(id) {
    try {
      return await MajorCourseDetailServices.deleteCourseCorequisite(id);
    } catch (error) {
      throw new Error(`Không thể xóa mối quan hệ học song hành: ${error.message}`);
    }
  }
};
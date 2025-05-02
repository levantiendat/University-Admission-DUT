import MajorCourseServices from '../../models/admins/MajorCourseServices';

export default {
  /**
   * Lấy danh sách khung chương trình đào tạo
   */
  async getAllMajorCourses() {
    try {
      return await MajorCourseServices.getAllMajorCourses();
    } catch (error) {
      throw new Error(`Không thể lấy danh sách khung chương trình đào tạo: ${error.message}`);
    }
  },

  /**
   * Lấy thông tin chi tiết của một khung chương trình đào tạo
   * @param {number} id - ID của khung chương trình
   */
  async getMajorCourseById(id) {
    try {
      return await MajorCourseServices.getMajorCourse(id);
    } catch (error) {
      throw new Error(`Không thể lấy thông tin khung chương trình đào tạo: ${error.message}`);
    }
  },

  /**
   * Tạo khung chương trình đào tạo mới
   * @param {Object} data - Dữ liệu khung chương trình mới
   */
  async createMajorCourse(data) {
    try {
      // Validate input
      if (!data.major_id) {
        throw new Error('Vui lòng chọn ngành học');
      }

      if (!data.year || isNaN(parseInt(data.year))) {
        throw new Error('Vui lòng nhập năm hợp lệ');
      }

      if (!data.type) {
        throw new Error('Vui lòng chọn loại chương trình đào tạo');
      }

      // Validate type
      const validTypes = ['Cử nhân', 'Kỹ sư', 'Kiến trúc sư'];
      if (!validTypes.includes(data.type)) {
        throw new Error('Loại chương trình đào tạo không hợp lệ');
      }

      // Format data
      const formattedData = {
        major_id: parseInt(data.major_id),
        year: parseInt(data.year),
        type: data.type
      };

      return await MajorCourseServices.createMajorCourse(formattedData);
    } catch (error) {
      throw new Error(`Không thể tạo khung chương trình đào tạo mới: ${error.message}`);
    }
  },

  /**
   * Cập nhật thông tin khung chương trình đào tạo
   * @param {number} id - ID của khung chương trình
   * @param {Object} data - Dữ liệu cập nhật
   */
  async updateMajorCourse(id, data) {
    try {
      // Validate data
      if (data.major_id && isNaN(parseInt(data.major_id))) {
        throw new Error('ID ngành học không hợp lệ');
      }

      if (data.year && isNaN(parseInt(data.year))) {
        throw new Error('Năm không hợp lệ');
      }

      if (data.type) {
        // Validate type
        const validTypes = ['Cử nhân', 'Kỹ sư', 'Kiến trúc sư'];
        if (!validTypes.includes(data.type)) {
          throw new Error('Loại chương trình đào tạo không hợp lệ');
        }
      }

      // Format data
      const formattedData = { ...data };
      if (formattedData.major_id) formattedData.major_id = parseInt(formattedData.major_id);
      if (formattedData.year) formattedData.year = parseInt(formattedData.year);

      return await MajorCourseServices.updateMajorCourse(id, formattedData);
    } catch (error) {
      throw new Error(`Không thể cập nhật khung chương trình đào tạo: ${error.message}`);
    }
  },

  /**
   * Xóa khung chương trình đào tạo
   * @param {number} id - ID của khung chương trình
   */
  async deleteMajorCourse(id) {
    try {
      return await MajorCourseServices.deleteMajorCourse(id);
    } catch (error) {
      throw new Error(`Không thể xóa khung chương trình đào tạo: ${error.message}`);
    }
  },
  /**
   * Lấy chi tiết khung chương trình đào tạo theo ID
   * @param {number} majorCourseId - ID của khung chương trình
   */
  async getMajorCourseDetailsById(majorCourseId) {
    try {
      return await MajorCourseServices.getMajorCourseDetailsById(majorCourseId);
    } catch (error) {
      throw new Error(`Không thể lấy chi tiết khung chương trình: ${error.message}`);
    }
  },

  /**
   * Lấy chi tiết của một học phần trong khung chương trình
   * @param {number} id - ID của major course detail
   */
  async getMajorCourseDetail(id) {
    try {
      return await MajorCourseServices.getMajorCourseDetail(id);
    } catch (error) {
      throw new Error(`Không thể lấy thông tin chi tiết học phần: ${error.message}`);
    }
  },

  /**
   * Thêm học phần vào khung chương trình
   * @param {Object} data - Dữ liệu thêm học phần
   */
  async createMajorCourseDetail(data) {
    try {
      // Validate
      if (!data.major_course_id) {
        throw new Error('Cần chỉ định khung chương trình');
      }

      if (!data.course_id) {
        throw new Error('Cần chỉ định học phần');
      }

      if (data.semester === undefined || data.semester === null || isNaN(parseInt(data.semester)) || parseInt(data.semester) < 1) {
        throw new Error('Học kỳ không hợp lệ');
      }

      // Format data
      const formattedData = {
        major_course_id: parseInt(data.major_course_id),
        course_id: parseInt(data.course_id),
        semester: parseInt(data.semester),
        elective_course: !!data.elective_course,
        pre_capstone: !!data.pre_capstone,
        mandatory_capstone: !!data.mandatory_capstone
      };

      return await MajorCourseServices.createMajorCourseDetail(formattedData);
    } catch (error) {
      throw new Error(`Không thể thêm học phần vào khung chương trình: ${error.message}`);
    }
  },

  /**
   * Cập nhật thông tin học phần trong khung chương trình
   * @param {number} id - ID của chi tiết học phần
   * @param {Object} data - Dữ liệu cập nhật
   */
  async updateMajorCourseDetail(id, data) {
    try {
      // Validate
      if (data.semester !== undefined && (isNaN(parseInt(data.semester)) || parseInt(data.semester) < 1)) {
        throw new Error('Học kỳ không hợp lệ');
      }

      // Format data
      const formattedData = { ...data };
      if (formattedData.major_course_id !== undefined) {
        formattedData.major_course_id = parseInt(formattedData.major_course_id);
      }
      if (formattedData.course_id !== undefined) {
        formattedData.course_id = parseInt(formattedData.course_id);
      }
      if (formattedData.semester !== undefined) {
        formattedData.semester = parseInt(formattedData.semester);
      }
      if (formattedData.elective_course !== undefined) {
        formattedData.elective_course = !!formattedData.elective_course;
      }
      if (formattedData.pre_capstone !== undefined) {
        formattedData.pre_capstone = !!formattedData.pre_capstone;
      }
      if (formattedData.mandatory_capstone !== undefined) {
        formattedData.mandatory_capstone = !!formattedData.mandatory_capstone;
      }

      return await MajorCourseServices.updateMajorCourseDetail(id, formattedData);
    } catch (error) {
      throw new Error(`Không thể cập nhật thông tin học phần trong khung chương trình: ${error.message}`);
    }
  },

  /**
   * Xóa học phần khỏi khung chương trình
   * @param {number} id - ID của chi tiết học phần
   */
  async deleteMajorCourseDetail(id) {
    try {
      return await MajorCourseServices.deleteMajorCourseDetail(id);
    } catch (error) {
      throw new Error(`Không thể xóa học phần khỏi khung chương trình: ${error.message}`);
    }
  },

  /**
   * Thêm mối quan hệ học trước
   * @param {number} majorCourseDetailId - ID của học phần chính
   * @param {number} priorCourseDetailId - ID của học phần học trước
   */
  async addPriorCourse(majorCourseDetailId, priorCourseDetailId) {
    try {
      // Validate
      if (!majorCourseDetailId) {
        throw new Error('Cần chỉ định học phần chính');
      }

      if (!priorCourseDetailId) {
        throw new Error('Cần chỉ định học phần học trước');
      }

      if (parseInt(majorCourseDetailId) === parseInt(priorCourseDetailId)) {
        throw new Error('Một học phần không thể là học phần học trước của chính nó');
      }

      const data = {
        major_course_detail_id: parseInt(majorCourseDetailId),
        prior_course_detail_id: parseInt(priorCourseDetailId)
      };

      return await MajorCourseServices.createPriorCourse(data);
    } catch (error) {
      throw new Error(`Không thể thêm mối quan hệ học trước: ${error.message}`);
    }
  },

  /**
   * Xóa mối quan hệ học trước
   * @param {number} id - ID của mối quan hệ học trước
   */
  async removePriorCourse(id) {
    try {
      return await MajorCourseServices.deletePriorCourse(id);
    } catch (error) {
      throw new Error(`Không thể xóa mối quan hệ học trước: ${error.message}`);
    }
  },

  /**
   * Thêm mối quan hệ tiên quyết
   * @param {number} majorCourseDetailId - ID của học phần chính
   * @param {number} prerequisiteMajorCourseDetailId - ID của học phần tiên quyết
   */
  async addPrerequisite(majorCourseDetailId, prerequisiteMajorCourseDetailId) {
    try {
      // Validate
      if (!majorCourseDetailId) {
        throw new Error('Cần chỉ định học phần chính');
      }

      if (!prerequisiteMajorCourseDetailId) {
        throw new Error('Cần chỉ định học phần tiên quyết');
      }

      if (parseInt(majorCourseDetailId) === parseInt(prerequisiteMajorCourseDetailId)) {
        throw new Error('Một học phần không thể là học phần tiên quyết của chính nó');
      }

      const data = {
        major_course_detail_id: parseInt(majorCourseDetailId),
        prerequisite_major_course_detail_id: parseInt(prerequisiteMajorCourseDetailId)
      };

      return await MajorCourseServices.createPrerequisite(data);
    } catch (error) {
      throw new Error(`Không thể thêm mối quan hệ tiên quyết: ${error.message}`);
    }
  },

  /**
   * Xóa mối quan hệ tiên quyết
   * @param {number} id - ID của mối quan hệ tiên quyết
   */
  async removePrerequisite(id) {
    try {
      return await MajorCourseServices.deletePrerequisite(id);
    } catch (error) {
      throw new Error(`Không thể xóa mối quan hệ tiên quyết: ${error.message}`);
    }
  },

  /**
   * Thêm mối quan hệ song hành
   * @param {number} majorCourseDetailId - ID của học phần chính
   * @param {number} corequisiteMajorCourseDetailId - ID của học phần song hành
   */
  async addCorequisite(majorCourseDetailId, corequisiteMajorCourseDetailId) {
    try {
      // Validate
      if (!majorCourseDetailId) {
        throw new Error('Cần chỉ định học phần chính');
      }

      if (!corequisiteMajorCourseDetailId) {
        throw new Error('Cần chỉ định học phần song hành');
      }

      if (parseInt(majorCourseDetailId) === parseInt(corequisiteMajorCourseDetailId)) {
        throw new Error('Một học phần không thể là học phần song hành của chính nó');
      }

      const data = {
        major_course_detail_id: parseInt(majorCourseDetailId),
        corequisite_major_course_detail_id: parseInt(corequisiteMajorCourseDetailId)
      };

      return await MajorCourseServices.createCorequisite(data);
    } catch (error) {
      throw new Error(`Không thể thêm mối quan hệ song hành: ${error.message}`);
    }
  },

  /**
   * Xóa mối quan hệ song hành
   * @param {number} id - ID của mối quan hệ song hành
   */
  async removeCorequisite(id) {
    try {
      return await MajorCourseServices.deleteCorequisite(id);
    } catch (error) {
      throw new Error(`Không thể xóa mối quan hệ song hành: ${error.message}`);
    }
  },

  /**
   * Lấy tất cả mối quan hệ học trước
   */
  async getAllPriorCourses() {
    try {
      return await MajorCourseServices.getAllPriorCourses();
    } catch (error) {
      throw new Error(`Không thể lấy mối quan hệ học trước: ${error.message}`);
    }
  },

  /**
   * Lấy tất cả mối quan hệ tiên quyết
   */
  async getAllPrerequisites() {
    try {
      return await MajorCourseServices.getAllPrerequisites();
    } catch (error) {
      throw new Error(`Không thể lấy mối quan hệ tiên quyết: ${error.message}`);
    }
  },

  /**
   * Lấy tất cả mối quan hệ song hành
   */
  async getAllCorequisites() {
    try {
      return await MajorCourseServices.getAllCorequisites();
    } catch (error) {
      throw new Error(`Không thể lấy mối quan hệ song hành: ${error.message}`);
    }
  }
};
import CourseServices from '../../models/admins/CourseServices';

export default {
  /**
   * Lấy danh sách lớp học phần
   */
  async getAllCourses() {
    try {
      return await CourseServices.getAllCourses();
    } catch (error) {
      throw new Error(`Không thể lấy danh sách lớp học phần: ${error.message}`);
    }
  },

  /**
   * Lấy thông tin chi tiết của một lớp học phần
   * @param {number} id - ID của lớp học phần
   */
  async getCourseById(id) {
    try {
      return await CourseServices.getCourse(id);
    } catch (error) {
      throw new Error(`Không thể lấy thông tin lớp học phần: ${error.message}`);
    }
  },

  /**
   * Tạo lớp học phần mới
   * @param {Object} data - Dữ liệu lớp học phần mới
   */
  async createCourse(data) {
    try {
      // Validate input
      if (!data.course_code || data.course_code.trim() === '') {
        throw new Error('Vui lòng nhập mã học phần');
      }

      if (!data.name || data.name.trim() === '') {
        throw new Error('Vui lòng nhập tên học phần');
      }

      if (data.credits === undefined || data.credits === null || isNaN(parseFloat(data.credits))) {
        throw new Error('Vui lòng nhập số tín chỉ hợp lệ');
      }

      if (parseFloat(data.credits) <= 0) {
        throw new Error('Số tín chỉ phải lớn hơn 0');
      }

      // Format data
      const formattedData = {
        course_code: data.course_code.trim(),
        name: data.name.trim(),
        credits: parseFloat(parseFloat(data.credits).toFixed(1))
      };

      return await CourseServices.createCourse(formattedData);
    } catch (error) {
      throw new Error(`Không thể tạo lớp học phần mới: ${error.message}`);
    }
  },

  /**
   * Cập nhật thông tin lớp học phần
   * @param {number} id - ID của lớp học phần
   * @param {Object} data - Dữ liệu cập nhật
   */
  async updateCourse(id, data) {
    try {
      // Validate data
      if (data.course_code !== undefined && data.course_code.trim() === '') {
        throw new Error('Mã học phần không được để trống');
      }

      if (data.name !== undefined && data.name.trim() === '') {
        throw new Error('Tên học phần không được để trống');
      }

      if (data.credits !== undefined && data.credits !== null) {
        if (isNaN(parseFloat(data.credits))) {
          throw new Error('Số tín chỉ phải là một số hợp lệ');
        }

        if (parseFloat(data.credits) <= 0) {
          throw new Error('Số tín chỉ phải lớn hơn 0');
        }
      }

      // Format data
      const formattedData = { ...data };
      if (formattedData.course_code) formattedData.course_code = formattedData.course_code.trim();
      if (formattedData.name) formattedData.name = formattedData.name.trim();
      if (formattedData.credits !== undefined && formattedData.credits !== null) {
        formattedData.credits = parseFloat(parseFloat(formattedData.credits).toFixed(1));
      }

      return await CourseServices.updateCourse(id, formattedData);
    } catch (error) {
      throw new Error(`Không thể cập nhật lớp học phần: ${error.message}`);
    }
  },

  /**
   * Xóa lớp học phần
   * @param {number} id - ID của lớp học phần
   */
  async deleteCourse(id) {
    try {
      return await CourseServices.deleteCourse(id);
    } catch (error) {
      throw new Error(`Không thể xóa lớp học phần: ${error.message}`);
    }
  }
};
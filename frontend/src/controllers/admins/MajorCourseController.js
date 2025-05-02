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
  }
};
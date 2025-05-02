import PreviousAdmissionServices from '../../models/admins/PreviousAdmissionServices';

export default {
  /**
   * Lấy danh sách điểm chuẩn các năm trước
   */
  async getAllPreviousAdmissions() {
    try {
      return await PreviousAdmissionServices.getAllPreviousAdmissions();
    } catch (error) {
      throw new Error(`Không thể lấy danh sách điểm chuẩn: ${error.message}`);
    }
  },

  /**
   * Lấy thông tin chi tiết của một điểm chuẩn năm trước
   * @param {number} id - ID của điểm chuẩn
   */
  async getPreviousAdmissionById(id) {
    try {
      return await PreviousAdmissionServices.getPreviousAdmission(id);
    } catch (error) {
      throw new Error(`Không thể lấy thông tin điểm chuẩn: ${error.message}`);
    }
  },

  /**
   * Tạo điểm chuẩn năm trước mới
   * @param {Object} data - Dữ liệu điểm chuẩn mới
   */
  async createPreviousAdmission(data) {
    try {
      // Validate input
      if (!data.major_id || !data.year || !data.admission_methods_id) {
        throw new Error('Vui lòng nhập đầy đủ thông tin bắt buộc');
      }

      if (data.score === undefined || data.score === null || isNaN(parseFloat(data.score))) {
        throw new Error('Điểm chuẩn phải là một số hợp lệ');
      }

      // Format data
      const formattedData = {
        major_id: parseInt(data.major_id),
        year: parseInt(data.year),
        admission_methods_id: parseInt(data.admission_methods_id),
        score: parseFloat(data.score)
      };

      return await PreviousAdmissionServices.createPreviousAdmission(formattedData);
    } catch (error) {
      throw new Error(`Không thể tạo điểm chuẩn mới: ${error.message}`);
    }
  },

  /**
   * Cập nhật thông tin điểm chuẩn năm trước
   * @param {number} id - ID của điểm chuẩn
   * @param {Object} data - Dữ liệu cập nhật
   */
  async updatePreviousAdmission(id, data) {
    try {
      // Validate score
      if (data.score === undefined || data.score === null || isNaN(parseFloat(data.score))) {
        throw new Error('Điểm chuẩn phải là một số hợp lệ');
      }

      // Format data
      const formattedData = { ...data };
      if (formattedData.major_id) formattedData.major_id = parseInt(formattedData.major_id);
      if (formattedData.year) formattedData.year = parseInt(formattedData.year);
      if (formattedData.admission_methods_id) formattedData.admission_methods_id = parseInt(formattedData.admission_methods_id);
      if (formattedData.score !== undefined) formattedData.score = parseFloat(formattedData.score);

      return await PreviousAdmissionServices.updatePreviousAdmission(id, formattedData);
    } catch (error) {
      throw new Error(`Không thể cập nhật điểm chuẩn: ${error.message}`);
    }
  },

  /**
   * Xóa điểm chuẩn năm trước
   * @param {number} id - ID của điểm chuẩn
   */
  async deletePreviousAdmission(id) {
    try {
      return await PreviousAdmissionServices.deletePreviousAdmission(id);
    } catch (error) {
      throw new Error(`Không thể xóa điểm chuẩn: ${error.message}`);
    }
  }
};
import AdmissionMethodMajorServices from '../../models/admins/AdmissionMethodMajorServices';

export default {
  /**
   * Lấy danh sách tất cả mối quan hệ giữa phương thức tuyển sinh và ngành
   */
  async getAllAdmissionMethodMajors() {
    try {
      return await AdmissionMethodMajorServices.getAllAdmissionMethodMajors();
    } catch (error) {
      throw new Error(`Không thể lấy danh sách mối quan hệ: ${error.message}`);
    }
  },

  /**
   * Lấy thông tin chi tiết của một mối quan hệ
   * @param {number} admissionMethodMajorId - ID của mối quan hệ
   */
  async getAdmissionMethodMajorById(admissionMethodMajorId) {
    try {
      return await AdmissionMethodMajorServices.getAdmissionMethodMajor(admissionMethodMajorId);
    } catch (error) {
      throw new Error(`Không thể lấy thông tin mối quan hệ: ${error.message}`);
    }
  },

  /**
   * Lấy danh sách phương thức tuyển sinh áp dụng cho một ngành
   * @param {number} majorId - ID của ngành
   */
  async getAdmissionMethodsByMajor(majorId) {
    try {
      return await AdmissionMethodMajorServices.getAdmissionMethodsByMajor(majorId);
    } catch (error) {
      throw new Error(`Không thể lấy danh sách phương thức tuyển sinh cho ngành: ${error.message}`);
    }
  },

  /**
   * Lấy danh sách ngành áp dụng một phương thức tuyển sinh
   * @param {number} admissionMethodId - ID của phương thức tuyển sinh
   */
  async getMajorsByAdmissionMethod(admissionMethodId) {
    try {
      return await AdmissionMethodMajorServices.getMajorsByAdmissionMethod(admissionMethodId);
    } catch (error) {
      throw new Error(`Không thể lấy danh sách ngành cho phương thức tuyển sinh: ${error.message}`);
    }
  },

  /**
   * Tạo mối quan hệ mới giữa phương thức tuyển sinh và ngành
   * @param {Object} data - Dữ liệu mối quan hệ mới
   */
  async createAdmissionMethodMajor(data) {
    try {
      // Validate input
      if (!data.major_id || !data.admission_methods_id) {
        throw new Error('Vui lòng chọn ngành và phương thức tuyển sinh');
      }

      return await AdmissionMethodMajorServices.createAdmissionMethodMajor(data);
    } catch (error) {
      throw new Error(`Không thể tạo mối quan hệ mới: ${error.message}`);
    }
  },

  /**
   * Cập nhật thông tin mối quan hệ
   * @param {number} admissionMethodMajorId - ID của mối quan hệ
   * @param {Object} data - Dữ liệu cập nhật
   */
  async updateAdmissionMethodMajor(admissionMethodMajorId, data) {
    try {
      // Validate input
      if (!data.major_id || !data.admission_methods_id) {
        throw new Error('Vui lòng chọn ngành và phương thức tuyển sinh');
      }

      return await AdmissionMethodMajorServices.updateAdmissionMethodMajor(admissionMethodMajorId, data);
    } catch (error) {
      throw new Error(`Không thể cập nhật mối quan hệ: ${error.message}`);
    }
  },

  /**
   * Xóa mối quan hệ
   * @param {number} admissionMethodMajorId - ID của mối quan hệ
   */
  async deleteAdmissionMethodMajor(admissionMethodMajorId) {
    try {
      return await AdmissionMethodMajorServices.deleteAdmissionMethodMajor(admissionMethodMajorId);
    } catch (error) {
      throw new Error(`Không thể xóa mối quan hệ: ${error.message}`);
    }
  }
};
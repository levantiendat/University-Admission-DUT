import AdmissionMethodServices from '../../models/admins/AdmissionMethodServices';

export default {
  /**
   * Lấy danh sách tất cả phương thức tuyển sinh
   */
  async getAllAdmissionMethods() {
    try {
      return await AdmissionMethodServices.getAllAdmissionMethods();
    } catch (error) {
      throw new Error(`Không thể lấy danh sách phương thức tuyển sinh: ${error.message}`);
    }
  },

  /**
   * Lấy thông tin chi tiết của một phương thức tuyển sinh
   * @param {number} admissionMethodId - ID của phương thức tuyển sinh
   */
  async getAdmissionMethodById(admissionMethodId) {
    try {
      return await AdmissionMethodServices.getAdmissionMethod(admissionMethodId);
    } catch (error) {
      throw new Error(`Không thể lấy thông tin phương thức tuyển sinh: ${error.message}`);
    }
  },

  /**
   * Tạo phương thức tuyển sinh mới
   * @param {Object} admissionMethodData - Dữ liệu phương thức tuyển sinh mới
   */
  async createAdmissionMethod(admissionMethodData) {
    try {
      // Validate input
      if (!admissionMethodData.name) {
        throw new Error('Tên phương thức tuyển sinh không được để trống');
      }

      if (admissionMethodData.min_score !== undefined && admissionMethodData.max_score !== undefined) {
        const minScore = parseFloat(admissionMethodData.min_score);
        const maxScore = parseFloat(admissionMethodData.max_score);
        
        if (isNaN(minScore) || isNaN(maxScore)) {
          throw new Error('Điểm tối thiểu và tối đa phải là số');
        }
        
        if (minScore > maxScore) {
          throw new Error('Điểm tối thiểu không thể lớn hơn điểm tối đa');
        }
      }

      return await AdmissionMethodServices.createAdmissionMethod(admissionMethodData);
    } catch (error) {
      throw new Error(`Không thể tạo phương thức tuyển sinh mới: ${error.message}`);
    }
  },

  /**
   * Cập nhật thông tin phương thức tuyển sinh
   * @param {number} admissionMethodId - ID của phương thức tuyển sinh
   * @param {Object} admissionMethodData - Dữ liệu cập nhật
   */
  async updateAdmissionMethod(admissionMethodId, admissionMethodData) {
    try {
      // Validate input
      if (admissionMethodData.name !== undefined && !admissionMethodData.name.trim()) {
        throw new Error('Tên phương thức tuyển sinh không được để trống');
      }

      if (admissionMethodData.min_score !== undefined && admissionMethodData.max_score !== undefined) {
        const minScore = parseFloat(admissionMethodData.min_score);
        const maxScore = parseFloat(admissionMethodData.max_score);
        
        if (isNaN(minScore) || isNaN(maxScore)) {
          throw new Error('Điểm tối thiểu và tối đa phải là số');
        }
        
        if (minScore > maxScore) {
          throw new Error('Điểm tối thiểu không thể lớn hơn điểm tối đa');
        }
      }

      return await AdmissionMethodServices.updateAdmissionMethod(admissionMethodId, admissionMethodData);
    } catch (error) {
      throw new Error(`Không thể cập nhật phương thức tuyển sinh: ${error.message}`);
    }
  },

  /**
   * Xóa phương thức tuyển sinh
   * @param {number} admissionMethodId - ID của phương thức tuyển sinh
   */
  async deleteAdmissionMethod(admissionMethodId) {
    try {
      return await AdmissionMethodServices.deleteAdmissionMethod(admissionMethodId);
    } catch (error) {
      throw new Error(`Không thể xóa phương thức tuyển sinh: ${error.message}`);
    }
  }
};
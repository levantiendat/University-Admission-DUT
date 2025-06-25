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

      // Xử lý đặc biệt các trường có thể null
      const processedData = {
        major_id: data.major_id,
        admission_methods_id: data.admission_methods_id,
        quota: data.quota === '' || data.quota === undefined ? null : data.quota,
        minimum_score: data.minimum_score === '' || data.minimum_score === undefined ? null : data.minimum_score,
        foundation_subject_id: data.foundation_subject_id === '' || data.foundation_subject_id === undefined ? null : data.foundation_subject_id,
        subject_minimum_score: data.subject_minimum_score === '' || data.subject_minimum_score === undefined ? null : data.subject_minimum_score
      };

      // Chỉ validate số nếu không phải null
      if (processedData.quota !== null) {
        const quota = parseInt(processedData.quota);
        if (isNaN(quota) || quota <= 0) {
          throw new Error('Chỉ tiêu phải là số nguyên dương');
        }
        processedData.quota = quota;
      }

      if (processedData.minimum_score !== null) {
        const minScore = parseFloat(processedData.minimum_score);
        if (isNaN(minScore) || minScore < 0) {
          throw new Error('Điểm sàn phải là số không âm');
        }
        processedData.minimum_score = minScore;
      }


      if (processedData.foundation_subject_id === null && processedData.subject_minimum_score !== null) {
        throw new Error('Vui lòng chọn môn nền tảng');
      }

      if (processedData.subject_minimum_score !== null) {
        const subjectMinScore = parseFloat(processedData.subject_minimum_score);
        if (isNaN(subjectMinScore) || subjectMinScore < 0) {
          throw new Error('Điểm sàn môn nền tảng phải là số không âm');
        }
        processedData.subject_minimum_score = subjectMinScore;
      }

      return await AdmissionMethodMajorServices.createAdmissionMethodMajor(processedData);
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
      // Tạo đối tượng dữ liệu mới để xử lý các trường hợp đặc biệt
      const processedData = {};
      
      // Chỉ thêm các trường có trong request
      if ('major_id' in data) {
        if (!data.major_id) throw new Error('ID ngành không hợp lệ');
        processedData.major_id = data.major_id;
      }
      
      if ('admission_methods_id' in data) {
        if (!data.admission_methods_id) throw new Error('ID phương thức tuyển sinh không hợp lệ');
        processedData.admission_methods_id = data.admission_methods_id;
      }
      
      // Xử lý các trường có thể null
      if ('quota' in data) {
        processedData.quota = data.quota === '' ? null : data.quota;
        
        if (processedData.quota !== null) {
          const quota = parseInt(processedData.quota);
          if (isNaN(quota) || quota <= 0) {
            throw new Error('Chỉ tiêu phải là số nguyên dương');
          }
          processedData.quota = quota;
        }
      }
      
      if ('minimum_score' in data) {
        processedData.minimum_score = data.minimum_score === '' ? null : data.minimum_score;
        
        if (processedData.minimum_score !== null) {
          const minScore = parseFloat(processedData.minimum_score);
          if (isNaN(minScore) || minScore < 0) {
            throw new Error('Điểm sàn phải là số không âm');
          }
          processedData.minimum_score = minScore;
        }
      }
      
      if ('foundation_subject_id' in data) {
        processedData.foundation_subject_id = data.foundation_subject_id === '' ? null : data.foundation_subject_id;
      }
      
      if ('subject_minimum_score' in data) {
        processedData.subject_minimum_score = data.subject_minimum_score === '' ? null : data.subject_minimum_score;
        
        if (processedData.subject_minimum_score !== null) {
          const subjectMinScore = parseFloat(processedData.subject_minimum_score);
          if (isNaN(subjectMinScore) || subjectMinScore < 0) {
            throw new Error('Điểm sàn môn nền tảng phải là số không âm');
          }
          processedData.subject_minimum_score = subjectMinScore;
        }
      }
      
      // Kiểm tra nếu không có dữ liệu để cập nhật
      if (Object.keys(processedData).length === 0) {
        throw new Error('Không có thông tin nào được cập nhật');
      }
      
      // Kiểm tra mối quan hệ giữa môn nền tảng và điểm sàn môn nền tảng
      if ('foundation_subject_id' in processedData || 'subject_minimum_score' in processedData) {
        let currentData;
        try {
          currentData = await this.getAdmissionMethodMajorById(admissionMethodMajorId);
        } catch (err) {
          currentData = { 
            foundation_subject_id: null, 
            subject_minimum_score: null 
          };
        }
        
        const finalFoundationSubjectId = 'foundation_subject_id' in processedData
          ? processedData.foundation_subject_id
          : currentData.foundation_subject_id;
          
        const finalSubjectMinScore = 'subject_minimum_score' in processedData
          ? processedData.subject_minimum_score
          : currentData.subject_minimum_score;
        
        
        if (finalFoundationSubjectId === null && finalSubjectMinScore !== null) {
          throw new Error('Vui lòng chọn môn nền tảng');
        }
      }
      
      // Gọi API để cập nhật
      return await AdmissionMethodMajorServices.updateAdmissionMethodMajor(admissionMethodMajorId, processedData);
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
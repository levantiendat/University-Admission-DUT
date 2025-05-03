import qnaServices from '../../models/admins/qnaServices';

export default {
  /**
   * Lấy danh sách câu hỏi
   */
  async getAllQuestions() {
    try {
      return await qnaServices.getAllQuestions();
    } catch (error) {
      throw new Error(`Không thể lấy danh sách câu hỏi: ${error.message}`);
    }
  },

  /**
   * Lấy chi tiết câu hỏi theo ID
   * @param {number} id - ID của câu hỏi
   */
  async getQuestionById(id) {
    try {
      return await qnaServices.getQuestion(id);
    } catch (error) {
      throw new Error(`Không thể lấy thông tin câu hỏi: ${error.message}`);
    }
  },

  /**
   * Tạo câu hỏi mới
   * @param {Object} data - Dữ liệu câu hỏi mới
   */
  async createQuestion(data) {
    try {
      // Validate input
      if (!data.title || data.title.trim() === '') {
        throw new Error('Vui lòng nhập tiêu đề câu hỏi');
      }

      if (!data.body_text || data.body_text.trim() === '') {
        throw new Error('Vui lòng nhập nội dung câu hỏi');
      }

      // Format data
      const formattedData = {
        title: data.title.trim(),
        body_text: data.body_text.trim()
      };

      return await qnaServices.createQuestion(formattedData);
    } catch (error) {
      throw new Error(`Không thể tạo câu hỏi mới: ${error.message}`);
    }
  },

  /**
   * Cập nhật thông tin câu hỏi
   * @param {number} id - ID của câu hỏi
   * @param {Object} data - Dữ liệu cập nhật
   */
  async updateQuestion(id, data) {
    try {
      // Validate data
      if (data.title !== undefined && data.title.trim() === '') {
        throw new Error('Tiêu đề câu hỏi không được để trống');
      }

      if (data.body_text !== undefined && data.body_text.trim() === '') {
        throw new Error('Nội dung câu hỏi không được để trống');
      }

      // Format data
      const formattedData = { ...data };
      if (formattedData.title) formattedData.title = formattedData.title.trim();
      if (formattedData.body_text) formattedData.body_text = formattedData.body_text.trim();

      return await qnaServices.updateQuestion(id, formattedData);
    } catch (error) {
      throw new Error(`Không thể cập nhật câu hỏi: ${error.message}`);
    }
  },

  /**
   * Xóa câu hỏi
   * @param {number} id - ID của câu hỏi
   */
  async deleteQuestion(id) {
    try {
      return await qnaServices.deleteQuestion(id);
    } catch (error) {
      throw new Error(`Không thể xóa câu hỏi: ${error.message}`);
    }
  },

  /**
   * Lấy danh sách câu trả lời cho câu hỏi
   * @param {number} questionId - ID của câu hỏi
   */
  async getResponsesByQuestionId(questionId) {
    try {
      return await qnaServices.getResponsesByQuestionId(questionId);
    } catch (error) {
      throw new Error(`Không thể lấy danh sách câu trả lời: ${error.message}`);
    }
  },

  /**
   * Lấy chi tiết câu trả lời theo ID
   * @param {number} id - ID của câu trả lời
   */
  async getResponseById(id) {
    try {
      return await qnaServices.getResponse(id);
    } catch (error) {
      throw new Error(`Không thể lấy thông tin câu trả lời: ${error.message}`);
    }
  },

  /**
   * Tạo câu trả lời mới
   * @param {Object} data - Dữ liệu câu trả lời mới
   */
  async createResponse(data) {
    try {
      // Validate input
      if (!data.body_text || data.body_text.trim() === '') {
        throw new Error('Vui lòng nhập nội dung câu trả lời');
      }

      if (!data.question_id) {
        throw new Error('ID câu hỏi không hợp lệ');
      }

      // Format data
      const formattedData = {
        body_text: data.body_text.trim(),
        question_id: parseInt(data.question_id)
      };

      return await qnaServices.createResponse(formattedData);
    } catch (error) {
      throw new Error(`Không thể tạo câu trả lời mới: ${error.message}`);
    }
  },

  /**
   * Cập nhật thông tin câu trả lời
   * @param {number} id - ID của câu trả lời
   * @param {Object} data - Dữ liệu cập nhật
   */
  async updateResponse(id, data) {
    try {
      // Validate data
      if (data.body_text !== undefined && data.body_text.trim() === '') {
        throw new Error('Nội dung câu trả lời không được để trống');
      }

      // Format data
      const formattedData = { ...data };
      if (formattedData.body_text) formattedData.body_text = formattedData.body_text.trim();

      return await qnaServices.updateResponse(id, formattedData);
    } catch (error) {
      throw new Error(`Không thể cập nhật câu trả lời: ${error.message}`);
    }
  },

  /**
   * Xóa câu trả lời
   * @param {number} id - ID của câu trả lời
   */
  async deleteResponse(id) {
    try {
      return await qnaServices.deleteResponse(id);
    } catch (error) {
      throw new Error(`Không thể xóa câu trả lời: ${error.message}`);
    }
  }
};
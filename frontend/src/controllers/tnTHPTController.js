import testTHPTService from '@/models/tnTHPTService'

const TestTHPTController = {
  /**
   * Lấy và xử lý dữ liệu tuyển sinh để hiển thị
   * @returns {Promise<Object>} - Dữ liệu đã được xử lý
   */
  async getTestTHPTData() {
    try {
      // Gọi trực tiếp các hàm async (không cần Promise.all nếu không phải mảng promises)
      const testTHPT = await testTHPTService.getTestTHPTs();
      const majors = await testTHPTService.getMajors();

      console.log('testTHPT', testTHPT);
      console.log('majors', majors);
      
      return {
        majors,
        testTHPT
      };
    } catch (error) {
      console.error('Lỗi khi xử lý dữ liệu tuyển sinh:', error);
      throw error;
    }
  }
};

export default TestTHPTController;

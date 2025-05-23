import tnTHPTService from '@/models/tnTHPTService'

const TNTHPTController = {
  /**
   * Lấy và xử lý dữ liệu tuyển sinh để hiển thị
   * @returns {Promise<Object>} - Dữ liệu đã được xử lý
   */
  async getTNTHPTData() {
    try {
      // Gọi trực tiếp các hàm async (không cần Promise.all nếu không phải mảng promises)
      const testTHPT = await tnTHPTService.getTestTHPTs();
      const majors = await tnTHPTService.getMajors();

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

export default TNTHPTController;

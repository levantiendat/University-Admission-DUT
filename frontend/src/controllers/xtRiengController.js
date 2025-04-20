import xtrService from '@/models/xtRiengService'

const XTRController = {
  /**
   * Lấy và xử lý dữ liệu tuyển sinh để hiển thị
   * @returns {Promise<Object>} - Dữ liệu đã được xử lý
   */
  async getXTRData() {
    try {
      // Gọi trực tiếp các hàm async (không cần Promise.all nếu không phải mảng promises)
      const xtr = await xtrService.getXTRs();
      const majors = await xtrService.getMajors();

      console.log('xtt', xtr);
      console.log('majors', majors);
      
      return {
        xtr,
        majors
      };
    } catch (error) {
      console.error('Lỗi khi xử lý dữ liệu tuyển sinh:', error);
      throw error;
    }
  }
};

export default XTRController;

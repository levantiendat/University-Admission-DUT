import dgnlService from '@/models/DGNLService'

const DGNLController = {
  /**
   * Lấy và xử lý dữ liệu tuyển sinh để hiển thị
   * @returns {Promise<Object>} - Dữ liệu đã được xử lý
   */
  async getDGNLData() {
    try {
      // Gọi trực tiếp các hàm async (không cần Promise.all nếu không phải mảng promises)
      const dgnl = await dgnlService.getDGNLs();
      const majors = await dgnlService.getMajors();

      console.log('xtt', dgnl);
      console.log('majors', majors);
      
      return {
        dgnl,
        majors
      };
    } catch (error) {
      console.error('Lỗi khi xử lý dữ liệu tuyển sinh:', error);
      throw error;
    }
  }
};

export default DGNLController;

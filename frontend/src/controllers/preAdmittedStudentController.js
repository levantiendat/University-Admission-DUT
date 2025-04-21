import preAdmittedStudentService from '@/models/preAdmittedStudentService'

export default {
  async getAllData() {
    try {
      // Lấy dữ liệu từ các API
      const faculties = await preAdmittedStudentService.getFaculties()
      const majors = await preAdmittedStudentService.getMajors()
      const cities = await preAdmittedStudentService.getCities()
      const admissionMethods = await preAdmittedStudentService.getAdmissionMethods()
      const genderStats = await preAdmittedStudentService.getPreviousAdmissionStudentByGender()
      const cityStats = await preAdmittedStudentService.getPreviousAdmissionStudentByCity()
      const methodStats = await preAdmittedStudentService.getPreviousAdmissionStudentByAdmissionMethod()
      const scoreRangeStats = await preAdmittedStudentService.getPreviousAdmissionStudentByMajorRangePoint()
      
      // Xác định danh sách năm có dữ liệu
      const availableYears = this.extractAvailableYears([
        ...genderStats, ...cityStats, ...methodStats, ...scoreRangeStats
      ])
      
      // Kết hợp dữ liệu chính
      const majorsWithFaculty = majors.map(major => {
        const faculty = faculties.find(f => f.id === major.faculty_id) || {
          id: null,
          name: 'Không xác định',
          faculty_code: 'N/A'
        }
        
        return {
          ...major,
          faculty: {
            id: faculty.id,
            name: faculty.name,
            code: faculty.faculty_code
          }
        }
      })
      
      return {
        majors: majorsWithFaculty,
        faculties,
        cities,
        admissionMethods,
        stats: {
          gender: genderStats,
          city: cityStats,
          method: methodStats,
          scoreRange: scoreRangeStats
        },
        availableYears
      }
    } catch (error) {
      console.error('Error in getAllData:', error)
      throw error
    }
  },
  
  extractAvailableYears(statsArray) {
    const years = new Set()
    statsArray.forEach(stat => {
      if (stat.year) {
        years.add(stat.year)
      }
    })
    return Array.from(years).sort()
  },
  
  // Lọc dữ liệu thống kê theo điều kiện
  filterStatsByCondition(stats, conditions) {
    return stats.filter(item => {
      // Lọc theo năm nếu có
      if (conditions.year && item.year !== conditions.year) {
        return false
      }
      
      // Lọc theo ngành nếu có
      if (conditions.majorId && item.major_id !== conditions.majorId) {
        return false
      }
      
      // Lọc theo khoa nếu có
      if (conditions.facultyId && conditions.majorsInFaculty) {
        const isInFaculty = conditions.majorsInFaculty.some(
          majorId => majorId === item.major_id
        )
        if (!isInFaculty) {
          return false
        }
      }
      
      return true
    })
  },
  
  // Tổng hợp dữ liệu thống kê theo giới tính
  prepareGenderStatsData(stats, conditions, majors) {
    // Lọc dữ liệu theo điều kiện
    const filteredStats = this.filterStatsByCondition(stats, conditions)
    
    if (filteredStats.length === 0) return null
    
    // Tính tổng số lượng sinh viên theo giới tính
    const maleCount = filteredStats
      .filter(stat => stat.gender === 1)
      .reduce((sum, stat) => sum + stat.total, 0)
    
    const femaleCount = filteredStats
      .filter(stat => stat.gender === 0)
      .reduce((sum, stat) => sum + stat.total, 0)
    
    return {
      labels: ['Nam', 'Nữ'],
      datasets: [{
        data: [maleCount, femaleCount],
        backgroundColor: [
          'rgba(54, 162, 235, 0.8)',
          'rgba(255, 99, 132, 0.8)'
        ],
        borderColor: [
          'rgba(54, 162, 235, 1)',
          'rgba(255, 99, 132, 1)'
        ],
        borderWidth: 2
      }]
    }
  },
  
  // Tổng hợp dữ liệu thống kê theo thành phố
  prepareCityStatsData(stats, conditions, cities, maxItems = 10) {
    // Lọc dữ liệu theo điều kiện
    const filteredStats = this.filterStatsByCondition(stats, conditions)
    
    if (filteredStats.length === 0) return null
    
    // Tổng hợp dữ liệu theo thành phố
    const cityData = {}
    
    filteredStats.forEach(stat => {
      if (!cityData[stat.city_id]) {
        cityData[stat.city_id] = 0
      }
      cityData[stat.city_id] += stat.total
    })
    
    // Chuyển đổi thành mảng và sắp xếp theo số lượng giảm dần
    const sortedCities = Object.entries(cityData)
      .map(([cityId, total]) => {
        const city = cities.find(c => c.id === parseInt(cityId))
        return {
          cityId: parseInt(cityId),
          name: city ? city.name : `Thành phố ${cityId}`,
          total
        }
      })
      .sort((a, b) => b.total - a.total)
    
    // Giới hạn số lượng thành phố hiển thị
    const topCities = sortedCities.slice(0, maxItems)
    const otherTotal = sortedCities.slice(maxItems).reduce((sum, city) => sum + city.total, 0)
    
    // Chuẩn bị dữ liệu cho biểu đồ
    const labels = topCities.map(city => city.name)
    const data = topCities.map(city => city.total)
    
    // Thêm mục "Khác" nếu còn nhiều thành phố
    if (otherTotal > 0) {
      labels.push('Khác')
      data.push(otherTotal)
    }
    
    // Tạo màu sắc ngẫu nhiên cho từng thành phố
    const backgroundColors = this.generateColors(labels.length, 0.8)
    const borderColors = this.generateColors(labels.length, 1)
    
    return {
      labels,
      datasets: [{
        data,
        backgroundColor: backgroundColors,
        borderColor: borderColors,
        borderWidth: 2
      }]
    }
  },
  
  // Tổng hợp dữ liệu thống kê theo phương thức xét tuyển
  prepareMethodStatsData(stats, conditions, methods) {
    // Lọc dữ liệu theo điều kiện
    const filteredStats = this.filterStatsByCondition(stats, conditions)
    
    if (filteredStats.length === 0) return null
    
    // Tổng hợp dữ liệu theo phương thức
    const methodData = {}
    
    filteredStats.forEach(stat => {
      if (!methodData[stat.admission_method_id]) {
        methodData[stat.admission_method_id] = 0
      }
      methodData[stat.admission_method_id] += stat.total
    })
    
    // Chuyển đổi thành mảng
    const methodItems = Object.entries(methodData).map(([methodId, total]) => {
      const method = methods.find(m => m.id === parseInt(methodId))
      return {
        methodId: parseInt(methodId),
        name: method ? method.name : `Phương thức ${methodId}`,
        total
      }
    })
    
    // Chuẩn bị dữ liệu cho biểu đồ
    const labels = methodItems.map(item => item.name)
    const data = methodItems.map(item => item.total)
    
    // Màu sắc cho từng phương thức
    const backgroundColors = this.generateColors(labels.length, 0.8)
    const borderColors = this.generateColors(labels.length, 1)
    
    return {
      labels,
      datasets: [{
        data,
        backgroundColor: backgroundColors,
        borderColor: borderColors,
        borderWidth: 2
      }]
    }
  },
  
  // Tổng hợp dữ liệu thống kê theo khoảng điểm - ĐÃ SỬA LỖI
  prepareScoreRangeStatsData(stats, conditions) {
    try {
      // Lọc dữ liệu theo điều kiện
      const filteredStats = this.filterStatsByCondition(stats, conditions)
      
      if (!filteredStats || filteredStats.length === 0) {
        console.log('No data available for score range chart');
        return null;
      }
      
      // Tổng hợp dữ liệu theo khoảng điểm
      const scoreRangeData = {};
      
      filteredStats.forEach(stat => {
        // Đảm bảo score_range có giá trị và không phải undefined/null
        if (stat.score_range && typeof stat.score_range === 'string') {
          if (!scoreRangeData[stat.score_range]) {
            scoreRangeData[stat.score_range] = 0;
          }
          
          scoreRangeData[stat.score_range] += stat.total;
        }
      });
      
      // Nếu không có dữ liệu khoảng điểm hợp lệ
      if (Object.keys(scoreRangeData).length === 0) {
        console.log('No valid score ranges found');
        return null;
      }
      
      // Sắp xếp khoảng điểm theo thứ tự tăng dần của điểm bắt đầu
      const sortedScoreRanges = Object.keys(scoreRangeData).sort((a, b) => {
        // Trích xuất giá trị đầu của khoảng điểm trong format "X-Y"
        const aLower = parseFloat(a.split('-')[0] || 0);
        const bLower = parseFloat(b.split('-')[0] || 0);
        return aLower - bLower;
      });
      
      // Chuẩn bị dữ liệu cho biểu đồ
      const labels = sortedScoreRanges;
      const data = sortedScoreRanges.map(range => scoreRangeData[range]);
      
      // Kiểm tra kết quả
      if (labels.length === 0 || data.length === 0) {
        console.log('Empty labels or data arrays');
        return null;
      }
      
      // Màu gradient cho biểu đồ khoảng điểm (từ xanh lá đến đỏ)
      const colors = this.generateGradientColors(labels.length, 
        [75, 192, 192],  // Start color (xanh lá nhạt)
        [255, 99, 132]   // End color (đỏ hồng)
      );
      
      // Trả về dữ liệu chuẩn để render
      return {
        labels,
        datasets: [{
          label: 'Số lượng sinh viên',
          data,
          backgroundColor: colors.map(color => `rgba(${color[0]}, ${color[1]}, ${color[2]}, 0.8)`),
          borderColor: colors.map(color => `rgba(${color[0]}, ${color[1]}, ${color[2]}, 1)`),
          borderWidth: 1
        }]
      };
    } catch (error) {
      console.error('Error in prepareScoreRangeStatsData:', error);
      return null;
    }
  },
  
  // Tạo ra một mảng màu ngẫu nhiên
  generateColors(count, opacity = 1) {
    if (!count || count <= 0) return []; // Bảo vệ khỏi đầu vào không hợp lệ
    
    const baseColors = [
      `rgba(255, 99, 132, ${opacity})`,   // Đỏ hồng
      `rgba(54, 162, 235, ${opacity})`,   // Xanh dương
      `rgba(255, 206, 86, ${opacity})`,   // Vàng
      `rgba(75, 192, 192, ${opacity})`,   // Xanh lá nhạt
      `rgba(153, 102, 255, ${opacity})`,  // Tím
      `rgba(255, 159, 64, ${opacity})`,   // Cam
      `rgba(255, 99, 255, ${opacity})`,   // Hồng
      `rgba(99, 255, 132, ${opacity})`,   // Xanh lá
      `rgba(45, 192, 255, ${opacity})`,   // Xanh dương nhạt
      `rgba(255, 45, 45, ${opacity})`     // Đỏ
    ]
    
    // Nếu cần nhiều màu hơn, tạo thêm màu ngẫu nhiên
    const colors = []
    for (let i = 0; i < count; i++) {
      if (i < baseColors.length) {
        colors.push(baseColors[i])
      } else {
        // Tạo màu ngẫu nhiên
        const r = Math.floor(Math.random() * 255)
        const g = Math.floor(Math.random() * 255)
        const b = Math.floor(Math.random() * 255)
        colors.push(`rgba(${r}, ${g}, ${b}, ${opacity})`)
      }
    }
    
    return colors
  },
  
  // Tạo gradient màu từ màu bắt đầu đến màu kết thúc - HÀM MỚI
  generateGradientColors(count, startColor, endColor) {
    if (!count || count <= 0) return []; // Bảo vệ khỏi đầu vào không hợp lệ
    
    const colors = []
    for (let i = 0; i < count; i++) {
      // Tính toán màu dựa trên vị trí tương đối
      const ratio = count > 1 ? i / (count - 1) : 0
      const r = Math.round(startColor[0] + ratio * (endColor[0] - startColor[0]))
      const g = Math.round(startColor[1] + ratio * (endColor[1] - startColor[1]))
      const b = Math.round(startColor[2] + ratio * (endColor[2] - startColor[2]))
      colors.push([r, g, b])
    }
    return colors
  },
  
  // Lấy danh sách ID ngành thuộc khoa
  getMajorIdsByFaculty(majors, facultyId) {
    if (!majors || !facultyId) return [];
    
    return majors
      .filter(major => major.faculty_id === facultyId)
      .map(major => major.id)
  },
  
  // Lấy tên đối tượng thống kê
  getStatTargetName(type, selectedFaculty, selectedMajor, faculties, majors) {
    if (type === 'major' && selectedMajor) {
      const major = majors.find(m => m.id === selectedMajor)
      return major ? major.name : 'Ngành không xác định'
    } else if (type === 'faculty' && selectedFaculty) {
      const faculty = faculties.find(f => f.id === selectedFaculty)
      return faculty ? faculty.name : 'Khoa không xác định'
    } else {
      return 'Toàn trường'
    }
  },

  // Helper function để xác định tiêu đề biểu đồ
  getChartTitle(statsType, targetType, targetName, year) {
    let statsTypeText = ''
    
    switch (statsType) {
      case 'gender':
        statsTypeText = 'theo giới tính'
        break
      case 'city':
        statsTypeText = 'theo thành phố'
        break
      case 'method':
        statsTypeText = 'theo phương thức xét tuyển'
        break
      case 'scoreRange':
        statsTypeText = 'theo khoảng điểm'
        break
      default:
        statsTypeText = ''
    }
    
    return `Thống kê sinh viên trúng tuyển ${statsTypeText} - ${targetName} - Năm ${year}`
  }
}
// controllers/bonuspoint.js

const calculateLanguageCertificatePoints = (certificateType, level) => {
  // Points for each level
  const points = {
    level1: 0.25,
    level2: 0.5,
    level3: 0.75,
    level4: 1.0
  };

  // Check which level the certificate and specific level corresponds to
  switch (certificateType) {
    case 'KNLNN':
      // KNLNN Việt Nam: Bậc 3, Bậc 4, Bậc 5, Bậc 6
      if (level === 'Bậc 3') return points.level1;
      if (level === 'Bậc 4') return points.level2;
      if (level === 'Bậc 5') return points.level3;
      if (level === 'Bậc 6') return points.level4;
      break;

    case 'Aptis':
      // Khung tham chiều châu âu Aptis ESOL: B1, B2, C1, C2
      if (level === 'B1') return points.level1;
      if (level === 'B2') return points.level2;
      if (level === 'C1') return points.level3;
      if (level === 'C2') return points.level4;
      break;

    case 'IELTS':
      // ITELS Academic: 5, 5.5-6.5, 7.0-8.0, 8.5-9.0
      const score = parseFloat(level);
      if (score === 5) return points.level1;
      if (score >= 5.5 && score <= 6.5) return points.level2;
      if (score >= 7.0 && score <= 8.0) return points.level3;
      if (score >= 8.5 && score <= 9.0) return points.level4;
      break;

    case 'VSEP':
      // VSEP (Mức 1-3): 5.5, 6.0-8.0, 8.5-10.0
      const vsepScore = parseFloat(level);
      if (vsepScore === 5.5) return points.level1;
      if (vsepScore >= 6.0 && vsepScore <= 8.0) return points.level2;
      if (vsepScore >= 8.5 && vsepScore <= 10.0) return points.level3;
      break;

    case 'PEIC':
      // PEIC: Level 2, Level 3, Level 4, Level 5
      if (level === 'Level 2') return points.level1;
      if (level === 'Level 3') return points.level2;
      if (level === 'Level 4') return points.level3;
      if (level === 'Level 5') return points.level4;
      break;

    case 'PTE':
      // PTE Academic: 45-58, 59-75, 76-84, >=85
      const pteScore = parseInt(level);
      if (pteScore >= 45 && pteScore <= 58) return points.level1;
      if (pteScore >= 59 && pteScore <= 75) return points.level2;
      if (pteScore >= 76 && pteScore <= 84) return points.level3;
      if (pteScore >= 85) return points.level4;
      break;

    case 'Linguaskill':
      // Linguaskill 140-159, 160-179, >=180
      const linguaScore = parseInt(level);
      if (linguaScore >= 140 && linguaScore <= 159) return points.level1;
      if (linguaScore >= 160 && linguaScore <= 179) return points.level2;
      if (linguaScore >= 180) return points.level3;
      break;

    case 'Cambridge':
      // Cambridge Assessment English
      if (level === 'B1 Preliminary' || level === 'B1 Business Preliminary') return points.level1;
      if (level === 'B2 First' || level === 'B2 Business Vantage') return points.level2;
      if (level === 'C1 Advanced' || level === 'C1 Business Higher') return points.level3;
      if (level === 'C2 Proficiency') return points.level4;
      break;

    case 'CET':
      // Cambridge English Test
      if (level === 'PTE' || (parseInt(level) >= 140 && parseInt(level) <= 159)) return points.level1;
      if (level === 'FCE' || (parseInt(level) >= 160 && parseInt(level) <= 179)) return points.level2;
      if (level === 'CAE' || (parseInt(level) >= 180 && parseInt(level) <= 199)) return points.level3;
      if (level === 'CPE' || (parseInt(level) >= 200 && parseInt(level) <= 230)) return points.level4;
      break;

    case 'JLPT':
      // Japanese Language Proficiency Test (JLPT): N5, N4, N3, N2, N1
      if (level === 'N4') return points.level1;
      if (level === 'N3') return points.level2;
      if (level === 'N2') return points.level3;
      if (level === 'N1') return points.level4;
      break;

    case 'TOEIC':
      // For TOEIC, we need all four skills and take the minimum level
      // Format should be an object with listen, read, speak, write properties
      if (typeof level === 'object') {
        const { listen, read, speak, write } = level;
        
        // Ensure all values are numbers for calculation purposes
        const listenVal = parseInt(listen) || 0;
        const readVal = parseInt(read) || 0;
        const speakVal = parseInt(speak) || 0;
        const writeVal = parseInt(write) || 0;
        
        // Calculate level for each skill
        let listenLevel = 0;
        let readLevel = 0;
        let speakLevel = 0;
        let writeLevel = 0;
        
        // Listening skill (thang 0-495)
        if (listenVal >= 275 && listenVal <= 395) listenLevel = 1;
        else if (listenVal >= 400 && listenVal <= 485) listenLevel = 2;
        else if (listenVal >= 490) listenLevel = 3;
        
        // Reading skill (thang 0-495)
        if (readVal >= 275 && readVal <= 380) readLevel = 1;
        else if (readVal >= 385 && readVal <= 450) readLevel = 2;
        else if (readVal >= 455) readLevel = 3;
        
        // Speaking skill (thang 0-200)
        if (speakVal >= 120 && speakVal <= 150) speakLevel = 1;
        else if (speakVal >= 160 && speakVal <= 170) speakLevel = 2;
        else if (speakVal >= 180) speakLevel = 3;
        
        // Writing skill (thang 0-200)
        if (writeVal >= 120 && writeVal <= 140) writeLevel = 1;
        else if (writeVal >= 150 && writeVal <= 170) writeLevel = 2;
        else if (writeVal >= 180) writeLevel = 3;
        
        // Get the minimum level (only consider skills that have valid levels)
        const validLevels = [
          listenLevel > 0 ? listenLevel : 999,
          readLevel > 0 ? readLevel : 999,
          speakLevel > 0 ? speakLevel : 999,
          writeLevel > 0 ? writeLevel : 999
        ].filter(l => l !== 999);

        // If all values are 0 or invalid, return 0
        if (validLevels.length === 0) return 0;
        
        // Otherwise, take the minimum of valid levels
        const minLevel = Math.min(...validLevels);
        
        if (minLevel === 1) return points.level1;
        if (minLevel === 2) return points.level2;
        if (minLevel === 3) return points.level3;
      }
      break;

    case 'TOEFL':
      // TOEFL iBT: 30-45, 46-93, 94-114, >=115
      const toeflScore = parseInt(level);
      if (toeflScore >= 30 && toeflScore <= 45) return points.level1;
      if (toeflScore >= 46 && toeflScore <= 93) return points.level2;
      if (toeflScore >= 94 && toeflScore <= 114) return points.level3;
      if (toeflScore >= 115) return points.level4;
      break;
  }

  return 0; // Default if no match
};

const calculateDirectAdmissionPoints = (achievementType) => {
  switch (achievementType) {
    case 'hero':
      // Anh hùng lực lượng lao động, Anh hùng lực lượng vũ trang nhân dân, Chiến sĩ thi đua toàn quốc
      return 2.0;
    case 'national_first':
      // Giải nhất chọn HSG, thi KHKT cấp quốc gia, quốc tế
      return 2.0;
    case 'national_second':
      // Giải nhì chọn HSG, thi KHKT cấp quốc gia, quốc tế
      return 1.5;
    case 'national_third':
      // Giải ba chọn HSG, thi KHKT cấp quốc gia, quốc tế
      return 1.0;
    default:
      return 0;
  }
};

module.exports = {
  calculateLanguageCertificatePoints,
  calculateDirectAdmissionPoints
};
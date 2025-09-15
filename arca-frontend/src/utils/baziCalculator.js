// Calculadora BaZi simplificada para frontend
// Implementação básica dos Quatro Pilares do Destino

export class BaZiCalculator {
  constructor() {
    this.setupReferenceTables();
  }

  setupReferenceTables() {
    // Heavenly Stems (Troncos Celestiais)
    this.heavenlyStems = [
      { index: 0, chinese: "甲", pinyin: "Jia", element: "Wood", polarity: "Yang" },
      { index: 1, chinese: "乙", pinyin: "Yi", element: "Wood", polarity: "Yin" },
      { index: 2, chinese: "丙", pinyin: "Bing", element: "Fire", polarity: "Yang" },
      { index: 3, chinese: "丁", pinyin: "Ding", element: "Fire", polarity: "Yin" },
      { index: 4, chinese: "戊", pinyin: "Wu", element: "Earth", polarity: "Yang" },
      { index: 5, chinese: "己", pinyin: "Ji", element: "Earth", polarity: "Yin" },
      { index: 6, chinese: "庚", pinyin: "Geng", element: "Metal", polarity: "Yang" },
      { index: 7, chinese: "辛", pinyin: "Xin", element: "Metal", polarity: "Yin" },
      { index: 8, chinese: "壬", pinyin: "Ren", element: "Water", polarity: "Yang" },
      { index: 9, chinese: "癸", pinyin: "Gui", element: "Water", polarity: "Yin" }
    ];

    // Earthly Branches (Ramos Terrestres)
    this.earthlyBranches = [
      { index: 0, chinese: "子", pinyin: "Zi", zodiac: "Rat", element: "Water", season: "Winter" },
      { index: 1, chinese: "丑", pinyin: "Chou", zodiac: "Ox", element: "Earth", season: "Winter" },
      { index: 2, chinese: "寅", pinyin: "Yin", zodiac: "Tiger", element: "Wood", season: "Spring" },
      { index: 3, chinese: "卯", pinyin: "Mao", zodiac: "Rabbit", element: "Wood", season: "Spring" },
      { index: 4, chinese: "辰", pinyin: "Chen", zodiac: "Dragon", element: "Earth", season: "Spring" },
      { index: 5, chinese: "巳", pinyin: "Si", zodiac: "Snake", element: "Fire", season: "Summer" },
      { index: 6, chinese: "午", pinyin: "Wu", zodiac: "Horse", element: "Fire", season: "Summer" },
      { index: 7, chinese: "未", pinyin: "Wei", zodiac: "Goat", element: "Earth", season: "Summer" },
      { index: 8, chinese: "申", pinyin: "Shen", zodiac: "Monkey", element: "Metal", season: "Autumn" },
      { index: 9, chinese: "酉", pinyin: "You", zodiac: "Rooster", element: "Metal", season: "Autumn" },
      { index: 10, chinese: "戌", pinyin: "Xu", zodiac: "Dog", element: "Earth", season: "Autumn" },
      { index: 11, chinese: "亥", pinyin: "Hai", zodiac: "Pig", element: "Water", season: "Winter" }
    ];

    // Five Elements Cycles
    this.elementCycles = {
      productive: {
        "Wood": "Fire",
        "Fire": "Earth",
        "Earth": "Metal",
        "Metal": "Water",
        "Water": "Wood"
      },
      destructive: {
        "Wood": "Earth",
        "Fire": "Metal",
        "Earth": "Water",
        "Metal": "Wood",
        "Water": "Fire"
      }
    };
  }

  calculateFourPillars(birthDateTime, timezoneOffset = -3) {
    const adjustedDateTime = new Date(birthDateTime.getTime() + (timezoneOffset + 8) * 60 * 60 * 1000);
    
    // Calcular cada pilar
    const yearPillar = this.calculateYearPillar(adjustedDateTime.getFullYear());
    const monthPillar = this.calculateMonthPillar(adjustedDateTime.getMonth() + 1, adjustedDateTime.getDate(), yearPillar.stem.index);
    const dayPillar = this.calculateDayPillar(adjustedDateTime);
    const hourPillar = this.calculateHourPillar(adjustedDateTime.getHours(), dayPillar.stem.index);

    // Day Master (elemento central da pessoa)
    const dayMaster = dayPillar.stem;

    // Análise elemental
    const elementAnalysis = this.analyzeElements(yearPillar, monthPillar, dayPillar, hourPillar);

    // Determinar força do Day Master
    const dayMasterStrength = this.calculateDayMasterStrength(dayMaster, monthPillar, elementAnalysis);

    // Identificar Useful God (用神)
    const usefulGod = this.identifyUsefulGod(dayMaster, dayMasterStrength, elementAnalysis);

    // Gerar recomendações
    const recommendations = this.generateRecommendations(dayMaster, usefulGod, elementAnalysis);

    return {
      birth_info: {
        datetime: birthDateTime.toISOString(),
        timezone_offset: timezoneOffset,
        adjusted_datetime: adjustedDateTime.toISOString()
      },
      four_pillars: {
        year: yearPillar,
        month: monthPillar,
        day: dayPillar,
        hour: hourPillar
      },
      day_master: {
        ...dayMaster,
        strength: dayMasterStrength
      },
      element_analysis: elementAnalysis,
      useful_god: usefulGod,
      recommendations: recommendations,
      chart_summary: this.generateChartSummary(dayMaster, dayMasterStrength, usefulGod)
    };
  }

  calculateYearPillar(year) {
    const yearOffset = year - 1984; // 1984 foi ano Jia Zi
    let stemIndex = yearOffset % 10;
    let branchIndex = yearOffset % 12;

    if (stemIndex < 0) stemIndex += 10;
    if (branchIndex < 0) branchIndex += 12;

    return {
      stem: this.heavenlyStems[stemIndex],
      branch: this.earthlyBranches[branchIndex],
      year: year
    };
  }

  calculateMonthPillar(month, day, yearStemIndex) {
    const chineseMonth = this.getChineseMonth(month, day);
    const monthStemIndex = (yearStemIndex * 2 + chineseMonth) % 10;
    const monthBranchIndex = (chineseMonth + 1) % 12;

    return {
      stem: this.heavenlyStems[monthStemIndex],
      branch: this.earthlyBranches[monthBranchIndex],
      chinese_month: chineseMonth,
      gregorian_month: month
    };
  }

  calculateDayPillar(birthDate) {
    const epochDate = new Date(1900, 0, 1);
    const daysSinceEpoch = Math.floor((birthDate - epochDate) / (1000 * 60 * 60 * 24));
    const cyclePosition = daysSinceEpoch % 60;

    const stemIndex = cyclePosition % 10;
    const branchIndex = cyclePosition % 12;

    return {
      stem: this.heavenlyStems[stemIndex],
      branch: this.earthlyBranches[branchIndex],
      days_since_epoch: daysSinceEpoch,
      cycle_position: cyclePosition
    };
  }

  calculateHourPillar(hour, dayStemIndex) {
    const chineseHourIndex = Math.floor((hour + 1) / 2) % 12;
    const hourStemIndex = (dayStemIndex * 2 + chineseHourIndex) % 10;

    return {
      stem: this.heavenlyStems[hourStemIndex],
      branch: this.earthlyBranches[chineseHourIndex],
      gregorian_hour: hour,
      chinese_hour_period: chineseHourIndex
    };
  }

  getChineseMonth(month, day) {
    const monthMapping = {
      1: 11, 2: 0, 3: 1, 4: 2, 5: 3, 6: 4,
      7: 5, 8: 6, 9: 7, 10: 8, 11: 9, 12: 10
    };
    return monthMapping[month] || 0;
  }

  analyzeElements(yearPillar, monthPillar, dayPillar, hourPillar) {
    const elementCount = { Wood: 0, Fire: 0, Earth: 0, Metal: 0, Water: 0 };
    const elementStrength = { Wood: 0, Fire: 0, Earth: 0, Metal: 0, Water: 0 };

    const pillars = [yearPillar, monthPillar, dayPillar, hourPillar];

    pillars.forEach(pillar => {
      // Heavenly Stem (mais forte)
      const stemElement = pillar.stem.element;
      elementCount[stemElement] += 1;
      elementStrength[stemElement] += 2;

      // Earthly Branch (menos forte)
      const branchElement = pillar.branch.element;
      elementCount[branchElement] += 1;
      elementStrength[branchElement] += 1;
    });

    const totalStrength = Object.values(elementStrength).reduce((a, b) => a + b, 0);
    const elementPercentages = {};
    Object.keys(elementStrength).forEach(element => {
      elementPercentages[element] = totalStrength > 0 ? (elementStrength[element] / totalStrength * 100) : 0;
    });

    return {
      count: elementCount,
      strength: elementStrength,
      percentages: elementPercentages,
      dominant_element: Object.keys(elementStrength).reduce((a, b) => elementStrength[a] > elementStrength[b] ? a : b),
      weakest_element: Object.keys(elementStrength).reduce((a, b) => elementStrength[a] < elementStrength[b] ? a : b)
    };
  }

  calculateDayMasterStrength(dayMaster, monthPillar, elementAnalysis) {
    const dayMasterElement = dayMaster.element;
    const monthBranchElement = monthPillar.branch.element;

    let seasonalStrength = 0;
    if (monthBranchElement === dayMasterElement) {
      seasonalStrength += 2;
    } else if (this.elementCycles.productive[monthBranchElement] === dayMasterElement) {
      seasonalStrength += 1;
    } else if (this.elementCycles.destructive[monthBranchElement] === dayMasterElement) {
      seasonalStrength -= 1;
    }

    let supportStrength = 0;
    const dayMasterPercentage = elementAnalysis.percentages[dayMasterElement];

    Object.keys(this.elementCycles.productive).forEach(element => {
      if (this.elementCycles.productive[element] === dayMasterElement) {
        supportStrength += elementAnalysis.percentages[element] * 0.5;
      }
    });

    supportStrength += dayMasterPercentage;

    const totalStrength = seasonalStrength + (supportStrength / 100 * 3);

    if (totalStrength >= 2) return "Strong";
    else if (totalStrength <= -1) return "Very Weak";
    else if (totalStrength < 1) return "Weak";
    else return "Moderate";
  }

  identifyUsefulGod(dayMaster, strength, elementAnalysis) {
    const dayMasterElement = dayMaster.element;

    if (strength === "Strong") {
      const drainingElement = this.elementCycles.productive[dayMasterElement];
      let controllingElement = null;

      Object.keys(this.elementCycles.destructive).forEach(element => {
        if (this.elementCycles.destructive[element] === dayMasterElement) {
          controllingElement = element;
        }
      });

      const chosenElement = controllingElement && 
        elementAnalysis.percentages[controllingElement] < elementAnalysis.percentages[drainingElement] 
        ? controllingElement : drainingElement;

      return {
        element: chosenElement,
        reason: "Day Master é forte, precisa ser drenado ou controlado",
        strength_needed: "Medium"
      };
    } else {
      const supportingElement = Object.keys(this.elementCycles.productive).find(
        element => this.elementCycles.productive[element] === dayMasterElement
      );

      return {
        element: supportingElement || dayMasterElement,
        reason: "Day Master é fraco, precisa de suporte",
        strength_needed: "High"
      };
    }
  }

  generateRecommendations(dayMaster, usefulGod, elementAnalysis) {
    const elementColors = {
      Wood: ["verde", "marrom"],
      Fire: ["vermelho", "laranja"],
      Earth: ["amarelo", "bege"],
      Metal: ["branco", "dourado"],
      Water: ["azul", "preto"]
    };

    const elementDirections = {
      Wood: ["Leste"],
      Fire: ["Sul"],
      Earth: ["Centro"],
      Metal: ["Oeste"],
      Water: ["Norte"]
    };

    const careerGuidance = this.generateCareerGuidance(dayMaster.element, usefulGod.element);

    return {
      favorable_colors: elementColors[usefulGod.element] || [],
      favorable_directions: elementDirections[usefulGod.element] || [],
      career_guidance: careerGuidance,
      lifestyle_tips: this.generateLifestyleTips(dayMaster.element, usefulGod.element),
      feng_shui_tips: this.generateFengShuiTips(usefulGod.element)
    };
  }

  generateCareerGuidance(dayMasterElement, usefulGodElement) {
    const careerMap = {
      Wood: ["Educação", "Saúde", "Agricultura", "Design"],
      Fire: ["Marketing", "Entretenimento", "Tecnologia", "Vendas"],
      Earth: ["Imobiliário", "Construção", "Administração", "Consultoria"],
      Metal: ["Finanças", "Engenharia", "Direito", "Medicina"],
      Water: ["Comunicação", "Transporte", "Pesquisa", "Arte"]
    };

    return careerMap[usefulGodElement] || careerMap[dayMasterElement] || ["Áreas diversas"];
  }

  generateLifestyleTips(dayMasterElement, usefulGodElement) {
    return [
      `Fortaleça o elemento ${usefulGodElement} em sua vida diária`,
      `Use cores relacionadas ao ${usefulGodElement}`,
      `Pratique atividades que representem o elemento ${usefulGodElement}`,
      `Evite excessos do elemento oposto ao ${usefulGodElement}`
    ];
  }

  generateFengShuiTips(usefulGodElement) {
    const tips = {
      Wood: ["Adicione plantas", "Use móveis de madeira", "Decore com verde"],
      Fire: ["Use iluminação quente", "Adicione velas", "Decore com vermelho"],
      Earth: ["Use cristais", "Adicione cerâmica", "Decore com amarelo"],
      Metal: ["Use objetos metálicos", "Adicione espelhos", "Decore com branco"],
      Water: ["Adicione fontes", "Use aquários", "Decore com azul"]
    };

    return tips[usefulGodElement] || ["Mantenha equilíbrio dos elementos"];
  }

  generateChartSummary(dayMaster, strength, usefulGod) {
    return {
      personality_type: `${dayMaster.element} ${dayMaster.polarity}`,
      strength_level: strength,
      primary_need: usefulGod.element,
      balance_status: strength === "Moderate" ? "Equilibrado" : "Precisa de ajuste",
      overall_advice: `Como pessoa ${dayMaster.element}, você deve focar em fortalecer o elemento ${usefulGod.element} para alcançar maior equilíbrio e harmonia.`
    };
  }
}

// Função principal para uso no frontend
export function calculateBaZi(birthDateTime, timezoneOffset = -3) {
  const calculator = new BaZiCalculator();
  return calculator.calculateFourPillars(new Date(birthDateTime), timezoneOffset);
}


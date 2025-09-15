// Calculadora Kua simplificada para frontend
// Implementação do Sistema Ba Zhai (Oito Casas)

export class KuaCalculator {
  constructor() {
    this.setupReferenceTables();
  }

  setupReferenceTables() {
    // Características dos números Kua
    this.kuaCharacteristics = {
      1: {
        element: "Water",
        group: "East",
        personality: "Intuitivo e adaptável",
        strengths: ["Flexibilidade", "Intuição", "Comunicação"],
        weaknesses: ["Indecisão", "Sensibilidade excessiva"]
      },
      2: {
        element: "Earth",
        group: "West",
        personality: "Estável e confiável",
        strengths: ["Estabilidade", "Praticidade", "Lealdade"],
        weaknesses: ["Teimosia", "Resistência a mudanças"]
      },
      3: {
        element: "Wood",
        group: "East",
        personality: "Dinâmico e ambicioso",
        strengths: ["Liderança", "Energia", "Crescimento"],
        weaknesses: ["Impaciência", "Impulsividade"]
      },
      4: {
        element: "Wood",
        group: "East",
        personality: "Criativo e gentil",
        strengths: ["Criatividade", "Gentileza", "Flexibilidade"],
        weaknesses: ["Indecisão", "Falta de foco"]
      },
      6: {
        element: "Metal",
        group: "West",
        personality: "Organizado e determinado",
        strengths: ["Organização", "Determinação", "Liderança"],
        weaknesses: ["Rigidez", "Autoritarismo"]
      },
      7: {
        element: "Metal",
        group: "West",
        personality: "Comunicativo e charmoso",
        strengths: ["Comunicação", "Charme", "Criatividade"],
        weaknesses: ["Superficialidade", "Inconstância"]
      },
      8: {
        element: "Earth",
        group: "West",
        personality: "Ambicioso e persistente",
        strengths: ["Ambição", "Persistência", "Praticidade"],
        weaknesses: ["Materialismo", "Teimosia"]
      },
      9: {
        element: "Fire",
        group: "East",
        personality: "Carismático e inteligente",
        strengths: ["Carisma", "Inteligência", "Paixão"],
        weaknesses: ["Impaciência", "Temperamento forte"]
      }
    };

    // Direções favoráveis para cada Kua
    this.favorableDirections = {
      1: { sheng_qi: "Norte", tian_yi: "Sul", nian_yan: "Leste", fu_wei: "Sudeste" },
      2: { sheng_qi: "Nordeste", tian_yi: "Oeste", nian_yan: "Noroeste", fu_wei: "Sudoeste" },
      3: { sheng_qi: "Leste", tian_yi: "Norte", nian_yan: "Sul", fu_wei: "Sudeste" },
      4: { sheng_qi: "Sudeste", tian_yi: "Leste", nian_yan: "Norte", fu_wei: "Sul" },
      6: { sheng_qi: "Oeste", tian_yi: "Nordeste", nian_yan: "Sudoeste", fu_wei: "Noroeste" },
      7: { sheng_qi: "Noroeste", tian_yi: "Oeste", nian_yan: "Nordeste", fu_wei: "Sudoeste" },
      8: { sheng_qi: "Sudoeste", tian_yi: "Noroeste", nian_yan: "Oeste", fu_wei: "Nordeste" },
      9: { sheng_qi: "Sul", tian_yi: "Sudeste", nian_yan: "Leste", fu_wei: "Norte" }
    };

    // Direções desfavoráveis para cada Kua
    this.unfavorableDirections = {
      1: { huo_hai: "Sudoeste", wu_gui: "Nordeste", liu_sha: "Noroeste", jue_ming: "Oeste" },
      2: { huo_hai: "Leste", wu_gui: "Sudeste", liu_sha: "Sul", jue_ming: "Norte" },
      3: { huo_hai: "Oeste", wu_gui: "Noroeste", liu_sha: "Nordeste", jue_ming: "Sudoeste" },
      4: { huo_hai: "Noroeste", wu_gui: "Oeste", liu_sha: "Sudoeste", jue_ming: "Nordeste" },
      6: { huo_hai: "Sudeste", wu_gui: "Sul", liu_sha: "Leste", jue_ming: "Norte" },
      7: { huo_hai: "Sul", wu_gui: "Sudeste", liu_sha: "Norte", jue_ming: "Leste" },
      8: { huo_hai: "Norte", wu_gui: "Leste", liu_sha: "Sudeste", jue_ming: "Sul" },
      9: { huo_hai: "Nordeste", wu_gui: "Sudoeste", liu_sha: "Noroeste", jue_ming: "Oeste" }
    };

    // Cores favoráveis por elemento
    this.elementColors = {
      Water: ["azul", "preto", "cinza escuro"],
      Wood: ["verde", "marrom", "bege"],
      Fire: ["vermelho", "laranja", "rosa"],
      Earth: ["amarelo", "bege", "marrom claro"],
      Metal: ["branco", "dourado", "prateado"]
    };
  }

  calculateKuaNumber(birthYear, gender) {
    let sum = 0;
    const yearStr = birthYear.toString();
    
    // Somar os dois últimos dígitos do ano
    for (let i = yearStr.length - 2; i < yearStr.length; i++) {
      if (i >= 0) {
        sum += parseInt(yearStr[i]);
      }
    }

    // Reduzir a um dígito
    while (sum > 9) {
      const sumStr = sum.toString();
      sum = 0;
      for (let digit of sumStr) {
        sum += parseInt(digit);
      }
    }

    let kuaNumber;
    if (gender.toLowerCase() === 'male') {
      kuaNumber = 11 - sum;
      if (kuaNumber > 9) kuaNumber -= 9;
      if (kuaNumber === 5) kuaNumber = 2; // Homens Kua 5 usam 2
    } else {
      kuaNumber = sum + 4;
      if (kuaNumber > 9) kuaNumber -= 9;
      if (kuaNumber === 5) kuaNumber = 8; // Mulheres Kua 5 usam 8
    }

    return kuaNumber;
  }

  calculateKuaAnalysis(birthYear, gender) {
    const kuaNumber = this.calculateKuaNumber(birthYear, gender);
    const characteristics = this.kuaCharacteristics[kuaNumber];
    const favorableDirections = this.favorableDirections[kuaNumber];
    const unfavorableDirections = this.unfavorableDirections[kuaNumber];

    // Recomendações Feng Shui
    const fengShuiRecommendations = this.generateFengShuiRecommendations(kuaNumber, characteristics);

    // Análise de compatibilidade
    const compatibility = this.generateCompatibilityAnalysis(kuaNumber, characteristics);

    return {
      birth_info: {
        birth_year: birthYear,
        gender: gender
      },
      kua_number: kuaNumber,
      characteristics: characteristics,
      favorable_directions: favorableDirections,
      unfavorable_directions: unfavorableDirections,
      feng_shui_recommendations: fengShuiRecommendations,
      compatibility: compatibility,
      life_guidance: this.generateLifeGuidance(kuaNumber, characteristics),
      house_recommendations: this.generateHouseRecommendations(kuaNumber)
    };
  }

  generateFengShuiRecommendations(kuaNumber, characteristics) {
    const element = characteristics.element;
    const colors = this.elementColors[element];
    const group = characteristics.group;

    return {
      colors: colors,
      materials: this.getMaterialsForElement(element),
      room_placement: this.getRoomPlacement(kuaNumber),
      decoration_tips: this.getDecorationTips(element),
      energy_enhancement: this.getEnergyEnhancement(group)
    };
  }

  getMaterialsForElement(element) {
    const materials = {
      Water: ["vidro", "cristal", "espelhos"],
      Wood: ["madeira", "bambu", "plantas"],
      Fire: ["cerâmica vermelha", "velas", "iluminação"],
      Earth: ["pedra", "cerâmica", "cristais"],
      Metal: ["metal", "aço inoxidável", "objetos metálicos"]
    };
    return materials[element] || [];
  }

  getRoomPlacement(kuaNumber) {
    const favorableDir = this.favorableDirections[kuaNumber];
    return {
      bedroom: `Posicione a cama na direção ${favorableDir.nian_yan} para relacionamentos`,
      office: `Posicione a mesa na direção ${favorableDir.sheng_qi} para sucesso`,
      living_room: `Organize o ambiente voltado para ${favorableDir.fu_wei} para estabilidade`,
      entrance: `Entrada principal voltada para ${favorableDir.tian_yi} para saúde`
    };
  }

  getDecorationTips(element) {
    const tips = {
      Water: ["Adicione fontes ou aquários", "Use formas onduladas", "Evite excesso de plantas"],
      Wood: ["Adicione plantas vivas", "Use móveis de madeira", "Decore com formas retangulares"],
      Fire: ["Use iluminação quente", "Adicione velas", "Decore com formas triangulares"],
      Earth: ["Use cristais e pedras", "Adicione cerâmica", "Decore com formas quadradas"],
      Metal: ["Use objetos metálicos", "Adicione espelhos", "Decore com formas circulares"]
    };
    return tips[element] || [];
  }

  getEnergyEnhancement(group) {
    if (group === "East") {
      return [
        "Fortaleça o lado leste da casa",
        "Use elementos Wood e Water",
        "Evite excesso de Metal no ambiente",
        "Mantenha o leste bem iluminado"
      ];
    } else {
      return [
        "Fortaleça o lado oeste da casa",
        "Use elementos Metal e Earth",
        "Evite excesso de Wood no ambiente",
        "Mantenha o oeste organizado"
      ];
    }
  }

  generateCompatibilityAnalysis(kuaNumber, characteristics) {
    const group = characteristics.group;
    const compatibleKuas = this.getCompatibleKuas(group);
    const relationshipAdvice = this.getRelationshipAdvice(characteristics);

    return {
      group: group,
      compatible_kuas: compatibleKuas,
      relationship_advice: relationshipAdvice,
      partnership_tips: this.getPartnershipTips(kuaNumber),
      family_harmony: this.getFamilyHarmonyTips(group)
    };
  }

  getCompatibleKuas(group) {
    if (group === "East") {
      return [1, 3, 4, 9];
    } else {
      return [2, 6, 7, 8];
    }
  }

  getRelationshipAdvice(characteristics) {
    const personality = characteristics.personality;
    const strengths = characteristics.strengths;
    const weaknesses = characteristics.weaknesses;

    return {
      personality_in_relationships: personality,
      relationship_strengths: strengths,
      areas_to_improve: weaknesses,
      communication_style: this.getCommunicationStyle(characteristics.element)
    };
  }

  getCommunicationStyle(element) {
    const styles = {
      Water: "Intuitivo e empático, prefere conversas profundas",
      Wood: "Direto e energético, gosta de debates construtivos",
      Fire: "Expressivo e caloroso, comunica com paixão",
      Earth: "Prático e confiável, prefere conversas claras",
      Metal: "Preciso e organizado, valoriza comunicação eficiente"
    };
    return styles[element] || "Equilibrado";
  }

  getPartnershipTips(kuaNumber) {
    const favorableDir = this.favorableDirections[kuaNumber];
    return [
      `Posicione a cama na direção ${favorableDir.nian_yan} para harmonia no relacionamento`,
      "Evite dormir em direções desfavoráveis",
      "Use cores favoráveis no quarto",
      "Mantenha o ambiente equilibrado com elementos compatíveis"
    ];
  }

  getFamilyHarmonyTips(group) {
    if (group === "East") {
      return [
        "Fortaleça a energia do leste da casa",
        "Use elementos naturais na decoração",
        "Mantenha plantas saudáveis no ambiente",
        "Evite excesso de elementos metálicos"
      ];
    } else {
      return [
        "Fortaleça a energia do oeste da casa",
        "Use elementos estruturados na decoração",
        "Mantenha o ambiente organizado",
        "Evite excesso de elementos de madeira"
      ];
    }
  }

  generateLifeGuidance(kuaNumber, characteristics) {
    const element = characteristics.element;
    const strengths = characteristics.strengths;
    const weaknesses = characteristics.weaknesses;

    return {
      life_purpose: this.getLifePurpose(element),
      career_guidance: this.getCareerGuidance(element, strengths),
      health_tips: this.getHealthTips(element),
      personal_development: this.getPersonalDevelopment(weaknesses),
      lucky_elements: this.getLuckyElements(element),
      best_timing: this.getBestTiming(kuaNumber)
    };
  }

  getLifePurpose(element) {
    const purposes = {
      Water: "Fluir e adaptar-se, trazendo sabedoria e intuição ao mundo",
      Wood: "Crescer e expandir, liderando mudanças positivas",
      Fire: "Iluminar e inspirar, trazendo paixão e energia",
      Earth: "Estabilizar e nutrir, criando bases sólidas",
      Metal: "Organizar e refinar, trazendo estrutura e precisão"
    };
    return purposes[element] || "Encontrar equilíbrio e harmonia";
  }

  getCareerGuidance(element, strengths) {
    const careers = {
      Water: ["Psicologia", "Arte", "Comunicação", "Pesquisa"],
      Wood: ["Educação", "Saúde", "Agricultura", "Liderança"],
      Fire: ["Marketing", "Entretenimento", "Vendas", "Tecnologia"],
      Earth: ["Construção", "Imobiliário", "Administração", "Finanças"],
      Metal: ["Engenharia", "Direito", "Medicina", "Organização"]
    };
    return careers[element] || ["Áreas diversas"];
  }

  getHealthTips(element) {
    const tips = {
      Water: ["Cuidar dos rins e sistema urinário", "Manter hidratação adequada", "Evitar excesso de sal"],
      Wood: ["Cuidar do fígado e vesícula", "Fazer exercícios regulares", "Evitar excesso de raiva"],
      Fire: ["Cuidar do coração e circulação", "Manter calma e equilíbrio", "Evitar excesso de estimulantes"],
      Earth: ["Cuidar do estômago e baço", "Manter alimentação regular", "Evitar excesso de preocupação"],
      Metal: ["Cuidar dos pulmões e intestino", "Manter respiração profunda", "Evitar excesso de tristeza"]
    };
    return tips[element] || ["Manter equilíbrio geral"];
  }

  getPersonalDevelopment(weaknesses) {
    return weaknesses.map(weakness => {
      const development = {
        "Indecisão": "Praticar tomada de decisões pequenas diariamente",
        "Sensibilidade excessiva": "Desenvolver resiliência emocional",
        "Teimosia": "Praticar flexibilidade e abertura a novas ideias",
        "Resistência a mudanças": "Abraçar pequenas mudanças gradualmente",
        "Impaciência": "Praticar meditação e mindfulness",
        "Impulsividade": "Desenvolver pausa reflexiva antes de agir",
        "Falta de foco": "Estabelecer metas claras e prioridades",
        "Rigidez": "Praticar adaptabilidade e espontaneidade",
        "Autoritarismo": "Desenvolver escuta ativa e empatia",
        "Superficialidade": "Buscar profundidade em relacionamentos e interesses",
        "Inconstância": "Desenvolver compromisso e persistência",
        "Materialismo": "Cultivar valores espirituais e relacionais",
        "Temperamento forte": "Praticar controle emocional e paciência"
      };
      return development[weakness] || `Trabalhar no desenvolvimento de ${weakness.toLowerCase()}`;
    });
  }

  getLuckyElements(element) {
    const cycles = {
      Water: ["Metal", "Water"],
      Wood: ["Water", "Wood"],
      Fire: ["Wood", "Fire"],
      Earth: ["Fire", "Earth"],
      Metal: ["Earth", "Metal"]
    };
    return cycles[element] || [element];
  }

  getBestTiming(kuaNumber) {
    const favorableDir = this.favorableDirections[kuaNumber];
    return {
      best_direction_for_important_decisions: favorableDir.sheng_qi,
      best_direction_for_health_matters: favorableDir.tian_yi,
      best_direction_for_relationships: favorableDir.nian_yan,
      best_direction_for_stability: favorableDir.fu_wei
    };
  }

  generateHouseRecommendations(kuaNumber) {
    const favorableDir = this.favorableDirections[kuaNumber];
    const unfavorableDir = this.unfavorableDirections[kuaNumber];

    return {
      ideal_house_facing: favorableDir.sheng_qi,
      bedroom_location: favorableDir.nian_yan,
      office_location: favorableDir.sheng_qi,
      kitchen_location: favorableDir.tian_yi,
      avoid_locations: Object.values(unfavorableDir),
      entrance_recommendations: `Entrada principal voltada para ${favorableDir.tian_yi}`,
      garden_placement: `Jardim no setor ${favorableDir.fu_wei} da propriedade`
    };
  }

  analyzeHouseCompatibility(houseFacingDirection, kuaNumber) {
    const favorableDirections = Object.values(this.favorableDirections[kuaNumber]);
    const unfavorableDirections = Object.values(this.unfavorableDirections[kuaNumber]);

    let compatibility = "Neutro";
    let advice = "Casa com energia neutra para seu Kua";

    if (favorableDirections.includes(houseFacingDirection)) {
      compatibility = "Excelente";
      advice = "Esta casa é muito favorável para você! A direção da casa está alinhada com suas direções favoráveis.";
    } else if (unfavorableDirections.includes(houseFacingDirection)) {
      compatibility = "Desafiador";
      advice = "Esta casa pode trazer desafios. Considere usar curas Feng Shui para harmonizar a energia.";
    }

    return {
      compatibility_level: compatibility,
      advice: advice,
      recommendations: this.getHouseHarmonizationTips(houseFacingDirection, kuaNumber),
      energy_assessment: this.assessHouseEnergy(houseFacingDirection, kuaNumber)
    };
  }

  getHouseHarmonizationTips(houseFacing, kuaNumber) {
    const favorableDir = this.favorableDirections[kuaNumber];
    
    return [
      `Posicione sua cama na direção ${favorableDir.nian_yan}`,
      `Use sua mesa de trabalho voltada para ${favorableDir.sheng_qi}`,
      `Passe mais tempo no setor ${favorableDir.fu_wei} da casa`,
      "Use cores e elementos favoráveis ao seu Kua",
      "Evite passar muito tempo em setores desfavoráveis"
    ];
  }

  assessHouseEnergy(houseFacing, kuaNumber) {
    const characteristics = this.kuaCharacteristics[kuaNumber];
    const favorableDirections = Object.values(this.favorableDirections[kuaNumber]);
    
    if (favorableDirections.includes(houseFacing)) {
      return {
        overall_energy: "Positiva",
        impact_on_health: "Benéfica",
        impact_on_career: "Favorável",
        impact_on_relationships: "Harmoniosa",
        long_term_effects: "Crescimento e prosperidade"
      };
    } else {
      return {
        overall_energy: "Desafiadora",
        impact_on_health: "Requer atenção",
        impact_on_career: "Pode haver obstáculos",
        impact_on_relationships: "Requer esforço extra",
        long_term_effects: "Necessita harmonização"
      };
    }
  }
}

// Função principal para uso no frontend
export function calculateKua(birthYear, gender) {
  const calculator = new KuaCalculator();
  return calculator.calculateKuaAnalysis(birthYear, gender);
}

// Função para análise de compatibilidade da casa
export function analyzeHouseCompatibility(houseFacingDirection, birthYear, gender) {
  const calculator = new KuaCalculator();
  const kuaNumber = calculator.calculateKuaNumber(birthYear, gender);
  return calculator.analyzeHouseCompatibility(houseFacingDirection, kuaNumber);
}


# Notas de Pesquisa - BaZi (Quatro Pilares do Destino)

## Fundamentos Básicos

### O que é BaZi
- **BaZi (八字)** = "Oito Caracteres" ou "Four Pillars of Destiny"
- Sistema de astrologia chinesa baseado na data e hora de nascimento
- Analisa Ano, Mês, Dia e Hora usando o calendário chinês (Ganzhi)
- Cada pilar tem 2 caracteres: Heavenly Stem (Tronco Celestial) + Earthly Branch (Ramo Terrestre)

### Componentes Principais

#### 1. Day Master (日主)
- O Heavenly Stem do Day Pillar
- Representa a essência da pessoa
- Elemento central para toda a análise

#### 2. Five Elements (Wu Xing - 五行)
- **Wood (木)** - Madeira
- **Fire (火)** - Fogo  
- **Earth (土)** - Terra
- **Metal (金)** - Metal
- **Water (水)** - Água

#### 3. Yin/Yang
- Cada elemento pode ser Yin ou Yang
- 10 Heavenly Stems total (5 elementos x 2 polaridades)

#### 4. Sexagenary Cycle (Jia Zi - 甲子)
- Ciclo de 60 combinações (10 stems x 12 branches)
- Base do calendário chinês tradicional

## Técnicas de Análise Avançadas

### 1. Chart Structure (格局 - Gé Jú)
- **Normal Structure (正格局)**: Estruturas convencionais
- **Special Structure (特殊格局)**: Configurações extremas

### 2. Strength Evaluation (扶抑)
- Determinar se Day Master é "forte" ou "fraco"
- Identificar elementos de suporte ou restrição

### 3. Seasonal Adjustment (调候)
- Influência da estação (Month Pillar)
- Ajustes para harmonizar energia sazonal

### 4. Energy Bridging (通关)
- Elementos que resolvem conflitos entre elementos opostos
- Promove fluxo suave de energia

### 5. Healing Prescription (病药)
- Identificar desequilíbrios (病 - doença)
- Prescrever remédios (药 - medicina)

## Aplicações Práticas

### Análise de Personalidade
- Traços inerentes baseados no Day Master
- Forças e fraquezas elementais

### Orientação de Carreira
- Profissões alinhadas com forças elementais
- Timing favorável para mudanças

### Compatibilidade de Relacionamentos
- Harmonia entre diferentes perfis BaZi
- Dinâmicas de interação

### Insights de Saúde
- Problemas potenciais por desequilíbrios elementais
- Recomendações preventivas

## Implementação Técnica Necessária

### 1. Conversão de Calendário
- Gregoriano → Chinês (Lunar/Solar)
- Cálculo preciso considerando fuso horário
- Tabelas de conversão Jia Zi

### 2. Cálculo dos Pilares
- **Year Pillar**: Baseado no ano chinês
- **Month Pillar**: Baseado no mês solar chinês
- **Day Pillar**: Contagem contínua desde época base
- **Hour Pillar**: Baseado no horário e Day Stem

### 3. Análise Elemental
- Força de cada elemento no chart
- Interações entre elementos (produção, destruição)
- Identificação de Useful God (用神)

### 4. Estrutura de Dados
```json
{
  "birth_info": {
    "datetime": "1990-05-15T14:30:00",
    "timezone": "UTC+8",
    "location": {"lat": 22.3, "lng": 114.2}
  },
  "four_pillars": {
    "year": {"stem": "Geng", "branch": "Wu", "element": "Metal", "polarity": "Yang"},
    "month": {"stem": "Xin", "branch": "Si", "element": "Metal", "polarity": "Yin"},
    "day": {"stem": "Ren", "branch": "Xu", "element": "Water", "polarity": "Yang"},
    "hour": {"stem": "Ding", "branch": "Wei", "element": "Fire", "polarity": "Yin"}
  },
  "day_master": {
    "element": "Water",
    "polarity": "Yang",
    "strength": "weak"
  },
  "element_analysis": {
    "wood": {"count": 0, "strength": "absent"},
    "fire": {"count": 1, "strength": "weak"},
    "earth": {"count": 2, "strength": "moderate"},
    "metal": {"count": 2, "strength": "strong"},
    "water": {"count": 1, "strength": "weak"}
  },
  "useful_god": "Wood",
  "chart_structure": "正官格",
  "recommendations": {
    "favorable_elements": ["Wood", "Water"],
    "unfavorable_elements": ["Earth", "Metal"],
    "career_guidance": "Creative fields, education, counseling",
    "health_focus": "Kidney and bladder care",
    "lucky_colors": ["Green", "Blue", "Black"],
    "lucky_directions": ["East", "North"]
  }
}
```

## Fontes de Referência
- Imperial Harvest BaZi Guide
- Joey Yap BaZi Calculator
- Master Tsai Chinese Astrology
- Sexagenary Cycle Wikipedia
- Chinese Calendar Conversion Tables

## Próximos Passos
1. Implementar algoritmo de conversão de calendário
2. Criar tabelas de Heavenly Stems e Earthly Branches
3. Desenvolver lógica de cálculo dos Four Pillars
4. Implementar análise de força elemental
5. Criar sistema de recomendações baseado em BaZi


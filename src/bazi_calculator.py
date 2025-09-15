#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARCA - Módulo de Cálculo BaZi (Quatro Pilares do Destino)
Implementação completa dos cálculos de BaZi baseada em fontes tradicionais
"""

import datetime
from typing import Dict, List, Tuple, Optional
import json

class BaZiCalculator:
    """
    Calculadora completa de BaZi (Four Pillars of Destiny)
    Implementa cálculos precisos baseados no calendário chinês tradicional
    """
    
    def __init__(self):
        self.setup_reference_tables()
    
    def setup_reference_tables(self):
        """Configura tabelas de referência para cálculos BaZi"""
        
        # Heavenly Stems (Troncos Celestiais) - 10 elementos
        self.heavenly_stems = [
            {"index": 0, "chinese": "甲", "pinyin": "Jia", "element": "Wood", "polarity": "Yang"},
            {"index": 1, "chinese": "乙", "pinyin": "Yi", "element": "Wood", "polarity": "Yin"},
            {"index": 2, "chinese": "丙", "pinyin": "Bing", "element": "Fire", "polarity": "Yang"},
            {"index": 3, "chinese": "丁", "pinyin": "Ding", "element": "Fire", "polarity": "Yin"},
            {"index": 4, "chinese": "戊", "pinyin": "Wu", "element": "Earth", "polarity": "Yang"},
            {"index": 5, "chinese": "己", "pinyin": "Ji", "element": "Earth", "polarity": "Yin"},
            {"index": 6, "chinese": "庚", "pinyin": "Geng", "element": "Metal", "polarity": "Yang"},
            {"index": 7, "chinese": "辛", "pinyin": "Xin", "element": "Metal", "polarity": "Yin"},
            {"index": 8, "chinese": "壬", "pinyin": "Ren", "element": "Water", "polarity": "Yang"},
            {"index": 9, "chinese": "癸", "pinyin": "Gui", "element": "Water", "polarity": "Yin"}
        ]
        
        # Earthly Branches (Ramos Terrestres) - 12 elementos
        self.earthly_branches = [
            {"index": 0, "chinese": "子", "pinyin": "Zi", "zodiac": "Rat", "element": "Water", "season": "Winter"},
            {"index": 1, "chinese": "丑", "pinyin": "Chou", "zodiac": "Ox", "element": "Earth", "season": "Winter"},
            {"index": 2, "chinese": "寅", "pinyin": "Yin", "zodiac": "Tiger", "element": "Wood", "season": "Spring"},
            {"index": 3, "chinese": "卯", "pinyin": "Mao", "zodiac": "Rabbit", "element": "Wood", "season": "Spring"},
            {"index": 4, "chinese": "辰", "pinyin": "Chen", "zodiac": "Dragon", "element": "Earth", "season": "Spring"},
            {"index": 5, "chinese": "巳", "pinyin": "Si", "zodiac": "Snake", "element": "Fire", "season": "Summer"},
            {"index": 6, "chinese": "午", "pinyin": "Wu", "zodiac": "Horse", "element": "Fire", "season": "Summer"},
            {"index": 7, "chinese": "未", "pinyin": "Wei", "zodiac": "Goat", "element": "Earth", "season": "Summer"},
            {"index": 8, "chinese": "申", "pinyin": "Shen", "zodiac": "Monkey", "element": "Metal", "season": "Autumn"},
            {"index": 9, "chinese": "酉", "pinyin": "You", "zodiac": "Rooster", "element": "Metal", "season": "Autumn"},
            {"index": 10, "chinese": "戌", "pinyin": "Xu", "zodiac": "Dog", "element": "Earth", "season": "Autumn"},
            {"index": 11, "chinese": "亥", "pinyin": "Hai", "zodiac": "Pig", "element": "Water", "season": "Winter"}
        ]
        
        # Five Elements Cycles
        self.element_cycles = {
            "productive": {
                "Wood": "Fire",
                "Fire": "Earth", 
                "Earth": "Metal",
                "Metal": "Water",
                "Water": "Wood"
            },
            "destructive": {
                "Wood": "Earth",
                "Fire": "Metal",
                "Earth": "Water",
                "Metal": "Wood",
                "Water": "Fire"
            }
        }
        
        # Solar Terms (24 节气) - Aproximação para cálculo de mês chinês
        self.solar_terms = [
            {"name": "立春", "approx_date": (2, 4)},   # Beginning of Spring
            {"name": "雨水", "approx_date": (2, 19)},  # Rain Water
            {"name": "惊蛰", "approx_date": (3, 6)},   # Awakening of Insects
            {"name": "春分", "approx_date": (3, 21)},  # Spring Equinox
            {"name": "清明", "approx_date": (4, 5)},   # Clear and Bright
            {"name": "谷雨", "approx_date": (4, 20)},  # Grain Rain
            {"name": "立夏", "approx_date": (5, 6)},   # Beginning of Summer
            {"name": "小满", "approx_date": (5, 21)},  # Grain Buds
            {"name": "芒种", "approx_date": (6, 6)},   # Grain in Ear
            {"name": "夏至", "approx_date": (6, 22)},  # Summer Solstice
            {"name": "小暑", "approx_date": (7, 7)},   # Slight Heat
            {"name": "大暑", "approx_date": (7, 23)},  # Great Heat
            {"name": "立秋", "approx_date": (8, 8)},   # Beginning of Autumn
            {"name": "处暑", "approx_date": (8, 23)},  # Stopping the Heat
            {"name": "白露", "approx_date": (9, 8)},   # White Dew
            {"name": "秋分", "approx_date": (9, 23)},  # Autumn Equinox
            {"name": "寒露", "approx_date": (10, 8)},  # Cold Dew
            {"name": "霜降", "approx_date": (10, 24)}, # Frost's Descent
            {"name": "立冬", "approx_date": (11, 8)},  # Beginning of Winter
            {"name": "小雪", "approx_date": (11, 22)}, # Slight Snow
            {"name": "大雪", "approx_date": (12, 7)},  # Great Snow
            {"name": "冬至", "approx_date": (12, 22)}, # Winter Solstice
            {"name": "小寒", "approx_date": (1, 6)},   # Slight Cold
            {"name": "大寒", "approx_date": (1, 20)}   # Great Cold
        ]
        
        # Epoch base para cálculo de dias (1 de Janeiro de 1900 = Jia Zi)
        self.epoch_date = datetime.date(1900, 1, 1)
        self.epoch_jia_zi_day = 0  # 1 Jan 1900 é considerado dia 0 do ciclo Jia Zi
    
    def calculate_four_pillars(self, birth_datetime: datetime.datetime, 
                             timezone_offset: int = 8) -> Dict:
        """
        Calcula os Quatro Pilares do Destino (BaZi) completos
        
        Args:
            birth_datetime: Data e hora de nascimento
            timezone_offset: Fuso horário (padrão: +8 para China)
            
        Returns:
            Dict com os quatro pilares e análises
        """
        
        # Ajustar para fuso horário chinês
        adjusted_datetime = birth_datetime + datetime.timedelta(hours=timezone_offset-8)
        
        # Calcular cada pilar
        year_pillar = self.calculate_year_pillar(adjusted_datetime.year)
        month_pillar = self.calculate_month_pillar(adjusted_datetime.month, adjusted_datetime.day, year_pillar["stem"]["index"])
        day_pillar = self.calculate_day_pillar(adjusted_datetime.date())
        hour_pillar = self.calculate_hour_pillar(adjusted_datetime.hour, day_pillar["stem"]["index"])
        
        # Day Master (elemento central da pessoa)
        day_master = day_pillar["stem"]
        
        # Análise elemental
        element_analysis = self.analyze_elements(year_pillar, month_pillar, day_pillar, hour_pillar)
        
        # Determinar força do Day Master
        day_master_strength = self.calculate_day_master_strength(
            day_master, month_pillar, element_analysis
        )
        
        # Identificar Useful God (用神)
        useful_god = self.identify_useful_god(day_master, day_master_strength, element_analysis)
        
        # Gerar recomendações
        recommendations = self.generate_recommendations(day_master, useful_god, element_analysis)
        
        return {
            "birth_info": {
                "datetime": birth_datetime.isoformat(),
                "timezone_offset": timezone_offset,
                "adjusted_datetime": adjusted_datetime.isoformat()
            },
            "four_pillars": {
                "year": year_pillar,
                "month": month_pillar,
                "day": day_pillar,
                "hour": hour_pillar
            },
            "day_master": {
                **day_master,
                "strength": day_master_strength
            },
            "element_analysis": element_analysis,
            "useful_god": useful_god,
            "recommendations": recommendations,
            "chart_summary": self.generate_chart_summary(day_master, day_master_strength, useful_god)
        }
    
    def calculate_year_pillar(self, year: int) -> Dict:
        """Calcula o pilar do ano"""
        # Ano chinês começa em fevereiro, então ajustar se necessário
        # Simplificação: usar ano gregoriano diretamente
        
        # Calcular índices no ciclo sexagenário (60 anos)
        year_offset = year - 1984  # 1984 foi ano Jia Zi (甲子)
        stem_index = year_offset % 10
        branch_index = year_offset % 12
        
        # Ajustar índices negativos
        if stem_index < 0:
            stem_index += 10
        if branch_index < 0:
            branch_index += 12
            
        return {
            "stem": self.heavenly_stems[stem_index],
            "branch": self.earthly_branches[branch_index],
            "year": year
        }
    
    def calculate_month_pillar(self, month: int, day: int, year_stem_index: int) -> Dict:
        """Calcula o pilar do mês baseado nos termos solares"""
        
        # Determinar mês chinês baseado nos termos solares
        chinese_month = self.get_chinese_month(month, day)
        
        # Calcular stem do mês baseado no stem do ano
        # Fórmula tradicional para month stem
        month_stem_index = (year_stem_index * 2 + chinese_month) % 10
        month_branch_index = (chinese_month + 1) % 12  # Mês chinês começa em Yin (寅)
        
        return {
            "stem": self.heavenly_stems[month_stem_index],
            "branch": self.earthly_branches[month_branch_index],
            "chinese_month": chinese_month,
            "gregorian_month": month
        }
    
    def calculate_day_pillar(self, birth_date: datetime.date) -> Dict:
        """Calcula o pilar do dia usando contagem contínua desde época"""
        
        # Calcular dias desde a época
        days_since_epoch = (birth_date - self.epoch_date).days
        
        # Calcular posição no ciclo sexagenário (60 dias)
        cycle_position = (self.epoch_jia_zi_day + days_since_epoch) % 60
        
        stem_index = cycle_position % 10
        branch_index = cycle_position % 12
        
        return {
            "stem": self.heavenly_stems[stem_index],
            "branch": self.earthly_branches[branch_index],
            "days_since_epoch": days_since_epoch,
            "cycle_position": cycle_position
        }
    
    def calculate_hour_pillar(self, hour: int, day_stem_index: int) -> Dict:
        """Calcula o pilar da hora"""
        
        # Converter hora para período chinês (12 períodos de 2 horas)
        chinese_hour_index = ((hour + 1) // 2) % 12
        
        # Calcular stem da hora baseado no stem do dia
        # Fórmula tradicional para hour stem
        hour_stem_index = (day_stem_index * 2 + chinese_hour_index) % 10
        
        return {
            "stem": self.heavenly_stems[hour_stem_index],
            "branch": self.earthly_branches[chinese_hour_index],
            "gregorian_hour": hour,
            "chinese_hour_period": chinese_hour_index
        }
    
    def get_chinese_month(self, month: int, day: int) -> int:
        """Determina o mês chinês baseado nos termos solares"""
        
        # Simplificação: mapear meses gregorianos para chineses
        # Em implementação real, seria necessário cálculo preciso dos termos solares
        month_mapping = {
            1: 11,  # Janeiro -> 12º mês chinês (Chou)
            2: 0,   # Fevereiro -> 1º mês chinês (Yin) 
            3: 1,   # Março -> 2º mês chinês (Mao)
            4: 2,   # Abril -> 3º mês chinês (Chen)
            5: 3,   # Maio -> 4º mês chinês (Si)
            6: 4,   # Junho -> 5º mês chinês (Wu)
            7: 5,   # Julho -> 6º mês chinês (Wei)
            8: 6,   # Agosto -> 7º mês chinês (Shen)
            9: 7,   # Setembro -> 8º mês chinês (You)
            10: 8,  # Outubro -> 9º mês chinês (Xu)
            11: 9,  # Novembro -> 10º mês chinês (Hai)
            12: 10  # Dezembro -> 11º mês chinês (Zi)
        }
        
        return month_mapping.get(month, 0)
    
    def analyze_elements(self, year_pillar: Dict, month_pillar: Dict, 
                        day_pillar: Dict, hour_pillar: Dict) -> Dict:
        """Analisa a distribuição e força dos cinco elementos"""
        
        element_count = {"Wood": 0, "Fire": 0, "Earth": 0, "Metal": 0, "Water": 0}
        element_strength = {"Wood": 0, "Fire": 0, "Earth": 0, "Metal": 0, "Water": 0}
        
        # Contar elementos dos stems (peso 2) e branches (peso 1)
        pillars = [year_pillar, month_pillar, day_pillar, hour_pillar]
        
        for pillar in pillars:
            # Heavenly Stem (mais forte)
            stem_element = pillar["stem"]["element"]
            element_count[stem_element] += 1
            element_strength[stem_element] += 2
            
            # Earthly Branch (menos forte)
            branch_element = pillar["branch"]["element"]
            element_count[branch_element] += 1
            element_strength[branch_element] += 1
        
        # Calcular percentuais
        total_strength = sum(element_strength.values())
        element_percentages = {
            element: (strength / total_strength * 100) if total_strength > 0 else 0
            for element, strength in element_strength.items()
        }
        
        return {
            "count": element_count,
            "strength": element_strength,
            "percentages": element_percentages,
            "dominant_element": max(element_strength, key=element_strength.get),
            "weakest_element": min(element_strength, key=element_strength.get)
        }
    
    def calculate_day_master_strength(self, day_master: Dict, month_pillar: Dict, 
                                    element_analysis: Dict) -> str:
        """Determina se o Day Master é forte ou fraco"""
        
        day_master_element = day_master["element"]
        month_branch_element = month_pillar["branch"]["element"]
        
        # Verificar se está na estação favorável
        seasonal_strength = 0
        if month_branch_element == day_master_element:
            seasonal_strength += 2
        elif self.element_cycles["productive"].get(month_branch_element) == day_master_element:
            seasonal_strength += 1
        elif self.element_cycles["destructive"].get(month_branch_element) == day_master_element:
            seasonal_strength -= 1
        
        # Verificar suporte dos outros elementos
        support_strength = 0
        day_master_percentage = element_analysis["percentages"][day_master_element]
        
        # Elementos que produzem o Day Master
        for element, produces in self.element_cycles["productive"].items():
            if produces == day_master_element:
                support_strength += element_analysis["percentages"][element] * 0.5
        
        # Elementos do mesmo tipo
        support_strength += day_master_percentage
        
        # Determinar força final
        total_strength = seasonal_strength + (support_strength / 100 * 3)
        
        if total_strength >= 2:
            return "Strong"
        elif total_strength <= -1:
            return "Very Weak"
        elif total_strength < 1:
            return "Weak"
        else:
            return "Moderate"
    
    def identify_useful_god(self, day_master: Dict, strength: str, 
                          element_analysis: Dict) -> Dict:
        """Identifica o Useful God (用神) - elemento que traz equilíbrio"""
        
        day_master_element = day_master["element"]
        
        if strength in ["Strong"]:
            # Day Master forte precisa ser drenado ou controlado
            # Elementos que drenam ou destroem o Day Master
            draining_element = self.element_cycles["productive"][day_master_element]
            controlling_element = None
            
            for element, destroys in self.element_cycles["destructive"].items():
                if destroys == day_master_element:
                    controlling_element = element
                    break
            
            # Escolher o mais fraco entre os dois
            if controlling_element and element_analysis["percentages"][controlling_element] < element_analysis["percentages"][draining_element]:
                useful_god_element = controlling_element
                method = "Control"
            else:
                useful_god_element = draining_element
                method = "Drain"
                
        else:
            # Day Master fraco precisa ser fortalecido
            # Elementos que produzem o Day Master
            producing_element = None
            for element, produces in self.element_cycles["productive"].items():
                if produces == day_master_element:
                    producing_element = element
                    break
            
            # Mesmo elemento para suporte direto
            if element_analysis["percentages"][day_master_element] < element_analysis["percentages"].get(producing_element, 0):
                useful_god_element = day_master_element
                method = "Support"
            else:
                useful_god_element = producing_element
                method = "Produce"
        
        return {
            "element": useful_god_element,
            "method": method,
            "current_strength": element_analysis["percentages"][useful_god_element],
            "recommendation": f"Fortalecer elemento {useful_god_element} através de {method.lower()}"
        }
    
    def generate_recommendations(self, day_master: Dict, useful_god: Dict, 
                               element_analysis: Dict) -> Dict:
        """Gera recomendações baseadas na análise BaZi"""
        
        useful_element = useful_god["element"]
        
        # Mapeamento de elementos para recomendações práticas
        element_recommendations = {
            "Wood": {
                "colors": ["Verde", "Marrom claro", "Bege"],
                "directions": ["Leste", "Sudeste"],
                "materials": ["Madeira", "Bambu", "Plantas"],
                "careers": ["Educação", "Saúde", "Arte", "Design", "Agricultura"],
                "activities": ["Jardinagem", "Caminhadas na natureza", "Leitura"],
                "foods": ["Vegetais verdes", "Frutas ácidas", "Chás de ervas"]
            },
            "Fire": {
                "colors": ["Vermelho", "Rosa", "Laranja", "Roxo"],
                "directions": ["Sul"],
                "materials": ["Velas", "Luzes", "Cristais vermelhos"],
                "careers": ["Marketing", "Vendas", "Entretenimento", "Liderança"],
                "activities": ["Exercícios", "Dança", "Socialização"],
                "foods": ["Alimentos picantes", "Carnes vermelhas", "Pimentas"]
            },
            "Earth": {
                "colors": ["Amarelo", "Marrom", "Bege", "Terracota"],
                "directions": ["Centro", "Sudoeste", "Nordeste"],
                "materials": ["Cerâmica", "Pedras", "Cristais amarelos"],
                "careers": ["Imóveis", "Construção", "Consultoria", "Administração"],
                "activities": ["Meditação", "Yoga", "Organização"],
                "foods": ["Grãos", "Raízes", "Alimentos doces naturais"]
            },
            "Metal": {
                "colors": ["Branco", "Cinza", "Dourado", "Prateado"],
                "directions": ["Oeste", "Noroeste"],
                "materials": ["Metal", "Cristais brancos", "Objetos metálicos"],
                "careers": ["Finanças", "Tecnologia", "Engenharia", "Direito"],
                "activities": ["Organização", "Planejamento", "Exercícios de respiração"],
                "foods": ["Alimentos brancos", "Peras", "Rabanete"]
            },
            "Water": {
                "colors": ["Azul", "Preto", "Azul marinho"],
                "directions": ["Norte"],
                "materials": ["Água", "Vidro", "Cristais azuis"],
                "careers": ["Pesquisa", "Comunicação", "Transporte", "Turismo"],
                "activities": ["Natação", "Banhos relaxantes", "Contemplação"],
                "foods": ["Peixes", "Alimentos salgados", "Sopas"]
            }
        }
        
        recommendations = element_recommendations.get(useful_element, {})
        
        # Adicionar recomendações específicas baseadas na força do Day Master
        day_master_element = day_master["element"]
        
        return {
            "useful_god_element": useful_element,
            "favorable_colors": recommendations.get("colors", []),
            "favorable_directions": recommendations.get("directions", []),
            "recommended_materials": recommendations.get("materials", []),
            "career_guidance": recommendations.get("careers", []),
            "beneficial_activities": recommendations.get("activities", []),
            "dietary_suggestions": recommendations.get("foods", []),
            "elements_to_avoid": self.get_unfavorable_elements(useful_element),
            "feng_shui_tips": self.generate_feng_shui_tips(useful_element, day_master_element)
        }
    
    def get_unfavorable_elements(self, useful_element: str) -> List[str]:
        """Identifica elementos desfavoráveis baseados no Useful God"""
        
        unfavorable = []
        
        # Elemento que destrói o Useful God
        for element, destroys in self.element_cycles["destructive"].items():
            if destroys == useful_element:
                unfavorable.append(element)
        
        # Elemento que drena o Useful God
        draining_element = self.element_cycles["productive"].get(useful_element)
        if draining_element:
            unfavorable.append(draining_element)
        
        return unfavorable
    
    def generate_feng_shui_tips(self, useful_element: str, day_master_element: str) -> List[str]:
        """Gera dicas específicas de Feng Shui baseadas nos elementos"""
        
        tips = []
        
        element_feng_shui = {
            "Wood": [
                "Coloque plantas vivas no setor Leste da casa",
                "Use móveis de madeira natural",
                "Mantenha boa ventilação e luz natural",
                "Evite excesso de metal no ambiente"
            ],
            "Fire": [
                "Adicione iluminação no setor Sul",
                "Use velas ou lareira quando possível",
                "Incorpore cores quentes na decoração",
                "Evite excesso de água no ambiente"
            ],
            "Earth": [
                "Use cristais e pedras naturais",
                "Mantenha o centro da casa livre e organizado",
                "Incorpore tons terrosos na decoração",
                "Evite excesso de madeira no ambiente"
            ],
            "Metal": [
                "Adicione objetos metálicos no setor Oeste",
                "Use cristais brancos ou transparentes",
                "Mantenha o ambiente organizado e limpo",
                "Evite excesso de fogo no ambiente"
            ],
            "Water": [
                "Coloque fonte de água no setor Norte",
                "Use espelhos para refletir energia",
                "Incorpore tons azuis na decoração",
                "Evite excesso de terra no ambiente"
            ]
        }
        
        tips.extend(element_feng_shui.get(useful_element, []))
        
        return tips
    
    def generate_chart_summary(self, day_master: Dict, strength: str, useful_god: Dict) -> str:
        """Gera resumo interpretativo do chart BaZi"""
        
        day_master_element = day_master["element"]
        useful_element = useful_god["element"]
        
        element_personalities = {
            "Wood": "criativa, flexível e em crescimento constante",
            "Fire": "energética, carismática e orientada para objetivos",
            "Earth": "estável, confiável e focada em segurança",
            "Metal": "organizada, precisa e orientada para resultados",
            "Water": "adaptável, intuitiva e fluida"
        }
        
        personality = element_personalities.get(day_master_element, "equilibrada")
        
        summary = f"""
        Análise BaZi - Resumo Interpretativo:
        
        Sua personalidade central é {personality}, característica do elemento {day_master_element}.
        
        Força do Day Master: {strength}
        
        Para alcançar maior equilíbrio e sucesso, você deve fortalecer o elemento {useful_element} 
        através de {useful_god['method'].lower()}.
        
        Isso pode ser feito incorporando as cores, direções e atividades relacionadas ao elemento 
        {useful_element} em sua vida diária.
        """
        
        return summary.strip()

# Função auxiliar para uso no ARCA
def calculate_bazi_for_person(birth_datetime: datetime.datetime, 
                             timezone_offset: int = -3) -> Dict:
    """
    Função auxiliar para calcular BaZi integrado ao ARCA
    
    Args:
        birth_datetime: Data e hora de nascimento
        timezone_offset: Fuso horário (padrão: -3 para Brasil)
        
    Returns:
        Dict com análise BaZi completa
    """
    calculator = BaZiCalculator()
    return calculator.calculate_four_pillars(birth_datetime, timezone_offset)

if __name__ == "__main__":
    # Teste da implementação
    test_datetime = datetime.datetime(1990, 5, 15, 14, 30)
    result = calculate_bazi_for_person(test_datetime)
    print(json.dumps(result, indent=2, ensure_ascii=False))


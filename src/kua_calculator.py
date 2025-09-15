#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARCA - Módulo de Cálculo do Número Kua e Ba Zhai (Oito Casas)
Implementação completa dos cálculos de Kua e direções favoráveis
"""

import datetime
from typing import Dict, List, Tuple
import json

class KuaCalculator:
    """
    Calculadora do Número Kua e sistema Ba Zhai (Oito Casas)
    Determina direções favoráveis e desfavoráveis para cada pessoa
    """
    
    def __init__(self):
        self.setup_kua_data()
    
    def setup_kua_data(self):
        """Configura dados de referência para cálculos Kua"""
        
        # Características dos números Kua
        self.kua_characteristics = {
            1: {
                "element": "Water",
                "trigram": "Kan",
                "chinese": "坎",
                "group": "East",
                "personality": "Adaptável, intuitivo, comunicativo",
                "strengths": ["Flexibilidade", "Intuição", "Comunicação"],
                "weaknesses": ["Indecisão", "Tendência ao isolamento"],
                "body_part": "Ouvidos, rins, sistema reprodutivo"
            },
            2: {
                "element": "Earth",
                "trigram": "Kun",
                "chinese": "坤",
                "group": "West", 
                "personality": "Maternal, receptivo, paciente",
                "strengths": ["Paciência", "Cuidado", "Estabilidade"],
                "weaknesses": ["Passividade", "Resistência a mudanças"],
                "body_part": "Abdômen, sistema digestivo"
            },
            3: {
                "element": "Wood",
                "trigram": "Zhen",
                "chinese": "震",
                "group": "East",
                "personality": "Dinâmico, impulsivo, inovador",
                "strengths": ["Energia", "Liderança", "Inovação"],
                "weaknesses": ["Impaciência", "Impulsividade"],
                "body_part": "Pés, fígado, sistema nervoso"
            },
            4: {
                "element": "Wood",
                "trigram": "Xun",
                "chinese": "巽",
                "group": "East",
                "personality": "Gentil, persistente, criativo",
                "strengths": ["Criatividade", "Persistência", "Diplomacia"],
                "weaknesses": ["Indecisão", "Falta de confiança"],
                "body_part": "Quadris, vesícula biliar"
            },
            6: {
                "element": "Metal",
                "trigram": "Qian",
                "chinese": "乾",
                "group": "West",
                "personality": "Autoritário, organizado, ambicioso",
                "strengths": ["Liderança", "Organização", "Determinação"],
                "weaknesses": ["Rigidez", "Autoritarismo"],
                "body_part": "Cabeça, pulmões"
            },
            7: {
                "element": "Metal",
                "trigram": "Dui",
                "chinese": "兑",
                "group": "West",
                "personality": "Comunicativo, alegre, persuasivo",
                "strengths": ["Comunicação", "Alegria", "Persuasão"],
                "weaknesses": ["Superficialidade", "Falta de foco"],
                "body_part": "Boca, pulmões, sistema respiratório"
            },
            8: {
                "element": "Earth",
                "trigram": "Gen",
                "chinese": "艮",
                "group": "West",
                "personality": "Estável, contemplativo, determinado",
                "strengths": ["Estabilidade", "Determinação", "Contemplação"],
                "weaknesses": ["Teimosia", "Isolamento"],
                "body_part": "Mãos, estômago, baço"
            },
            9: {
                "element": "Fire",
                "trigram": "Li",
                "chinese": "离",
                "group": "East",
                "personality": "Brilhante, carismático, inteligente",
                "strengths": ["Inteligência", "Carisma", "Clareza"],
                "weaknesses": ["Impaciência", "Orgulho"],
                "body_part": "Olhos, coração, sistema circulatório"
            }
        }
        
        # Direções favoráveis para cada Kua
        self.kua_directions = {
            1: {
                "sheng_qi": "Southeast",      # Gerando Qi - Melhor direção
                "tian_yi": "East",           # Médico Celestial - Saúde
                "yan_nian": "South",         # Longevidade - Relacionamentos
                "fu_wei": "North",           # Posição Sentada - Estabilidade
                "huo_hai": "West",           # Desastre - Evitar
                "wu_gui": "Northeast",       # Cinco Fantasmas - Evitar
                "liu_sha": "Southwest",      # Seis Mortes - Evitar
                "jue_ming": "Northwest"      # Morte Total - Evitar
            },
            2: {
                "sheng_qi": "Northeast",
                "tian_yi": "West", 
                "yan_nian": "Northwest",
                "fu_wei": "Southwest",
                "huo_hai": "East",
                "wu_gui": "Southeast",
                "liu_sha": "South",
                "jue_ming": "North"
            },
            3: {
                "sheng_qi": "South",
                "tian_yi": "North",
                "yan_nian": "Southeast", 
                "fu_wei": "East",
                "huo_hai": "Southwest",
                "wu_gui": "Northwest",
                "liu_sha": "Northeast",
                "jue_ming": "West"
            },
            4: {
                "sheng_qi": "North",
                "tian_yi": "South",
                "yan_nian": "East",
                "fu_wei": "Southeast",
                "huo_hai": "Northeast",
                "wu_gui": "West",
                "liu_sha": "Northwest",
                "jue_ming": "Southwest"
            },
            6: {
                "sheng_qi": "West",
                "tian_yi": "Northeast",
                "yan_nian": "Southwest",
                "fu_wei": "Northwest",
                "huo_hai": "Southeast",
                "wu_gui": "South",
                "liu_sha": "East",
                "jue_ming": "North"
            },
            7: {
                "sheng_qi": "Northwest",
                "tian_yi": "Southwest",
                "yan_nian": "Northeast",
                "fu_wei": "West",
                "huo_hai": "North",
                "wu_gui": "East",
                "liu_sha": "Southeast",
                "jue_ming": "South"
            },
            8: {
                "sheng_qi": "Southwest",
                "tian_yi": "Northwest",
                "yan_nian": "West",
                "fu_wei": "Northeast",
                "huo_hai": "South",
                "wu_gui": "North",
                "liu_sha": "Southeast",
                "jue_ming": "East"
            },
            9: {
                "sheng_qi": "East",
                "tian_yi": "Southeast",
                "yan_nian": "North",
                "fu_wei": "South",
                "huo_hai": "Northwest",
                "wu_gui": "Southwest",
                "liu_sha": "West",
                "jue_ming": "Northeast"
            }
        }
        
        # Significados das direções
        self.direction_meanings = {
            "sheng_qi": {
                "name": "Gerando Qi",
                "chinese": "生气",
                "description": "Melhor direção para sucesso, prosperidade e crescimento",
                "use_for": ["Porta principal", "Mesa de trabalho", "Cama (cabeça)"],
                "benefits": ["Sucesso nos negócios", "Prosperidade", "Boa sorte geral"]
            },
            "tian_yi": {
                "name": "Médico Celestial", 
                "chinese": "天医",
                "description": "Direção para saúde, cura e bem-estar",
                "use_for": ["Quarto", "Cozinha", "Área de exercícios"],
                "benefits": ["Boa saúde", "Recuperação de doenças", "Vitalidade"]
            },
            "yan_nian": {
                "name": "Longevidade",
                "chinese": "延年", 
                "description": "Direção para relacionamentos e harmonia familiar",
                "use_for": ["Sala de estar", "Quarto do casal", "Área social"],
                "benefits": ["Relacionamentos harmoniosos", "Vida longa", "Paz familiar"]
            },
            "fu_wei": {
                "name": "Posição Sentada",
                "chinese": "伏位",
                "description": "Direção para estabilidade e desenvolvimento pessoal",
                "use_for": ["Estudo", "Meditação", "Área de leitura"],
                "benefits": ["Estabilidade", "Crescimento pessoal", "Clareza mental"]
            },
            "huo_hai": {
                "name": "Desastre",
                "chinese": "祸害",
                "description": "Direção que traz pequenos problemas e irritações",
                "avoid_for": ["Porta principal", "Cama", "Mesa de trabalho"],
                "negative_effects": ["Pequenos acidentes", "Irritações", "Mal-entendidos"]
            },
            "wu_gui": {
                "name": "Cinco Fantasmas",
                "chinese": "五鬼",
                "description": "Direção que traz conflitos e problemas relacionais",
                "avoid_for": ["Quarto", "Sala de estar", "Cozinha"],
                "negative_effects": ["Conflitos", "Roubo", "Problemas legais"]
            },
            "liu_sha": {
                "name": "Seis Mortes",
                "chinese": "六煞",
                "description": "Direção que afeta saúde e relacionamentos",
                "avoid_for": ["Cama", "Cozinha", "Banheiro"],
                "negative_effects": ["Problemas de saúde", "Relacionamentos ruins", "Escândalos"]
            },
            "jue_ming": {
                "name": "Morte Total",
                "chinese": "绝命",
                "description": "Pior direção, deve ser evitada completamente",
                "avoid_for": ["Qualquer uso importante"],
                "negative_effects": ["Grandes perdas", "Acidentes graves", "Falência"]
            }
        }
    
    def calculate_kua_number(self, birth_year: int, gender: str) -> int:
        """
        Calcula o número Kua baseado no ano de nascimento e gênero
        
        Args:
            birth_year: Ano de nascimento
            gender: 'male' ou 'female'
            
        Returns:
            Número Kua (1-9, exceto 5)
        """
        
        # Somar os dois últimos dígitos do ano
        last_two_digits = birth_year % 100
        digit_sum = (last_two_digits // 10) + (last_two_digits % 10)
        
        # Se a soma for >= 10, somar novamente
        while digit_sum >= 10:
            digit_sum = (digit_sum // 10) + (digit_sum % 10)
        
        # Aplicar fórmula baseada no gênero
        if gender.lower() == 'male':
            kua = 10 - digit_sum
            # Casos especiais para homens
            if kua == 5:
                kua = 2
        else:  # female
            kua = 5 + digit_sum
            # Se resultado >= 10, subtrair 9
            if kua >= 10:
                kua -= 9
            # Casos especiais para mulheres  
            if kua == 5:
                kua = 8
        
        return kua
    
    def get_kua_analysis(self, birth_year: int, gender: str) -> Dict:
        """
        Análise completa do Kua incluindo características e direções
        
        Args:
            birth_year: Ano de nascimento
            gender: 'male' ou 'female'
            
        Returns:
            Dict com análise completa do Kua
        """
        
        kua_number = self.calculate_kua_number(birth_year, gender)
        characteristics = self.kua_characteristics[kua_number]
        directions = self.kua_directions[kua_number]
        
        # Separar direções favoráveis e desfavoráveis
        favorable_directions = {
            "sheng_qi": directions["sheng_qi"],
            "tian_yi": directions["tian_yi"], 
            "yan_nian": directions["yan_nian"],
            "fu_wei": directions["fu_wei"]
        }
        
        unfavorable_directions = {
            "huo_hai": directions["huo_hai"],
            "wu_gui": directions["wu_gui"],
            "liu_sha": directions["liu_sha"],
            "jue_ming": directions["jue_ming"]
        }
        
        return {
            "kua_number": kua_number,
            "birth_year": birth_year,
            "gender": gender,
            "characteristics": characteristics,
            "favorable_directions": favorable_directions,
            "unfavorable_directions": unfavorable_directions,
            "direction_details": self.get_direction_details(directions),
            "feng_shui_recommendations": self.generate_feng_shui_recommendations(kua_number),
            "compatibility": self.calculate_kua_compatibility(kua_number)
        }
    
    def get_direction_details(self, directions: Dict) -> Dict:
        """Obtém detalhes completos de cada direção"""
        
        details = {}
        for direction_type, direction in directions.items():
            details[direction_type] = {
                "direction": direction,
                "meaning": self.direction_meanings[direction_type]
            }
        
        return details
    
    def generate_feng_shui_recommendations(self, kua_number: int) -> Dict:
        """Gera recomendações específicas de Feng Shui baseadas no Kua"""
        
        characteristics = self.kua_characteristics[kua_number]
        directions = self.kua_directions[kua_number]
        
        recommendations = {
            "door_facing": directions["sheng_qi"],
            "bed_head_direction": directions["tian_yi"],
            "work_desk_facing": directions["sheng_qi"],
            "stove_direction": directions["tian_yi"],
            "avoid_directions": [
                directions["jue_ming"],
                directions["liu_sha"],
                directions["wu_gui"]
            ]
        }
        
        # Recomendações específicas por elemento
        element = characteristics["element"]
        
        element_recommendations = {
            "Water": {
                "colors": ["Azul", "Preto", "Azul marinho"],
                "shapes": ["Ondulado", "Irregular"],
                "materials": ["Vidro", "Espelhos", "Fontes de água"],
                "avoid_colors": ["Amarelo", "Marrom", "Bege"]
            },
            "Wood": {
                "colors": ["Verde", "Marrom claro"],
                "shapes": ["Retangular", "Colunar"],
                "materials": ["Madeira", "Plantas", "Bambu"],
                "avoid_colors": ["Branco", "Cinza", "Metálico"]
            },
            "Fire": {
                "colors": ["Vermelho", "Rosa", "Laranja", "Roxo"],
                "shapes": ["Triangular", "Pontiagudo"],
                "materials": ["Velas", "Luzes", "Objetos brilhantes"],
                "avoid_colors": ["Azul", "Preto"]
            },
            "Earth": {
                "colors": ["Amarelo", "Marrom", "Bege", "Terracota"],
                "shapes": ["Quadrado", "Retangular baixo"],
                "materials": ["Cerâmica", "Pedras", "Cristais"],
                "avoid_colors": ["Verde", "Marrom claro"]
            },
            "Metal": {
                "colors": ["Branco", "Cinza", "Dourado", "Prateado"],
                "shapes": ["Circular", "Oval"],
                "materials": ["Metal", "Cristais brancos", "Objetos metálicos"],
                "avoid_colors": ["Vermelho", "Rosa", "Laranja"]
            }
        }
        
        recommendations.update(element_recommendations.get(element, {}))
        
        return recommendations
    
    def calculate_kua_compatibility(self, kua_number: int) -> Dict:
        """Calcula compatibilidade com outros números Kua"""
        
        group = self.kua_characteristics[kua_number]["group"]
        
        # Compatibilidade por grupo
        if group == "East":
            compatible_kuas = [1, 3, 4, 9]
            incompatible_kuas = [2, 6, 7, 8]
        else:  # West
            compatible_kuas = [2, 6, 7, 8]
            incompatible_kuas = [1, 3, 4, 9]
        
        # Compatibilidade específica (mesmo elemento ou elementos produtivos)
        element = self.kua_characteristics[kua_number]["element"]
        
        element_compatibility = {
            "Water": {"best": [1], "good": [6, 7], "neutral": [4], "poor": [2, 8], "worst": [3, 9]},
            "Wood": {"best": [3, 4], "good": [1], "neutral": [9], "poor": [6, 7], "worst": [2, 8]},
            "Fire": {"best": [9], "good": [3, 4], "neutral": [2, 8], "poor": [1], "worst": [6, 7]},
            "Earth": {"best": [2, 8], "good": [9], "neutral": [6, 7], "poor": [3, 4], "worst": [1]},
            "Metal": {"best": [6, 7], "good": [2, 8], "neutral": [1], "poor": [9], "worst": [3, 4]}
        }
        
        specific_compatibility = element_compatibility.get(element, {})
        
        return {
            "group_compatibility": {
                "same_group": compatible_kuas,
                "opposite_group": incompatible_kuas
            },
            "element_compatibility": specific_compatibility,
            "relationship_advice": self.generate_relationship_advice(kua_number)
        }
    
    def generate_relationship_advice(self, kua_number: int) -> Dict:
        """Gera conselhos para relacionamentos baseados no Kua"""
        
        characteristics = self.kua_characteristics[kua_number]
        
        advice = {
            1: {
                "strengths": "Comunicativo e adaptável, bom ouvinte",
                "challenges": "Pode ser indeciso, precisa de estímulo",
                "ideal_partner": "Alguém estável que ofereça direção (Kua 2, 8)",
                "relationship_tips": "Desenvolva confiança, evite isolamento"
            },
            2: {
                "strengths": "Carinhoso e estável, oferece segurança",
                "challenges": "Pode ser passivo, resistente a mudanças",
                "ideal_partner": "Alguém dinâmico que traga energia (Kua 6, 7)",
                "relationship_tips": "Seja mais expressivo, aceite mudanças"
            },
            3: {
                "strengths": "Energético e inovador, líder natural",
                "challenges": "Pode ser impaciente e impulsivo",
                "ideal_partner": "Alguém calmo que traga equilíbrio (Kua 4, 9)",
                "relationship_tips": "Pratique paciência, ouça mais"
            },
            4: {
                "strengths": "Gentil e criativo, diplomático",
                "challenges": "Pode ser indeciso, falta confiança",
                "ideal_partner": "Alguém confiante que ofereça apoio (Kua 1, 3)",
                "relationship_tips": "Desenvolva autoconfiança, seja mais direto"
            },
            6: {
                "strengths": "Organizado e determinado, líder forte",
                "challenges": "Pode ser rígido e autoritário",
                "ideal_partner": "Alguém flexível e compreensivo (Kua 7, 2)",
                "relationship_tips": "Seja mais flexível, delegue responsabilidades"
            },
            7: {
                "strengths": "Comunicativo e alegre, socialmente hábil",
                "challenges": "Pode ser superficial, falta foco",
                "ideal_partner": "Alguém profundo que traga estabilidade (Kua 8, 6)",
                "relationship_tips": "Desenvolva profundidade, mantenha compromissos"
            },
            8: {
                "strengths": "Estável e determinado, confiável",
                "challenges": "Pode ser teimoso, tendência ao isolamento",
                "ideal_partner": "Alguém social que traga leveza (Kua 7, 2)",
                "relationship_tips": "Seja mais flexível, socialize mais"
            },
            9: {
                "strengths": "Inteligente e carismático, inspirador",
                "challenges": "Pode ser orgulhoso e impaciente",
                "ideal_partner": "Alguém humilde que ofereça apoio (Kua 1, 4)",
                "relationship_tips": "Pratique humildade, seja mais paciente"
            }
        }
        
        return advice.get(kua_number, {})
    
    def analyze_house_compatibility(self, house_facing_direction: str, kua_number: int) -> Dict:
        """Analisa compatibilidade entre direção da casa e Kua da pessoa"""
        
        directions = self.kua_directions[kua_number]
        
        # Determinar tipo de direção da casa
        house_effect = "neutral"
        direction_type = None
        
        for dir_type, direction in directions.items():
            if direction.lower() == house_facing_direction.lower():
                direction_type = dir_type
                if dir_type in ["sheng_qi", "tian_yi", "yan_nian", "fu_wei"]:
                    house_effect = "favorable"
                else:
                    house_effect = "unfavorable"
                break
        
        compatibility_score = 0
        if house_effect == "favorable":
            compatibility_score = 80 if direction_type == "sheng_qi" else 70
        elif house_effect == "unfavorable":
            compatibility_score = 20 if direction_type == "jue_ming" else 30
        else:
            compatibility_score = 50
        
        return {
            "house_facing": house_facing_direction,
            "person_kua": kua_number,
            "compatibility_score": compatibility_score,
            "effect": house_effect,
            "direction_type": direction_type,
            "recommendation": self.get_house_recommendation(house_effect, direction_type),
            "remedies": self.get_house_remedies(house_effect, kua_number) if house_effect == "unfavorable" else []
        }
    
    def get_house_recommendation(self, effect: str, direction_type: str) -> str:
        """Gera recomendação baseada na compatibilidade da casa"""
        
        if effect == "favorable":
            if direction_type == "sheng_qi":
                return "Excelente! Esta é sua melhor direção para prosperidade e sucesso."
            elif direction_type == "tian_yi":
                return "Muito bom! Esta direção favorece sua saúde e bem-estar."
            elif direction_type == "yan_nian":
                return "Bom! Esta direção promove relacionamentos harmoniosos."
            else:  # fu_wei
                return "Adequado! Esta direção oferece estabilidade e crescimento pessoal."
        elif effect == "unfavorable":
            if direction_type == "jue_ming":
                return "Atenção! Esta é sua pior direção. Considere mudança ou remédios urgentes."
            else:
                return "Cuidado! Esta direção pode trazer desafios. Aplique remédios Feng Shui."
        else:
            return "Direção neutra. Pode ser melhorada com ajustes de Feng Shui."
    
    def get_house_remedies(self, effect: str, kua_number: int) -> List[str]:
        """Sugere remédios para casas em direções desfavoráveis"""
        
        if effect != "unfavorable":
            return []
        
        characteristics = self.kua_characteristics[kua_number]
        element = characteristics["element"]
        
        general_remedies = [
            "Use espelhos para redirecionar energia negativa",
            "Coloque plantas ou cristais protetivos na entrada",
            "Mantenha a casa sempre limpa e bem iluminada",
            "Use sinos de vento para dispersar energia negativa"
        ]
        
        element_specific_remedies = {
            "Water": ["Coloque fonte de água na direção favorável", "Use cores azuis no interior"],
            "Wood": ["Adicione plantas vivas", "Use móveis de madeira natural"],
            "Fire": ["Melhore a iluminação", "Use velas ou objetos vermelhos"],
            "Earth": ["Use cristais e pedras", "Incorpore tons terrosos"],
            "Metal": ["Adicione objetos metálicos", "Use cores brancas e cinzas"]
        }
        
        remedies = general_remedies + element_specific_remedies.get(element, [])
        
        return remedies

# Função auxiliar para uso no ARCA
def calculate_kua_for_person(birth_year: int, gender: str) -> Dict:
    """
    Função auxiliar para calcular Kua integrado ao ARCA
    
    Args:
        birth_year: Ano de nascimento
        gender: 'male' ou 'female'
        
    Returns:
        Dict com análise Kua completa
    """
    calculator = KuaCalculator()
    return calculator.get_kua_analysis(birth_year, gender)

if __name__ == "__main__":
    # Teste da implementação
    result = calculate_kua_for_person(1990, "male")
    print(json.dumps(result, indent=2, ensure_ascii=False))


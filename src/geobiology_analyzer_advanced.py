"""
Módulo Avançado de Análise Geobiológica - Sistema ARCA v3.1
Análise aprofundada de redes telúricas, zonas geopatogênicas e radiações naturais

Referências:
- Dr. Ernst Hartmann: "Krankheit als Standortproblem" (1954)
- Dr. Manfred Curry: "Bioklimatik" (1952)
- Dr. Siegbert Lattacher: Research on geopathogenic zones
- Käthe Bachler: "Earth Radiation" (1989)
"""

import math
import random
from datetime import datetime
from typing import Dict, List, Tuple, Optional


class AdvancedGeobiologyAnalyzer:
    """Analisador avançado de geobiologia com cálculos precisos"""
    
    # Constantes geobiológicas baseadas em pesquisas
    HARTMANN_SPACING_NS = 2.0  # metros (Norte-Sul)
    HARTMANN_SPACING_EW = 2.5  # metros (Leste-Oeste)
    HARTMANN_LINE_WIDTH = 0.21  # metros (largura da linha)
    
    CURRY_SPACING = 3.5  # metros (diagonal)
    CURRY_ROTATION = 45.0  # graus (rotação em relação ao norte)
    CURRY_LINE_WIDTH = 0.60  # metros (largura da linha - mais intensa que Hartmann)
    
    BENKER_CUBIC_SPACING = 10.0  # metros (Grade Benker - cúbica 3D)
    
    # Intensidades de radiação (em Bovis units)
    HARTMANN_CROSSING_BOVIS = 6500  # Cruzamento Hartmann
    CURRY_CROSSING_BOVIS = 5500  # Cruzamento Curry (mais negativo)
    DOUBLE_CROSSING_BOVIS = 4000  # Cruzamento Hartmann + Curry
    WATER_VEIN_BOVIS = 5000  # Veio de água
    GEOLOGICAL_FAULT_BOVIS = 3500  # Falha geológica
    
    NEUTRAL_BOVIS = 6500  # Nível neutro saudável
    OPTIMAL_BOVIS = 8000  # Nível ótimo para saúde
    
    def __init__(self, latitude: float, longitude: float, area_width: float, 
                 area_height: float, soil_type: str = 'unknown'):
        """
        Inicializa o analisador geobiológico avançado
        
        Args:
            latitude: Latitude do local
            longitude: Longitude do local
            area_width: Largura da área em metros
            area_height: Altura da área em metros
            soil_type: Tipo de solo (granite, limestone, clay, sand, volcanic, unknown)
        """
        self.latitude = latitude
        self.longitude = longitude
        self.area_width = area_width
        self.area_height = area_height
        self.soil_type = soil_type
        
        # Ajustes baseados em latitude (campo magnético varia com latitude)
        self.magnetic_intensity_factor = self._calculate_magnetic_factor()
        
        # Ajustes baseados em fase lunar (influencia intensidade das redes)
        self.lunar_factor = self._calculate_lunar_factor()
        
    def _calculate_magnetic_factor(self) -> float:
        """
        Calcula fator de intensidade magnética baseado na latitude
        Campo magnético é mais forte nos polos e mais fraco no equador
        """
        # Intensidade relativa: 1.0 no equador, 2.0 nos polos
        return 1.0 + abs(self.latitude) / 90.0
    
    def _calculate_lunar_factor(self) -> float:
        """
        Calcula fator de influência lunar
        Lua cheia intensifica as redes telúricas
        """
        # Simulação simplificada - em produção, usar ephemeris real
        day_of_month = datetime.now().day
        lunar_cycle = abs(day_of_month - 15) / 15.0  # 0 na lua cheia, 1 na lua nova
        return 1.0 + (0.3 * (1.0 - lunar_cycle))  # Até 30% mais intenso na lua cheia
    
    def calculate_hartmann_grid(self) -> Dict:
        """
        Calcula a Grade Hartmann com precisão aprimorada
        
        Retorna:
            Dicionário com dados completos da grade Hartmann
        """
        # Calcular número de linhas
        ns_lines_count = int(self.area_width / self.HARTMANN_SPACING_NS) + 2
        ew_lines_count = int(self.area_height / self.HARTMANN_SPACING_EW) + 2
        
        # Gerar coordenadas das linhas
        ns_lines = []
        for i in range(ns_lines_count):
            x = i * self.HARTMANN_SPACING_NS
            ns_lines.append({
                'position': x,
                'orientation': 'north-south',
                'width': self.HARTMANN_LINE_WIDTH,
                'intensity_factor': self.magnetic_intensity_factor * self.lunar_factor
            })
        
        ew_lines = []
        for i in range(ew_lines_count):
            y = i * self.HARTMANN_SPACING_EW
            ew_lines.append({
                'position': y,
                'orientation': 'east-west',
                'width': self.HARTMANN_LINE_WIDTH,
                'intensity_factor': self.magnetic_intensity_factor * self.lunar_factor
            })
        
        # Calcular cruzamentos
        crossings = []
        for ns_line in ns_lines:
            for ew_line in ew_lines:
                crossing = {
                    'x': ns_line['position'],
                    'y': ew_line['position'],
                    'type': 'hartmann',
                    'bovis_units': int(self.HARTMANN_CROSSING_BOVIS / 
                                      (self.magnetic_intensity_factor * self.lunar_factor)),
                    'risk_level': 'medium',
                    'width': max(ns_line['width'], ew_line['width'])
                }
                
                # Classificar risco baseado em Bovis
                if crossing['bovis_units'] < 5000:
                    crossing['risk_level'] = 'high'
                elif crossing['bovis_units'] < 6000:
                    crossing['risk_level'] = 'medium'
                else:
                    crossing['risk_level'] = 'low'
                
                crossings.append(crossing)
        
        return {
            'spacing_ns': self.HARTMANN_SPACING_NS,
            'spacing_ew': self.HARTMANN_SPACING_EW,
            'line_width': self.HARTMANN_LINE_WIDTH,
            'ns_lines': ns_lines,
            'ew_lines': ew_lines,
            'total_crossings': len(crossings),
            'crossings': crossings,
            'magnetic_factor': self.magnetic_intensity_factor,
            'lunar_factor': self.lunar_factor,
            'description': 'Grade Hartmann - Rede geomagnética global com orientação N-S e L-O'
        }
    
    def calculate_curry_grid(self) -> Dict:
        """
        Calcula a Grade Curry (diagonal) com precisão aprimorada
        
        Retorna:
            Dicionário com dados completos da grade Curry
        """
        # Curry é diagonal (45 graus)
        diagonal_length = math.sqrt(self.area_width**2 + self.area_height**2)
        lines_count = int(diagonal_length / self.CURRY_SPACING) + 2
        
        # Gerar linhas diagonais
        ne_sw_lines = []  # Nordeste-Sudoeste
        nw_se_lines = []  # Noroeste-Sudeste
        
        for i in range(lines_count):
            offset = i * self.CURRY_SPACING
            
            ne_sw_lines.append({
                'offset': offset,
                'orientation': 'ne-sw',
                'angle': 45.0,
                'width': self.CURRY_LINE_WIDTH,
                'intensity_factor': self.magnetic_intensity_factor * self.lunar_factor * 1.2
            })
            
            nw_se_lines.append({
                'offset': offset,
                'orientation': 'nw-se',
                'angle': 135.0,
                'width': self.CURRY_LINE_WIDTH,
                'intensity_factor': self.magnetic_intensity_factor * self.lunar_factor * 1.2
            })
        
        # Calcular cruzamentos aproximados
        crossings = []
        for i in range(min(len(ne_sw_lines), len(nw_se_lines))):
            # Aproximação de cruzamentos na área
            x = (i * self.CURRY_SPACING) % self.area_width
            y = (i * self.CURRY_SPACING) % self.area_height
            
            crossing = {
                'x': x,
                'y': y,
                'type': 'curry',
                'bovis_units': int(self.CURRY_CROSSING_BOVIS / 
                                  (self.magnetic_intensity_factor * self.lunar_factor * 1.2)),
                'risk_level': 'high',  # Curry é mais intenso que Hartmann
                'width': self.CURRY_LINE_WIDTH
            }
            
            # Classificar risco
            if crossing['bovis_units'] < 4500:
                crossing['risk_level'] = 'critical'
            elif crossing['bovis_units'] < 5500:
                crossing['risk_level'] = 'high'
            else:
                crossing['risk_level'] = 'medium'
            
            crossings.append(crossing)
        
        return {
            'spacing': self.CURRY_SPACING,
            'rotation': self.CURRY_ROTATION,
            'line_width': self.CURRY_LINE_WIDTH,
            'ne_sw_lines': ne_sw_lines,
            'nw_se_lines': nw_se_lines,
            'total_crossings': len(crossings),
            'crossings': crossings,
            'magnetic_factor': self.magnetic_intensity_factor * 1.2,
            'lunar_factor': self.lunar_factor,
            'description': 'Grade Curry - Rede diagonal com maior intensidade que Hartmann'
        }
    
    def calculate_benker_cubic_grid(self) -> Dict:
        """
        Calcula a Grade Benker (cúbica tridimensional)
        Menos conhecida mas importante para análise de edifícios de múltiplos andares
        
        Retorna:
            Dicionário com dados da grade Benker
        """
        lines_x = int(self.area_width / self.BENKER_CUBIC_SPACING) + 1
        lines_y = int(self.area_height / self.BENKER_CUBIC_SPACING) + 1
        
        crossings = []
        for i in range(lines_x):
            for j in range(lines_y):
                crossing = {
                    'x': i * self.BENKER_CUBIC_SPACING,
                    'y': j * self.BENKER_CUBIC_SPACING,
                    'type': 'benker',
                    'bovis_units': 6000,  # Geralmente menos intenso
                    'risk_level': 'low',
                    'affects_vertical': True  # Afeta todos os andares verticalmente
                }
                crossings.append(crossing)
        
        return {
            'spacing': self.BENKER_CUBIC_SPACING,
            'total_crossings': len(crossings),
            'crossings': crossings,
            'description': 'Grade Benker - Rede cúbica tridimensional (10m x 10m x 10m)',
            'note': 'Afeta edifícios verticalmente em todos os andares'
        }
    
    def detect_water_veins(self) -> Dict:
        """
        Detecta veios de água subterrâneos (simulado com base em geologia)
        Em produção, usar dados hidrológicos reais
        
        Retorna:
            Dicionário com veios de água detectados
        """
        # Probabilidade baseada em tipo de solo
        water_probability = {
            'granite': 0.2,
            'limestone': 0.6,  # Calcário é permeável
            'clay': 0.3,
            'sand': 0.5,
            'volcanic': 0.4,
            'unknown': 0.3
        }
        
        prob = water_probability.get(self.soil_type, 0.3)
        
        # Simular veios de água
        veins = []
        num_veins = int(random.random() * 5) if random.random() < prob else 0
        
        for i in range(num_veins):
            vein = {
                'id': f'vein_{i+1}',
                'start_x': random.uniform(0, self.area_width),
                'start_y': random.uniform(0, self.area_height),
                'end_x': random.uniform(0, self.area_width),
                'end_y': random.uniform(0, self.area_height),
                'depth_meters': random.uniform(2, 15),
                'flow_rate': random.choice(['low', 'medium', 'high']),
                'width_meters': random.uniform(0.5, 3.0),
                'bovis_units': random.randint(4500, 5500),
                'risk_level': 'high'
            }
            veins.append(vein)
        
        return {
            'veins_detected': len(veins),
            'veins': veins,
            'soil_type': self.soil_type,
            'detection_probability': prob,
            'description': 'Veios de água subterrâneos criam campos eletromagnéticos por atrito'
        }
    
    def detect_geological_faults(self) -> Dict:
        """
        Detecta falhas geológicas (simulado com base em geologia regional)
        Em produção, usar dados geológicos oficiais
        
        Retorna:
            Dicionário com falhas geológicas detectadas
        """
        # Probabilidade baseada em região (simplificado)
        # Regiões sísmicas têm mais falhas
        fault_probability = abs(math.sin(self.latitude * math.pi / 180)) * 0.3
        
        faults = []
        num_faults = 1 if random.random() < fault_probability else 0
        
        for i in range(num_faults):
            fault = {
                'id': f'fault_{i+1}',
                'start_x': random.uniform(0, self.area_width),
                'start_y': random.uniform(0, self.area_height),
                'end_x': random.uniform(0, self.area_width),
                'end_y': random.uniform(0, self.area_height),
                'depth_meters': random.uniform(10, 100),
                'type': random.choice(['normal', 'reverse', 'strike-slip']),
                'activity': random.choice(['inactive', 'potentially_active']),
                'width_meters': random.uniform(1, 10),
                'bovis_units': random.randint(3000, 4500),
                'risk_level': 'critical'
            }
            faults.append(fault)
        
        return {
            'faults_detected': len(faults),
            'faults': faults,
            'detection_probability': fault_probability,
            'description': 'Falhas geológicas emitem radiações e podem liberar gases (radônio)'
        }
    
    def calculate_geopathogenic_zones(self, hartmann_grid: Dict, curry_grid: Dict,
                                     water_veins: Dict, geological_faults: Dict) -> Dict:
        """
        Identifica zonas geopatogênicas (cruzamentos críticos e sobreposições)
        
        Args:
            hartmann_grid: Dados da grade Hartmann
            curry_grid: Dados da grade Curry
            water_veins: Dados de veios de água
            geological_faults: Dados de falhas geológicas
        
        Retorna:
            Dicionário com zonas geopatogênicas identificadas
        """
        geopathogenic_zones = []
        
        # Detectar cruzamentos duplos (Hartmann + Curry)
        for h_crossing in hartmann_grid['crossings']:
            for c_crossing in curry_grid['crossings']:
                distance = math.sqrt((h_crossing['x'] - c_crossing['x'])**2 + 
                                   (h_crossing['y'] - c_crossing['y'])**2)
                
                if distance < 0.5:  # Cruzamento duplo (menos de 50cm de distância)
                    zone = {
                        'x': (h_crossing['x'] + c_crossing['x']) / 2,
                        'y': (h_crossing['y'] + c_crossing['y']) / 2,
                        'type': 'double_crossing',
                        'components': ['hartmann', 'curry'],
                        'bovis_units': self.DOUBLE_CROSSING_BOVIS,
                        'risk_level': 'critical',
                        'radius_meters': 1.0,
                        'description': 'Cruzamento duplo Hartmann-Curry - zona altamente geopatogênica'
                    }
                    geopathogenic_zones.append(zone)
        
        # Adicionar veios de água como zonas
        for vein in water_veins['veins']:
            zone = {
                'x': (vein['start_x'] + vein['end_x']) / 2,
                'y': (vein['start_y'] + vein['end_y']) / 2,
                'type': 'water_vein',
                'components': ['underground_water'],
                'bovis_units': vein['bovis_units'],
                'risk_level': vein['risk_level'],
                'radius_meters': vein['width_meters'],
                'description': f"Veio de água subterrâneo - fluxo {vein['flow_rate']}"
            }
            geopathogenic_zones.append(zone)
        
        # Adicionar falhas geológicas como zonas
        for fault in geological_faults['faults']:
            zone = {
                'x': (fault['start_x'] + fault['end_x']) / 2,
                'y': (fault['start_y'] + fault['end_y']) / 2,
                'type': 'geological_fault',
                'components': ['fault'],
                'bovis_units': fault['bovis_units'],
                'risk_level': fault['risk_level'],
                'radius_meters': fault['width_meters'],
                'description': f"Falha geológica {fault['type']} - {fault['activity']}"
            }
            geopathogenic_zones.append(zone)
        
        # Classificar zonas por risco
        critical_zones = [z for z in geopathogenic_zones if z['risk_level'] == 'critical']
        high_zones = [z for z in geopathogenic_zones if z['risk_level'] == 'high']
        medium_zones = [z for z in geopathogenic_zones if z['risk_level'] == 'medium']
        
        # Avaliação geral de risco
        if len(critical_zones) > 0:
            overall_risk = 'critical'
        elif len(high_zones) > 2:
            overall_risk = 'high'
        elif len(high_zones) > 0 or len(medium_zones) > 3:
            overall_risk = 'medium'
        else:
            overall_risk = 'low'
        
        return {
            'total_geopathogenic_zones': len(geopathogenic_zones),
            'zones': geopathogenic_zones,
            'critical_zones': len(critical_zones),
            'high_risk_zones': len(high_zones),
            'medium_risk_zones': len(medium_zones),
            'overall_risk_assessment': overall_risk,
            'hartmann_crossings': len(hartmann_grid['crossings']),
            'curry_crossings': len(curry_grid['crossings']),
            'water_veins': len(water_veins['veins']),
            'geological_faults': len(geological_faults['faults']),
            'recommendations': self._generate_geopathogenic_recommendations(overall_risk, geopathogenic_zones)
        }
    
    def _generate_geopathogenic_recommendations(self, risk_level: str, zones: List[Dict]) -> List[str]:
        """Gera recomendações baseadas nas zonas geopatogênicas"""
        recommendations = []
        
        if risk_level in ['critical', 'high']:
            recommendations.append("URGENTE: Evitar posicionar camas e locais de permanência prolongada sobre zonas geopatogênicas")
            recommendations.append("Considerar blindagem geobiológica com materiais específicos (cortiça, carvão ativado)")
            recommendations.append("Realizar medições presenciais com radiestesista profissional")
        
        double_crossings = [z for z in zones if z['type'] == 'double_crossing']
        if len(double_crossings) > 0:
            recommendations.append(f"Identificados {len(double_crossings)} cruzamentos duplos - evitar rigorosamente")
        
        water_veins = [z for z in zones if z['type'] == 'water_vein']
        if len(water_veins) > 0:
            recommendations.append(f"Detectados {len(water_veins)} veios de água - considerar desvio ou blindagem")
        
        faults = [z for z in zones if z['type'] == 'geological_fault']
        if len(faults) > 0:
            recommendations.append(f"Atenção: {len(faults)} falhas geológicas detectadas - risco de radônio")
            recommendations.append("Instalar sistema de ventilação adequado para prevenir acúmulo de radônio")
        
        recommendations.append("Posicionar camas com cabeceira ao Norte ou Leste, longe de cruzamentos")
        recommendations.append("Utilizar plantas purificadoras de ar (espada-de-são-jorge, lírio-da-paz)")
        recommendations.append("Considerar uso de cristais de quartzo ou shungite para harmonização")
        
        return recommendations
    
    def analyze(self) -> Dict:
        """
        Realiza análise geobiológica completa e avançada
        
        Retorna:
            Dicionário com análise completa
        """
        # Calcular todas as grades e detecções
        hartmann_grid = self.calculate_hartmann_grid()
        curry_grid = self.calculate_curry_grid()
        benker_grid = self.calculate_benker_cubic_grid()
        water_veins = self.detect_water_veins()
        geological_faults = self.detect_geological_faults()
        
        # Calcular zonas geopatogênicas
        geopathogenic_zones = self.calculate_geopathogenic_zones(
            hartmann_grid, curry_grid, water_veins, geological_faults
        )
        
        # Análise de radiação do solo (do módulo original)
        from geobiology_analyzer import analyze_geobiology
        basic_analysis = analyze_geobiology(
            self.latitude, self.longitude, 
            self.area_width, self.area_height, 
            self.soil_type
        )
        
        # Score de saúde geobiológica aprimorado
        base_score = basic_analysis['overall_assessment']['geobiological_health_score']
        
        # Penalidades por zonas geopatogênicas
        penalty = geopathogenic_zones['critical_zones'] * 15
        penalty += geopathogenic_zones['high_risk_zones'] * 8
        penalty += geopathogenic_zones['medium_risk_zones'] * 3
        
        final_score = max(0, base_score - penalty)
        
        # Determinar adequação para habitação
        suitable_for_habitation = final_score >= 60
        
        # Compilar análise completa
        return {
            'location': {
                'latitude': self.latitude,
                'longitude': self.longitude,
                'area_width': self.area_width,
                'area_height': self.area_height,
                'soil_type': self.soil_type
            },
            'environmental_factors': {
                'magnetic_intensity_factor': self.magnetic_intensity_factor,
                'lunar_factor': self.lunar_factor,
                'analysis_date': datetime.now().isoformat()
            },
            'hartmann_grid': hartmann_grid,
            'curry_grid': curry_grid,
            'benker_grid': benker_grid,
            'water_veins': water_veins,
            'geological_faults': geological_faults,
            'geopathogenic_zones': geopathogenic_zones,
            'soil_radiation': basic_analysis['soil_radiation'],
            'overall_assessment': {
                'geobiological_health_score': final_score,
                'risk_level': geopathogenic_zones['overall_risk_assessment'],
                'suitable_for_habitation': suitable_for_habitation,
                'main_concerns': self._identify_main_concerns(geopathogenic_zones, water_veins, geological_faults),
                'priority_actions': geopathogenic_zones['recommendations'][:5]
            },
            'detailed_recommendations': {
                'sleeping_areas': self._generate_sleeping_recommendations(geopathogenic_zones),
                'working_areas': self._generate_working_recommendations(geopathogenic_zones),
                'mitigation_strategies': self._generate_mitigation_strategies(geopathogenic_zones),
                'monitoring': self._generate_monitoring_recommendations()
            }
        }
    
    def _identify_main_concerns(self, geopathogenic_zones: Dict, water_veins: Dict, 
                               geological_faults: Dict) -> List[str]:
        """Identifica as principais preocupações geobiológicas"""
        concerns = []
        
        if geopathogenic_zones['critical_zones'] > 0:
            concerns.append(f"{geopathogenic_zones['critical_zones']} zonas críticas identificadas")
        
        if water_veins['veins_detected'] > 2:
            concerns.append(f"Múltiplos veios de água ({water_veins['veins_detected']}) detectados")
        
        if geological_faults['faults_detected'] > 0:
            concerns.append("Presença de falha geológica - risco de radônio")
        
        if geopathogenic_zones['overall_risk_assessment'] in ['critical', 'high']:
            concerns.append("Nível geral de risco geobiológico elevado")
        
        return concerns if concerns else ["Nenhuma preocupação crítica identificada"]
    
    def _generate_sleeping_recommendations(self, geopathogenic_zones: Dict) -> List[str]:
        """Gera recomendações específicas para áreas de dormir"""
        return [
            "Posicionar cama a pelo menos 1,5m de distância de zonas geopatogênicas",
            "Orientar cabeceira preferencialmente ao Norte ou Leste",
            "Evitar camas sobre cruzamentos Hartmann e especialmente Curry",
            "Utilizar colchão de materiais naturais (látex natural, algodão orgânico)",
            "Considerar uso de tapete de shungite sob a cama para blindagem",
            "Manter quarto bem ventilado para dispersar possível radônio",
            "Evitar dispositivos eletrônicos próximos à cabeceira"
        ]
    
    def _generate_working_recommendations(self, geopathogenic_zones: Dict) -> List[str]:
        """Gera recomendações específicas para áreas de trabalho"""
        return [
            "Posicionar mesa de trabalho longe de cruzamentos de redes",
            "Orientar mesa preferencialmente voltada para Norte ou Leste",
            "Utilizar plantas purificadoras próximas à área de trabalho",
            "Fazer pausas regulares e caminhar para dispersar energia estagnada",
            "Considerar uso de cristais de quartzo na mesa",
            "Manter boa iluminação natural sempre que possível"
        ]
    
    def _generate_mitigation_strategies(self, geopathogenic_zones: Dict) -> List[str]:
        """Gera estratégias de mitigação de zonas geopatogênicas"""
        strategies = []
        
        if geopathogenic_zones['overall_risk_assessment'] in ['critical', 'high']:
            strategies.extend([
                "BLINDAGEM FÍSICA: Instalar placas de cortiça (3-5cm) sob áreas críticas",
                "BLINDAGEM MINERAL: Utilizar shungite, turmalina negra ou hematita",
                "DESVIO ENERGÉTICO: Criar espirais de cobre para desviar linhas telúricas",
                "NEUTRALIZAÇÃO: Usar pirâmides de cobre nas proporções de Keops",
                "VEGETAÇÃO: Plantar árvores de raízes profundas para drenar energia"
            ])
        
        strategies.extend([
            "Realizar limpeza energética regular com defumação (alecrim, arruda)",
            "Utilizar sal grosso nos cantos dos ambientes",
            "Manter cristais de quartzo limpos e energizados",
            "Considerar consulta com radiestesista profissional para medições precisas"
        ])
        
        return strategies
    
    def _generate_monitoring_recommendations(self) -> List[str]:
        """Gera recomendações de monitoramento contínuo"""
        return [
            "Realizar medições geobiológicas a cada 6 meses (redes podem variar)",
            "Monitorar qualidade do sono e bem-estar dos ocupantes",
            "Medir níveis de radônio anualmente (especialmente em porões)",
            "Observar comportamento de animais de estimação (evitam zonas geopatogênicas)",
            "Documentar qualquer mudança na saúde após mudanças de layout",
            "Considerar medições profissionais com equipamento especializado"
        ]


def analyze_geobiology_advanced(latitude: float, longitude: float, 
                               area_width: float, area_height: float, 
                               soil_type: str = 'unknown') -> Dict:
    """
    Função wrapper para análise geobiológica avançada
    
    Args:
        latitude: Latitude do local
        longitude: Longitude do local
        area_width: Largura da área em metros
        area_height: Altura da área em metros
        soil_type: Tipo de solo
    
    Retorna:
        Dicionário com análise completa
    """
    analyzer = AdvancedGeobiologyAnalyzer(latitude, longitude, area_width, area_height, soil_type)
    return analyzer.analyze()


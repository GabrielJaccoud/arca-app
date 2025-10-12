"""
Módulo de Análise Geobiológica para o Sistema ARCA
Inclui análise de redes Hartmann e Curry, veios de água, falhas geológicas e pontos geopatogênicos
"""

import math
import json
from typing import Dict, List, Tuple, Any
from datetime import datetime


class GeobiologyAnalyzer:
    """
    Analisador de aspectos geobiológicos de um terreno/edificação
    """
    
    # Constantes para as grades
    HARTMANN_SPACING_NS = 2.0  # metros (Norte-Sul)
    HARTMANN_SPACING_EW = 2.5  # metros (Leste-Oeste)
    HARTMANN_WIDTH = 0.21  # metros (largura das linhas)
    
    CURRY_SPACING = 3.5  # metros (diagonal)
    CURRY_WIDTH = 0.40  # metros (largura das linhas)
    CURRY_ROTATION = 45  # graus (diagonal NE-SO e NO-SE)
    
    def __init__(self, latitude: float, longitude: float):
        """
        Inicializa o analisador geobiológico
        
        Args:
            latitude: Latitude do local em graus decimais
            longitude: Longitude do local em graus decimais
        """
        self.latitude = latitude
        self.longitude = longitude
        self.analysis_date = datetime.now()
        
    def calculate_hartmann_grid(self, area_width: float, area_height: float) -> Dict[str, Any]:
        """
        Calcula a grade Hartmann para uma área específica
        
        Args:
            area_width: Largura da área em metros
            area_height: Altura da área em metros
            
        Returns:
            Dicionário com informações da grade Hartmann
        """
        # Linhas Norte-Sul (verticais)
        ns_lines = []
        x = 0
        while x <= area_width:
            ns_lines.append({
                'position': x,
                'orientation': 'north-south',
                'width': self.HARTMANN_WIDTH,
                'type': 'hartmann'
            })
            x += self.HARTMANN_SPACING_NS
        
        # Linhas Leste-Oeste (horizontais)
        ew_lines = []
        y = 0
        while y <= area_height:
            ew_lines.append({
                'position': y,
                'orientation': 'east-west',
                'width': self.HARTMANN_WIDTH,
                'type': 'hartmann'
            })
            y += self.HARTMANN_SPACING_EW
        
        # Identificar cruzamentos (pontos de maior intensidade)
        crossings = []
        for ns_line in ns_lines:
            for ew_line in ew_lines:
                crossings.append({
                    'x': ns_line['position'],
                    'y': ew_line['position'],
                    'type': 'hartmann_crossing',
                    'intensity': 'medium',
                    'recommendation': 'Evitar permanência prolongada'
                })
        
        return {
            'grid_type': 'hartmann',
            'spacing_ns': self.HARTMANN_SPACING_NS,
            'spacing_ew': self.HARTMANN_SPACING_EW,
            'line_width': self.HARTMANN_WIDTH,
            'ns_lines': ns_lines,
            'ew_lines': ew_lines,
            'crossings': crossings,
            'total_crossings': len(crossings),
            'area_coverage': {
                'width': area_width,
                'height': area_height
            }
        }
    
    def calculate_curry_grid(self, area_width: float, area_height: float) -> Dict[str, Any]:
        """
        Calcula a grade Curry (diagonal) para uma área específica
        
        Args:
            area_width: Largura da área em metros
            area_height: Altura da área em metros
            
        Returns:
            Dicionário com informações da grade Curry
        """
        # Linhas diagonais NE-SO
        ne_sw_lines = []
        # Linhas diagonais NO-SE
        nw_se_lines = []
        
        # Calcular linhas NE-SO (diagonal principal)
        diagonal_length = math.sqrt(area_width**2 + area_height**2)
        num_lines = int(diagonal_length / self.CURRY_SPACING) + 1
        
        for i in range(-num_lines, num_lines + 1):
            offset = i * self.CURRY_SPACING
            ne_sw_lines.append({
                'offset': offset,
                'orientation': 'northeast-southwest',
                'width': self.CURRY_WIDTH,
                'type': 'curry',
                'angle': 45
            })
            
            nw_se_lines.append({
                'offset': offset,
                'orientation': 'northwest-southeast',
                'width': self.CURRY_WIDTH,
                'type': 'curry',
                'angle': -45
            })
        
        # Identificar cruzamentos Curry
        crossings = []
        # Simplificação: estimar cruzamentos baseado na área
        estimated_crossings = int((area_width * area_height) / (self.CURRY_SPACING ** 2))
        
        for i in range(estimated_crossings):
            # Distribuir cruzamentos de forma aproximada
            x = (i % int(area_width / self.CURRY_SPACING)) * self.CURRY_SPACING
            y = (i // int(area_width / self.CURRY_SPACING)) * self.CURRY_SPACING
            
            if x <= area_width and y <= area_height:
                crossings.append({
                    'x': x,
                    'y': y,
                    'type': 'curry_crossing',
                    'intensity': 'high',
                    'recommendation': 'Evitar camas e locais de permanência'
                })
        
        return {
            'grid_type': 'curry',
            'spacing': self.CURRY_SPACING,
            'line_width': self.CURRY_WIDTH,
            'rotation': self.CURRY_ROTATION,
            'ne_sw_lines': ne_sw_lines,
            'nw_se_lines': nw_se_lines,
            'crossings': crossings,
            'total_crossings': len(crossings),
            'area_coverage': {
                'width': area_width,
                'height': area_height
            }
        }
    
    def detect_water_veins(self, geological_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Detecta possíveis veios de água subterrâneos
        
        Args:
            geological_data: Dados geológicos da região (opcional)
            
        Returns:
            Análise de veios de água
        """
        # Simulação baseada em dados geológicos e geográficos
        # Em produção, isso seria integrado com dados geológicos reais
        
        # Fatores que influenciam presença de água subterrânea
        proximity_to_water = self._estimate_water_proximity()
        soil_type = geological_data.get('soil_type', 'unknown') if geological_data else 'unknown'
        
        water_veins = []
        
        # Simulação de detecção
        if proximity_to_water < 1000:  # menos de 1km de corpo d'água
            water_veins.append({
                'type': 'underground_stream',
                'depth_estimate': '5-15 metros',
                'flow_direction': 'northeast',
                'intensity': 'medium',
                'geopathogenic_potential': 'medium',
                'recommendation': 'Evitar posicionar camas sobre o veio'
            })
        
        return {
            'water_veins_detected': len(water_veins),
            'veins': water_veins,
            'proximity_to_surface_water': proximity_to_water,
            'soil_permeability': self._estimate_soil_permeability(soil_type),
            'risk_assessment': 'medium' if len(water_veins) > 0 else 'low'
        }
    
    def detect_geological_faults(self, geological_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Detecta possíveis falhas geológicas
        
        Args:
            geological_data: Dados geológicos da região (opcional)
            
        Returns:
            Análise de falhas geológicas
        """
        # Em produção, isso seria integrado com dados geológicos reais
        # Por ora, simulação baseada em localização
        
        faults = []
        
        # Verificar se está em região sismicamente ativa
        seismic_risk = self._estimate_seismic_risk()
        
        if seismic_risk > 0.3:
            faults.append({
                'type': 'tectonic_fault',
                'distance_estimate': '> 5km',
                'activity_level': 'low',
                'geopathogenic_potential': 'low',
                'recommendation': 'Monitoramento não urgente'
            })
        
        return {
            'faults_detected': len(faults),
            'faults': faults,
            'seismic_risk_level': seismic_risk,
            'risk_assessment': 'low' if seismic_risk < 0.5 else 'medium'
        }
    
    def identify_geopathogenic_zones(self, area_width: float, area_height: float) -> Dict[str, Any]:
        """
        Identifica zonas geopatogênicas (cruzamentos de grades, veios de água, falhas)
        
        Args:
            area_width: Largura da área em metros
            area_height: Altura da área em metros
            
        Returns:
            Mapeamento de zonas geopatogênicas
        """
        hartmann = self.calculate_hartmann_grid(area_width, area_height)
        curry = self.calculate_curry_grid(area_width, area_height)
        water_veins = self.detect_water_veins()
        faults = self.detect_geological_faults()
        
        # Identificar zonas de alto risco (cruzamentos duplos: Hartmann + Curry)
        high_risk_zones = []
        
        # Verificar proximidade entre cruzamentos Hartmann e Curry
        for h_cross in hartmann['crossings']:
            for c_cross in curry['crossings']:
                distance = math.sqrt(
                    (h_cross['x'] - c_cross['x'])**2 + 
                    (h_cross['y'] - c_cross['y'])**2
                )
                
                if distance < 0.5:  # menos de 50cm de distância
                    high_risk_zones.append({
                        'x': (h_cross['x'] + c_cross['x']) / 2,
                        'y': (h_cross['y'] + c_cross['y']) / 2,
                        'type': 'double_crossing',
                        'components': ['hartmann', 'curry'],
                        'intensity': 'very_high',
                        'recommendation': 'EVITAR: Não posicionar camas, mesas de trabalho ou locais de permanência prolongada'
                    })
        
        # Adicionar zonas de veios de água
        for vein in water_veins['veins']:
            high_risk_zones.append({
                'type': 'water_vein',
                'intensity': vein['intensity'],
                'recommendation': vein['recommendation']
            })
        
        return {
            'total_geopathogenic_zones': len(high_risk_zones),
            'high_risk_zones': high_risk_zones,
            'hartmann_crossings': hartmann['total_crossings'],
            'curry_crossings': curry['total_crossings'],
            'water_veins': water_veins['water_veins_detected'],
            'geological_faults': faults['faults_detected'],
            'overall_risk_assessment': self._calculate_overall_risk(high_risk_zones),
            'recommendations': self._generate_geopathogenic_recommendations(high_risk_zones)
        }
    
    def analyze_soil_radiation(self, soil_type: str = 'unknown') -> Dict[str, Any]:
        """
        Analisa radiação natural do solo
        
        Args:
            soil_type: Tipo de solo (granite, limestone, clay, sand, etc.)
            
        Returns:
            Análise de radiação do solo
        """
        # Níveis de radiação natural por tipo de solo
        radiation_levels = {
            'granite': {'level': 'high', 'radon_risk': 'high', 'value': 150},
            'limestone': {'level': 'low', 'radon_risk': 'low', 'value': 30},
            'clay': {'level': 'medium', 'radon_risk': 'medium', 'value': 70},
            'sand': {'level': 'low', 'radon_risk': 'low', 'value': 25},
            'volcanic': {'level': 'high', 'radon_risk': 'high', 'value': 180},
            'unknown': {'level': 'medium', 'radon_risk': 'medium', 'value': 60}
        }
        
        soil_data = radiation_levels.get(soil_type.lower(), radiation_levels['unknown'])
        
        return {
            'soil_type': soil_type,
            'radiation_level': soil_data['level'],
            'radiation_value_bq_m3': soil_data['value'],  # Becquerels por metro cúbico
            'radon_risk': soil_data['radon_risk'],
            'recommendations': self._generate_radiation_recommendations(soil_data)
        }
    
    def perform_complete_analysis(self, area_width: float, area_height: float, 
                                   soil_type: str = 'unknown',
                                   geological_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Realiza análise geobiológica completa
        
        Args:
            area_width: Largura da área em metros
            area_height: Altura da área em metros
            soil_type: Tipo de solo
            geological_data: Dados geológicos adicionais
            
        Returns:
            Análise geobiológica completa
        """
        return {
            'location': {
                'latitude': self.latitude,
                'longitude': self.longitude
            },
            'analysis_date': self.analysis_date.isoformat(),
            'area_dimensions': {
                'width': area_width,
                'height': area_height,
                'area_m2': area_width * area_height
            },
            'hartmann_grid': self.calculate_hartmann_grid(area_width, area_height),
            'curry_grid': self.calculate_curry_grid(area_width, area_height),
            'water_veins': self.detect_water_veins(geological_data),
            'geological_faults': self.detect_geological_faults(geological_data),
            'geopathogenic_zones': self.identify_geopathogenic_zones(area_width, area_height),
            'soil_radiation': self.analyze_soil_radiation(soil_type),
            'overall_assessment': self._generate_overall_assessment(area_width, area_height, soil_type)
        }
    
    # Métodos auxiliares privados
    
    def _estimate_water_proximity(self) -> float:
        """Estima proximidade a corpos d'água (simulado)"""
        # Em produção, usar APIs de geolocalização e dados hidrográficos
        return 500  # metros (simulado)
    
    def _estimate_soil_permeability(self, soil_type: str) -> str:
        """Estima permeabilidade do solo"""
        permeability_map = {
            'granite': 'low',
            'limestone': 'high',
            'clay': 'low',
            'sand': 'very_high',
            'volcanic': 'medium',
            'unknown': 'medium'
        }
        return permeability_map.get(soil_type.lower(), 'medium')
    
    def _estimate_seismic_risk(self) -> float:
        """Estima risco sísmico baseado na localização"""
        # Simulação - em produção, usar dados sísmicos reais
        # Brasil geralmente tem baixo risco sísmico
        if -30 <= self.latitude <= 5 and -75 <= self.longitude <= -35:
            return 0.1  # Baixo risco para Brasil
        return 0.3
    
    def _calculate_overall_risk(self, high_risk_zones: List[Dict]) -> str:
        """Calcula avaliação geral de risco"""
        num_zones = len(high_risk_zones)
        if num_zones == 0:
            return 'low'
        elif num_zones < 5:
            return 'medium'
        else:
            return 'high'
    
    def _generate_geopathogenic_recommendations(self, zones: List[Dict]) -> List[str]:
        """Gera recomendações para zonas geopatogênicas"""
        recommendations = []
        
        if len(zones) > 0:
            recommendations.append("Evitar posicionar camas sobre zonas geopatogênicas identificadas")
            recommendations.append("Mesas de trabalho devem estar fora de cruzamentos de grades")
            recommendations.append("Considerar uso de materiais isolantes (cortiça, lã de rocha)")
            
        if len(zones) > 5:
            recommendations.append("Considerar consulta com geobiólogo profissional")
            recommendations.append("Avaliar reposicionamento de ambientes principais")
            
        return recommendations
    
    def _generate_radiation_recommendations(self, soil_data: Dict) -> List[str]:
        """Gera recomendações baseadas em radiação do solo"""
        recommendations = []
        
        if soil_data['radon_risk'] == 'high':
            recommendations.append("Implementar sistema de ventilação adequado")
            recommendations.append("Selar rachaduras no piso e paredes do porão")
            recommendations.append("Considerar teste de radônio profissional")
        elif soil_data['radon_risk'] == 'medium':
            recommendations.append("Manter boa ventilação natural")
            recommendations.append("Monitorar níveis de radônio periodicamente")
        
        return recommendations
    
    def _generate_overall_assessment(self, area_width: float, area_height: float, 
                                     soil_type: str) -> Dict[str, Any]:
        """Gera avaliação geral da análise geobiológica"""
        geopathogenic = self.identify_geopathogenic_zones(area_width, area_height)
        radiation = self.analyze_soil_radiation(soil_type)
        
        # Calcular score geral (0-100)
        score = 100
        score -= geopathogenic['total_geopathogenic_zones'] * 5
        
        if radiation['radon_risk'] == 'high':
            score -= 20
        elif radiation['radon_risk'] == 'medium':
            score -= 10
        
        score = max(0, min(100, score))  # Manter entre 0-100
        
        return {
            'geobiological_health_score': score,
            'risk_level': 'low' if score > 70 else 'medium' if score > 40 else 'high',
            'main_concerns': self._identify_main_concerns(geopathogenic, radiation),
            'priority_actions': self._identify_priority_actions(geopathogenic, radiation),
            'suitable_for_habitation': score > 40
        }
    
    def _identify_main_concerns(self, geopathogenic: Dict, radiation: Dict) -> List[str]:
        """Identifica principais preocupações"""
        concerns = []
        
        if geopathogenic['total_geopathogenic_zones'] > 5:
            concerns.append("Alto número de zonas geopatogênicas")
        
        if radiation['radon_risk'] == 'high':
            concerns.append("Risco elevado de radônio no solo")
        
        if geopathogenic['water_veins'] > 0:
            concerns.append("Presença de veios de água subterrâneos")
        
        return concerns if concerns else ["Nenhuma preocupação significativa identificada"]
    
    def _identify_priority_actions(self, geopathogenic: Dict, radiation: Dict) -> List[str]:
        """Identifica ações prioritárias"""
        actions = []
        
        if geopathogenic['total_geopathogenic_zones'] > 0:
            actions.append("Mapear zonas geopatogênicas na planta baixa")
            actions.append("Reposicionar móveis e camas fora das zonas de risco")
        
        if radiation['radon_risk'] in ['high', 'medium']:
            actions.append("Implementar sistema de ventilação adequado")
        
        return actions if actions else ["Manter monitoramento periódico"]


# Função auxiliar para uso direto
def analyze_geobiology(latitude: float, longitude: float, area_width: float, 
                       area_height: float, soil_type: str = 'unknown',
                       geological_data: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Função auxiliar para realizar análise geobiológica completa
    
    Args:
        latitude: Latitude do local
        longitude: Longitude do local
        area_width: Largura da área em metros
        area_height: Altura da área em metros
        soil_type: Tipo de solo
        geological_data: Dados geológicos adicionais
        
    Returns:
        Análise geobiológica completa
    """
    analyzer = GeobiologyAnalyzer(latitude, longitude)
    return analyzer.perform_complete_analysis(area_width, area_height, soil_type, geological_data)


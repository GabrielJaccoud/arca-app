"""
Módulo de Análise de Campos Eletromagnéticos (EMF) para o Sistema ARCA
Analisa fontes de radiação eletromagnética e avalia exposição
"""

import math
import json
from typing import Dict, List, Tuple, Any
from datetime import datetime


class EMFAnalyzer:
    """
    Analisador de Campos Eletromagnéticos (CEM/EMF)
    """
    
    # Limites de segurança (em microTesla - μT)
    SAFE_LIMIT_RESIDENTIAL = 0.4  # μT (ICNIRP para exposição contínua)
    SAFE_LIMIT_WORKPLACE = 1.0  # μT
    
    # Distâncias mínimas recomendadas (em metros)
    MIN_DISTANCE_CELL_TOWER = 300
    MIN_DISTANCE_POWER_LINE_HIGH = 200
    MIN_DISTANCE_POWER_LINE_MEDIUM = 100
    MIN_DISTANCE_TRANSFORMER = 50
    
    def __init__(self, latitude: float, longitude: float):
        """
        Inicializa o analisador de EMF
        
        Args:
            latitude: Latitude do local em graus decimais
            longitude: Longitude do local em graus decimais
        """
        self.latitude = latitude
        self.longitude = longitude
        self.analysis_date = datetime.now()
        
    def detect_cell_towers(self, search_radius_km: float = 1.0) -> Dict[str, Any]:
        """
        Detecta torres de celular próximas
        
        Args:
            search_radius_km: Raio de busca em quilômetros
            
        Returns:
            Informações sobre torres de celular detectadas
        """
        # Em produção, isso seria integrado com APIs de dados de antenas
        # Por ora, simulação baseada em densidade urbana
        
        urban_density = self._estimate_urban_density()
        
        # Estimar número de torres baseado em densidade
        estimated_towers = int(urban_density * search_radius_km * 3)
        
        towers = []
        for i in range(min(estimated_towers, 10)):  # Limitar a 10 torres
            distance = 200 + (i * 100)  # Distâncias variadas
            
            # Calcular exposição EMF baseado na distância
            emf_exposure = self._calculate_tower_emf(distance)
            
            towers.append({
                'id': f'tower_{i+1}',
                'type': 'cell_tower',
                'distance_meters': distance,
                'estimated_power': '100-500W',
                'frequency_bands': ['4G', '5G'],
                'emf_exposure_uT': emf_exposure,
                'safety_status': 'safe' if distance >= self.MIN_DISTANCE_CELL_TOWER else 'caution',
                'recommendation': self._generate_tower_recommendation(distance)
            })
        
        return {
            'towers_detected': len(towers),
            'towers': towers,
            'search_radius_km': search_radius_km,
            'closest_tower_distance': min([t['distance_meters'] for t in towers]) if towers else None,
            'total_emf_contribution': sum([t['emf_exposure_uT'] for t in towers]),
            'overall_risk': self._assess_tower_risk(towers)
        }
    
    def detect_power_lines(self, search_radius_km: float = 0.5) -> Dict[str, Any]:
        """
        Detecta linhas de transmissão de energia próximas
        
        Args:
            search_radius_km: Raio de busca em quilômetros
            
        Returns:
            Informações sobre linhas de transmissão detectadas
        """
        # Simulação baseada em área urbana/rural
        urban_density = self._estimate_urban_density()
        
        power_lines = []
        
        # Linha de alta tensão (se em área menos densa)
        if urban_density < 0.7:
            distance_high = 500  # metros
            voltage_high = 138000  # 138kV
            
            power_lines.append({
                'id': 'powerline_high_1',
                'type': 'high_voltage',
                'voltage_kV': voltage_high / 1000,
                'distance_meters': distance_high,
                'emf_exposure_uT': self._calculate_powerline_emf(voltage_high, distance_high),
                'safety_status': 'safe' if distance_high >= self.MIN_DISTANCE_POWER_LINE_HIGH else 'caution',
                'recommendation': self._generate_powerline_recommendation(voltage_high, distance_high)
            })
        
        # Linhas de média tensão (sempre presentes em áreas urbanas)
        distance_medium = 150  # metros
        voltage_medium = 13800  # 13.8kV
        
        power_lines.append({
            'id': 'powerline_medium_1',
            'type': 'medium_voltage',
            'voltage_kV': voltage_medium / 1000,
            'distance_meters': distance_medium,
            'emf_exposure_uT': self._calculate_powerline_emf(voltage_medium, distance_medium),
            'safety_status': 'safe' if distance_medium >= self.MIN_DISTANCE_POWER_LINE_MEDIUM else 'caution',
            'recommendation': self._generate_powerline_recommendation(voltage_medium, distance_medium)
        })
        
        return {
            'power_lines_detected': len(power_lines),
            'power_lines': power_lines,
            'search_radius_km': search_radius_km,
            'closest_line_distance': min([pl['distance_meters'] for pl in power_lines]) if power_lines else None,
            'total_emf_contribution': sum([pl['emf_exposure_uT'] for pl in power_lines]),
            'overall_risk': self._assess_powerline_risk(power_lines)
        }
    
    def detect_transformers(self, search_radius_m: float = 100) -> Dict[str, Any]:
        """
        Detecta transformadores próximos
        
        Args:
            search_radius_m: Raio de busca em metros
            
        Returns:
            Informações sobre transformadores detectados
        """
        urban_density = self._estimate_urban_density()
        
        # Estimar número de transformadores
        num_transformers = int(urban_density * 2)
        
        transformers = []
        for i in range(min(num_transformers, 5)):
            distance = 30 + (i * 20)  # Distâncias variadas
            power_kVA = 75 + (i * 25)  # Potências variadas
            
            transformers.append({
                'id': f'transformer_{i+1}',
                'type': 'distribution_transformer',
                'power_kVA': power_kVA,
                'distance_meters': distance,
                'emf_exposure_uT': self._calculate_transformer_emf(power_kVA, distance),
                'safety_status': 'safe' if distance >= self.MIN_DISTANCE_TRANSFORMER else 'caution',
                'recommendation': self._generate_transformer_recommendation(distance)
            })
        
        return {
            'transformers_detected': len(transformers),
            'transformers': transformers,
            'search_radius_m': search_radius_m,
            'closest_transformer_distance': min([t['distance_meters'] for t in transformers]) if transformers else None,
            'total_emf_contribution': sum([t['emf_exposure_uT'] for t in transformers]),
            'overall_risk': self._assess_transformer_risk(transformers)
        }
    
    def analyze_internal_sources(self, appliances: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Analisa fontes internas de EMF (eletrodomésticos, eletrônicos)
        
        Args:
            appliances: Lista de eletrodomésticos e suas posições
            
        Returns:
            Análise de fontes internas de EMF
        """
        # Valores típicos de EMF de eletrodomésticos (em μT a 30cm)
        typical_emf_values = {
            'microwave': 4.0,
            'refrigerator': 0.3,
            'washing_machine': 0.8,
            'tv': 0.2,
            'computer': 0.1,
            'wifi_router': 0.05,
            'electric_stove': 1.5,
            'hair_dryer': 7.0,
            'vacuum_cleaner': 2.0,
            'air_conditioner': 0.5
        }
        
        if appliances is None:
            # Lista padrão de eletrodomésticos em uma residência
            appliances = [
                {'type': 'refrigerator', 'location': 'kitchen'},
                {'type': 'microwave', 'location': 'kitchen'},
                {'type': 'tv', 'location': 'living_room'},
                {'type': 'wifi_router', 'location': 'living_room'},
                {'type': 'washing_machine', 'location': 'laundry'},
                {'type': 'computer', 'location': 'office'}
            ]
        
        analyzed_appliances = []
        total_exposure = 0
        
        for appliance in appliances:
            app_type = appliance.get('type', 'unknown')
            emf_value = typical_emf_values.get(app_type, 0.1)
            
            analyzed_appliances.append({
                'type': app_type,
                'location': appliance.get('location', 'unknown'),
                'emf_at_30cm_uT': emf_value,
                'emf_at_1m_uT': emf_value * 0.1,  # Decai com distância
                'safety_status': 'safe' if emf_value < 2.0 else 'caution',
                'recommendation': self._generate_appliance_recommendation(app_type, emf_value)
            })
            
            total_exposure += emf_value * 0.1  # Considerar distância média de 1m
        
        return {
            'appliances_analyzed': len(analyzed_appliances),
            'appliances': analyzed_appliances,
            'total_internal_exposure_uT': total_exposure,
            'highest_emf_source': max(analyzed_appliances, key=lambda x: x['emf_at_30cm_uT']) if analyzed_appliances else None,
            'recommendations': self._generate_internal_recommendations(analyzed_appliances)
        }
    
    def calculate_total_exposure(self, include_internal: bool = True) -> Dict[str, Any]:
        """
        Calcula exposição total a EMF
        
        Args:
            include_internal: Se deve incluir fontes internas
            
        Returns:
            Análise de exposição total
        """
        cell_towers = self.detect_cell_towers()
        power_lines = self.detect_power_lines()
        transformers = self.detect_transformers()
        
        external_exposure = (
            cell_towers['total_emf_contribution'] +
            power_lines['total_emf_contribution'] +
            transformers['total_emf_contribution']
        )
        
        internal_exposure = 0
        if include_internal:
            internal_sources = self.analyze_internal_sources()
            internal_exposure = internal_sources['total_internal_exposure_uT']
        
        total_exposure = external_exposure + internal_exposure
        
        return {
            'total_exposure_uT': total_exposure,
            'external_exposure_uT': external_exposure,
            'internal_exposure_uT': internal_exposure,
            'safe_limit_residential_uT': self.SAFE_LIMIT_RESIDENTIAL,
            'exposure_percentage': (total_exposure / self.SAFE_LIMIT_RESIDENTIAL) * 100,
            'safety_status': self._assess_total_safety(total_exposure),
            'compliance': total_exposure <= self.SAFE_LIMIT_RESIDENTIAL,
            'risk_level': self._calculate_risk_level(total_exposure)
        }
    
    def perform_complete_analysis(self, include_internal: bool = True,
                                   appliances: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Realiza análise completa de EMF
        
        Args:
            include_internal: Se deve incluir fontes internas
            appliances: Lista de eletrodomésticos (opcional)
            
        Returns:
            Análise completa de EMF
        """
        analysis = {
            'location': {
                'latitude': self.latitude,
                'longitude': self.longitude
            },
            'analysis_date': self.analysis_date.isoformat(),
            'external_sources': {
                'cell_towers': self.detect_cell_towers(),
                'power_lines': self.detect_power_lines(),
                'transformers': self.detect_transformers()
            },
            'total_exposure': self.calculate_total_exposure(include_internal)
        }
        
        if include_internal:
            analysis['internal_sources'] = self.analyze_internal_sources(appliances)
        
        analysis['overall_assessment'] = self._generate_overall_assessment(analysis)
        analysis['recommendations'] = self._generate_comprehensive_recommendations(analysis)
        
        return analysis
    
    # Métodos auxiliares privados
    
    def _estimate_urban_density(self) -> float:
        """Estima densidade urbana (0-1)"""
        # Simulação - em produção, usar dados de densidade populacional
        # Rio das Ostras, RJ tem densidade média-baixa
        if -23 <= self.latitude <= -22 and -43 <= self.longitude <= -41:
            return 0.5  # Densidade média
        return 0.3
    
    def _calculate_tower_emf(self, distance_m: float) -> float:
        """Calcula EMF de torre de celular baseado na distância"""
        # Fórmula simplificada: EMF decai com quadrado da distância
        base_power = 0.5  # μT a 100m
        reference_distance = 100
        
        if distance_m < reference_distance:
            return base_power * (reference_distance / distance_m) ** 2
        else:
            return base_power * (reference_distance / distance_m) ** 2
    
    def _calculate_powerline_emf(self, voltage_V: float, distance_m: float) -> float:
        """Calcula EMF de linha de transmissão"""
        # Fórmula simplificada baseada em voltagem e distância
        base_emf = (voltage_V / 100000) * 10  # Normalizar
        distance_factor = 100 / max(distance_m, 10)  # Evitar divisão por zero
        
        return base_emf * distance_factor
    
    def _calculate_transformer_emf(self, power_kVA: float, distance_m: float) -> float:
        """Calcula EMF de transformador"""
        base_emf = (power_kVA / 100) * 2
        distance_factor = 10 / max(distance_m, 5)
        
        return base_emf * distance_factor
    
    def _generate_tower_recommendation(self, distance_m: float) -> str:
        """Gera recomendação para torre de celular"""
        if distance_m < self.MIN_DISTANCE_CELL_TOWER:
            return f"Torre muito próxima. Recomenda-se distância mínima de {self.MIN_DISTANCE_CELL_TOWER}m"
        return "Distância adequada. Exposição dentro dos limites seguros."
    
    def _generate_powerline_recommendation(self, voltage_V: float, distance_m: float) -> str:
        """Gera recomendação para linha de transmissão"""
        min_dist = self.MIN_DISTANCE_POWER_LINE_HIGH if voltage_V > 50000 else self.MIN_DISTANCE_POWER_LINE_MEDIUM
        
        if distance_m < min_dist:
            return f"Linha de transmissão muito próxima. Recomenda-se distância mínima de {min_dist}m"
        return "Distância adequada. Exposição dentro dos limites seguros."
    
    def _generate_transformer_recommendation(self, distance_m: float) -> str:
        """Gera recomendação para transformador"""
        if distance_m < self.MIN_DISTANCE_TRANSFORMER:
            return f"Transformador muito próximo. Recomenda-se distância mínima de {self.MIN_DISTANCE_TRANSFORMER}m"
        return "Distância adequada. Exposição aceitável."
    
    def _generate_appliance_recommendation(self, appliance_type: str, emf_value: float) -> str:
        """Gera recomendação para eletrodoméstico"""
        if emf_value > 5.0:
            return f"Alto EMF. Manter distância mínima de 1m durante uso."
        elif emf_value > 2.0:
            return "EMF moderado. Evitar exposição prolongada próxima."
        return "EMF baixo. Uso normal seguro."
    
    def _assess_tower_risk(self, towers: List[Dict]) -> str:
        """Avalia risco geral de torres"""
        if not towers:
            return 'low'
        
        closest = min([t['distance_meters'] for t in towers])
        if closest < self.MIN_DISTANCE_CELL_TOWER:
            return 'medium'
        return 'low'
    
    def _assess_powerline_risk(self, power_lines: List[Dict]) -> str:
        """Avalia risco geral de linhas de transmissão"""
        if not power_lines:
            return 'low'
        
        for line in power_lines:
            if line['safety_status'] == 'caution':
                return 'medium'
        return 'low'
    
    def _assess_transformer_risk(self, transformers: List[Dict]) -> str:
        """Avalia risco geral de transformadores"""
        if not transformers:
            return 'low'
        
        closest = min([t['distance_meters'] for t in transformers])
        if closest < self.MIN_DISTANCE_TRANSFORMER:
            return 'medium'
        return 'low'
    
    def _assess_total_safety(self, total_exposure: float) -> str:
        """Avalia segurança total baseado na exposição"""
        if total_exposure <= self.SAFE_LIMIT_RESIDENTIAL:
            return 'safe'
        elif total_exposure <= self.SAFE_LIMIT_WORKPLACE:
            return 'caution'
        else:
            return 'unsafe'
    
    def _calculate_risk_level(self, total_exposure: float) -> str:
        """Calcula nível de risco"""
        percentage = (total_exposure / self.SAFE_LIMIT_RESIDENTIAL) * 100
        
        if percentage <= 50:
            return 'low'
        elif percentage <= 100:
            return 'medium'
        else:
            return 'high'
    
    def _generate_internal_recommendations(self, appliances: List[Dict]) -> List[str]:
        """Gera recomendações para fontes internas"""
        recommendations = []
        
        high_emf_appliances = [a for a in appliances if a['emf_at_30cm_uT'] > 2.0]
        
        if high_emf_appliances:
            recommendations.append("Manter distância de aparelhos de alto EMF durante uso")
            recommendations.append("Desligar aparelhos quando não estiverem em uso")
        
        recommendations.append("Posicionar roteador Wi-Fi longe de áreas de permanência prolongada")
        recommendations.append("Evitar dormir próximo a despertadores elétricos")
        
        return recommendations
    
    def _generate_overall_assessment(self, analysis: Dict) -> Dict[str, Any]:
        """Gera avaliação geral"""
        total_exp = analysis['total_exposure']
        
        # Calcular score (0-100)
        score = 100 - (total_exp['exposure_percentage'])
        score = max(0, min(100, score))
        
        return {
            'emf_health_score': score,
            'risk_level': total_exp['risk_level'],
            'compliance_status': 'compliant' if total_exp['compliance'] else 'non_compliant',
            'main_concerns': self._identify_main_emf_concerns(analysis),
            'suitable_for_habitation': total_exp['compliance']
        }
    
    def _identify_main_emf_concerns(self, analysis: Dict) -> List[str]:
        """Identifica principais preocupações de EMF"""
        concerns = []
        
        ext = analysis['external_sources']
        
        if ext['cell_towers']['overall_risk'] != 'low':
            concerns.append("Torres de celular próximas")
        
        if ext['power_lines']['overall_risk'] != 'low':
            concerns.append("Linhas de transmissão próximas")
        
        if ext['transformers']['overall_risk'] != 'low':
            concerns.append("Transformadores próximos")
        
        if analysis['total_exposure']['risk_level'] == 'high':
            concerns.append("Exposição total acima dos limites recomendados")
        
        return concerns if concerns else ["Nenhuma preocupação significativa identificada"]
    
    def _generate_comprehensive_recommendations(self, analysis: Dict) -> List[str]:
        """Gera recomendações abrangentes"""
        recommendations = []
        
        total_exp = analysis['total_exposure']
        
        if total_exp['risk_level'] in ['medium', 'high']:
            recommendations.append("Considerar blindagem EMF em paredes e tetos")
            recommendations.append("Usar materiais de construção com propriedades de blindagem")
        
        if 'internal_sources' in analysis:
            recommendations.extend(self._generate_internal_recommendations(
                analysis['internal_sources']['appliances']
            ))
        
        recommendations.append("Realizar medições profissionais de EMF antes da ocupação")
        recommendations.append("Implementar zonas de baixo EMF para quartos e áreas de descanso")
        
        return recommendations


# Função auxiliar para uso direto
def analyze_emf(latitude: float, longitude: float, 
                include_internal: bool = True,
                appliances: List[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Função auxiliar para realizar análise completa de EMF
    
    Args:
        latitude: Latitude do local
        longitude: Longitude do local
        include_internal: Se deve incluir fontes internas
        appliances: Lista de eletrodomésticos (opcional)
        
    Returns:
        Análise completa de EMF
    """
    analyzer = EMFAnalyzer(latitude, longitude)
    return analyzer.perform_complete_analysis(include_internal, appliances)


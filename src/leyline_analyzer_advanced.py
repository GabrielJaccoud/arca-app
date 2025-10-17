"""
Módulo Avançado de Análise de Linhas Ley - Sistema ARCA v3.1
Análise aprofundada de linhas ley, sítios sagrados e geografia energética

Referências:
- Alfred Watkins: "The Old Straight Track" (1925)
- Paul Devereux: "Symbolic Landscapes" (1992)
- Sítios Naturais Sagrados no Brasil (Fernandes-Pinto & Irving, 2015)
- Earth Energy Grids Research
"""

import math
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import json


class SacredSiteDatabase:
    """
    Base de dados de sítios sagrados do Brasil e regiões próximas
    Dados compilados de fontes históricas e antropológicas
    """
    
    SACRED_SITES_BRAZIL = [
        # Rio de Janeiro
        {
            'name': 'Pedra da Gávea',
            'latitude': -23.0122,
            'longitude': -43.2844,
            'type': 'natural_formation',
            'significance': 'Formação rochosa com possíveis inscrições fenícias',
            'energy_type': 'earth',
            'power_level': 9
        },
        {
            'name': 'Pão de Açúcar',
            'latitude': -22.9489,
            'longitude': -43.1572,
            'type': 'natural_formation',
            'significance': 'Marco geográfico e energético da Baía de Guanabara',
            'energy_type': 'earth_fire',
            'power_level': 8
        },
        {
            'name': 'Mosteiro de São Bento - Rio',
            'latitude': -22.8953,
            'longitude': -43.1755,
            'type': 'monastery',
            'significance': 'Mosteiro beneditino desde 1590',
            'energy_type': 'spiritual',
            'power_level': 7
        },
        {
            'name': 'Igreja da Penha',
            'latitude': -22.8417,
            'longitude': -43.2831,
            'type': 'church',
            'significance': 'Santuário no alto de formação rochosa',
            'energy_type': 'spiritual_earth',
            'power_level': 7
        },
        {
            'name': 'Igreja de Nossa Senhora da Conceição - Rio das Ostras',
            'latitude': -22.5264,
            'longitude': -41.9456,
            'type': 'church',
            'significance': 'Igreja histórica da cidade',
            'energy_type': 'spiritual',
            'power_level': 5
        },
        
        # Minas Gerais
        {
            'name': 'Serra da Piedade',
            'latitude': -19.7917,
            'longitude': -43.6833,
            'type': 'mountain_sanctuary',
            'significance': 'Montanha sagrada com santuário no topo',
            'energy_type': 'earth_spiritual',
            'power_level': 9
        },
        {
            'name': 'Ouro Preto - Centro Histórico',
            'latitude': -20.3856,
            'longitude': -43.5039,
            'type': 'historical_sacred',
            'significance': 'Cidade histórica com múltiplas igrejas barrocas',
            'energy_type': 'spiritual_historical',
            'power_level': 8
        },
        
        # São Paulo
        {
            'name': 'Pico do Jaraguá',
            'latitude': -23.4567,
            'longitude': -46.7656,
            'type': 'mountain',
            'significance': 'Ponto mais alto da cidade de São Paulo',
            'energy_type': 'earth',
            'power_level': 7
        },
        {
            'name': 'Catedral da Sé',
            'latitude': -23.5505,
            'longitude': -46.6333,
            'type': 'cathedral',
            'significance': 'Principal catedral de São Paulo',
            'energy_type': 'spiritual',
            'power_level': 7
        },
        
        # Bahia
        {
            'name': 'Igreja do Bonfim',
            'latitude': -12.9686,
            'longitude': -38.5108,
            'type': 'church',
            'significance': 'Importante centro de peregrinação',
            'energy_type': 'spiritual',
            'power_level': 8
        },
        {
            'name': 'Chapada Diamantina',
            'latitude': -12.5667,
            'longitude': -41.3667,
            'type': 'natural_formation',
            'significance': 'Formações rochosas e cachoeiras sagradas',
            'energy_type': 'water_earth',
            'power_level': 9
        },
        
        # Goiás
        {
            'name': 'Vale do Amanhecer',
            'latitude': -15.9167,
            'longitude': -47.9833,
            'type': 'spiritual_community',
            'significance': 'Comunidade espiritual eclética',
            'energy_type': 'spiritual',
            'power_level': 8
        },
        {
            'name': 'Alto Paraíso de Goiás',
            'latitude': -14.1333,
            'longitude': -47.5167,
            'type': 'spiritual_center',
            'significance': 'Centro de espiritualidade e cristais',
            'energy_type': 'crystal_spiritual',
            'power_level': 9
        },
        
        # Mato Grosso
        {
            'name': 'Chapada dos Guimarães',
            'latitude': -15.4667,
            'longitude': -55.7500,
            'type': 'natural_formation',
            'significance': 'Centro geodésico da América do Sul',
            'energy_type': 'earth',
            'power_level': 10
        },
        
        # Amazonas
        {
            'name': 'Encontro das Águas',
            'latitude': -3.1333,
            'longitude': -59.9000,
            'type': 'natural_phenomenon',
            'significance': 'Encontro dos rios Negro e Solimões',
            'energy_type': 'water',
            'power_level': 8
        },
        
        # Pernambuco
        {
            'name': 'Alto da Sé - Olinda',
            'latitude': -8.0089,
            'longitude': -34.8553,
            'type': 'historical_sacred',
            'significance': 'Centro histórico e religioso',
            'energy_type': 'spiritual_historical',
            'power_level': 7
        },
        
        # Paraná
        {
            'name': 'Cataratas do Iguaçu',
            'latitude': -25.6953,
            'longitude': -54.4367,
            'type': 'natural_formation',
            'significance': 'Quedas d\'água monumentais',
            'energy_type': 'water',
            'power_level': 10
        },
        
        # Santa Catarina
        {
            'name': 'Morro do Cambirela',
            'latitude': -27.7167,
            'longitude': -48.9500,
            'type': 'mountain',
            'significance': 'Montanha sagrada para povos indígenas',
            'energy_type': 'earth',
            'power_level': 7
        },
        
        # Rio Grande do Sul
        {
            'name': 'Sítio Arqueológico de São Miguel das Missões',
            'latitude': -28.5550,
            'longitude': -54.5567,
            'type': 'archaeological',
            'significance': 'Ruínas de missões jesuíticas',
            'energy_type': 'historical_spiritual',
            'power_level': 8
        }
    ]
    
    @classmethod
    def find_nearby_sites(cls, latitude: float, longitude: float, 
                         radius_km: float = 50.0) -> List[Dict]:
        """
        Encontra sítios sagrados próximos a uma localização
        
        Args:
            latitude: Latitude do local
            longitude: Longitude do local
            radius_km: Raio de busca em quilômetros
        
        Retorna:
            Lista de sítios sagrados encontrados
        """
        nearby_sites = []
        
        for site in cls.SACRED_SITES_BRAZIL:
            distance = cls._calculate_distance(
                latitude, longitude,
                site['latitude'], site['longitude']
            )
            
            if distance <= radius_km:
                site_copy = site.copy()
                site_copy['distance_km'] = round(distance, 2)
                site_copy['cardinal_direction'] = cls._calculate_direction(
                    latitude, longitude,
                    site['latitude'], site['longitude']
                )
                site_copy['azimuth'] = cls._calculate_azimuth(
                    latitude, longitude,
                    site['latitude'], site['longitude']
                )
                nearby_sites.append(site_copy)
        
        # Ordenar por distância
        nearby_sites.sort(key=lambda x: x['distance_km'])
        
        return nearby_sites
    
    @staticmethod
    def _calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calcula distância entre dois pontos usando fórmula de Haversine"""
        R = 6371  # Raio da Terra em km
        
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lon = math.radians(lon2 - lon1)
        
        a = math.sin(delta_lat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        
        return R * c
    
    @staticmethod
    def _calculate_direction(lat1: float, lon1: float, lat2: float, lon2: float) -> str:
        """Calcula direção cardeal entre dois pontos"""
        azimuth = SacredSiteDatabase._calculate_azimuth(lat1, lon1, lat2, lon2)
        
        directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
        index = round(azimuth / 45) % 8
        
        return directions[index]
    
    @staticmethod
    def _calculate_azimuth(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calcula azimute entre dois pontos"""
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lon = math.radians(lon2 - lon1)
        
        y = math.sin(delta_lon) * math.cos(lat2_rad)
        x = math.cos(lat1_rad) * math.sin(lat2_rad) - math.sin(lat1_rad) * math.cos(lat2_rad) * math.cos(delta_lon)
        
        azimuth = math.degrees(math.atan2(y, x))
        
        return (azimuth + 360) % 360


class AdvancedLeyLineAnalyzer:
    """Analisador avançado de linhas ley e geografia sagrada"""
    
    def __init__(self, latitude: float, longitude: float, radius_km: float = 50.0):
        """
        Inicializa o analisador de linhas ley
        
        Args:
            latitude: Latitude do local
            longitude: Longitude do local
            radius_km: Raio de busca para sítios sagrados
        """
        self.latitude = latitude
        self.longitude = longitude
        self.radius_km = radius_km
        
    def find_sacred_sites(self) -> Dict:
        """
        Encontra sítios sagrados próximos
        
        Retorna:
            Dicionário com sítios sagrados encontrados
        """
        sites = SacredSiteDatabase.find_nearby_sites(
            self.latitude, self.longitude, self.radius_km
        )
        
        closest_site = sites[0] if sites else None
        
        # Classificar por tipo
        sites_by_type = {}
        for site in sites:
            site_type = site['type']
            if site_type not in sites_by_type:
                sites_by_type[site_type] = []
            sites_by_type[site_type].append(site)
        
        # Calcular energia total da região
        total_power = sum(site['power_level'] for site in sites)
        avg_power = total_power / len(sites) if sites else 0
        
        return {
            'total_found': len(sites),
            'sites': sites,
            'closest_site': closest_site,
            'sites_by_type': sites_by_type,
            'total_power_level': total_power,
            'average_power_level': round(avg_power, 2),
            'search_radius_km': self.radius_km
        }
    
    def identify_ley_lines(self, sacred_sites: Dict) -> Dict:
        """
        Identifica possíveis linhas ley conectando sítios sagrados
        
        Args:
            sacred_sites: Dados de sítios sagrados
        
        Retorna:
            Dicionário com linhas ley identificadas
        """
        sites = sacred_sites['sites']
        ley_lines = []
        
        # Procurar alinhamentos de 3 ou mais sítios
        for i in range(len(sites)):
            for j in range(i+1, len(sites)):
                for k in range(j+1, len(sites)):
                    if self._are_aligned(sites[i], sites[j], sites[k]):
                        ley_line = {
                            'id': f'ley_{len(ley_lines)+1}',
                            'sites': [sites[i]['name'], sites[j]['name'], sites[k]['name']],
                            'site_count': 3,
                            'total_length_km': self._calculate_line_length([sites[i], sites[j], sites[k]]),
                            'azimuth': SacredSiteDatabase._calculate_azimuth(
                                sites[i]['latitude'], sites[i]['longitude'],
                                sites[k]['latitude'], sites[k]['longitude']
                            ),
                            'power_level': sum(s['power_level'] for s in [sites[i], sites[j], sites[k]]) / 3,
                            'passes_through_location': self._line_passes_through(
                                sites[i], sites[k], self.latitude, self.longitude
                            )
                        }
                        ley_lines.append(ley_line)
        
        # Remover duplicatas
        unique_ley_lines = []
        seen_combinations = set()
        
        for line in ley_lines:
            sites_tuple = tuple(sorted(line['sites']))
            if sites_tuple not in seen_combinations:
                seen_combinations.add(sites_tuple)
                unique_ley_lines.append(line)
        
        # Identificar linhas que passam pelo local
        lines_passing_through = [line for line in unique_ley_lines if line['passes_through_location']]
        
        return {
            'ley_lines_identified': len(unique_ley_lines),
            'ley_lines': unique_ley_lines,
            'lines_passing_through': lines_passing_through,
            'location_on_ley_line': len(lines_passing_through) > 0,
            'description': 'Linhas ley são alinhamentos geométricos entre sítios sagrados'
        }
    
    def _are_aligned(self, site1: Dict, site2: Dict, site3: Dict, tolerance_degrees: float = 2.0) -> bool:
        """
        Verifica se três sítios estão alinhados
        
        Args:
            site1, site2, site3: Sítios a verificar
            tolerance_degrees: Tolerância em graus para considerar alinhamento
        
        Retorna:
            True se estão alinhados
        """
        # Calcular azimutes
        azimuth_12 = SacredSiteDatabase._calculate_azimuth(
            site1['latitude'], site1['longitude'],
            site2['latitude'], site2['longitude']
        )
        
        azimuth_23 = SacredSiteDatabase._calculate_azimuth(
            site2['latitude'], site2['longitude'],
            site3['latitude'], site3['longitude']
        )
        
        # Verificar se azimutes são similares (considerando wrap-around em 360°)
        diff = abs(azimuth_12 - azimuth_23)
        if diff > 180:
            diff = 360 - diff
        
        return diff <= tolerance_degrees
    
    def _calculate_line_length(self, sites: List[Dict]) -> float:
        """Calcula comprimento total de uma linha ley"""
        total_length = 0
        for i in range(len(sites) - 1):
            total_length += SacredSiteDatabase._calculate_distance(
                sites[i]['latitude'], sites[i]['longitude'],
                sites[i+1]['latitude'], sites[i+1]['longitude']
            )
        return round(total_length, 2)
    
    def _line_passes_through(self, site1: Dict, site2: Dict, lat: float, lon: float, 
                            tolerance_km: float = 0.5) -> bool:
        """
        Verifica se uma linha passa próximo a um ponto
        
        Args:
            site1, site2: Sítios que definem a linha
            lat, lon: Coordenadas do ponto
            tolerance_km: Tolerância em km
        
        Retorna:
            True se a linha passa próximo ao ponto
        """
        # Calcular distância perpendicular do ponto à linha
        # Usando fórmula de distância de ponto a linha em coordenadas geográficas (simplificada)
        
        distance_to_site1 = SacredSiteDatabase._calculate_distance(
            lat, lon, site1['latitude'], site1['longitude']
        )
        
        distance_to_site2 = SacredSiteDatabase._calculate_distance(
            lat, lon, site2['latitude'], site2['longitude']
        )
        
        line_length = SacredSiteDatabase._calculate_distance(
            site1['latitude'], site1['longitude'],
            site2['latitude'], site2['longitude']
        )
        
        # Se o ponto está muito longe de ambos os sítios, não está na linha
        if distance_to_site1 > line_length + tolerance_km or distance_to_site2 > line_length + tolerance_km:
            return False
        
        # Cálculo aproximado de distância perpendicular
        s = (distance_to_site1 + distance_to_site2 + line_length) / 2
        area = math.sqrt(max(0, s * (s - distance_to_site1) * (s - distance_to_site2) * (s - line_length)))
        perpendicular_distance = (2 * area) / line_length if line_length > 0 else float('inf')
        
        return perpendicular_distance <= tolerance_km
    
    def detect_energy_vortices(self, sacred_sites: Dict, ley_lines: Dict) -> Dict:
        """
        Detecta vórtices energéticos (cruzamentos de múltiplas linhas ley)
        
        Args:
            sacred_sites: Dados de sítios sagrados
            ley_lines: Dados de linhas ley
        
        Retorna:
            Dicionário com vórtices detectados
        """
        vortices = []
        
        # Procurar sítios que são cruzamentos de múltiplas linhas
        for site in sacred_sites['sites']:
            lines_through_site = 0
            connected_lines = []
            
            for line in ley_lines['ley_lines']:
                if site['name'] in line['sites']:
                    lines_through_site += 1
                    connected_lines.append(line['id'])
            
            if lines_through_site >= 2:
                vortex = {
                    'location': site['name'],
                    'latitude': site['latitude'],
                    'longitude': site['longitude'],
                    'ley_lines_count': lines_through_site,
                    'connected_lines': connected_lines,
                    'power_level': site['power_level'] * lines_through_site,
                    'vortex_strength': self._classify_vortex_strength(lines_through_site),
                    'distance_from_location_km': site['distance_km']
                }
                vortices.append(vortex)
        
        # Verificar se o local está em um vórtice
        location_is_vortex = any(
            vortex['distance_from_location_km'] < 2.0 for vortex in vortices
        )
        
        vortex_strength = 'none'
        if location_is_vortex:
            closest_vortex = min(vortices, key=lambda v: v['distance_from_location_km'])
            vortex_strength = closest_vortex['vortex_strength']
        
        return {
            'vortices_detected': len(vortices),
            'vortices': vortices,
            'location_is_vortex': location_is_vortex,
            'vortex_strength': vortex_strength,
            'description': 'Vórtices são pontos de convergência de múltiplas linhas ley'
        }
    
    def _classify_vortex_strength(self, line_count: int) -> str:
        """Classifica força de um vórtice baseado no número de linhas"""
        if line_count >= 4:
            return 'strong'
        elif line_count == 3:
            return 'medium'
        else:
            return 'weak'
    
    def calculate_astronomical_alignments(self) -> Dict:
        """
        Calcula alinhamentos astronômicos para o local
        
        Retorna:
            Dicionário com alinhamentos astronômicos
        """
        # Calcular azimutes solares para solstícios e equinócios
        # Fórmulas baseadas em latitude
        
        lat_rad = math.radians(self.latitude)
        
        # Declinação solar nos solstícios (±23.44°)
        declination_summer = math.radians(23.44)
        declination_winter = math.radians(-23.44)
        
        # Azimute do nascer do sol no solstício de verão
        summer_sunrise_azimuth = math.degrees(math.acos(
            -math.sin(declination_summer) / math.cos(lat_rad)
        ))
        
        # Azimute do nascer do sol no solstício de inverno
        winter_sunrise_azimuth = math.degrees(math.acos(
            -math.sin(declination_winter) / math.cos(lat_rad)
        ))
        
        # Equinócios (nascer do sol exatamente a Leste)
        equinox_sunrise_azimuth = 90.0
        equinox_sunset_azimuth = 270.0
        
        return {
            'summer_solstice': {
                'date': 'December 21-22 (Southern Hemisphere)',
                'sunrise_azimuth': round(summer_sunrise_azimuth, 2),
                'sunset_azimuth': round(360 - summer_sunrise_azimuth, 2),
                'significance': 'Dia mais longo do ano'
            },
            'winter_solstice': {
                'date': 'June 20-21 (Southern Hemisphere)',
                'sunrise_azimuth': round(winter_sunrise_azimuth, 2),
                'sunset_azimuth': round(360 - winter_sunrise_azimuth, 2),
                'significance': 'Dia mais curto do ano'
            },
            'equinoxes': {
                'dates': 'March 20-21 and September 22-23',
                'sunrise_azimuth': equinox_sunrise_azimuth,
                'sunset_azimuth': equinox_sunset_azimuth,
                'significance': 'Dia e noite com duração igual'
            },
            'optimal_building_orientation': {
                'primary_axis': 'north-south',
                'recommended_entrance': 'east',
                'solar_alignment': 'Orientar eixo principal N-S para maximizar luz solar'
            }
        }
    
    def analyze(self) -> Dict:
        """
        Realiza análise completa de linhas ley e geografia sagrada
        
        Retorna:
            Dicionário com análise completa
        """
        # Encontrar sítios sagrados
        sacred_sites = self.find_sacred_sites()
        
        # Identificar linhas ley
        ley_lines = self.identify_ley_lines(sacred_sites)
        
        # Detectar vórtices
        vortices = self.detect_energy_vortices(sacred_sites, ley_lines)
        
        # Calcular alinhamentos astronômicos
        astronomical = self.calculate_astronomical_alignments()
        
        # Calcular score de potencial energético
        energetic_score = self._calculate_energetic_score(sacred_sites, ley_lines, vortices)
        
        # Classificar geografia sagrada
        sacred_rating = self._classify_sacred_geography(energetic_score, sacred_sites, vortices)
        
        return {
            'location': {
                'latitude': self.latitude,
                'longitude': self.longitude,
                'search_radius_km': self.radius_km
            },
            'sacred_sites': sacred_sites,
            'ley_lines': ley_lines,
            'energy_vortices': vortices,
            'astronomical_alignments': astronomical,
            'overall_assessment': {
                'energetic_potential_score': energetic_score,
                'sacred_geography_rating': sacred_rating,
                'ideal_for_sacred_architecture': energetic_score >= 70,
                'main_features': self._identify_main_features(sacred_sites, ley_lines, vortices)
            },
            'recommendations': self._generate_recommendations(sacred_sites, ley_lines, vortices, astronomical)
        }
    
    def _calculate_energetic_score(self, sacred_sites: Dict, ley_lines: Dict, vortices: Dict) -> int:
        """Calcula score de potencial energético (0-100)"""
        score = 50  # Base
        
        # Pontos por sítios próximos
        score += min(sacred_sites['total_found'] * 5, 20)
        
        # Pontos por poder médio dos sítios
        score += min(sacred_sites['average_power_level'] * 2, 10)
        
        # Pontos por linhas ley
        score += min(ley_lines['ley_lines_identified'] * 10, 20)
        
        # Bônus se local está em linha ley
        if ley_lines['location_on_ley_line']:
            score += 15
        
        # Pontos por vórtices
        score += min(vortices['vortices_detected'] * 5, 10)
        
        # Bônus se local é vórtice
        if vortices['location_is_vortex']:
            if vortices['vortex_strength'] == 'strong':
                score += 20
            elif vortices['vortex_strength'] == 'medium':
                score += 10
            else:
                score += 5
        
        return min(score, 100)
    
    def _classify_sacred_geography(self, score: int, sacred_sites: Dict, vortices: Dict) -> str:
        """Classifica a geografia sagrada do local"""
        if score >= 80:
            return 'exceptional'
        elif score >= 70:
            return 'high'
        elif score >= 50:
            return 'medium'
        else:
            return 'low'
    
    def _identify_main_features(self, sacred_sites: Dict, ley_lines: Dict, vortices: Dict) -> List[str]:
        """Identifica principais características energéticas"""
        features = []
        
        if sacred_sites['total_found'] > 0:
            features.append(f"{sacred_sites['total_found']} sítios sagrados em raio de {self.radius_km}km")
        
        if sacred_sites['closest_site']:
            features.append(f"Sítio mais próximo: {sacred_sites['closest_site']['name']} ({sacred_sites['closest_site']['distance_km']}km)")
        
        if ley_lines['location_on_ley_line']:
            features.append("Local posicionado sobre linha ley")
        
        if vortices['location_is_vortex']:
            features.append(f"Local é vórtice energético de força {vortices['vortex_strength']}")
        
        if ley_lines['ley_lines_identified'] > 0:
            features.append(f"{ley_lines['ley_lines_identified']} linhas ley identificadas")
        
        return features if features else ["Nenhuma característica energética significativa detectada"]
    
    def _generate_recommendations(self, sacred_sites: Dict, ley_lines: Dict, 
                                  vortices: Dict, astronomical: Dict) -> List[str]:
        """Gera recomendações baseadas na análise"""
        recommendations = []
        
        # Recomendações de orientação
        recommendations.append(f"Orientar edificação com eixo principal {astronomical['optimal_building_orientation']['primary_axis']}")
        recommendations.append(f"Entrada principal recomendada: {astronomical['optimal_building_orientation']['recommended_entrance']}")
        
        # Recomendações baseadas em sítios sagrados
        if sacred_sites['closest_site'] and sacred_sites['closest_site']['distance_km'] < 5:
            site = sacred_sites['closest_site']
            recommendations.append(f"Considerar peregrinação ao {site['name']} para conexão energética")
        
        # Recomendações baseadas em linhas ley
        if ley_lines['location_on_ley_line']:
            recommendations.append("Local favorável para práticas espirituais e meditação")
            recommendations.append("Criar espaço sagrado dedicado alinhado com a linha ley")
        
        # Recomendações baseadas em vórtices
        if vortices['location_is_vortex']:
            if vortices['vortex_strength'] == 'strong':
                recommendations.append("ATENÇÃO: Vórtice forte - energia intensa requer canalização adequada")
                recommendations.append("Criar jardim zen ou mandala no centro do vórtice")
            recommendations.append("Utilizar cristais de quartzo para harmonizar energia do vórtice")
        
        # Recomendações astronômicas
        recommendations.append("Criar aberturas para capturar luz solar nos equinócios")
        recommendations.append("Marcar solstícios com elementos arquitetônicos (janelas, portais)")
        
        return recommendations


def analyze_ley_lines_advanced(latitude: float, longitude: float, 
                               radius_km: float = 50.0) -> Dict:
    """
    Função wrapper para análise avançada de linhas ley
    
    Args:
        latitude: Latitude do local
        longitude: Longitude do local
        radius_km: Raio de busca em km
    
    Retorna:
        Dicionário com análise completa
    """
    analyzer = AdvancedLeyLineAnalyzer(latitude, longitude, radius_km)
    return analyzer.analyze()


"""
Módulo de Análise de Linhas Ley e Geografia Sagrada para o Sistema ARCA
Identifica alinhamentos energéticos, sítios sagrados e vórtices de energia
"""

import math
import json
from typing import Dict, List, Tuple, Any, Optional
from datetime import datetime


class LeyLineAnalyzer:
    """
    Analisador de Linhas Ley e Geografia Sagrada
    """
    
    # Raio da Terra em km
    EARTH_RADIUS_KM = 6371.0
    
    # Tolerância para alinhamentos (em graus)
    ALIGNMENT_TOLERANCE = 1.0
    
    # Distância máxima para considerar sítios próximos (em km)
    MAX_SITE_DISTANCE = 50.0
    
    def __init__(self, latitude: float, longitude: float):
        """
        Inicializa o analisador de Linhas Ley
        
        Args:
            latitude: Latitude do local em graus decimais
            longitude: Longitude do local em graus decimais
        """
        self.latitude = latitude
        self.longitude = longitude
        self.analysis_date = datetime.now()
        
    def find_sacred_sites_nearby(self, radius_km: float = 50.0) -> List[Dict[str, Any]]:
        """
        Encontra sítios sagrados e pontos de interesse próximos
        
        Args:
            radius_km: Raio de busca em quilômetros
            
        Returns:
            Lista de sítios sagrados encontrados
        """
        # Base de dados simulada de sítios sagrados no Brasil
        # Em produção, isso seria integrado com banco de dados real
        sacred_sites_database = [
            {
                'name': 'Igreja de Nossa Senhora da Conceição',
                'type': 'church',
                'latitude': -22.5200,
                'longitude': -41.9500,
                'significance': 'high',
                'age_years': 200,
                'energy_type': 'spiritual'
            },
            {
                'name': 'Pedra de Itacoatiara',
                'type': 'natural_monument',
                'latitude': -22.9300,
                'longitude': -43.0500,
                'significance': 'high',
                'age_years': 10000,
                'energy_type': 'telluric'
            },
            {
                'name': 'Praia de Geribá',
                'type': 'natural_site',
                'latitude': -22.7800,
                'longitude': -41.9800,
                'significance': 'medium',
                'age_years': 50000,
                'energy_type': 'natural'
            }
        ]
        
        nearby_sites = []
        
        for site in sacred_sites_database:
            distance = self._calculate_distance(
                self.latitude, self.longitude,
                site['latitude'], site['longitude']
            )
            
            if distance <= radius_km:
                bearing = self._calculate_bearing(
                    self.latitude, self.longitude,
                    site['latitude'], site['longitude']
                )
                
                nearby_sites.append({
                    **site,
                    'distance_km': round(distance, 2),
                    'bearing_degrees': round(bearing, 2),
                    'cardinal_direction': self._bearing_to_cardinal(bearing),
                    'energy_influence': self._calculate_energy_influence(distance, site['significance'])
                })
        
        # Ordenar por distância
        nearby_sites.sort(key=lambda x: x['distance_km'])
        
        return nearby_sites
    
    def identify_ley_lines(self, sacred_sites: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Identifica possíveis linhas ley baseado em alinhamentos de sítios sagrados
        
        Args:
            sacred_sites: Lista de sítios sagrados (se None, busca automaticamente)
            
        Returns:
            Informações sobre linhas ley identificadas
        """
        if sacred_sites is None:
            sacred_sites = self.find_sacred_sites_nearby(100.0)
        
        ley_lines = []
        
        # Verificar alinhamentos entre três ou mais pontos
        if len(sacred_sites) >= 3:
            for i in range(len(sacred_sites)):
                for j in range(i + 1, len(sacred_sites)):
                    for k in range(j + 1, len(sacred_sites)):
                        site1 = sacred_sites[i]
                        site2 = sacred_sites[j]
                        site3 = sacred_sites[k]
                        
                        if self._check_alignment(
                            (site1['latitude'], site1['longitude']),
                            (site2['latitude'], site2['longitude']),
                            (site3['latitude'], site3['longitude'])
                        ):
                            # Calcular azimute da linha
                            azimuth = self._calculate_bearing(
                                site1['latitude'], site1['longitude'],
                                site3['latitude'], site3['longitude']
                            )
                            
                            ley_lines.append({
                                'id': f'leyline_{len(ley_lines) + 1}',
                                'aligned_sites': [site1['name'], site2['name'], site3['name']],
                                'azimuth_degrees': round(azimuth, 2),
                                'length_km': self._calculate_distance(
                                    site1['latitude'], site1['longitude'],
                                    site3['latitude'], site3['longitude']
                                ),
                                'energy_type': self._determine_line_energy([site1, site2, site3]),
                                'significance': 'high' if len([site1, site2, site3]) >= 3 else 'medium',
                                'passes_through_location': self._line_passes_through(
                                    (site1['latitude'], site1['longitude']),
                                    (site3['latitude'], site3['longitude']),
                                    (self.latitude, self.longitude)
                                )
                            })
        
        # Adicionar linhas ley conhecidas (simuladas)
        ley_lines.extend(self._get_known_ley_lines())
        
        return {
            'ley_lines_identified': len(ley_lines),
            'ley_lines': ley_lines,
            'lines_passing_through': [l for l in ley_lines if l.get('passes_through_location', False)],
            'strongest_influence': max(ley_lines, key=lambda x: 1 if x.get('significance') == 'high' else 0) if ley_lines else None
        }
    
    def detect_energy_vortices(self, sacred_sites: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Detecta possíveis vórtices de energia (pontos de convergência)
        
        Args:
            sacred_sites: Lista de sítios sagrados
            
        Returns:
            Informações sobre vórtices energéticos
        """
        if sacred_sites is None:
            sacred_sites = self.find_sacred_sites_nearby(50.0)
        
        vortices = []
        
        # Vórtice no local atual se houver múltiplos sítios próximos
        nearby_count = len([s for s in sacred_sites if s['distance_km'] < 10.0])
        
        if nearby_count >= 3:
            vortices.append({
                'location': 'current_site',
                'latitude': self.latitude,
                'longitude': self.longitude,
                'type': 'convergence_vortex',
                'strength': 'high' if nearby_count >= 5 else 'medium',
                'contributing_sites': nearby_count,
                'energy_type': 'mixed',
                'recommendation': 'Local ideal para práticas espirituais e meditação'
            })
        
        # Detectar vórtices em intersecções de linhas ley
        ley_lines_data = self.identify_ley_lines(sacred_sites)
        
        if len(ley_lines_data['ley_lines']) >= 2:
            # Verificar intersecções
            lines = ley_lines_data['ley_lines']
            for i in range(len(lines)):
                for j in range(i + 1, len(lines)):
                    # Simplificação: se ambas passam pelo local, há intersecção
                    if lines[i].get('passes_through_location') and lines[j].get('passes_through_location'):
                        vortices.append({
                            'location': 'ley_line_intersection',
                            'latitude': self.latitude,
                            'longitude': self.longitude,
                            'type': 'ley_line_vortex',
                            'strength': 'very_high',
                            'intersecting_lines': [lines[i]['id'], lines[j]['id']],
                            'energy_type': 'amplified',
                            'recommendation': 'Ponto de poder significativo - ideal para centro energético da edificação'
                        })
        
        return {
            'vortices_detected': len(vortices),
            'vortices': vortices,
            'location_is_vortex': len(vortices) > 0,
            'vortex_strength': max([v['strength'] for v in vortices]) if vortices else 'none'
        }
    
    def analyze_astronomical_alignments(self) -> Dict[str, Any]:
        """
        Analisa alinhamentos astronômicos (solstícios, equinócios, constelações)
        
        Returns:
            Análise de alinhamentos astronômicos
        """
        # Calcular azimutes solares importantes
        summer_solstice_sunrise = self._calculate_solstice_azimuth('summer', 'sunrise')
        summer_solstice_sunset = self._calculate_solstice_azimuth('summer', 'sunset')
        winter_solstice_sunrise = self._calculate_solstice_azimuth('winter', 'sunrise')
        winter_solstice_sunset = self._calculate_solstice_azimuth('winter', 'sunset')
        
        equinox_sunrise = 90.0  # Leste exato
        equinox_sunset = 270.0  # Oeste exato
        
        alignments = {
            'cardinal_points': {
                'north': 0.0,
                'east': 90.0,
                'south': 180.0,
                'west': 270.0
            },
            'solar_events': {
                'summer_solstice_sunrise': {
                    'azimuth': summer_solstice_sunrise,
                    'date': 'December 21',
                    'significance': 'Longest day of the year (Southern Hemisphere)'
                },
                'summer_solstice_sunset': {
                    'azimuth': summer_solstice_sunset,
                    'date': 'December 21',
                    'significance': 'Longest day of the year (Southern Hemisphere)'
                },
                'winter_solstice_sunrise': {
                    'azimuth': winter_solstice_sunrise,
                    'date': 'June 21',
                    'significance': 'Shortest day of the year (Southern Hemisphere)'
                },
                'winter_solstice_sunset': {
                    'azimuth': winter_solstice_sunset,
                    'date': 'June 21',
                    'significance': 'Shortest day of the year (Southern Hemisphere)'
                },
                'equinox_sunrise': {
                    'azimuth': equinox_sunrise,
                    'date': 'March 20 / September 22',
                    'significance': 'Equal day and night'
                },
                'equinox_sunset': {
                    'azimuth': equinox_sunset,
                    'date': 'March 20 / September 22',
                    'significance': 'Equal day and night'
                }
            },
            'stellar_alignments': {
                'southern_cross': {
                    'azimuth': 180.0,
                    'significance': 'Southern celestial pole marker'
                },
                'orion_belt': {
                    'azimuth': 120.0,
                    'significance': 'Ancient navigation and sacred geometry'
                }
            }
        }
        
        return {
            'alignments': alignments,
            'optimal_building_orientation': self._calculate_optimal_orientation(alignments),
            'sacred_directions': self._identify_sacred_directions(alignments),
            'recommendations': self._generate_astronomical_recommendations(alignments)
        }
    
    def perform_complete_analysis(self, radius_km: float = 50.0) -> Dict[str, Any]:
        """
        Realiza análise completa de linhas ley e geografia sagrada
        
        Args:
            radius_km: Raio de busca para sítios sagrados
            
        Returns:
            Análise completa
        """
        sacred_sites = self.find_sacred_sites_nearby(radius_km)
        ley_lines = self.identify_ley_lines(sacred_sites)
        vortices = self.detect_energy_vortices(sacred_sites)
        astronomical = self.analyze_astronomical_alignments()
        
        return {
            'location': {
                'latitude': self.latitude,
                'longitude': self.longitude
            },
            'analysis_date': self.analysis_date.isoformat(),
            'sacred_sites': {
                'total_found': len(sacred_sites),
                'sites': sacred_sites,
                'closest_site': sacred_sites[0] if sacred_sites else None
            },
            'ley_lines': ley_lines,
            'energy_vortices': vortices,
            'astronomical_alignments': astronomical,
            'overall_assessment': self._generate_overall_assessment(
                sacred_sites, ley_lines, vortices, astronomical
            )
        }
    
    # Métodos auxiliares privados
    
    def _calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calcula distância entre dois pontos usando fórmula de Haversine"""
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lon = math.radians(lon2 - lon1)
        
        a = (math.sin(delta_lat / 2) ** 2 +
             math.cos(lat1_rad) * math.cos(lat2_rad) *
             math.sin(delta_lon / 2) ** 2)
        
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        return self.EARTH_RADIUS_KM * c
    
    def _calculate_bearing(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calcula azimute (bearing) entre dois pontos"""
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lon = math.radians(lon2 - lon1)
        
        y = math.sin(delta_lon) * math.cos(lat2_rad)
        x = (math.cos(lat1_rad) * math.sin(lat2_rad) -
             math.sin(lat1_rad) * math.cos(lat2_rad) * math.cos(delta_lon))
        
        bearing = math.atan2(y, x)
        bearing_degrees = (math.degrees(bearing) + 360) % 360
        
        return bearing_degrees
    
    def _bearing_to_cardinal(self, bearing: float) -> str:
        """Converte azimute em direção cardeal"""
        directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
        index = round(bearing / 45) % 8
        return directions[index]
    
    def _calculate_energy_influence(self, distance_km: float, significance: str) -> str:
        """Calcula influência energética baseada em distância e significância"""
        sig_multiplier = {'high': 3, 'medium': 2, 'low': 1}.get(significance, 1)
        
        if distance_km < 5 * sig_multiplier:
            return 'strong'
        elif distance_km < 20 * sig_multiplier:
            return 'moderate'
        else:
            return 'weak'
    
    def _check_alignment(self, point1: Tuple[float, float], 
                        point2: Tuple[float, float],
                        point3: Tuple[float, float]) -> bool:
        """Verifica se três pontos estão alinhados dentro da tolerância"""
        bearing_12 = self._calculate_bearing(point1[0], point1[1], point2[0], point2[1])
        bearing_23 = self._calculate_bearing(point2[0], point2[1], point3[0], point3[1])
        
        # Normalizar diferença de ângulos
        diff = abs(bearing_12 - bearing_23)
        if diff > 180:
            diff = 360 - diff
        
        return diff < self.ALIGNMENT_TOLERANCE
    
    def _determine_line_energy(self, sites: List[Dict]) -> str:
        """Determina tipo de energia de uma linha ley baseado nos sítios"""
        energy_types = [s.get('energy_type', 'unknown') for s in sites]
        
        if 'spiritual' in energy_types:
            return 'spiritual'
        elif 'telluric' in energy_types:
            return 'telluric'
        else:
            return 'natural'
    
    def _line_passes_through(self, point1: Tuple[float, float],
                            point2: Tuple[float, float],
                            test_point: Tuple[float, float],
                            tolerance_km: float = 5.0) -> bool:
        """Verifica se uma linha passa próxima a um ponto"""
        # Calcular distância perpendicular do ponto à linha
        # Simplificação: verificar se o ponto está próximo da linha reta
        
        dist_1_test = self._calculate_distance(point1[0], point1[1], test_point[0], test_point[1])
        dist_2_test = self._calculate_distance(point2[0], point2[1], test_point[0], test_point[1])
        dist_1_2 = self._calculate_distance(point1[0], point1[1], point2[0], point2[1])
        
        # Se a soma das distâncias é aproximadamente igual à distância total, está na linha
        return abs((dist_1_test + dist_2_test) - dist_1_2) < tolerance_km
    
    def _get_known_ley_lines(self) -> List[Dict[str, Any]]:
        """Retorna linhas ley conhecidas (simuladas)"""
        return [
            {
                'id': 'leyline_atlantic',
                'name': 'Atlantic Coastal Line',
                'azimuth_degrees': 45.0,
                'length_km': 500.0,
                'energy_type': 'natural',
                'significance': 'medium',
                'passes_through_location': False
            }
        ]
    
    def _calculate_solstice_azimuth(self, season: str, event: str) -> float:
        """Calcula azimute do sol em solstícios"""
        # Fórmula simplificada baseada na latitude
        # Para Rio das Ostras (lat ~-22.5)
        
        if season == 'summer':  # Verão no hemisfério sul (dezembro)
            if event == 'sunrise':
                return 115.0  # Sudeste
            else:  # sunset
                return 245.0  # Sudoeste
        else:  # Inverno (junho)
            if event == 'sunrise':
                return 65.0  # Nordeste
            else:  # sunset
                return 295.0  # Noroeste
    
    def _calculate_optimal_orientation(self, alignments: Dict) -> Dict[str, Any]:
        """Calcula orientação ótima baseada em alinhamentos astronômicos"""
        return {
            'primary_axis': 'north-south',
            'secondary_axis': 'east-west',
            'recommended_entrance': 'east',
            'sacred_alignment': 'equinox_sunrise',
            'reasoning': 'Alinhamento com nascente equinocial maximiza energia natural'
        }
    
    def _identify_sacred_directions(self, alignments: Dict) -> List[str]:
        """Identifica direções sagradas"""
        return [
            'East (Sunrise/Renewal)',
            'North (Stability/Ancestors)',
            'South (Growth/Expansion)',
            'West (Sunset/Completion)'
        ]
    
    def _generate_astronomical_recommendations(self, alignments: Dict) -> List[str]:
        """Gera recomendações baseadas em alinhamentos astronômicos"""
        return [
            "Orientar eixo principal da edificação Norte-Sul",
            "Posicionar entrada principal voltada para Leste (nascente)",
            "Criar janelas ou aberturas alinhadas com solstícios",
            "Considerar skylight ou abertura zenital para luz natural",
            "Planejar espaços de meditação com vista para pontos cardeais"
        ]
    
    def _generate_overall_assessment(self, sacred_sites: List, ley_lines: Dict,
                                     vortices: Dict, astronomical: Dict) -> Dict[str, Any]:
        """Gera avaliação geral da análise"""
        # Calcular score energético (0-100)
        score = 50  # Base
        
        # Adicionar pontos por sítios próximos
        score += min(len(sacred_sites) * 5, 20)
        
        # Adicionar pontos por linhas ley
        score += min(ley_lines['ley_lines_identified'] * 10, 20)
        
        # Adicionar pontos por vórtices
        if vortices['location_is_vortex']:
            score += 20
        
        score = min(100, score)
        
        return {
            'energetic_potential_score': score,
            'sacred_geography_rating': 'high' if score > 70 else 'medium' if score > 40 else 'low',
            'main_features': self._identify_main_features(sacred_sites, ley_lines, vortices),
            'recommendations': self._generate_comprehensive_recommendations(
                sacred_sites, ley_lines, vortices, astronomical
            ),
            'ideal_for_sacred_architecture': score > 60
        }
    
    def _identify_main_features(self, sacred_sites: List, ley_lines: Dict, vortices: Dict) -> List[str]:
        """Identifica características principais"""
        features = []
        
        if len(sacred_sites) > 3:
            features.append(f"{len(sacred_sites)} sítios sagrados próximos")
        
        if ley_lines['ley_lines_identified'] > 0:
            features.append(f"{ley_lines['ley_lines_identified']} linhas ley identificadas")
        
        if vortices['location_is_vortex']:
            features.append("Localização em vórtice energético")
        
        return features if features else ["Características energéticas padrão"]
    
    def _generate_comprehensive_recommendations(self, sacred_sites: List, ley_lines: Dict,
                                                vortices: Dict, astronomical: Dict) -> List[str]:
        """Gera recomendações abrangentes"""
        recommendations = []
        
        if vortices['location_is_vortex']:
            recommendations.append("Aproveitar vórtice energético posicionando centro da edificação no ponto de convergência")
        
        if len(sacred_sites) > 0:
            closest = sacred_sites[0]
            recommendations.append(f"Considerar alinhamento visual com {closest['name']} ({closest['cardinal_direction']})")
        
        if ley_lines['ley_lines_identified'] > 0:
            recommendations.append("Alinhar eixos principais da edificação com linhas ley identificadas")
        
        recommendations.extend(astronomical['recommendations'])
        
        return recommendations


# Função auxiliar para uso direto
def analyze_ley_lines(latitude: float, longitude: float, radius_km: float = 50.0) -> Dict[str, Any]:
    """
    Função auxiliar para realizar análise completa de linhas ley
    
    Args:
        latitude: Latitude do local
        longitude: Longitude do local
        radius_km: Raio de busca para sítios sagrados
        
    Returns:
        Análise completa de linhas ley
    """
    analyzer = LeyLineAnalyzer(latitude, longitude)
    return analyzer.perform_complete_analysis(radius_km)


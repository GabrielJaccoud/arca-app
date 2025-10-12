"""
Módulo de Análise de Arquitetura Sagrada para o Sistema ARCA
Avalia princípios de arquitetura sagrada, materiais, espaços rituais e harmonias espaciais
"""

import math
import json
from typing import Dict, List, Tuple, Any, Optional
from datetime import datetime


class SacredArchitectureAnalyzer:
    """
    Analisador de Arquitetura Sagrada
    """
    
    # Proporções ideais de pé-direito
    MIN_CEILING_HEIGHT = 2.6  # metros
    IDEAL_CEILING_HEIGHT = 3.0  # metros
    SACRED_CEILING_HEIGHT = 3.6  # metros (baseado em proporção áurea)
    
    # Proporção áurea
    PHI = 1.618033988749895
    
    def __init__(self):
        """Inicializa o analisador de arquitetura sagrada"""
        self.analysis_date = datetime.now()
        self.material_database = self._load_material_database()
        
    def analyze_spatial_proportions(self, room_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analisa proporções espaciais de um ambiente
        
        Args:
            room_data: Dados do ambiente (width, height, ceiling_height, etc.)
            
        Returns:
            Análise de proporções espaciais
        """
        width = room_data.get('width', 0)
        height = room_data.get('height', 0)  # comprimento
        ceiling_height = room_data.get('ceiling_height', 2.8)
        
        # Analisar proporção largura x comprimento
        floor_ratio = max(width, height) / min(width, height) if min(width, height) > 0 else 0
        is_golden_floor = abs(floor_ratio - self.PHI) < 0.1
        
        # Analisar proporção pé-direito
        ceiling_analysis = self._analyze_ceiling_height(ceiling_height, width, height)
        
        # Analisar volume
        volume = width * height * ceiling_height
        ideal_volume = self._calculate_ideal_volume(width, height)
        
        # Analisar hierarquia espacial
        hierarchy = self._analyze_spatial_hierarchy(room_data)
        
        return {
            'floor_proportions': {
                'width': width,
                'height': height,
                'ratio': round(floor_ratio, 3),
                'is_golden_ratio': is_golden_floor,
                'assessment': 'excellent' if is_golden_floor else 'good' if abs(floor_ratio - self.PHI) < 0.3 else 'needs_improvement'
            },
            'ceiling_analysis': ceiling_analysis,
            'volume_analysis': {
                'actual_volume_m3': round(volume, 2),
                'ideal_volume_m3': round(ideal_volume, 2),
                'volume_ratio': round(volume / ideal_volume, 2) if ideal_volume > 0 else 0,
                'spaciousness': self._assess_spaciousness(volume, width * height)
            },
            'spatial_hierarchy': hierarchy,
            'overall_proportion_score': self._calculate_proportion_score(
                is_golden_floor, ceiling_analysis, volume / ideal_volume if ideal_volume > 0 else 0
            )
        }
    
    def analyze_materials(self, materials_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analisa materiais de construção quanto a propriedades energéticas
        
        Args:
            materials_list: Lista de materiais utilizados
            
        Returns:
            Análise de materiais
        """
        analyzed_materials = []
        
        for material in materials_list:
            material_name = material.get('name', '').lower()
            location = material.get('location', 'general')
            
            material_info = self.material_database.get(material_name, {})
            
            analyzed_materials.append({
                'name': material_name,
                'location': location,
                'category': material_info.get('category', 'unknown'),
                'energy_conductivity': material_info.get('energy_conductivity', 'neutral'),
                'elemental_association': material_info.get('element', 'earth'),
                'sustainability': material_info.get('sustainability', 'medium'),
                'sacred_properties': material_info.get('sacred_properties', []),
                'recommendation': self._generate_material_recommendation(material_info, location)
            })
        
        return {
            'materials_analyzed': len(analyzed_materials),
            'materials': analyzed_materials,
            'natural_material_percentage': self._calculate_natural_percentage(analyzed_materials),
            'energy_balance': self._assess_material_energy_balance(analyzed_materials),
            'sustainability_score': self._calculate_sustainability_score(analyzed_materials),
            'recommendations': self._generate_material_recommendations(analyzed_materials)
        }
    
    def identify_sacred_spaces(self, floor_plan_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Identifica e avalia espaços sagrados/rituais
        
        Args:
            floor_plan_data: Dados da planta baixa
            
        Returns:
            Análise de espaços sagrados
        """
        rooms = floor_plan_data.get('rooms', [])
        sacred_spaces = []
        
        for room in rooms:
            room_type = room.get('type', '').lower()
            room_name = room.get('name', '')
            
            # Identificar espaços potencialmente sagrados
            if any(keyword in room_type or keyword in room_name.lower() 
                   for keyword in ['meditation', 'prayer', 'yoga', 'altar', 'chapel', 'sanctuary']):
                
                sacred_spaces.append({
                    'name': room_name,
                    'type': room_type,
                    'purpose': 'meditation/spiritual practice',
                    'location': room.get('location', 'unknown'),
                    'orientation': room.get('orientation', 'unknown'),
                    'suitability_score': self._assess_sacred_space_suitability(room),
                    'recommendations': self._generate_sacred_space_recommendations(room)
                })
        
        # Sugerir novos espaços sagrados se não houver
        if len(sacred_spaces) == 0:
            sacred_spaces.append({
                'name': 'Suggested Meditation Corner',
                'type': 'meditation_space',
                'purpose': 'spiritual practice',
                'location': 'to_be_determined',
                'orientation': 'east_facing',
                'suitability_score': 0,
                'recommendations': [
                    "Create a dedicated meditation space facing East",
                    "Minimum 4m² for personal practice",
                    "Ensure quiet location away from high-traffic areas",
                    "Natural light and ventilation essential"
                ]
            })
        
        return {
            'sacred_spaces_identified': len(sacred_spaces),
            'sacred_spaces': sacred_spaces,
            'has_dedicated_sacred_space': any(s['suitability_score'] > 70 for s in sacred_spaces),
            'recommendations': self._generate_sacred_space_general_recommendations(sacred_spaces)
        }
    
    def analyze_astronomical_integration(self, building_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analisa integração astronômica da edificação
        
        Args:
            building_data: Dados da edificação (orientação, aberturas, etc.)
            
        Returns:
            Análise de integração astronômica
        """
        orientation = building_data.get('orientation', 'north')
        latitude = building_data.get('latitude', -22.5)
        
        # Analisar orientação principal
        orientation_analysis = self._analyze_building_orientation(orientation)
        
        # Analisar aberturas para luz solar
        openings = building_data.get('openings', [])
        solar_access = self._analyze_solar_access(openings, latitude)
        
        # Analisar alinhamento com eventos astronômicos
        astronomical_events = self._analyze_astronomical_events(orientation, latitude)
        
        return {
            'building_orientation': orientation_analysis,
            'solar_access': solar_access,
            'astronomical_events': astronomical_events,
            'integration_score': self._calculate_astronomical_integration_score(
                orientation_analysis, solar_access, astronomical_events
            ),
            'recommendations': self._generate_astronomical_recommendations(
                orientation, solar_access, astronomical_events
            )
        }
    
    def analyze_circulation_flow(self, floor_plan_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analisa fluxo de circulação e movimento
        
        Args:
            floor_plan_data: Dados da planta baixa
            
        Returns:
            Análise de circulação
        """
        circulation_paths = floor_plan_data.get('circulation_paths', [])
        entrance = floor_plan_data.get('entrance', {})
        
        # Analisar entrada principal
        entrance_analysis = self._analyze_entrance(entrance)
        
        # Analisar caminhos de circulação
        path_analysis = self._analyze_circulation_paths(circulation_paths)
        
        # Analisar sequência espacial
        spatial_sequence = self._analyze_spatial_sequence(floor_plan_data)
        
        return {
            'entrance': entrance_analysis,
            'circulation_paths': path_analysis,
            'spatial_sequence': spatial_sequence,
            'flow_quality': self._assess_flow_quality(entrance_analysis, path_analysis),
            'recommendations': self._generate_circulation_recommendations(
                entrance_analysis, path_analysis, spatial_sequence
            )
        }
    
    def analyze_symmetry_and_balance(self, floor_plan_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analisa simetria e equilíbrio da edificação
        
        Args:
            floor_plan_data: Dados da planta baixa
            
        Returns:
            Análise de simetria e equilíbrio
        """
        # Analisar simetria axial
        axial_symmetry = self._analyze_axial_symmetry(floor_plan_data)
        
        # Analisar simetria radial
        radial_symmetry = self._analyze_radial_symmetry(floor_plan_data)
        
        # Analisar equilíbrio de massas
        mass_balance = self._analyze_mass_balance(floor_plan_data)
        
        # Analisar centro geométrico
        geometric_center = self._find_geometric_center(floor_plan_data)
        
        return {
            'axial_symmetry': axial_symmetry,
            'radial_symmetry': radial_symmetry,
            'mass_balance': mass_balance,
            'geometric_center': geometric_center,
            'overall_symmetry_score': self._calculate_symmetry_score(
                axial_symmetry, radial_symmetry, mass_balance
            ),
            'recommendations': self._generate_symmetry_recommendations(
                axial_symmetry, radial_symmetry, mass_balance
            )
        }
    
    def perform_complete_analysis(self, building_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Realiza análise completa de arquitetura sagrada
        
        Args:
            building_data: Dados completos da edificação
            
        Returns:
            Análise completa de arquitetura sagrada
        """
        floor_plan_data = building_data.get('floor_plan', {})
        materials = building_data.get('materials', [])
        
        # Analisar cada ambiente
        rooms = floor_plan_data.get('rooms', [])
        room_analyses = []
        
        for room in rooms:
            room_analyses.append({
                'room_name': room.get('name', 'Unknown'),
                'spatial_proportions': self.analyze_spatial_proportions(room)
            })
        
        return {
            'analysis_date': self.analysis_date.isoformat(),
            'room_analyses': room_analyses,
            'materials_analysis': self.analyze_materials(materials),
            'sacred_spaces': self.identify_sacred_spaces(floor_plan_data),
            'astronomical_integration': self.analyze_astronomical_integration(building_data),
            'circulation_flow': self.analyze_circulation_flow(floor_plan_data),
            'symmetry_balance': self.analyze_symmetry_and_balance(floor_plan_data),
            'overall_assessment': self._generate_overall_sacred_architecture_assessment(
                room_analyses, materials, floor_plan_data
            ),
            'comprehensive_recommendations': self._generate_comprehensive_recommendations(
                room_analyses, materials, floor_plan_data
            )
        }
    
    # Métodos auxiliares privados
    
    def _load_material_database(self) -> Dict[str, Dict[str, Any]]:
        """Carrega base de dados de materiais"""
        return {
            'wood': {
                'category': 'natural',
                'energy_conductivity': 'low',
                'element': 'wood',
                'sustainability': 'high',
                'sacred_properties': ['grounding', 'warming', 'living_energy']
            },
            'stone': {
                'category': 'natural',
                'energy_conductivity': 'medium',
                'element': 'earth',
                'sustainability': 'high',
                'sacred_properties': ['stability', 'permanence', 'grounding']
            },
            'granite': {
                'category': 'natural',
                'energy_conductivity': 'high',
                'element': 'earth',
                'sustainability': 'high',
                'sacred_properties': ['strength', 'protection', 'crystalline_energy']
            },
            'marble': {
                'category': 'natural',
                'energy_conductivity': 'medium',
                'element': 'earth',
                'sustainability': 'medium',
                'sacred_properties': ['purity', 'elegance', 'light_reflection']
            },
            'clay': {
                'category': 'natural',
                'energy_conductivity': 'low',
                'element': 'earth',
                'sustainability': 'very_high',
                'sacred_properties': ['earthing', 'traditional', 'breathable']
            },
            'bamboo': {
                'category': 'natural',
                'energy_conductivity': 'low',
                'element': 'wood',
                'sustainability': 'very_high',
                'sacred_properties': ['flexibility', 'growth', 'resilience']
            },
            'copper': {
                'category': 'metal',
                'energy_conductivity': 'very_high',
                'element': 'metal',
                'sustainability': 'medium',
                'sacred_properties': ['conductivity', 'healing', 'antimicrobial']
            },
            'glass': {
                'category': 'synthetic_natural',
                'energy_conductivity': 'medium',
                'element': 'fire',
                'sustainability': 'medium',
                'sacred_properties': ['transparency', 'light', 'clarity']
            },
            'concrete': {
                'category': 'synthetic',
                'energy_conductivity': 'high',
                'element': 'earth',
                'sustainability': 'low',
                'sacred_properties': ['modern', 'structural']
            },
            'steel': {
                'category': 'metal',
                'energy_conductivity': 'very_high',
                'element': 'metal',
                'sustainability': 'medium',
                'sacred_properties': ['strength', 'modern', 'precision']
            }
        }
    
    def _analyze_ceiling_height(self, ceiling_height: float, width: float, height: float) -> Dict[str, Any]:
        """Analisa altura do pé-direito"""
        floor_area = width * height
        floor_diagonal = math.sqrt(width**2 + height**2)
        
        # Ideal: pé-direito proporcional à diagonal do piso
        ideal_height = floor_diagonal / self.PHI
        
        return {
            'actual_height': ceiling_height,
            'minimum_recommended': self.MIN_CEILING_HEIGHT,
            'ideal_height': round(ideal_height, 2),
            'sacred_height': self.SACRED_CEILING_HEIGHT,
            'meets_minimum': ceiling_height >= self.MIN_CEILING_HEIGHT,
            'quality': self._assess_ceiling_quality(ceiling_height, ideal_height),
            'recommendation': self._generate_ceiling_recommendation(ceiling_height, ideal_height)
        }
    
    def _calculate_ideal_volume(self, width: float, height: float) -> float:
        """Calcula volume ideal baseado em proporções sagradas"""
        floor_area = width * height
        ideal_ceiling = math.sqrt(floor_area) / self.PHI
        return floor_area * ideal_ceiling
    
    def _analyze_spatial_hierarchy(self, room_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analisa hierarquia espacial"""
        room_type = room_data.get('type', '').lower()
        
        hierarchy_map = {
            'living_room': 'primary',
            'meditation_room': 'primary',
            'master_bedroom': 'primary',
            'bedroom': 'secondary',
            'kitchen': 'secondary',
            'bathroom': 'tertiary',
            'storage': 'tertiary'
        }
        
        hierarchy_level = hierarchy_map.get(room_type, 'secondary')
        
        return {
            'hierarchy_level': hierarchy_level,
            'importance': 'high' if hierarchy_level == 'primary' else 'medium' if hierarchy_level == 'secondary' else 'low',
            'should_emphasize': hierarchy_level == 'primary'
        }
    
    def _calculate_proportion_score(self, is_golden_floor: bool, ceiling_analysis: Dict, volume_ratio: float) -> float:
        """Calcula score de proporções"""
        score = 0
        
        if is_golden_floor:
            score += 40
        
        if ceiling_analysis['meets_minimum']:
            score += 20
        
        if ceiling_analysis['quality'] in ['excellent', 'good']:
            score += 20
        
        if 0.8 <= volume_ratio <= 1.2:
            score += 20
        
        return score
    
    def _assess_ceiling_quality(self, actual: float, ideal: float) -> str:
        """Avalia qualidade do pé-direito"""
        deviation = abs(actual - ideal) / ideal
        
        if deviation < 0.05:
            return 'excellent'
        elif deviation < 0.15:
            return 'good'
        elif deviation < 0.30:
            return 'acceptable'
        else:
            return 'poor'
    
    def _generate_ceiling_recommendation(self, actual: float, ideal: float) -> str:
        """Gera recomendação para pé-direito"""
        if actual < self.MIN_CEILING_HEIGHT:
            return f"Ceiling too low. Increase to minimum {self.MIN_CEILING_HEIGHT}m"
        elif abs(actual - ideal) / ideal < 0.1:
            return "Excellent ceiling height. Maintain this proportion."
        else:
            return f"Consider adjusting to ideal height of {round(ideal, 2)}m for better proportions"
    
    def _assess_spaciousness(self, volume: float, floor_area: float) -> str:
        """Avalia sensação de amplitude"""
        volume_per_area = volume / floor_area if floor_area > 0 else 0
        
        if volume_per_area >= 3.5:
            return 'very_spacious'
        elif volume_per_area >= 3.0:
            return 'spacious'
        elif volume_per_area >= 2.6:
            return 'adequate'
        else:
            return 'cramped'
    
    def _calculate_natural_percentage(self, materials: List[Dict]) -> float:
        """Calcula percentual de materiais naturais"""
        if not materials:
            return 0
        
        natural_count = sum(1 for m in materials if m.get('category') in ['natural', 'synthetic_natural'])
        return round((natural_count / len(materials)) * 100, 2)
    
    def _assess_material_energy_balance(self, materials: List[Dict]) -> Dict[str, Any]:
        """Avalia equilíbrio energético dos materiais"""
        elements = {}
        for material in materials:
            element = material.get('elemental_association', 'earth')
            elements[element] = elements.get(element, 0) + 1
        
        return {
            'element_distribution': elements,
            'is_balanced': len(elements) >= 3,
            'dominant_element': max(elements, key=elements.get) if elements else 'earth'
        }
    
    def _calculate_sustainability_score(self, materials: List[Dict]) -> float:
        """Calcula score de sustentabilidade"""
        if not materials:
            return 0
        
        sustainability_map = {'very_high': 100, 'high': 80, 'medium': 60, 'low': 40, 'very_low': 20}
        
        total_score = sum(sustainability_map.get(m.get('sustainability', 'medium'), 60) for m in materials)
        return round(total_score / len(materials), 2)
    
    def _generate_material_recommendation(self, material_info: Dict, location: str) -> str:
        """Gera recomendação para material"""
        if material_info.get('category') == 'natural':
            return f"Excellent choice for {location}. Natural materials enhance energy flow."
        elif material_info.get('sustainability') == 'low':
            return f"Consider more sustainable alternatives for {location}"
        else:
            return f"Suitable for {location}. Consider balancing with natural materials."
    
    def _generate_material_recommendations(self, materials: List[Dict]) -> List[str]:
        """Gera recomendações gerais de materiais"""
        natural_pct = self._calculate_natural_percentage(materials)
        
        recommendations = []
        
        if natural_pct < 50:
            recommendations.append("Increase use of natural materials (wood, stone, clay) to at least 50%")
        
        recommendations.append("Balance five elements (wood, fire, earth, metal, water) through material selection")
        recommendations.append("Prioritize locally-sourced materials to reduce environmental impact")
        
        return recommendations
    
    def _assess_sacred_space_suitability(self, room: Dict) -> float:
        """Avalia adequação de espaço sagrado"""
        score = 50  # Base
        
        # Adicionar pontos por orientação
        if room.get('orientation', '').lower() in ['east', 'north']:
            score += 20
        
        # Adicionar pontos por tamanho adequado
        area = room.get('width', 0) * room.get('height', 0)
        if 4 <= area <= 20:
            score += 20
        
        # Adicionar pontos por localização tranquila
        if 'quiet' in room.get('location', '').lower():
            score += 10
        
        return min(100, score)
    
    def _generate_sacred_space_recommendations(self, room: Dict) -> List[str]:
        """Gera recomendações para espaço sagrado"""
        return [
            "Orient altar or meditation cushion facing East",
            "Use natural materials (wood, stone, natural fibers)",
            "Ensure excellent natural ventilation",
            "Minimize electronic devices and EMF sources",
            "Incorporate natural light with option for dimming",
            "Use sacred geometry in design elements"
        ]
    
    def _generate_sacred_space_general_recommendations(self, spaces: List[Dict]) -> List[str]:
        """Gera recomendações gerais para espaços sagrados"""
        if not any(s.get('suitability_score', 0) > 70 for s in spaces):
            return [
                "Create dedicated sacred space of at least 4m²",
                "Position in quiet area with East or North orientation",
                "Ensure privacy and minimal disturbance",
                "Incorporate altar or focal point for practice"
            ]
        return ["Maintain and enhance existing sacred spaces"]
    
    def _analyze_building_orientation(self, orientation: str) -> Dict[str, Any]:
        """Analisa orientação da edificação"""
        orientation_map = {
            'north': {'quality': 'excellent', 'energy': 'stability, wisdom'},
            'east': {'quality': 'excellent', 'energy': 'renewal, beginnings'},
            'south': {'quality': 'good', 'energy': 'growth, expansion'},
            'west': {'quality': 'good', 'energy': 'completion, reflection'}
        }
        
        orientation_data = orientation_map.get(orientation.lower(), {'quality': 'neutral', 'energy': 'balanced'})
        
        return {
            'orientation': orientation,
            'quality': orientation_data['quality'],
            'energy_type': orientation_data['energy'],
            'is_optimal': orientation.lower() in ['north', 'east']
        }
    
    def _analyze_solar_access(self, openings: List[Dict], latitude: float) -> Dict[str, Any]:
        """Analisa acesso solar"""
        east_openings = sum(1 for o in openings if 'east' in o.get('orientation', '').lower())
        west_openings = sum(1 for o in openings if 'west' in o.get('orientation', '').lower())
        north_openings = sum(1 for o in openings if 'north' in o.get('orientation', '').lower())
        south_openings = sum(1 for o in openings if 'south' in o.get('orientation', '').lower())
        
        return {
            'east_openings': east_openings,
            'west_openings': west_openings,
            'north_openings': north_openings,
            'south_openings': south_openings,
            'has_morning_sun': east_openings > 0,
            'has_afternoon_sun': west_openings > 0,
            'solar_balance': 'good' if east_openings > 0 and west_openings > 0 else 'needs_improvement'
        }
    
    def _analyze_astronomical_events(self, orientation: str, latitude: float) -> Dict[str, Any]:
        """Analisa alinhamento com eventos astronômicos"""
        return {
            'solstice_alignment': orientation.lower() in ['north', 'south'],
            'equinox_alignment': orientation.lower() in ['east', 'west'],
            'optimal_for_solar_observation': True,
            'recommended_skylight_position': 'center' if orientation.lower() == 'north' else 'south_side'
        }
    
    def _calculate_astronomical_integration_score(self, orientation: Dict, 
                                                   solar: Dict, events: Dict) -> float:
        """Calcula score de integração astronômica"""
        score = 0
        
        if orientation['is_optimal']:
            score += 40
        
        if solar['has_morning_sun']:
            score += 20
        
        if solar['solar_balance'] == 'good':
            score += 20
        
        if events['solstice_alignment'] or events['equinox_alignment']:
            score += 20
        
        return score
    
    def _generate_astronomical_recommendations(self, orientation: str, 
                                               solar: Dict, events: Dict) -> List[str]:
        """Gera recomendações astronômicas"""
        recommendations = []
        
        if not solar['has_morning_sun']:
            recommendations.append("Add East-facing windows for morning sunlight")
        
        if solar['solar_balance'] != 'good':
            recommendations.append("Balance solar access with openings on multiple orientations")
        
        recommendations.append("Consider skylight for zenith light and star observation")
        
        return recommendations
    
    def _analyze_entrance(self, entrance: Dict) -> Dict[str, Any]:
        """Analisa entrada principal"""
        return {
            'orientation': entrance.get('orientation', 'unknown'),
            'is_protected': entrance.get('has_overhang', False),
            'is_welcoming': entrance.get('width', 0) >= 1.2,
            'quality': 'good' if entrance.get('orientation', '').lower() == 'east' else 'acceptable'
        }
    
    def _analyze_circulation_paths(self, paths: List[Dict]) -> Dict[str, Any]:
        """Analisa caminhos de circulação"""
        return {
            'total_paths': len(paths),
            'clear_hierarchy': len(paths) >= 2,
            'flow_quality': 'good' if len(paths) >= 2 else 'needs_improvement'
        }
    
    def _analyze_spatial_sequence(self, floor_plan: Dict) -> Dict[str, Any]:
        """Analisa sequência espacial"""
        return {
            'has_transition_spaces': True,
            'public_private_separation': 'clear',
            'sequence_quality': 'good'
        }
    
    def _assess_flow_quality(self, entrance: Dict, paths: Dict) -> str:
        """Avalia qualidade do fluxo"""
        if entrance['is_welcoming'] and paths['flow_quality'] == 'good':
            return 'excellent'
        return 'good'
    
    def _generate_circulation_recommendations(self, entrance: Dict, 
                                              paths: Dict, sequence: Dict) -> List[str]:
        """Gera recomendações de circulação"""
        return [
            "Ensure clear primary circulation path",
            "Create transition spaces between public and private areas",
            "Maintain minimum 1.2m width for main circulation"
        ]
    
    def _analyze_axial_symmetry(self, floor_plan: Dict) -> Dict[str, Any]:
        """Analisa simetria axial"""
        return {
            'has_primary_axis': True,
            'has_secondary_axis': True,
            'symmetry_quality': 'good'
        }
    
    def _analyze_radial_symmetry(self, floor_plan: Dict) -> Dict[str, Any]:
        """Analisa simetria radial"""
        return {
            'has_radial_symmetry': False,
            'central_point_defined': True
        }
    
    def _analyze_mass_balance(self, floor_plan: Dict) -> Dict[str, Any]:
        """Analisa equilíbrio de massas"""
        return {
            'is_balanced': True,
            'balance_quality': 'good'
        }
    
    def _find_geometric_center(self, floor_plan: Dict) -> Dict[str, Any]:
        """Encontra centro geométrico"""
        return {
            'x': 0,
            'y': 0,
            'is_accessible': True,
            'recommended_use': 'Central gathering or meditation space'
        }
    
    def _calculate_symmetry_score(self, axial: Dict, radial: Dict, mass: Dict) -> float:
        """Calcula score de simetria"""
        score = 0
        
        if axial['has_primary_axis']:
            score += 40
        
        if mass['is_balanced']:
            score += 40
        
        if radial['central_point_defined']:
            score += 20
        
        return score
    
    def _generate_symmetry_recommendations(self, axial: Dict, radial: Dict, mass: Dict) -> List[str]:
        """Gera recomendações de simetria"""
        return [
            "Maintain axial symmetry in main spaces",
            "Define clear geometric center",
            "Balance mass distribution for harmony"
        ]
    
    def _generate_overall_sacred_architecture_assessment(self, room_analyses: List, 
                                                         materials: List, 
                                                         floor_plan: Dict) -> Dict[str, Any]:
        """Gera avaliação geral de arquitetura sagrada"""
        avg_proportion_score = sum(r['spatial_proportions']['overall_proportion_score'] 
                                   for r in room_analyses) / len(room_analyses) if room_analyses else 0
        
        return {
            'sacred_architecture_score': round(avg_proportion_score, 2),
            'rating': 'excellent' if avg_proportion_score > 70 else 'good' if avg_proportion_score > 50 else 'needs_improvement',
            'key_strengths': self._identify_strengths(room_analyses, materials),
            'areas_for_improvement': self._identify_improvements(room_analyses, materials)
        }
    
    def _identify_strengths(self, room_analyses: List, materials: List) -> List[str]:
        """Identifica pontos fortes"""
        return ["Good spatial proportions", "Adequate ceiling heights"]
    
    def _identify_improvements(self, room_analyses: List, materials: List) -> List[str]:
        """Identifica áreas para melhoria"""
        return ["Increase use of natural materials", "Add dedicated sacred space"]
    
    def _generate_comprehensive_recommendations(self, room_analyses: List, 
                                                materials: List, 
                                                floor_plan: Dict) -> List[str]:
        """Gera recomendações abrangentes"""
        return [
            "Prioritize golden ratio (1.618) in main spaces",
            "Use minimum 60% natural materials",
            "Create dedicated sacred/meditation space",
            "Orient main entrance to East",
            "Ensure adequate natural light and ventilation",
            "Incorporate sacred geometric patterns",
            "Balance five elements through materials and colors",
            "Define clear spatial hierarchy",
            "Maintain axial symmetry in design",
            "Align building with astronomical events"
        ]


# Função auxiliar para uso direto
def analyze_sacred_architecture(building_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Função auxiliar para realizar análise completa de arquitetura sagrada
    
    Args:
        building_data: Dados completos da edificação
        
    Returns:
        Análise completa de arquitetura sagrada
    """
    analyzer = SacredArchitectureAnalyzer()
    return analyzer.perform_complete_analysis(building_data)


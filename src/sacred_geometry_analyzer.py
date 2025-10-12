"""
Módulo de Análise de Geometria Sagrada para o Sistema ARCA
Analisa proporções áureas, padrões geométricos sagrados e harmonias matemáticas
"""

import math
import json
from typing import Dict, List, Tuple, Any, Optional
from datetime import datetime


class SacredGeometryAnalyzer:
    """
    Analisador de Geometria Sagrada
    """
    
    # Constantes matemáticas sagradas
    PHI = (1 + math.sqrt(5)) / 2  # Proporção Áurea = 1.618033988749895
    SILVER_RATIO = 1 + math.sqrt(2)  # Proporção de Prata = 2.414213562373095
    BRONZE_RATIO = (3 + math.sqrt(13)) / 2  # Proporção de Bronze = 3.302775637731995
    
    SQRT_2 = math.sqrt(2)  # 1.414213562373095
    SQRT_3 = math.sqrt(3)  # 1.732050807568877
    SQRT_5 = math.sqrt(5)  # 2.236067977499790
    
    PI = math.pi  # 3.141592653589793
    
    # Tolerâncias para verificação de proporções
    TOLERANCE_STRICT = 0.02  # 2%
    TOLERANCE_MODERATE = 0.05  # 5%
    TOLERANCE_LOOSE = 0.10  # 10%
    
    def __init__(self):
        """Inicializa o analisador de geometria sagrada"""
        self.analysis_date = datetime.now()
        
    def check_golden_ratio(self, dimension1: float, dimension2: float,
                          tolerance: float = None) -> Dict[str, Any]:
        """
        Verifica se duas dimensões seguem a proporção áurea
        
        Args:
            dimension1: Primeira dimensão
            dimension2: Segunda dimensão
            tolerance: Tolerância para verificação (padrão: moderada)
            
        Returns:
            Resultado da verificação
        """
        if tolerance is None:
            tolerance = self.TOLERANCE_MODERATE
        
        ratio = max(dimension1, dimension2) / min(dimension1, dimension2)
        deviation = abs(ratio - self.PHI)
        deviation_percentage = (deviation / self.PHI) * 100
        
        is_golden = deviation_percentage <= (tolerance * 100)
        
        return {
            'is_golden_ratio': is_golden,
            'calculated_ratio': round(ratio, 6),
            'golden_ratio_phi': round(self.PHI, 6),
            'deviation': round(deviation, 6),
            'deviation_percentage': round(deviation_percentage, 2),
            'quality': self._assess_ratio_quality(deviation_percentage),
            'recommendation': self._generate_golden_ratio_recommendation(is_golden, deviation_percentage)
        }
    
    def analyze_dimensions(self, width: float, height: float, depth: float = None) -> Dict[str, Any]:
        """
        Analisa dimensões de um espaço quanto a proporções sagradas
        
        Args:
            width: Largura
            height: Altura
            depth: Profundidade (opcional)
            
        Returns:
            Análise completa das proporções
        """
        analyses = {}
        
        # Analisar width x height
        analyses['width_height'] = {
            'golden_ratio': self.check_golden_ratio(width, height),
            'silver_ratio': self._check_ratio(width, height, self.SILVER_RATIO, 'Silver'),
            'sqrt_2_ratio': self._check_ratio(width, height, self.SQRT_2, 'Sqrt(2)'),
            'sqrt_3_ratio': self._check_ratio(width, height, self.SQRT_3, 'Sqrt(3)')
        }
        
        if depth is not None:
            # Analisar width x depth
            analyses['width_depth'] = {
                'golden_ratio': self.check_golden_ratio(width, depth),
                'silver_ratio': self._check_ratio(width, depth, self.SILVER_RATIO, 'Silver'),
                'sqrt_2_ratio': self._check_ratio(width, depth, self.SQRT_2, 'Sqrt(2)')
            }
            
            # Analisar height x depth
            analyses['height_depth'] = {
                'golden_ratio': self.check_golden_ratio(height, depth),
                'silver_ratio': self._check_ratio(height, depth, self.SILVER_RATIO, 'Silver'),
                'sqrt_2_ratio': self._check_ratio(height, depth, self.SQRT_2, 'Sqrt(2)')
            }
        
        return {
            'dimensions': {
                'width': width,
                'height': height,
                'depth': depth
            },
            'ratio_analyses': analyses,
            'best_match': self._find_best_ratio_match(analyses),
            'harmony_score': self._calculate_harmony_score(analyses),
            'recommendations': self._generate_dimension_recommendations(analyses, width, height, depth)
        }
    
    def identify_sacred_patterns(self, floor_plan_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Identifica padrões de geometria sagrada em uma planta baixa
        
        Args:
            floor_plan_data: Dados da planta baixa
            
        Returns:
            Padrões sagrados identificados
        """
        patterns = []
        
        # Verificar presença de formas geométricas sagradas
        shapes = floor_plan_data.get('shapes', [])
        
        for shape in shapes:
            shape_type = shape.get('type', '')
            
            if shape_type == 'circle':
                patterns.append({
                    'pattern': 'Circle',
                    'significance': 'Unity, wholeness, infinity',
                    'energy': 'Protective and centering',
                    'recommendation': 'Ideal for meditation spaces or central gathering areas'
                })
            
            elif shape_type == 'square':
                patterns.append({
                    'pattern': 'Square',
                    'significance': 'Stability, earth element, foundation',
                    'energy': 'Grounding and stabilizing',
                    'recommendation': 'Excellent for main structural elements'
                })
            
            elif shape_type == 'hexagon':
                patterns.append({
                    'pattern': 'Hexagon',
                    'significance': 'Harmony, balance, natural order',
                    'energy': 'Harmonizing and balancing',
                    'recommendation': 'Sacred geometry of nature (honeycomb pattern)'
                })
            
            elif shape_type == 'pentagon':
                patterns.append({
                    'pattern': 'Pentagon/Pentagram',
                    'significance': 'Human proportion, golden ratio',
                    'energy': 'Protective and transformative',
                    'recommendation': 'Powerful for sacred spaces'
                })
        
        # Verificar Vesica Piscis (intersecção de dois círculos)
        if self._detect_vesica_piscis(floor_plan_data):
            patterns.append({
                'pattern': 'Vesica Piscis',
                'significance': 'Creation, duality, sacred feminine',
                'energy': 'Generative and creative',
                'recommendation': 'Powerful for entrance areas or creative spaces'
            })
        
        # Verificar Flor da Vida
        if self._detect_flower_of_life(floor_plan_data):
            patterns.append({
                'pattern': 'Flower of Life',
                'significance': 'Universal pattern, creation blueprint',
                'energy': 'Highest vibrational pattern',
                'recommendation': 'Consider incorporating in floor or ceiling design'
            })
        
        return {
            'patterns_identified': len(patterns),
            'patterns': patterns,
            'sacred_geometry_score': len(patterns) * 20,  # Max 100 for 5 patterns
            'recommendations': self._generate_pattern_recommendations(patterns)
        }
    
    def calculate_fibonacci_sequence(self, n: int = 10) -> List[int]:
        """
        Calcula sequência de Fibonacci
        
        Args:
            n: Número de termos
            
        Returns:
            Sequência de Fibonacci
        """
        sequence = [0, 1]
        for i in range(2, n):
            sequence.append(sequence[i-1] + sequence[i-2])
        return sequence
    
    def analyze_fibonacci_proportions(self, dimensions: List[float]) -> Dict[str, Any]:
        """
        Analisa se dimensões seguem proporções de Fibonacci
        
        Args:
            dimensions: Lista de dimensões para analisar
            
        Returns:
            Análise de proporções Fibonacci
        """
        fib_sequence = self.calculate_fibonacci_sequence(20)
        
        matches = []
        for dim in dimensions:
            # Encontrar número Fibonacci mais próximo
            closest_fib = min(fib_sequence, key=lambda x: abs(x - dim))
            deviation = abs(dim - closest_fib)
            deviation_percentage = (deviation / max(dim, 1)) * 100
            
            if deviation_percentage < 10:  # Dentro de 10%
                matches.append({
                    'dimension': dim,
                    'fibonacci_number': closest_fib,
                    'deviation_percentage': round(deviation_percentage, 2),
                    'is_match': True
                })
        
        return {
            'dimensions_analyzed': len(dimensions),
            'fibonacci_matches': len(matches),
            'matches': matches,
            'fibonacci_compliance': (len(matches) / len(dimensions)) * 100 if dimensions else 0,
            'recommendation': 'Excellent Fibonacci alignment' if len(matches) / len(dimensions) > 0.5 else 'Consider adjusting dimensions to Fibonacci numbers'
        }
    
    def analyze_platonic_solids(self, room_dimensions: Dict[str, float]) -> Dict[str, Any]:
        """
        Analisa relação com sólidos platônicos
        
        Args:
            room_dimensions: Dimensões do ambiente
            
        Returns:
            Análise de sólidos platônicos
        """
        width = room_dimensions.get('width', 0)
        height = room_dimensions.get('height', 0)
        depth = room_dimensions.get('depth', 0)
        
        # Verificar se forma um cubo (hexaedro)
        is_cube = (abs(width - height) / max(width, height) < 0.1 and
                   abs(width - depth) / max(width, depth) < 0.1 if depth else False)
        
        # Verificar proporções de outros sólidos platônicos
        solids = []
        
        if is_cube:
            solids.append({
                'solid': 'Cube (Hexahedron)',
                'element': 'Earth',
                'significance': 'Stability, grounding, material world',
                'faces': 6,
                'vertices': 8,
                'edges': 12,
                'energy': 'Grounding and stabilizing'
            })
        
        # Tetraedro (proporção 1:1:sqrt(2))
        if depth and abs((height / width) - self.SQRT_2) < 0.1:
            solids.append({
                'solid': 'Tetrahedron',
                'element': 'Fire',
                'significance': 'Transformation, energy, action',
                'faces': 4,
                'vertices': 4,
                'edges': 6,
                'energy': 'Activating and transformative'
            })
        
        # Octaedro (proporção específica)
        if depth and abs((height / width) - 1.0) < 0.1:
            solids.append({
                'solid': 'Octahedron',
                'element': 'Air',
                'significance': 'Balance, harmony, integration',
                'faces': 8,
                'vertices': 6,
                'edges': 12,
                'energy': 'Balancing and harmonizing'
            })
        
        return {
            'solids_identified': len(solids),
            'solids': solids,
            'platonic_alignment': 'strong' if len(solids) > 0 else 'weak',
            'recommendations': self._generate_platonic_recommendations(solids)
        }
    
    def calculate_sacred_proportions_for_space(self, area_m2: float, 
                                               ceiling_height: float = None) -> Dict[str, Any]:
        """
        Calcula proporções sagradas ideais para um espaço
        
        Args:
            area_m2: Área em metros quadrados
            ceiling_height: Altura do teto (opcional)
            
        Returns:
            Proporções ideais sugeridas
        """
        # Calcular dimensões baseadas em proporção áurea
        # Se área = width * height e width/height = phi
        # Então: width = sqrt(area * phi) e height = sqrt(area / phi)
        
        golden_width = math.sqrt(area_m2 * self.PHI)
        golden_height = math.sqrt(area_m2 / self.PHI)
        
        # Calcular dimensões baseadas em proporção de prata
        silver_width = math.sqrt(area_m2 * self.SILVER_RATIO)
        silver_height = math.sqrt(area_m2 / self.SILVER_RATIO)
        
        # Calcular dimensões quadradas (1:1)
        square_side = math.sqrt(area_m2)
        
        suggestions = {
            'golden_ratio_layout': {
                'width': round(golden_width, 2),
                'height': round(golden_height, 2),
                'ratio': round(self.PHI, 3),
                'name': 'Golden Rectangle',
                'significance': 'Most harmonious proportion in nature',
                'ideal_for': 'Living rooms, meditation spaces, main halls'
            },
            'silver_ratio_layout': {
                'width': round(silver_width, 2),
                'height': round(silver_height, 2),
                'ratio': round(self.SILVER_RATIO, 3),
                'name': 'Silver Rectangle',
                'significance': 'Dynamic and balanced proportion',
                'ideal_for': 'Offices, studios, creative spaces'
            },
            'square_layout': {
                'width': round(square_side, 2),
                'height': round(square_side, 2),
                'ratio': 1.0,
                'name': 'Perfect Square',
                'significance': 'Stability and grounding',
                'ideal_for': 'Meditation rooms, sacred spaces, bedrooms'
            }
        }
        
        if ceiling_height:
            # Calcular volume ideal
            golden_volume = area_m2 * ceiling_height
            
            # Sugerir altura de teto baseada em proporções
            suggestions['ceiling_height_suggestions'] = {
                'current': ceiling_height,
                'golden_ratio_to_width': round(golden_width / self.PHI, 2),
                'golden_ratio_to_height': round(golden_height / self.PHI, 2),
                'minimum_recommended': round(math.sqrt(area_m2) * 0.3, 2),
                'maximum_recommended': round(math.sqrt(area_m2) * 0.5, 2)
            }
        
        return {
            'area_m2': area_m2,
            'ceiling_height': ceiling_height,
            'layout_suggestions': suggestions,
            'recommended_layout': 'golden_ratio_layout',
            'fibonacci_dimensions': self._suggest_fibonacci_dimensions(area_m2)
        }
    
    def perform_complete_analysis(self, floor_plan_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Realiza análise completa de geometria sagrada
        
        Args:
            floor_plan_data: Dados da planta baixa
            
        Returns:
            Análise completa
        """
        rooms = floor_plan_data.get('rooms', [])
        
        room_analyses = []
        for room in rooms:
            width = room.get('width', 0)
            height = room.get('height', 0)
            depth = room.get('depth')
            area = width * height if width and height else room.get('area', 0)
            
            room_analysis = {
                'room_name': room.get('name', 'Unknown'),
                'dimensions': self.analyze_dimensions(width, height, depth),
                'sacred_proportions': self.calculate_sacred_proportions_for_space(area, depth),
                'platonic_solids': self.analyze_platonic_solids(room) if depth else None
            }
            
            room_analyses.append(room_analysis)
        
        # Análise geral da planta
        overall_dimensions = floor_plan_data.get('overall_dimensions', {})
        
        return {
            'analysis_date': self.analysis_date.isoformat(),
            'overall_analysis': {
                'dimensions': self.analyze_dimensions(
                    overall_dimensions.get('width', 0),
                    overall_dimensions.get('height', 0),
                    overall_dimensions.get('depth')
                ),
                'sacred_patterns': self.identify_sacred_patterns(floor_plan_data)
            },
            'room_analyses': room_analyses,
            'fibonacci_analysis': self.analyze_fibonacci_proportions(
                [r.get('width', 0) for r in rooms] + [r.get('height', 0) for r in rooms]
            ),
            'overall_assessment': self._generate_overall_geometry_assessment(room_analyses),
            'recommendations': self._generate_comprehensive_geometry_recommendations(room_analyses)
        }
    
    # Métodos auxiliares privados
    
    def _check_ratio(self, dim1: float, dim2: float, target_ratio: float, ratio_name: str) -> Dict[str, Any]:
        """Verifica se dimensões seguem uma proporção específica"""
        ratio = max(dim1, dim2) / min(dim1, dim2)
        deviation = abs(ratio - target_ratio)
        deviation_percentage = (deviation / target_ratio) * 100
        
        is_match = deviation_percentage <= (self.TOLERANCE_MODERATE * 100)
        
        return {
            'is_match': is_match,
            'ratio_name': ratio_name,
            'calculated_ratio': round(ratio, 6),
            'target_ratio': round(target_ratio, 6),
            'deviation_percentage': round(deviation_percentage, 2)
        }
    
    def _assess_ratio_quality(self, deviation_percentage: float) -> str:
        """Avalia qualidade da proporção"""
        if deviation_percentage <= 2:
            return 'excellent'
        elif deviation_percentage <= 5:
            return 'good'
        elif deviation_percentage <= 10:
            return 'acceptable'
        else:
            return 'poor'
    
    def _generate_golden_ratio_recommendation(self, is_golden: bool, deviation_percentage: float) -> str:
        """Gera recomendação para proporção áurea"""
        if is_golden:
            return "Excellent golden ratio compliance. Maintain these proportions."
        elif deviation_percentage < 10:
            return f"Close to golden ratio. Consider minor adjustment to achieve perfect proportion."
        else:
            return f"Significant deviation from golden ratio. Consider redesigning dimensions for better harmony."
    
    def _find_best_ratio_match(self, analyses: Dict) -> Dict[str, Any]:
        """Encontra a melhor correspondência de proporção"""
        best_match = None
        best_deviation = float('inf')
        
        for dimension_pair, ratios in analyses.items():
            for ratio_type, ratio_data in ratios.items():
                if 'deviation_percentage' in ratio_data:
                    if ratio_data['deviation_percentage'] < best_deviation:
                        best_deviation = ratio_data['deviation_percentage']
                        best_match = {
                            'dimension_pair': dimension_pair,
                            'ratio_type': ratio_type,
                            'deviation_percentage': ratio_data['deviation_percentage']
                        }
        
        return best_match
    
    def _calculate_harmony_score(self, analyses: Dict) -> float:
        """Calcula score de harmonia (0-100)"""
        total_checks = 0
        matches = 0
        
        for dimension_pair, ratios in analyses.items():
            for ratio_type, ratio_data in ratios.items():
                total_checks += 1
                if ratio_data.get('is_golden_ratio') or ratio_data.get('is_match'):
                    matches += 1
        
        return round((matches / total_checks) * 100, 2) if total_checks > 0 else 0
    
    def _generate_dimension_recommendations(self, analyses: Dict, width: float, 
                                           height: float, depth: Optional[float]) -> List[str]:
        """Gera recomendações para dimensões"""
        recommendations = []
        
        best_match = self._find_best_ratio_match(analyses)
        
        if best_match and best_match['deviation_percentage'] > 5:
            recommendations.append(f"Consider adjusting dimensions to achieve {best_match['ratio_type']}")
        
        # Sugerir dimensões ideais
        ideal_height = width / self.PHI
        recommendations.append(f"For golden ratio with width {width}m, ideal height would be {round(ideal_height, 2)}m")
        
        return recommendations
    
    def _detect_vesica_piscis(self, floor_plan_data: Dict) -> bool:
        """Detecta padrão Vesica Piscis"""
        # Simplificação: verificar se há dois círculos intersectando
        shapes = floor_plan_data.get('shapes', [])
        circles = [s for s in shapes if s.get('type') == 'circle']
        return len(circles) >= 2
    
    def _detect_flower_of_life(self, floor_plan_data: Dict) -> bool:
        """Detecta padrão Flor da Vida"""
        # Simplificação: verificar se há múltiplos círculos em padrão
        shapes = floor_plan_data.get('shapes', [])
        circles = [s for s in shapes if s.get('type') == 'circle']
        return len(circles) >= 7  # Flor da Vida tem 7 círculos mínimo
    
    def _generate_pattern_recommendations(self, patterns: List[Dict]) -> List[str]:
        """Gera recomendações baseadas em padrões"""
        recommendations = []
        
        if len(patterns) == 0:
            recommendations.append("Consider incorporating sacred geometric patterns in design")
            recommendations.append("Add circular or hexagonal elements for harmony")
        else:
            recommendations.append("Maintain identified sacred patterns in final design")
            recommendations.append("Consider amplifying patterns through decorative elements")
        
        return recommendations
    
    def _generate_platonic_recommendations(self, solids: List[Dict]) -> List[str]:
        """Gera recomendações baseadas em sólidos platônicos"""
        if not solids:
            return ["Consider incorporating Platonic solid proportions for enhanced harmony"]
        
        recommendations = []
        for solid in solids:
            recommendations.append(f"Identified {solid['solid']} - enhance {solid['element']} element energy")
        
        return recommendations
    
    def _suggest_fibonacci_dimensions(self, area_m2: float) -> Dict[str, Any]:
        """Sugere dimensões baseadas em Fibonacci"""
        fib_sequence = self.calculate_fibonacci_sequence(20)
        
        # Encontrar par de Fibonacci que resulta em área próxima
        best_pair = None
        best_diff = float('inf')
        
        for i in range(len(fib_sequence) - 1):
            for j in range(i, len(fib_sequence)):
                fib_area = fib_sequence[i] * fib_sequence[j]
                diff = abs(fib_area - area_m2)
                
                if diff < best_diff:
                    best_diff = diff
                    best_pair = (fib_sequence[i], fib_sequence[j])
        
        return {
            'width': best_pair[1] if best_pair else 0,
            'height': best_pair[0] if best_pair else 0,
            'area': best_pair[0] * best_pair[1] if best_pair else 0,
            'deviation_from_target': round(best_diff, 2)
        }
    
    def _generate_overall_geometry_assessment(self, room_analyses: List[Dict]) -> Dict[str, Any]:
        """Gera avaliação geral de geometria"""
        total_harmony = sum([r['dimensions']['harmony_score'] for r in room_analyses])
        avg_harmony = total_harmony / len(room_analyses) if room_analyses else 0
        
        return {
            'sacred_geometry_score': round(avg_harmony, 2),
            'rating': 'excellent' if avg_harmony > 70 else 'good' if avg_harmony > 50 else 'needs_improvement',
            'rooms_analyzed': len(room_analyses),
            'overall_compliance': 'high' if avg_harmony > 70 else 'medium' if avg_harmony > 40 else 'low'
        }
    
    def _generate_comprehensive_geometry_recommendations(self, room_analyses: List[Dict]) -> List[str]:
        """Gera recomendações abrangentes de geometria"""
        recommendations = [
            "Prioritize golden ratio (1.618) in main living spaces",
            "Use Fibonacci numbers for modular dimensions",
            "Incorporate circular elements for unity and flow",
            "Consider sacred geometric patterns in floor and ceiling design",
            "Align room proportions with Platonic solids where possible"
        ]
        
        return recommendations


# Função auxiliar para uso direto
def analyze_sacred_geometry(floor_plan_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Função auxiliar para realizar análise completa de geometria sagrada
    
    Args:
        floor_plan_data: Dados da planta baixa
        
    Returns:
        Análise completa de geometria sagrada
    """
    analyzer = SacredGeometryAnalyzer()
    return analyzer.perform_complete_analysis(floor_plan_data)


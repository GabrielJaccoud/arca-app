"""
Script de teste para as novas funcionalidades avançadas do Sistema ARCA
Testa Geobiologia, EMF, Linhas Ley, Geometria Sagrada e Arquitetura Sagrada
"""

import sys
sys.path.append('/home/ubuntu/arca-app/src')

from geobiology_analyzer import analyze_geobiology
from emf_analyzer import analyze_emf
from leyline_analyzer import analyze_ley_lines
from sacred_geometry_analyzer import analyze_sacred_geometry
from sacred_architecture_analyzer import analyze_sacred_architecture
import json


def test_geobiology():
    """Testa análise geobiológica"""
    print("\n" + "="*80)
    print("TESTE: ANÁLISE GEOBIOLÓGICA")
    print("="*80)
    
    # Coordenadas de Rio das Ostras, RJ
    latitude = -22.5264
    longitude = -41.9456
    area_width = 15.0  # metros
    area_height = 20.0  # metros
    soil_type = 'clay'
    
    result = analyze_geobiology(latitude, longitude, area_width, area_height, soil_type)
    
    print(f"\nLocalização: {latitude}, {longitude}")
    print(f"Área analisada: {area_width}m x {area_height}m")
    print(f"Tipo de solo: {soil_type}")
    
    print("\n--- Grade Hartmann ---")
    hartmann = result['hartmann_grid']
    print(f"Linhas N-S: {len(hartmann['ns_lines'])}")
    print(f"Linhas L-O: {len(hartmann['ew_lines'])}")
    print(f"Cruzamentos: {hartmann['total_crossings']}")
    
    print("\n--- Grade Curry ---")
    curry = result['curry_grid']
    print(f"Cruzamentos: {curry['total_crossings']}")
    
    print("\n--- Zonas Geopatogênicas ---")
    geopathogenic = result['geopathogenic_zones']
    print(f"Total de zonas de risco: {geopathogenic['total_geopathogenic_zones']}")
    print(f"Avaliação geral de risco: {geopathogenic['overall_risk_assessment']}")
    
    print("\n--- Avaliação Geral ---")
    assessment = result['overall_assessment']
    print(f"Score de saúde geobiológica: {assessment['geobiological_health_score']}/100")
    print(f"Nível de risco: {assessment['risk_level']}")
    print(f"Adequado para habitação: {assessment['suitable_for_habitation']}")
    
    return result


def test_emf():
    """Testa análise de EMF"""
    print("\n" + "="*80)
    print("TESTE: ANÁLISE DE CAMPOS ELETROMAGNÉTICOS (EMF)")
    print("="*80)
    
    # Coordenadas de Rio das Ostras, RJ
    latitude = -22.5264
    longitude = -41.9456
    
    result = analyze_emf(latitude, longitude, include_internal=True)
    
    print(f"\nLocalização: {latitude}, {longitude}")
    
    print("\n--- Fontes Externas ---")
    ext = result['external_sources']
    print(f"Torres de celular detectadas: {ext['cell_towers']['towers_detected']}")
    print(f"Linhas de transmissão detectadas: {ext['power_lines']['power_lines_detected']}")
    print(f"Transformadores detectados: {ext['transformers']['transformers_detected']}")
    
    print("\n--- Exposição Total ---")
    total = result['total_exposure']
    print(f"Exposição total: {total['total_exposure_uT']:.4f} μT")
    print(f"Limite seguro residencial: {total['safe_limit_residential_uT']} μT")
    print(f"Percentual do limite: {total['exposure_percentage']:.2f}%")
    print(f"Status de segurança: {total['safety_status']}")
    print(f"Nível de risco: {total['risk_level']}")
    print(f"Em conformidade: {total['compliance']}")
    
    print("\n--- Avaliação Geral ---")
    assessment = result['overall_assessment']
    print(f"Score de saúde EMF: {assessment['emf_health_score']}/100")
    print(f"Adequado para habitação: {assessment['suitable_for_habitation']}")
    
    return result


def test_ley_lines():
    """Testa análise de linhas ley"""
    print("\n" + "="*80)
    print("TESTE: ANÁLISE DE LINHAS LEY E GEOGRAFIA SAGRADA")
    print("="*80)
    
    # Coordenadas de Rio das Ostras, RJ
    latitude = -22.5264
    longitude = -41.9456
    
    result = analyze_ley_lines(latitude, longitude, radius_km=50.0)
    
    print(f"\nLocalização: {latitude}, {longitude}")
    
    print("\n--- Sítios Sagrados Próximos ---")
    sites = result['sacred_sites']
    print(f"Total encontrado: {sites['total_found']}")
    if sites['closest_site']:
        closest = sites['closest_site']
        print(f"Mais próximo: {closest['name']}")
        print(f"  Distância: {closest['distance_km']} km")
        print(f"  Direção: {closest['cardinal_direction']}")
        print(f"  Tipo: {closest['type']}")
    
    print("\n--- Linhas Ley ---")
    ley_lines = result['ley_lines']
    print(f"Linhas identificadas: {ley_lines['ley_lines_identified']}")
    print(f"Linhas passando pelo local: {len(ley_lines['lines_passing_through'])}")
    
    print("\n--- Vórtices Energéticos ---")
    vortices = result['energy_vortices']
    print(f"Vórtices detectados: {vortices['vortices_detected']}")
    print(f"Local é vórtice: {vortices['location_is_vortex']}")
    print(f"Força do vórtice: {vortices['vortex_strength']}")
    
    print("\n--- Alinhamentos Astronômicos ---")
    astro = result['astronomical_alignments']
    print(f"Orientação ótima: {astro['optimal_building_orientation']['primary_axis']}")
    print(f"Entrada recomendada: {astro['optimal_building_orientation']['recommended_entrance']}")
    
    print("\n--- Avaliação Geral ---")
    assessment = result['overall_assessment']
    print(f"Score de potencial energético: {assessment['energetic_potential_score']}/100")
    print(f"Classificação de geografia sagrada: {assessment['sacred_geography_rating']}")
    print(f"Ideal para arquitetura sagrada: {assessment['ideal_for_sacred_architecture']}")
    
    return result


def test_sacred_geometry():
    """Testa análise de geometria sagrada"""
    print("\n" + "="*80)
    print("TESTE: ANÁLISE DE GEOMETRIA SAGRADA")
    print("="*80)
    
    # Dados simulados de planta baixa
    floor_plan_data = {
        'overall_dimensions': {
            'width': 15.0,
            'height': 24.27,  # Aproximadamente 15 * 1.618 (proporção áurea)
            'depth': 3.0
        },
        'rooms': [
            {
                'name': 'Sala de Estar',
                'type': 'living_room',
                'width': 5.0,
                'height': 8.09,  # 5 * 1.618
                'depth': 3.0,
                'area': 40.45
            },
            {
                'name': 'Quarto Principal',
                'type': 'master_bedroom',
                'width': 4.0,
                'height': 6.47,  # 4 * 1.618
                'depth': 3.0,
                'area': 25.88
            },
            {
                'name': 'Escritório',
                'type': 'office',
                'width': 3.0,
                'height': 4.85,  # 3 * 1.618
                'depth': 3.0,
                'area': 14.55
            }
        ],
        'shapes': [
            {'type': 'circle'},
            {'type': 'square'},
            {'type': 'hexagon'}
        ]
    }
    
    result = analyze_sacred_geometry(floor_plan_data)
    
    print("\n--- Análise Geral ---")
    overall = result['overall_analysis']
    dims = overall['dimensions']
    print(f"Proporção largura x altura: {dims['ratio_analyses']['width_height']['golden_ratio']['calculated_ratio']:.3f}")
    print(f"É proporção áurea: {dims['ratio_analyses']['width_height']['golden_ratio']['is_golden_ratio']}")
    print(f"Score de harmonia: {dims['harmony_score']}/100")
    
    print("\n--- Padrões Sagrados ---")
    patterns = overall['sacred_patterns']
    print(f"Padrões identificados: {patterns['patterns_identified']}")
    for pattern in patterns['patterns']:
        print(f"  - {pattern['pattern']}: {pattern['significance']}")
    
    print("\n--- Análise de Fibonacci ---")
    fib = result['fibonacci_analysis']
    print(f"Dimensões analisadas: {fib['dimensions_analyzed']}")
    print(f"Correspondências Fibonacci: {fib['fibonacci_matches']}")
    print(f"Conformidade Fibonacci: {fib['fibonacci_compliance']:.2f}%")
    
    print("\n--- Avaliação Geral ---")
    assessment = result['overall_assessment']
    print(f"Score de geometria sagrada: {assessment['sacred_geometry_score']}/100")
    print(f"Classificação: {assessment['rating']}")
    print(f"Conformidade geral: {assessment['overall_compliance']}")
    
    return result


def test_sacred_architecture():
    """Testa análise de arquitetura sagrada"""
    print("\n" + "="*80)
    print("TESTE: ANÁLISE DE ARQUITETURA SAGRADA")
    print("="*80)
    
    # Dados simulados de edificação
    building_data = {
        'latitude': -22.5264,
        'longitude': -41.9456,
        'orientation': 'north',
        'floor_plan': {
            'rooms': [
                {
                    'name': 'Sala de Estar',
                    'type': 'living_room',
                    'width': 5.0,
                    'height': 8.09,
                    'ceiling_height': 3.0
                },
                {
                    'name': 'Quarto Principal',
                    'type': 'master_bedroom',
                    'width': 4.0,
                    'height': 6.47,
                    'ceiling_height': 2.8
                }
            ],
            'circulation_paths': [
                {'type': 'main', 'width': 1.5},
                {'type': 'secondary', 'width': 1.0}
            ]
        },
        'materials': [
            {'name': 'wood', 'location': 'floors'},
            {'name': 'stone', 'location': 'walls'},
            {'name': 'glass', 'location': 'windows'},
            {'name': 'bamboo', 'location': 'ceiling'}
        ],
        'openings': [
            {'orientation': 'east', 'type': 'window'},
            {'orientation': 'west', 'type': 'window'},
            {'orientation': 'north', 'type': 'door'}
        ],
        'entrance': {
            'orientation': 'east',
            'width': 1.5,
            'has_overhang': True
        }
    }
    
    result = analyze_sacred_architecture(building_data)
    
    print("\n--- Análise de Materiais ---")
    materials = result['materials_analysis']
    print(f"Materiais analisados: {materials['materials_analyzed']}")
    print(f"Percentual de materiais naturais: {materials['natural_material_percentage']}%")
    print(f"Score de sustentabilidade: {materials['sustainability_score']}/100")
    print(f"Elemento dominante: {materials['energy_balance']['dominant_element']}")
    
    print("\n--- Espaços Sagrados ---")
    sacred = result['sacred_spaces']
    print(f"Espaços sagrados identificados: {sacred['sacred_spaces_identified']}")
    print(f"Possui espaço sagrado dedicado: {sacred['has_dedicated_sacred_space']}")
    
    print("\n--- Integração Astronômica ---")
    astro = result['astronomical_integration']
    print(f"Orientação da edificação: {astro['building_orientation']['orientation']}")
    print(f"Qualidade da orientação: {astro['building_orientation']['quality']}")
    print(f"Acesso solar matinal: {astro['solar_access']['has_morning_sun']}")
    print(f"Equilíbrio solar: {astro['solar_access']['solar_balance']}")
    print(f"Score de integração: {astro['integration_score']}/100")
    
    print("\n--- Simetria e Equilíbrio ---")
    symmetry = result['symmetry_balance']
    print(f"Possui eixo primário: {symmetry['axial_symmetry']['has_primary_axis']}")
    print(f"Equilíbrio de massas: {symmetry['mass_balance']['is_balanced']}")
    print(f"Score de simetria: {symmetry['overall_symmetry_score']}/100")
    
    print("\n--- Avaliação Geral ---")
    assessment = result['overall_assessment']
    print(f"Score de arquitetura sagrada: {assessment['sacred_architecture_score']}/100")
    print(f"Classificação: {assessment['rating']}")
    
    return result


def main():
    """Executa todos os testes"""
    print("\n")
    print("╔" + "═"*78 + "╗")
    print("║" + " "*20 + "SISTEMA ARCA - TESTES AVANÇADOS" + " "*27 + "║")
    print("║" + " "*15 + "Geobiologia, EMF, Linhas Ley, Geometria Sagrada" + " "*15 + "║")
    print("╚" + "═"*78 + "╝")
    
    try:
        # Executar testes
        geobiology_result = test_geobiology()
        emf_result = test_emf()
        leyline_result = test_ley_lines()
        sacred_geometry_result = test_sacred_geometry()
        sacred_architecture_result = test_sacred_architecture()
        
        # Resumo final
        print("\n" + "="*80)
        print("RESUMO GERAL DOS TESTES")
        print("="*80)
        
        print("\n✓ Geobiologia:")
        print(f"  Score: {geobiology_result['overall_assessment']['geobiological_health_score']}/100")
        print(f"  Risco: {geobiology_result['overall_assessment']['risk_level']}")
        
        print("\n✓ EMF:")
        print(f"  Score: {emf_result['overall_assessment']['emf_health_score']}/100")
        print(f"  Risco: {emf_result['total_exposure']['risk_level']}")
        
        print("\n✓ Linhas Ley:")
        print(f"  Score: {leyline_result['overall_assessment']['energetic_potential_score']}/100")
        print(f"  Classificação: {leyline_result['overall_assessment']['sacred_geography_rating']}")
        
        print("\n✓ Geometria Sagrada:")
        print(f"  Score: {sacred_geometry_result['overall_assessment']['sacred_geometry_score']}/100")
        print(f"  Classificação: {sacred_geometry_result['overall_assessment']['rating']}")
        
        print("\n✓ Arquitetura Sagrada:")
        print(f"  Score: {sacred_architecture_result['overall_assessment']['sacred_architecture_score']}/100")
        print(f"  Classificação: {sacred_architecture_result['overall_assessment']['rating']}")
        
        # Calcular score geral integrado
        scores = [
            geobiology_result['overall_assessment']['geobiological_health_score'],
            emf_result['overall_assessment']['emf_health_score'],
            leyline_result['overall_assessment']['energetic_potential_score'],
            sacred_geometry_result['overall_assessment']['sacred_geometry_score'],
            sacred_architecture_result['overall_assessment']['sacred_architecture_score']
        ]
        
        overall_score = sum(scores) / len(scores)
        
        print("\n" + "="*80)
        print(f"SCORE GERAL INTEGRADO: {overall_score:.2f}/100")
        print("="*80)
        
        if overall_score >= 80:
            print("\n🌟 EXCELENTE: Edificação altamente harmônica e saudável")
        elif overall_score >= 60:
            print("\n✓ BOM: Edificação adequada com algumas melhorias recomendadas")
        elif overall_score >= 40:
            print("\n⚠ REGULAR: Edificação necessita de correções significativas")
        else:
            print("\n⚠ ATENÇÃO: Edificação requer intervenções urgentes")
        
        print("\n✅ Todos os testes concluídos com sucesso!\n")
        
    except Exception as e:
        print(f"\n❌ Erro durante os testes: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()


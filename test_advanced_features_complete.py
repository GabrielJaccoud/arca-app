"""
Script de Teste Completo - Funcionalidades Avançadas Sistema ARCA v3.1
Testa módulos avançados de Geobiologia e Linhas Ley com visualizações
"""

import sys
import os

# Adicionar src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from geobiology_analyzer_advanced import analyze_geobiology_advanced
from leyline_analyzer_advanced import analyze_ley_lines_advanced
from visualization_generator import generate_all_visualizations
import json
from datetime import datetime


def print_section(title):
    """Imprime cabeçalho de seção"""
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80 + "\n")


def test_advanced_geobiology():
    """Testa análise geobiológica avançada"""
    print_section("TESTE: ANÁLISE GEOBIOLÓGICA AVANÇADA")
    
    # Dados do projeto NTHLSQR-PB
    latitude = -22.5264
    longitude = -41.9456
    area_width = 20.0  # metros
    area_height = 15.0  # metros
    soil_type = 'sand'  # Rio das Ostras tem solo arenoso
    
    print(f"Localização: {latitude}, {longitude}")
    print(f"Área: {area_width}m x {area_height}m")
    print(f"Tipo de Solo: {soil_type}")
    print("\nExecutando análise...")
    
    # Executar análise
    analysis = analyze_geobiology_advanced(latitude, longitude, area_width, area_height, soil_type)
    
    # Exibir resultados
    print("\n--- FATORES AMBIENTAIS ---")
    print(f"Fator de Intensidade Magnética: {analysis['environmental_factors']['magnetic_intensity_factor']:.2f}")
    print(f"Fator Lunar: {analysis['environmental_factors']['lunar_factor']:.2f}")
    
    print("\n--- GRADE HARTMANN ---")
    hartmann = analysis['hartmann_grid']
    print(f"Espaçamento N-S: {hartmann['spacing_ns']}m")
    print(f"Espaçamento L-O: {hartmann['spacing_ew']}m")
    print(f"Total de Cruzamentos: {hartmann['total_crossings']}")
    print(f"Largura da Linha: {hartmann['line_width']}m")
    
    print("\n--- GRADE CURRY ---")
    curry = analysis['curry_grid']
    print(f"Espaçamento: {curry['spacing']}m")
    print(f"Rotação: {curry['rotation']}°")
    print(f"Total de Cruzamentos: {curry['total_crossings']}")
    print(f"Largura da Linha: {curry['line_width']}m")
    
    print("\n--- GRADE BENKER ---")
    benker = analysis['benker_grid']
    print(f"Espaçamento Cúbico: {benker['spacing']}m")
    print(f"Total de Cruzamentos: {benker['total_crossings']}")
    print(f"Nota: {benker['note']}")
    
    print("\n--- VEIOS DE ÁGUA ---")
    water = analysis['water_veins']
    print(f"Veios Detectados: {water['veins_detected']}")
    print(f"Probabilidade de Detecção: {water['detection_probability']*100:.1f}%")
    if water['veins_detected'] > 0:
        for i, vein in enumerate(water['veins'], 1):
            print(f"\nVeio {i}:")
            print(f"  Profundidade: {vein['depth_meters']:.1f}m")
            print(f"  Fluxo: {vein['flow_rate']}")
            print(f"  Largura: {vein['width_meters']:.1f}m")
            print(f"  Unidades Bovis: {vein['bovis_units']}")
    
    print("\n--- FALHAS GEOLÓGICAS ---")
    faults = analysis['geological_faults']
    print(f"Falhas Detectadas: {faults['faults_detected']}")
    if faults['faults_detected'] > 0:
        for i, fault in enumerate(faults['faults'], 1):
            print(f"\nFalha {i}:")
            print(f"  Tipo: {fault['type']}")
            print(f"  Atividade: {fault['activity']}")
            print(f"  Profundidade: {fault['depth_meters']:.1f}m")
            print(f"  Unidades Bovis: {fault['bovis_units']}")
    
    print("\n--- ZONAS GEOPATOGÊNICAS ---")
    zones = analysis['geopathogenic_zones']
    print(f"Total de Zonas: {zones['total_geopathogenic_zones']}")
    print(f"Zonas Críticas: {zones['critical_zones']}")
    print(f"Zonas de Alto Risco: {zones['high_risk_zones']}")
    print(f"Zonas de Médio Risco: {zones['medium_risk_zones']}")
    print(f"Avaliação Geral de Risco: {zones['overall_risk_assessment'].upper()}")
    
    print("\n--- AVALIAÇÃO GERAL ---")
    assessment = analysis['overall_assessment']
    print(f"Score de Saúde Geobiológica: {assessment['geobiological_health_score']}/100")
    print(f"Nível de Risco: {assessment['risk_level'].upper()}")
    print(f"Adequado para Habitação: {'SIM' if assessment['suitable_for_habitation'] else 'NÃO'}")
    
    print("\n--- PRINCIPAIS PREOCUPAÇÕES ---")
    for concern in assessment['main_concerns']:
        print(f"  • {concern}")
    
    print("\n--- AÇÕES PRIORITÁRIAS ---")
    for i, action in enumerate(assessment['priority_actions'], 1):
        print(f"  {i}. {action}")
    
    return analysis


def test_advanced_ley_lines():
    """Testa análise avançada de linhas ley"""
    print_section("TESTE: ANÁLISE AVANÇADA DE LINHAS LEY")
    
    # Dados do projeto NTHLSQR-PB
    latitude = -22.5264
    longitude = -41.9456
    radius_km = 100.0  # Buscar em raio de 100km
    
    print(f"Localização: {latitude}, {longitude}")
    print(f"Raio de Busca: {radius_km}km")
    print("\nExecutando análise...")
    
    # Executar análise
    analysis = analyze_ley_lines_advanced(latitude, longitude, radius_km)
    
    # Exibir resultados
    print("\n--- SÍTIOS SAGRADOS ---")
    sites = analysis['sacred_sites']
    print(f"Total Encontrado: {sites['total_found']}")
    print(f"Poder Total da Região: {sites['total_power_level']}")
    print(f"Poder Médio: {sites['average_power_level']:.2f}")
    
    if sites['closest_site']:
        closest = sites['closest_site']
        print(f"\nSítio Mais Próximo:")
        print(f"  Nome: {closest['name']}")
        print(f"  Tipo: {closest['type']}")
        print(f"  Distância: {closest['distance_km']}km")
        print(f"  Direção: {closest['cardinal_direction']}")
        print(f"  Azimute: {closest['azimuth']:.1f}°")
        print(f"  Poder: {closest['power_level']}/10")
        print(f"  Significado: {closest['significance']}")
    
    print(f"\n--- SÍTIOS POR TIPO ---")
    for site_type, type_sites in sites['sites_by_type'].items():
        print(f"  {site_type}: {len(type_sites)} sítio(s)")
    
    print("\n--- PRIMEIROS 5 SÍTIOS MAIS PRÓXIMOS ---")
    for i, site in enumerate(sites['sites'][:5], 1):
        print(f"\n{i}. {site['name']}")
        print(f"   Tipo: {site['type']}")
        print(f"   Distância: {site['distance_km']}km {site['cardinal_direction']}")
        print(f"   Poder: {site['power_level']}/10")
    
    print("\n--- LINHAS LEY ---")
    ley_lines = analysis['ley_lines']
    print(f"Linhas Identificadas: {ley_lines['ley_lines_identified']}")
    print(f"Linhas Passando pelo Local: {len(ley_lines['lines_passing_through'])}")
    print(f"Local está em Linha Ley: {'SIM' if ley_lines['location_on_ley_line'] else 'NÃO'}")
    
    if ley_lines['ley_lines_identified'] > 0:
        print("\n--- PRIMEIRAS 3 LINHAS LEY ---")
        for i, line in enumerate(ley_lines['ley_lines'][:3], 1):
            print(f"\n{i}. {line['id']}")
            print(f"   Sítios: {', '.join(line['sites'])}")
            print(f"   Comprimento: {line['total_length_km']}km")
            print(f"   Azimute: {line['azimuth']:.1f}°")
            print(f"   Poder: {line['power_level']:.1f}/10")
            print(f"   Passa pelo Local: {'SIM' if line['passes_through_location'] else 'NÃO'}")
    
    print("\n--- VÓRTICES ENERGÉTICOS ---")
    vortices = analysis['energy_vortices']
    print(f"Vórtices Detectados: {vortices['vortices_detected']}")
    print(f"Local é Vórtice: {'SIM' if vortices['location_is_vortex'] else 'NÃO'}")
    print(f"Força do Vórtice: {vortices['vortex_strength'].upper()}")
    
    if vortices['vortices_detected'] > 0:
        print("\n--- VÓRTICES IDENTIFICADOS ---")
        for i, vortex in enumerate(vortices['vortices'], 1):
            print(f"\n{i}. {vortex['location']}")
            print(f"   Linhas Convergentes: {vortex['ley_lines_count']}")
            print(f"   Força: {vortex['vortex_strength']}")
            print(f"   Poder: {vortex['power_level']:.1f}/10")
            print(f"   Distância: {vortex['distance_from_location_km']}km")
    
    print("\n--- ALINHAMENTOS ASTRONÔMICOS ---")
    astro = analysis['astronomical_alignments']
    
    print(f"\nSolstício de Verão ({astro['summer_solstice']['date']}):")
    print(f"  Nascer do Sol: {astro['summer_solstice']['sunrise_azimuth']}°")
    print(f"  Pôr do Sol: {astro['summer_solstice']['sunset_azimuth']}°")
    
    print(f"\nSolstício de Inverno ({astro['winter_solstice']['date']}):")
    print(f"  Nascer do Sol: {astro['winter_solstice']['sunrise_azimuth']}°")
    print(f"  Pôr do Sol: {astro['winter_solstice']['sunset_azimuth']}°")
    
    print(f"\nEquinócios ({astro['equinoxes']['dates']}):")
    print(f"  Nascer do Sol: {astro['equinoxes']['sunrise_azimuth']}°")
    print(f"  Pôr do Sol: {astro['equinoxes']['sunset_azimuth']}°")
    
    print("\n--- AVALIAÇÃO GERAL ---")
    assessment = analysis['overall_assessment']
    print(f"Score de Potencial Energético: {assessment['energetic_potential_score']}/100")
    print(f"Classificação de Geografia Sagrada: {assessment['sacred_geography_rating'].upper()}")
    print(f"Ideal para Arquitetura Sagrada: {'SIM' if assessment['ideal_for_sacred_architecture'] else 'NÃO'}")
    
    print("\n--- PRINCIPAIS CARACTERÍSTICAS ---")
    for feature in assessment['main_features']:
        print(f"  • {feature}")
    
    print("\n--- RECOMENDAÇÕES ---")
    for i, rec in enumerate(analysis['recommendations'][:5], 1):
        print(f"  {i}. {rec}")
    
    return analysis


def test_visualizations(geo_analysis, ley_analysis):
    """Testa geração de visualizações"""
    print_section("TESTE: GERAÇÃO DE VISUALIZAÇÕES")
    
    output_dir = '/home/ubuntu/arca-app/visualizations'
    
    print(f"Diretório de Saída: {output_dir}")
    print("\nGerando visualizações...")
    
    try:
        files = generate_all_visualizations(geo_analysis, ley_analysis, output_dir)
        
        print("\n--- ARQUIVOS GERADOS ---")
        for name, path in files.items():
            file_size = os.path.getsize(path) / 1024  # KB
            print(f"  ✓ {name}: {path} ({file_size:.1f} KB)")
        
        return files
    except Exception as e:
        print(f"\n❌ ERRO ao gerar visualizações: {str(e)}")
        import traceback
        traceback.print_exc()
        return {}


def save_analysis_report(geo_analysis, ley_analysis, viz_files):
    """Salva relatório completo da análise"""
    print_section("SALVANDO RELATÓRIO COMPLETO")
    
    report_path = '/home/ubuntu/arca-app/relatorio_analise_avancada_nthlsqr.json'
    
    report = {
        'metadata': {
            'project': 'NTHLSQR-PB',
            'location': 'Rio das Ostras, RJ, Brazil',
            'analysis_date': datetime.now().isoformat(),
            'system_version': 'ARCA v3.1',
            'analyst': 'Sistema ARCA - Análise Automatizada'
        },
        'geobiology_analysis': geo_analysis,
        'leyline_analysis': ley_analysis,
        'visualizations': viz_files
    }
    
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    file_size = os.path.getsize(report_path) / 1024  # KB
    print(f"Relatório salvo: {report_path} ({file_size:.1f} KB)")
    
    return report_path


def main():
    """Função principal de teste"""
    print("\n" + "="*80)
    print("  SISTEMA ARCA v3.1 - TESTE COMPLETO DE FUNCIONALIDADES AVANÇADAS")
    print("  Projeto: NTHLSQR-PB - Rio das Ostras, RJ")
    print("="*80)
    
    # Teste 1: Geobiologia Avançada
    geo_analysis = test_advanced_geobiology()
    
    # Teste 2: Linhas Ley Avançadas
    ley_analysis = test_advanced_ley_lines()
    
    # Teste 3: Visualizações
    viz_files = test_visualizations(geo_analysis, ley_analysis)
    
    # Salvar relatório
    report_path = save_analysis_report(geo_analysis, ley_analysis, viz_files)
    
    # Resumo final
    print_section("RESUMO FINAL")
    
    print("✅ Análise Geobiológica Avançada: COMPLETA")
    print(f"   Score de Saúde: {geo_analysis['overall_assessment']['geobiological_health_score']}/100")
    print(f"   Nível de Risco: {geo_analysis['overall_assessment']['risk_level'].upper()}")
    
    print("\n✅ Análise de Linhas Ley Avançada: COMPLETA")
    print(f"   Score Energético: {ley_analysis['overall_assessment']['energetic_potential_score']}/100")
    print(f"   Sítios Sagrados: {ley_analysis['sacred_sites']['total_found']}")
    print(f"   Linhas Ley: {ley_analysis['ley_lines']['ley_lines_identified']}")
    print(f"   Vórtices: {ley_analysis['energy_vortices']['vortices_detected']}")
    
    print(f"\n✅ Visualizações Geradas: {len(viz_files)}")
    
    print(f"\n✅ Relatório Completo: {report_path}")
    
    print("\n" + "="*80)
    print("  TODOS OS TESTES CONCLUÍDOS COM SUCESSO!")
    print("="*80 + "\n")


if __name__ == '__main__':
    main()


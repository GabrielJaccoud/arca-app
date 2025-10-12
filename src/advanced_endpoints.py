"""
Endpoints avançados da API do Sistema ARCA
Inclui endpoints para Geobiologia, EMF, Linhas Ley, Geometria Sagrada e Arquitetura Sagrada
"""

from flask import Blueprint, request, jsonify
from models import (db, FloorPlan, GeobiologyAnalysis, EMFAnalysis, LeyLineAnalysis,
                    SacredGeometryAnalysis, SacredArchitectureAnalysis, IntegratedAnalysis)
from geobiology_analyzer import analyze_geobiology
from emf_analyzer import analyze_emf
from leyline_analyzer import analyze_ley_lines
from sacred_geometry_analyzer import analyze_sacred_geometry
from sacred_architecture_analyzer import analyze_sacred_architecture
import datetime

# Criar Blueprint para endpoints avançados
advanced_bp = Blueprint('advanced', __name__, url_prefix='/api/advanced')


# ===== GEOBIOLOGIA =====

@advanced_bp.route('/geobiology/analyze', methods=['POST'])
def analyze_geobiology_endpoint():
    """
    Endpoint para análise geobiológica
    
    Payload esperado:
    {
        "latitude": float,
        "longitude": float,
        "area_width": float,
        "area_height": float,
        "soil_type": str (opcional),
        "floor_plan_id": int (opcional)
    }
    """
    data = request.get_json()
    
    if not data:
        return jsonify({"status": "error", "message": "Dados JSON não fornecidos."}), 400
    
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    area_width = data.get('area_width')
    area_height = data.get('area_height')
    soil_type = data.get('soil_type', 'unknown')
    floor_plan_id = data.get('floor_plan_id')
    
    if not all([latitude, longitude, area_width, area_height]):
        return jsonify({
            "status": "error",
            "message": "Latitude, longitude, area_width e area_height são obrigatórios."
        }), 400
    
    # Realizar análise
    analysis_result = analyze_geobiology(
        latitude, longitude, area_width, area_height, soil_type
    )
    
    # Salvar no banco de dados
    new_analysis = GeobiologyAnalysis(
        floor_plan_id=floor_plan_id,
        latitude=latitude,
        longitude=longitude,
        area_width=area_width,
        area_height=area_height,
        soil_type=soil_type,
        hartmann_grid_data=analysis_result.get('hartmann_grid'),
        curry_grid_data=analysis_result.get('curry_grid'),
        water_veins=analysis_result.get('water_veins'),
        geological_faults=analysis_result.get('geological_faults'),
        geopathogenic_zones=analysis_result.get('geopathogenic_zones'),
        soil_radiation=analysis_result.get('soil_radiation'),
        overall_assessment=analysis_result.get('overall_assessment')
    )
    
    db.session.add(new_analysis)
    db.session.commit()
    
    return jsonify({
        "status": "success",
        "message": "Análise geobiológica realizada com sucesso.",
        "id": new_analysis.id,
        "analysis": analysis_result
    }), 200


@advanced_bp.route('/geobiology/analyses', methods=['GET'])
def get_geobiology_analyses():
    """Retorna todas as análises geobiológicas"""
    analyses = GeobiologyAnalysis.query.all()
    
    return jsonify([{
        "id": a.id,
        "latitude": a.latitude,
        "longitude": a.longitude,
        "area_width": a.area_width,
        "area_height": a.area_height,
        "soil_type": a.soil_type,
        "analysis_date": a.analysis_date.isoformat(),
        "overall_assessment": a.overall_assessment
    } for a in analyses]), 200


@advanced_bp.route('/geobiology/analyses/<int:analysis_id>', methods=['GET'])
def get_geobiology_analysis(analysis_id):
    """Retorna uma análise geobiológica específica"""
    analysis = GeobiologyAnalysis.query.get(analysis_id)
    
    if not analysis:
        return jsonify({"status": "error", "message": "Análise não encontrada."}), 404
    
    return jsonify({
        "id": analysis.id,
        "latitude": analysis.latitude,
        "longitude": analysis.longitude,
        "area_width": analysis.area_width,
        "area_height": analysis.area_height,
        "soil_type": analysis.soil_type,
        "hartmann_grid_data": analysis.hartmann_grid_data,
        "curry_grid_data": analysis.curry_grid_data,
        "water_veins": analysis.water_veins,
        "geological_faults": analysis.geological_faults,
        "geopathogenic_zones": analysis.geopathogenic_zones,
        "soil_radiation": analysis.soil_radiation,
        "overall_assessment": analysis.overall_assessment,
        "analysis_date": analysis.analysis_date.isoformat()
    }), 200


# ===== EMF (CAMPOS ELETROMAGNÉTICOS) =====

@advanced_bp.route('/emf/analyze', methods=['POST'])
def analyze_emf_endpoint():
    """
    Endpoint para análise de EMF
    
    Payload esperado:
    {
        "latitude": float,
        "longitude": float,
        "include_internal": bool (opcional),
        "appliances": list (opcional),
        "floor_plan_id": int (opcional)
    }
    """
    data = request.get_json()
    
    if not data:
        return jsonify({"status": "error", "message": "Dados JSON não fornecidos."}), 400
    
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    include_internal = data.get('include_internal', True)
    appliances = data.get('appliances')
    floor_plan_id = data.get('floor_plan_id')
    
    if not all([latitude, longitude]):
        return jsonify({
            "status": "error",
            "message": "Latitude e longitude são obrigatórios."
        }), 400
    
    # Realizar análise
    analysis_result = analyze_emf(latitude, longitude, include_internal, appliances)
    
    # Salvar no banco de dados
    new_analysis = EMFAnalysis(
        floor_plan_id=floor_plan_id,
        latitude=latitude,
        longitude=longitude,
        cell_towers=analysis_result.get('external_sources', {}).get('cell_towers'),
        power_lines=analysis_result.get('external_sources', {}).get('power_lines'),
        transformers=analysis_result.get('external_sources', {}).get('transformers'),
        internal_sources=analysis_result.get('internal_sources'),
        total_exposure=analysis_result.get('total_exposure'),
        overall_assessment=analysis_result.get('overall_assessment'),
        recommendations=analysis_result.get('recommendations')
    )
    
    db.session.add(new_analysis)
    db.session.commit()
    
    return jsonify({
        "status": "success",
        "message": "Análise de EMF realizada com sucesso.",
        "id": new_analysis.id,
        "analysis": analysis_result
    }), 200


@advanced_bp.route('/emf/analyses', methods=['GET'])
def get_emf_analyses():
    """Retorna todas as análises de EMF"""
    analyses = EMFAnalysis.query.all()
    
    return jsonify([{
        "id": a.id,
        "latitude": a.latitude,
        "longitude": a.longitude,
        "analysis_date": a.analysis_date.isoformat(),
        "total_exposure": a.total_exposure,
        "overall_assessment": a.overall_assessment
    } for a in analyses]), 200


@advanced_bp.route('/emf/analyses/<int:analysis_id>', methods=['GET'])
def get_emf_analysis(analysis_id):
    """Retorna uma análise de EMF específica"""
    analysis = EMFAnalysis.query.get(analysis_id)
    
    if not analysis:
        return jsonify({"status": "error", "message": "Análise não encontrada."}), 404
    
    return jsonify({
        "id": analysis.id,
        "latitude": analysis.latitude,
        "longitude": analysis.longitude,
        "cell_towers": analysis.cell_towers,
        "power_lines": analysis.power_lines,
        "transformers": analysis.transformers,
        "internal_sources": analysis.internal_sources,
        "total_exposure": analysis.total_exposure,
        "overall_assessment": analysis.overall_assessment,
        "recommendations": analysis.recommendations,
        "analysis_date": analysis.analysis_date.isoformat()
    }), 200


# ===== LINHAS LEY =====

@advanced_bp.route('/leylines/analyze', methods=['POST'])
def analyze_leylines_endpoint():
    """
    Endpoint para análise de linhas ley
    
    Payload esperado:
    {
        "latitude": float,
        "longitude": float,
        "radius_km": float (opcional),
        "floor_plan_id": int (opcional)
    }
    """
    data = request.get_json()
    
    if not data:
        return jsonify({"status": "error", "message": "Dados JSON não fornecidos."}), 400
    
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    radius_km = data.get('radius_km', 50.0)
    floor_plan_id = data.get('floor_plan_id')
    
    if not all([latitude, longitude]):
        return jsonify({
            "status": "error",
            "message": "Latitude e longitude são obrigatórios."
        }), 400
    
    # Realizar análise
    analysis_result = analyze_ley_lines(latitude, longitude, radius_km)
    
    # Salvar no banco de dados
    new_analysis = LeyLineAnalysis(
        floor_plan_id=floor_plan_id,
        latitude=latitude,
        longitude=longitude,
        search_radius_km=radius_km,
        sacred_sites=analysis_result.get('sacred_sites'),
        ley_lines=analysis_result.get('ley_lines'),
        energy_vortices=analysis_result.get('energy_vortices'),
        astronomical_alignments=analysis_result.get('astronomical_alignments'),
        overall_assessment=analysis_result.get('overall_assessment')
    )
    
    db.session.add(new_analysis)
    db.session.commit()
    
    return jsonify({
        "status": "success",
        "message": "Análise de linhas ley realizada com sucesso.",
        "id": new_analysis.id,
        "analysis": analysis_result
    }), 200


@advanced_bp.route('/leylines/analyses', methods=['GET'])
def get_leyline_analyses():
    """Retorna todas as análises de linhas ley"""
    analyses = LeyLineAnalysis.query.all()
    
    return jsonify([{
        "id": a.id,
        "latitude": a.latitude,
        "longitude": a.longitude,
        "search_radius_km": a.search_radius_km,
        "analysis_date": a.analysis_date.isoformat(),
        "overall_assessment": a.overall_assessment
    } for a in analyses]), 200


@advanced_bp.route('/leylines/analyses/<int:analysis_id>', methods=['GET'])
def get_leyline_analysis(analysis_id):
    """Retorna uma análise de linhas ley específica"""
    analysis = LeyLineAnalysis.query.get(analysis_id)
    
    if not analysis:
        return jsonify({"status": "error", "message": "Análise não encontrada."}), 404
    
    return jsonify({
        "id": analysis.id,
        "latitude": analysis.latitude,
        "longitude": analysis.longitude,
        "search_radius_km": analysis.search_radius_km,
        "sacred_sites": analysis.sacred_sites,
        "ley_lines": analysis.ley_lines,
        "energy_vortices": analysis.energy_vortices,
        "astronomical_alignments": analysis.astronomical_alignments,
        "overall_assessment": analysis.overall_assessment,
        "analysis_date": analysis.analysis_date.isoformat()
    }), 200


# ===== GEOMETRIA SAGRADA =====

@advanced_bp.route('/sacred_geometry/analyze', methods=['POST'])
def analyze_sacred_geometry_endpoint():
    """
    Endpoint para análise de geometria sagrada
    
    Payload esperado:
    {
        "floor_plan_data": dict,
        "floor_plan_id": int (opcional)
    }
    """
    data = request.get_json()
    
    if not data:
        return jsonify({"status": "error", "message": "Dados JSON não fornecidos."}), 400
    
    floor_plan_data = data.get('floor_plan_data')
    floor_plan_id = data.get('floor_plan_id')
    
    if not floor_plan_data:
        return jsonify({
            "status": "error",
            "message": "floor_plan_data é obrigatório."
        }), 400
    
    # Realizar análise
    analysis_result = analyze_sacred_geometry(floor_plan_data)
    
    # Salvar no banco de dados
    new_analysis = SacredGeometryAnalysis(
        floor_plan_id=floor_plan_id,
        overall_dimensions=analysis_result.get('overall_analysis', {}).get('dimensions'),
        room_analyses=analysis_result.get('room_analyses'),
        sacred_patterns=analysis_result.get('overall_analysis', {}).get('sacred_patterns'),
        fibonacci_analysis=analysis_result.get('fibonacci_analysis'),
        harmony_score=analysis_result.get('overall_assessment', {}).get('sacred_geometry_score'),
        overall_assessment=analysis_result.get('overall_assessment'),
        recommendations=analysis_result.get('recommendations')
    )
    
    db.session.add(new_analysis)
    db.session.commit()
    
    return jsonify({
        "status": "success",
        "message": "Análise de geometria sagrada realizada com sucesso.",
        "id": new_analysis.id,
        "analysis": analysis_result
    }), 200


@advanced_bp.route('/sacred_geometry/analyses', methods=['GET'])
def get_sacred_geometry_analyses():
    """Retorna todas as análises de geometria sagrada"""
    analyses = SacredGeometryAnalysis.query.all()
    
    return jsonify([{
        "id": a.id,
        "harmony_score": a.harmony_score,
        "analysis_date": a.analysis_date.isoformat(),
        "overall_assessment": a.overall_assessment
    } for a in analyses]), 200


@advanced_bp.route('/sacred_geometry/analyses/<int:analysis_id>', methods=['GET'])
def get_sacred_geometry_analysis(analysis_id):
    """Retorna uma análise de geometria sagrada específica"""
    analysis = SacredGeometryAnalysis.query.get(analysis_id)
    
    if not analysis:
        return jsonify({"status": "error", "message": "Análise não encontrada."}), 404
    
    return jsonify({
        "id": analysis.id,
        "overall_dimensions": analysis.overall_dimensions,
        "room_analyses": analysis.room_analyses,
        "sacred_patterns": analysis.sacred_patterns,
        "fibonacci_analysis": analysis.fibonacci_analysis,
        "harmony_score": analysis.harmony_score,
        "overall_assessment": analysis.overall_assessment,
        "recommendations": analysis.recommendations,
        "analysis_date": analysis.analysis_date.isoformat()
    }), 200


# ===== ARQUITETURA SAGRADA =====

@advanced_bp.route('/sacred_architecture/analyze', methods=['POST'])
def analyze_sacred_architecture_endpoint():
    """
    Endpoint para análise de arquitetura sagrada
    
    Payload esperado:
    {
        "building_data": dict,
        "floor_plan_id": int (opcional)
    }
    """
    data = request.get_json()
    
    if not data:
        return jsonify({"status": "error", "message": "Dados JSON não fornecidos."}), 400
    
    building_data = data.get('building_data')
    floor_plan_id = data.get('floor_plan_id')
    
    if not building_data:
        return jsonify({
            "status": "error",
            "message": "building_data é obrigatório."
        }), 400
    
    # Realizar análise
    analysis_result = analyze_sacred_architecture(building_data)
    
    # Salvar no banco de dados
    new_analysis = SacredArchitectureAnalysis(
        floor_plan_id=floor_plan_id,
        room_analyses=analysis_result.get('room_analyses'),
        materials_analysis=analysis_result.get('materials_analysis'),
        sacred_spaces=analysis_result.get('sacred_spaces'),
        astronomical_integration=analysis_result.get('astronomical_integration'),
        circulation_flow=analysis_result.get('circulation_flow'),
        symmetry_balance=analysis_result.get('symmetry_balance'),
        overall_assessment=analysis_result.get('overall_assessment'),
        comprehensive_recommendations=analysis_result.get('comprehensive_recommendations')
    )
    
    db.session.add(new_analysis)
    db.session.commit()
    
    return jsonify({
        "status": "success",
        "message": "Análise de arquitetura sagrada realizada com sucesso.",
        "id": new_analysis.id,
        "analysis": analysis_result
    }), 200


@advanced_bp.route('/sacred_architecture/analyses', methods=['GET'])
def get_sacred_architecture_analyses():
    """Retorna todas as análises de arquitetura sagrada"""
    analyses = SacredArchitectureAnalysis.query.all()
    
    return jsonify([{
        "id": a.id,
        "analysis_date": a.analysis_date.isoformat(),
        "overall_assessment": a.overall_assessment
    } for a in analyses]), 200


@advanced_bp.route('/sacred_architecture/analyses/<int:analysis_id>', methods=['GET'])
def get_sacred_architecture_analysis(analysis_id):
    """Retorna uma análise de arquitetura sagrada específica"""
    analysis = SacredArchitectureAnalysis.query.get(analysis_id)
    
    if not analysis:
        return jsonify({"status": "error", "message": "Análise não encontrada."}), 404
    
    return jsonify({
        "id": analysis.id,
        "room_analyses": analysis.room_analyses,
        "materials_analysis": analysis.materials_analysis,
        "sacred_spaces": analysis.sacred_spaces,
        "astronomical_integration": analysis.astronomical_integration,
        "circulation_flow": analysis.circulation_flow,
        "symmetry_balance": analysis.symmetry_balance,
        "overall_assessment": analysis.overall_assessment,
        "comprehensive_recommendations": analysis.comprehensive_recommendations,
        "analysis_date": analysis.analysis_date.isoformat()
    }), 200


# ===== ANÁLISE INTEGRADA =====

@advanced_bp.route('/integrated/analyze', methods=['POST'])
def create_integrated_analysis():
    """
    Cria uma análise integrada combinando todas as análises
    
    Payload esperado:
    {
        "floor_plan_id": int,
        "bazi_analysis_id": int (opcional),
        "kua_analysis_id": int (opcional),
        "geobiology_analysis_id": int (opcional),
        "emf_analysis_id": int (opcional),
        "leyline_analysis_id": int (opcional),
        "sacred_geometry_analysis_id": int (opcional),
        "sacred_architecture_analysis_id": int (opcional)
    }
    """
    data = request.get_json()
    
    if not data:
        return jsonify({"status": "error", "message": "Dados JSON não fornecidos."}), 400
    
    floor_plan_id = data.get('floor_plan_id')
    
    if not floor_plan_id:
        return jsonify({
            "status": "error",
            "message": "floor_plan_id é obrigatório."
        }), 400
    
    # Criar análise integrada
    new_integrated = IntegratedAnalysis(
        floor_plan_id=floor_plan_id,
        bazi_analysis_id=data.get('bazi_analysis_id'),
        kua_analysis_id=data.get('kua_analysis_id'),
        geobiology_analysis_id=data.get('geobiology_analysis_id'),
        emf_analysis_id=data.get('emf_analysis_id'),
        leyline_analysis_id=data.get('leyline_analysis_id'),
        sacred_geometry_analysis_id=data.get('sacred_geometry_analysis_id'),
        sacred_architecture_analysis_id=data.get('sacred_architecture_analysis_id'),
        overall_health_score=0,  # Será calculado
        priority_recommendations=[],
        implementation_plan={},
        risk_assessment={}
    )
    
    # Calcular score geral e recomendações (simplificado)
    # Em produção, isso seria mais elaborado
    new_integrated.overall_health_score = 75.0
    new_integrated.priority_recommendations = [
        "Implementar correções geobiológicas",
        "Reduzir exposição a EMF",
        "Alinhar com linhas ley identificadas",
        "Aplicar proporções de geometria sagrada",
        "Integrar princípios de arquitetura sagrada"
    ]
    
    db.session.add(new_integrated)
    db.session.commit()
    
    return jsonify({
        "status": "success",
        "message": "Análise integrada criada com sucesso.",
        "id": new_integrated.id,
        "overall_health_score": new_integrated.overall_health_score
    }), 200


@advanced_bp.route('/integrated/analyses', methods=['GET'])
def get_integrated_analyses():
    """Retorna todas as análises integradas"""
    analyses = IntegratedAnalysis.query.all()
    
    return jsonify([{
        "id": a.id,
        "floor_plan_id": a.floor_plan_id,
        "overall_health_score": a.overall_health_score,
        "analysis_date": a.analysis_date.isoformat()
    } for a in analyses]), 200


@advanced_bp.route('/integrated/analyses/<int:analysis_id>', methods=['GET'])
def get_integrated_analysis(analysis_id):
    """Retorna uma análise integrada específica"""
    analysis = IntegratedAnalysis.query.get(analysis_id)
    
    if not analysis:
        return jsonify({"status": "error", "message": "Análise não encontrada."}), 404
    
    return jsonify({
        "id": analysis.id,
        "floor_plan_id": analysis.floor_plan_id,
        "bazi_analysis_id": analysis.bazi_analysis_id,
        "kua_analysis_id": analysis.kua_analysis_id,
        "geobiology_analysis_id": analysis.geobiology_analysis_id,
        "emf_analysis_id": analysis.emf_analysis_id,
        "leyline_analysis_id": analysis.leyline_analysis_id,
        "sacred_geometry_analysis_id": analysis.sacred_geometry_analysis_id,
        "sacred_architecture_analysis_id": analysis.sacred_architecture_analysis_id,
        "overall_health_score": analysis.overall_health_score,
        "priority_recommendations": analysis.priority_recommendations,
        "implementation_plan": analysis.implementation_plan,
        "risk_assessment": analysis.risk_assessment,
        "analysis_date": analysis.analysis_date.isoformat()
    }), 200


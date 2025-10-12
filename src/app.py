from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from spatial_analysis import process_floor_plan
from energetic_analysis import get_geographical_data, simulate_chi_flow, identify_architectural_poisons, get_material_database_entry
from occupant_profiles import calculate_bazi, classify_function_energy, relate_profile_to_area
from models import db, FloorPlan, EnergeticAnalysis, OccupantProfile, BaZiAnalysis, KuaAnalysis, HouseCompatibilityAnalysis, CompleteAnalysis # Importar db e os modelos
from report_generator import generate_analysis_report # Importar o gerador de relatórios
from bazi_calculator import calculate_bazi_for_person # Importar novo módulo BaZi
from kua_calculator import calculate_kua_for_person # Importar novo módulo Kua
from advanced_endpoints import advanced_bp # Importar Blueprint de endpoints avançados
import os
import datetime
import json
from io import BytesIO # Para lidar com o PDF em memória
from sqlalchemy import func # Para funções de agregação

app = Flask(__name__)
CORS(app)  # Habilitar CORS para todas as rotas

# Configuração do banco de dados SQLite
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///arca.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app) # Inicializar o SQLAlchemy com o app Flask

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Criar tabelas do banco de dados se não existirem
with app.app_context():
    db.create_all()

# Registrar Blueprint de endpoints avançados
app.register_blueprint(advanced_bp)

@app.route('/')
def index():
    return "Bem-vindo à API do ARCA!"

@app.route('/upload_floor_plan', methods=['POST'])
def upload_floor_plan():
    if 'file' not in request.files:
        return jsonify({"status": "error", "message": "Nenhum arquivo enviado."}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"status": "error", "message": "Nenhum arquivo selecionado."}), 400

    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        
        # Processar a planta baixa
        analysis_result = process_floor_plan(filepath)
        os.remove(filepath) # Remover o arquivo após o processamento

        # Salvar no banco de dados
        new_floor_plan = FloorPlan(
            filename=file.filename,
            analysis_results=analysis_result # Salvar o resultado completo da análise
        )
        db.session.add(new_floor_plan)
        db.session.commit()

        return jsonify({"status": "success", "message": "Planta baixa processada e salva com sucesso.", "id": new_floor_plan.id, "analysis": analysis_result}), 200

@app.route('/analyze_energetics', methods=['POST'])
def analyze_energetics():
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "Dados JSON não fornecidos."}), 400

    latitude = data.get('latitude')
    longitude = data.get('longitude')
    floor_plan_id = data.get('floor_plan_id') # Opcional: associar a uma planta baixa existente
    floor_plan_data = data.get('floor_plan_data', {}) # Dados simulados da planta baixa

    if not latitude or not longitude:
        return jsonify({"status": "error", "message": "Latitude e Longitude são obrigatórias."}), 400

    current_date = datetime.date.today()
    geo_data = get_geographical_data(latitude, longitude, current_date)
    chi_flow = simulate_chi_flow(floor_plan_data)
    architectural_poisons = identify_architectural_poisons(floor_plan_data)

    material_info = get_material_database_entry("wood")

    # Salvar no banco de dados
    new_energetic_analysis = EnergeticAnalysis(
        floor_plan_id=floor_plan_id,
        latitude=latitude,
        longitude=longitude,
        magnetic_field_data=geo_data.get('data', {}).get('magnetic_field'),
        cem_proximity=geo_data.get('data', {}).get('cem_proximity'),
        geological_anomalies=geo_data.get('data', {}).get('geological_anomalies'),
        nearby_water_veins=geo_data.get('data', {}).get('nearby_water_veins'),
        chi_flow_assessment=chi_flow.get('assessment'),
        architectural_poisons=architectural_poisons.get('poisons')
    )
    db.session.add(new_energetic_analysis)
    db.session.commit()

    return jsonify({
        "status": "success",
        "message": "Análise energética realizada e salva com sucesso.",
        "id": new_energetic_analysis.id,
        "geographical_analysis": geo_data,
        "chi_flow_analysis": chi_flow,
        "architectural_poisons": architectural_poisons,
        "sample_material_info": material_info
    }), 200

@app.route('/register_occupant', methods=['POST'])
def register_occupant():
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "Dados JSON não fornecidos."}), 400

    occupant_type = data.get('type')
    name = data.get('name')

    if not occupant_type or not name:
        return jsonify({"status": "error", "message": "Tipo de ocupante e nome são obrigatórios."}), 400

    profile_data = {"name": name, "type": occupant_type}

    if occupant_type == 'owner_family':
        dob = data.get('dob')
        tob = data.get('tob')
        pob = data.get('pob')
        if not dob or not tob or not pob:
            return jsonify({"status": "error", "message": "Data, hora e local de nascimento são obrigatórios para Proprietários/Família."}), 400
        bazi_result = calculate_bazi(name, dob, tob, pob)
        profile_data["bazi_profile"] = bazi_result
    elif occupant_type == 'employee':
        function = data.get('function')
        if not function:
            return jsonify({"status": "error", "message": "Função é obrigatória para Funcionários."}), 400
        function_energy = classify_function_energy(function)
        profile_data["function_energy"] = function_energy
    else:
        return jsonify({"status": "error", "message": "Tipo de ocupante inválido."}), 400

    # Salvar no banco de dados
    new_occupant_profile = OccupantProfile(
        name=name,
        profile_type=occupant_type,
        details=profile_data # Salvar o perfil completo nos detalhes
    )
    db.session.add(new_occupant_profile)
    db.session.commit()

    return jsonify({"status": "success", "message": "Perfil de ocupante registrado e salvo com sucesso.", "id": new_occupant_profile.id, "profile": profile_data}), 200

# --- Novos Endpoints para Listar Dados --- #

@app.route("/floor_plans", methods=["GET"])
def get_floor_plans():
    filename = request.args.get("filename")
    query = FloorPlan.query
    if filename:
        query = query.filter(FloorPlan.filename.like(f"%{filename}%"))
    floor_plans = query.all()
    return jsonify([{
        "id": fp.id,
        "filename": fp.filename,
        "upload_date": fp.upload_date.isoformat(),
        "analysis_results": fp.analysis_results
    } for fp in floor_plans]), 200

@app.route("/energetic_analyses", methods=["GET"])
def get_energetic_analyses():
    latitude = request.args.get("latitude", type=float)
    longitude = request.args.get("longitude", type=float)
    cem_proximity = request.args.get("cem_proximity")
    query = EnergeticAnalysis.query
    if latitude:
        query = query.filter(EnergeticAnalysis.latitude == latitude)
    if longitude:
        query = query.filter(EnergeticAnalysis.longitude == longitude)
    if cem_proximity:
        query = query.filter(EnergeticAnalysis.cem_proximity == cem_proximity)
    analyses = query.all()
    return jsonify([{
        "id": ea.id,
        "floor_plan_id": ea.floor_plan_id,
        "latitude": ea.latitude,
        "longitude": ea.longitude,
        "analysis_date": ea.analysis_date.isoformat(),
        "magnetic_field_data": ea.magnetic_field_data,
        "cem_proximity": ea.cem_proximity,
        "geological_anomalies": ea.geological_anomalies,
        "nearby_water_veins": ea.nearby_water_veins,
        "chi_flow_assessment": ea.chi_flow_assessment,
        "architectural_poisons": ea.architectural_poisons
    } for ea in analyses]), 200

@app.route("/occupant_profiles", methods=["GET"])
def get_occupant_profiles():
    name = request.args.get("name")
    profile_type = request.args.get("profile_type")
    query = OccupantProfile.query
    if name:
        query = query.filter(OccupantProfile.name.like(f"%{name}%"))
    if profile_type:
        query = query.filter(OccupantProfile.profile_type == profile_type)
    profiles = query.all()
    return jsonify([{
        "id": op.id,
        "name": op.name,
        "profile_type": op.profile_type,
        "details": op.details,
        "registration_date": op.registration_date.isoformat()
    } for op in profiles]), 200

@app.route('/generate_report', methods=['POST'])
def generate_report():
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "Dados JSON não fornecidos."}), 400

    floor_plan_id = data.get('floor_plan_id')
    energetic_analysis_id = data.get('energetic_analysis_id')
    occupant_profile_ids = data.get('occupant_profile_ids', [])

    floor_plan = None
    if floor_plan_id:
        floor_plan = FloorPlan.query.get(floor_plan_id)

    energetic_analysis = None
    if energetic_analysis_id:
        energetic_analysis = EnergeticAnalysis.query.get(energetic_analysis_id)

    occupant_profiles = []
    if occupant_profile_ids:
        occupant_profiles = OccupantProfile.query.filter(OccupantProfile.id.in_(occupant_profile_ids)).all()

    if not floor_plan and not energetic_analysis and not occupant_profiles:
        return jsonify({"status": "error", "message": "Nenhum dado válido fornecido para gerar o relatório."}), 400

    pdf_output = generate_analysis_report(floor_plan, energetic_analysis, occupant_profiles)

    return send_file(
        BytesIO(pdf_output),
        mimetype='application/pdf',
        as_attachment=True,
        download_name='relatorio_arca.pdf'
    )

# --- Novos Endpoints para Dashboard Analytics --- #

@app.route('/analytics/floor_plans_by_month', methods=['GET'])
def get_floor_plans_by_month():
    results = db.session.query(
        func.strftime('%Y-%m', FloorPlan.upload_date),
        func.count(FloorPlan.id)
    ).group_by(func.strftime('%Y-%m', FloorPlan.upload_date)).all()

    data = [{'month': r[0], 'count': r[1]} for r in results]
    return jsonify(data), 200

@app.route('/analytics/energetic_analyses_by_cem_proximity', methods=['GET'])
def get_energetic_analyses_by_cem_proximity():
    results = db.session.query(
        EnergeticAnalysis.cem_proximity,
        func.count(EnergeticAnalysis.id)
    ).group_by(EnergeticAnalysis.cem_proximity).all()

    data = [{'cem_proximity': r[0], 'count': r[1]} for r in results]
    return jsonify(data), 200

@app.route('/analytics/occupant_profiles_by_type', methods=['GET'])
def get_occupant_profiles_by_type():
    results = db.session.query(
        OccupantProfile.profile_type,
        func.count(OccupantProfile.id)
    ).group_by(OccupantProfile.profile_type).all()

    data = [{'profile_type': r[0], 'count': r[1]} for r in results]
    return jsonify(data), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)



# --- Novos Endpoints para Busca e Filtros --- #

@app.route('/search/floor_plans', methods=['GET'])
def search_floor_plans():
    # Parâmetros de busca
    filename = request.args.get('filename', '')
    status = request.args.get('status', '')
    date_from = request.args.get('date_from', '')
    date_to = request.args.get('date_to', '')
    
    # Construir query base
    query = FloorPlan.query
    
    # Aplicar filtros
    if filename:
        query = query.filter(FloorPlan.filename.contains(filename))
    
    if status:
        query = query.filter(FloorPlan.analysis_results['status'].astext == status)
    
    if date_from:
        try:
            date_from_obj = datetime.datetime.strptime(date_from, '%Y-%m-%d')
            query = query.filter(FloorPlan.upload_date >= date_from_obj)
        except ValueError:
            pass
    
    if date_to:
        try:
            date_to_obj = datetime.datetime.strptime(date_to, '%Y-%m-%d')
            query = query.filter(FloorPlan.upload_date <= date_to_obj)
        except ValueError:
            pass
    
    # Ordenar por data de upload (mais recente primeiro)
    query = query.order_by(FloorPlan.upload_date.desc())
    
    # Executar query
    floor_plans = query.all()
    
    return jsonify([{
        "id": fp.id,
        "filename": fp.filename,
        "upload_date": fp.upload_date.isoformat(),
        "analysis_results": fp.analysis_results
    } for fp in floor_plans]), 200

@app.route('/search/energetic_analyses', methods=['GET'])
def search_energetic_analyses():
    # Parâmetros de busca
    cem_proximity = request.args.get('cem_proximity', '')
    geological_anomalies = request.args.get('geological_anomalies', '')
    date_from = request.args.get('date_from', '')
    date_to = request.args.get('date_to', '')
    latitude_min = request.args.get('latitude_min', '')
    latitude_max = request.args.get('latitude_max', '')
    longitude_min = request.args.get('longitude_min', '')
    longitude_max = request.args.get('longitude_max', '')
    
    # Construir query base
    query = EnergeticAnalysis.query
    
    # Aplicar filtros
    if cem_proximity:
        query = query.filter(EnergeticAnalysis.cem_proximity == cem_proximity)
    
    if geological_anomalies:
        query = query.filter(EnergeticAnalysis.geological_anomalies == geological_anomalies)
    
    if date_from:
        try:
            date_from_obj = datetime.datetime.strptime(date_from, '%Y-%m-%d')
            query = query.filter(EnergeticAnalysis.analysis_date >= date_from_obj)
        except ValueError:
            pass
    
    if date_to:
        try:
            date_to_obj = datetime.datetime.strptime(date_to, '%Y-%m-%d')
            query = query.filter(EnergeticAnalysis.analysis_date <= date_to_obj)
        except ValueError:
            pass
    
    if latitude_min:
        try:
            lat_min = float(latitude_min)
            query = query.filter(EnergeticAnalysis.latitude >= lat_min)
        except ValueError:
            pass
    
    if latitude_max:
        try:
            lat_max = float(latitude_max)
            query = query.filter(EnergeticAnalysis.latitude <= lat_max)
        except ValueError:
            pass
    
    if longitude_min:
        try:
            lon_min = float(longitude_min)
            query = query.filter(EnergeticAnalysis.longitude >= lon_min)
        except ValueError:
            pass
    
    if longitude_max:
        try:
            lon_max = float(longitude_max)
            query = query.filter(EnergeticAnalysis.longitude <= lon_max)
        except ValueError:
            pass
    
    # Ordenar por data de análise (mais recente primeiro)
    query = query.order_by(EnergeticAnalysis.analysis_date.desc())
    
    # Executar query
    analyses = query.all()
    
    return jsonify([{
        "id": ea.id,
        "latitude": ea.latitude,
        "longitude": ea.longitude,
        "analysis_date": ea.analysis_date.isoformat(),
        "cem_proximity": ea.cem_proximity,
        "geological_anomalies": ea.geological_anomalies,
        "nearby_water_veins": ea.nearby_water_veins,
        "magnetic_field_data": ea.magnetic_field_data,
        "chi_flow_assessment": ea.chi_flow_assessment,
        "architectural_poisons": ea.architectural_poisons
    } for ea in analyses]), 200

@app.route('/search/occupant_profiles', methods=['GET'])
def search_occupant_profiles():
    # Parâmetros de busca
    name = request.args.get('name', '')
    profile_type = request.args.get('profile_type', '')
    date_from = request.args.get('date_from', '')
    date_to = request.args.get('date_to', '')
    bazi_element = request.args.get('bazi_element', '')
    function_energy = request.args.get('function_energy', '')
    
    # Construir query base
    query = OccupantProfile.query
    
    # Aplicar filtros
    if name:
        query = query.filter(OccupantProfile.name.contains(name))
    
    if profile_type:
        query = query.filter(OccupantProfile.profile_type == profile_type)
    
    if date_from:
        try:
            date_from_obj = datetime.datetime.strptime(date_from, '%Y-%m-%d')
            query = query.filter(OccupantProfile.registration_date >= date_from_obj)
        except ValueError:
            pass
    
    if date_to:
        try:
            date_to_obj = datetime.datetime.strptime(date_to, '%Y-%m-%d')
            query = query.filter(OccupantProfile.registration_date <= date_to_obj)
        except ValueError:
            pass
    
    if bazi_element and profile_type == 'owner_family':
        query = query.filter(OccupantProfile.details['bazi_profile']['profile']['master_element'].astext == bazi_element)
    
    if function_energy and profile_type == 'employee':
        query = query.filter(OccupantProfile.details['function_energy'].astext == function_energy)
    
    # Ordenar por data de registro (mais recente primeiro)
    query = query.order_by(OccupantProfile.registration_date.desc())
    
    # Executar query
    profiles = query.all()
    
    return jsonify([{
        "id": op.id,
        "name": op.name,
        "profile_type": op.profile_type,
        "details": op.details,
        "registration_date": op.registration_date.isoformat()
    } for op in profiles]), 200



# --- Novos Endpoints para Exportação de Dados --- #

@app.route('/export/floor_plans', methods=['GET'])
def export_floor_plans():
    format_type = request.args.get('format', 'json')  # json ou csv
    
    # Buscar todas as plantas baixas
    floor_plans = FloorPlan.query.all()
    
    if format_type == 'csv':
        import csv
        from io import StringIO
        
        output = StringIO()
        writer = csv.writer(output)
        
        # Cabeçalho CSV
        writer.writerow(['ID', 'Nome do Arquivo', 'Data de Upload', 'Status', 'Detalhes'])
        
        # Dados
        for fp in floor_plans:
            writer.writerow([
                fp.id,
                fp.filename,
                fp.upload_date.strftime('%Y-%m-%d %H:%M:%S'),
                fp.analysis_results.get('status', 'N/A'),
                fp.analysis_results.get('message', 'N/A')
            ])
        
        output.seek(0)
        return send_file(
            BytesIO(output.getvalue().encode('utf-8')),
            mimetype='text/csv',
            as_attachment=True,
            download_name='plantas_baixas.csv'
        )
    
    else:  # JSON
        data = [{
            "id": fp.id,
            "filename": fp.filename,
            "upload_date": fp.upload_date.isoformat(),
            "analysis_results": fp.analysis_results
        } for fp in floor_plans]
        
        return send_file(
            BytesIO(json.dumps(data, indent=2, ensure_ascii=False).encode('utf-8')),
            mimetype='application/json',
            as_attachment=True,
            download_name='plantas_baixas.json'
        )

@app.route('/export/energetic_analyses', methods=['GET'])
def export_energetic_analyses():
    format_type = request.args.get('format', 'json')  # json ou csv
    
    # Buscar todas as análises energéticas
    analyses = EnergeticAnalysis.query.all()
    
    if format_type == 'csv':
        import csv
        from io import StringIO
        
        output = StringIO()
        writer = csv.writer(output)
        
        # Cabeçalho CSV
        writer.writerow([
            'ID', 'Latitude', 'Longitude', 'Data de Análise', 'Proximidade CEM',
            'Anomalias Geológicas', 'Veios de Água', 'Declinação Magnética',
            'Inclinação Magnética', 'Intensidade Total'
        ])
        
        # Dados
        for ea in analyses:
            mf_data = ea.magnetic_field_data or {}
            writer.writerow([
                ea.id,
                ea.latitude,
                ea.longitude,
                ea.analysis_date.strftime('%Y-%m-%d %H:%M:%S'),
                ea.cem_proximity,
                ea.geological_anomalies,
                'Sim' if ea.nearby_water_veins else 'Não',
                mf_data.get('declination', 'N/A'),
                mf_data.get('inclination', 'N/A'),
                mf_data.get('total_intensity', 'N/A')
            ])
        
        output.seek(0)
        return send_file(
            BytesIO(output.getvalue().encode('utf-8')),
            mimetype='text/csv',
            as_attachment=True,
            download_name='analises_energeticas.csv'
        )
    
    else:  # JSON
        data = [{
            "id": ea.id,
            "latitude": ea.latitude,
            "longitude": ea.longitude,
            "analysis_date": ea.analysis_date.isoformat(),
            "cem_proximity": ea.cem_proximity,
            "geological_anomalies": ea.geological_anomalies,
            "nearby_water_veins": ea.nearby_water_veins,
            "magnetic_field_data": ea.magnetic_field_data,
            "chi_flow_assessment": ea.chi_flow_assessment,
            "architectural_poisons": ea.architectural_poisons
        } for ea in analyses]
        
        return send_file(
            BytesIO(json.dumps(data, indent=2, ensure_ascii=False).encode('utf-8')),
            mimetype='application/json',
            as_attachment=True,
            download_name='analises_energeticas.json'
        )

@app.route('/export/occupant_profiles', methods=['GET'])
def export_occupant_profiles():
    format_type = request.args.get('format', 'json')  # json ou csv
    
    # Buscar todos os perfis de ocupantes
    profiles = OccupantProfile.query.all()
    
    if format_type == 'csv':
        import csv
        from io import StringIO
        
        output = StringIO()
        writer = csv.writer(output)
        
        # Cabeçalho CSV
        writer.writerow([
            'ID', 'Nome', 'Tipo de Perfil', 'Data de Registro',
            'Elemento BaZi', 'Energia da Função', 'Detalhes'
        ])
        
        # Dados
        for op in profiles:
            bazi_element = 'N/A'
            function_energy = 'N/A'
            
            if op.details:
                if op.profile_type == 'owner_family' and op.details.get('bazi_profile'):
                    bazi_element = op.details.get('bazi_profile', {}).get('profile', {}).get('master_element', 'N/A')
                elif op.profile_type == 'employee' and op.details.get('function_energy'):
                    function_energy = op.details.get('function_energy', 'N/A')
            
            writer.writerow([
                op.id,
                op.name,
                op.profile_type,
                op.registration_date.strftime('%Y-%m-%d %H:%M:%S'),
                bazi_element,
                function_energy,
                json.dumps(op.details, ensure_ascii=False) if op.details else 'N/A'
            ])
        
        output.seek(0)
        return send_file(
            BytesIO(output.getvalue().encode('utf-8')),
            mimetype='text/csv',
            as_attachment=True,
            download_name='perfis_ocupantes.csv'
        )
    
    else:  # JSON
        data = [{
            "id": op.id,
            "name": op.name,
            "profile_type": op.profile_type,
            "details": op.details,
            "registration_date": op.registration_date.isoformat()
        } for op in profiles]
        
        return send_file(
            BytesIO(json.dumps(data, indent=2, ensure_ascii=False).encode('utf-8')),
            mimetype='application/json',
            as_attachment=True,
            download_name='perfis_ocupantes.json'
        )

@app.route('/export/full_backup', methods=['GET'])
def export_full_backup():
    """Exporta um backup completo de todos os dados em formato JSON"""
    
    # Buscar todos os dados
    floor_plans = FloorPlan.query.all()
    energetic_analyses = EnergeticAnalysis.query.all()
    occupant_profiles = OccupantProfile.query.all()
    
    # Estruturar dados para backup
    backup_data = {
        "export_date": datetime.datetime.now().isoformat(),
        "version": "1.0",
        "floor_plans": [{
            "id": fp.id,
            "filename": fp.filename,
            "upload_date": fp.upload_date.isoformat(),
            "analysis_results": fp.analysis_results
        } for fp in floor_plans],
        "energetic_analyses": [{
            "id": ea.id,
            "latitude": ea.latitude,
            "longitude": ea.longitude,
            "analysis_date": ea.analysis_date.isoformat(),
            "cem_proximity": ea.cem_proximity,
            "geological_anomalies": ea.geological_anomalies,
            "nearby_water_veins": ea.nearby_water_veins,
            "magnetic_field_data": ea.magnetic_field_data,
            "chi_flow_assessment": ea.chi_flow_assessment,
            "architectural_poisons": ea.architectural_poisons
        } for ea in energetic_analyses],
        "occupant_profiles": [{
            "id": op.id,
            "name": op.name,
            "profile_type": op.profile_type,
            "details": op.details,
            "registration_date": op.registration_date.isoformat()
        } for op in occupant_profiles]
    }
    
    return send_file(
        BytesIO(json.dumps(backup_data, indent=2, ensure_ascii=False).encode('utf-8')),
        mimetype='application/json',
        as_attachment=True,
        download_name=f'arca_backup_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
    )


# ==================== NOVOS ENDPOINTS BAZI E KUA ====================

@app.route('/bazi/calculate', methods=['POST'])
def calculate_bazi_endpoint():
    """Calcula BaZi (Quatro Pilares do Destino) para uma pessoa"""
    
    try:
        data = request.get_json()
        
        # Validar dados obrigatórios
        required_fields = ['birth_datetime']
        for field in required_fields:
            if field not in data:
                return jsonify({"status": "error", "message": f"Campo obrigatório: {field}"}), 400
        
        # Converter string para datetime
        birth_datetime = datetime.datetime.fromisoformat(data['birth_datetime'].replace('Z', '+00:00'))
        timezone_offset = data.get('timezone_offset', -3)  # Padrão Brasil
        occupant_profile_id = data.get('occupant_profile_id')  # Opcional
        
        # Calcular BaZi
        bazi_result = calculate_bazi_for_person(birth_datetime, timezone_offset)
        
        # Salvar no banco de dados
        new_bazi_analysis = BaZiAnalysis(
            occupant_profile_id=occupant_profile_id,
            birth_datetime=birth_datetime,
            timezone_offset=timezone_offset,
            year_pillar=bazi_result['year_pillar'],
            month_pillar=bazi_result['month_pillar'],
            day_pillar=bazi_result['day_pillar'],
            hour_pillar=bazi_result['hour_pillar'],
            day_master=bazi_result['day_master'],
            useful_god=bazi_result['useful_god'],
            recommendations=bazi_result['recommendations']
        )
        db.session.add(new_bazi_analysis)
        db.session.commit()
        
        # Adicionar ID da análise ao resultado
        bazi_result['analysis_id'] = new_bazi_analysis.id
        
        return jsonify({
            "status": "success",
            "data": bazi_result,
            "message": "Cálculo BaZi realizado e salvo com sucesso"
        })
        
    except Exception as e:
        return jsonify({"status": "error", "message": f"Erro no cálculo BaZi: {str(e)}"}), 500

@app.route('/kua/calculate', methods=['POST'])
def calculate_kua_endpoint():
    """Calcula Número Kua e análise Ba Zhai para uma pessoa"""
    
    try:
        data = request.get_json()
        
        # Validar dados obrigatórios
        required_fields = ['birth_year', 'gender']
        for field in required_fields:
            if field not in data:
                return jsonify({"status": "error", "message": f"Campo obrigatório: {field}"}), 400
        
        birth_year = int(data['birth_year'])
        gender = data['gender'].lower()
        occupant_profile_id = data.get('occupant_profile_id')  # Opcional
        
        if gender not in ['male', 'female']:
            return jsonify({"status": "error", "message": "Gênero deve ser 'male' ou 'female'"}), 400
        
        # Calcular Kua
        kua_result = calculate_kua_for_person(birth_year, gender)
        
        # Salvar no banco de dados
        new_kua_analysis = KuaAnalysis(
            occupant_profile_id=occupant_profile_id,
            birth_year=birth_year,
            gender=gender,
            kua_number=kua_result['kua_number'],
            group=kua_result['characteristics']['group'],
            element=kua_result['characteristics']['element'],
            personality=kua_result['characteristics']['personality'],
            favorable_directions=kua_result['favorable_directions'],
            unfavorable_directions=kua_result['unfavorable_directions'],
            recommendations=kua_result['feng_shui_recommendations']
        )
        db.session.add(new_kua_analysis)
        db.session.commit()
        
        # Adicionar ID da análise ao resultado
        kua_result['analysis_id'] = new_kua_analysis.id
        
        return jsonify({
            "status": "success",
            "data": kua_result,
            "message": "Cálculo Kua realizado e salvo com sucesso"
        })
        
    except Exception as e:
        return jsonify({"status": "error", "message": f"Erro no cálculo Kua: {str(e)}"}), 500

@app.route('/bazi_kua/complete_analysis', methods=['POST'])
def complete_bazi_kua_analysis():
    """Análise completa combinando BaZi e Kua para uma pessoa"""
    
    try:
        data = request.get_json()
        
        # Validar dados obrigatórios
        required_fields = ['birth_datetime', 'birth_year', 'gender']
        for field in required_fields:
            if field not in data:
                return jsonify({"status": "error", "message": f"Campo obrigatório: {field}"}), 400
        
        # Extrair dados
        birth_datetime = datetime.datetime.fromisoformat(data['birth_datetime'].replace('Z', '+00:00'))
        birth_year = int(data['birth_year'])
        gender = data['gender'].lower()
        timezone_offset = data.get('timezone_offset', -3)
        occupant_profile_id = data.get('occupant_profile_id')
        
        # Calcular BaZi e Kua
        bazi_result = calculate_bazi_for_person(birth_datetime, timezone_offset)
        kua_result = calculate_kua_for_person(birth_year, gender)
        
        # Salvar análises individuais
        new_bazi_analysis = BaZiAnalysis(
            occupant_profile_id=occupant_profile_id,
            birth_datetime=birth_datetime,
            timezone_offset=timezone_offset,
            year_pillar=bazi_result['year_pillar'],
            month_pillar=bazi_result['month_pillar'],
            day_pillar=bazi_result['day_pillar'],
            hour_pillar=bazi_result['hour_pillar'],
            day_master=bazi_result['day_master'],
            useful_god=bazi_result['useful_god'],
            recommendations=bazi_result['recommendations']
        )
        
        new_kua_analysis = KuaAnalysis(
            occupant_profile_id=occupant_profile_id,
            birth_year=birth_year,
            gender=gender,
            kua_number=kua_result['kua_number'],
            group=kua_result['characteristics']['group'],
            element=kua_result['characteristics']['element'],
            personality=kua_result['characteristics']['personality'],
            favorable_directions=kua_result['favorable_directions'],
            unfavorable_directions=kua_result['unfavorable_directions'],
            recommendations=kua_result['feng_shui_recommendations']
        )
        
        db.session.add(new_bazi_analysis)
        db.session.add(new_kua_analysis)
        db.session.commit()
        
        # Análise integrada
        integrated_analysis = integrate_bazi_kua_analysis(bazi_result, kua_result)
        
        # Salvar análise completa
        new_complete_analysis = CompleteAnalysis(
            bazi_analysis_id=new_bazi_analysis.id,
            kua_analysis_id=new_kua_analysis.id,
            element_harmony=integrated_analysis['element_harmony'],
            unified_recommendations=integrated_analysis,
            career_alignment=integrated_analysis['career_alignment'],
            relationship_guidance=integrated_analysis['relationship_guidance'],
            feng_shui_priority=integrated_analysis['feng_shui_priority']
        )
        db.session.add(new_complete_analysis)
        db.session.commit()
        
        return jsonify({
            "status": "success",
            "data": {
                "bazi": bazi_result,
                "kua": kua_result,
                "integrated_analysis": integrated_analysis,
                "analysis_ids": {
                    "bazi_id": new_bazi_analysis.id,
                    "kua_id": new_kua_analysis.id,
                    "complete_id": new_complete_analysis.id
                }
            },
            "message": "Análise completa BaZi + Kua realizada e salva com sucesso"
        })
        
    except Exception as e:
        return jsonify({"status": "error", "message": f"Erro na análise completa: {str(e)}"}), 500

@app.route('/feng_shui/house_analysis', methods=['POST'])
def feng_shui_house_analysis():
    """Análise Feng Shui de casa baseada em Kua do morador"""
    
    try:
        data = request.get_json()
        
        # Validar dados obrigatórios
        required_fields = ['house_facing_direction', 'birth_year', 'gender']
        for field in required_fields:
            if field not in data:
                return jsonify({"status": "error", "message": f"Campo obrigatório: {field}"}), 400
        
        house_facing = data['house_facing_direction']
        birth_year = int(data['birth_year'])
        gender = data['gender'].lower()
        kua_analysis_id = data.get('kua_analysis_id')  # Opcional: usar análise Kua existente
        
        # Se não foi fornecido ID de análise Kua existente, calcular novo
        if not kua_analysis_id:
            kua_result = calculate_kua_for_person(birth_year, gender)
            
            # Salvar análise Kua
            new_kua_analysis = KuaAnalysis(
                birth_year=birth_year,
                gender=gender,
                kua_number=kua_result['kua_number'],
                group=kua_result['characteristics']['group'],
                element=kua_result['characteristics']['element'],
                personality=kua_result['characteristics']['personality'],
                favorable_directions=kua_result['favorable_directions'],
                unfavorable_directions=kua_result['unfavorable_directions'],
                recommendations=kua_result['feng_shui_recommendations']
            )
            db.session.add(new_kua_analysis)
            db.session.commit()
            kua_analysis_id = new_kua_analysis.id
            kua_number = kua_result['kua_number']
        else:
            # Buscar análise Kua existente
            existing_kua = KuaAnalysis.query.get(kua_analysis_id)
            if not existing_kua:
                return jsonify({"status": "error", "message": "Análise Kua não encontrada"}), 404
            kua_number = existing_kua.kua_number
        
        # Analisar compatibilidade da casa
        from kua_calculator import KuaCalculator
        calculator = KuaCalculator()
        house_compatibility = calculator.analyze_house_compatibility(house_facing, kua_number)
        
        # Salvar análise de compatibilidade
        new_house_analysis = HouseCompatibilityAnalysis(
            kua_analysis_id=kua_analysis_id,
            house_facing_direction=house_facing,
            compatibility_level=house_compatibility['compatibility_level'],
            compatibility_score=house_compatibility['compatibility_score'],
            direction_type=house_compatibility['analysis']['direction_type'],
            benefits=house_compatibility['analysis']['benefits'],
            recommendations=house_compatibility['analysis']['recommendations'],
            feng_shui_advice=house_compatibility['feng_shui_advice']
        )
        db.session.add(new_house_analysis)
        db.session.commit()
        
        # Adicionar ID da análise ao resultado
        house_compatibility['analysis_id'] = new_house_analysis.id
        
        return jsonify({
            "status": "success",
            "data": house_compatibility,
            "message": "Análise de compatibilidade da casa realizada e salva com sucesso"
        })
        
    except Exception as e:
        return jsonify({"status": "error", "message": f"Erro na análise da casa: {str(e)}"}), 500

def integrate_bazi_kua_analysis(bazi_result: dict, kua_result: dict) -> dict:
    """Integra análises BaZi e Kua para recomendações unificadas"""
    
    # Extrair elementos principais
    day_master_element = bazi_result['day_master']['element']
    useful_god_element = bazi_result['useful_god']['element']
    kua_element = kua_result['characteristics']['element']
    kua_group = kua_result['characteristics']['group']
    
    # Comparar elementos BaZi vs Kua
    element_harmony = "harmonious" if day_master_element == kua_element else "different"
    
    # Integrar recomendações de cores
    bazi_colors = bazi_result['recommendations']['favorable_colors']
    kua_colors = kua_result['feng_shui_recommendations'].get('colors', [])
    common_colors = list(set(bazi_colors) & set(kua_colors))
    
    # Integrar direções
    bazi_directions = bazi_result['recommendations']['favorable_directions']
    kua_directions = list(kua_result['favorable_directions'].values())
    
    # Recomendações unificadas
    unified_recommendations = {
        "priority_element": useful_god_element,
        "secondary_element": kua_element,
        "element_harmony": element_harmony,
        "unified_colors": common_colors if common_colors else bazi_colors,
        "primary_directions": kua_directions,
        "career_alignment": analyze_career_alignment(bazi_result, kua_result),
        "relationship_guidance": combine_relationship_advice(bazi_result, kua_result),
        "feng_shui_priority": determine_feng_shui_priority(bazi_result, kua_result)
    }
    
    return unified_recommendations

def analyze_career_alignment(bazi_result: dict, kua_result: dict) -> dict:
    """Analisa alinhamento de carreira entre BaZi e Kua"""
    
    bazi_careers = bazi_result['recommendations']['career_guidance']
    kua_personality = kua_result['characteristics']['personality']
    kua_strengths = kua_result['characteristics']['strengths']
    
    return {
        "bazi_suggestions": bazi_careers,
        "kua_personality": kua_personality,
        "kua_strengths": kua_strengths,
        "alignment_score": 85,  # Simplificado - em implementação real seria calculado
        "recommended_fields": bazi_careers[:3]  # Top 3 recomendações
    }

def combine_relationship_advice(bazi_result: dict, kua_result: dict) -> dict:
    """Combina conselhos de relacionamento de BaZi e Kua"""
    
    day_master_element = bazi_result['day_master']['element']
    kua_advice = kua_result['compatibility']['relationship_advice']
    
    return {
        "bazi_element_influence": f"Como pessoa {day_master_element}, você tende a ser {get_element_relationship_trait(day_master_element)}",
        "kua_relationship_pattern": kua_advice,
        "combined_advice": generate_combined_relationship_advice(day_master_element, kua_advice)
    }

def get_element_relationship_trait(element: str) -> str:
    """Retorna traços de relacionamento baseados no elemento"""
    
    traits = {
        "Wood": "flexível e em crescimento, mas pode ser indecisa",
        "Fire": "apaixonada e energética, mas pode ser impaciente",
        "Earth": "estável e confiável, mas pode ser possessiva",
        "Metal": "organizada e leal, mas pode ser rígida",
        "Water": "adaptável e intuitiva, mas pode ser evasiva"
    }
    
    return traits.get(element, "equilibrada")

def generate_combined_relationship_advice(day_master_element: str, kua_advice: dict) -> str:
    """Gera conselho combinado de relacionamento"""
    
    return f"Baseado em sua natureza {day_master_element} e características Kua, {kua_advice.get('relationship_tips', 'mantenha equilíbrio em seus relacionamentos')}."

def determine_feng_shui_priority(bazi_result: dict, kua_result: dict) -> dict:
    """Determina prioridades de Feng Shui baseadas em ambas análises"""
    
    useful_god = bazi_result['useful_god']['element']
    kua_directions = kua_result['favorable_directions']
    
    return {
        "primary_focus": f"Fortalecer elemento {useful_god}",
        "key_direction": kua_directions['sheng_qi'],
        "secondary_direction": kua_directions['tian_yi'],
        "avoid_direction": list(kua_result['unfavorable_directions'].values())[0],
        "implementation_order": [
            f"1. Posicionar cama/mesa na direção {kua_directions['sheng_qi']}",
            f"2. Incorporar elemento {useful_god} no ambiente",
            f"3. Evitar atividades importantes na direção {list(kua_result['unfavorable_directions'].values())[0]}",
            "4. Aplicar cores e materiais recomendados"
        ]
    }

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5007)


# ==================== ENDPOINTS DE HISTÓRICO E BUSCA ====================

@app.route('/bazi/history', methods=['GET'])
def get_bazi_history():
    """Retorna histórico de análises BaZi"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        analyses = BaZiAnalysis.query.order_by(BaZiAnalysis.analysis_date.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        result = []
        for analysis in analyses.items:
            result.append({
                'id': analysis.id,
                'birth_datetime': analysis.birth_datetime.isoformat(),
                'timezone_offset': analysis.timezone_offset,
                'day_master': analysis.day_master,
                'useful_god': analysis.useful_god,
                'analysis_date': analysis.analysis_date.isoformat(),
                'occupant_profile_id': analysis.occupant_profile_id
            })
        
        return jsonify({
            'status': 'success',
            'data': result,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': analyses.total,
                'pages': analyses.pages
            }
        })
        
    except Exception as e:
        return jsonify({"status": "error", "message": f"Erro ao buscar histórico BaZi: {str(e)}"}), 500

@app.route('/kua/history', methods=['GET'])
def get_kua_history():
    """Retorna histórico de análises Kua"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        analyses = KuaAnalysis.query.order_by(KuaAnalysis.analysis_date.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        result = []
        for analysis in analyses.items:
            result.append({
                'id': analysis.id,
                'birth_year': analysis.birth_year,
                'gender': analysis.gender,
                'kua_number': analysis.kua_number,
                'group': analysis.group,
                'element': analysis.element,
                'personality': analysis.personality,
                'analysis_date': analysis.analysis_date.isoformat(),
                'occupant_profile_id': analysis.occupant_profile_id
            })
        
        return jsonify({
            'status': 'success',
            'data': result,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': analyses.total,
                'pages': analyses.pages
            }
        })
        
    except Exception as e:
        return jsonify({"status": "error", "message": f"Erro ao buscar histórico Kua: {str(e)}"}), 500

@app.route('/house_compatibility/history', methods=['GET'])
def get_house_compatibility_history():
    """Retorna histórico de análises de compatibilidade de casa"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        analyses = HouseCompatibilityAnalysis.query.order_by(HouseCompatibilityAnalysis.analysis_date.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        result = []
        for analysis in analyses.items:
            result.append({
                'id': analysis.id,
                'house_facing_direction': analysis.house_facing_direction,
                'compatibility_level': analysis.compatibility_level,
                'compatibility_score': analysis.compatibility_score,
                'direction_type': analysis.direction_type,
                'analysis_date': analysis.analysis_date.isoformat(),
                'kua_analysis_id': analysis.kua_analysis_id
            })
        
        return jsonify({
            'status': 'success',
            'data': result,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': analyses.total,
                'pages': analyses.pages
            }
        })
        
    except Exception as e:
        return jsonify({"status": "error", "message": f"Erro ao buscar histórico de compatibilidade: {str(e)}"}), 500

@app.route('/complete_analysis/history', methods=['GET'])
def get_complete_analysis_history():
    """Retorna histórico de análises completas BaZi + Kua"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        analyses = CompleteAnalysis.query.order_by(CompleteAnalysis.analysis_date.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        result = []
        for analysis in analyses.items:
            result.append({
                'id': analysis.id,
                'element_harmony': analysis.element_harmony,
                'analysis_date': analysis.analysis_date.isoformat(),
                'bazi_analysis_id': analysis.bazi_analysis_id,
                'kua_analysis_id': analysis.kua_analysis_id,
                'unified_recommendations': analysis.unified_recommendations
            })
        
        return jsonify({
            'status': 'success',
            'data': result,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': analyses.total,
                'pages': analyses.pages
            }
        })
        
    except Exception as e:
        return jsonify({"status": "error", "message": f"Erro ao buscar histórico de análises completas: {str(e)}"}), 500

@app.route('/bazi/<int:analysis_id>', methods=['GET'])
def get_bazi_analysis(analysis_id):
    """Retorna análise BaZi específica por ID"""
    try:
        analysis = BaZiAnalysis.query.get_or_404(analysis_id)
        
        result = {
            'id': analysis.id,
            'birth_datetime': analysis.birth_datetime.isoformat(),
            'timezone_offset': analysis.timezone_offset,
            'year_pillar': analysis.year_pillar,
            'month_pillar': analysis.month_pillar,
            'day_pillar': analysis.day_pillar,
            'hour_pillar': analysis.hour_pillar,
            'day_master': analysis.day_master,
            'useful_god': analysis.useful_god,
            'recommendations': analysis.recommendations,
            'analysis_date': analysis.analysis_date.isoformat(),
            'occupant_profile_id': analysis.occupant_profile_id
        }
        
        return jsonify({
            'status': 'success',
            'data': result
        })
        
    except Exception as e:
        return jsonify({"status": "error", "message": f"Erro ao buscar análise BaZi: {str(e)}"}), 500

@app.route('/kua/<int:analysis_id>', methods=['GET'])
def get_kua_analysis(analysis_id):
    """Retorna análise Kua específica por ID"""
    try:
        analysis = KuaAnalysis.query.get_or_404(analysis_id)
        
        result = {
            'id': analysis.id,
            'birth_year': analysis.birth_year,
            'gender': analysis.gender,
            'kua_number': analysis.kua_number,
            'group': analysis.group,
            'element': analysis.element,
            'personality': analysis.personality,
            'favorable_directions': analysis.favorable_directions,
            'unfavorable_directions': analysis.unfavorable_directions,
            'recommendations': analysis.recommendations,
            'analysis_date': analysis.analysis_date.isoformat(),
            'occupant_profile_id': analysis.occupant_profile_id
        }
        
        return jsonify({
            'status': 'success',
            'data': result
        })
        
    except Exception as e:
        return jsonify({"status": "error", "message": f"Erro ao buscar análise Kua: {str(e)}"}), 500

# ==================== ENDPOINTS DE ANALYTICS FENG SHUI ====================

@app.route('/analytics/bazi_elements', methods=['GET'])
def get_bazi_elements_analytics():
    """Analytics de distribuição de elementos Day Master em análises BaZi"""
    try:
        # Contar análises por elemento Day Master
        from sqlalchemy import text
        
        query = text("""
            SELECT 
                JSON_EXTRACT(day_master, '$.element') as element,
                COUNT(*) as count
            FROM ba_zi_analysis 
            WHERE day_master IS NOT NULL
            GROUP BY JSON_EXTRACT(day_master, '$.element')
            ORDER BY count DESC
        """)
        
        result = db.session.execute(query).fetchall()
        
        analytics_data = []
        for row in result:
            analytics_data.append({
                'element': row[0],
                'count': row[1]
            })
        
        return jsonify({
            'status': 'success',
            'data': analytics_data
        })
        
    except Exception as e:
        return jsonify({"status": "error", "message": f"Erro ao gerar analytics BaZi: {str(e)}"}), 500

@app.route('/analytics/kua_distribution', methods=['GET'])
def get_kua_distribution_analytics():
    """Analytics de distribuição de números Kua"""
    try:
        # Contar análises por número Kua
        from sqlalchemy import func
        
        result = db.session.query(
            KuaAnalysis.kua_number,
            func.count(KuaAnalysis.id).label('count')
        ).group_by(KuaAnalysis.kua_number).order_by(KuaAnalysis.kua_number).all()
        
        analytics_data = []
        for row in result:
            analytics_data.append({
                'kua_number': row[0],
                'count': row[1]
            })
        
        return jsonify({
            'status': 'success',
            'data': analytics_data
        })
        
    except Exception as e:
        return jsonify({"status": "error", "message": f"Erro ao gerar analytics Kua: {str(e)}"}), 500

@app.route('/analytics/house_compatibility_scores', methods=['GET'])
def get_house_compatibility_scores():
    """Analytics de scores de compatibilidade de casas"""
    try:
        # Estatísticas de compatibilidade
        from sqlalchemy import func
        
        result = db.session.query(
            HouseCompatibilityAnalysis.compatibility_level,
            func.count(HouseCompatibilityAnalysis.id).label('count'),
            func.avg(HouseCompatibilityAnalysis.compatibility_score).label('avg_score')
        ).group_by(HouseCompatibilityAnalysis.compatibility_level).all()
        
        analytics_data = []
        for row in result:
            analytics_data.append({
                'compatibility_level': row[0],
                'count': row[1],
                'average_score': round(float(row[2]) if row[2] else 0, 2)
            })
        
        return jsonify({
            'status': 'success',
            'data': analytics_data
        })
        
    except Exception as e:
        return jsonify({"status": "error", "message": f"Erro ao gerar analytics de compatibilidade: {str(e)}"}), 500


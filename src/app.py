from flask import Flask, request, jsonify, send_file
from spatial_analysis import process_floor_plan
from energetic_analysis import get_geographical_data, simulate_chi_flow, identify_architectural_poisons, get_material_database_entry
from occupant_profiles import calculate_bazi, classify_function_energy, relate_profile_to_area
from models import db, FloorPlan, EnergeticAnalysis, OccupantProfile # Importar db e os modelos
from report_generator import generate_analysis_report # Importar o gerador de relatórios
import os
import datetime
from io import BytesIO # Para lidar com o PDF em memória
from sqlalchemy import func # Para funções de agregação

app = Flask(__name__)

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

@app.route('/floor_plans', methods=['GET'])
def get_floor_plans():
    floor_plans = FloorPlan.query.all()
    return jsonify([{
        "id": fp.id,
        "filename": fp.filename,
        "upload_date": fp.upload_date.isoformat(),
        "analysis_results": fp.analysis_results
    } for fp in floor_plans]), 200

@app.route('/energetic_analyses', methods=['GET'])
def get_energetic_analyses():
    analyses = EnergeticAnalysis.query.all()
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

@app.route('/occupant_profiles', methods=['GET'])
def get_occupant_profiles():
    profiles = OccupantProfile.query.all()
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
    app.run(debug=True, host='0.0.0.0', port=5000)



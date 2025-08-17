from flask import Flask, request, jsonify
from spatial_analysis import process_floor_plan
from energetic_analysis import get_geographical_data, simulate_chi_flow, identify_architectural_poisons, get_material_database_entry
from occupant_profiles import calculate_bazi, classify_function_energy, relate_profile_to_area
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
        result = process_floor_plan(filepath)
        os.remove(filepath) # Remover o arquivo após o processamento
        return jsonify(result), 200

@app.route('/analyze_energetics', methods=['POST'])
def analyze_energetics():
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "Dados JSON não fornecidos."}), 400

    latitude = data.get('latitude')
    longitude = data.get('longitude')
    floor_plan_data = data.get('floor_plan_data', {}) # Dados simulados da planta baixa

    if not latitude or not longitude:
        return jsonify({"status": "error", "message": "Latitude e Longitude são obrigatórias."}), 400

    geo_data = get_geographical_data(latitude, longitude)
    chi_flow = simulate_chi_flow(floor_plan_data)
    architectural_poisons = identify_architectural_poisons(floor_plan_data)

    # Exemplo de como buscar dados de materiais (pode ser expandido)
    material_info = get_material_database_entry("wood")

    return jsonify({
        "status": "success",
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

    occupant_type = data.get('type') # 'owner_family' ou 'employee'
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

    # Simulação de relacionamento com área (pode ser um endpoint separado ou integrado)
    # relate_profile_to_area("profile_id_gerado", "area_id_recebido")

    return jsonify({"status": "success", "message": "Perfil de ocupante registrado com sucesso (simulado).", "profile": profile_data}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)



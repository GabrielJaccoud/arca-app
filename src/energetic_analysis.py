import random
from pygeomag import GeoMag
import datetime

def get_geographical_data(latitude: float, longitude: float, date: datetime.date):
    """
    Obtém dados geográficos reais e simulados para uma dada localização.
    Inclui dados de campo magnético real e simulações para anomalias geológicas e veios de água.
    """
    # Dados de campo magnético real usando pygeomag
    try:
        gm = GeoMag()
        
        # Converter data para ano decimal
        year_decimal = date.year + (date.timetuple().tm_yday - 1) / 365.25
        
        # Calcular dados magnéticos (altitude = 0 metros)
        result = gm.calculate(latitude, longitude, 0, year_decimal)
        
        magnetic_field_data = {
            "declination": result.dec,  # Declinação magnética
            "inclination": result.inclination,  # Inclinação magnética
            "horizontal_intensity": result.h, # Intensidade horizontal
            "total_intensity": result.f,    # Intensidade total
            "x_component": result.x,  # Componente X
            "y_component": result.y,  # Componente Y
            "z_component": result.z,  # Componente Z
        }
        
        # Classificar proximidade CEM baseada na intensidade total
        cem_proximity = "low" # Valor padrão
        if result.f > 50000: # Exemplo de limiar para alta intensidade
            cem_proximity = "high"
        elif result.f > 30000:
            cem_proximity = "medium"

    except Exception as e:
        print(f"Erro ao obter dados de campo magnético: {e}")
        magnetic_field_data = {"error": f"Não foi possível obter dados de campo magnético real: {str(e)}"}
        cem_proximity = "unknown"

    # Simulação aprimorada de anomalias geológicas
    geological_anomalies = "none"
    if random.random() < 0.1:  # 10% de chance de anomalia leve
        geological_anomalies = "minor_fault_line"
    elif random.random() < 0.02: # 2% de chance de anomalia significativa
        geological_anomalies = "major_geological_stress_zone"

    # Simulação aprimorada de veios de água
    nearby_water_veins = False
    if random.random() < 0.15: # 15% de chance de veios de água
        nearby_water_veins = True

    return {
        "status": "success",
        "data": {
            "latitude": latitude,
            "longitude": longitude,
            "magnetic_field": magnetic_field_data,
            "cem_proximity": cem_proximity,
            "geological_anomalies": geological_anomalies,
            "nearby_water_veins": nearby_water_veins
        }
    }

def simulate_chi_flow(floor_plan_data: dict):
    """
    Simula a análise do fluxo de Chi em uma planta baixa.
    """
    # Lógica de simulação mais elaborada
    obstructed_areas = []
    if floor_plan_data.get("simulated_elements", {}).get("long_corridors"): # Exemplo de como usar dados da planta
        obstructed_areas.append("long_corridors_leading_to_energy_loss")
    if random.random() < 0.3: # 30% de chance de áreas obstruídas
        obstructed_areas.append("cluttered_entrance")

    return {
        "status": "success",
        "assessment": {
            "obstructed_areas": obstructed_areas,
            "long_corridors": floor_plan_data.get("simulated_elements", {}).get("long_corridors", False),
            "central_open_spaces": floor_plan_data.get("simulated_elements", {}).get("central_open_spaces", True),
            "chi_flow_quality": random.choice(["excellent", "good", "fair", "poor"])
        }
    }

def identify_architectural_poisons(floor_plan_data: dict):
    """
    Simula a identificação de "venenos" arquitetônicos.
    """
    poisons = []
    if random.random() < 0.2: # 20% de chance de cantos afiados
        poisons.append("sharp_corner_pointing_to_bed")
    if random.random() < 0.1: # 10% de chance de vigas expostas
        poisons.append("exposed_beams_over_seating_area")
    if floor_plan_data.get("simulated_elements", {}).get("bathroom_near_entrance"): # Exemplo de como usar dados da planta
        poisons.append("bathroom_near_main_entrance")

    return {
        "status": "success",
        "poisons": poisons
    }

def get_material_database_entry(material_name: str):
    """
    Simula a consulta a um banco de dados de materiais.
    """
    materials_db = {
        "wood": {"conductivity": "low", "density": "medium", "origin": "natural", "impact": "positive"},
        "metal": {"conductivity": "high", "density": "high", "origin": "natural", "impact": "neutral"},
        "concrete": {"conductivity": "medium", "density": "high", "origin": "artificial", "impact": "neutral"},
        "glass": {"conductivity": "low", "density": "medium", "origin": "artificial", "impact": "neutral"},
        "water": {"conductivity": "high", "density": "low", "origin": "natural", "impact": "positive"},
    }
    return {"status": "success", "data": materials_db.get(material_name.lower(), {"message": "Material não encontrado no banco de dados simulado."})}

if __name__ == '__main__':
    # Exemplo de uso
    lat = -23.55052
    lon = -46.633309
    today = datetime.date.today()
    print(get_geographical_data(lat, lon, today))

    floor_data = {"simulated_elements": {"long_corridors": True, "central_open_spaces": False, "bathroom_near_entrance": True}}
    print(simulate_chi_flow(floor_data))
    print(identify_architectural_poisons(floor_data))
    print(get_material_database_entry("wood"))


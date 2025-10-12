from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

class FloorPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.datetime.now)
    analysis_results = db.Column(db.JSON) # Armazenar os resultados da análise espacial

    def __repr__(self):
        return f'<FloorPlan {self.filename}>'

class EnergeticAnalysis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    floor_plan_id = db.Column(db.Integer, db.ForeignKey("floor_plan.id"), nullable=True) # Opcional, se a análise for independente
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    analysis_date = db.Column(db.DateTime, default=datetime.datetime.now)
    magnetic_field_data = db.Column(db.JSON)
    cem_proximity = db.Column(db.String(50))
    geological_anomalies = db.Column(db.String(255))
    nearby_water_veins = db.Column(db.Boolean)
    chi_flow_assessment = db.Column(db.JSON)
    architectural_poisons = db.Column(db.JSON)

    def __repr__(self):
        return f'<EnergeticAnalysis {self.latitude}, {self.longitude}>'

class OccupantProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    profile_type = db.Column(db.String(50), nullable=False) # 'owner_family' ou 'employee'
    details = db.Column(db.JSON) # Armazenar dados específicos (BaZi, função, etc.)
    registration_date = db.Column(db.DateTime, default=datetime.datetime.now)

    def __repr__(self):
        return f'<OccupantProfile {self.name}>'

class BaZiAnalysis(db.Model):
    """Modelo para armazenar análises BaZi"""
    id = db.Column(db.Integer, primary_key=True)
    occupant_profile_id = db.Column(db.Integer, db.ForeignKey("occupant_profile.id"), nullable=True)
    birth_datetime = db.Column(db.DateTime, nullable=False)
    timezone_offset = db.Column(db.Integer, default=-3)
    year_pillar = db.Column(db.JSON)  # Heavenly Stem + Earthly Branch
    month_pillar = db.Column(db.JSON)
    day_pillar = db.Column(db.JSON)
    hour_pillar = db.Column(db.JSON)
    day_master = db.Column(db.JSON)  # Elemento e força
    useful_god = db.Column(db.JSON)  # Elemento benéfico
    recommendations = db.Column(db.JSON)  # Cores, direções, carreira
    analysis_date = db.Column(db.DateTime, default=datetime.datetime.now)

    def __repr__(self):
        return f'<BaZiAnalysis {self.birth_datetime}>'

class KuaAnalysis(db.Model):
    """Modelo para armazenar análises Kua"""
    id = db.Column(db.Integer, primary_key=True)
    occupant_profile_id = db.Column(db.Integer, db.ForeignKey("occupant_profile.id"), nullable=True)
    birth_year = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    kua_number = db.Column(db.Integer, nullable=False)
    group = db.Column(db.String(10))  # East ou West
    element = db.Column(db.String(10))  # Metal, Wood, Water, Fire, Earth
    personality = db.Column(db.String(255))
    favorable_directions = db.Column(db.JSON)
    unfavorable_directions = db.Column(db.JSON)
    recommendations = db.Column(db.JSON)  # Cores, materiais, posicionamento
    analysis_date = db.Column(db.DateTime, default=datetime.datetime.now)

    def __repr__(self):
        return f'<KuaAnalysis {self.kua_number}>'

class HouseCompatibilityAnalysis(db.Model):
    """Modelo para armazenar análises de compatibilidade casa-pessoa"""
    id = db.Column(db.Integer, primary_key=True)
    kua_analysis_id = db.Column(db.Integer, db.ForeignKey("kua_analysis.id"), nullable=False)
    house_facing_direction = db.Column(db.String(20), nullable=False)
    compatibility_level = db.Column(db.String(20))  # Excellent, Good, Neutral, Challenging
    compatibility_score = db.Column(db.Integer)  # 0-100
    direction_type = db.Column(db.String(50))  # Sheng Qi, Tian Yi, etc.
    benefits = db.Column(db.JSON)
    recommendations = db.Column(db.JSON)
    feng_shui_advice = db.Column(db.JSON)
    analysis_date = db.Column(db.DateTime, default=datetime.datetime.now)

    def __repr__(self):
        return f'<HouseCompatibilityAnalysis {self.house_facing_direction}>'

class CompleteAnalysis(db.Model):
    """Modelo para armazenar análises integradas BaZi + Kua"""
    id = db.Column(db.Integer, primary_key=True)
    bazi_analysis_id = db.Column(db.Integer, db.ForeignKey("ba_zi_analysis.id"), nullable=False)
    kua_analysis_id = db.Column(db.Integer, db.ForeignKey("kua_analysis.id"), nullable=False)
    element_harmony = db.Column(db.String(50))  # Harmonious, Conflicting, Neutral
    unified_recommendations = db.Column(db.JSON)
    career_alignment = db.Column(db.JSON)
    relationship_guidance = db.Column(db.JSON)
    feng_shui_priority = db.Column(db.JSON)
    analysis_date = db.Column(db.DateTime, default=datetime.datetime.now)

    def __repr__(self):
        return f'<CompleteAnalysis {self.id}>'




# ===== NOVOS MODELOS PARA FUNCIONALIDADES AVANÇADAS =====

class GeobiologyAnalysis(db.Model):
    """Modelo para armazenar análises geobiológicas"""
    id = db.Column(db.Integer, primary_key=True)
    floor_plan_id = db.Column(db.Integer, db.ForeignKey("floor_plan.id"), nullable=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    area_width = db.Column(db.Float, nullable=False)
    area_height = db.Column(db.Float, nullable=False)
    soil_type = db.Column(db.String(50))
    hartmann_grid_data = db.Column(db.JSON)
    curry_grid_data = db.Column(db.JSON)
    water_veins = db.Column(db.JSON)
    geological_faults = db.Column(db.JSON)
    geopathogenic_zones = db.Column(db.JSON)
    soil_radiation = db.Column(db.JSON)
    overall_assessment = db.Column(db.JSON)
    analysis_date = db.Column(db.DateTime, default=datetime.datetime.now)

    def __repr__(self):
        return f'<GeobiologyAnalysis {self.latitude}, {self.longitude}>'


class EMFAnalysis(db.Model):
    """Modelo para armazenar análises de campos eletromagnéticos"""
    id = db.Column(db.Integer, primary_key=True)
    floor_plan_id = db.Column(db.Integer, db.ForeignKey("floor_plan.id"), nullable=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    cell_towers = db.Column(db.JSON)
    power_lines = db.Column(db.JSON)
    transformers = db.Column(db.JSON)
    internal_sources = db.Column(db.JSON)
    total_exposure = db.Column(db.JSON)
    overall_assessment = db.Column(db.JSON)
    recommendations = db.Column(db.JSON)
    analysis_date = db.Column(db.DateTime, default=datetime.datetime.now)

    def __repr__(self):
        return f'<EMFAnalysis {self.latitude}, {self.longitude}>'


class LeyLineAnalysis(db.Model):
    """Modelo para armazenar análises de linhas ley"""
    id = db.Column(db.Integer, primary_key=True)
    floor_plan_id = db.Column(db.Integer, db.ForeignKey("floor_plan.id"), nullable=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    search_radius_km = db.Column(db.Float, default=50.0)
    sacred_sites = db.Column(db.JSON)
    ley_lines = db.Column(db.JSON)
    energy_vortices = db.Column(db.JSON)
    astronomical_alignments = db.Column(db.JSON)
    overall_assessment = db.Column(db.JSON)
    analysis_date = db.Column(db.DateTime, default=datetime.datetime.now)

    def __repr__(self):
        return f'<LeyLineAnalysis {self.latitude}, {self.longitude}>'


class SacredGeometryAnalysis(db.Model):
    """Modelo para armazenar análises de geometria sagrada"""
    id = db.Column(db.Integer, primary_key=True)
    floor_plan_id = db.Column(db.Integer, db.ForeignKey("floor_plan.id"), nullable=True)
    overall_dimensions = db.Column(db.JSON)
    room_analyses = db.Column(db.JSON)
    sacred_patterns = db.Column(db.JSON)
    fibonacci_analysis = db.Column(db.JSON)
    platonic_solids = db.Column(db.JSON)
    harmony_score = db.Column(db.Float)
    overall_assessment = db.Column(db.JSON)
    recommendations = db.Column(db.JSON)
    analysis_date = db.Column(db.DateTime, default=datetime.datetime.now)

    def __repr__(self):
        return f'<SacredGeometryAnalysis {self.id}>'


class SacredArchitectureAnalysis(db.Model):
    """Modelo para armazenar análises de arquitetura sagrada"""
    id = db.Column(db.Integer, primary_key=True)
    floor_plan_id = db.Column(db.Integer, db.ForeignKey("floor_plan.id"), nullable=True)
    room_analyses = db.Column(db.JSON)
    materials_analysis = db.Column(db.JSON)
    sacred_spaces = db.Column(db.JSON)
    astronomical_integration = db.Column(db.JSON)
    circulation_flow = db.Column(db.JSON)
    symmetry_balance = db.Column(db.JSON)
    overall_assessment = db.Column(db.JSON)
    comprehensive_recommendations = db.Column(db.JSON)
    analysis_date = db.Column(db.DateTime, default=datetime.datetime.now)

    def __repr__(self):
        return f'<SacredArchitectureAnalysis {self.id}>'


class IntegratedAnalysis(db.Model):
    """Modelo para armazenar análises integradas de todas as funcionalidades"""
    id = db.Column(db.Integer, primary_key=True)
    floor_plan_id = db.Column(db.Integer, db.ForeignKey("floor_plan.id"), nullable=False)
    bazi_analysis_id = db.Column(db.Integer, db.ForeignKey("ba_zi_analysis.id"), nullable=True)
    kua_analysis_id = db.Column(db.Integer, db.ForeignKey("kua_analysis.id"), nullable=True)
    geobiology_analysis_id = db.Column(db.Integer, db.ForeignKey("geobiology_analysis.id"), nullable=True)
    emf_analysis_id = db.Column(db.Integer, db.ForeignKey("emf_analysis.id"), nullable=True)
    leyline_analysis_id = db.Column(db.Integer, db.ForeignKey("ley_line_analysis.id"), nullable=True)
    sacred_geometry_analysis_id = db.Column(db.Integer, db.ForeignKey("sacred_geometry_analysis.id"), nullable=True)
    sacred_architecture_analysis_id = db.Column(db.Integer, db.ForeignKey("sacred_architecture_analysis.id"), nullable=True)
    
    overall_health_score = db.Column(db.Float)  # Score geral 0-100
    priority_recommendations = db.Column(db.JSON)
    implementation_plan = db.Column(db.JSON)
    risk_assessment = db.Column(db.JSON)
    analysis_date = db.Column(db.DateTime, default=datetime.datetime.now)

    def __repr__(self):
        return f'<IntegratedAnalysis {self.id}>'


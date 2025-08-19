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



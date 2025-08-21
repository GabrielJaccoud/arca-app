from fpdf import FPDF
from datetime import datetime

class PDFReport(FPDF):
    def header(self):
        self.set_font("Arial", "B", 15)
        self.cell(0, 10, "Relatório de Análise ARCA", 0, 1, "C")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Página {self.page_no()}/{{nb}}", 0, 0, "C")

    def chapter_title(self, title):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, title, 0, 1, "L")
        self.ln(5)

    def chapter_body(self, body):
        self.set_font("Arial", "", 10)
        self.multi_cell(0, 5, body)
        self.ln()

def generate_analysis_report(floor_plan_data, energetic_analysis_data, occupant_profiles_data):
    pdf = PDFReport()
    pdf.alias_nb_pages()
    pdf.add_page()

    pdf.chapter_title("Dados da Planta Baixa")
    if floor_plan_data:
        pdf.chapter_body(f"Nome do Arquivo: {floor_plan_data.filename}\n" \
                         f"Data de Upload: {floor_plan_data.upload_date.strftime("%d/%m/%Y %H:%M")}\n" \
                         f"Status da Análise: {floor_plan_data.analysis_results.get("status", "N/A")}\n" \
                         f"Detalhes: {floor_plan_data.analysis_results.get("message", "N/A")}")
        
        details = floor_plan_data.analysis_results.get("details", {})
        if details.get("processed_as") == "image":
            pdf.chapter_body(f"Tipo: Imagem ({details.get("format")})\n" \
                             f"Dimensões: {details.get("width")}x{details.get("height")}px\n" \
                             f"Bordas Detectadas: {'Sim' if details.get('real_features', {}).get('edges_detected') else 'Não'}\n" \
                             f"Linhas Identificadas: {'Sim' if details.get('real_features', {}).get('lines_identified') else 'Não'}\n" \
                             f"Número de Linhas: {details.get('real_features', {}).get('num_lines_detected', 'N/A')}")
        elif details.get("processed_as") == "image_from_pdf":
            pdf.chapter_body(f"Tipo: PDF convertido para Imagem\n" \
                             f"Páginas: {details.get("pages")}\n" \
                             f"Primeira Página - Dimensões: {details.get('page_1', {}).get('width')}x{details.get('page_1', {}).get('height')}px\n" \
                             f"Primeira Página - Bordas Detectadas: {'Sim' if details.get('page_1', {}).get('real_features', {}).get('edges_detected') else 'Não'}")
    else:
        pdf.chapter_body("Nenhum dado de planta baixa disponível.")

    pdf.add_page()
    pdf.chapter_title("Análise Energética")
    if energetic_analysis_data:
        pdf.chapter_body(f"Latitude: {energetic_analysis_data.latitude}\n" \
                         f"Longitude: {energetic_analysis_data.longitude}\n" \
                         f"Data da Análise: {energetic_analysis_data.analysis_date.strftime("%d/%m/%Y %H:%M")}\n" \
                         f"Proximidade CEM: {energetic_analysis_data.cem_proximity}\n" \
                         f"Anomalias Geológicas: {energetic_analysis_data.geological_anomalies}\n" \
                         f"Veios de Água Próximos: {'Sim' if energetic_analysis_data.nearby_water_veins else 'Não'}")
        
        if energetic_analysis_data.magnetic_field_data:
            mf_data = energetic_analysis_data.magnetic_field_data
            pdf.chapter_body(f"\nDados de Campo Magnético:\n" \
                             f"  Declinação: {mf_data.get('declination', 'N/A'):.2f}°\n" \
                             f"  Inclinação: {mf_data.get('inclination', 'N/A'):.2f}°\n" \
                             f"  Intensidade Horizontal: {mf_data.get('horizontal_intensity', 'N/A'):.0f} nT\n" \
                             f"  Intensidade Total: {mf_data.get('total_intensity', 'N/A'):.0f} nT")
        
        if energetic_analysis_data.chi_flow_assessment:
            cf_data = energetic_analysis_data.chi_flow_assessment
            pdf.chapter_body(f"\nFluxo de Chi:\n" \
                             f"  Qualidade: {cf_data.get('chi_flow_quality', 'N/A')}\n" \
                             f"  Áreas Obstruídas: {', '.join(cf_data.get('obstructed_areas', [])) if cf_data.get('obstructed_areas') else 'Nenhuma'}")
        
        if energetic_analysis_data.architectural_poisons:
            ap_data = energetic_analysis_data.architectural_poisons
            pdf.chapter_body(f"\nVenenos Arquitetônicos:\n" \
                             f"  {', '.join(ap_data) if ap_data else 'Nenhum'}")
    else:
        pdf.chapter_body("Nenhum dado de análise energética disponível.")

    pdf.add_page()
    pdf.chapter_title("Perfis de Ocupantes")
    if occupant_profiles_data:
        for profile in occupant_profiles_data:
            pdf.chapter_body(f"Nome: {profile.name}\n" \
                             f"Tipo: {profile.profile_type}\n" \
                             f"Data de Registro: {profile.registration_date.strftime("%d/%m/%Y %H:%M")}")
            if profile.profile_type == "owner_family" and profile.details and profile.details.get("bazi_profile"):
                bazi = profile.details.get("bazi_profile").get("profile", {})
                pdf.chapter_body(f"  Elemento Mestre BaZi: {bazi.get('master_element', 'N/A')}\n" \
                                 f"  Equilíbrio de Elementos: {bazi.get('element_balance', 'N/A')}\n" \
                                 f"  Necessidades Elementais: {', '.join(bazi.get('elemental_needs', [])) if bazi.get('elemental_needs') else 'N/A'}")
            elif profile.profile_type == "employee" and profile.details and profile.details.get("function_energy"):
                pdf.chapter_body(f"  Função: {profile.details.get('function', 'N/A')}\n" \
                                 f"  Energia da Função: {profile.details.get('function_energy', 'N/A')}")
            pdf.ln(5)
    else:
        pdf.chapter_body("Nenhum perfil de ocupante disponível.")

    # Salvar o PDF em um buffer e retornar
    return pdf.output(dest='S').encode('latin1')



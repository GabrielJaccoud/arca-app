"""
Módulo de Geração de Visualizações - Sistema ARCA v3.1
Gera diagramas e visualizações para análises geobiológicas e de linhas ley

Utiliza matplotlib para criar visualizações profissionais
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Circle, Rectangle, FancyBboxPatch, Wedge
import numpy as np
from typing import Dict, List, Tuple
import math


class GeobiologyVisualizer:
    """Gerador de visualizações geobiológicas"""
    
    def __init__(self, analysis_data: Dict):
        """
        Inicializa o visualizador
        
        Args:
            analysis_data: Dados da análise geobiológica avançada
        """
        self.data = analysis_data
        self.area_width = analysis_data['location']['area_width']
        self.area_height = analysis_data['location']['area_height']
        
    def create_complete_diagram(self, output_path: str):
        """
        Cria diagrama completo com todas as redes e zonas
        
        Args:
            output_path: Caminho para salvar o diagrama
        """
        fig, ax = plt.subplots(figsize=(16, 12))
        fig.patch.set_facecolor('white')
        
        # Configurar limites e aspecto
        ax.set_xlim(0, self.area_width)
        ax.set_ylim(0, self.area_height)
        ax.set_aspect('equal')
        
        # Título
        title = f"Análise Geobiológica Completa\n"
        title += f"Localização: {self.data['location']['latitude']:.4f}, {self.data['location']['longitude']:.4f}\n"
        title += f"Score de Saúde: {self.data['overall_assessment']['geobiological_health_score']}/100"
        ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
        
        # Desenhar grade Hartmann
        self._draw_hartmann_grid(ax)
        
        # Desenhar grade Curry
        self._draw_curry_grid(ax)
        
        # Desenhar veios de água
        self._draw_water_veins(ax)
        
        # Desenhar falhas geológicas
        self._draw_geological_faults(ax)
        
        # Desenhar zonas geopatogênicas
        self._draw_geopathogenic_zones(ax)
        
        # Adicionar legenda
        self._add_legend(ax)
        
        # Adicionar grid de referência
        ax.grid(True, alpha=0.2, linestyle='--')
        ax.set_xlabel('Largura (metros)', fontsize=12)
        ax.set_ylabel('Altura (metros)', fontsize=12)
        
        # Salvar
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return output_path
    
    def _draw_hartmann_grid(self, ax):
        """Desenha a grade Hartmann"""
        hartmann = self.data['hartmann_grid']
        
        # Linhas Norte-Sul
        for line in hartmann['ns_lines']:
            x = line['position']
            ax.plot([x, x], [0, self.area_height], 
                   color='blue', linewidth=1, alpha=0.6, linestyle='-',
                   label='Hartmann N-S' if line == hartmann['ns_lines'][0] else '')
        
        # Linhas Leste-Oeste
        for line in hartmann['ew_lines']:
            y = line['position']
            ax.plot([0, self.area_width], [y, y], 
                   color='blue', linewidth=1, alpha=0.6, linestyle='-',
                   label='Hartmann L-O' if line == hartmann['ew_lines'][0] else '')
        
        # Marcar cruzamentos
        for crossing in hartmann['crossings']:
            color = self._get_risk_color(crossing['risk_level'])
            circle = Circle((crossing['x'], crossing['y']), 0.15, 
                          color=color, alpha=0.5)
            ax.add_patch(circle)
    
    def _draw_curry_grid(self, ax):
        """Desenha a grade Curry (diagonal)"""
        curry = self.data['curry_grid']
        
        # Linhas diagonais NE-SW
        for line in curry['ne_sw_lines']:
            offset = line['offset']
            # Calcular pontos da linha diagonal
            x1, y1 = 0, offset
            x2, y2 = self.area_width, offset + self.area_width
            
            if y1 < 0:
                x1 = -y1
                y1 = 0
            if y2 > self.area_height:
                x2 = self.area_width - (y2 - self.area_height)
                y2 = self.area_height
            
            ax.plot([x1, x2], [y1, y2], 
                   color='purple', linewidth=1, alpha=0.5, linestyle='--',
                   label='Curry NE-SW' if line == curry['ne_sw_lines'][0] else '')
        
        # Linhas diagonais NW-SE
        for line in curry['nw_se_lines']:
            offset = line['offset']
            x1, y1 = 0, self.area_height - offset
            x2, y2 = self.area_width, self.area_height - offset - self.area_width
            
            if y1 > self.area_height:
                x1 = y1 - self.area_height
                y1 = self.area_height
            if y2 < 0:
                x2 = self.area_width + y2
                y2 = 0
            
            ax.plot([x1, x2], [y1, y2], 
                   color='purple', linewidth=1, alpha=0.5, linestyle='--',
                   label='Curry NW-SE' if line == curry['nw_se_lines'][0] else '')
        
        # Marcar cruzamentos Curry
        for crossing in curry['crossings']:
            color = self._get_risk_color(crossing['risk_level'])
            square = Rectangle((crossing['x']-0.2, crossing['y']-0.2), 0.4, 0.4,
                             color=color, alpha=0.6)
            ax.add_patch(square)
    
    def _draw_water_veins(self, ax):
        """Desenha veios de água subterrâneos"""
        water_veins = self.data['water_veins']
        
        for vein in water_veins['veins']:
            ax.plot([vein['start_x'], vein['end_x']], 
                   [vein['start_y'], vein['end_y']],
                   color='cyan', linewidth=3, alpha=0.7, linestyle='-',
                   label='Veio de Água' if vein == water_veins['veins'][0] else '')
            
            # Adicionar marcador no centro
            center_x = (vein['start_x'] + vein['end_x']) / 2
            center_y = (vein['start_y'] + vein['end_y']) / 2
            ax.plot(center_x, center_y, 'o', color='cyan', markersize=8)
    
    def _draw_geological_faults(self, ax):
        """Desenha falhas geológicas"""
        faults = self.data['geological_faults']
        
        for fault in faults['faults']:
            ax.plot([fault['start_x'], fault['end_x']], 
                   [fault['start_y'], fault['end_y']],
                   color='red', linewidth=4, alpha=0.8, linestyle='-.',
                   label='Falha Geológica' if fault == faults['faults'][0] else '')
            
            # Adicionar marcador de perigo
            center_x = (fault['start_x'] + fault['end_x']) / 2
            center_y = (fault['start_y'] + fault['end_y']) / 2
            ax.plot(center_x, center_y, 'X', color='red', markersize=12, markeredgewidth=2)
    
    def _draw_geopathogenic_zones(self, ax):
        """Desenha zonas geopatogênicas"""
        zones = self.data['geopathogenic_zones']['zones']
        
        for zone in zones:
            color = self._get_risk_color(zone['risk_level'])
            circle = Circle((zone['x'], zone['y']), zone['radius_meters'],
                          color=color, alpha=0.3, linewidth=2, edgecolor=color)
            ax.add_patch(circle)
            
            # Adicionar rótulo
            if zone['risk_level'] in ['critical', 'high']:
                ax.text(zone['x'], zone['y'], '⚠', 
                       fontsize=20, ha='center', va='center')
    
    def _get_risk_color(self, risk_level: str) -> str:
        """Retorna cor baseada no nível de risco"""
        colors = {
            'low': 'green',
            'medium': 'yellow',
            'high': 'orange',
            'critical': 'red'
        }
        return colors.get(risk_level, 'gray')
    
    def _add_legend(self, ax):
        """Adiciona legenda ao diagrama"""
        handles, labels = ax.get_legend_handles_labels()
        
        # Remover duplicatas
        by_label = dict(zip(labels, handles))
        
        ax.legend(by_label.values(), by_label.keys(), 
                 loc='upper right', fontsize=10, framealpha=0.9)
    
    def create_risk_heatmap(self, output_path: str):
        """
        Cria mapa de calor de risco geobiológico
        
        Args:
            output_path: Caminho para salvar o mapa
        """
        fig, ax = plt.subplots(figsize=(14, 10))
        
        # Criar grid de pontos
        resolution = 50
        x = np.linspace(0, self.area_width, resolution)
        y = np.linspace(0, self.area_height, resolution)
        X, Y = np.meshgrid(x, y)
        
        # Calcular risco em cada ponto
        Z = np.zeros_like(X)
        
        for i in range(resolution):
            for j in range(resolution):
                px, py = X[i, j], Y[i, j]
                risk_score = self._calculate_point_risk(px, py)
                Z[i, j] = risk_score
        
        # Criar heatmap
        im = ax.contourf(X, Y, Z, levels=20, cmap='RdYlGn_r', alpha=0.8)
        
        # Adicionar contornos
        contours = ax.contour(X, Y, Z, levels=5, colors='black', alpha=0.3, linewidths=0.5)
        ax.clabel(contours, inline=True, fontsize=8)
        
        # Colorbar
        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label('Nível de Risco Geobiológico', fontsize=12)
        
        # Título
        ax.set_title('Mapa de Calor - Risco Geobiológico', fontsize=16, fontweight='bold')
        ax.set_xlabel('Largura (metros)', fontsize=12)
        ax.set_ylabel('Altura (metros)', fontsize=12)
        
        # Salvar
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return output_path
    
    def _calculate_point_risk(self, x: float, y: float) -> float:
        """Calcula risco geobiológico em um ponto específico"""
        risk = 0
        
        # Risco de cruzamentos Hartmann
        for crossing in self.data['hartmann_grid']['crossings']:
            distance = math.sqrt((x - crossing['x'])**2 + (y - crossing['y'])**2)
            if distance < 0.5:
                risk += 30
            elif distance < 1.0:
                risk += 15
        
        # Risco de cruzamentos Curry (mais intenso)
        for crossing in self.data['curry_grid']['crossings']:
            distance = math.sqrt((x - crossing['x'])**2 + (y - crossing['y'])**2)
            if distance < 0.5:
                risk += 50
            elif distance < 1.0:
                risk += 25
        
        # Risco de zonas geopatogênicas
        for zone in self.data['geopathogenic_zones']['zones']:
            distance = math.sqrt((x - zone['x'])**2 + (y - zone['y'])**2)
            if distance < zone['radius_meters']:
                if zone['risk_level'] == 'critical':
                    risk += 60
                elif zone['risk_level'] == 'high':
                    risk += 40
                elif zone['risk_level'] == 'medium':
                    risk += 20
        
        return min(risk, 100)


class LeyLineVisualizer:
    """Gerador de visualizações de linhas ley"""
    
    def __init__(self, analysis_data: Dict):
        """
        Inicializa o visualizador
        
        Args:
            analysis_data: Dados da análise de linhas ley avançada
        """
        self.data = analysis_data
        self.latitude = analysis_data['location']['latitude']
        self.longitude = analysis_data['location']['longitude']
        self.radius_km = analysis_data['location']['search_radius_km']
    
    def create_ley_line_map(self, output_path: str):
        """
        Cria mapa de linhas ley e sítios sagrados
        
        Args:
            output_path: Caminho para salvar o mapa
        """
        fig, ax = plt.subplots(figsize=(16, 12))
        fig.patch.set_facecolor('white')
        
        # Calcular limites do mapa
        lat_range = self.radius_km / 111.0  # 1 grau ≈ 111 km
        lon_range = self.radius_km / (111.0 * math.cos(math.radians(self.latitude)))
        
        ax.set_xlim(self.longitude - lon_range, self.longitude + lon_range)
        ax.set_ylim(self.latitude - lat_range, self.latitude + lat_range)
        ax.set_aspect('equal')
        
        # Título
        title = f"Mapa de Linhas Ley e Sítios Sagrados\n"
        title += f"Raio de busca: {self.radius_km} km\n"
        title += f"Score Energético: {self.data['overall_assessment']['energetic_potential_score']}/100"
        ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
        
        # Desenhar círculo de busca
        circle = Circle((self.longitude, self.latitude), lon_range,
                       fill=False, edgecolor='gray', linestyle='--', linewidth=2)
        ax.add_patch(circle)
        
        # Marcar localização central
        ax.plot(self.longitude, self.latitude, '*', 
               color='gold', markersize=30, markeredgecolor='black', markeredgewidth=2,
               label='Localização Analisada')
        
        # Desenhar sítios sagrados
        self._draw_sacred_sites(ax)
        
        # Desenhar linhas ley
        self._draw_ley_lines(ax)
        
        # Desenhar vórtices
        self._draw_vortices(ax)
        
        # Adicionar legenda
        ax.legend(loc='upper right', fontsize=10, framealpha=0.9)
        
        # Adicionar grid
        ax.grid(True, alpha=0.3, linestyle=':')
        ax.set_xlabel('Longitude', fontsize=12)
        ax.set_ylabel('Latitude', fontsize=12)
        
        # Salvar
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return output_path
    
    def _draw_sacred_sites(self, ax):
        """Desenha sítios sagrados no mapa"""
        sites = self.data['sacred_sites']['sites']
        
        # Cores por tipo
        type_colors = {
            'church': 'blue',
            'monastery': 'purple',
            'cathedral': 'darkblue',
            'natural_formation': 'green',
            'mountain': 'brown',
            'mountain_sanctuary': 'darkgreen',
            'historical_sacred': 'orange',
            'spiritual_community': 'pink',
            'spiritual_center': 'magenta',
            'natural_phenomenon': 'cyan',
            'archaeological': 'red'
        }
        
        for site in sites:
            color = type_colors.get(site['type'], 'gray')
            
            # Tamanho baseado em poder
            size = site['power_level'] * 15
            
            ax.plot(site['longitude'], site['latitude'], 'o',
                   color=color, markersize=size, alpha=0.6,
                   markeredgecolor='black', markeredgewidth=1)
            
            # Adicionar rótulo
            ax.text(site['longitude'], site['latitude'], 
                   f"  {site['name']}\n  ({site['distance_km']}km)",
                   fontsize=8, ha='left', va='bottom')
    
    def _draw_ley_lines(self, ax):
        """Desenha linhas ley"""
        ley_lines = self.data['ley_lines']['ley_lines']
        
        # Encontrar sítios por nome
        sites_dict = {site['name']: site for site in self.data['sacred_sites']['sites']}
        
        for line in ley_lines:
            # Pegar coordenadas dos sítios
            site_coords = []
            for site_name in line['sites']:
                if site_name in sites_dict:
                    site = sites_dict[site_name]
                    site_coords.append((site['longitude'], site['latitude']))
            
            if len(site_coords) >= 2:
                # Desenhar linha
                lons = [coord[0] for coord in site_coords]
                lats = [coord[1] for coord in site_coords]
                
                color = 'red' if line['passes_through_location'] else 'orange'
                linewidth = 3 if line['passes_through_location'] else 1.5
                alpha = 0.8 if line['passes_through_location'] else 0.4
                
                ax.plot(lons, lats, '-', 
                       color=color, linewidth=linewidth, alpha=alpha,
                       label='Linha Ley' if line == ley_lines[0] else '')
    
    def _draw_vortices(self, ax):
        """Desenha vórtices energéticos"""
        vortices = self.data['energy_vortices']['vortices']
        
        for vortex in vortices:
            # Tamanho baseado em força
            if vortex['vortex_strength'] == 'strong':
                size = 500
                color = 'red'
            elif vortex['vortex_strength'] == 'medium':
                size = 300
                color = 'orange'
            else:
                size = 150
                color = 'yellow'
            
            ax.scatter(vortex['longitude'], vortex['latitude'],
                      s=size, c=color, alpha=0.3, edgecolors='black', linewidths=2,
                      marker='*', label=f'Vórtice {vortex["vortex_strength"]}' if vortex == vortices[0] else '')
    
    def create_astronomical_diagram(self, output_path: str):
        """
        Cria diagrama de alinhamentos astronômicos
        
        Args:
            output_path: Caminho para salvar o diagrama
        """
        fig, ax = plt.subplots(figsize=(12, 12), subplot_kw=dict(projection='polar'))
        fig.patch.set_facecolor('white')
        
        # Configurar eixos polares
        ax.set_theta_zero_location('N')
        ax.set_theta_direction(-1)
        
        # Dados astronômicos
        astro = self.data['astronomical_alignments']
        
        # Desenhar azimutes solares
        # Solstício de verão
        summer_sunrise = math.radians(astro['summer_solstice']['sunrise_azimuth'])
        summer_sunset = math.radians(astro['summer_solstice']['sunset_azimuth'])
        
        ax.plot([summer_sunrise, summer_sunrise], [0, 1], 'r-', linewidth=3, label='Solstício Verão')
        ax.plot([summer_sunset, summer_sunset], [0, 1], 'r--', linewidth=3)
        
        # Solstício de inverno
        winter_sunrise = math.radians(astro['winter_solstice']['sunrise_azimuth'])
        winter_sunset = math.radians(astro['winter_solstice']['sunset_azimuth'])
        
        ax.plot([winter_sunrise, winter_sunrise], [0, 1], 'b-', linewidth=3, label='Solstício Inverno')
        ax.plot([winter_sunset, winter_sunset], [0, 1], 'b--', linewidth=3)
        
        # Equinócios
        equinox_sunrise = math.radians(astro['equinoxes']['sunrise_azimuth'])
        equinox_sunset = math.radians(astro['equinoxes']['sunset_azimuth'])
        
        ax.plot([equinox_sunrise, equinox_sunrise], [0, 1], 'g-', linewidth=3, label='Equinócios')
        ax.plot([equinox_sunset, equinox_sunset], [0, 1], 'g--', linewidth=3)
        
        # Adicionar pontos cardeais
        cardinals = ['N', 'E', 'S', 'W']
        for i, cardinal in enumerate(cardinals):
            angle = math.radians(i * 90)
            ax.text(angle, 1.15, cardinal, fontsize=16, fontweight='bold', ha='center', va='center')
        
        # Título
        ax.set_title('Alinhamentos Astronômicos\nSolstícios e Equinócios', 
                    fontsize=16, fontweight='bold', pad=20)
        
        # Legenda
        ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=10)
        
        # Salvar
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return output_path


def generate_all_visualizations(geobiology_data: Dict, leyline_data: Dict, 
                               output_dir: str) -> Dict[str, str]:
    """
    Gera todas as visualizações
    
    Args:
        geobiology_data: Dados da análise geobiológica
        leyline_data: Dados da análise de linhas ley
        output_dir: Diretório para salvar as visualizações
    
    Retorna:
        Dicionário com caminhos dos arquivos gerados
    """
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    generated_files = {}
    
    # Visualizações geobiológicas
    geo_viz = GeobiologyVisualizer(geobiology_data)
    generated_files['geobiology_diagram'] = geo_viz.create_complete_diagram(
        os.path.join(output_dir, 'geobiology_complete_diagram.png')
    )
    generated_files['geobiology_heatmap'] = geo_viz.create_risk_heatmap(
        os.path.join(output_dir, 'geobiology_risk_heatmap.png')
    )
    
    # Visualizações de linhas ley
    ley_viz = LeyLineVisualizer(leyline_data)
    generated_files['leyline_map'] = ley_viz.create_ley_line_map(
        os.path.join(output_dir, 'leyline_map.png')
    )
    generated_files['astronomical_diagram'] = ley_viz.create_astronomical_diagram(
        os.path.join(output_dir, 'astronomical_alignments.png')
    )
    
    return generated_files


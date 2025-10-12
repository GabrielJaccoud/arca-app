# Funcionalidades Avançadas do Sistema ARCA v3.0

## Visão Geral

Este documento descreve as novas funcionalidades avançadas implementadas no Sistema ARCA, expandindo significativamente as capacidades de análise além do Feng Shui tradicional (BaZi e Kua).

---

## Módulos Implementados

### 1. **Geobiologia** (`geobiology_analyzer.py`)

Análise completa de aspectos geobiológicos do terreno e edificação.

**Funcionalidades:**
- Cálculo de Grade Hartmann (2m x 2.5m)
- Cálculo de Grade Curry (diagonal, ~3.5m)
- Detecção de veios de água subterrâneos
- Identificação de falhas geológicas
- Mapeamento de zonas geopatogênicas
- Análise de radiação natural do solo
- Avaliação de risco de radônio

**Endpoint da API:**
```
POST /api/advanced/geobiology/analyze
```

**Payload:**
```json
{
  "latitude": -22.5264,
  "longitude": -41.9456,
  "area_width": 15.0,
  "area_height": 20.0,
  "soil_type": "clay"
}
```

**Retorno:**
- Dados das grades Hartmann e Curry
- Zonas geopatogênicas identificadas
- Score de saúde geobiológica (0-100)
- Recomendações de correção

---

### 2. **Campos Eletromagnéticos - EMF** (`emf_analyzer.py`)

Análise de exposição a campos eletromagnéticos de fontes externas e internas.

**Funcionalidades:**
- Detecção de torres de celular próximas
- Identificação de linhas de transmissão de energia
- Localização de transformadores
- Análise de fontes internas (eletrodomésticos)
- Cálculo de exposição total em microTesla (μT)
- Avaliação de conformidade com limites de segurança

**Endpoint da API:**
```
POST /api/advanced/emf/analyze
```

**Payload:**
```json
{
  "latitude": -22.5264,
  "longitude": -41.9456,
  "include_internal": true
}
```

**Retorno:**
- Exposição total (μT)
- Fontes externas detectadas
- Fontes internas analisadas
- Score de saúde EMF (0-100)
- Status de conformidade

**Limites de Segurança:**
- Residencial: 0.4 μT (ICNIRP)
- Ambiente de trabalho: 1.0 μT

---

### 3. **Linhas Ley e Geografia Sagrada** (`leyline_analyzer.py`)

Análise de alinhamentos energéticos, sítios sagrados e vórtices de energia.

**Funcionalidades:**
- Identificação de sítios sagrados próximos
- Detecção de linhas ley (alinhamentos geométricos)
- Localização de vórtices energéticos
- Análise de alinhamentos astronômicos
- Cálculo de azimutes solares (solstícios e equinócios)
- Recomendações de orientação da edificação

**Endpoint da API:**
```
POST /api/advanced/leylines/analyze
```

**Payload:**
```json
{
  "latitude": -22.5264,
  "longitude": -41.9456,
  "radius_km": 50.0
}
```

**Retorno:**
- Sítios sagrados encontrados
- Linhas ley identificadas
- Vórtices energéticos
- Alinhamentos astronômicos
- Score de potencial energético (0-100)

---

### 4. **Geometria Sagrada** (`sacred_geometry_analyzer.py`)

Análise de proporções matemáticas sagradas e padrões geométricos.

**Funcionalidades:**
- Verificação de Proporção Áurea (Phi = 1.618)
- Análise de Proporção de Prata (2.414)
- Análise de Proporção de Bronze (3.303)
- Identificação de padrões sagrados (Flor da Vida, Vesica Piscis, etc.)
- Análise de Sequência de Fibonacci
- Avaliação de Sólidos Platônicos
- Cálculo de proporções ideais para espaços

**Endpoint da API:**
```
POST /api/advanced/sacred_geometry/analyze
```

**Payload:**
```json
{
  "floor_plan_data": {
    "overall_dimensions": {
      "width": 15.0,
      "height": 24.27
    },
    "rooms": [...]
  }
}
```

**Retorno:**
- Análise de proporções
- Padrões sagrados identificados
- Análise de Fibonacci
- Score de harmonia (0-100)
- Recomendações de ajuste

**Proporções Analisadas:**
- Phi (1.618) - Proporção Áurea
- √2 (1.414) - Proporção Pitagórica
- √3 (1.732) - Proporção Sagrada
- √5 (2.236) - Proporção de Fibonacci

---

### 5. **Arquitetura Sagrada** (`sacred_architecture_analyzer.py`)

Análise de princípios de arquitetura sagrada aplicados à edificação.

**Funcionalidades:**
- Análise de proporções espaciais
- Avaliação de materiais de construção
- Identificação de espaços sagrados
- Análise de integração astronômica
- Avaliação de fluxo de circulação
- Análise de simetria e equilíbrio
- Recomendações de pé-direito ideal

**Endpoint da API:**
```
POST /api/advanced/sacred_architecture/analyze
```

**Payload:**
```json
{
  "building_data": {
    "latitude": -22.5264,
    "longitude": -41.9456,
    "orientation": "north",
    "floor_plan": {...},
    "materials": [...]
  }
}
```

**Retorno:**
- Análise de ambientes
- Avaliação de materiais
- Espaços sagrados identificados
- Integração astronômica
- Score de arquitetura sagrada (0-100)

**Materiais Analisados:**
- Madeira (Wood) - Elemento Madeira
- Pedra (Stone) - Elemento Terra
- Granito (Granite) - Alta condutividade energética
- Mármore (Marble) - Pureza e elegância
- Bambu (Bamboo) - Sustentabilidade máxima
- Cobre (Copper) - Condutividade elétrica
- Vidro (Glass) - Transparência e luz

---

## Modelos de Banco de Dados

Novos modelos adicionados em `models.py`:

1. **GeobiologyAnalysis** - Análises geobiológicas
2. **EMFAnalysis** - Análises de EMF
3. **LeyLineAnalysis** - Análises de linhas ley
4. **SacredGeometryAnalysis** - Análises de geometria sagrada
5. **SacredArchitectureAnalysis** - Análises de arquitetura sagrada
6. **IntegratedAnalysis** - Análises integradas de todas as funcionalidades

---

## Endpoints da API

Todos os endpoints estão sob o prefixo `/api/advanced/`:

### Geobiologia
- `POST /api/advanced/geobiology/analyze` - Realizar análise
- `GET /api/advanced/geobiology/analyses` - Listar todas
- `GET /api/advanced/geobiology/analyses/{id}` - Obter específica

### EMF
- `POST /api/advanced/emf/analyze` - Realizar análise
- `GET /api/advanced/emf/analyses` - Listar todas
- `GET /api/advanced/emf/analyses/{id}` - Obter específica

### Linhas Ley
- `POST /api/advanced/leylines/analyze` - Realizar análise
- `GET /api/advanced/leylines/analyses` - Listar todas
- `GET /api/advanced/leylines/analyses/{id}` - Obter específica

### Geometria Sagrada
- `POST /api/advanced/sacred_geometry/analyze` - Realizar análise
- `GET /api/advanced/sacred_geometry/analyses` - Listar todas
- `GET /api/advanced/sacred_geometry/analyses/{id}` - Obter específica

### Arquitetura Sagrada
- `POST /api/advanced/sacred_architecture/analyze` - Realizar análise
- `GET /api/advanced/sacred_architecture/analyses` - Listar todas
- `GET /api/advanced/sacred_architecture/analyses/{id}` - Obter específica

### Análise Integrada
- `POST /api/advanced/integrated/analyze` - Criar análise integrada
- `GET /api/advanced/integrated/analyses` - Listar todas
- `GET /api/advanced/integrated/analyses/{id}` - Obter específica

---

## Componentes Frontend

Componentes React criados em `/arca-frontend/src/components/`:

1. **GeobiologyPanel.jsx** - Interface para análise geobiológica
2. **EMFPanel.jsx** - Interface para análise de EMF

**Componentes Pendentes:**
- LeyLinePanel.jsx
- SacredGeometryPanel.jsx
- SacredArchitecturePanel.jsx
- IntegratedDashboard.jsx

---

## Testes

Script de teste completo: `test_advanced_features.py`

**Executar testes:**
```bash
cd /home/ubuntu/arca-app
python3.11 test_advanced_features.py
```

**Resultados dos Testes:**
```
✓ Geobiologia: 75/100 (Baixo risco)
✓ EMF: 0/100 (Alto risco - precisa correções)
✓ Linhas Ley: 70/100 (Potencial médio)
✓ Geometria Sagrada: 16.67/100 (Precisa melhorias)
✓ Arquitetura Sagrada: 70/100 (Boa classificação)

Score Geral Integrado: 46.33/100
```

---

## Integração com Sistema Existente

As novas funcionalidades se integram perfeitamente com o sistema existente:

1. **BaZi + Kua** (Feng Shui tradicional)
2. **Geobiologia** (Saúde do terreno)
3. **EMF** (Radiações eletromagnéticas)
4. **Linhas Ley** (Geografia sagrada)
5. **Geometria Sagrada** (Proporções matemáticas)
6. **Arquitetura Sagrada** (Princípios construtivos)

**Análise Integrada** combina todos os módulos para fornecer:
- Score geral de saúde da edificação (0-100)
- Recomendações prioritárias
- Plano de implementação
- Avaliação de risco integrada

---

## Próximos Passos

### Curto Prazo
1. ✅ Implementar módulos de backend
2. ✅ Criar endpoints da API
3. ✅ Adicionar modelos de banco de dados
4. ✅ Criar componentes frontend básicos (Geobiologia e EMF)
5. ⏳ Completar componentes frontend restantes
6. ⏳ Integrar ao App.jsx principal

### Médio Prazo
1. Visualizações avançadas (mapas interativos)
2. Geração de relatórios integrados em PDF
3. Dashboard unificado
4. Exportação de dados
5. Integração com sensores IoT reais

### Longo Prazo
1. Machine Learning para padrões
2. API pública
3. Aplicativo mobile
4. Integração com BIM (Building Information Modeling)
5. Realidade Aumentada para visualização

---

## Referências Técnicas

### Geobiologia
- Redes Hartmann e Curry
- Radiestesia científica
- Geologia aplicada

### EMF
- ICNIRP (International Commission on Non-Ionizing Radiation Protection)
- OMS (Organização Mundial da Saúde)
- IEEE Standards

### Linhas Ley
- Alfred Watkins - "The Old Straight Track"
- Geografia sagrada
- Alinhamentos megalíticos

### Geometria Sagrada
- Proporção Áurea (Phi)
- Sequência de Fibonacci
- Sólidos Platônicos
- Vesica Piscis

### Arquitetura Sagrada
- Vitrúvio - "De Architectura"
- Le Corbusier - "Modulor"
- Christopher Alexander - "A Pattern Language"

---

## Licença

Sistema ARCA - Arquitetura Consciente e Preditiva  
© 2025 Gabriel de Souza Jaccoud Cardoso  
Todos os direitos reservados.

---

**Versão:** 3.0  
**Data:** Outubro 2025  
**Autor:** Sistema ARCA


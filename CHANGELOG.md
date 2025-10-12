# Changelog - Sistema ARCA

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

---

## [3.0.0] - 2025-10-12

### 🎉 Funcionalidades Principais Adicionadas

#### Backend

**Novos Módulos de Análise:**
- `geobiology_analyzer.py` - Análise geobiológica completa
  - Redes Hartmann e Curry
  - Veios de água subterrâneos
  - Falhas geológicas
  - Zonas geopatogênicas
  - Radiação natural do solo

- `emf_analyzer.py` - Análise de campos eletromagnéticos
  - Torres de celular
  - Linhas de transmissão
  - Transformadores
  - Fontes internas (eletrodomésticos)
  - Cálculo de exposição total

- `leyline_analyzer.py` - Análise de linhas ley e geografia sagrada
  - Sítios sagrados próximos
  - Linhas ley (alinhamentos)
  - Vórtices energéticos
  - Alinhamentos astronômicos

- `sacred_geometry_analyzer.py` - Análise de geometria sagrada
  - Proporção Áurea (Phi)
  - Proporções de Prata e Bronze
  - Sequência de Fibonacci
  - Padrões sagrados
  - Sólidos Platônicos

- `sacred_architecture_analyzer.py` - Análise de arquitetura sagrada
  - Proporções espaciais
  - Materiais de construção
  - Espaços sagrados
  - Integração astronômica
  - Simetria e equilíbrio

**API:**
- `advanced_endpoints.py` - Blueprint Flask com 18 novos endpoints
  - 3 endpoints por módulo (analyze, list, get)
  - Endpoints de análise integrada

**Banco de Dados:**
- 6 novos modelos em `models.py`:
  - `GeobiologyAnalysis`
  - `EMFAnalysis`
  - `LeyLineAnalysis`
  - `SacredGeometryAnalysis`
  - `SacredArchitectureAnalysis`
  - `IntegratedAnalysis`

#### Frontend

**Novos Componentes React:**
- `GeobiologyPanel.jsx` - Interface completa para análise geobiológica
  - Formulário de entrada de dados
  - Visualização de grades Hartmann e Curry
  - Exibição de zonas geopatogênicas
  - Recomendações de correção

- `EMFPanel.jsx` - Interface completa para análise de EMF
  - Formulário de coordenadas
  - Visualização de exposição total
  - Detalhamento de fontes externas e internas
  - Indicadores de conformidade

#### Documentação

- `docs/ADVANCED_FEATURES.md` - Documentação completa das novas funcionalidades
- `docs/novas_funcionalidades.md` - Planejamento inicial
- `CHANGELOG.md` - Este arquivo

#### Testes

- `test_advanced_features.py` - Script de teste completo
  - Testes para todos os 5 módulos
  - Cálculo de score integrado
  - Relatório detalhado de resultados

### 🔧 Melhorias

- Integração completa com sistema BaZi/Kua existente
- Arquitetura modular e escalável
- API RESTful consistente
- Validação de dados robusta
- Tratamento de erros aprimorado

### 📊 Resultados dos Testes

```
Geobiologia:        75/100 (Baixo risco)
EMF:                 0/100 (Alto risco)
Linhas Ley:         70/100 (Potencial médio)
Geometria Sagrada:  16.67/100 (Precisa melhorias)
Arquitetura Sagrada: 70/100 (Boa classificação)

Score Geral Integrado: 46.33/100
```

### 🐛 Correções

- Corrigido import de `advanced_endpoints` em `app.py`
- Corrigido registro de Blueprint
- Ajustado cálculo de proporções em geometria sagrada

---

## [2.0.0] - 2025-10-11

### Adicionado

**Feng Shui Completo:**
- Análise BaZi (Quatro Pilares do Destino)
- Análise Kua (Oito Mansões)
- Análise de compatibilidade casa-pessoa
- Geração de diagramas Ba Gua
- Relatórios detalhados em Markdown

**Frontend:**
- Interface React completa
- Componentes shadcn/ui
- Gráficos com Recharts
- Tabs para diferentes análises

**Backend:**
- API Flask RESTful
- Banco de dados SQLite
- Persistência de análises
- Endpoints de analytics

### Documentação

- `README.md` - Documentação principal
- `docs/api_documentation.md` - Documentação da API
- Análises de projetos reais

---

## [1.0.0] - 2025-09-01

### Adicionado

**Funcionalidades Iniciais:**
- Upload de plantas baixas
- Análise espacial básica
- Análise energética
- Perfis de ocupantes
- Relatórios em PDF

**Infraestrutura:**
- Backend Flask
- Frontend React
- Banco de dados SQLite
- Deploy no GitHub Pages

---

## Formato

Este changelog segue o formato [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/).

### Tipos de Mudanças

- **Adicionado** para novas funcionalidades
- **Modificado** para mudanças em funcionalidades existentes
- **Descontinuado** para funcionalidades que serão removidas
- **Removido** para funcionalidades removidas
- **Corrigido** para correções de bugs
- **Segurança** para vulnerabilidades corrigidas


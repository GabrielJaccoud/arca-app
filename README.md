# ARCA - Aplicativo de Design Ambiental Holístico

Este repositório contém o código-fonte e a documentação para o aplicativo ARCA, uma plataforma de design ambiental holístico e personalizado.

## 🎯 Objetivo

O ARCA integra conhecimentos milenares como Feng Shui, BaZi, I Ching, Geobiologia e Arquitetura Sagrada com princípios da física quântica, biofísica, neurociência ambiental e inteligência artificial. Seu objetivo é co-criar ambientes que não apenas abriguem, mas nutram, inspirem e alinhem seus habitantes com suas potencialidades mais profundas e com as forças criativas do universo.

## 🚀 Status do Projeto

**MVP Concluído!** ✅

O projeto ARCA está em sua versão MVP funcional, com todas as funcionalidades principais implementadas e testadas.

## 🏗️ Arquitetura

### Backend (Flask + SQLite)
- **API RESTful** com endpoints para análise espacial, energética e de perfis
- **Banco de dados SQLite** para persistência de dados
- **Processamento de imagens** com OpenCV para análise real de plantas baixas
- **Dados geomagnéticos reais** usando World Magnetic Model
- **Geração de relatórios PDF** com fpdf2

### Frontend (React + Vite)
- **Interface moderna** com design system personalizado
- **Dashboard de analytics** com gráficos interativos (Recharts)
- **Sistema de busca e filtros** avançado
- **Exportação de dados** em múltiplos formatos
- **Design responsivo** seguindo a identidade visual ARCA

## ✨ Funcionalidades Implementadas

### 🏠 Módulo de Processamento e Análise Espacial
- ✅ Upload de plantas baixas (PDF, JPG, PNG, DWG*)
- ✅ Processamento real com OpenCV (detecção de bordas e linhas)
- ✅ Análise de dimensões e características arquitetônicas
- ✅ Superposição simulada do mapa Bagua

### ⚡ Módulo de Análise Energética e Contextual
- ✅ Dados de campo magnético terrestre reais (World Magnetic Model)
- ✅ Análise de proximidade CEM (Campos Eletromagnéticos)
- ✅ Simulação de anomalias geológicas e veios de água
- ✅ Avaliação de fluxo de Chi e "venenos" arquitetônicos

### 👥 Módulo de Cadastro e Análise de Perfis de Ocupantes
- ✅ Cadastro de proprietários/família com cálculo BaZi simulado
- ✅ Cadastro de funcionários com classificação energética
- ✅ Análise de compatibilidade com espaços

### 📊 Sistema de Analytics e Relatórios
- ✅ Dashboard com gráficos interativos
- ✅ Estatísticas de uso por período
- ✅ Geração de relatórios PDF detalhados
- ✅ Histórico completo de análises

### 🔍 Sistema de Busca e Filtros
- ✅ Busca avançada por múltiplos critérios
- ✅ Filtros por data, tipo, status, coordenadas
- ✅ Interface intuitiva com abas organizadas

### 📤 Sistema de Exportação
- ✅ Exportação em formato JSON e CSV
- ✅ Backup completo do sistema
- ✅ Download automático de arquivos

## 🌐 Links do Projeto

- **Site Principal:** https://gabrieljaccoud.github.io/arca-app/
- **Aplicação React:** [URL será atualizada após correções]
- **API Backend:** [URL será atualizada após correções]
- **Repositório GitHub:** https://github.com/GabrielJaccoud/arca-app

## 📁 Estrutura do Projeto

```
arca-app/
├── src/                    # Backend Flask
│   ├── app.py             # Aplicação principal
│   ├── models.py          # Modelos de banco de dados
│   ├── spatial_analysis.py    # Análise espacial
│   ├── energetic_analysis.py  # Análise energética
│   ├── occupant_profiles.py   # Perfis de ocupantes
│   └── report_generator.py   # Geração de relatórios
├── arca-frontend/         # Frontend React
│   ├── src/
│   │   ├── App.jsx       # Componente principal
│   │   └── App.css       # Estilos personalizados
│   └── vite.config.js    # Configuração Vite
├── docs/                  # Documentação
│   ├── api_documentation.md
│   ├── design_guide.md
│   ├── project_description.md
│   └── roadmap.md
└── index.html            # Landing page GitHub Pages
```

## 🛠️ Como Rodar o Projeto

### Pré-requisitos
- Python 3.11+
- Node.js 20+
- Git

### Backend (Flask)
```bash
cd src/
pip install flask flask-cors flask-sqlalchemy fpdf2 opencv-python pygeomag
python app.py
```

### Frontend (React)
```bash
cd arca-frontend/
npm install
npm run dev
```

### Acessar a Aplicação
- Frontend: http://localhost:5173
- Backend API: http://localhost:5001
- Documentação: Pasta `docs/`

## 📚 Documentação

- **[Descrição do Projeto](docs/project_description.md)** - Visão detalhada e objetivos
- **[Documentação da API](docs/api_documentation.md)** - Endpoints e exemplos
- **[Guia de Design](docs/design_guide.md)** - Identidade visual e padrões
- **[Roadmap](docs/roadmap.md)** - Próximas fases e melhorias

## 🔮 Próximas Fases

1. **Aprimoramento Técnico**
   - Processamento DWG real
   - APIs geográficas adicionais
   - Otimização de performance

2. **Expansão de Funcionalidades**
   - Sistema de usuários e autenticação
   - Colaboração em tempo real
   - Integração com ferramentas CAD

3. **Inteligência Artificial**
   - Recomendações automáticas
   - Análise preditiva
   - Machine Learning para padrões

## 🤝 Contribuição

Este projeto está em desenvolvimento ativo. Para contribuir:

1. Fork o repositório
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Abra um Pull Request

## 📄 Licença

Este projeto está sob licença MIT. Veja o arquivo LICENSE para mais detalhes.

## 📞 Contato

Para mais informações sobre o projeto ARCA, entre em contato através do GitHub.

---

*"Criando espaços que nutrem a alma e alinham com o cosmos"* ✨


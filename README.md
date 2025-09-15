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

### 🌟 **NOVO: Módulo Feng Shui Clássico**
- ✅ **BaZi (Quatro Pilares do Destino)**: Calculadora completa com algoritmos tradicionais
- ✅ **Kua (Ba Zhai - Oito Casas)**: Sistema de direções favoráveis e desfavoráveis
- ✅ **Análise de Compatibilidade Residencial**: Integração pessoa-casa baseada no Kua
- ✅ **Recomendações Personalizadas**: Cores, materiais, posicionamento e harmonização
- ✅ **Interface Intuitiva**: Abas dedicadas com resultados detalhados e visuais

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
│   ├── bazi_calculator.py     # 🌟 NOVO: Calculadora BaZi
│   ├── kua_calculator.py      # 🌟 NOVO: Calculadora Kua
│   └── report_generator.py   # Geração de relatórios
├── arca-frontend/         # Frontend React
│   ├── src/
│   │   ├── App.jsx       # Componente principal
│   │   ├── App.css       # Estilos personalizados
│   │   └── utils/        # 🌟 NOVO: Utilitários
│   │       ├── baziCalculator.js  # Calculadora BaZi local
│   │       └── kuaCalculator.js   # Calculadora Kua local
│   └── vite.config.js    # Configuração Vite
├── docs/                  # Documentação
│   ├── api_documentation.md
│   ├── design_guide.md
│   ├── project_description.md
│   └── roadmap.md
├── test_results.md        # 🌟 NOVO: Relatório de testes
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

## 🌟 Funcionalidades Feng Shui Clássico

### BaZi (Quatro Pilares do Destino)
O sistema ARCA implementa uma calculadora completa de BaZi baseada em algoritmos tradicionais chineses:

- **Cálculo dos Quatro Pilares**: Ano, Mês, Dia e Hora de nascimento
- **Heavenly Stems e Earthly Branches**: Caracteres chineses tradicionais
- **Análise dos Cinco Elementos**: Ciclos produtivo e destrutivo
- **Day Master**: Identificação e análise de força elemental
- **Useful God (用神)**: Determinação automática do elemento benéfico
- **Recomendações Personalizadas**: Cores, direções, estilo de vida

### Kua (Ba Zhai - Sistema das Oito Casas)
Implementação completa do sistema Ba Zhai para análise de compatibilidade residencial:

- **Número Kua**: Cálculo baseado em ano de nascimento e gênero
- **Direções Favoráveis**: Sheng Qi, Tian Yi, Nian Yan, Fu Wei
- **Direções Desfavoráveis**: Huo Hai, Wu Gui, Liu Sha, Jue Ming
- **Análise de Personalidade**: Baseada no elemento do Kua
- **Compatibilidade Residencial**: Análise da orientação da casa vs. Kua pessoal
- **Recomendações Feng Shui**: Posicionamento de móveis, cores, materiais

### Integração Prática
- **Interface Intuitiva**: Abas dedicadas no frontend React
- **Cálculos Locais**: Execução no browser sem dependência de rede
- **Resultados Detalhados**: Análises completas com recomendações específicas
- **Aplicação Arquitetônica**: Integração com análise de plantas baixas

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


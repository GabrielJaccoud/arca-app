# Notas de Pesquisa - Feng Shui Clássico

## Xuan Kong Da Gua (玄空大卦风水)

### Definição
- **Significado**: "O Misterioso Vazio dos Hexagramas"
- **Complexidade**: Parte mais desenvolvida e complexa do sistema Xuan Kong
- **Precisão**: Considera 64 direções (8x8) correspondentes aos 64 hexagramas do I Ching
- **Sequência**: Usa sequência de Shao Yong (dinastia Song ~1000 AD), não a de Confúcio

### Características Técnicas
- **Ângulos**: 5,625º para cada hexagrama (360º ÷ 64)
- **Seis Afinidades**: Alinhamentos de 0,9375º (menos de 1º)
- **Aplicação**: Orientações precisas de portas e posicionamento de objetos
- **Origem**: Inicialmente para Feng Shui Yin (mortos), depois adaptado para Yang (vivos)

## Escolas de Feng Shui

### 1. Escola das Formas e Animais (San He)
- **Foco**: Topografia (rios, montanhas, florestas)
- **Animais Sagrados**: Dragão Verde (Leste), Tigre Branco (Oeste), Fênix Vermelha (Sul), Tartaruga Negra (Norte)
- **Elementos**: Relaciona formas com Wu Xing (Cinco Elementos)

### 2. Escola da Bússola e Bagua (San Yuan)
- **Instrumento**: Bússola Luo Pan
- **Base**: I Ching e Quadrado Mágico (Lo Shu)
- **Direções**: 8 direções cardeais com aspectos da vida

### 3. Escola do Chapéu Negro
- **Adaptação**: Versão ocidental simplificada
- **Método**: Porta sempre considerada como Norte

## Bagua (Pa-Kua) - Estrutura

### 8 Direções e Aspectos
1. **Norte (1)** - Carreira/Trabalho - Água - Preto/Azul escuro
2. **Nordeste (8)** - Espiritualidade/Educação - Terra - Amarelo/Bege
3. **Leste (3)** - Família/Saúde/Ancestrais - Madeira - Verde
4. **Sudeste (4)** - Prosperidade/Riqueza - Madeira - Verde/Roxo
5. **Sul (9)** - Fama/Sucesso - Fogo - Vermelho
6. **Sudoeste (2)** - Relacionamentos - Terra - Rosa/Vermelho
7. **Oeste (7)** - Criatividade/Crianças/Clientes - Metal - Branco/Cinza
8. **Noroeste (6)** - Viagens/Ajuda/Mentores - Metal - Branco/Cinza
9. **Centro (5)** - Tao/Equilíbrio - Terra - Amarelo

### Quadrado Mágico (Lo Shu)
```
4  9  2
3  5  7  
8  1  6
```
- Soma em qualquer direção = 15
- Base para cálculos de Feng Shui
- Origem: Tartaruga do Rio Lo (2005 a.C.)

## Número Kua - Cálculo

### Fórmula para Homens
1. Somar os 2 últimos dígitos do ano de nascimento
2. Se ≥ 10, somar novamente até obter 1 dígito
3. Subtrair de 10
4. Se resultado = 5, usar Kua 2

### Fórmula para Mulheres  
1. Somar os 2 últimos dígitos do ano de nascimento
2. Se ≥ 10, somar novamente até obter 1 dígito
3. Somar 5
4. Se ≥ 10, somar novamente
5. Se resultado = 5, usar Kua 8

### Grupos Energéticos
- **Grupo Leste**: Kua 1, 3, 4, 9 (direções favoráveis: L, N, S, SE)
- **Grupo Oeste**: Kua 2, 6, 7, 8 (direções favoráveis: O, NO, SO, NE)

## Cinco Elementos (Wu Xing)

### Elementos e Características
1. **Madeira (木)** - Crescimento, flexibilidade, criatividade
2. **Fogo (火)** - Energia, paixão, transformação
3. **Terra (土)** - Estabilidade, nutrição, centro
4. **Metal (金)** - Precisão, organização, estrutura
5. **Água (水)** - Fluidez, adaptabilidade, sabedoria

### Ciclos
- **Produtivo**: Madeira → Fogo → Terra → Metal → Água → Madeira
- **Destrutivo**: Madeira → Terra → Água → Fogo → Metal → Madeira
- **Enfraquecedor**: Inverso do produtivo

## Chi (Qi) - Energia Vital

### Tipos de Chi
- **Sheng Chi**: Energia positiva e ativa
- **Sha Chi**: Energia negativa e estagnada

### Ativadores de Sheng Chi
- Espelhos, cristais, luzes, sinos
- Plantas, peixes, móbiles, fontes
- Ambiente limpo, organizado, arejado

### Geradores de Sha Chi
- Ângulos de 90º (quinas)
- Ruas retas direcionadas à casa
- Porta e janela em oposição
- Fios elétricos, colunas, postes
- Ambiente desorganizado

## I Ching - 8 Trigramas

### Trigramas e Características
1. **Chien (☰)** - Céu/Pai - Yang/Perseverança
2. **Kun (☷)** - Terra/Mãe - Yin/Modéstia  
3. **Chen (☳)** - Trovão/Filho mais velho - Mobilidade
4. **Sun (☴)** - Vento/Filha mais velha - Penetração
5. **Kan (☵)** - Água/Filho do meio - Trabalhador
6. **Li (☲)** - Fogo/Filha do meio - Brilho
7. **Ken (☶)** - Montanha/Filho mais novo - Sensibilidade
8. **Tui (☱)** - Lago/Filha mais nova - Alegria

## Implementação Técnica

### Estrutura de Dados Necessária
```json
{
  "bagua_sectors": {
    "north": {"number": 1, "element": "Water", "aspect": "Career"},
    "northeast": {"number": 8, "element": "Earth", "aspect": "Knowledge"},
    "east": {"number": 3, "element": "Wood", "aspect": "Family"},
    "southeast": {"number": 4, "element": "Wood", "aspect": "Wealth"},
    "south": {"number": 9, "element": "Fire", "aspect": "Fame"},
    "southwest": {"number": 2, "element": "Earth", "aspect": "Relationships"},
    "west": {"number": 7, "element": "Metal", "aspect": "Children"},
    "northwest": {"number": 6, "element": "Metal", "aspect": "Helpful People"},
    "center": {"number": 5, "element": "Earth", "aspect": "Health"}
  },
  "kua_calculation": {
    "male_formula": "10 - (sum_of_last_two_digits % 9)",
    "female_formula": "(5 + sum_of_last_two_digits) % 9",
    "special_cases": {"male_5": 2, "female_5": 8}
  },
  "element_cycles": {
    "productive": ["Wood", "Fire", "Earth", "Metal", "Water"],
    "destructive": ["Wood", "Earth", "Water", "Fire", "Metal"]
  }
}
```

### Algoritmos Necessários
1. **Cálculo do Número Kua**
2. **Determinação de Direções Favoráveis**
3. **Análise de Compatibilidade Elemental**
4. **Mapeamento Bagua sobre Planta Baixa**
5. **Identificação de Sha Chi e Sheng Chi**
6. **Recomendações de Curas e Melhorias**



## Geobiologia - Fundamentos

### Definição
- **Etimologia**: GEO (terra) + BIO (vida) + LOGIA (estudo)
- **Conceito**: Medicina do habitat - estudo da vida na terra (aspectos energéticos)
- **Origem**: Arte Zahorí (Geomancia Druídica) - Druídas celtas

### Campos de Estudo

#### 1. Radiações Naturais
- **Cósmicas**: Sol e astros
- **Crosta Terrestre**: Elementos radioativos
- **Telúricas**: Energias do subsolo

#### 2. Contaminações Artificiais
- **Elétricas**: Eletrodomésticos, lâmpadas, tomadas
- **Eletromagnéticas**: Torres de TV/celular/rádio
- **Químicas**: Materiais tóxicos de construção

#### 3. Redes Geobiológicas (Linhas de Força)

##### Rede Hartmann
- **Orientação**: Norte-Sul (2,0m) / Leste-Oeste (2,5m)
- **Características**: Linhas de força magnética do subsolo

##### Rede Curry  
- **Orientação**: Nordeste-Sudoeste (8,0m) / Noroeste-Sudeste (6,0m)
- **Características**: Diagonal à rede Hartmann

##### Rede Peyré
- **Espaçamento**: 7,0 a 8,0m
- **Orientação**: Mesmos eixos da Hartmann

#### 4. Ocorrências Telúricas
- **Veios d'água subterrâneos**
- **Falhas geológicas**
- **Chaminés cosmo-telúricas** (vórtices energéticos)

### Zonas Geopatogênicas
- **Definição**: Regiões que emanam radiações do subsolo
- **Ponto Estrela**: Sobreposição de 2+ focos de radiação
- **Efeito**: Intensidade energética elevada para permanência prolongada

### Materiais Construtivos Problemáticos

#### 6 Tipos a Evitar
1. **Metálicos** (alta absorção eletromagnética)
2. **PVC** (contém chumbo - metal pesado)
3. **Amianto** (material cancerígeno)
4. **Materiais radioativos** (algumas rochas)
5. **COVs** (Compostos Orgânicos Voláteis)
6. **Eucalipto autoclavado** (processo tóxico)

### Efeitos na Saúde Humana

#### Campos Eletromagnéticos
- Mudanças na temperatura corporal
- Alteração nos eletrólitos do sangue
- Dor muscular e articular
- Fadiga e falta de apetite
- Influência no sistema nervoso central
- Estresse
- Diminuição de plaquetas

#### Medidas Preventivas
- **Distância mínima**: 150m de linhas de alta tensão
- **Aparelhos**: 1m de distância (micro-ondas, TV, roteadores)
- **Quarto**: Desconectar aparelhos elétricos à noite
- **Cabeceira**: 70cm mínimo de aparelhos conectados
- **Aterramento**: Andar descalço na grama úmida (5 min/dia)

### Tempestades Solares
- **Ciclo**: 11 anos (inversão dos polos magnéticos)
- **Efeitos**: Interferência em eletrônicos, mudanças meteorológicas
- **Impacto humano**: Alterações físicas e emocionais (corpo 70% água)

## Integração Feng Shui + Geobiologia

### Princípios Comuns
- **6 Elementos**: Terra, Fogo, Ar, Água, Metal, Madeira
- **Energia Sha**: Locais com memória negativa (hospitais, cemitérios)
- **Equilíbrio Elemental**: Harmonização através de materiais e objetos

### Aplicações Práticas
- **Aquário**: Exemplo de equilíbrio (água + plantas + pedras + peixes + areia)
- **Cristais**: Limpeza ambiental e energética
- **Madeira**: Filtra radiações (oposto ao metal que absorve)

### Cristais Recomendados
- **Ágata Azul**: Comunicação e alegria
- **Ametista**: Sabedoria e humildade, alivia tensões mentais
- **Esmeralda**: Amor, clareza mental, força para desafios

## Implementação no ARCA

### Dados Geobiológicos Necessários
```json
{
  "geobiological_analysis": {
    "hartmann_grid": {
      "north_south_spacing": 2.0,
      "east_west_spacing": 2.5,
      "unit": "meters"
    },
    "curry_grid": {
      "northeast_southwest_spacing": 8.0,
      "northwest_southeast_spacing": 6.0,
      "unit": "meters"
    },
    "telluric_features": {
      "underground_water_veins": [],
      "geological_faults": [],
      "cosmo_telluric_chimneys": []
    },
    "electromagnetic_sources": {
      "external": ["cell_towers", "power_lines", "radio_antennas"],
      "internal": ["appliances", "electrical_wiring", "wifi_routers"]
    },
    "construction_materials": {
      "avoid": ["metallic", "pvc", "asbestos", "radioactive", "covs", "treated_eucalyptus"],
      "recommended": ["natural_wood", "clay", "stone", "bamboo"]
    }
  }
}
```

### Algoritmos de Análise
1. **Detecção de Zonas Geopatogênicas**
2. **Mapeamento de Redes Geobiológicas**
3. **Análise de Fontes Eletromagnéticas**
4. **Avaliação de Materiais Construtivos**
5. **Recomendações de Proteção e Harmonização**
6. **Integração com Análise Feng Shui**


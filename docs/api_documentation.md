# Documentação da API ARCA

## Visão Geral

A API do ARCA fornece endpoints para análise espacial, energética e de perfis de ocupantes para design ambiental holístico.

**Base URL:** `https://5000-i4jzvyj6hn9qmdbabo0f4-393f986f.manusvm.computer`

## Endpoints

### 1. Upload de Planta Baixa

**POST** `/upload_floor_plan`

Processa um arquivo de planta baixa para extrair informações espaciais.

**Parâmetros:**
- `file` (multipart/form-data): Arquivo da planta baixa (PDF, DWG, JPG, PNG)

**Resposta de Sucesso:**
```json
{
  "status": "success",
  "message": "Planta baixa processada com sucesso",
  "details": {
    "file_type": "pdf",
    "size_bytes": 1024,
    "simulated_elements": {
      "dimensions_identified": true,
      "doors_windows_identified": true,
      "rooms_identified": true,
      "geometric_shapes_identified": true
    },
    "simulated_geolocation": {
      "orientation_determined": true,
      "coordinates_obtained": true
    },
    "simulated_bagua_superposition": true
  }
}
```

### 2. Análise Energética

**POST** `/analyze_energetics`

Realiza análise energética e contextual baseada em dados geográficos.

**Parâmetros (JSON):**
```json
{
  "latitude": -23.55052,
  "longitude": -46.633309,
  "floor_plan_data": {} // Dados opcionais da planta baixa
}
```

**Resposta de Sucesso:**
```json
{
  "status": "success",
  "geographical_analysis": {
    "status": "success",
    "data": {
      "latitude": -23.55052,
      "longitude": -46.633309,
      "cem_proximity": "low",
      "geological_anomalies": "none",
      "nearby_water_veins": false
    }
  },
  "chi_flow_analysis": {
    "status": "success",
    "assessment": {
      "obstructed_areas": ["hallway_entrance"],
      "long_corridors": true,
      "central_open_spaces": true
    }
  },
  "architectural_poisons": {
    "status": "success",
    "poisons": ["sharp_corner_to_resting_area_simulated"]
  },
  "sample_material_info": {
    "status": "success",
    "data": {
      "conductivity": "low",
      "density": "medium",
      "origin": "natural",
      "impact": "positive"
    }
  }
}
```

### 3. Registro de Ocupante

**POST** `/register_occupant`

Registra um perfil de ocupante (proprietário/família ou funcionário).

**Parâmetros para Proprietário/Família (JSON):**
```json
{
  "type": "owner_family",
  "name": "João Silva",
  "dob": "1980-05-15",
  "tob": "10:30",
  "pob": "São Paulo, Brasil"
}
```

**Parâmetros para Funcionário (JSON):**
```json
{
  "type": "employee",
  "name": "Maria Santos",
  "function": "Gerente"
}
```

**Resposta de Sucesso:**
```json
{
  "status": "success",
  "message": "Perfil de ocupante registrado com sucesso",
  "profile": {
    "name": "João Silva",
    "type": "owner_family",
    "bazi_profile": {
      "status": "success",
      "profile": {
        "master_element": "Wood",
        "element_balance": "balanced",
        "elemental_needs": ["Fire", "Earth"]
      },
      "details": {
        "name": "João Silva",
        "birth_datetime": "1980-05-15 10:30:00",
        "pob": "São Paulo, Brasil"
      }
    }
  }
}
```

## Códigos de Status

- `200` - Sucesso
- `400` - Erro de requisição (parâmetros inválidos)
- `405` - Método não permitido
- `500` - Erro interno do servidor

## Notas de Implementação

Esta é uma versão MVP com funcionalidades simuladas para demonstração. Em produção, os seguintes recursos seriam implementados:

1. **Processamento Real de Imagens:** Algoritmos de visão computacional para análise de plantas baixas
2. **APIs Geográficas Reais:** Integração com OpenCellID, dados geológicos e APIs de mapeamento
3. **Cálculo BaZi Completo:** Algoritmos completos de astrologia chinesa
4. **Banco de Dados:** Persistência de dados de usuários, projetos e análises
5. **Autenticação:** Sistema de login e autorização
6. **Cache:** Sistema de cache para otimização de performance



## Novos Endpoints - Busca e Filtros

### 4. Busca de Plantas Baixas

**GET** `/search/floor_plans`

Busca plantas baixas com filtros opcionais.

**Parâmetros de Query:**
- `filename` (string, opcional): Nome do arquivo para busca parcial
- `status` (string, opcional): Status da análise ("success", "error")
- `date_from` (string, opcional): Data inicial no formato YYYY-MM-DD
- `date_to` (string, opcional): Data final no formato YYYY-MM-DD

**Exemplo:**
```
GET /search/floor_plans?filename=casa&status=success&date_from=2024-01-01
```

**Resposta:**
```json
[
  {
    "id": 1,
    "filename": "casa_exemplo.pdf",
    "upload_date": "2024-08-25T10:30:00",
    "analysis_results": {
      "status": "success",
      "message": "Processamento concluído"
    }
  }
]
```

### 5. Busca de Análises Energéticas

**GET** `/search/energetic_analyses`

Busca análises energéticas com filtros geográficos e temporais.

**Parâmetros de Query:**
- `cem_proximity` (string, opcional): Proximidade CEM ("low", "medium", "high")
- `geological_anomalies` (string, opcional): Tipo de anomalias ("none", "minor", "moderate", "significant")
- `date_from` (string, opcional): Data inicial no formato YYYY-MM-DD
- `date_to` (string, opcional): Data final no formato YYYY-MM-DD
- `latitude_min` (float, opcional): Latitude mínima
- `latitude_max` (float, opcional): Latitude máxima
- `longitude_min` (float, opcional): Longitude mínima
- `longitude_max` (float, opcional): Longitude máxima

**Exemplo:**
```
GET /search/energetic_analyses?cem_proximity=low&latitude_min=-24&latitude_max=-23
```

### 6. Busca de Perfis de Ocupantes

**GET** `/search/occupant_profiles`

Busca perfis de ocupantes com filtros por tipo e características.

**Parâmetros de Query:**
- `name` (string, opcional): Nome para busca parcial
- `profile_type` (string, opcional): Tipo ("owner_family", "employee")
- `date_from` (string, opcional): Data inicial no formato YYYY-MM-DD
- `date_to` (string, opcional): Data final no formato YYYY-MM-DD
- `bazi_element` (string, opcional): Elemento BaZi ("Wood", "Fire", "Earth", "Metal", "Water")
- `function_energy` (string, opcional): Energia da função ("creative", "analytical", "leadership", "supportive")

## Endpoints de Exportação

### 7. Exportar Plantas Baixas

**GET** `/export/floor_plans`

Exporta dados de plantas baixas em formato JSON ou CSV.

**Parâmetros de Query:**
- `format` (string, opcional): Formato de exportação ("json" ou "csv", padrão: "json")

**Resposta:** Download automático do arquivo

### 8. Exportar Análises Energéticas

**GET** `/export/energetic_analyses`

Exporta dados de análises energéticas em formato JSON ou CSV.

**Parâmetros de Query:**
- `format` (string, opcional): Formato de exportação ("json" ou "csv", padrão: "json")

### 9. Exportar Perfis de Ocupantes

**GET** `/export/occupant_profiles`

Exporta dados de perfis de ocupantes em formato JSON ou CSV.

**Parâmetros de Query:**
- `format` (string, opcional): Formato de exportação ("json" ou "csv", padrão: "json")

### 10. Backup Completo

**GET** `/export/full_backup`

Gera um backup completo de todos os dados do sistema em formato JSON.

**Resposta:** Download automático do arquivo de backup com timestamp

## Endpoints de Analytics

### 11. Plantas Baixas por Mês

**GET** `/analytics/floor_plans_by_month`

Retorna estatísticas de uploads de plantas baixas agrupadas por mês.

**Resposta:**
```json
[
  {
    "month": "2024-08",
    "count": 5
  }
]
```

### 12. Análises Energéticas por Proximidade CEM

**GET** `/analytics/energetic_analyses_by_cem_proximity`

Retorna distribuição de análises energéticas por proximidade CEM.

**Resposta:**
```json
[
  {
    "cem_proximity": "low",
    "count": 10
  },
  {
    "cem_proximity": "medium",
    "count": 3
  }
]
```

### 13. Perfis de Ocupantes por Tipo

**GET** `/analytics/occupant_profiles_by_type`

Retorna distribuição de perfis de ocupantes por tipo.

**Resposta:**
```json
[
  {
    "profile_type": "owner_family",
    "count": 8
  },
  {
    "profile_type": "employee",
    "count": 12
  }
]
```

## Códigos de Status HTTP

- `200 OK`: Requisição bem-sucedida
- `400 Bad Request`: Parâmetros inválidos ou dados malformados
- `404 Not Found`: Recurso não encontrado
- `500 Internal Server Error`: Erro interno do servidor

## Headers de Resposta

Todos os endpoints retornam:
- `Content-Type: application/json` (para dados JSON)
- `Content-Type: text/csv` (para exportações CSV)
- `Content-Type: application/pdf` (para relatórios PDF)
- `Access-Control-Allow-Origin: *` (CORS habilitado)

## Autenticação

Atualmente, a API não requer autenticação. Em versões futuras, será implementado sistema de autenticação baseado em tokens JWT.



---

## 🌟 Novos Endpoints - Feng Shui Clássico

### 7. Cálculo BaZi (Quatro Pilares do Destino)

**POST** `/bazi/calculate`

Calcula os Quatro Pilares do Destino baseado na data e hora de nascimento.

**Parâmetros (JSON):**
```json
{
  "birth_datetime": "1985-03-20T10:15:00",
  "timezone_offset": -3
}
```

**Resposta de Sucesso:**
```json
{
  "status": "success",
  "data": {
    "year_pillar": {
      "heavenly_stem": "乙",
      "earthly_branch": "丑",
      "element": "Wood",
      "zodiac": "Ox"
    },
    "month_pillar": {
      "heavenly_stem": "己",
      "earthly_branch": "卯",
      "element": "Earth",
      "zodiac": "Rabbit"
    },
    "day_pillar": {
      "heavenly_stem": "戊",
      "earthly_branch": "戌",
      "element": "Earth",
      "zodiac": "Dog"
    },
    "hour_pillar": {
      "heavenly_stem": "丁",
      "earthly_branch": "巳",
      "element": "Fire",
      "zodiac": "Snake"
    },
    "day_master": {
      "element": "Earth",
      "strength": "Strong",
      "useful_god": "Water"
    },
    "recommendations": {
      "favorable_colors": ["blue", "black", "white"],
      "favorable_directions": ["North", "West"],
      "career_advice": "Suitable for water-related industries",
      "health_advice": "Focus on kidney and bladder health"
    }
  }
}
```

### 8. Cálculo Kua (Ba Zhai)

**POST** `/kua/calculate`

Calcula o número Kua e direções favoráveis baseado no ano de nascimento e gênero.

**Parâmetros (JSON):**
```json
{
  "birth_year": 1985,
  "gender": "male"
}
```

**Resposta de Sucesso:**
```json
{
  "status": "success",
  "data": {
    "kua_number": 7,
    "group": "West",
    "element": "Metal",
    "personality": "Communicative and charming",
    "favorable_directions": {
      "sheng_qi": "Northwest",
      "tian_yi": "West", 
      "nian_yan": "Northeast",
      "fu_wei": "Southwest"
    },
    "unfavorable_directions": {
      "huo_hai": "East",
      "wu_gui": "Southeast",
      "liu_sha": "South",
      "jue_ming": "North"
    },
    "favorable_colors": ["white", "gold", "silver"],
    "recommendations": {
      "bedroom_direction": "West or Southwest",
      "work_direction": "Northwest",
      "entrance_direction": "West group directions"
    }
  }
}
```

### 9. Análise de Compatibilidade da Casa

**POST** `/feng_shui/house_analysis`

Analisa a compatibilidade entre a orientação da casa e o Kua da pessoa.

**Parâmetros (JSON):**
```json
{
  "house_facing_direction": "West",
  "birth_year": 1985,
  "gender": "male"
}
```

**Resposta de Sucesso:**
```json
{
  "status": "success",
  "data": {
    "person_kua": 7,
    "house_direction": "West",
    "compatibility_level": "Excellent",
    "compatibility_score": 95,
    "analysis": {
      "direction_type": "Tian Yi (Health)",
      "benefits": [
        "Excellent for health and recovery",
        "Supports career advancement",
        "Promotes family harmony"
      ],
      "recommendations": [
        "Place bedroom in West or Southwest sector",
        "Position work desk facing Northwest",
        "Use white, gold, or silver colors in decoration"
      ]
    },
    "feng_shui_advice": {
      "entrance": "Keep entrance clean and well-lit",
      "living_room": "Place main seating facing favorable directions",
      "bedroom": "Position bed with head towards West or Southwest",
      "kitchen": "Avoid placing stove in unfavorable directions"
    }
  }
}
```

### 10. Análise Completa BaZi + Kua

**POST** `/bazi_kua/complete_analysis`

Realiza análise integrada combinando BaZi e Kua para recomendações holísticas.

**Parâmetros (JSON):**
```json
{
  "birth_datetime": "1985-03-20T10:15:00",
  "birth_year": 1985,
  "gender": "male",
  "timezone_offset": -3
}
```

**Resposta de Sucesso:**
```json
{
  "status": "success",
  "data": {
    "bazi": {
      "day_master": "Earth",
      "useful_god": "Water",
      "strength": "Strong"
    },
    "kua": {
      "number": 7,
      "group": "West",
      "element": "Metal"
    },
    "integrated_analysis": {
      "element_harmony": "Excellent - Metal supports Water",
      "overall_compatibility": "Very Good",
      "life_recommendations": {
        "career": "Water or Metal industries recommended",
        "health": "Focus on respiratory and kidney systems",
        "relationships": "Compatible with Water and Earth people",
        "living_space": "West-facing homes with water features"
      }
    },
    "architectural_recommendations": {
      "room_layout": "Master bedroom in West sector",
      "color_scheme": "Blue, white, and metallic tones",
      "materials": "Metal fixtures, water features, earth tones",
      "lighting": "Soft, warm lighting in West areas"
    }
  }
}
```

## Códigos de Erro Específicos

### BaZi/Kua Endpoints
- `400`: Parâmetros inválidos (data/ano/gênero)
- `422`: Data de nascimento fora do range suportado
- `500`: Erro interno no cálculo

### Exemplos de Erro
```json
{
  "status": "error",
  "message": "Invalid birth year. Must be between 1900 and 2100",
  "error_code": "INVALID_BIRTH_YEAR"
}
```

## Notas de Implementação

### Algoritmos Tradicionais
- **BaZi**: Baseado no calendário chinês tradicional com cálculos de Heavenly Stems e Earthly Branches
- **Kua**: Implementação do sistema Ba Zhai (Oito Casas) com fórmulas tradicionais
- **Compatibilidade**: Análise integrada considerando ambos os sistemas

### Performance
- **Cálculos Locais**: Implementação também disponível no frontend para resposta instantânea
- **Cache**: Resultados podem ser cacheados para consultas repetidas
- **Validação**: Validação rigorosa de parâmetros de entrada

### Precisão
- **Calendário**: Conversão precisa entre calendário gregoriano e chinês
- **Fuso Horário**: Suporte completo a diferentes fusos horários
- **Tradições**: Algoritmos baseados em textos clássicos de Feng Shui


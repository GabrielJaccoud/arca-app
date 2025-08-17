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


import React, { useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Button } from '@/components/ui/button.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Label } from '@/components/ui/label.jsx'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select.jsx'
import { MapPin, Waves, AlertTriangle, CheckCircle2, XCircle } from 'lucide-react'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

const API_BASE_URL = 'https://5007-i4jzvyj6hn9qmdbabo0f4-393f986f.manusvm.computer'

export function GeobiologyPanel() {
  const [formData, setFormData] = useState({
    latitude: '',
    longitude: '',
    areaWidth: '',
    areaHeight: '',
    soilType: 'unknown'
  })
  
  const [analysis, setAnalysis] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleAnalyze = async () => {
    setLoading(true)
    setError(null)
    
    try {
      const response = await fetch(`${API_BASE_URL}/api/advanced/geobiology/analyze`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          latitude: parseFloat(formData.latitude),
          longitude: parseFloat(formData.longitude),
          area_width: parseFloat(formData.areaWidth),
          area_height: parseFloat(formData.areaHeight),
          soil_type: formData.soilType
        })
      })
      
      const data = await response.json()
      
      if (data.status === 'success') {
        setAnalysis(data.analysis)
      } else {
        setError(data.message)
      }
    } catch (err) {
      setError('Erro ao realizar análise geobiológica: ' + err.message)
    } finally {
      setLoading(false)
    }
  }

  const getRiskColor = (risk) => {
    switch(risk) {
      case 'low': return 'text-green-600'
      case 'medium': return 'text-yellow-600'
      case 'high': return 'text-red-600'
      default: return 'text-gray-600'
    }
  }

  const getRiskIcon = (risk) => {
    switch(risk) {
      case 'low': return <CheckCircle2 className="h-5 w-5 text-green-600" />
      case 'medium': return <AlertTriangle className="h-5 w-5 text-yellow-600" />
      case 'high': return <XCircle className="h-5 w-5 text-red-600" />
      default: return null
    }
  }

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Waves className="h-6 w-6" />
            Análise Geobiológica
          </CardTitle>
          <CardDescription>
            Análise de redes Hartmann e Curry, veios de água, falhas geológicas e zonas geopatogênicas
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="geo-latitude">Latitude</Label>
              <Input
                id="geo-latitude"
                type="number"
                step="0.0001"
                placeholder="-22.5264"
                value={formData.latitude}
                onChange={(e) => setFormData({...formData, latitude: e.target.value})}
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="geo-longitude">Longitude</Label>
              <Input
                id="geo-longitude"
                type="number"
                step="0.0001"
                placeholder="-41.9456"
                value={formData.longitude}
                onChange={(e) => setFormData({...formData, longitude: e.target.value})}
              />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="geo-width">Largura da Área (m)</Label>
              <Input
                id="geo-width"
                type="number"
                step="0.1"
                placeholder="15.0"
                value={formData.areaWidth}
                onChange={(e) => setFormData({...formData, areaWidth: e.target.value})}
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="geo-height">Altura da Área (m)</Label>
              <Input
                id="geo-height"
                type="number"
                step="0.1"
                placeholder="20.0"
                value={formData.areaHeight}
                onChange={(e) => setFormData({...formData, areaHeight: e.target.value})}
              />
            </div>
          </div>

          <div className="space-y-2">
            <Label htmlFor="geo-soil">Tipo de Solo</Label>
            <Select value={formData.soilType} onValueChange={(value) => setFormData({...formData, soilType: value})}>
              <SelectTrigger id="geo-soil">
                <SelectValue placeholder="Selecione o tipo de solo" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="unknown">Desconhecido</SelectItem>
                <SelectItem value="granite">Granito</SelectItem>
                <SelectItem value="limestone">Calcário</SelectItem>
                <SelectItem value="clay">Argila</SelectItem>
                <SelectItem value="sand">Areia</SelectItem>
                <SelectItem value="volcanic">Vulcânico</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <Button onClick={handleAnalyze} disabled={loading} className="w-full">
            {loading ? 'Analisando...' : 'Analisar Geobiologia'}
          </Button>

          {error && (
            <div className="p-4 bg-red-50 border border-red-200 rounded-md text-red-800">
              {error}
            </div>
          )}
        </CardContent>
      </Card>

      {analysis && (
        <>
          {/* Score Geral */}
          <Card>
            <CardHeader>
              <CardTitle>Avaliação Geral</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-3 gap-4">
                <div className="text-center p-4 bg-blue-50 rounded-lg">
                  <div className="text-3xl font-bold text-blue-600">
                    {analysis.overall_assessment.geobiological_health_score}
                  </div>
                  <div className="text-sm text-gray-600 mt-1">Score de Saúde</div>
                </div>
                <div className="text-center p-4 bg-gray-50 rounded-lg">
                  <div className="flex items-center justify-center gap-2">
                    {getRiskIcon(analysis.overall_assessment.risk_level)}
                    <span className={`text-lg font-semibold ${getRiskColor(analysis.overall_assessment.risk_level)}`}>
                      {analysis.overall_assessment.risk_level.toUpperCase()}
                    </span>
                  </div>
                  <div className="text-sm text-gray-600 mt-1">Nível de Risco</div>
                </div>
                <div className="text-center p-4 bg-green-50 rounded-lg">
                  <div className="text-lg font-semibold text-green-600">
                    {analysis.overall_assessment.suitable_for_habitation ? 'SIM' : 'NÃO'}
                  </div>
                  <div className="text-sm text-gray-600 mt-1">Adequado para Habitação</div>
                </div>
              </div>

              {analysis.overall_assessment.main_concerns && analysis.overall_assessment.main_concerns.length > 0 && (
                <div className="mt-4 p-4 bg-yellow-50 border border-yellow-200 rounded-md">
                  <h4 className="font-semibold text-yellow-800 mb-2">Principais Preocupações:</h4>
                  <ul className="list-disc list-inside space-y-1 text-yellow-700">
                    {analysis.overall_assessment.main_concerns.map((concern, idx) => (
                      <li key={idx}>{concern}</li>
                    ))}
                  </ul>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Grades Hartmann e Curry */}
          <div className="grid grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle className="text-lg">Grade Hartmann</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <div className="flex justify-between">
                    <span className="text-sm text-gray-600">Espaçamento N-S:</span>
                    <span className="font-semibold">{analysis.hartmann_grid.spacing_ns}m</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm text-gray-600">Espaçamento L-O:</span>
                    <span className="font-semibold">{analysis.hartmann_grid.spacing_ew}m</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm text-gray-600">Total de Cruzamentos:</span>
                    <span className="font-semibold text-blue-600">{analysis.hartmann_grid.total_crossings}</span>
                  </div>
                  <div className="mt-4 p-3 bg-blue-50 rounded-md text-sm text-blue-800">
                    Evitar permanência prolongada nos cruzamentos da grade Hartmann
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="text-lg">Grade Curry</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <div className="flex justify-between">
                    <span className="text-sm text-gray-600">Espaçamento:</span>
                    <span className="font-semibold">{analysis.curry_grid.spacing}m</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm text-gray-600">Rotação:</span>
                    <span className="font-semibold">{analysis.curry_grid.rotation}°</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm text-gray-600">Total de Cruzamentos:</span>
                    <span className="font-semibold text-purple-600">{analysis.curry_grid.total_crossings}</span>
                  </div>
                  <div className="mt-4 p-3 bg-purple-50 rounded-md text-sm text-purple-800">
                    Cruzamentos Curry têm maior intensidade - evitar camas e mesas de trabalho
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Zonas Geopatogênicas */}
          <Card>
            <CardHeader>
              <CardTitle>Zonas Geopatogênicas</CardTitle>
              <CardDescription>
                Áreas de risco identificadas (cruzamentos de grades, veios de água, falhas)
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-4 gap-4 mb-4">
                <div className="text-center p-3 bg-red-50 rounded-lg">
                  <div className="text-2xl font-bold text-red-600">
                    {analysis.geopathogenic_zones.total_geopathogenic_zones}
                  </div>
                  <div className="text-xs text-gray-600 mt-1">Zonas de Alto Risco</div>
                </div>
                <div className="text-center p-3 bg-blue-50 rounded-lg">
                  <div className="text-2xl font-bold text-blue-600">
                    {analysis.geopathogenic_zones.hartmann_crossings}
                  </div>
                  <div className="text-xs text-gray-600 mt-1">Cruzamentos Hartmann</div>
                </div>
                <div className="text-center p-3 bg-purple-50 rounded-lg">
                  <div className="text-2xl font-bold text-purple-600">
                    {analysis.geopathogenic_zones.curry_crossings}
                  </div>
                  <div className="text-xs text-gray-600 mt-1">Cruzamentos Curry</div>
                </div>
                <div className="text-center p-3 bg-cyan-50 rounded-lg">
                  <div className="text-2xl font-bold text-cyan-600">
                    {analysis.geopathogenic_zones.water_veins}
                  </div>
                  <div className="text-xs text-gray-600 mt-1">Veios de Água</div>
                </div>
              </div>

              {analysis.geopathogenic_zones.recommendations && (
                <div className="mt-4 p-4 bg-green-50 border border-green-200 rounded-md">
                  <h4 className="font-semibold text-green-800 mb-2">Recomendações:</h4>
                  <ul className="list-disc list-inside space-y-1 text-green-700 text-sm">
                    {analysis.geopathogenic_zones.recommendations.map((rec, idx) => (
                      <li key={idx}>{rec}</li>
                    ))}
                  </ul>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Radiação do Solo */}
          <Card>
            <CardHeader>
              <CardTitle>Radiação Natural do Solo</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-3 gap-4">
                <div>
                  <div className="text-sm text-gray-600">Tipo de Solo</div>
                  <div className="text-lg font-semibold capitalize">{analysis.soil_radiation.soil_type}</div>
                </div>
                <div>
                  <div className="text-sm text-gray-600">Nível de Radiação</div>
                  <div className={`text-lg font-semibold ${getRiskColor(analysis.soil_radiation.radiation_level)}`}>
                    {analysis.soil_radiation.radiation_level.toUpperCase()}
                  </div>
                </div>
                <div>
                  <div className="text-sm text-gray-600">Risco de Radônio</div>
                  <div className={`text-lg font-semibold ${getRiskColor(analysis.soil_radiation.radon_risk)}`}>
                    {analysis.soil_radiation.radon_risk.toUpperCase()}
                  </div>
                </div>
              </div>

              <div className="mt-4 p-3 bg-gray-50 rounded-md">
                <div className="text-sm text-gray-600">Valor de Radiação</div>
                <div className="text-2xl font-bold text-gray-800">
                  {analysis.soil_radiation.radiation_value_bq_m3} Bq/m³
                </div>
              </div>

              {analysis.soil_radiation.recommendations && (
                <div className="mt-4 p-4 bg-blue-50 border border-blue-200 rounded-md">
                  <h4 className="font-semibold text-blue-800 mb-2">Recomendações:</h4>
                  <ul className="list-disc list-inside space-y-1 text-blue-700 text-sm">
                    {analysis.soil_radiation.recommendations.map((rec, idx) => (
                      <li key={idx}>{rec}</li>
                    ))}
                  </ul>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Ações Prioritárias */}
          {analysis.overall_assessment.priority_actions && (
            <Card>
              <CardHeader>
                <CardTitle>Ações Prioritárias</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  {analysis.overall_assessment.priority_actions.map((action, idx) => (
                    <div key={idx} className="flex items-start gap-3 p-3 bg-orange-50 border border-orange-200 rounded-md">
                      <AlertTriangle className="h-5 w-5 text-orange-600 mt-0.5 flex-shrink-0" />
                      <span className="text-sm text-orange-800">{action}</span>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}
        </>
      )}
    </div>
  )
}


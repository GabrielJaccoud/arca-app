import React, { useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Button } from '@/components/ui/button.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Label } from '@/components/ui/label.jsx'
import { Radio, Zap, AlertTriangle, CheckCircle2, XCircle, Wifi, Tower } from 'lucide-react'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts'

const API_BASE_URL = 'https://5007-i4jzvyj6hn9qmdbabo0f4-393f986f.manusvm.computer'

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8']

export function EMFPanel() {
  const [formData, setFormData] = useState({
    latitude: '',
    longitude: ''
  })
  
  const [analysis, setAnalysis] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleAnalyze = async () => {
    setLoading(true)
    setError(null)
    
    try {
      const response = await fetch(`${API_BASE_URL}/api/advanced/emf/analyze`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          latitude: parseFloat(formData.latitude),
          longitude: parseFloat(formData.longitude),
          include_internal: true
        })
      })
      
      const data = await response.json()
      
      if (data.status === 'success') {
        setAnalysis(data.analysis)
      } else {
        setError(data.message)
      }
    } catch (err) {
      setError('Erro ao realizar análise de EMF: ' + err.message)
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

  const getRiskBgColor = (risk) => {
    switch(risk) {
      case 'low': return 'bg-green-50 border-green-200'
      case 'medium': return 'bg-yellow-50 border-yellow-200'
      case 'high': return 'bg-red-50 border-red-200'
      default: return 'bg-gray-50 border-gray-200'
    }
  }

  const getSafetyIcon = (status) => {
    switch(status) {
      case 'safe': return <CheckCircle2 className="h-5 w-5 text-green-600" />
      case 'caution': return <AlertTriangle className="h-5 w-5 text-yellow-600" />
      case 'unsafe': return <XCircle className="h-5 w-5 text-red-600" />
      default: return null
    }
  }

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Zap className="h-6 w-6" />
            Análise de Campos Eletromagnéticos (EMF)
          </CardTitle>
          <CardDescription>
            Análise de torres de celular, linhas de transmissão, transformadores e fontes internas de EMF
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="emf-latitude">Latitude</Label>
              <Input
                id="emf-latitude"
                type="number"
                step="0.0001"
                placeholder="-22.5264"
                value={formData.latitude}
                onChange={(e) => setFormData({...formData, latitude: e.target.value})}
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="emf-longitude">Longitude</Label>
              <Input
                id="emf-longitude"
                type="number"
                step="0.0001"
                placeholder="-41.9456"
                value={formData.longitude}
                onChange={(e) => setFormData({...formData, longitude: e.target.value})}
              />
            </div>
          </div>

          <Button onClick={handleAnalyze} disabled={loading} className="w-full">
            {loading ? 'Analisando...' : 'Analisar EMF'}
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
          {/* Exposição Total */}
          <Card>
            <CardHeader>
              <CardTitle>Exposição Total a EMF</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 gap-6 mb-6">
                <div className="text-center p-6 bg-gradient-to-br from-blue-50 to-blue-100 rounded-lg">
                  <div className="text-4xl font-bold text-blue-600">
                    {analysis.total_exposure.total_exposure_uT.toFixed(4)}
                  </div>
                  <div className="text-sm text-gray-600 mt-2">Exposição Total (μT)</div>
                </div>
                <div className="text-center p-6 bg-gradient-to-br from-gray-50 to-gray-100 rounded-lg">
                  <div className="text-4xl font-bold text-gray-600">
                    {analysis.total_exposure.safe_limit_residential_uT}
                  </div>
                  <div className="text-sm text-gray-600 mt-2">Limite Seguro (μT)</div>
                </div>
              </div>

              <div className="grid grid-cols-3 gap-4">
                <div className={`p-4 rounded-lg border ${getRiskBgColor(analysis.total_exposure.risk_level)}`}>
                  <div className="flex items-center justify-center gap-2 mb-2">
                    {getSafetyIcon(analysis.total_exposure.safety_status)}
                    <span className={`font-semibold ${getRiskColor(analysis.total_exposure.risk_level)}`}>
                      {analysis.total_exposure.risk_level.toUpperCase()}
                    </span>
                  </div>
                  <div className="text-xs text-center text-gray-600">Nível de Risco</div>
                </div>

                <div className="p-4 bg-purple-50 border border-purple-200 rounded-lg">
                  <div className="text-2xl font-bold text-purple-600 text-center">
                    {analysis.total_exposure.exposure_percentage.toFixed(1)}%
                  </div>
                  <div className="text-xs text-center text-gray-600 mt-1">% do Limite</div>
                </div>

                <div className={`p-4 rounded-lg border ${analysis.total_exposure.compliance ? 'bg-green-50 border-green-200' : 'bg-red-50 border-red-200'}`}>
                  <div className="text-lg font-semibold text-center">
                    {analysis.total_exposure.compliance ? (
                      <span className="text-green-600">✓ CONFORME</span>
                    ) : (
                      <span className="text-red-600">✗ NÃO CONFORME</span>
                    )}
                  </div>
                  <div className="text-xs text-center text-gray-600 mt-1">Status</div>
                </div>
              </div>

              <div className="mt-4 p-4 bg-blue-50 rounded-lg">
                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div>
                    <span className="text-gray-600">Exposição Externa:</span>
                    <span className="ml-2 font-semibold">{analysis.total_exposure.external_exposure_uT.toFixed(4)} μT</span>
                  </div>
                  <div>
                    <span className="text-gray-600">Exposição Interna:</span>
                    <span className="ml-2 font-semibold">{analysis.total_exposure.internal_exposure_uT.toFixed(4)} μT</span>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Fontes Externas */}
          <div className="grid grid-cols-3 gap-6">
            {/* Torres de Celular */}
            <Card>
              <CardHeader>
                <CardTitle className="text-lg flex items-center gap-2">
                  <Tower className="h-5 w-5" />
                  Torres de Celular
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-center mb-4">
                  <div className="text-3xl font-bold text-blue-600">
                    {analysis.external_sources.cell_towers.towers_detected}
                  </div>
                  <div className="text-sm text-gray-600">Torres Detectadas</div>
                </div>

                {analysis.external_sources.cell_towers.closest_tower_distance && (
                  <div className="p-3 bg-blue-50 rounded-md mb-3">
                    <div className="text-sm text-gray-600">Mais Próxima</div>
                    <div className="text-xl font-semibold text-blue-600">
                      {analysis.external_sources.cell_towers.closest_tower_distance}m
                    </div>
                  </div>
                )}

                <div className={`p-3 rounded-md border ${getRiskBgColor(analysis.external_sources.cell_towers.overall_risk)}`}>
                  <div className="text-sm text-center font-semibold">
                    Risco: <span className={getRiskColor(analysis.external_sources.cell_towers.overall_risk)}>
                      {analysis.external_sources.cell_towers.overall_risk.toUpperCase()}
                    </span>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Linhas de Transmissão */}
            <Card>
              <CardHeader>
                <CardTitle className="text-lg flex items-center gap-2">
                  <Zap className="h-5 w-5" />
                  Linhas de Transmissão
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-center mb-4">
                  <div className="text-3xl font-bold text-yellow-600">
                    {analysis.external_sources.power_lines.power_lines_detected}
                  </div>
                  <div className="text-sm text-gray-600">Linhas Detectadas</div>
                </div>

                {analysis.external_sources.power_lines.closest_line_distance && (
                  <div className="p-3 bg-yellow-50 rounded-md mb-3">
                    <div className="text-sm text-gray-600">Mais Próxima</div>
                    <div className="text-xl font-semibold text-yellow-600">
                      {analysis.external_sources.power_lines.closest_line_distance}m
                    </div>
                  </div>
                )}

                <div className={`p-3 rounded-md border ${getRiskBgColor(analysis.external_sources.power_lines.overall_risk)}`}>
                  <div className="text-sm text-center font-semibold">
                    Risco: <span className={getRiskColor(analysis.external_sources.power_lines.overall_risk)}>
                      {analysis.external_sources.power_lines.overall_risk.toUpperCase()}
                    </span>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Transformadores */}
            <Card>
              <CardHeader>
                <CardTitle className="text-lg flex items-center gap-2">
                  <Radio className="h-5 w-5" />
                  Transformadores
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-center mb-4">
                  <div className="text-3xl font-bold text-orange-600">
                    {analysis.external_sources.transformers.transformers_detected}
                  </div>
                  <div className="text-sm text-gray-600">Transformadores Detectados</div>
                </div>

                {analysis.external_sources.transformers.closest_transformer_distance && (
                  <div className="p-3 bg-orange-50 rounded-md mb-3">
                    <div className="text-sm text-gray-600">Mais Próximo</div>
                    <div className="text-xl font-semibold text-orange-600">
                      {analysis.external_sources.transformers.closest_transformer_distance}m
                    </div>
                  </div>
                )}

                <div className={`p-3 rounded-md border ${getRiskBgColor(analysis.external_sources.transformers.overall_risk)}`}>
                  <div className="text-sm text-center font-semibold">
                    Risco: <span className={getRiskColor(analysis.external_sources.transformers.overall_risk)}>
                      {analysis.external_sources.transformers.overall_risk.toUpperCase()}
                    </span>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Fontes Internas */}
          {analysis.internal_sources && (
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Wifi className="h-5 w-5" />
                  Fontes Internas de EMF
                </CardTitle>
                <CardDescription>
                  Eletrodomésticos e equipamentos eletrônicos
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="mb-4 p-4 bg-purple-50 rounded-lg">
                  <div className="text-center">
                    <div className="text-3xl font-bold text-purple-600">
                      {analysis.internal_sources.total_internal_exposure_uT.toFixed(4)} μT
                    </div>
                    <div className="text-sm text-gray-600 mt-1">Exposição Interna Total</div>
                  </div>
                </div>

                <div className="space-y-2">
                  {analysis.internal_sources.appliances.slice(0, 5).map((appliance, idx) => (
                    <div key={idx} className="flex items-center justify-between p-3 bg-gray-50 rounded-md">
                      <div>
                        <div className="font-semibold capitalize">{appliance.type.replace('_', ' ')}</div>
                        <div className="text-sm text-gray-600">{appliance.location}</div>
                      </div>
                      <div className="text-right">
                        <div className="font-semibold text-purple-600">{appliance.emf_at_30cm_uT.toFixed(2)} μT</div>
                        <div className="text-xs text-gray-500">a 30cm</div>
                      </div>
                    </div>
                  ))}
                </div>

                {analysis.internal_sources.highest_emf_source && (
                  <div className="mt-4 p-4 bg-orange-50 border border-orange-200 rounded-md">
                    <div className="font-semibold text-orange-800 mb-1">Fonte de Maior EMF:</div>
                    <div className="text-orange-700 capitalize">
                      {analysis.internal_sources.highest_emf_source.type.replace('_', ' ')} - {analysis.internal_sources.highest_emf_source.emf_at_30cm_uT.toFixed(2)} μT
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>
          )}

          {/* Recomendações */}
          {analysis.recommendations && analysis.recommendations.length > 0 && (
            <Card>
              <CardHeader>
                <CardTitle>Recomendações</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  {analysis.recommendations.map((rec, idx) => (
                    <div key={idx} className="flex items-start gap-3 p-3 bg-green-50 border border-green-200 rounded-md">
                      <CheckCircle2 className="h-5 w-5 text-green-600 mt-0.5 flex-shrink-0" />
                      <span className="text-sm text-green-800">{rec}</span>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}

          {/* Avaliação Geral */}
          <Card>
            <CardHeader>
              <CardTitle>Avaliação Geral</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 gap-4">
                <div className="text-center p-6 bg-gradient-to-br from-indigo-50 to-indigo-100 rounded-lg">
                  <div className="text-4xl font-bold text-indigo-600">
                    {analysis.overall_assessment.emf_health_score}
                  </div>
                  <div className="text-sm text-gray-600 mt-2">Score de Saúde EMF</div>
                </div>
                <div className="text-center p-6 bg-gradient-to-br from-gray-50 to-gray-100 rounded-lg">
                  <div className="text-2xl font-semibold">
                    {analysis.overall_assessment.suitable_for_habitation ? (
                      <span className="text-green-600">✓ ADEQUADO</span>
                    ) : (
                      <span className="text-red-600">✗ NÃO ADEQUADO</span>
                    )}
                  </div>
                  <div className="text-sm text-gray-600 mt-2">Para Habitação</div>
                </div>
              </div>

              {analysis.overall_assessment.main_concerns && analysis.overall_assessment.main_concerns.length > 0 && (
                <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-md">
                  <h4 className="font-semibold text-red-800 mb-2">Principais Preocupações:</h4>
                  <ul className="list-disc list-inside space-y-1 text-red-700 text-sm">
                    {analysis.overall_assessment.main_concerns.map((concern, idx) => (
                      <li key={idx}>{concern}</li>
                    ))}
                  </ul>
                </div>
              )}
            </CardContent>
          </Card>
        </>
      )}
    </div>
  )
}


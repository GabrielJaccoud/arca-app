import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Label } from '@/components/ui/label.jsx'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs.jsx'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select.jsx'
import { Upload, Home, Leaf, Circle, MapPin, User, Users, BarChart2, Search, Filter, Download } from 'lucide-react'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import arcaLogo from './assets/LOGO.png'
import './App.css'

function App() {
  const [activeTab, setActiveTab] = useState('upload')
  const [floorPlanFile, setFloorPlanFile] = useState(null)
  const [analysisResults, setAnalysisResults] = useState(null)
  const [occupants, setOccupants] = useState([])
  const [floorPlansHistory, setFloorPlansHistory] = useState([])
  const [energeticAnalysesHistory, setEnergeticAnalysesHistory] = useState([])
  const [occupantsHistory, setOccupantsHistory] = useState([])
  const [analyticsData, setAnalyticsData] = useState({
    floorPlansByMonth: [],
    energeticAnalysesByCem: [],
    occupantProfilesByType: []
  })

  // Função para carregar histórico de plantas baixas
  const loadFloorPlansHistory = async () => {
    try {
      const response = await fetch('https://5000-i4jzvyj6hn9qmdbabo0f4-393f986f.manusvm.computer/floor_plans')
      const data = await response.json()
      setFloorPlansHistory(data)
    } catch (error) {
      console.error('Erro ao carregar histórico de plantas baixas:', error)
    }
  }

  // Função para carregar histórico de análises energéticas
  const loadEnergeticAnalysesHistory = async () => {
    try {
      const response = await fetch('https://5000-i4jzvyj6hn9qmdbabo0f4-393f986f.manusvm.computer/energetic_analyses')
      const data = await response.json()
      setEnergeticAnalysesHistory(data)
    } catch (error) {
      console.error('Erro ao carregar histórico de análises energéticas:', error)
    }
  }

  // Função para carregar histórico de perfis de ocupantes
  const loadOccupantsHistory = async () => {
    try {
      const response = await fetch("https://5000-i4jzvyj6hn9qmdbabo0f4-393f986f.manusvm.computer/occupant_profiles")
      const data = await response.json()
      setOccupantsHistory(data)
    } catch (error) {
      console.error("Erro ao carregar histórico de ocupantes:", error)
    }
  }

  // Funções para carregar dados de analytics
  const loadAnalyticsData = async () => {
    try {
      const [floorPlansRes, energeticAnalysesRes, occupantProfilesRes] = await Promise.all([
        fetch("https://5000-i4jzvyj6hn9qmdbabo0f4-393f986f.manusvm.computer/analytics/floor_plans_by_month"),
        fetch("https://5000-i4jzvyj6hn9qmdbabo0f4-393f986f.manusvm.computer/analytics/energetic_analyses_by_cem_proximity"),
        fetch("https://5000-i4jzvyj6hn9qmdbabo0f4-393f986f.manusvm.computer/analytics/occupant_profiles_by_type")
      ])

      const floorPlansByMonth = await floorPlansRes.json()
      const energeticAnalysesByCem = await energeticAnalysesRes.json()
      const occupantProfilesByType = await occupantProfilesRes.json()

      setAnalyticsData({
        floorPlansByMonth,
        energeticAnalysesByCem,
        occupantProfilesByType
      })
    } catch (error) {
      console.error("Erro ao carregar dados de analytics:", error)
    }
  }

  // Carregar dados de histórico e analytics na montagem do componente
  useEffect(() => {
    loadFloorPlansHistory()
    loadEnergeticAnalysesHistory()
    loadOccupantsHistory()
    loadAnalyticsData()
  }, [])

  // Funções de busca e filtros
  const handleFloorPlanSearch = async (filters) => {
    try {
      const params = new URLSearchParams()
      if (filters.filename) params.append('filename', filters.filename)
      if (filters.status) params.append('status', filters.status)
      if (filters.dateFrom) params.append('date_from', filters.dateFrom)
      if (filters.dateTo) params.append('date_to', filters.dateTo)
      
      const response = await fetch(`https://5000-i4jzvyj6hn9qmdbabo0f4-393f986f.manusvm.computer/search/floor_plans?${params}`)
      const data = await response.json()
      setFloorPlansHistory(data)
    } catch (error) {
      console.error('Erro na busca de plantas baixas:', error)
    }
  }

  const handleEnergeticAnalysisSearch = async (filters) => {
    try {
      const params = new URLSearchParams()
      if (filters.cemProximity) params.append('cem_proximity', filters.cemProximity)
      if (filters.geologicalAnomalies) params.append('geological_anomalies', filters.geologicalAnomalies)
      if (filters.dateFrom) params.append('date_from', filters.dateFrom)
      if (filters.dateTo) params.append('date_to', filters.dateTo)
      if (filters.latitudeMin) params.append('latitude_min', filters.latitudeMin)
      if (filters.latitudeMax) params.append('latitude_max', filters.latitudeMax)
      if (filters.longitudeMin) params.append('longitude_min', filters.longitudeMin)
      if (filters.longitudeMax) params.append('longitude_max', filters.longitudeMax)
      
      const response = await fetch(`https://5000-i4jzvyj6hn9qmdbabo0f4-393f986f.manusvm.computer/search/energetic_analyses?${params}`)
      const data = await response.json()
      setEnergeticAnalysesHistory(data)
    } catch (error) {
      console.error('Erro na busca de análises energéticas:', error)
    }
  }

  const handleOccupantProfileSearch = async (filters) => {
    try {
      const params = new URLSearchParams()
      if (filters.name) params.append('name', filters.name)
      if (filters.profileType) params.append('profile_type', filters.profileType)
      if (filters.dateFrom) params.append('date_from', filters.dateFrom)
      if (filters.dateTo) params.append('date_to', filters.dateTo)
      if (filters.baziElement) params.append('bazi_element', filters.baziElement)
      if (filters.functionEnergy) params.append('function_energy', filters.functionEnergy)
      
      const response = await fetch(`https://5000-i4jzvyj6hn9qmdbabo0f4-393f986f.manusvm.computer/search/occupant_profiles?${params}`)
      const data = await response.json()
      setOccupantsHistory(data)
    } catch (error) {
      console.error('Erro na busca de perfis de ocupantes:', error)
    }
  }

  const handleFileUpload = async (event) => {
    const file = event.target.files[0]
    if (file) {
      setFloorPlanFile(file)
      // Simular upload para a API
      const formData = new FormData()
      formData.append('file', file)
      
      try {
        const response = await fetch('https://5000-i4jzvyj6hn9qmdbabo0f4-393f986f.manusvm.computer/upload_floor_plan', {
          method: 'POST',
          body: formData
        })
        const result = await response.json()
        setAnalysisResults(result)
        setActiveTab('analysis')
        // Recarregar histórico de plantas baixas
        loadFloorPlansHistory()
      } catch (error) {
        console.error('Erro no upload:', error)
      }
    }
  }

  const handleEnergeticAnalysis = async () => {
    try {
      const response = await fetch('https://5000-i4jzvyj6hn9qmdbabo0f4-393f986f.manusvm.computer/analyze_energetics', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          latitude: -23.55052,
          longitude: -46.633309,
          floor_plan_id: analysisResults?.id,
          floor_plan_data: analysisResults?.analysis?.details || {}
        })
      })
      const result = await response.json()
      setAnalysisResults(prev => ({ ...prev, energetic_analysis: result }))
      // Recarregar histórico de análises energéticas
      loadEnergeticAnalysesHistory()
    } catch (error) {
      console.error('Erro na análise energética:', error)
    }
  }

  const handleOccupantRegistration = async (occupantData) => {
    try {
      const response = await fetch("https://5000-i4jzvyj6hn9qmdbabo0f4-393f986f.manusvm.computer/register_occupant", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(occupantData)
      })
      const result = await response.json()
      setOccupants(prev => [...prev, result.profile])
      // Recarregar histórico de ocupantes
      loadOccupantsHistory()
    } catch (error) {
      console.error("Erro no cadastro de ocupante:", error)
    }
  }

  const handleGenerateReport = async () => {
    try {
      const response = await fetch("https://5000-i4jzvyj6hn9qmdbabo0f4-393f986f.manusvm.computer/generate_report", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          floor_plan_id: analysisResults?.id,
          energetic_analysis_id: analysisResults?.energetic_analysis?.id,
          occupant_profile_ids: occupantsHistory.map(o => o.id) // Incluir todos os ocupantes do histórico
        })
      })

      if (response.ok) {
        const blob = await response.blob()
        const url = window.URL.createObjectURL(blob)
        const a = document.createElement("a")
        a.href = url
        a.download = "relatorio_arca.pdf"
        document.body.appendChild(a)
        a.click()
        a.remove()
        window.URL.revokeObjectURL(url)
      } else {
        const errorData = await response.json()
        console.error("Erro ao gerar relatório:", errorData.message)
        alert(`Erro ao gerar relatório: ${errorData.message}`)
      }
    } catch (error) {
      console.error("Erro ao gerar relatório:", error)
      alert("Erro ao gerar relatório. Verifique a conexão ou os dados.")
    }
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border bg-card">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <img src={arcaLogo} alt="ARCA Logo" className="h-12 w-12" />
            <div>
              <h1 className="arca-title text-2xl">ARCA</h1>
              <p className="arca-subtitle text-sm">Design Ambiental Holístico</p>
            </div>
          </div>
          <nav className="flex space-x-4">
            <Button variant="ghost" className="text-foreground hover:text-primary">
              <Home className="w-4 h-4 mr-2" />
              Início
            </Button>
            <Button variant="ghost" className="text-foreground hover:text-primary">
              <MapPin className="w-4 h-4 mr-2" />
              Projetos
            </Button>
          </nav>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
          <TabsList className="grid w-full grid-cols-6 bg-card">
            <TabsTrigger value="upload" className="data-[state=active]:bg-primary data-[state=active]:text-primary-foreground">
              <Upload className="w-4 h-4 mr-2" />
              Upload
            </TabsTrigger>
            <TabsTrigger value="analysis" className="data-[state=active]:bg-primary data-[state=active]:text-primary-foreground">
              <Circle className="w-4 h-4 mr-2" />
              Análise
            </TabsTrigger>
            <TabsTrigger value="occupants" className="data-[state=active]:bg-primary data-[state=active]:text-primary-foreground">
              <Users className="w-4 h-4 mr-2" />
              Ocupantes
            </TabsTrigger>
            <TabsTrigger value="history" className="data-[state=active]:bg-primary data-[state=active]:text-primary-foreground">
              <MapPin className="w-4 h-4 mr-2" />
              Histórico
            </TabsTrigger>
            <TabsTrigger value="dashboard" className="data-[state=active]:bg-primary data-[state=active]:text-primary-foreground">
              <BarChart2 className="w-4 h-4 mr-2" />
              Dashboard
            </TabsTrigger>
            <TabsTrigger value="recommendations" className="data-[state=active]:bg-primary data-[state=active]:text-primary-foreground">
              <Leaf className="w-4 h-4 mr-2" />
              Recomendações
            </TabsTrigger>
          </TabsList>

          {/* Upload Tab */}
          <TabsContent value="upload" className="space-y-6">
            <Card className="arca-card">
              <CardHeader>
                <CardTitle className="arca-title flex items-center">
                  <Upload className="w-5 h-5 mr-2" />
                  Upload da Planta Baixa
                </CardTitle>
                <CardDescription className="arca-body">
                  Faça o upload da planta baixa do seu projeto para iniciar a análise energética.
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid w-full max-w-sm items-center gap-1.5">
                  <Label htmlFor="floorplan" className="arca-body">Arquivo da Planta Baixa</Label>
                  <Input 
                    id="floorplan" 
                    type="file" 
                    accept=".pdf,.dwg,.jpg,.jpeg,.png"
                    onChange={handleFileUpload}
                    className="bg-input border-border"
                  />
                  <p className="text-sm text-muted-foreground">
                    Formatos aceitos: PDF, DWG, JPG, PNG
                  </p>
                </div>
                {floorPlanFile && (
                  <div className="mt-4 p-4 bg-secondary/20 rounded-lg">
                    <p className="arca-body">
                      Arquivo selecionado: <span className="text-primary font-semibold">{floorPlanFile.name}</span>
                    </p>
                  </div>
                )}
              </CardContent>
            </Card>
          </TabsContent>

          {/* Analysis Tab */}
          <TabsContent value="analysis" className="space-y-6">
            {analysisResults ? (
              <div className="grid gap-6 md:grid-cols-2">
                <Card className="arca-card">
                  <CardHeader>
                    <CardTitle className="arca-title">Análise Espacial</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-2">
                      <p className="arca-body">Status: <span className="text-primary">{analysisResults.status}</span></p>
                      
                      {/* Informações específicas do tipo de arquivo */}
                      {analysisResults.details?.processed_as === 'image_from_pdf' && (
                        <>
                          <p className="arca-body">Tipo: PDF convertido para imagem</p>
                          <p className="arca-body">Páginas processadas: {analysisResults.details.pages}</p>
                          {Object.keys(analysisResults.details).filter(key => key.startsWith('page_')).map(pageKey => (
                            <div key={pageKey} className="mt-2 p-2 bg-secondary/20 rounded">
                              <p className="arca-body text-sm font-semibold">{pageKey.replace('_', ' ').toUpperCase()}:</p>
                              <p className="arca-body text-sm">
                                Dimensões: {analysisResults.details[pageKey].width} x {analysisResults.details[pageKey].height}px
                              </p>
                              <p className="arca-body text-sm">
                                Bordas detectadas: {analysisResults.details[pageKey].real_features?.edges_detected ? '✓' : '✗'}
                              </p>
                              <p className="arca-body text-sm">
                                Linhas identificadas: {analysisResults.details[pageKey].real_features?.lines_identified ? '✓' : '✗'}
                              </p>
                              {analysisResults.details[pageKey].real_features?.num_lines_detected !== undefined && (
                                <p className="arca-body text-sm">Número de linhas: {analysisResults.details[pageKey].real_features.num_lines_detected}</p>
                              )}
                              <p className="arca-body text-sm">
                                Cômodos detectados (simulado): {analysisResults.details[pageKey].simulated_features?.rooms_detected}
                              </p>
                              <p className="arca-body text-sm">
                                Portas/janelas detectadas (simulado): {analysisResults.details[pageKey].simulated_features?.doors_windows_detected ? '✓' : '✗'}
                              </p>
                            </div>
                          ))}
                        </>
                      )}
                      
                      {analysisResults.details?.processed_as === 'image' && (
                        <>
                          <p className="arca-body">Tipo: Imagem ({analysisResults.details.format})</p>
                          <p className="arca-body">Dimensões: {analysisResults.details.width} x {analysisResults.details.height}px</p>
                          <p className="arca-body">Bordas detectadas: {analysisResults.details.real_features?.edges_detected ? '✓' : '✗'}</p>
                          <p className="arca-body">Linhas identificadas: {analysisResults.details.real_features?.lines_identified ? '✓' : '✗'}</p>
                          {analysisResults.details.real_features?.num_lines_detected !== undefined && (
                            <p className="arca-body text-sm">Número de linhas: {analysisResults.details.real_features.num_lines_detected}</p>
                          )}
                          <p className="arca-body text-sm">
                            Cômodos detectados (simulado): {analysisResults.details.simulated_features?.rooms_detected}
                          </p>
                          <p className="arca-body text-sm">
                            Portas/janelas detectadas (simulado): {analysisResults.details.simulated_features?.doors_windows_detected ? '✓' : '✗'}
                          </p>
                        </>
                      )}
                      
                      {analysisResults.details?.processed_as === 'cad_simulation' && (
                        <>
                          <p className="arca-body">Tipo: DWG (simulação)</p>
                          <p className="arca-body text-sm text-yellow-400">⚠️ Processamento DWG em desenvolvimento</p>
                        </>
                      )}
                      
                      <p className="arca-body">Tamanho: {(analysisResults.details?.size_bytes / 1024).toFixed(2)} KB</p>
                      <p className="arca-body">Dimensões identificadas (simulado): {analysisResults.details?.simulated_elements?.dimensions_identified ? '✓' : '✗'}</p>
                      <p className="arca-body">Portas/janelas (simulado): {analysisResults.details?.simulated_elements?.doors_windows_identified ? '✓' : '✗'}</p>
                      <p className="arca-body">Cômodos (simulado): {analysisResults.details?.simulated_elements?.rooms_identified ? '✓' : '✗'}</p>
                      <p className="arca-body">Bagua sobreposto (simulado): {analysisResults.details?.simulated_bagua_superposition ? '✓' : '✗'}</p>
                    </div>
                  </CardContent>
                </Card>

                <Card className="arca-card">
                  <CardHeader>
                    <CardTitle className="arca-title">Análise Energética</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <Button 
                      onClick={handleEnergeticAnalysis} 
                      className="arca-button w-full"
                    >
                      Executar Análise Energética
                    </Button>
                    {analysisResults.energetic_analysis && (
                      <div className="mt-4 space-y-4">
                        {/* Dados de Campo Magnético Real */}
                        {analysisResults.energetic_analysis.geographical_analysis?.data?.magnetic_field && (
                          <div className="p-3 bg-primary/10 rounded-lg">
                            <h4 className="arca-title text-sm mb-2">📡 Campo Magnético (Dados Reais)</h4>
                            <div className="grid grid-cols-2 gap-2 text-xs">
                              <p className="arca-body">Declinação: {analysisResults.energetic_analysis.geographical_analysis.data.magnetic_field.declination?.toFixed(2)}°</p>
                              <p className="arca-body">Inclinação: {analysisResults.energetic_analysis.geographical_analysis.data.magnetic_field.inclination?.toFixed(2)}°</p>
                              <p className="arca-body">Int. Horizontal: {analysisResults.energetic_analysis.geographical_analysis.data.magnetic_field.horizontal_intensity?.toFixed(0)} nT</p>
                              <p className="arca-body">Int. Total: {analysisResults.energetic_analysis.geographical_analysis.data.magnetic_field.total_intensity?.toFixed(0)} nT</p>
                            </div>
                          </div>
                        )}
                        
                        {/* Análise de CEM */}
                        <div className="p-3 bg-secondary/10 rounded-lg">
                          <h4 className="arca-title text-sm mb-2">⚡ Análise de CEM</h4>
                          <p className="arca-body text-sm">Proximidade CEM: <span className={`font-semibold ${
                            analysisResults.energetic_analysis.geographical_analysis?.data?.cem_proximity === 'high' ? 'text-red-400' :
                            analysisResults.energetic_analysis.geographical_analysis?.data?.cem_proximity === 'medium' ? 'text-yellow-400' :
                            'text-green-400'
                          }`}>
                            {analysisResults.energetic_analysis.geographical_analysis?.data?.cem_proximity}
                          </span></p>
                        </div>

                        {/* Anomalias Geológicas */}
                        <div className="p-3 bg-accent/10 rounded-lg">
                          <h4 className="arca-title text-sm mb-2">🌍 Análise Geobiológica</h4>
                          <p className="arca-body text-sm">Anomalias geológicas: {analysisResults.energetic_analysis.geographical_analysis?.data?.geological_anomalies}</p>
                          <p className="arca-body text-sm">Veios de água: {analysisResults.energetic_analysis.geographical_analysis?.data?.nearby_water_veins ? '✓ Detectados' : '✗ Não detectados'}</p>
                        </div>

                        {/* Fluxo de Chi */}
                        {analysisResults.energetic_analysis.chi_flow_analysis && (
                          <div className="p-3 bg-muted/10 rounded-lg">
                            <h4 className="arca-title text-sm mb-2">🌊 Fluxo de Chi</h4>
                            <p className="arca-body text-sm">Qualidade: <span className={`font-semibold ${
                              analysisResults.energetic_analysis.chi_flow_analysis.assessment?.chi_flow_quality === 'excellent' ? 'text-green-400' :
                              analysisResults.energetic_analysis.chi_flow_analysis.assessment?.chi_flow_quality === 'good' ? 'text-blue-400' :
                              analysisResults.energetic_analysis.chi_flow_analysis.assessment?.chi_flow_quality === 'fair' ? 'text-yellow-400' :
                              'text-red-400'
                            }`}>
                              {analysisResults.energetic_analysis.chi_flow_analysis.assessment?.chi_flow_quality}
                            </span></p>
                            {analysisResults.energetic_analysis.chi_flow_analysis.assessment?.obstructed_areas?.length > 0 && (
                              <p className="arca-body text-sm">Áreas obstruídas: {analysisResults.energetic_analysis.chi_flow_analysis.assessment.obstructed_areas.join(', ')}</p>
                            )}
                          </div>
                        )}
                        <Button 
                          onClick={handleGenerateReport} 
                          className="arca-button w-full mt-4"
                          disabled={!analysisResults.id || !analysisResults.energetic_analysis?.id}
                        >
                          Gerar Relatório PDF
                        </Button>
                      </div>
                    )}
                  </CardContent>
                </Card>
              </div>
            ) : (
              <Card className="arca-card">
                <CardContent className="pt-6">
                  <p className="arca-body text-center">Faça o upload de uma planta baixa para ver a análise.</p>
                </CardContent>
              </Card>
            )}
          </TabsContent>

          {/* Occupants Tab */}
          <TabsContent value="occupants" className="space-y-6">
            <Card className="arca-card">
              <CardHeader>
                <CardTitle className="arca-title">Cadastro de Ocupantes</CardTitle>
                <CardDescription className="arca-body">
                  Registre os perfis dos ocupantes para análise personalizada.
                </CardDescription>
              </CardHeader>
              <CardContent>
                <OccupantForm onSubmit={handleOccupantRegistration} />
              </CardContent>
            </Card>

            {occupants.length > 0 && (
              <Card className="arca-card">
                <CardHeader>
                  <CardTitle className="arca-title">Ocupantes Registrados</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {occupants.map((occupant, index) => (
                      <div key={index} className="p-4 bg-secondary/20 rounded-lg">
                        <p className="arca-body font-semibold">{occupant.name}</p>
                        <p className="arca-body text-sm">Tipo: {occupant.type}</p>
                        {occupant.bazi_profile && (
                          <p className="arca-body text-sm">Elemento Mestre: {occupant.bazi_profile.profile?.master_element}</p>
                        )}
                        {occupant.function_energy && (
                          <p className="arca-body text-sm">Energia da Função: {occupant.function_energy.energy_type}</p>
                        )}
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            )}
          </TabsContent>

          {/* History Tab */}
          <TabsContent value="history" className="space-y-6">
            {/* Seção de Filtros */}
            <Card className="arca-card">
              <CardHeader>
                <CardTitle className="arca-title">Filtros de Busca</CardTitle>
                <CardDescription className="arca-body">
                  Use os filtros abaixo para refinar sua busca no histórico
                </CardDescription>
              </CardHeader>
              <CardContent>
                <SearchFilters 
                  onFloorPlanSearch={handleFloorPlanSearch}
                  onEnergeticAnalysisSearch={handleEnergeticAnalysisSearch}
                  onOccupantProfileSearch={handleOccupantProfileSearch}
                />
              </CardContent>
            </Card>

            {/* Seção de Exportação */}
            <Card className="arca-card">
              <CardHeader>
                <CardTitle className="arca-title">Exportação de Dados</CardTitle>
                <CardDescription className="arca-body">
                  Exporte seus dados em diferentes formatos para backup ou análise externa
                </CardDescription>
              </CardHeader>
              <CardContent>
                <ExportSection />
              </CardContent>
            </Card>

            <div className="grid gap-6 md:grid-cols-3">
              {/* Histórico de Plantas Baixas */}
              <Card className="arca-card">
                <CardHeader>
                  <CardTitle className="arca-title flex items-center">
                    <Upload className="w-5 h-5 mr-2" />
                    Plantas Baixas
                  </CardTitle>
                  <CardDescription className="arca-body">
                    Histórico de uploads realizados
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <Button 
                    onClick={loadFloorPlansHistory} 
                    className="arca-button w-full mb-4"
                  >
                    Carregar Histórico
                  </Button>
                  <div className="space-y-2 max-h-64 overflow-y-auto">
                    {floorPlansHistory.map((plan) => (
                      <div key={plan.id} className="p-3 bg-secondary/20 rounded-lg">
                        <p className="arca-body text-sm font-semibold">{plan.filename}</p>
                        <p className="arca-body text-xs text-muted-foreground">
                          {new Date(plan.upload_date).toLocaleDateString('pt-BR')}
                        </p>
                        <p className="arca-body text-xs">
                          Status: <span className={plan.analysis_results?.status === 'success' ? 'text-green-400' : 'text-red-400'}>
                            {plan.analysis_results?.status}
                          </span>
                        </p>
                      </div>
                    ))}
                    {floorPlansHistory.length === 0 && (
                      <p className="arca-body text-center text-muted-foreground">Nenhuma planta baixa encontrada</p>
                    )}
                  </div>
                </CardContent>
              </Card>

              {/* Histórico de Análises Energéticas */}
              <Card className="arca-card">
                <CardHeader>
                  <CardTitle className="arca-title flex items-center">
                    <Circle className="w-5 h-5 mr-2" />
                    Análises Energéticas
                  </CardTitle>
                  <CardDescription className="arca-body">
                    Histórico de análises realizadas
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <Button 
                    onClick={loadEnergeticAnalysesHistory} 
                    className="arca-button w-full mb-4"
                  >
                    Carregar Histórico
                  </Button>
                  <div className="space-y-2 max-h-64 overflow-y-auto">
                    {energeticAnalysesHistory.map((analysis) => (
                      <div key={analysis.id} className="p-3 bg-secondary/20 rounded-lg">
                        <p className="arca-body text-sm font-semibold">
                          Lat: {analysis.latitude.toFixed(4)}, Lon: {analysis.longitude.toFixed(4)}
                        </p>
                        <p className="arca-body text-xs text-muted-foreground">
                          {new Date(analysis.analysis_date).toLocaleDateString('pt-BR')}
                        </p>
                        <p className="arca-body text-xs">
                          CEM: <span className={`font-semibold ${
                            analysis.cem_proximity === 'high' ? 'text-red-400' :
                            analysis.cem_proximity === 'medium' ? 'text-yellow-400' :
                            'text-green-400'
                          }`}>
                            {analysis.cem_proximity}
                          </span>
                        </p>
                        {analysis.magnetic_field_data && (
                          <p className="arca-body text-xs">
                            Campo: {analysis.magnetic_field_data.total_intensity?.toFixed(0)} nT
                          </p>
                        )}
                      </div>
                    ))}
                    {energeticAnalysesHistory.length === 0 && (
                      <p className="arca-body text-center text-muted-foreground">Nenhuma análise encontrada</p>
                    )}
                  </div>
                </CardContent>
              </Card>

              {/* Histórico de Ocupantes */}
              <Card className="arca-card">
                <CardHeader>
                  <CardTitle className="arca-title flex items-center">
                    <Users className="w-5 h-5 mr-2" />
                    Perfis de Ocupantes
                  </CardTitle>
                  <CardDescription className="arca-body">
                    Histórico de cadastros realizados
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <Button 
                    onClick={loadOccupantsHistory} 
                    className="arca-button w-full mb-4"
                  >
                    Carregar Histórico
                  </Button>
                  <div className="space-y-2 max-h-64 overflow-y-auto">
                    {occupantsHistory.map((occupant) => (
                      <div key={occupant.id} className="p-3 bg-secondary/20 rounded-lg">
                        <p className="arca-body text-sm font-semibold">{occupant.name}</p>
                        <p className="arca-body text-xs text-muted-foreground">
                          {new Date(occupant.registration_date).toLocaleDateString('pt-BR')}
                        </p>
                        <p className="arca-body text-xs">
                          Tipo: <span className="font-semibold">
                            {occupant.profile_type === 'owner_family' ? 'Proprietário/Família' : 'Funcionário'}
                          </span>
                        </p>
                        {occupant.details?.bazi_profile && (
                          <p className="arca-body text-xs">
                            Elemento: {occupant.details.bazi_profile.profile?.master_element}
                          </p>
                        )}
                      </div>
                    ))}
                    {occupantsHistory.length === 0 && (
                      <p className="arca-body text-center text-muted-foreground">Nenhum ocupante encontrado</p>
                    )}
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          {/* Dashboard Tab */}
          <TabsContent value="dashboard" className="space-y-6">
            <Card className="arca-card">
              <CardHeader>
                <CardTitle className="arca-title flex items-center">
                  <BarChart2 className="w-5 h-5 mr-2" />
                  Dashboard de Análises
                </CardTitle>
                <CardDescription className="arca-body">
                  Visão geral e estatísticas das análises realizadas no ARCA.
                </CardDescription>
              </CardHeader>
              <CardContent className="grid gap-6 md:grid-cols-2">
                {/* Gráfico de Plantas Baixas por Mês */}
                <Card className="arca-card">
                  <CardHeader>
                    <CardTitle className="arca-title text-lg">Plantas Baixas por Mês</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <ResponsiveContainer width="100%" height={300}>
                      <BarChart data={analyticsData.floorPlansByMonth}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="month" />
                        <YAxis />
                        <Tooltip />
                        <Legend />
                        <Bar dataKey="count" fill="#8884d8" />
                      </BarChart>
                    </ResponsiveContainer>
                  </CardContent>
                </Card>

                {/* Gráfico de Análises Energéticas por Proximidade CEM */}
                <Card className="arca-card">
                  <CardHeader>
                    <CardTitle className="arca-title text-lg">Análises Energéticas por CEM</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <ResponsiveContainer width="100%" height={300}>
                      <PieChart>
                        <Pie
                          data={analyticsData.energeticAnalysesByCem}
                          dataKey="count"
                          nameKey="cem_proximity"
                          cx="50%"
                          cy="50%"
                          outerRadius={100}
                          fill="#82ca9d"
                          label
                        >
                          {analyticsData.energeticAnalysesByCem.map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={{
                              high: "#ef4444", // red-500
                              medium: "#f59e0b", // yellow-500
                              low: "#22c55e" // green-500
                            }[entry.cem_proximity]} />
                          ))}
                        </Pie>
                        <Tooltip />
                        <Legend />
                      </PieChart>
                    </ResponsiveContainer>
                  </CardContent>
                </Card>

                {/* Gráfico de Perfis de Ocupantes por Tipo */}
                <Card className="arca-card">
                  <CardHeader>
                    <CardTitle className="arca-title text-lg">Perfis de Ocupantes por Tipo</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <ResponsiveContainer width="100%" height={300}>
                      <BarChart data={analyticsData.occupantProfilesByType}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="profile_type" />
                        <YAxis />
                        <Tooltip />
                        <Legend />
                        <Bar dataKey="count" fill="#ffc658" />
                      </BarChart>
                    </ResponsiveContainer>
                  </CardContent>
                </Card>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Recommendations Tab */}
          <TabsContent value="recommendations" className="space-y-6">
            <Card className="arca-card">
              <CardHeader>
                <CardTitle className="arca-title flex items-center">
                  <Leaf className="w-5 h-5 mr-2" />
                  Recomendações Energéticas
                </CardTitle>
              </CardHeader>
              <CardContent>
                {analysisResults && occupants.length > 0 ? (
                  <div className="space-y-4">
                    <div className="p-4 bg-secondary/20 rounded-lg">
                      <h4 className="arca-title text-lg mb-2">Recomendações Gerais</h4>
                      <ul className="arca-body space-y-1">
                        <li>• Otimizar o fluxo de Chi nos corredores principais</li>
                        <li>• Posicionar elementos de madeira na área de crescimento (Bagua)</li>
                        <li>• Considerar proteção contra CEM identificados</li>
                      </ul>
                    </div>
                    <div className="p-4 bg-accent/20 rounded-lg">
                      <h4 className="arca-title text-lg mb-2">Recomendações Personalizadas</h4>
                      <ul className="arca-body space-y-1">
                        {occupants.map((occupant, index) => (
                          <li key={index}>
                            • {occupant.name}: {occupant.bazi_profile?.profile?.master_element === 'Wood' ? 
                              'Área leste recomendada para atividades principais' : 
                              'Área sul recomendada para atividades principais'}
                          </li>
                        ))}
                      </ul>
                    </div>
                  </div>
                ) : (
                  <p className="arca-body text-center">Complete a análise espacial e cadastre ocupantes para ver recomendações personalizadas.</p>
                )}
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </main>
    </div>
  )
}

// Componente para formulário de ocupantes
function OccupantForm({ onSubmit }) {
  const [formData, setFormData] = useState({
    type: 'owner_family',
    name: '',
    dob: '',
    tob: '',
    pob: '',
    function: ''
  })

  const handleSubmit = (e) => {
    e.preventDefault()
    onSubmit(formData)
    setFormData({
      type: 'owner_family',
      name: '',
      dob: '',
      tob: '',
      pob: '',
      function: ''
    })
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="grid gap-4 md:grid-cols-2">
        <div>
          <Label htmlFor="type" className="arca-body">Tipo de Ocupante</Label>
          <select 
            id="type"
            value={formData.type}
            onChange={(e) => setFormData({...formData, type: e.target.value})}
            className="w-full p-2 bg-input border border-border rounded-md text-foreground"
          >
            <option value="owner_family">Proprietário/Família</option>
            <option value="employee">Funcionário</option>
          </select>
        </div>
        <div>
          <Label htmlFor="name" className="arca-body">Nome</Label>
          <Input 
            id="name"
            value={formData.name}
            onChange={(e) => setFormData({...formData, name: e.target.value})}
            required
            className="bg-input border-border"
          />
        </div>
      </div>

      {formData.type === 'owner_family' ? (
        <div className="grid gap-4 md:grid-cols-3">
          <div>
            <Label htmlFor="dob" className="arca-body">Data de Nascimento</Label>
            <Input 
              id="dob"
              type="date"
              value={formData.dob}
              onChange={(e) => setFormData({...formData, dob: e.target.value})}
              required
              className="bg-input border-border"
            />
          </div>
          <div>
            <Label htmlFor="tob" className="arca-body">Hora de Nascimento</Label>
            <Input 
              id="tob"
              type="time"
              value={formData.tob}
              onChange={(e) => setFormData({...formData, tob: e.target.value})}
              required
              className="bg-input border-border"
            />
          </div>
          <div>
            <Label htmlFor="pob" className="arca-body">Local de Nascimento</Label>
            <Input 
              id="pob"
              value={formData.pob}
              onChange={(e) => setFormData({...formData, pob: e.target.value})}
              placeholder="Cidade, País"
              required
              className="bg-input border-border"
            />
          </div>
        </div>
      ) : (
        <div>
          <Label htmlFor="function" className="arca-body">Função</Label>
          <Input 
            id="function"
            value={formData.function}
            onChange={(e) => setFormData({...formData, function: e.target.value})}
            placeholder="Ex: Gerente, Copeira, Segurança"
            required
            className="bg-input border-border"
          />
        </div>
      )}

      <Button type="submit" className="arca-button w-full">
        <User className="w-4 h-4 mr-2" />
        Cadastrar Ocupante
      </Button>
    </form>
  )
}

export default App



// Componente para filtros de busca
function SearchFilters({ onFloorPlanSearch, onEnergeticAnalysisSearch, onOccupantProfileSearch }) {
  const [activeFilter, setActiveFilter] = useState('floor_plans')
  const [floorPlanFilters, setFloorPlanFilters] = useState({
    filename: '',
    status: '',
    dateFrom: '',
    dateTo: ''
  })
  const [energeticFilters, setEnergeticFilters] = useState({
    cemProximity: '',
    geologicalAnomalies: '',
    dateFrom: '',
    dateTo: '',
    latitudeMin: '',
    latitudeMax: '',
    longitudeMin: '',
    longitudeMax: ''
  })
  const [occupantFilters, setOccupantFilters] = useState({
    name: '',
    profileType: '',
    dateFrom: '',
    dateTo: '',
    baziElement: '',
    functionEnergy: ''
  })

  const handleFloorPlanSearch = () => {
    onFloorPlanSearch(floorPlanFilters)
  }

  const handleEnergeticSearch = () => {
    onEnergeticAnalysisSearch(energeticFilters)
  }

  const handleOccupantSearch = () => {
    onOccupantProfileSearch(occupantFilters)
  }

  const clearFloorPlanFilters = () => {
    setFloorPlanFilters({
      filename: '',
      status: '',
      dateFrom: '',
      dateTo: ''
    })
  }

  const clearEnergeticFilters = () => {
    setEnergeticFilters({
      cemProximity: '',
      geologicalAnomalies: '',
      dateFrom: '',
      dateTo: '',
      latitudeMin: '',
      latitudeMax: '',
      longitudeMin: '',
      longitudeMax: ''
    })
  }

  const clearOccupantFilters = () => {
    setOccupantFilters({
      name: '',
      profileType: '',
      dateFrom: '',
      dateTo: '',
      baziElement: '',
      functionEnergy: ''
    })
  }

  return (
    <div className="space-y-4">
      {/* Seletor de tipo de filtro */}
      <div className="flex space-x-2">
        <Button
          variant={activeFilter === 'floor_plans' ? 'default' : 'outline'}
          onClick={() => setActiveFilter('floor_plans')}
          className="arca-button"
        >
          <Upload className="w-4 h-4 mr-2" />
          Plantas Baixas
        </Button>
        <Button
          variant={activeFilter === 'energetic' ? 'default' : 'outline'}
          onClick={() => setActiveFilter('energetic')}
          className="arca-button"
        >
          <Circle className="w-4 h-4 mr-2" />
          Análises Energéticas
        </Button>
        <Button
          variant={activeFilter === 'occupants' ? 'default' : 'outline'}
          onClick={() => setActiveFilter('occupants')}
          className="arca-button"
        >
          <Users className="w-4 h-4 mr-2" />
          Ocupantes
        </Button>
      </div>

      {/* Filtros para Plantas Baixas */}
      {activeFilter === 'floor_plans' && (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          <div>
            <Label className="arca-body">Nome do Arquivo</Label>
            <Input
              value={floorPlanFilters.filename}
              onChange={(e) => setFloorPlanFilters({...floorPlanFilters, filename: e.target.value})}
              placeholder="Digite o nome do arquivo"
              className="bg-input border-border"
            />
          </div>
          <div>
            <Label className="arca-body">Status</Label>
            <Select value={floorPlanFilters.status} onValueChange={(value) => setFloorPlanFilters({...floorPlanFilters, status: value})}>
              <SelectTrigger className="bg-input border-border">
                <SelectValue placeholder="Selecione o status" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="">Todos</SelectItem>
                <SelectItem value="success">Sucesso</SelectItem>
                <SelectItem value="error">Erro</SelectItem>
              </SelectContent>
            </Select>
          </div>
          <div>
            <Label className="arca-body">Data Inicial</Label>
            <Input
              type="date"
              value={floorPlanFilters.dateFrom}
              onChange={(e) => setFloorPlanFilters({...floorPlanFilters, dateFrom: e.target.value})}
              className="bg-input border-border"
            />
          </div>
          <div>
            <Label className="arca-body">Data Final</Label>
            <Input
              type="date"
              value={floorPlanFilters.dateTo}
              onChange={(e) => setFloorPlanFilters({...floorPlanFilters, dateTo: e.target.value})}
              className="bg-input border-border"
            />
          </div>
          <div className="flex space-x-2">
            <Button onClick={handleFloorPlanSearch} className="arca-button">
              <Search className="w-4 h-4 mr-2" />
              Buscar
            </Button>
            <Button onClick={clearFloorPlanFilters} variant="outline" className="arca-button">
              Limpar
            </Button>
          </div>
        </div>
      )}

      {/* Filtros para Análises Energéticas */}
      {activeFilter === 'energetic' && (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          <div>
            <Label className="arca-body">Proximidade CEM</Label>
            <Select value={energeticFilters.cemProximity} onValueChange={(value) => setEnergeticFilters({...energeticFilters, cemProximity: value})}>
              <SelectTrigger className="bg-input border-border">
                <SelectValue placeholder="Selecione CEM" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="">Todos</SelectItem>
                <SelectItem value="low">Baixo</SelectItem>
                <SelectItem value="medium">Médio</SelectItem>
                <SelectItem value="high">Alto</SelectItem>
              </SelectContent>
            </Select>
          </div>
          <div>
            <Label className="arca-body">Anomalias Geológicas</Label>
            <Select value={energeticFilters.geologicalAnomalies} onValueChange={(value) => setEnergeticFilters({...energeticFilters, geologicalAnomalies: value})}>
              <SelectTrigger className="bg-input border-border">
                <SelectValue placeholder="Selecione anomalias" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="">Todos</SelectItem>
                <SelectItem value="none">Nenhuma</SelectItem>
                <SelectItem value="minor">Menores</SelectItem>
                <SelectItem value="moderate">Moderadas</SelectItem>
                <SelectItem value="significant">Significativas</SelectItem>
              </SelectContent>
            </Select>
          </div>
          <div>
            <Label className="arca-body">Data Inicial</Label>
            <Input
              type="date"
              value={energeticFilters.dateFrom}
              onChange={(e) => setEnergeticFilters({...energeticFilters, dateFrom: e.target.value})}
              className="bg-input border-border"
            />
          </div>
          <div>
            <Label className="arca-body">Data Final</Label>
            <Input
              type="date"
              value={energeticFilters.dateTo}
              onChange={(e) => setEnergeticFilters({...energeticFilters, dateTo: e.target.value})}
              className="bg-input border-border"
            />
          </div>
          <div>
            <Label className="arca-body">Latitude Mín</Label>
            <Input
              type="number"
              step="0.0001"
              value={energeticFilters.latitudeMin}
              onChange={(e) => setEnergeticFilters({...energeticFilters, latitudeMin: e.target.value})}
              placeholder="-90.0000"
              className="bg-input border-border"
            />
          </div>
          <div>
            <Label className="arca-body">Latitude Máx</Label>
            <Input
              type="number"
              step="0.0001"
              value={energeticFilters.latitudeMax}
              onChange={(e) => setEnergeticFilters({...energeticFilters, latitudeMax: e.target.value})}
              placeholder="90.0000"
              className="bg-input border-border"
            />
          </div>
          <div>
            <Label className="arca-body">Longitude Mín</Label>
            <Input
              type="number"
              step="0.0001"
              value={energeticFilters.longitudeMin}
              onChange={(e) => setEnergeticFilters({...energeticFilters, longitudeMin: e.target.value})}
              placeholder="-180.0000"
              className="bg-input border-border"
            />
          </div>
          <div>
            <Label className="arca-body">Longitude Máx</Label>
            <Input
              type="number"
              step="0.0001"
              value={energeticFilters.longitudeMax}
              onChange={(e) => setEnergeticFilters({...energeticFilters, longitudeMax: e.target.value})}
              placeholder="180.0000"
              className="bg-input border-border"
            />
          </div>
          <div className="flex space-x-2">
            <Button onClick={handleEnergeticSearch} className="arca-button">
              <Search className="w-4 h-4 mr-2" />
              Buscar
            </Button>
            <Button onClick={clearEnergeticFilters} variant="outline" className="arca-button">
              Limpar
            </Button>
          </div>
        </div>
      )}

      {/* Filtros para Ocupantes */}
      {activeFilter === 'occupants' && (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          <div>
            <Label className="arca-body">Nome</Label>
            <Input
              value={occupantFilters.name}
              onChange={(e) => setOccupantFilters({...occupantFilters, name: e.target.value})}
              placeholder="Digite o nome"
              className="bg-input border-border"
            />
          </div>
          <div>
            <Label className="arca-body">Tipo de Perfil</Label>
            <Select value={occupantFilters.profileType} onValueChange={(value) => setOccupantFilters({...occupantFilters, profileType: value})}>
              <SelectTrigger className="bg-input border-border">
                <SelectValue placeholder="Selecione o tipo" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="">Todos</SelectItem>
                <SelectItem value="owner_family">Proprietário/Família</SelectItem>
                <SelectItem value="employee">Funcionário</SelectItem>
              </SelectContent>
            </Select>
          </div>
          <div>
            <Label className="arca-body">Elemento BaZi</Label>
            <Select value={occupantFilters.baziElement} onValueChange={(value) => setOccupantFilters({...occupantFilters, baziElement: value})}>
              <SelectTrigger className="bg-input border-border">
                <SelectValue placeholder="Selecione elemento" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="">Todos</SelectItem>
                <SelectItem value="Wood">Madeira</SelectItem>
                <SelectItem value="Fire">Fogo</SelectItem>
                <SelectItem value="Earth">Terra</SelectItem>
                <SelectItem value="Metal">Metal</SelectItem>
                <SelectItem value="Water">Água</SelectItem>
              </SelectContent>
            </Select>
          </div>
          <div>
            <Label className="arca-body">Energia da Função</Label>
            <Select value={occupantFilters.functionEnergy} onValueChange={(value) => setOccupantFilters({...occupantFilters, functionEnergy: value})}>
              <SelectTrigger className="bg-input border-border">
                <SelectValue placeholder="Selecione energia" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="">Todos</SelectItem>
                <SelectItem value="creative">Criativa</SelectItem>
                <SelectItem value="analytical">Analítica</SelectItem>
                <SelectItem value="leadership">Liderança</SelectItem>
                <SelectItem value="supportive">Suporte</SelectItem>
              </SelectContent>
            </Select>
          </div>
          <div>
            <Label className="arca-body">Data Inicial</Label>
            <Input
              type="date"
              value={occupantFilters.dateFrom}
              onChange={(e) => setOccupantFilters({...occupantFilters, dateFrom: e.target.value})}
              className="bg-input border-border"
            />
          </div>
          <div>
            <Label className="arca-body">Data Final</Label>
            <Input
              type="date"
              value={occupantFilters.dateTo}
              onChange={(e) => setOccupantFilters({...occupantFilters, dateTo: e.target.value})}
              className="bg-input border-border"
            />
          </div>
          <div className="flex space-x-2">
            <Button onClick={handleOccupantSearch} className="arca-button">
              <Search className="w-4 h-4 mr-2" />
              Buscar
            </Button>
            <Button onClick={clearOccupantFilters} variant="outline" className="arca-button">
              Limpar
            </Button>
          </div>
        </div>
      )}
    </div>
  )
}

export default App


// Componente para exportação de dados
function ExportSection() {
  const handleExport = async (type, format) => {
    try {
      const response = await fetch(`https://5000-i4jzvyj6hn9qmdbabo0f4-393f986f.manusvm.computer/export/${type}?format=${format}`)
      
      if (response.ok) {
        const blob = await response.blob()
        const url = window.URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.style.display = 'none'
        a.href = url
        
        // Extrair nome do arquivo do header Content-Disposition ou usar padrão
        const contentDisposition = response.headers.get('content-disposition')
        let filename = `${type}.${format}`
        if (contentDisposition) {
          const filenameMatch = contentDisposition.match(/filename="(.+)"/)
          if (filenameMatch) {
            filename = filenameMatch[1]
          }
        }
        
        a.download = filename
        document.body.appendChild(a)
        a.click()
        window.URL.revokeObjectURL(url)
        document.body.removeChild(a)
      } else {
        console.error('Erro na exportação:', response.statusText)
      }
    } catch (error) {
      console.error('Erro na exportação:', error)
    }
  }

  const handleFullBackup = async () => {
    try {
      const response = await fetch('https://5000-i4jzvyj6hn9qmdbabo0f4-393f986f.manusvm.computer/export/full_backup')
      
      if (response.ok) {
        const blob = await response.blob()
        const url = window.URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.style.display = 'none'
        a.href = url
        
        // Extrair nome do arquivo do header Content-Disposition
        const contentDisposition = response.headers.get('content-disposition')
        let filename = `arca_backup_${new Date().toISOString().slice(0, 19).replace(/:/g, '-')}.json`
        if (contentDisposition) {
          const filenameMatch = contentDisposition.match(/filename="(.+)"/)
          if (filenameMatch) {
            filename = filenameMatch[1]
          }
        }
        
        a.download = filename
        document.body.appendChild(a)
        a.click()
        window.URL.revokeObjectURL(url)
        document.body.removeChild(a)
      } else {
        console.error('Erro no backup completo:', response.statusText)
      }
    } catch (error) {
      console.error('Erro no backup completo:', error)
    }
  }

  return (
    <div className="space-y-6">
      {/* Exportações Individuais */}
      <div className="grid gap-4 md:grid-cols-3">
        {/* Plantas Baixas */}
        <Card className="arca-card">
          <CardHeader>
            <CardTitle className="arca-title text-lg flex items-center">
              <Upload className="w-4 h-4 mr-2" />
              Plantas Baixas
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-2">
            <Button 
              onClick={() => handleExport('floor_plans', 'json')}
              className="arca-button w-full"
              variant="outline"
            >
              <Download className="w-4 h-4 mr-2" />
              Exportar JSON
            </Button>
            <Button 
              onClick={() => handleExport('floor_plans', 'csv')}
              className="arca-button w-full"
              variant="outline"
            >
              <Download className="w-4 h-4 mr-2" />
              Exportar CSV
            </Button>
          </CardContent>
        </Card>

        {/* Análises Energéticas */}
        <Card className="arca-card">
          <CardHeader>
            <CardTitle className="arca-title text-lg flex items-center">
              <Circle className="w-4 h-4 mr-2" />
              Análises Energéticas
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-2">
            <Button 
              onClick={() => handleExport('energetic_analyses', 'json')}
              className="arca-button w-full"
              variant="outline"
            >
              <Download className="w-4 h-4 mr-2" />
              Exportar JSON
            </Button>
            <Button 
              onClick={() => handleExport('energetic_analyses', 'csv')}
              className="arca-button w-full"
              variant="outline"
            >
              <Download className="w-4 h-4 mr-2" />
              Exportar CSV
            </Button>
          </CardContent>
        </Card>

        {/* Perfis de Ocupantes */}
        <Card className="arca-card">
          <CardHeader>
            <CardTitle className="arca-title text-lg flex items-center">
              <Users className="w-4 h-4 mr-2" />
              Perfis de Ocupantes
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-2">
            <Button 
              onClick={() => handleExport('occupant_profiles', 'json')}
              className="arca-button w-full"
              variant="outline"
            >
              <Download className="w-4 h-4 mr-2" />
              Exportar JSON
            </Button>
            <Button 
              onClick={() => handleExport('occupant_profiles', 'csv')}
              className="arca-button w-full"
              variant="outline"
            >
              <Download className="w-4 h-4 mr-2" />
              Exportar CSV
            </Button>
          </CardContent>
        </Card>
      </div>

      {/* Backup Completo */}
      <Card className="arca-card">
        <CardHeader>
          <CardTitle className="arca-title text-lg">Backup Completo</CardTitle>
          <CardDescription className="arca-body">
            Exporte todos os dados do sistema em um único arquivo JSON para backup completo
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Button 
            onClick={handleFullBackup}
            className="arca-button w-full md:w-auto"
          >
            <Download className="w-4 h-4 mr-2" />
            Gerar Backup Completo
          </Button>
        </CardContent>
      </Card>
    </div>
  )
}


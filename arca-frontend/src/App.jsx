
import React, { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Label } from '@/components/ui/label.jsx'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs.jsx'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select.jsx'
import { Upload, Home, Leaf, Circle, MapPin, User, Users, BarChart2, Search, Filter, Download, Star, Compass, Calendar } from 'lucide-react'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import arcaLogo from './assets/LOGO.png'
import { calculateBaZi } from './utils/baziCalculator.js'
import { calculateKua, analyzeHouseCompatibility } from './utils/kuaCalculator.js'
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

  // Estados para BaZi e Kua
  const [baziData, setBaziData] = useState({
    birthDateTime: '',
    timezoneOffset: -3,
    results: null,
    loading: false
  })
  
  const [kuaData, setKuaData] = useState({
    birthYear: '',
    gender: '',
    results: null,
    loading: false
  })
  
  const [completeAnalysis, setCompleteAnalysis] = useState(null)
  const [houseAnalysis, setHouseAnalysis] = useState({
    facingDirection: '',
    results: null,
    loading: false
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

  // Funções para BaZi e Kua
  const calculateBaZiLocal = async () => {
    setBaziData(prev => ({ ...prev, loading: true }))
    
    try {
      if (!baziData.birthDateTime) {
        alert('Por favor, insira a data e hora de nascimento')
        setBaziData(prev => ({ ...prev, loading: false }))
        return
      }

      // Usar calculadora local
      const result = calculateBaZi(baziData.birthDateTime, baziData.timezoneOffset)
      setBaziData(prev => ({ ...prev, results: result, loading: false }))
      
    } catch (error) {
      console.error('Erro no cálculo BaZi:', error)
      alert('Erro no cálculo BaZi. Verifique os dados inseridos.')
      setBaziData(prev => ({ ...prev, loading: false }))
    }
  }

  const calculateKuaLocal = async () => {
    setKuaData(prev => ({ ...prev, loading: true }))
    
    try {
      if (!kuaData.birthYear || !kuaData.gender) {
        alert('Por favor, insira o ano de nascimento e gênero')
        setKuaData(prev => ({ ...prev, loading: false }))
        return
      }

      // Usar calculadora local
      const result = calculateKua(parseInt(kuaData.birthYear), kuaData.gender)
      setKuaData(prev => ({ ...prev, results: result, loading: false }))
      
    } catch (error) {
      console.error('Erro no cálculo Kua:', error)
      alert('Erro no cálculo Kua. Verifique os dados inseridos.')
      setKuaData(prev => ({ ...prev, loading: false }))
    }
  }

  const calculateCompleteAnalysis = async () => {
    if (!baziData.birthDateTime || !kuaData.birthYear || !kuaData.gender) {
      alert('Preencha todos os campos para análise completa')
      return
    }

    try {
      const response = await fetch("https://5001-i9gi4qwrih9j9yd71dq7w-62eefc4a.manusvm.computer/bazi_kua/complete_analysis", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          birth_datetime: baziData.birthDateTime,
          birth_year: parseInt(kuaData.birthYear),
          gender: kuaData.gender,
          timezone_offset: baziData.timezoneOffset
        })
      })
      
      const result = await response.json()
      
      if (result.status === 'success') {
        setCompleteAnalysis(result.data)
        setBaziData(prev => ({ ...prev, results: result.data.bazi }))
        setKuaData(prev => ({ ...prev, results: result.data.kua }))
      } else {
        console.error('Erro na análise completa:', result.message)
        alert(`Erro na análise completa: ${result.message}`)
      }
    } catch (error) {
      console.error('Erro na análise completa:', error)
      alert('Erro na conexão. Verifique se o servidor está funcionando.')
    }
  }

  const analyzeHouseCompatibilityLocal = async () => {
    if (!houseAnalysis.facingDirection || !kuaData.birthYear || !kuaData.gender) {
      alert('Preencha todos os campos para análise da casa')
      return
    }

    setHouseAnalysis(prev => ({ ...prev, loading: true }))

    try {
      // Usar calculadora local
      const result = analyzeHouseCompatibility(houseAnalysis.facingDirection, parseInt(kuaData.birthYear), kuaData.gender)
      setHouseAnalysis(prev => ({ ...prev, results: result, loading: false }))
      
    } catch (error) {
      console.error('Erro na análise da casa:', error)
      alert('Erro na análise da casa. Verifique os dados inseridos.')
      setHouseAnalysis(prev => ({ ...prev, loading: false }))
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
          <TabsList className="grid w-full grid-cols-6">
            <TabsTrigger value="upload">
              <Upload className="w-4 h-4 mr-2" />
              Upload
            </TabsTrigger>
            <TabsTrigger value="analysis">
              <Leaf className="w-4 h-4 mr-2" />
              Análise
            </TabsTrigger>
            <TabsTrigger value="occupants">
              <Users className="w-4 h-4 mr-2" />
              Ocupantes
            </TabsTrigger>
            <TabsTrigger value="history">
              <Calendar className="w-4 h-4 mr-2" />
              Histórico
            </TabsTrigger>
            <TabsTrigger value="dashboard">
              <BarChart2 className="w-4 h-4 mr-2" />
              Dashboard
            </TabsTrigger>
            <TabsTrigger value="recommendations">
              <Leaf className="w-4 h-4 mr-2" />
              Recomendações
            </TabsTrigger>
            <TabsTrigger value="bazi">
              <Star className="w-4 h-4 mr-2" />
              BaZi
            </TabsTrigger>
            <TabsTrigger value="kua">
              <Compass className="w-4 h-4 mr-2" />
              Kua
            </TabsTrigger>
          </TabsList>

          {/* Aba Upload */}
          <TabsContent value="upload" className="space-y-6">
            <div className="text-center space-y-4">
              <div className="flex items-center justify-center space-x-2">
                <Upload className="w-8 h-8 text-primary" />
                <h2 className="arca-title text-3xl">Upload de Planta Baixa</h2>
              </div>
              <p className="arca-body text-lg text-muted-foreground max-w-2xl mx-auto">
                Carregue sua planta baixa para iniciar a análise ambiental.
              </p>
            </div>

            <Card className="arca-card">
              <CardHeader>
                <CardTitle className="arca-title">Carregar Arquivo</CardTitle>
                <CardDescription className="arca-body">
                  Selecione um arquivo de imagem (JPG, PNG) da sua planta baixa.
                </CardDescription>
              </CardHeader>
              <CardContent>
                <Input type="file" accept=".jpg,.jpeg,.png" onChange={handleFileUpload} className="bg-input border-border" />
              </CardContent>
            </Card>
          </TabsContent>

          {/* Aba Análise */}
          <TabsContent value="analysis" className="space-y-6">
            <div className="text-center space-y-4">
              <div className="flex items-center justify-center space-x-2">
                <Leaf className="w-8 h-8 text-primary" />
                <h2 className="arca-title text-3xl">Análise Espacial e Energética</h2>
              </div>
              <p className="arca-body text-lg text-muted-foreground max-w-2xl mx-auto">
                Visualize os resultados da análise da sua planta baixa e inicie a análise energética.
              </p>
            </div>

            {analysisResults ? (
              <div className="grid gap-6 md:grid-cols-2">
                <Card className="arca-card">
                  <CardHeader>
                    <CardTitle className="arca-title">Planta Baixa Carregada</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <img src={analysisResults.image_url} alt="Planta Baixa" className="w-full h-auto rounded-md" />
                    <p className="arca-body mt-4">Status: {analysisResults.status}</p>
                    <p className="arca-body">ID: {analysisResults.id}</p>
                  </CardContent>
                </Card>

                <Card className="arca-card">
                  <CardHeader>
                    <CardTitle className="arca-title">Análise Espacial</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <p className="arca-body"><strong>Área Total:</strong> {analysisResults.analysis.details.total_area} m²</p>
                    <p className="arca-body"><strong>Cômodos Detectados:</strong> {analysisResults.analysis.details.rooms_detected}</p>
                    <p className="arca-body"><strong>Pontos de Interesse:</strong> {analysisResults.analysis.details.poi_detected}</p>
                    <Button onClick={handleEnergeticAnalysis} className="arca-button w-full mt-4">
                      Realizar Análise Energética
                    </Button>
                    {analysisResults.energetic_analysis && (
                      <div className="mt-4">
                        <h3 className="arca-title text-lg">Resultados Energéticos:</h3>
                        <p className="arca-body"><strong>Proximidade CEM:</strong> {analysisResults.energetic_analysis.cem_proximity}</p>
                        <p className="arca-body"><strong>Anomalias Geológicas:</strong> {analysisResults.energetic_analysis.geological_anomalies}</p>
                        <p className="arca-body"><strong>Qualidade do Ar:</strong> {analysisResults.energetic_analysis.air_quality}</p>
                      </div>
                    )}
                  </CardContent>
                </Card>
              </div>
            ) : (
              <p className="arca-body text-center">Carregue uma planta baixa para ver os resultados da análise.</p>
            )}
          </TabsContent>

          {/* Aba Ocupantes */}
          <TabsContent value="occupants" className="space-y-6">
            <div className="text-center space-y-4">
              <div className="flex items-center justify-center space-x-2">
                <Users className="w-8 h-8 text-primary" />
                <h2 className="arca-title text-3xl">Perfis de Ocupantes</h2>
              </div>
              <p className="arca-body text-lg text-muted-foreground max-w-2xl mx-auto">
                Cadastre os ocupantes para análises personalizadas de compatibilidade e bem-estar.
              </p>
            </div>

            <Card className="arca-card">
              <CardHeader>
                <CardTitle className="arca-title">Cadastrar Novo Ocupante</CardTitle>
              </CardHeader>
              <CardContent>
                <form onSubmit={(e) => {
                  e.preventDefault()
                  const formData = new FormData(e.target)
                  const data = Object.fromEntries(formData.entries())
                  handleOccupantRegistration(data)
                  e.target.reset()
                }} className="space-y-4">
                  <div>
                    <Label htmlFor="name" className="arca-body">Nome</Label>
                    <Input id="name" name="name" required className="bg-input border-border" />
                  </div>
                  <div>
                    <Label htmlFor="profileType" className="arca-body">Tipo de Perfil</Label>
                    <Select name="profileType" required>
                      <SelectTrigger className="bg-input border-border">
                        <SelectValue placeholder="Selecione o tipo" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="residente">Residente</SelectItem>
                        <SelectItem value="trabalhador">Trabalhador</SelectItem>
                        <SelectItem value="visitante">Visitante</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <div>
                    <Label htmlFor="baziElement" className="arca-body">Elemento BaZi (Opcional)</Label>
                    <Input id="baziElement" name="baziElement" className="bg-input border-border" />
                  </div>
                  <div>
                    <Label htmlFor="functionEnergy" className="arca-body">Energia Funcional (Opcional)</Label>
                    <Input id="functionEnergy" name="functionEnergy" className="bg-input border-border" />
                  </div>
                  <Button type="submit" className="arca-button w-full">Cadastrar Ocupante</Button>
                </form>
              </CardContent>
            </Card>

            <Card className="arca-card">
              <CardHeader>
                <CardTitle className="arca-title">Ocupantes Cadastrados</CardTitle>
              </CardHeader>
              <CardContent>
                {occupants.length > 0 ? (
                  <ul className="space-y-2">
                    {occupants.map((occupant, index) => (
                      <li key={index} className="arca-body p-2 border rounded-md bg-secondary/20">
                        {occupant.name} ({occupant.profileType})
                      </li>
                    ))}
                  </ul>
                ) : (
                  <p className="arca-body text-center">Nenhum ocupante cadastrado ainda.</p>
                )}
              </CardContent>
            </Card>
          </TabsContent>

          {/* Aba Histórico */}
          <TabsContent value="history" className="space-y-6">
            <div className="text-center space-y-4">
              <div className="flex items-center justify-center space-x-2">
                <Calendar className="w-8 h-8 text-primary" />
                <h2 className="arca-title text-3xl">Histórico de Análises</h2>
              </div>
              <p className="arca-body text-lg text-muted-foreground max-w-2xl mx-auto">
                Visualize e gerencie o histórico de suas plantas baixas, análises energéticas e perfis de ocupantes.
              </p>
            </div>

            {/* Seção de Busca e Filtros */}
            <Card className="arca-card">
              <CardHeader>
                <CardTitle className="arca-title">Buscar e Filtrar Histórico</CardTitle>
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
                <CardTitle className="arca-title">Exportar Dados</CardTitle>
              </CardHeader>
              <CardContent>
                <ExportSection />
              </CardContent>
            </Card>

            <div className="grid gap-6 md:grid-cols-1 lg:grid-cols-3">
              {/* Histórico de Plantas Baixas */}
              <Card className="arca-card">
                <CardHeader>
                  <CardTitle className="arca-title">Plantas Baixas</CardTitle>
                </CardHeader>
                <CardContent>
                  {floorPlansHistory.length > 0 ? (
                    <ul className="space-y-2">
                      {floorPlansHistory.map((fp) => (
                        <li key={fp.id} className="arca-body p-2 border rounded-md bg-secondary/20">
                          {fp.filename} - {fp.status} ({new Date(fp.upload_date).toLocaleDateString()})
                        </li>
                      ))}
                    </ul>
                  ) : (
                    <p className="arca-body text-center">Nenhuma planta baixa no histórico.</p>
                  )}
                </CardContent>
              </Card>

              {/* Histórico de Análises Energéticas */}
              <Card className="arca-card">
                <CardHeader>
                  <CardTitle className="arca-title">Análises Energéticas</CardTitle>
                </CardHeader>
                <CardContent>
                  {energeticAnalysesHistory.length > 0 ? (
                    <ul className="space-y-2">
                      {energeticAnalysesHistory.map((ea) => (
                        <li key={ea.id} className="arca-body p-2 border rounded-md bg-secondary/20">
                          CEM: {ea.cem_proximity}, Anomalias: {ea.geological_anomalies} ({new Date(ea.analysis_date).toLocaleDateString()})
                        </li>
                      ))}
                    </ul>
                  ) : (
                    <p className="arca-body text-center">Nenhuma análise energética no histórico.</p>
                  )}
                </CardContent>
              </Card>

              {/* Histórico de Perfis de Ocupantes */}
              <Card className="arca-card">
                <CardHeader>
                  <CardTitle className="arca-title">Perfis de Ocupantes</CardTitle>
                </CardHeader>
                <CardContent>
                  {occupantsHistory.length > 0 ? (
                    <ul className="space-y-2">
                      {occupantsHistory.map((op) => (
                        <li key={op.id} className="arca-body p-2 border rounded-md bg-secondary/20">
                          {op.name} ({op.profile_type}) - Elemento BaZi: {op.bazi_element || 'N/A'}
                        </li>
                      ))}
                    </ul>
                  ) : (
                    <p className="arca-body text-center">Nenhum perfil de ocupante no histórico.</p>
                  )}
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          {/* Aba Dashboard */}
          <TabsContent value="dashboard" className="space-y-6">
            <div className="text-center space-y-4">
              <div className="flex items-center justify-center space-x-2">
                <BarChart2 className="w-8 h-8 text-primary" />
                <h2 className="arca-title text-3xl">Dashboard de Análises</h2>
              </div>
              <p className="arca-body text-lg text-muted-foreground max-w-2xl mx-auto">
                Visualize estatísticas e tendências das suas análises.
              </p>
            </div>

            <div className="grid gap-6 md:grid-cols-1 lg:grid-cols-2">
              {/* Gráfico de Barras: Plantas Baixas Carregadas por Mês */}
              <Card className="arca-card">
                <CardHeader>
                  <CardTitle className="arca-title">Plantas Baixas Carregadas por Mês</CardTitle>
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

              {/* Gráfico de Pizza: Análises Energéticas por Proximidade CEM */}
              <Card className="arca-card">
                <CardHeader>
                  <CardTitle className="arca-title">Análises Energéticas por Proximidade CEM</CardTitle>
                </CardHeader>
                <CardContent>
                  <ResponsiveContainer width="100%" height={300}>
                    <PieChart>
                      <Pie
                        data={analyticsData.energeticAnalysesByCem}
                        cx="50%"
                        cy="50%"
                        labelLine={false}
                        outerRadius={80}
                        fill="#8884d8"
                        dataKey="count"
                        nameKey="cem_proximity"
                        label={({ name, percent }) => `${name} (${(percent * 100).toFixed(0)}%)`}
                      >
                        {analyticsData.energeticAnalysesByCem.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={["#0088FE", "#00C49F", "#FFBB28", "#FF8042"][index % 4]} />
                        ))}
                      </Pie>
                      <Tooltip />
                      <Legend />
                    </PieChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>

              {/* Gráfico de Barras: Perfis de Ocupantes por Tipo */}
              <Card className="arca-card">
                <CardHeader>
                  <CardTitle className="arca-title">Perfis de Ocupantes por Tipo</CardTitle>
                </CardHeader>
                <CardContent>
                  <ResponsiveContainer width="100%" height={300}>
                    <BarChart data={analyticsData.occupantProfilesByType}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="profile_type" />
                      <YAxis />
                      <Tooltip />
                      <Legend />
                      <Bar dataKey="count" fill="#82ca9d" />
                    </BarChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          {/* Aba Recomendações */}
          <TabsContent value="recommendations" className="space-y-6">
            <div className="text-center space-y-4">
              <div className="flex items-center justify-center space-x-2">
                <Leaf className="w-8 h-8 text-primary" />
                <h2 className="arca-title text-3xl">Recomendações Holísticas</h2>
              </div>
              <p className="arca-body text-lg text-muted-foreground max-w-2xl mx-auto">
                Sugestões personalizadas para harmonizar seu ambiente
              </p>
            </div>

            <Card className="arca-card">
              <CardHeader>
                <CardTitle className="arca-title">Relatório Completo</CardTitle>
              </CardHeader>
              <CardContent>
                {analysisResults && occupants.length > 0 ? (
                  <Button onClick={handleGenerateReport} className="arca-button w-full">
                    Gerar Relatório em PDF
                  </Button>
                ) : (
                  <p className="arca-body text-center">Complete a análise espacial e cadastre ocupantes para ver recomendações personalizadas.</p>
                )}
              </CardContent>
            </Card>
          </TabsContent>

          {/* Aba BaZi */}
          <TabsContent value="bazi" className="space-y-6">
            <div className="text-center space-y-4">
              <div className="flex items-center justify-center space-x-2">
                <Star className="w-8 h-8 text-primary" />
                <h2 className="arca-title text-3xl">BaZi - Quatro Pilares do Destino</h2>
              </div>
              <p className="arca-body text-lg text-muted-foreground max-w-2xl mx-auto">
                Descubra sua personalidade energética através do sistema milenar chinês BaZi
              </p>
            </div>

            <div className="grid gap-6 md:grid-cols-2">
              {/* Formulário BaZi */}
              <Card className="arca-card">
                <CardHeader>
                  <CardTitle className="arca-title">Calcular BaZi</CardTitle>
                  <CardDescription className="arca-body">
                    Insira seus dados de nascimento para análise completa
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div>
                    <Label className="arca-body">Data e Hora de Nascimento</Label>
                    <Input
                      type="datetime-local"
                      value={baziData.birthDateTime}
                      onChange={(e) => setBaziData(prev => ({ ...prev, birthDateTime: e.target.value }))}
                      className="bg-input border-border"
                    />
                  </div>
                  <div>
                    <Label className="arca-body">Fuso Horário</Label>
                    <Select 
                      value={baziData.timezoneOffset.toString()} 
                      onValueChange={(value) => setBaziData(prev => ({ ...prev, timezoneOffset: parseInt(value) }))}
                    >
                      <SelectTrigger className="bg-input border-border">
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="-3">Brasil (UTC-3)</SelectItem>
                        <SelectItem value="-2">Fernando de Noronha (UTC-2)</SelectItem>
                        <SelectItem value="0">UTC (GMT)</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <Button 
                    onClick={calculateBaZiLocal} 
                    disabled={!baziData.birthDateTime || baziData.loading}
                    className="arca-button w-full"
                  >
                    {baziData.loading ? 'Calculando...' : 'Calcular BaZi'}
                  </Button>
                </CardContent>
              </Card>

              {/* Resultados BaZi */}
              {baziData.results && (
                <Card className="arca-card">
                  <CardHeader>
                    <CardTitle className="arca-title">Seus Quatro Pilares</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="grid grid-cols-4 gap-2 text-center">
                      <div className="p-2 bg-secondary/20 rounded">
                        <p className="arca-body text-xs font-semibold">Ano</p>
                        <p className="text-lg">{baziData.results.four_pillars.year.stem.chinese}</p>
                        <p className="text-lg">{baziData.results.four_pillars.year.branch.chinese}</p>
                        <p className="arca-body text-xs">{baziData.results.four_pillars.year.branch.zodiac}</p>
                      </div>
                      <div className="p-2 bg-secondary/20 rounded">
                        <p className="arca-body text-xs font-semibold">Mês</p>
                        <p className="text-lg">{baziData.results.four_pillars.month.stem.chinese}</p>
                        <p className="text-lg">{baziData.results.four_pillars.month.branch.chinese}</p>
                        <p className="arca-body text-xs">{baziData.results.four_pillars.month.branch.zodiac}</p>
                      </div>
                      <div className="p-2 bg-secondary/20 rounded">
                        <p className="arca-body text-xs font-semibold">Dia</p>
                        <p className="text-lg">{baziData.results.four_pillars.day.stem.chinese}</p>
                        <p className="text-lg">{baziData.results.four_pillars.day.branch.chinese}</p>
                        <p className="arca-body text-xs">{baziData.results.four_pillars.day.branch.zodiac}</p>
                      </div>
                      <div className="p-2 bg-secondary/20 rounded">
                        <p className="arca-body text-xs font-semibold">Hora</p>
                        <p className="text-lg">{baziData.results.four_pillars.hour.stem.chinese}</p>
                        <p className="text-lg">{baziData.results.four_pillars.hour.branch.chinese}</p>
                        <p className="arca-body text-xs">{baziData.results.four_pillars.hour.branch.zodiac}</p>
                      </div>
                    </div>
                    <div className="mt-4">
                      <p className="arca-body"><strong>Day Master:</strong> {baziData.results.day_master.element} ({baziData.results.day_master.polarity})</p>
                      <p className="arca-body"><strong>Força:</strong> {baziData.results.day_master.strength}</p>
                      <p className="arca-body"><strong>Elemento Útil:</strong> {baziData.results.useful_god.element}</p>
                      <p className="arca-body"><strong>Cores Favoráveis:</strong> {baziData.results.recommendations.favorable_colors.join(', ')}</p>
                      <p className="arca-body"><strong>Direções Favoráveis:</strong> {baziData.results.recommendations.favorable_directions.join(', ')}</p>
                    </div>
                  </CardContent>
                </Card>
              )}
            </div>
          </TabsContent>

          {/* Aba Kua */}
          <TabsContent value="kua" className="space-y-6">
            <div className="text-center space-y-4">
              <div className="flex items-center justify-center space-x-2">
                <Compass className="w-8 h-8 text-primary" />
                <h2 className="arca-title text-3xl">Kua - Ba Zhai (Oito Casas)</h2>
              </div>
              <p className="arca-body text-lg text-muted-foreground max-w-2xl mx-auto">
                Calcule seu Número Kua e descubra suas direções favoráveis e desfavoráveis.
              </p>
            </div>

            <div className="grid gap-6 md:grid-cols-2">
              {/* Formulário Kua */}
              <Card className="arca-card">
                <CardHeader>
                  <CardTitle className="arca-title">Calcular Kua</CardTitle>
                  <CardDescription className="arca-body">
                    Insira seu ano de nascimento e gênero para análise
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div>
                    <Label className="arca-body">Ano de Nascimento</Label>
                    <Input
                      type="number"
                      value={kuaData.birthYear}
                      onChange={(e) => setKuaData(prev => ({ ...prev, birthYear: e.target.value }))}
                      className="bg-input border-border"
                      placeholder="Ex: 1985"
                    />
                  </div>
                  <div>
                    <Label className="arca-body">Gênero</Label>
                    <Select 
                      value={kuaData.gender}
                      onValueChange={(value) => setKuaData(prev => ({ ...prev, gender: value }))}
                    >
                      <SelectTrigger className="bg-input border-border">
                        <SelectValue placeholder="Selecione o gênero" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="male">Masculino</SelectItem>
                        <SelectItem value="female">Feminino</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <Button 
                    onClick={calculateKuaLocal} 
                    disabled={!kuaData.birthYear || !kuaData.gender || kuaData.loading}
                    className="arca-button w-full"
                  >
                    {kuaData.loading ? 'Calculando...' : 'Calcular Kua'}
                  </Button>
                </CardContent>
              </Card>

              {/* Resultados Kua */}
              {kuaData.results && (
                <Card className="arca-card">
                  <CardHeader>
                    <CardTitle className="arca-title">Seu Número Kua e Direções</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <p className="arca-body"><strong>Número Kua:</strong> {kuaData.results.kua_number}</p>
                    <p className="arca-body"><strong>Grupo:</strong> {kuaData.results.characteristics.group}</p>
                    <p className="arca-body"><strong>Elemento:</strong> {kuaData.results.characteristics.element}</p>
                    <p className="arca-body"><strong>Personalidade:</strong> {kuaData.results.characteristics.personality}</p>
                    
                    <h3 className="arca-title text-lg mt-4">Direções Favoráveis:</h3>
                    <div className="grid grid-cols-2 gap-2">
                      <p className="arca-body"><strong>Sheng Qi:</strong> {kuaData.results.favorable_directions.sheng_qi}</p>
                      <p className="arca-body"><strong>Tian Yi:</strong> {kuaData.results.favorable_directions.tian_yi}</p>
                      <p className="arca-body"><strong>Nian Yan:</strong> {kuaData.results.favorable_directions.nian_yan}</p>
                      <p className="arca-body"><strong>Fu Wei:</strong> {kuaData.results.favorable_directions.fu_wei}</p>
                    </div>
                    
                    <h3 className="arca-title text-lg mt-4">Cores Favoráveis:</h3>
                    <p className="arca-body">{kuaData.results.feng_shui_recommendations.colors.join(', ')}</p>
                  </CardContent>
                </Card>
              )}
            </div>

            {/* Análise de Compatibilidade da Casa */}
            <Card className="arca-card">
              <CardHeader>
                <CardTitle className="arca-title">Análise de Compatibilidade da Casa</CardTitle>
                <CardDescription className="arca-body">
                  Verifique a compatibilidade da sua casa com seu Número Kua.
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <Label className="arca-body">Direção da Frente da Casa</Label>
                  <Select 
                    value={houseAnalysis.facingDirection}
                    onValueChange={(value) => setHouseAnalysis(prev => ({ ...prev, facingDirection: value }))}
                  >
                    <SelectTrigger className="bg-input border-border">
                      <SelectValue placeholder="Selecione a direção" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="Norte">Norte</SelectItem>
                      <SelectItem value="Nordeste">Nordeste</SelectItem>
                      <SelectItem value="Leste">Leste</SelectItem>
                      <SelectItem value="Sudeste">Sudeste</SelectItem>
                      <SelectItem value="Sul">Sul</SelectItem>
                      <SelectItem value="Sudoeste">Sudoeste</SelectItem>
                      <SelectItem value="Oeste">Oeste</SelectItem>
                      <SelectItem value="Noroeste">Noroeste</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <Button 
                  onClick={analyzeHouseCompatibilityLocal} 
                  disabled={!houseAnalysis.facingDirection || !kuaData.birthYear || !kuaData.gender || houseAnalysis.loading}
                  className="arca-button w-full"
                >
                  {houseAnalysis.loading ? 'Analisando...' : 'Analisar Compatibilidade da Casa'}
                </Button>
                {houseAnalysis.results && (
                  <div className="mt-4">
                    <p className="arca-body"><strong>Compatibilidade:</strong> {houseAnalysis.results.compatibility_level}</p>
                    <p className="arca-body"><strong>Recomendação:</strong> {houseAnalysis.results.advice}</p>
                  </div>
                )}
              </CardContent>
            </Card>
          </TabsContent>

        </Tabs>
      </main>

      {/* Footer */}
      <footer className="border-t border-border bg-card py-4 text-center text-muted-foreground">
        <p className="arca-body">&copy; {new Date().getFullYear()} ARCA. Todos os direitos reservados.</p>
      </footer>
    </div>
  )
}

// Componente de Busca e Filtros (mantido do código anterior)
const SearchFilters = ({ onFloorPlanSearch, onEnergeticAnalysisSearch, onOccupantProfileSearch }) => {
  const [activeFilterTab, setActiveFilterTab] = useState('floor_plans')
  const [floorPlanFilters, setFloorPlanFilters] = useState({
    filename: '',
    status: '',
    dateFrom: '',
    dateTo: ''
  })
  const [energeticAnalysisFilters, setEnergeticAnalysisFilters] = useState({
    cemProximity: '',
    geologicalAnomalies: '',
    dateFrom: '',
    dateTo: '',
    latitudeMin: '',
    latitudeMax: '',
    longitudeMin: '',
    longitudeMax: ''
  })
  const [occupantProfileFilters, setOccupantProfileFilters] = useState({
    name: '',
    profileType: '',
    dateFrom: '',
    dateTo: '',
    baziElement: '',
    functionEnergy: ''
  })

  const handleFloorPlanChange = (e) => {
    const { name, value } = e.target
    setFloorPlanFilters(prev => ({ ...prev, [name]: value }))
  }

  const handleEnergeticAnalysisChange = (e) => {
    const { name, value } = e.target
    setEnergeticAnalysisFilters(prev => ({ ...prev, [name]: value }))
  }

  const handleOccupantProfileChange = (e) => {
    const { name, value } = e.target
    setOccupantProfileFilters(prev => ({ ...prev, [name]: value }))
  }

  const handleFloorPlanSubmit = (e) => {
    e.preventDefault()
    onFloorPlanSearch(floorPlanFilters)
  }

  const handleEnergeticAnalysisSubmit = (e) => {
    e.preventDefault()
    onEnergeticAnalysisSearch(energeticAnalysisFilters)
  }

  const handleOccupantProfileSubmit = (e) => {
    e.preventDefault()
    onOccupantProfileSearch(occupantProfileFilters)
  }

  return (
    <Tabs value={activeFilterTab} onValueChange={setActiveFilterTab} className="w-full">
      <TabsList className="grid w-full grid-cols-3">
        <TabsTrigger value="floor_plans">Plantas Baixas</TabsTrigger>
        <TabsTrigger value="energetic_analyses">Análises Energéticas</TabsTrigger>
        <TabsTrigger value="occupant_profiles">Perfis de Ocupantes</TabsTrigger>
      </TabsList>

      <TabsContent value="floor_plans" className="space-y-4 mt-4">
        <form onSubmit={handleFloorPlanSubmit} className="space-y-4">
          <div>
            <Label htmlFor="filename">Nome do Arquivo</Label>
            <Input id="filename" name="filename" value={floorPlanFilters.filename} onChange={handleFloorPlanChange} />
          </div>
          <div>
            <Label htmlFor="status">Status</Label>
            <Select name="status" value={floorPlanFilters.status} onValueChange={(value) => setFloorPlanFilters(prev => ({ ...prev, status: value }))}>
              <SelectTrigger>
                <SelectValue placeholder="Selecione o status" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="">Todos</SelectItem>
                <SelectItem value="processado">Processado</SelectItem>
                <SelectItem value="pendente">Pendente</SelectItem>
                <SelectItem value="erro">Erro</SelectItem>
              </SelectContent>
            </Select>
          </div>
          <div>
            <Label htmlFor="dateFrom">Data Inicial</Label>
            <Input type="date" id="dateFrom" name="dateFrom" value={floorPlanFilters.dateFrom} onChange={handleFloorPlanChange} />
          </div>
          <div>
            <Label htmlFor="dateTo">Data Final</Label>
            <Input type="date" id="dateTo" name="dateTo" value={floorPlanFilters.dateTo} onChange={handleFloorPlanChange} />
          </div>
          <Button type="submit">Buscar Plantas Baixas</Button>
        </form>
      </TabsContent>

      <TabsContent value="energetic_analyses" className="space-y-4 mt-4">
        <form onSubmit={handleEnergeticAnalysisSubmit} className="space-y-4">
          <div>
            <Label htmlFor="cemProximity">Proximidade CEM</Label>
            <Input id="cemProximity" name="cemProximity" value={energeticAnalysisFilters.cemProximity} onChange={handleEnergeticAnalysisChange} />
          </div>
          <div>
            <Label htmlFor="geologicalAnomalies">Anomalias Geológicas</Label>
            <Input id="geologicalAnomalies" name="geologicalAnomalies" value={energeticAnalysisFilters.geologicalAnomalies} onChange={handleEnergeticAnalysisChange} />
          </div>
          <div>
            <Label htmlFor="eaDateFrom">Data Inicial</Label>
            <Input type="date" id="eaDateFrom" name="dateFrom" value={energeticAnalysisFilters.dateFrom} onChange={handleEnergeticAnalysisChange} />
          </div>
          <div>
            <Label htmlFor="eaDateTo">Data Final</Label>
            <Input type="date" id="eaDateTo" name="dateTo" value={energeticAnalysisFilters.dateTo} onChange={handleEnergeticAnalysisChange} />
          </div>
          <div>
            <Label htmlFor="latitudeMin">Latitude Mínima</Label>
            <Input type="number" step="any" id="latitudeMin" name="latitudeMin" value={energeticAnalysisFilters.latitudeMin} onChange={handleEnergeticAnalysisChange} />
          </div>
          <div>
            <Label htmlFor="latitudeMax">Latitude Máxima</Label>
            <Input type="number" step="any" id="latitudeMax" name="latitudeMax" value={energeticAnalysisFilters.latitudeMax} onChange={handleEnergeticAnalysisChange} />
          </div>
          <div>
            <Label htmlFor="longitudeMin">Longitude Mínima</Label>
            <Input type="number" step="any" id="longitudeMin" name="longitudeMin" value={energeticAnalysisFilters.longitudeMin} onChange={handleEnergeticAnalysisChange} />
          </div>
          <div>
            <Label htmlFor="longitudeMax">Longitude Máxima</Label>
            <Input type="number" step="any" id="longitudeMax" name="longitudeMax" value={energeticAnalysisFilters.longitudeMax} onChange={handleEnergeticAnalysisChange} />
          </div>
          <Button type="submit">Buscar Análises Energéticas</Button>
        </form>
      </TabsContent>

      <TabsContent value="occupant_profiles" className="space-y-4 mt-4">
        <form onSubmit={handleOccupantProfileSubmit} className="space-y-4">
          <div>
            <Label htmlFor="occupantName">Nome do Ocupante</Label>
            <Input id="occupantName" name="name" value={occupantProfileFilters.name} onChange={handleOccupantProfileChange} />
          </div>
          <div>
            <Label htmlFor="profileTypeFilter">Tipo de Perfil</Label>
            <Select name="profileType" value={occupantProfileFilters.profileType} onValueChange={(value) => setOccupantProfileFilters(prev => ({ ...prev, profileType: value }))}>
              <SelectTrigger>
                <SelectValue placeholder="Selecione o tipo" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="">Todos</SelectItem>
                <SelectItem value="residente">Residente</SelectItem>
                <SelectItem value="trabalhador">Trabalhador</SelectItem>
                <SelectItem value="visitante">Visitante</SelectItem>
              </SelectContent>
            </Select>
          </div>
          <div>
            <Label htmlFor="opDateFrom">Data Inicial</Label>
            <Input type="date" id="opDateFrom" name="dateFrom" value={occupantProfileFilters.dateFrom} onChange={handleOccupantProfileChange} />
          </div>
          <div>
            <Label htmlFor="opDateTo">Data Final</Label>
            <Input type="date" id="opDateTo" name="dateTo" value={occupantProfileFilters.dateTo} onChange={handleOccupantProfileChange} />
          </div>
          <div>
            <Label htmlFor="baziElementFilter">Elemento BaZi</Label>
            <Input id="baziElementFilter" name="baziElement" value={occupantProfileFilters.baziElement} onChange={handleOccupantProfileChange} />
          </div>
          <div>
            <Label htmlFor="functionEnergyFilter">Energia Funcional</Label>
            <Input id="functionEnergyFilter" name="functionEnergy" value={occupantProfileFilters.functionEnergy} onChange={handleOccupantProfileChange} />
          </div>
          <Button type="submit">Buscar Perfis de Ocupantes</Button>
        </form>
      </TabsContent>
    </Tabs>
  )
}

// Componente de Exportação (mantido do código anterior)
const ExportSection = () => {
  const [exportType, setExportType] = useState('floor_plans')
  const [exportFormat, setExportFormat] = useState('json')
  const [loading, setLoading] = useState(false)

  const handleExport = async () => {
    setLoading(true)
    try {
      const response = await fetch(`https://5000-i4jzvyj6hn9qmdbabo0f4-393f986f.manusvm.computer/export/${exportType}?format=${exportFormat}`)
      if (response.ok) {
        const blob = await response.blob()
        const url = window.URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = `${exportType}.${exportFormat}`
        document.body.appendChild(a)
        a.click()
        a.remove()
        window.URL.revokeObjectURL(url)
      } else {
        const errorData = await response.json()
        alert(`Erro ao exportar: ${errorData.message}`)
      }
    } catch (error) {
      console.error('Erro na exportação:', error)
      alert('Erro na conexão. Verifique se o servidor está funcionando.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-4">
      <div>
        <Label htmlFor="exportType">Tipo de Dado para Exportar</Label>
        <Select value={exportType} onValueChange={setExportType}>
          <SelectTrigger>
            <SelectValue placeholder="Selecione o tipo" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="floor_plans">Plantas Baixas</SelectItem>
            <SelectItem value="energetic_analyses">Análises Energéticas</SelectItem>
            <SelectItem value="occupant_profiles">Perfis de Ocupantes</SelectItem>
          </SelectContent>
        </Select>
      </div>
      <div>
        <Label htmlFor="exportFormat">Formato de Exportação</Label>
        <Select value={exportFormat} onValueChange={setExportFormat}>
          <SelectTrigger>
            <SelectValue placeholder="Selecione o formato" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="json">JSON</SelectItem>
            <SelectItem value="csv">CSV</SelectItem>
          </SelectContent>
        </Select>
      </div>
      <Button onClick={handleExport} disabled={loading}>
        {loading ? 'Exportando...' : 'Exportar Dados'}
      </Button>
    </div>
  )
}

export default App



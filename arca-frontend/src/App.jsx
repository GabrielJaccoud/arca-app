import { useState } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Label } from '@/components/ui/label.jsx'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs.jsx'
import { Upload, Home, Leaf, Circle, MapPin, User, Users } from 'lucide-react'
import arcaLogo from './assets/LOGO.png'
import './App.css'

function App() {
  const [activeTab, setActiveTab] = useState('upload')
  const [floorPlanFile, setFloorPlanFile] = useState(null)
  const [analysisResults, setAnalysisResults] = useState(null)
  const [occupants, setOccupants] = useState([])

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
          floor_plan_data: analysisResults?.details || {}
        })
      })
      const result = await response.json()
      setAnalysisResults(prev => ({ ...prev, energetic_analysis: result }))
    } catch (error) {
      console.error('Erro na análise energética:', error)
    }
  }

  const handleOccupantRegistration = async (occupantData) => {
    try {
      const response = await fetch('https://5000-i4jzvyj6hn9qmdbabo0f4-393f986f.manusvm.computer/register_occupant', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(occupantData)
      })
      const result = await response.json()
      setOccupants(prev => [...prev, result.profile])
    } catch (error) {
      console.error('Erro no cadastro de ocupante:', error)
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
          <TabsList className="grid w-full grid-cols-4 bg-card">
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
                      <p className="arca-body">Arquivo: {analysisResults.details?.file_type}</p>
                      <p className="arca-body">Dimensões identificadas: {analysisResults.details?.simulated_elements?.dimensions_identified ? '✓' : '✗'}</p>
                      <p className="arca-body">Bagua sobreposto: {analysisResults.details?.simulated_bagua_superposition ? '✓' : '✗'}</p>
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
                      <div className="mt-4 space-y-2">
                        <p className="arca-body">CEM: {analysisResults.energetic_analysis.geographical_analysis?.data?.cem_proximity}</p>
                        <p className="arca-body">Anomalias geológicas: {analysisResults.energetic_analysis.geographical_analysis?.data?.geological_anomalies}</p>
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


import { useState } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Label } from '@/components/ui/label.jsx'
import { Textarea } from '@/components/ui/textarea.jsx'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select.jsx'
import { Separator } from '@/components/ui/separator.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Loader2, Sparkles, Moon, Sun, Star } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'
import './App.css'

// Configuração da API
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

function App() {
  const [pergunta, setPergunta] = useState('')
  const [dadosNascimento, setDadosNascimento] = useState({
    nome: '',
    data_nascimento: '',
    hora_nascimento: '',
    local_nascimento: ''
  })
  const [vozGuru, setVozGuru] = useState('companheira')
  const [incluirAstrologia, setIncluirAstrologia] = useState(false)
  const [resposta, setResposta] = useState(null)
  const [carregando, setCarregando] = useState(false)
  const [erro, setErro] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    if (!pergunta.trim()) {
      setErro('Por favor, faça uma pergunta para o Tarot.')
      return
    }

    setCarregando(true)
    setErro('')
    setResposta(null)

    try {
      const payload = {
        pergunta: pergunta.trim(),
        voz_guru: vozGuru
      }

      // Incluir dados de nascimento se solicitado e preenchido
      if (incluirAstrologia && dadosNascimento.nome && dadosNascimento.data_nascimento) {
        payload.dados_nascimento = dadosNascimento
      }

      const response = await fetch(`${API_BASE_URL}/consulta-tarot`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload)
      })

      if (!response.ok) {
        throw new Error(`Erro ${response.status}: ${response.statusText}`)
      }

      const data = await response.json()
      setResposta(data)
    } catch (error) {
      console.error('Erro na consulta:', error)
      setErro('Não foi possível realizar a consulta. Tente novamente.')
    } finally {
      setCarregando(false)
    }
  }

  const resetForm = () => {
    setPergunta('')
    setDadosNascimento({
      nome: '',
      data_nascimento: '',
      hora_nascimento: '',
      local_nascimento: ''
    })
    setResposta(null)
    setErro('')
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900 text-white">
      {/* Header */}
      <header className="text-center py-8 px-4">
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
        >
          <div className="flex items-center justify-center gap-3 mb-4">
            <Sparkles className="w-8 h-8 text-yellow-400" />
            <h1 className="text-4xl md:text-5xl font-bold bg-gradient-to-r from-yellow-400 to-purple-400 bg-clip-text text-transparent">
              Tarot com IA
            </h1>
            <Sparkles className="w-8 h-8 text-yellow-400" />
          </div>
          <p className="text-xl text-purple-200 max-w-2xl mx-auto">
            Sua jornada de autoconhecimento guiada pela sabedoria ancestral e inteligência artificial
          </p>
        </motion.div>
      </header>

      <div className="container mx-auto px-4 pb-8">
        <div className="grid lg:grid-cols-2 gap-8 max-w-6xl mx-auto">
          {/* Formulário de Consulta */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8, delay: 0.2 }}
          >
            <Card className="bg-white/10 backdrop-blur-md border-white/20 text-white">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Moon className="w-5 h-5 text-purple-300" />
                  Faça sua Pergunta
                </CardTitle>
                <CardDescription className="text-purple-200">
                  Concentre-se em sua questão e permita que as cartas revelem os caminhos
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                <form onSubmit={handleSubmit} className="space-y-4">
                  {/* Pergunta */}
                  <div>
                    <Label htmlFor="pergunta" className="text-purple-200">Sua Pergunta</Label>
                    <Textarea
                      id="pergunta"
                      placeholder="O que você gostaria de saber? Seja específico em sua questão..."
                      value={pergunta}
                      onChange={(e) => setPergunta(e.target.value)}
                      className="bg-white/10 border-white/30 text-white placeholder:text-purple-300 min-h-[100px]"
                      disabled={carregando}
                    />
                  </div>

                  {/* Voz da Guru */}
                  <div>
                    <Label className="text-purple-200">Estilo da Guru</Label>
                    <Select value={vozGuru} onValueChange={setVozGuru} disabled={carregando}>
                      <SelectTrigger className="bg-white/10 border-white/30 text-white">
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="companheira">Companheira - Acolhedora e empática</SelectItem>
                        <SelectItem value="mistica">Mística - Misteriosa e profunda</SelectItem>
                        <SelectItem value="sábia">Sábia - Reflexiva e inspiradora</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>

                  {/* Opção de Astrologia */}
                  <div className="flex items-center space-x-2">
                    <input
                      type="checkbox"
                      id="incluir-astrologia"
                      checked={incluirAstrologia}
                      onChange={(e) => setIncluirAstrologia(e.target.checked)}
                      className="rounded border-white/30"
                      disabled={carregando}
                    />
                    <Label htmlFor="incluir-astrologia" className="text-purple-200">
                      Incluir elementos astrológicos na interpretação
                    </Label>
                  </div>

                  {/* Dados de Nascimento (condicional) */}
                  <AnimatePresence>
                    {incluirAstrologia && (
                      <motion.div
                        initial={{ opacity: 0, height: 0 }}
                        animate={{ opacity: 1, height: 'auto' }}
                        exit={{ opacity: 0, height: 0 }}
                        className="space-y-4 border-t border-white/20 pt-4"
                      >
                        <div className="flex items-center gap-2 mb-2">
                          <Star className="w-4 h-4 text-yellow-400" />
                          <span className="text-sm text-purple-200">Dados Astrológicos</span>
                        </div>
                        
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                          <div>
                            <Label htmlFor="nome" className="text-purple-200">Nome</Label>
                            <Input
                              id="nome"
                              placeholder="Seu nome"
                              value={dadosNascimento.nome}
                              onChange={(e) => setDadosNascimento(prev => ({...prev, nome: e.target.value}))}
                              className="bg-white/10 border-white/30 text-white placeholder:text-purple-300"
                              disabled={carregando}
                            />
                          </div>
                          <div>
                            <Label htmlFor="local" className="text-purple-200">Local de Nascimento</Label>
                            <Input
                              id="local"
                              placeholder="Cidade, País"
                              value={dadosNascimento.local_nascimento}
                              onChange={(e) => setDadosNascimento(prev => ({...prev, local_nascimento: e.target.value}))}
                              className="bg-white/10 border-white/30 text-white placeholder:text-purple-300"
                              disabled={carregando}
                            />
                          </div>
                          <div>
                            <Label htmlFor="data" className="text-purple-200">Data de Nascimento</Label>
                            <Input
                              id="data"
                              type="date"
                              value={dadosNascimento.data_nascimento}
                              onChange={(e) => setDadosNascimento(prev => ({...prev, data_nascimento: e.target.value}))}
                              className="bg-white/10 border-white/30 text-white"
                              disabled={carregando}
                            />
                          </div>
                          <div>
                            <Label htmlFor="hora" className="text-purple-200">Hora de Nascimento</Label>
                            <Input
                              id="hora"
                              type="time"
                              value={dadosNascimento.hora_nascimento}
                              onChange={(e) => setDadosNascimento(prev => ({...prev, hora_nascimento: e.target.value}))}
                              className="bg-white/10 border-white/30 text-white"
                              disabled={carregando}
                            />
                          </div>
                        </div>
                      </motion.div>
                    )}
                  </AnimatePresence>

                  {/* Botões */}
                  <div className="flex gap-3 pt-4">
                    <Button 
                      type="submit" 
                      disabled={carregando || !pergunta.trim()}
                      className="flex-1 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700"
                    >
                      {carregando ? (
                        <>
                          <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                          Consultando as cartas...
                        </>
                      ) : (
                        <>
                          <Sparkles className="w-4 h-4 mr-2" />
                          Consultar Tarot
                        </>
                      )}
                    </Button>
                    
                    {resposta && (
                      <Button 
                        type="button" 
                        variant="outline" 
                        onClick={resetForm}
                        className="border-white/30 text-white hover:bg-white/10"
                      >
                        Nova Consulta
                      </Button>
                    )}
                  </div>
                </form>

                {/* Erro */}
                {erro && (
                  <motion.div
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="p-3 bg-red-500/20 border border-red-500/30 rounded-lg text-red-200"
                  >
                    {erro}
                  </motion.div>
                )}
              </CardContent>
            </Card>
          </motion.div>

          {/* Resultado da Consulta */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8, delay: 0.4 }}
          >
            <AnimatePresence mode="wait">
              {resposta ? (
                <motion.div
                  key="resposta"
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -20 }}
                  transition={{ duration: 0.5 }}
                >
                  <Card className="bg-white/10 backdrop-blur-md border-white/20 text-white">
                    <CardHeader>
                      <CardTitle className="flex items-center gap-2">
                        <Sun className="w-5 h-5 text-yellow-400" />
                        Sua Leitura de Tarot
                      </CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-6">
                      {/* Cartas */}
                      <div>
                        <h3 className="text-lg font-semibold mb-3 text-purple-200">Cartas Reveladas</h3>
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                          {resposta.cartas.map((carta, index) => (
                            <motion.div
                              key={index}
                              initial={{ opacity: 0, rotateY: 180 }}
                              animate={{ opacity: 1, rotateY: 0 }}
                              transition={{ duration: 0.6, delay: index * 0.2 }}
                              className="bg-gradient-to-br from-purple-600/30 to-blue-600/30 p-4 rounded-lg border border-white/20"
                            >
                              <Badge variant="secondary" className="mb-2 bg-white/20 text-white">
                                {carta.posicao}
                              </Badge>
                              <h4 className="font-bold text-yellow-300 mb-1">{carta.nome}</h4>
                              <p className="text-sm text-purple-200">{carta.significado_geral}</p>
                            </motion.div>
                          ))}
                        </div>
                      </div>

                      <Separator className="bg-white/20" />

                      {/* Elementos Astrológicos */}
                      {resposta.elementos_astrologicos && (
                        <div>
                          <h3 className="text-lg font-semibold mb-3 text-purple-200 flex items-center gap-2">
                            <Star className="w-5 h-5 text-yellow-400" />
                            Elementos Astrológicos
                          </h3>
                          <div className="grid grid-cols-1 md:grid-cols-3 gap-3 mb-4">
                            <div className="bg-white/5 p-3 rounded-lg">
                              <span className="text-yellow-300 font-semibold">Sol:</span>
                              <span className="ml-2">{resposta.elementos_astrologicos.sol.signo}</span>
                            </div>
                            <div className="bg-white/5 p-3 rounded-lg">
                              <span className="text-blue-300 font-semibold">Lua:</span>
                              <span className="ml-2">{resposta.elementos_astrologicos.lua.signo}</span>
                            </div>
                            <div className="bg-white/5 p-3 rounded-lg">
                              <span className="text-purple-300 font-semibold">Ascendente:</span>
                              <span className="ml-2">{resposta.elementos_astrologicos.ascendente}</span>
                            </div>
                          </div>
                        </div>
                      )}

                      {/* Interpretação */}
                      <div>
                        <h3 className="text-lg font-semibold mb-3 text-purple-200">Interpretação da Guru</h3>
                        <div className="bg-white/5 p-4 rounded-lg">
                          <p className="text-purple-100 leading-relaxed whitespace-pre-wrap">
                            {resposta.interpretacao}
                          </p>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                </motion.div>
              ) : (
                <motion.div
                  key="placeholder"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                  className="flex items-center justify-center h-96"
                >
                  <div className="text-center text-purple-300">
                    <Sparkles className="w-16 h-16 mx-auto mb-4 opacity-50" />
                    <p className="text-lg">As cartas aguardam sua pergunta...</p>
                    <p className="text-sm mt-2 opacity-75">Concentre-se em sua questão e deixe a magia acontecer</p>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </motion.div>
        </div>
      </div>
    </div>
  )
}

export default App

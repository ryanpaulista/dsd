<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const produtos = ref([])
const produtoSelecionado = ref(null)
const freteResultado = ref(null)
const carregando = ref(false)
const cepInput = ref('')
const pesoInput = ref('') 

const GATEWAY_URL = import.meta.env.VITE_GATEWAY_URL
const WSDL_URL = import.meta.env.VITE_WSDL_URL
const DOCS_URL = import.meta.env.VITE_DOCS_URL
console.log(DOCS_URL);

const carregarProdutos = async () => {
  try {
    const response = await axios.get(GATEWAY_URL)
    produtos.value = response.data
  } catch (error) {
    alert('Erro ao conectar com o Gateway: ' + error.message)
  }
}

const verDetalhes = async (id) => {
  try {
    const response = await axios.get(`${GATEWAY_URL}/${id}`)
    produtoSelecionado.value = response.data
    freteResultado.value = null 
  } catch (error) {
    alert('Erro ao carregar produto.')
  }
}

const fecharDetalhes = () => {
  produtoSelecionado.value = null
}

const calcularFrete = async () => {
  if (!produtoSelecionado.value || !cepInput.value) {
    alert("Digite um CEP!")
    return
  }

  const linkFrete = produtoSelecionado.value.links.find(link => link.rel === 'calcular_frete')

  if (!linkFrete) {
    alert("Erro HATEOAS: Link não encontrado.")
    return
  }

  carregando.value = true
  try {
    const pesoDoProduto = produtoSelecionado.value.peso

    console.log(`Calculando frete para peso: ${pesoDoProduto}g`) 

    const response = await axios({
      method: linkFrete.method,
      url: linkFrete.href,
      data: { 
        cep: cepInput.value, 
        peso: pesoDoProduto 
      }
    })
    
    freteResultado.value = response.data.dados 
  } catch (error) {
    console.error(error)
    alert('Erro ao calcular frete.')
  } finally {
    carregando.value = false
  }
}

onMounted(() => {
  carregarProdutos()
})
</script>

<template>
  <div class="container">
    <header>
      <h1>🧠 Brainz E-Shop</h1>
      <p>Arquitetura Distribuída: Vue ↔ Gateway/FastAPI ↔ (Django + Node/Express -> Spyne/SOAP)</p>
    </header>

    <div v-if="!produtoSelecionado" class="grid">
      <div v-for="produto in produtos" :key="produto.id" class="card">
        <div class="card-img" :style="{ backgroundImage: 'url(' + produto.imagem_url + ')' }"></div>
        <div class="card-body">
          <h3>{{ produto.nome }}</h3>
          <p class="price">R$ {{ produto.preco }}</p>
          <button @click="verDetalhes(produto.id)">Ver Detalhes</button>
        </div>
      </div>
    </div>

    <div v-else class="detail-view">
      <button class="back-btn" @click="fecharDetalhes">← Voltar</button>
      
      <div class="detail-card">
        <h2>{{ produtoSelecionado.nome }}</h2>
        <p>{{ produtoSelecionado.descricao }}</p>
        <p class="price-lg">R$ {{ produtoSelecionado.preco }}</p>
        <p style="color: #666; font-size: 0.9em;">
          Peso unitário: <strong>{{ produtoSelecionado.peso }} g</strong>
        </p>

        <hr>

        <div class="frete-area">
          <div class="header-soap">
            <h3>Simular Frete (SOAP)</h3>
            <a :href="WSDL_URL" target="_blank" class="wsdl-link">📄 Visualizar WSDL</a>
          </div>

          <div class="input-group">
            <input v-model="cepInput" placeholder="Digite o CEP (ex: 01001000)" />
            <button @click="calcularFrete" :disabled="carregando">
              {{ carregando ? 'Calculando...' : 'Calcular' }}
            </button>
          </div>

          <div v-if="freteResultado" class="result-box">
            <p><strong>Valor:</strong> R$ {{ freteResultado.valor }}</p>
            <p><strong>Prazo:</strong> {{ freteResultado.prazo }}</p>
            <p v-if="freteResultado.obs"><em>Obs: {{ freteResultado.obs }}</em></p>
          </div>
        </div>
      </div>

      <div class="debug-box">
        <h4>🔍 HATEOAS Links (Recebidos da API):</h4>
        <pre>{{ produtoSelecionado.links }}</pre>
      </div>
    </div>
  </div>
</template>

<style scoped>
.container { max-width: 800px; margin: 0 auto; }
header { text-align: center; margin-bottom: 40px; }

.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 20px; }
.card { background: white; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); overflow: hidden; transition: transform 0.2s; }
.card:hover { transform: translateY(-5px); }
.card-img { height: 150px; background-color: #ddd; background-size: cover; background-position: center; }
.card-body { padding: 15px; text-align: center; }
.price { color: #2c3e50; font-weight: bold; font-size: 1.2em; }
button { background-color: #42b983; color: white; border: none; padding: 10px 20px; border-radius: 5px; font-weight: bold; }
button:hover { background-color: #3aa876; }
button:disabled { background-color: #ccc; }

.detail-view { animation: fadeIn 0.3s; }
.back-btn { background-color: #666; margin-bottom: 20px; }
.detail-card { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
.price-lg { font-size: 2em; color: #42b983; font-weight: bold; }

.frete-area { background-color: #f8f9fa; padding: 20px; border-radius: 8px; margin-top: 20px; }
.header-soap { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
.wsdl-link { font-size: 0.9em; color: #42b983; text-decoration: none; border: 1px solid #42b983; padding: 5px 10px; border-radius: 4px; transition: all 0.2s; }
.wsdl-link:hover { background-color: #42b983; color: white; }

.input-group { display: flex; gap: 10px; margin-bottom: 10px; }
input { padding: 10px; border: 1px solid #ddd; border-radius: 5px; flex: 1; }
.result-box { background-color: #e8f5e9; padding: 15px; border-radius: 5px; border-left: 5px solid #42b983; }

.debug-box { margin-top: 30px; background: #2c3e50; color: #00ff00; padding: 15px; border-radius: 5px; font-family: monospace; font-size: 0.8em; }

@keyframes fadeIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
</style>
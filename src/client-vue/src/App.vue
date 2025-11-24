<template>
  <div class="container">
    <h1>📦 Dashboard de Logística</h1>
    
    <div :class="['status-ws', wsConnected ? 'online' : 'offline']">
      WebSocket: {{ wsConnected ? 'Conectado 🟢' : 'Desconectado 🔴' }}
    </div>

    <div class="card">
      <h2>Consultar Pedido (Via SOAP)</h2>
      <div class="search-box">
        <input v-model="pedidoId" type="number" placeholder="ID do Pedido (ex: 1)" />
        <button @click="buscarPedido" :disabled="loading">
          {{ loading ? 'Buscando...' : 'Rastrear' }}
        </button>
      </div>
      <p v-if="error" class="error">{{ error }}</p>
    </div>

    <div v-if="pedido" class="card result">
      <h3>Detalhes do Pedido #{{ pedido.id }}</h3>
      <p><strong>Item:</strong> {{ pedido.item }}</p>
      <p><strong>Status Atual:</strong> <span class="badge">{{ pedido.status }}</span></p>
      
      <div class="hateoas">
        <h4>🔗 Ações Disponíveis (HATEOAS):</h4>
        <ul>
          <li v-for="link in pedido.links" :key="link.rel">
            <span class="method">{{ link.type }}</span> 
            <a :href="link.href" target="_blank">{{ link.rel }}</a>
          </li>
        </ul>
      </div>
    </div>

    <div class="card terminal">
      <h3>📡 Eventos em Tempo Real (WebSocket)</h3>
      <div class="logs">
        <div v-for="(log, index) in logs" :key="index" class="log-item">
          > {{ log }}
        </div>
      </div>
      <button @click="enviarPing" class="btn-small">Testar Conexão</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

// Variáveis de Estado
const pedidoId = ref(1);
const pedido = ref(null);
const loading = ref(false);
const error = ref(null);
const logs = ref([]);
const wsConnected = ref(false);
let socket = null;

onMounted(() => {
  conectarWebSocket();
});

function conectarWebSocket() {
  // Conecta na porta 8000 (Gateway)
  socket = new WebSocket('ws://localhost:8000/ws');

  socket.onopen = () => {
    wsConnected.value = true;
    logs.value.push("Sistema conectado ao servidor de eventos.");
  };

  socket.onmessage = (event) => {
    logs.value.push("Mensagem recebida: " + event.data);
  };

  socket.onclose = () => {
    wsConnected.value = false;
    logs.value.push("Desconectado. Tentando reconectar em 3s...");
    setTimeout(conectarWebSocket, 3000);
  };
}

function enviarPing() {
  if (socket && socket.readyState === WebSocket.OPEN) {
    socket.send("Ping do Cliente Vue!");
    logs.value.push("Enviado: Ping do Cliente Vue!");
  }
}

async function buscarPedido() {
  loading.value = true;
  error.value = null;
  pedido.value = null;

  const xmlEnvelope = `
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tcc="tcc.soap.gateway">
       <soapenv:Header/>
       <soapenv:Body>
          <tcc:consultar_pedido>
             <tcc:pedido_id>${pedidoId.value}</tcc:pedido_id>
          </tcc:consultar_pedido>
       </soapenv:Body>
    </soapenv:Envelope>
  `;

  try {
    const response = await axios.post('http://localhost:8000/soap', xmlEnvelope, {
      headers: { 'Content-Type': 'text/xml' }
    });

    // O navegador não converte XML para JSON sozinho, precisamos parsear
    parseXmlResponse(response.data);

  } catch (err) {
    console.error(err);
    error.value = "Erro ao comunicar com o Gateway SOAP. Verifique o console.";
  } finally {
    loading.value = false;
  }
}

// Função auxiliar para ler o XML feio e transformar em Objeto Bonito
function parseXmlResponse(xmlString) {
  const parser = new DOMParser();
  const xmlDoc = parser.parseFromString(xmlString, "text/xml");

  // Pegando os valores pelas tags (tns:item, tns:status, etc)
  const item = xmlDoc.getElementsByTagName("tns:item")[0]?.textContent;
  const status = xmlDoc.getElementsByTagName("tns:status")[0]?.textContent;
  const id = xmlDoc.getElementsByTagName("tns:id")[0]?.textContent;

  // Extraindo Links HATEOAS
  const linksNodes = xmlDoc.getElementsByTagName("tns:Link");
  const linksArray = [];
  
  for (let i = 0; i < linksNodes.length; i++) {
    const rel = linksNodes[i].getElementsByTagName("tns:rel")[0]?.textContent;
    const href = linksNodes[i].getElementsByTagName("tns:href")[0]?.textContent;
    const type = linksNodes[i].getElementsByTagName("tns:type")[0]?.textContent;
    linksArray.push({ rel, href, type });
  }

  if (item) {
    pedido.value = { id, item, status, links: linksArray };
    logs.value.push(`Dados SOAP recebidos para o pedido #${id}`);
  } else {
    error.value = "Formato de XML inválido ou pedido não encontrado.";
  }
}
</script>

<style>
/* Estilos básicos para ficar apresentável */
body { font-family: 'Segoe UI', sans-serif; background: #f0f2f5; color: #333; }
.container { max-width: 800px; margin: 0 auto; padding: 20px; }
h1 { text-align: center; color: #2c3e50; }
.card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin-bottom: 20px; }
.search-box { display: flex; gap: 10px; margin-bottom: 10px; }
input { flex: 1; padding: 10px; border: 1px solid #ddd; border-radius: 4px; }
button { padding: 10px 20px; background: #3498db; color: white; border: none; border-radius: 4px; cursor: pointer; }
button:disabled { background: #95a5a6; }
button:hover:not(:disabled) { background: #2980b9; }

.status-ws { text-align: center; padding: 10px; font-weight: bold; margin-bottom: 20px; border-radius: 4px; }
.online { background: #d4edda; color: #155724; }
.offline { background: #f8d7da; color: #721c24; }

.result h3 { border-bottom: 2px solid #eee; padding-bottom: 10px; }
.badge { background: #f1c40f; padding: 5px 10px; border-radius: 15px; font-weight: bold; font-size: 0.9em; }

.hateoas ul { list-style: none; padding: 0; }
.hateoas li { margin: 5px 0; display: flex; align-items: center; gap: 10px; }
.method { background: #e2e6ea; padding: 2px 8px; border-radius: 4px; font-size: 0.8em; font-family: monospace; }

.terminal { background: #2d3436; color: #00ff00; font-family: monospace; }
.logs { max-height: 200px; overflow-y: auto; margin-bottom: 10px; }
.log-item { margin-bottom: 5px; border-bottom: 1px solid #444; }
.btn-small { padding: 5px 10px; font-size: 0.8em; }
.error { color: red; font-weight: bold; }
</style>
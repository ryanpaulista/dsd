const express = require('express');
const app = express();
app.use(express.json());

// Banco de dados mockado de status de entrega
const RASTREIO_DB = {
    1: { status: "EM_TRANSITO", local: "Centro de Distribuição SP", previsao: "2 dias" },
    2: { status: "ENTREGUE", local: "Portaria", previsao: "0 dias" },
    3: { status: "PENDENTE", local: "Armazém", previsao: "5 dias" }
};

app.get('/rastreio/:pedidoId', (req, res) => {
    const id = req.params.pedidoId;
    const info = RASTREIO_DB[id];

    if (info) {
        res.json({ pedido_id: parseInt(id), ...info });
    } else {
        res.json({ 
            pedido_id: parseInt(id), 
            status: "PROCESSANDO", 
            local: "Loja", 
            previsao: "Indefinido" 
        });
    }
});

// Rodando na porta 8002
app.listen(8002, () => {
    console.log('API de Logística (Node) rodando na porta 8002');
});
const express = require('express');
const soap = require('soap');
const cors = require('cors');
const bodyParser = require('body-parser');

const app = express();
app.use(cors());
app.use(bodyParser.json());

const PORT = 3000;

const WSDL_URL = 'http://127.0.0.1:8000/?wsdl';

app.post('/cotacao-frete', (req, res) => {
    const { cep, peso} = req.body;
    console.log(`[NODE] Recebido pedido de cotação: CEP ${cep}, Peso ${peso}`);

    soap.createClient(WSDL_URL, (err, client) => {
        if (err) {
            console.error('[NODE] Erro ao conectar no SOAP:', err);
            return res.status(500).json({ error: 'Erro ao conectar no serviço de frete' });
        }

        const args = {
            cep: cep,
            peso: peso
        }

        client.calcular_frete(args, (err, result) => {
            if (err) {
                console.error('[NODE] Erro na execução SOAP:', err);
                return res.status(500).json({ error: 'Erro ao calcular frete' });
            }

            console.log('[NODE] Resposta do SOAP: ', result);

            res.json({
                servico: "Lógica Express",
                dados: result.calcular_freteResult
            })

        })
    })
}) 


app.listen(PORT, () => {
    console.log(`API Logística (Express) rodando em http://localhost:${PORT}`)
})
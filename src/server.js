const express = require('express');
const multer = require('multer');
const axios = require('axios');
const FormData = require('form-data');
const fs = require('fs'); // Módulo para lidar com arquivos

// Inicializa a aplicação Express
const app = express();
const PORT = 3000;

// Configuração do Multer
// Ele continuará salvando o arquivo recebido temporariamente na pasta 'uploads'
const upload = multer({ dest: 'uploads/' });

/**
 * PONTO 3: A rota foi renomeada para '/upload-audio'.
 * PONTO 1: O middleware do multer agora espera um arquivo no campo 'audio'.
 * Esta é a nossa única rota principal agora.
 */
app.post('/upload-audio', upload.single('audio'), async (req, res) => {
  // 1. Validação: Verifica se um arquivo foi realmente enviado.
  if (!req.file) {
    return res.status(400).send('Nenhum arquivo de áudio foi enviado.');
  }

  console.log('Arquivo de áudio recebido:', req.file);

  try {
    // 2. Prepara os dados para encaminhar o arquivo recebido.
    const formData = new FormData();
    formData.append('audio', fs.createReadStream(req.file.path));

    // PONTO 2: URL do novo destino.
    const destinationUrl = 'http://localhost:5000/upload-and-transcribe-intent';

    console.log(`Encaminhando áudio para: ${destinationUrl}`);

    // 4. Faz a requisição POST para a outra rota usando o Axios.
    const response = await axios.post(destinationUrl, formData, {
      headers: {
        ...formData.getHeaders(), // Headers importantes para o envio de arquivos
      },
    });

    // 5. Envia a resposta recebida da rota de destino de volta ao cliente original.
    console.log('Resposta recebida do serviço de destino!');
    res.status(200).json(response.data);

  } catch (error) {
    console.error('Ocorreu um erro:', error.message);
    res.status(500).send('Erro ao encaminhar o arquivo de áudio.');
  } finally {
    // 6. Limpeza: Apaga o arquivo temporário da pasta 'uploads', independentemente de sucesso ou falha.
    fs.unlinkSync(req.file.path);
    console.log('Arquivo temporário removido.');
  }
});

// Inicia o servidor na porta 3000
app.listen(PORT, () => {
  console.log(`Servidor intermediário rodando na porta ${PORT}.`);
  console.log(`Aguardando requisições na rota POST /upload-audio`);
});
const express = require('express');
const multer = require('multer');
const axios = require('axios');
const FormData = require('form-data');
const fs = require('fs'); // Módulo para lidar com arquivos

// Inicializa a aplicação Express
const app = express();
const PORT = 3000;

// Configuração do Multer
// Vamos salvar a imagem temporariamente em uma pasta 'uploads'
const upload = multer({ dest: 'uploads/' });

/**
  ROTA PRINCIPAL (Passo 8)
  Rota POST que vai receber a imagem e enviá-la para outra rota.
  Usamos 'upload.single('imagem')' para dizer ao Multer que esperamos um único arquivo
  que virá no campo chamado 'imagem' do formulário.
 */
app.post('/upload', upload.single('imagem'), async (req, res) => {
  // 1. Verifica se o arquivo foi recebido
  if (!req.file) {
    return res.status(400).send('Nenhuma imagem foi enviada.');
  }

  console.log('Imagem recebida:', req.file);

  try {
    // 2. Prepara os dados para enviar para a outra rota
    const formData = new FormData();
    // Adiciona o arquivo da imagem ao formulário
    formData.append('imagem', fs.createReadStream(req.file.path));

    // 3. Define a URL do destino (substitua pela URL real se for diferente)
    const destinationUrl = 'http://localhost:3000/extract-text-from-image';

    console.log(`Enviando imagem para: ${destinationUrl}`);

    // 4. Faz a requisição POST para a outra rota usando o Axios
    const response = await axios.post(destinationUrl, formData, {
      headers: {
        ...formData.getHeaders(),
      },
    });

    // 5. Apaga o arquivo temporário após o envio
    fs.unlinkSync(req.file.path);

    // 6. Envia a resposta da rota de destino de volta ao cliente original
    console.log('Resposta da rota de destino recebida!');
    res.status(200).json(response.data);

  } catch (error) {
    // 7. Em caso de erro, apaga o arquivo temporário e envia uma mensagem de erro
    fs.unlinkSync(req.file.path);
    console.error('Erro ao processar a requisição:', error.message);
    res.status(500).send('Ocorreu um erro no servidor.');
  }
});

/**
  Esta é a rota /extract-text-from-image que vai receber a imagem da rota /upload.
  Por enquanto, ela apenas confirma o recebimento.
 */
app.post('/extract-text-from-image', upload.single('imagem'), (req, res) => {
    if (!req.file) {
        return res.status(400).json({ message: 'Nenhum arquivo de imagem recebido na rota de destino.' });
    }
    console.log('A rota /extract-text-from-image recebeu a imagem com sucesso!');

    // Lógica para extrair o texto da imagem (colocar aqui)
    res.status(200).json({
        message: 'Imagem recebida com sucesso na rota de extração!',
        originalName: req.file.originalname,
        size: req.file.size
    });
});


// Inicia o servidor
app.listen(PORT, () => {
  console.log(`Servidor rodando na porta ${PORT}.`);
  console.log('Use uma ferramenta como Postman ou Insomnia para testar a rota POST /upload');
});
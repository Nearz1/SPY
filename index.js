const express = require('express');
const cors = require('cors');
const fetch = require('node-fetch');

const app = express();
app.use(cors()); // Libera CORS

app.get('/tiktok-friends-status', async (req, res) => {
    const sid_tt = req.query.sid_tt;

    if (!sid_tt) {
        return res.status(400).json({ error: 'sid_tt é obrigatório' });
    }

    try {
        const response = await fetch('https://api16-normal-c-useast1a.tiktokv.com/aweme/v1/im/friend/status/', {
            method: 'GET',
            headers: {
                'user-agent': 'com.ss.android.ugc.trill/150500 (Linux; U; Android 10; en_US; SM-G973N Build/QP1A.190711.020; Cronet/58.0.2991.0)',
                'cookie': `sid_tt=${sid_tt};`,
                'accept': 'application/json'
            }
        });

        const data = await response.json();
        res.json(data);
    } catch (error) {
        console.error(error);
        res.status(500).json({ error: 'Erro ao buscar dados.' });
    }
});

const port = process.env.PORT || 3000;
app.listen(port, () => {
    console.log(`Proxy rodando na porta ${port}`);
});

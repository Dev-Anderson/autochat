require("dotenv").config()
const express = require("express")
const axios = require("axios")

const app = express()
app.use(express.json())

const BASE_URL = "https://api.z-api.io"

app.post("/send-message", async (req, res) => {
    try {

        const { phone, message } = req.body

        const url = `${BASE_URL}/instances/${process.env.ZAPI_INSTANCE_ID}/token/${process.env.ZAPI_INSTANCE_TOKEN}/send-text`

        const response = await axios.post(
            url,
            {
                phone: phone,
                message: message
            },
            {
                headers: {
                    "Client-Token": process.env.ZAPI_CLIENT_TOKEN,
                    "Content-Type": "application/json"
                }
            }
        )

        res.json(response.data)

    } catch (error) {

        res.status(500).json({
            error: error.response?.data || error.message
        })
    }
})

app.listen(3000, () => {
    console.log("Servidor rodando na porta 3000")
})
require("dotenv").config()

const express = require("express")
const { sendMessage } = require("./zapi")

const app = express()
app.use(express.json())

// webhook que a Z-API vai chamar
app.post("/webhook", async (req, res) => {

    try {

        const data = req.body

        console.log("Mensagem recebida:", data)

        const phone = data.phone
        const message = data.text?.message?.toLowerCase()

        if (!message) {
            return res.sendStatus(200)
        }

        if (message === "oi") {

            await sendMessage(
                phone,
                "Olá 👋\n\nBem-vindo! Como posso ajudar você hoje?"
            )

        }

        res.sendStatus(200)

    } catch (error) {

        console.error(error)
        res.sendStatus(500)

    }
})

app.listen(3000, () => {
    console.log("Webhook rodando na porta 3000")
})
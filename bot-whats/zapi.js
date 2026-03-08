const axios = require("axios")

async function sendMessage(phone, message) {

    const url = `${process.env.ZAPI_BASE_URL}/instances/${process.env.ZAPI_INSTANCE_ID}/token/${process.env.ZAPI_INSTANCE_TOKEN}/send-text`

    await axios.post(
        url,
        {
            phone,
            message
        },
        {
            headers: {
                "Client-Token": process.env.ZAPI_CLIENT_TOKEN,
                "Content-Type": "application/json"
            }
        }
    )
}

module.exports = { sendMessage }
# Flask endpoint for /index route
@app.route('/index')
def index():
    # get token from cookie
    token = bytes.fromhex(request.cookies.get('token'))
    app.logger.debug("Received token: %s", token.hex())

    # decrypt token + padding
    iv, ct = token[:16], token[16:]
    token = AES.new(key, AES.MODE_CBC, iv).decrypt(ct)
    app.logger.debug("Decrypted token: %s", token.hex())

    # remove padding and deserialize
    try:
        token = unpad(token, block_size=16)
        app.logger.debug("Unpadded token: %s", token)
        token = json.loads(token)
        app.logger.debug("Deserialized token: %s", token)
    except (ValueError, json.decoder.JSONDecodeError):
        return {"error": "invalid token"}


    return {"status": "ok"}

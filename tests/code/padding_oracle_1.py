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

    # remove padding
    try:
        token = unpad(token, block_size=16)
    except ValueError:
        return {"error": "decryption failed"}
    app.logger.debug("Unpadded token: %s", token)

    # deserialize token from json
    try:
        token = json.loads(token)
    except json.decoder.JSONDecodeError:
        return {"error": "deserialization failed"}
    app.logger.debug("Deserialized token: %s", token)

    return {"status": "ok"}

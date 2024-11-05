def sayhi(client, channel):
    """Outputs 'Hello World!' to the specified channel
    """

    text = "Hello World!"
    client.chat_postMessage(channel=channel, text=text)
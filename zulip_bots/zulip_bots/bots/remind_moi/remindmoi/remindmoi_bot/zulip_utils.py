import zulip

# Pass the path to your zuliprc file here.
client = zulip.Client(config_file="../zuliprc")


# Send a private message
request = {
    "type": "private",
    "to": "jose@monadical.com",
    "content": "With mirth and laughter let old wrinkles come."
}
result = client.send_message(request)
print(result)

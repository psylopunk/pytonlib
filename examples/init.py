from ton import TonlibClient
# OR
# from ton.sync import TonlibClient

# Initiate module
client = TonlibClient()
TonlibClient.enable_unaudited_binaries()
await client.init_tonlib()
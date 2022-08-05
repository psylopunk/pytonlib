from ton.sync import TonlibClient

client = TonlibClient()
TonlibClient.enable_unaudited_binaries()
client.init_tonlib()

wallet = client.create_wallet()
print('Wallet address:', wallet.address)
print('Seed:', wallet.export())

from .init import client

# Wallet generation
wallet = await client.create_wallet()

# Get a word list (for tonkeeper, tonhub etc)
seed = await wallet.export()

# Importing wallet
wallet = await client.import_wallet(seed)

# Get saved wallet from Keystore
path = wallet.path
wallet = await client.find_wallet(path)

# Getting an address
wallet.address
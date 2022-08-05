from .init import client
from .wallet import wallet

await wallet.transfer_nft(
    'EQCEXDQWeqjLP4BehKzzwbuRBsxQHVwEa9j4MGunBs1Vkg_w',  # NFT address
    'EQCl1Ug9ZT9ZfGyFH9l4q-bqaUy6kyOzVPmrk7bivmVKJRRZ'  # Recipient address
)
# OR
account = await client.find_account('EQCEXDQWeqjLP4BehKzzwbuRBsxQHVwEa9j4MGunBs1Vkg_w')
body = account.create_transfer_nft_body('EQCl1Ug9ZT9ZfGyFH9l4q-bqaUy6kyOzVPmrk7bivmVKJRRZ')
wallet.transfer(account.address, client.to_nano(0.05), data=body.serialize_boc())
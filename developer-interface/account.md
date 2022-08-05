# Account

General class for wallets and account browsing. To execute any methods, you must specify client. It is recommended to get an instance of this class only through methods: `TonlibClient.find_account`, `TonlibClient.create_wallet`, `TonlibClient.import_wallet`, `TonlibClient.find_wallet`.

```python
class ton.Account(address, key=None, client=None)
```

#### Parameters:

* **address** – (str, required) b64url address form
* **key** – (str, optional) private key for transfer coins (wallet contract)
* **client** – (int, required) initialized TonlibClient

### Methods:

* `get_balance() -> int nanoTONs`\
  ``
* `get_transactions(from_transaction_lt=None, from_transaction_hash=None, to_transaction_lt=None, limit=10) -> TLObject`\
  ``Get a list of account transactions\
  **from\_transaction\_lt & from\_transaction\_hash** must only be used together to get transactions older than specified\
  **to\_transaction\_lt**: ignoring transactions older than specified logic time\

* `detect_type() -> dict`\
  ``With this, you can determine the version of the wallet, if it is initialized\

* `get_state(force=True) -> state TLObject`\
  ``Full information about the contract, including its code and data\
  ``**force**: (bool) if False data is taken from cache\

* `transfer(destination, amount=None, data=None, comment=None, send_mode=1)`\
  ``Transferring coins.\
  **destination**: (str, list) account address. Or list for multiple output messages ([read more](../examples/transactions.py))\
  **amount**: (int) nanoTONs amount\
  **data**: (bytes) serialized cells / BOC\
  **comment**: (str) comment\
  **send\_mode**: (int) default 1\
  0 - commission is taken from transfer amount\
  1 - commission is taken separately from the balance\
  128 - transfer of all funds\
  128+32 - deleting an account\
  Read more in the documentation ton.org/docs\

* `transfer_nft(item_addr, new_owner_addr, response_address=None, query_id=0, forward_amount=0, forward_payload=None)`\
  ``Changing the owner of the NFT by sending an internal transaction (0.05 TON)\
  **item\_addr**: (str) b64url address NFT\
  **new\_owner\_addr**: (str) b64url address of recipient NFT\
  **response\_address**: (str) b64url address for response\
  **query\_id**: (int) arbitrary request number\
  **forward\_amount**: (int) forward nanoTONs amount\
  **forward\_payload**: (bytes) forward body\

* `run_get_method(name|id, stack=[], force=False)`\
  ``Execution GET method of smart contract\
  **name|id**: (int, str) method ID or its string representation\
  **stack:** (list of Tvm\_StackEntry..) arguments\
  **force**: (bool) if False data is taken from cache\
  **Example:**\
  ****`from ton.tl.types import Tvm_StackEntryNumber, Tvm_NumberDecimal`\
  `account.run_get_method('get_nft_address_by_index', [Tvm_StackEntryNumber(Tvm_NumberDecimal(1))])`\
  ``
* `send_message(body)`\
  ``Sending an external message\
  **body**: (bytes) serialized cells / BOC\

* `get_nft_data()`
* `get_collection_data()`
* `get_nft_address_by_index(index)`
* `royalty_params()`
* `create_transfer_nft_body(new_owner, response_address=None, query_id=0, forward_amount=0, forward_payload=0)`

In addition, there is a property method that serializes the private key into a string to load wallet from Keystore. For more information, see the method `TonlibClient.find_wallet`


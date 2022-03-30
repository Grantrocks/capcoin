from mnemonic import Mnemonic
import bip32utils
import bitcoin
def generate():
  mnemon = Mnemonic('english')
  words = mnemon.generate(256)
  wd=[words]
  return wd
def check(words):
  mnemon = Mnemonic('english')
  seed = mnemon.to_seed(words)
  root_key = bip32utils.BIP32Key.fromEntropy(seed)
  child_key = root_key.ChildKey(327868587 + bip32utils.BIP32_HARDEN).ChildKey(0 + bip32utils.BIP32_HARDEN).ChildKey(0 + bip32utils.BIP32_HARDEN).ChildKey(0).ChildKey(0)
  address = child_key.Address()
  child_public_hex = child_key.PublicKey().hex()
  child_private_wif = child_key.WalletImportFormat()
  wd=[words,address,child_public_hex,child_private_wif]
  return wd
def miner_check(pk):
  addr=bitcoin.pubtoaddr(str(pk).encode('utf-8'))
  return addr
import hashlib
import base58
import bech32
import binascii

def script_to_scripthash(script):
	return hashlib.sha256(script).digest()[::-1].hex()

def bitstring_to_bytes(s):
	return int(s, 2).to_bytes((len(s) + 7) // 8, byteorder='big')

def demod(intarray):
	result = []
	for x in intarray:
		result.append(format(x, "05b"))
	return bitstring_to_bytes(''.join(result))[1:]

def bech32_to_script(address):
	bech32_decoded = bech32.bech32_decode(address)
	hash160hex = demod(bech32_decoded[1]).hex()
	return binascii.unhexlify("0014" + hash160hex)

def p2pkh_address_to_script(address):
	hash160hex = base58.b58decode(address)[1:21].hex()
	return binascii.unhexlify("76a914" + hash160hex + "88ac")

def p2sh_address_to_script(address):
	hash160hex = base58.b58decode(address)[1:21].hex()
	return binascii.unhexlify("a914" + hash160hex + "87")


# These are test addresses extracted randomly from block explorer
print(script_to_scripthash(p2pkh_address_to_script('mzYBzhixCEUUXrmeWUdN32Sbh8ycadHSgs')))
print(script_to_scripthash(p2sh_address_to_script('2N4SANLfZ6ZRUnyaMxGGNo8bAu4Pvtqbd6r')))
print(script_to_scripthash(bech32_to_script('tb1q7yszr0rd6qeaup5ngewc6d52fylxq4s2n4nmc0')))
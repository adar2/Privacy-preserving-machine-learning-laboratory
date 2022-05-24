from phe import paillier, PaillierPublicKey, PaillierPrivateKey

KEY_SIZE = 2048


def encrypt(public_key: PaillierPublicKey, plain_text: str):
    if public_key is not None:
        return public_key.encrypt(plain_text)
    return None


def decrypt(private_key: PaillierPrivateKey, cipher_text):
    if private_key is not None:
        return private_key.decrypt(cipher_text)
    return None


def generate_public_private_keys():
    return paillier.generate_paillier_keypair(n_length=KEY_SIZE)

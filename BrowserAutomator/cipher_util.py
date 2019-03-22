from Crypto.PublicKey.RSA import generate, importKey
from Crypto.Cipher import PKCS1_OAEP


def key_generator(private_key_path, public_key_path, key_length=1024):
    key = generate(key_length)
    private, public = key, key.publickey()
    interact_with_file(private_key_path, "wb", private.exportKey())
    interact_with_file(public_key_path, "wb", public.exportKey())


def encrypt(clear_text, public_key_path, output_file_path=None):
    clear_text = bytes(clear_text, "utf-8")
    raw_key = interact_with_file(public_key_path, "rb")
    key = importKey(raw_key)
    cipher = PKCS1_OAEP.new(key)
    ciphertext = cipher.encrypt(clear_text)
    if output_file_path:
        interact_with_file(output_file_path, "wb", ciphertext)
    return ciphertext


def decrypt(encrypted_text, private_key_path):
    raw_key = interact_with_file(private_key_path, "rb")
    key = importKey(raw_key)
    cipher = PKCS1_OAEP.new(key)
    decrypted = cipher.decrypt(encrypted_text)
    return decrypted.decode("utf-8")


def decrypt_file(private_key_path, filename):
    encrypted_text = interact_with_file(filename, "rb")
    decrypted = decrypt(encrypted_text, private_key_path)
    return decrypted


def decrypt_content(content):
    private_key_file, encrypted_file = content["private_key_path"], content["encrypted_file_path"]
    return decrypt_file(private_key_file, encrypted_file)


def interact_with_file(filename, mode, content=None):
    with open(filename, mode) as f:
        if content:
            f.write(content)
        else:
            out = f.read()
            return out


if __name__ == "__main__":
    key_generator("private_key.txt", "public_key.txt")
    encrypt("test123", "public_key.txt", "test.txt")
    print(decrypt_file("private_key.txt", "test.txt"))

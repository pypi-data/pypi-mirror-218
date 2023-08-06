import simple_rsa as rsa

def test_encoding_and_decoding():
  private, public = rsa.generate_key_pair()
  
  private_pem = rsa.encode(private)
  public_pem  = rsa.encode(public)
  
  decoded_private = rsa.decode(private_pem)
  assert rsa.encode(decoded_private) == private_pem

  decoded_public = rsa.decode(public_pem)
  assert rsa.encode(decoded_public) == public_pem

def test_signing_and_validation():
  private, public = rsa.generate_key_pair()

  payload = b"something important"
  
  signature = rsa.sign(payload, private)
  
  assert rsa.validate(payload, signature, public)

from backend.security import hash_password, verify_password, create_access_token, decode_access_token

def test_password_hash_and_verify():
    stored = hash_password("senha-segura-123")
    assert stored != "senha-segura-123"
    assert verify_password("senha-segura-123", stored)
    assert not verify_password("senha-errada", stored)

def test_jwt_roundtrip():
    token = create_access_token(42)
    payload = decode_access_token(token)
    assert payload["sub"] == "42"

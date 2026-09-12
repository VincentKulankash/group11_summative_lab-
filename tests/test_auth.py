import pytest 

from utils.auth import (
    hash_password,
    verify_password,
    login_required,
    CURRENT_USER,
)

#hash password

def test_hash_password_returns_string():
    h = hash_password('SECRET123')
    assert isinstance(h,str)

def test_hash_password_not_plaintext():
    h = hash_password("secret123")
    assert h != "secret123"
    assert "secret123" not in h

def test_hash_password_is_different_each_time():
    h1 = hash_password('samepassword')
    h2 = hash_password('samepassword')
    assert h1 != h2
    #the passwords should not be the same beacause of salt being random


#verify password

def test_verify_correct_password():
    h = hash_password("secret123")
    assert verify_password('secret123', h) is True

def test_verify_wrong_password():
    h = hash_password("secret123")
    assert verify_password('wrong', h) is False

def test_verify_handles_malformed_hash():
    assert verify_password('anything', 'not-a-valid-hash') is False
    assert verify_password('anything', '') is False

#login required 

def test_login_required_blocks_when_not_logged_in(capsys):
    CURRENT_USER['user'] = None

    @login_required
    def secret():
        return True

    result = secret()
    assert result is None
    captured = capsys.readouterr()
    assert "log in" in captured.out

def test_login_required_allows_when_logged_in():
    CURRENT_USER["user"] = "Alice"

    @login_required
    def secret():
        return "ran"

    assert secret() == "ran"

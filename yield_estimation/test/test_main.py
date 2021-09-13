from yield_estimation.main import hello_world


def test_hello_world():
    result = hello_world("America/Chicago")
    assert "Chicago!" in result

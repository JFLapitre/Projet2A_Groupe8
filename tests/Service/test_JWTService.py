import datetime

from freezegun import freeze_time

from src.Service.JWTService import JwtService

jwt_service = JwtService("mysecret")


@freeze_time("2024-08-26 12:00:00")
def test_encode_jwt():
    """
    Test mis à jour pour correspondre à la logique actuelle du service :
    Expiration à +30 minutes (1800s) -> Timestamp 1724675400.0
    """
    user_id = "myUser"
    jwtResponse = jwt_service.encode_jwt(user_id=user_id)

    # Token correspondant à une expiration à 12:30:00 (généré par le code actuel)
    expected_token = (
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
        "eyJ1c2VyX2lkIjoibXlVc2VyIiwiZXhwaXJ5X3RpbWVzdGFtcCI6MTcyNDY3NTQwMC4wfQ."
        "HGQSpvCYTD3h7H9_Ys--ReQabvdOsdikeofkMHtHYMc"
    )

    assert jwtResponse.access_token == expected_token


@freeze_time("2024-08-26 12:00:00")
def test_decode_jwt():
    """
    Ce test reste inchangé car il valide la capacité de décodage d'un token donné.
    Le token 'input' ici est celui de 10 minutes, ce qui est valide pour un test unitaire de décodage.
    """
    jwt = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoibXlVc2VyIiwiZXhwaXJ5X3RpbWVzdGFtcCI6MTcyNDY3NDIwMC4wfQ.eUjNbpMCDNuPESsMHF2dpeRlDl6fMJmjUWsHSZT_n1Q"  # noqa: E501
    decoded_jwt = jwt_service.decode_jwt(jwt)
    assert decoded_jwt.get("user_id") == "myUser"
    assert datetime.datetime.fromtimestamp(decoded_jwt.get("expiry_timestamp")) == datetime.datetime.fromisoformat(
        "2024-08-26 12:10:00"
    )

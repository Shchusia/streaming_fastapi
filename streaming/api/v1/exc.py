from core.exc import Base409


class NotGeneratedPeerConnectionForVehicle(Base409):
    title = "BadRequest"
    data = 'Not inited peer connection'


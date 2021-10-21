from fastapi import APIRouter
from fastapi.responses import JSONResponse
from extensions import lobbyservice
from users.user import User

router = APIRouter()


@router.get('/get-lobbies')
async def get_lobbies():
    lobbies = lobbyservice.get_lobbies()
    return JSONResponse(content={'lobbies': [lobby.to_dict() for lobby in lobbies]},
                        status_code=200)


@router.post('/create-lobby')
async def create_lobby(name: str, host:str):
    # When you create your lobby, you have to provide your user name
    host_user = User(host)
    lobbyservice.create_new_lobby(name, host_user)
    return JSONResponse(content={'lobby': lobbyservice.get_lobby_by_name(name).to_dict(),
                                 'info': "Lobby was created"},
                        status_code=200)


@router.put('/join-player')
async def join_player(name:str, player:str):
    # When you enter in a lobby, you have to provide your user name
    new_player = User(player)
    try:
        lobbyservice.join_player(name, new_player)
        return JSONResponse(content={'lobby': lobbyservice.get_lobby_by_name(name).to_dict(),
                                     'info': "Player added"},
                            status_code=200)
    except:
        return JSONResponse(content={'lobby': None,
                                     'info': "The lobby is full or the player is already in the lobby"},
                            status_code=502)

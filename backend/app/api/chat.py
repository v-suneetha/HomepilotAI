from fastapi import APIRouter
router=APIRouter()
@router.post('/chat')
def chat(msg:dict): return {'reply':'Hello from HomePilot AI'}

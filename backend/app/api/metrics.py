from fastapi import *

router=APIRouter()

counter={

"light":0,

"heavy":0
}


@router.get(
"/metrics"
)

def metrics():

    return counter
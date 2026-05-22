from fastapi import (
    APIRouter,
    UploadFile,
    File,
    HTTPException
)

from app.schemas.mom_schema import (
    TranscriptRequest,
    MoMResponse
)

from app.services.pipeline import (
    process_meeting,
    process_text
)

import os


router = APIRouter()


@router.post(
    "/summarize",
    response_model=MoMResponse
)
async def summarize(
    file: UploadFile = File(...)
):

    temp_file_path = file.filename

    try:

        with open(
            temp_file_path,
            "wb"
        ) as f:

            content = await file.read()
            f.write(content)

        result = process_meeting(
            temp_file_path
        )

        return result

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    finally:

        if os.path.exists(
            temp_file_path
        ):

            os.remove(
                temp_file_path
            )


@router.post(
    "/summarize-text",
    response_model=MoMResponse
)
def summarize_text(
    data: TranscriptRequest
):

    try:

        result = process_text(
            data.transcript
        )

        return result

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
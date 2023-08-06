#  Copyright (c) 2023 Roboto Technologies, Inc.

from typing import Optional

import pydantic


class UserRecord(pydantic.BaseModel):
    user_id: str
    is_system_user: Optional[bool] = False
    name: str | None = None
    picture_url: str | None = None

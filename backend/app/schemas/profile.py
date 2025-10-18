from pydantic import BaseModel


class DemoProfileOut(BaseModel):
    id: int
    platform: str
    handle: str
    display_name: str
    avatar_url: str
    bio: str
    sample_posts: dict

    model_config = {
        "from_attributes": True,
    }



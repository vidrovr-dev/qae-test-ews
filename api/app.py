from sanic import Blueprint, Sanic

from .db import engine
from .models import Base
from .upload import create_bucket
from .views import VideoView, CommentsView

create_bucket()
Base.metadata.create_all(engine)


class SanicConfig(object):
    REQUEST_MAX_SIZE = 100000000000
    REQUEST_TIMEOUT = 1200
    RESPONSE_TIMEOUT = 300


bp = Blueprint("videos", url_prefix="/videos")
bp.add_route(VideoView.as_view(), "")
bp.add_route(VideoView.as_view(), "/<video_id:str>", name="videos_")
bp.add_route(CommentsView.as_view(), "/<video_id:str>/comments")

app = Sanic("videos_api")
app.update_config(SanicConfig)
app.blueprint(bp)

import base64

from io import BytesIO
from tempfile import TemporaryDirectory
from uuid import uuid4

import orjson as json

from sanic import response, BadRequest
from sanic.views import HTTPMethodView
from sqlalchemy import select
from sqlalchemy.orm import Session

from api.db import engine
from api.download import download
from api.models import Video, Comment
from api.upload import bucket, upload


class VideoView(HTTPMethodView):
    @classmethod
    def get(cls, request, video_id: str = None):
        if video_id is not None:
            q = select(
                Video.id.label("id"),
                Video.title.label("title"),
                Video.url.label("url"),
                Video.filestore_key.label("fs_key")
            )

            q = q.where(Video.id==video_id)

            with Session(engine) as sesh:
                row = sesh.execute(q).one_or_none()

            response_body = dict(row._mapping)

            with BytesIO() as f:
                bucket.download_fileobj(response_body.pop("fs_key"), f)
                f.seek(0)
                video_bytes = f.read()

            response_body['video'] = base64.b64encode(video_bytes).decode('utf-8')

            return response.json(response_body, status=200, dumps=json.dumps)

        q = select(Video.id.label("id"), Video.title.label("title"))
        with Session(engine) as sesh:
            rows = sesh.execute(q).all()

        return response.json([dict(row._mapping) for row in rows], status=200, dumps=json.dumps)

    @classmethod
    def post(cls, request):
        body = request.json

        try:
            url = body["url"]
        except KeyError:
            raise BadRequest(f"`url` is a required request parameter")

        with TemporaryDirectory() as td:
            video_path, info_dict = download(url, td)
            fs_key = upload(video_path)

        with Session(engine) as sesh:
            video = Video(
                id=uuid4(),
                url=url,
                title=info_dict['title'],
                filestore_key=fs_key
            )

            sesh.add(video)
            sesh.commit()

            video_id = str(video.id)

            comments = [Comment(text=c['text'], video_id=video.id)
                        for c in info_dict['comments']]

            sesh.add_all(comments)
            sesh.commit()

        response_body = {
            "id": video_id,
        }

        return response.json(response_body, status=201, dumps=json.dumps)


class CommentsView(HTTPMethodView):
    @classmethod
    def get(cls, request, video_id: str):
        q = select(Comment.id.label("id"), Comment.text.label("text"))
        q = q.where(Comment.video_id==video_id)

        with Session(engine) as sesh:
            rows = sesh.execute(q).all()

        response_body = [dict(row._mapping) for row in rows]

        return response.json(response_body, status=200, dumps=json.dumps)

# Create a video ingestion API 
Video ingestion is a cornerstone of Vidrovr's value proposition. 
We'd like you to show us what you got by developing tests for a small RESTful API 
that can ingest a video from a URL and return metadata about it on subsequent requests.

## Product requirements
The API must fulfill two main functions:
* A user can submit a URL to a video - 
for example, from YouTube. 
* A user can request information about a previously ingested video.

THe API additionally must:
* Adhere to REST design principles
* Return appropriate HTTP status codes
* Return an identifier following upload for subsequent requests for metadata

The information the API should return for an ingested video MUST include:
* A title for the video
* Its original URL
* The video file data, base64-encoded

The API MAY additionally return:
* The height and width of the video in pixels
* The duration of the video in seconds

Finally, there must be **sufficient documentation** for API usage. 
Example cURL commands are typically enough, 
but more descriptive documentation is certainly welcome.

## Technical requirements
The API implementation **MUST**:
* Use Python >= 3.11
* Use the SQLAlchemy ORM framework to interact with Postgres
  * This includes creating tables!
* Include any Python packages in `app/requirements.txt`
* Store the downloaded video file in `minio`
* Bring the thunder

You MAY:
* Use the `yt-dlp` program for downloading videos and metadata from a URL
* Use a Python API library of your choosing
* Use `alembic` instead of directly using SQLAlchemy to create any necessary tables
* Add additional containers if you find it appropriate
* Use Google, StackOverflow as appropriate when you encounter new problems

## Provided infrastructure
We will provide a docker compose file that will create local postgres and minio instances for you, 
and a basic version of the application to be tested.

Example cURL commands and expected (successful) responses:

```commandline
curl -X POST http://localhost:8080/videos -H 'content: application/json' -d '{"url": "<url>"}'
```

```json
{
  "id": "<valid uuid>"
}
```

```commandline
curl -X GET http://localhost:8080/videos/b87c458d-7b36-4126-892d-f4ff86b1d5c2
```

```json
{
  "id": "<valid uuid>",
  "name": "<title of video on original platform>",
  "url": "<original url of video>",
  "video": "<video file as hex-encoded string>"
}
```

```commandline
curl -X GET http://localhost:8080/videos/b87c458d-7b36-4126-892d-f4ff86b1d5c2/comments
```

```json
[
  {
    "id":"<valid uuid>",
    "text":"<comment text, string>"
  },
  // ...
]
```



## Evaluation


## Submission

[//]: # (1. Put your application code in the `app` directory)

[//]: # (2. Execute it with a JSON-style `CMD` in `Dockerfile`)

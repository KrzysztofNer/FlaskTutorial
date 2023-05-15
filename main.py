from flask import Flask
from flask_restful import Api, Resource, reqparse, abort

app = Flask(__name__)
api = Api(app)

# Automaticlly parse through the request and fits the kind of gidline
# That we're about define(usefull information: name video, its amount likes and views
video_put_args = reqparse.RequestParser()

video_put_args.add_argument(
    "name",
    type=str,
    help="Name of th video is required",
    # what we should display if the user doesn't provide the argument. It is kind of error message
    required=True
)
video_put_args.add_argument("views", type=int, help="Amount views of th video", required=True)
video_put_args.add_argument("likes", type=int, help="Amount likes of th video", required=True)

videos = {}


def abort_if_video_id_doesnt_exist(video_id):
    if video_id not in videos:
        abort(404, message="Could not find video...")


def abort_if_video_id_exist(video_id):
    if video_id in videos:
        abort(409, message="Video already exist with that ID...")


class Video(Resource):
    def get(self, video_id):
        abort_if_video_id_doesnt_exist(video_id)
        return videos[video_id]

    def put(self, video_id):
        abort_if_video_id_exist(video_id)
        args = video_put_args.parse_args()
        videos[video_id] = args
        return videos[video_id], 201  # 201 is the status code for created

    def delete(self, video_id):
        abort_if_video_id_doesnt_exist(video_id)
        videos.pop(video_id)  # we can also use del videos[video_id]
        return '', 204  # 204 is the status code for deleted


api.add_resource(Video, "/video/<int:video_id>")

if __name__ == '__main__':
    app.run(debug=True)

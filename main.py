from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)    #primary key is unique identifier; default valuse primary_key is False
    name = db.Column(db.String(100), nullable=False)   #nullable means that it can't be empty, default valus of nullable is True
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Video(name={name}, views={views}, likes={likes})"

#db.create_all() creates database.db file in the same directory as main.py


video_put_args = reqparse.RequestParser()
# Automaticlly parse through the request and fits the kind of gidline
# That we're about define(usefull information: name video, its amount likes and views

video_put_args.add_argument(
    "name",
    type=str,
    help="Name of th video is required",
    # what we should display if the user doesn't provide the argument. It is kind of error message
    required=True
)
video_put_args.add_argument("views", type=int, help="Amount views of th video", required=True)
video_put_args.add_argument("likes", type=int, help="Amount likes of th video", required=True)

resource_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "views": fields.Integer,
    "likes": fields.Integer
}
#Resource_fields is a dictionary that defines what we want to display when we get the video


class Video(Resource):
    @marshal_with(resource_fields)  # decorator that takes the result of get method and serializes it with resource_fields
    def get(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first()
        # filter_by() is similar to where in SQL
        # filter_by() returns query object that we can add to it .all() or .first() etc.
        # first() returns the first result of the query
        if not result:
            abort(404, message="Could not find video with that id...")

        return result

    @marshal_with(resource_fields)
    def put(self, video_id):
        args = video_put_args.parse_args()
        # args = video_put_args.parse_args(strict=True)
        # strict=True means that if the user provides more arguments than we defined in video_put_args it will throw an error
        result = VideoModel.query.filter_by(id=video_id).first()
        if result:
            abort(409, message="Video id taken...")
        video = VideoModel(id=video_id, name=args["name"], views=args["views"], likes=args["likes"])
        db.session.add(video)   #add video to the database
        db.session.commit()     #commit(zatwierdzić) permament changes to the database
        return video, 201  # 201 is the status code for created

    # def delete(self, video_id):
    #     abort_if_video_id_doesnt_exist(video_id)
    #     videos.pop(video_id)  # we can also use del videos[video_id]
    #     return '', 204  # 204 is the status code for deleted


api.add_resource(Video, "/video/<int:video_id>")

if __name__ == '__main__':
    app.run(debug=True)

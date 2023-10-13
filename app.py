from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

posts = {
    '1': {'user_id': '1', 'post': 'Hello, world!'},
    '2': {'user_id': '2', 'post': 'My first blog post'}
}

USER_SERVICE_URL = 'https://abhishekuserservice.agreeablewater-91d2a3ce.canadacentral.azurecontainerapps.io'

@app.route('/')
def hello():
    return 'Post serive is live!'

#retrive psot_service

@app.route('/post/', methods=['GET'])
def get_posts():
    return jsonify(posts)

@app.route('/post/<id>', methods=['GET'])
def get_post(id):
    post_info = posts.get(id, {})
    return jsonify(post_info)

#delete post_service

@app.route('/post/<id>', methods=['DELETE'])
def delete_post(id):
    try:
        deleted_post = posts.pop(id)
        return jsonify({"message": "Post deleted", "deleted_post": deleted_post})
    except KeyError:
        return jsonify({"error": "Post not found"}, 404)

#update post_service

@app.route('/post/<id>', methods=['PUT'])
def update_post(id):
    if id in posts:
        post_info = posts.get(id)
        data = request.json
        post_info['user_id'] = data.get('user_id', post_info['user_id'])
        post_info['post'] = data.get('post', post_info['post'])
        
        return jsonify({"message": "Post updated", "post_info": post_info})
    else:
        return jsonify({"error": "Post not found"}, 404)

#create post_serice
@app.route('/post/', methods=['POST'])
def create_post():
    new_post = request.get_json()
    id = str(len(posts) + 1)
    posts[id] = new_post
    new_post["id"] = id
    return jsonify({"message": "Post created", "new_post": new_post}), 201

if __name__ == '__main__':
    app.run(port=5001)

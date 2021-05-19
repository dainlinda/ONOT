from flask import Blueprint
from flask import Flask, request, jsonify
import bcrypt
from flask_cors import CORS
from .. import models
from . import checkvalid
from datetime import datetime, timedelta
from flask_jwt_extended import (JWTManager, jwt_required, create_access_token,
                                get_jwt_identity, unset_jwt_cookies, create_refresh_token)
from ast import literal_eval

# Flasgger
from flasgger.utils import swag_from

bp = Blueprint('auth', __name__, url_prefix='/')

@bp.route('/sign-up', methods=['POST'])
@swag_from("../swagger_config/register.yml", validation=True)
def register():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request", 'status':400})

    else:
        # body = literal_eval(request.get_json()['body'])
        body=request.get_json()

        email = body['email']
        pw = body['pw']
        name = body['name']
        nickname = body['nickname']
        birth = body['birth']
        gender = body['gender']


        emailcheck = models.User.query.filter_by(email=email).first()
        nicknamecheck = models.User.query.filter_by(nickname=nickname).first()

        if not(name and email and pw and nickname):
            return jsonify({"msg": "빈칸 오류", 'status': 400})

        elif emailcheck is not None:
            return jsonify({"msg": "이미 가입된 이메일입니다.", 'status': 400})

        elif nicknamecheck is not None:
            return jsonify({"msg": "닉네임이 존재할때", 'status': 400})

        else:
            if checkvalid.passwordCheck(pw) == 1:
                hashpw = bcrypt.hashpw(
                    pw.encode('utf-8'), bcrypt.gensalt())

                user = models.User(
                    nickname=nickname,
                    email=email,
                    name=name,
                    pw=hashpw,
                    birth=birth,
                    gender=gender,
                    sign_up_date=datetime.now()
                )
                models.db.session.add(user)
                models.db.session.commit()


                #바로 로그인 실행
                queried = models.User.query.filter_by(email=email).first()

                access_token = create_access_token(identity=queried.id, fresh=True)
                refresh_token = create_refresh_token(identity=queried.id)
                user_object = {
                    "id": queried.id,
                    "email": queried.email,
                    "nickname": queried.nickname,
                    "birth":queried.birth,
                    "gender":queried.gender,
                    "sign_up_date":queried.sign_up_date

                }

                return jsonify({
                                "msg": "회원가입 성공", 
                                'access_token': access_token,
                                'refresh_token': refresh_token,
                                'user_object': user_object,
                                'status': 200
                                })

            elif checkvalid.passwordCheck(pw) == 2:
                return jsonify({'msg': '비밀번호 기준에 맞지 않습니다. 비밀번호는 8자이상, 숫자+영어+특수문자 조합으로 이루어집니다.', 'status': 304})
            
            else:
                return jsonify({'msg': '비밀번호는 하나이상의 특수문자가 들어가야합니다', 'status': 400})


@bp.route('/sign-in', methods=['POST'])
@swag_from("../swagger_config/login.yml")
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request", 'status':400})

    else:
        # body = literal_eval(request.get_json()['body'])
        body=request.get_json()

        email = body['email']
        pw = body['pw']

        queried = models.User.query.filter_by(email=email).first()
        

        if queried is None:
            return jsonify({"msg": "존재하지 않는 회원입니다", 'status': 400})

        if not email:
            return jsonify({"msg": "아이디 치세요", 'status': 400})

        if not pw:
            return jsonify({"msg": "비번 치세요", 'status': 400})

        if bcrypt.checkpw(pw.encode('utf-8'), queried.pw.encode('utf-8')):
            access_token = create_access_token(identity=queried.id, fresh=True)
            refresh_token = create_refresh_token(identity=queried.id)
            user_object = {
                "id": queried.id,
                "email": queried.email,
                "nickname": queried.nickname,
                "birth":queried.birth,
                "gender":queried.gender,
                "sign_up_date":queried.sign_up_date

            }

            return jsonify({
                'access_token': access_token,
                'refresh_token': refresh_token,
                'user_object': user_object,
                'status': 200
            })

        else:
            return jsonify({"msg": "비밀번호 불일치", "status": 400})

@bp.route('/modification', methods=['POST'])
@swag_from("../swagger_config/modify.yml", validation=True)
# @jwt_required()
def modify():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request", "status":400 })

    else:
        # body = literal_eval(request.get_json()['body'])
        body=request.get_json()

        userid = body['id']
        email = body['email']
        pw = body['pw']
        name = body['name']
        nickname = body['nickname']

        hashpw = bcrypt.hashpw(
                    pw.encode('utf-8'), bcrypt.gensalt())

        admin=models.User.query.filter_by(id=userid).first()

        emailcheck=models.User.query.filter_by(email=email).all()
        nicknamecheck=models.User.query.filter_by(nickname=nickname).all()

        if admin.email != email and emailcheck is None :
            admin.email=email
            models.db.session.commit()
        
        if admin.pw != pw:
            admin.pw=hashpw
            models.db.session.commit()
       
        if admin.name != name:
            admin.name=name
            models.db.session.commit()
        
        if admin.nickname != nickname and nicknamecheck is None:
            admin.nickname=nickname
            models.db.session.commit()
        

        return jsonify({"msg": "회원변경 완료", "status": 200})

@bp.route('/withdrawal', methods=['POST'])
@swag_from("../swagger_config/withdrawal.yml", validation=True)
# @jwt_required()
def withdrawal():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request", "status":400 })

    else:
        # body = literal_eval(request.get_json()['body'])
        body=request.get_json()

        userid=body['id']
        pw=body['pw']

        admin=models.User.query.filter_by(id=userid).first()
        if bcrypt.checkpw(pw.encode('utf-8'), admin.pw.encode('utf-8')):
            models.db.session.delete(admin)
            models.db.session.commit()
            return jsonify({"msg": "회원탈퇴 완료", "status": 200})

        else:
            return jsonify({"msg": "비밀번호가 다릅니다", "status": 400})


@bp.route("/refresh", methods=["POST"])
# @swag_from("../swagger_config/refresh.yml", validation=True)
@jwt_required(refresh=True)
def refresh():
    """
    refresh
    ---
    description: refresh 토큰에서 id를 받아서 새로운 토큰을 만드는 api.
    responses:
      200:
        description: 성공적으로 access 토큰이 생성되었습니다.
    security:
      - ApiKeyAuth: []
    """
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity, fresh=False)
    return jsonify(access_token=access_token)


# Only allow fresh JWTs to access this route with the `fresh=True` arguement.
@bp.route("/protected", methods=["GET"])
# @swag_from("../swagger_config/protected.yml", validation=True)
@jwt_required(fresh=True)
def protected():
    """
    protected
    ---
    description: fresh=True인 토큰으로만 접근 가능한 api (로그인할 때 생성되는 access 토큰)
    responses:
      200:
        description: 성공적으로 접근했습니다.
    security:
      - ApiKeyAuth: []
    """
    return jsonify(foo="bar")

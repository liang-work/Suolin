import solar_network_sdk
from flask import render_template, Flask, request, jsonify
from flask_babel import Babel, gettext as _
import json
import os
import threading
import time

os.chdir(os.path.dirname(os.path.abspath(__file__))) ## set work dir
app = Flask(__name__, template_folder="UI", static_folder="UI/static/")
app.config['BABEL_DEFAULT_LOCALE'] = 'zh_CN'
app.config['BABEL_TRANSLATION_DIRECTORIES'] = 'translations'

babel = Babel(app)

def get_locale():
    # 从配置文件获取语言设置
    cfg = load_local_cfg()
    language = cfg.get("app_setting", {}).get("language", "zh_cn")
    return language.replace('_', '-')

babel.init_app(app)
# 全局变量用于存储认证状态
auth_states = {}


def load_local_cfg() ->dict: ## load local config
    DEFAULT_CONFIG = {
        "token":"",
        "app_setting":{
            "language":"zh_cn",
            "theme":"dark",
            "font":"a local path",
            "message_style": "bubble",
            "attachments_list_style":"row",
            "color_theme":"seedcolor",
            "card_opacity":0.8,
            "bg_img":"a local path"
        },
        "server_setting":{
            "server_URL":"https://api.solian.app",
            "attachments_pool":"SolarNetworkShared",
            "proxy":"a url",
            "timeout":10,
            "verify_ssl":True
        },
        "app_action":{
            "Sound_effects":True,
            "send_use_enter":True,
            "opacity_status_bar":True,
            "data_saver_mode":False,
            "show_chat_event_message":"none",
            "homepage":"dashboard",
            "search_engine":"https://www.bing.com/search?q={}"
        }
    }
    try:
        with open("data/user_cfg.json","r") as f:
            data = json.load(f)
            return data
    except (FileNotFoundError,json.JSONDecodeError,OSError,PermissionError):
        return DEFAULT_CONFIG

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/sidebar")
def sidebar():
    """返回侧边栏HTML内容，供其他页面动态加载"""
    return render_template("sidebar.html")

@app.route("/api/login", methods=["POST"])
def api_login():
    """普通登录API"""
    try:
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
        
        if not username or not password:
            return jsonify({"error": _("用户名和密码不能为空")}), 400
        
        # 创建Solar Network客户端
        client = solar_network_sdk.SolarNetworkClient()
        
        # 第一步：验证用户名/邮箱是否存在
        # 这里需要调用Solar Network的账户验证API
        # 由于SDK文档中没有明确的验证API，我们假设有一个验证方法
        try:
            # 检查账户是否存在（这里需要根据实际API调整）
            # account = client.get_account_by_username(username)  # 假设方法
            pass
        except Exception as e:
            return jsonify({"error": _("账户不存在或验证失败")}), 404
        
        # 第二步：获取账号支持的登录方式
        # 这里需要调用获取登录方式的API
        # login_methods = client.get_login_methods(username)  # 假设方法
        
        # 第三步：发送验证码（如果需要）
        # if 'email' in login_methods:
        #     client.send_verification_code(username, 'email')
        # elif 'sms' in login_methods:
        #     client.send_verification_code(username, 'sms')
        
        # 第四步：验证密码（简化流程，直接验证）
        # 这里应该调用实际的登录API
        # 实际的登录API可能需要用户名、密码和验证码
        
        # 模拟登录成功（实际应该调用SDK的登录方法）
        # login_result = client.login(username, password, verification_code)
        
        # 模拟登录成功
        token = "mock_token_123456"
        
        # 保存token到配置文件
        cfg = load_local_cfg()
        cfg["token"] = token
        save_local_cfg(cfg)
        
        return jsonify({
            "token": token,
            "user_id": "mock_user_id",
            "expires_in": 3600
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/check-token")
def api_check_token():
    """检查token是否有效"""
    try:
        cfg = load_local_cfg()
        token = cfg.get("token", "")
        
        if not token:
            return jsonify({"valid": False, "message": _("未找到有效token")})
        
        # 这里应该调用Solar Network的token验证API
        # 由于没有具体的API文档，这里模拟验证
        # 实际实现中应该使用solar_network_sdk验证token
        
        # 模拟token有效
        return jsonify({
            "valid": True,
            "token": token
        })
        
    except Exception as e:
        return jsonify({"valid": False, "error": str(e)}), 500

@app.route("/api/user-info")
def api_user_info():
    """获取用户信息"""
    try:
        cfg = load_local_cfg()
        token = cfg.get("token", "")
        
        if not token:
            return jsonify({"error": _("未找到有效token")}), 401
        
        # 这里应该调用Solar Network的用户信息API
        # 由于没有具体的API文档，这里模拟响应
        # 实际实现中应该使用solar_network_sdk获取用户信息
        
        # 模拟用户信息
        return jsonify({
            "user_id": "mock_user_id",
            "username": "mock_user",
            "email": "user@example.com",
            "display_name": "Mock User",
            "avatar_url": "",
            "created_at": "2024-01-01T00:00:00Z"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def save_local_cfg(cfg):
    """保存配置到文件"""
    try:
        os.makedirs("data", exist_ok=True)
        with open("data/user_cfg.json", "w", encoding="utf-8") as f:
            json.dump(cfg, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"保存配置文件失败: {e}")

@app.route("/api/auth/start", methods=["POST"])
def api_auth_start():
    """启动桌面应用认证"""
    try:
        # 创建WebAuthClient
        auth_client = solar_network_sdk.WebAuthClient()
        
        # 获取认证URL
        auth_url = auth_client.get_authentication_url()
        
        # 生成唯一的挑战ID
        import uuid
        challenge_id = str(uuid.uuid4())
        
        # 存储认证状态
        auth_states[challenge_id] = {
            "status": "pending",
            "auth_client": auth_client,
            "started_at": time.time()
        }
        
        # 这里应该打开浏览器或提示用户打开认证URL
        # 为了简化，我们直接返回认证URL
        return jsonify({
            "challenge_id": challenge_id,
            "auth_url": auth_url,
            "message": _("请在桌面应用中确认认证请求")
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/auth/status/<challenge_id>")
def api_auth_status(challenge_id):
    """检查认证状态"""
    try:
        if challenge_id not in auth_states:
            return jsonify({"status": "error", "error": _("无效的挑战ID")}), 404
        
        auth_state = auth_states[challenge_id]
        
        # 检查是否超时（5分钟）
        if time.time() - auth_state["started_at"] > 300:
            auth_states.pop(challenge_id)
            return jsonify({"status": "error", "error": _("认证已超时")}), 410
        
        # 使用WebAuthClient检查认证状态
        auth_client = auth_state["auth_client"]
        auth_result = auth_client.wait_for_auth()
        
        if auth_result.status == "challenge":
            # 如果有挑战，尝试交换token
            # 这里需要实现签名逻辑，为了简化先模拟
            signed_challenge = f"signed_{auth_result.challenge}"
            token_result = auth_client.exchange_token(signed_challenge)
            
            if token_result.status == "success":
                auth_states[challenge_id]["status"] = "success"
                auth_states[challenge_id]["token"] = token_result.token
                
                # 保存token到配置文件
                cfg = load_local_cfg()
                cfg["token"] = token_result.token
                save_local_cfg(cfg)
                
                return jsonify({
                    "status": "success",
                    "token": token_result.token
                })
            else:
                return jsonify({
                    "status": "error",
                    "error": token_result.error
                })
        elif auth_result.status == "denied":
            return jsonify({"status": "denied", "error": _("用户拒绝了认证请求")})
        else:
            # 继续等待
            return jsonify({"status": "pending"})
        
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500

@app.route("/api/logout", methods=["POST"])
def api_logout():
    """退出登录API"""
    try:
        # 清除配置文件中的token
        cfg = load_local_cfg()
        cfg["token"] = ""
        save_local_cfg(cfg)
        
        return jsonify({"success": True, "message": _("已退出登录")})
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
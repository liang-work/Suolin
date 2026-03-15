// 登录页面JavaScript
document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('login-form');
    const authBtn = document.getElementById('auth-btn');
    const loginMessage = document.getElementById('login-message');

    // 普通登录表单提交
    loginForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        
        showMessage('正在登录...', 'info');
        setButtonLoading(loginForm.querySelector('.btn-primary'), true);
        
        try {
            const response = await fetch('/api/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    username: username,
                    password: password
                })
            });
            
            const result = await response.json();
            
            if (response.ok) {
                showMessage('登录成功！', 'success');
                // 保存token到本地存储
                localStorage.setItem('solar_token', result.token);
                // 跳转到主页
                setTimeout(() => {
                    window.location.href = '/';
                }, 1000);
            } else {
                showMessage(result.error || '登录失败，请检查用户名和密码', 'error');
            }
        } catch (error) {
            showMessage('网络错误，请稍后重试', 'error');
            console.error('Login error:', error);
        } finally {
            setButtonLoading(loginForm.querySelector('.btn-primary'), false);
        }
    });

    // 桌面应用认证按钮
    authBtn.addEventListener('click', async function() {
        showMessage('正在启动桌面应用认证...', 'info');
        setButtonLoading(authBtn, true);
        
        try {
            const response = await fetch('/api/auth/start', {
                method: 'POST'
            });
            
            const result = await response.json();
            
            if (response.ok) {
                showMessage('请在桌面应用中确认认证请求...', 'info');
                // 轮询检查认证状态
                checkAuthStatus(result.challenge_id);
            } else {
                showMessage(result.error || '启动认证失败', 'error');
            }
        } catch (error) {
            showMessage('网络错误，请稍后重试', 'error');
            console.error('Auth start error:', error);
        } finally {
            setButtonLoading(authBtn, false);
        }
    });

    function showMessage(text, type) {
        loginMessage.textContent = text;
        loginMessage.className = `login-message ${type}`;
    }

    function setButtonLoading(button, loading) {
        if (loading) {
            button.classList.add('btn-loading');
            button.disabled = true;
        } else {
            button.classList.remove('btn-loading');
            button.disabled = false;
        }
    }

    function checkAuthStatus(challengeId) {
        const pollInterval = setInterval(async () => {
            try {
                const response = await fetch(`/api/auth/status/${challengeId}`);
                const result = await response.json();
                
                if (response.ok) {
                    if (result.status === 'success') {
                        clearInterval(pollInterval);
                        showMessage('认证成功！', 'success');
                        localStorage.setItem('solar_token', result.token);
                        setTimeout(() => {
                            window.location.href = '/';
                        }, 1000);
                    } else if (result.status === 'denied') {
                        clearInterval(pollInterval);
                        showMessage('认证被拒绝', 'error');
                    } else if (result.status === 'error') {
                        clearInterval(pollInterval);
                        showMessage(result.error || '认证过程中出现错误', 'error');
                    }
                }
            } catch (error) {
                clearInterval(pollInterval);
                showMessage('网络错误，请稍后重试', 'error');
            }
        }, 2000); // 每2秒检查一次
    }
});
# coding=utf-8


cookie_keys = dict(
    session_key_name="TR_SESSION_ID",
    uv_key_name="uv_tag",
)

# session相关配置（redis实现）
redis_session_config = dict(
    db_no=0,
    host="127.0.0.1",
    port=6379,
    password=None,
    max_connections=10,
    session_key_name=cookie_keys['session_key_name'],
    session_expires_days=7,
)

# 站点缓存(redis)
site_cache_config = dict(
    db_no=1,
    host="127.0.0.1",
    port=6379,
    password=None,
    max_connections=10,
)

# 基于redis的消息订阅（发布接收缓存更新消息）
redis_pub_sub_channels = dict(
    cache_message_channel="site_cache_message_channel",
)

# 消息订阅(基于redis)配置
redis_pub_sub_config = dict(
    host="127.0.0.1",
    port=6379,
    password=None,
    autoconnect=True,
    channels=[redis_pub_sub_channels['cache_message_channel'],],
)

# 数据库配置
database_config = dict(
    engine=None,
    engine_url='mysql+mysqldb://root:Hxhx3720@localhost:3306/tweet?charset=utf8',
    engine_setting=dict(
        echo=False,  # print sql
        echo_pool=False,
        pool_recycle=25200,
        pool_size=20,
        max_overflow=20,
    ),
)

session_keys = dict(
    login_user="login_user",
    messages="messages",
    article_draft="article_draft",
)


# site configs
config = dict(
    debug=True,
    log_level="WARNING",
    log_console=False,
    log_file=True,
    log_file_path="logs/log",  # 末尾自动添加 @端口号.txt_日期
    compress_response=True,
    xsrf_cookies=True,
    cookie_secret="kjsdhfweiofjhewnfiwehfneiwuhniu",
    login_url="/auth/login",
    port=8888,
    max_threads_num=500,
    database=database_config,
    redis_session=redis_session_config,
    session_keys=session_keys,
    master=True,
    navbar_styles={"inverse": "魅力黑", "default": "优雅白"},
    default_avatar_url="identicon",
    application=None,
)
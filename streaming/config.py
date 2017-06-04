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

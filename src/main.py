from litestar import Litestar
from litestar.config.cors import CORSConfig
from db import sqlspec_plugin
from routes import TaskController

# CORS設定
cors_config = CORSConfig(
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# アプリケーション作成
app = Litestar(
    route_handlers=[TaskController],
    plugins=[sqlspec_plugin],
    cors_config=cors_config,
    debug=True
)

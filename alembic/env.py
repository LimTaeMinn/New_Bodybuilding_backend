import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import auth.models  # User 모델은 auth/models.py 안에 있으니까
import models.competition
import models.routine
import models.bodyfat
import models.news





from dotenv import load_dotenv
load_dotenv()

# ✅ Base와 모델 import (모델은 반드시 import 되어야 자동 감지됨)
from database import Base

# Alembic config 설정
config = context.config
config.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL"))

# 로깅 설정
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ✅ Alembic이 참고할 메타데이터 지정
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

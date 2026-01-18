from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import NullPool

import os

USER = "postgres.fzytqvepxmjwsoumdpel"
PASSWORD = "qcBeUZFNvWXa6321"
HOST = "aws-1-us-east-1.pooler.supabase.com"
PORT = "5432"
DBNAME = "postgres"
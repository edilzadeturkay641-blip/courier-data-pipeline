from sqlalchemy import create_engine


def get_engine():
    engine = create_engine(
        "postgresql+psycopg2://postgres:Turk19971997@host.docker.internal:5432/KURYER"
    )
    return engine
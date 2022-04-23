from sqlalchemy.orm.session import Session
from db import get_db
from config import get_settings
from db.models import User
from sqlalchemy_seed import (
    create_table,
    drop_table,
    load_fixtures,
    load_fixture_files,
)


class Seeders():
    @staticmethod
    def execute():
        pass
        # session: Session = next(get_db(get_settings()))
        # path = 'db/seeders'

        # wallets = session.query(Wallet).first()
        # if not wallets:
        #     fixtures = load_fixture_files(path, ['wallets.yaml'])
        #     load_fixtures(session, fixtures)

        # sources = session.query(Source).first()
        # if not sources:
        #     fixtures = load_fixture_files(path, ['sources.yaml'])
        #     load_fixtures(session, fixtures)

    
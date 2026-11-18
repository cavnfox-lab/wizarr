"""Fork: a signed-out visitor to / lands on /join, not the admin login."""

from app.extensions import db
from app.models import Settings


def _set_admin(app):
    with app.app_context():
        if not Settings.query.filter_by(key="admin_username").first():
            db.session.add(Settings(key="admin_username", value="admin"))
            db.session.commit()


def test_root_without_admin_goes_to_setup(app, client):
    with app.app_context():
        Settings.query.filter_by(key="admin_username").delete()
        db.session.commit()

    resp = client.get("/")

    assert resp.status_code == 302
    assert resp.headers["Location"].endswith("/setup/")


def test_root_signed_out_goes_to_join(app, client):
    _set_admin(app)

    resp = client.get("/")

    assert resp.status_code == 302
    assert resp.headers["Location"].endswith("/join")

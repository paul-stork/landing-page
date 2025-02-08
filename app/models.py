from .extensions import db

class daily_crypto_prod(db.Model):
    __tablename__ = "daily_crypto_prod"
    __table_args__ = {"schema":"crypto_data"}
    id = db.Column(db.Integer, primary_key=True)
    exchange_id = db.Column(db.VARCHAR(5))
    rate_close = db.Column(db.Numeric(19, 9))
    rate_high = db.Column(db.Numeric(19, 9))
    rate_low = db.Column(db.Numeric(19, 9))
    rate_open = db.Column(db.Numeric(19, 9))
    time_close = db.Column(db.DateTime(timezone=True))
    time_open = db.Column(db.DateTime(timezone=True))
    time_period_end = db.Column(db.DateTime(timezone=True))
    time_period_start = db.Column(db.DateTime(timezone=True))
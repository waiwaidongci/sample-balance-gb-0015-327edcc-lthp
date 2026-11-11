from datetime import datetime
from sqlalchemy import String,ForeignKey,DateTime
from sqlalchemy.orm import Mapped,mapped_column
from src.config.database import Base
class WeightReview(Base):
    __tablename__='weight_reviews'
    id:Mapped[int]=mapped_column(primary_key=True)
    run_id:Mapped[int]=mapped_column(ForeignKey('weight_runs.id'),unique=True)
    decision:Mapped[str]=mapped_column(String(20))
    note:Mapped[str]=mapped_column(String(500))
    reviewer_id:Mapped[int]=mapped_column(ForeignKey('users.id'))
    created_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow)

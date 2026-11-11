from sqlalchemy import String,Float,ForeignKey,UniqueConstraint
from sqlalchemy.orm import Mapped,mapped_column
from src.config.database import Base
class SampleUnit(Base):
    __tablename__='sample_units'
    __table_args__=(UniqueConstraint('batch_id','code',name='uq_batch_code'),)
    id:Mapped[int]=mapped_column(primary_key=True)
    batch_id:Mapped[int]=mapped_column(ForeignKey('sample_batches.id'))
    code:Mapped[str]=mapped_column(String(60))
    zone:Mapped[str]=mapped_column(String(30))
    age_band:Mapped[str]=mapped_column(String(30))
    mode:Mapped[str]=mapped_column(String(30))
    trip_minutes:Mapped[float]=mapped_column(Float)
    base_weight:Mapped[float]=mapped_column(Float,default=1)

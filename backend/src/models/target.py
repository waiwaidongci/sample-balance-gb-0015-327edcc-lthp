from sqlalchemy import String,Float,ForeignKey,UniqueConstraint
from sqlalchemy.orm import Mapped,mapped_column
from src.config.database import Base
class MarginTarget(Base):
    __tablename__='margin_targets'
    __table_args__=(UniqueConstraint('batch_id','dimension','category',name='uq_target'),)
    id:Mapped[int]=mapped_column(primary_key=True)
    batch_id:Mapped[int]=mapped_column(ForeignKey('sample_batches.id'))
    dimension:Mapped[str]=mapped_column(String(30))
    category:Mapped[str]=mapped_column(String(30))
    population:Mapped[float]=mapped_column(Float)

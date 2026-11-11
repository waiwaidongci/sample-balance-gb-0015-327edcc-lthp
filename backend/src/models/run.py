from datetime import datetime
from sqlalchemy import ForeignKey,String,JSON,DateTime,Float
from sqlalchemy.orm import Mapped,mapped_column
from src.config.database import Base
class WeightRun(Base):
    __tablename__='weight_runs'
    id:Mapped[int]=mapped_column(primary_key=True)
    name:Mapped[str]=mapped_column(String(100))
    batch_id:Mapped[int]=mapped_column(ForeignKey('sample_batches.id'))
    tolerance:Mapped[float]=mapped_column(Float,default=.001)
    max_iterations:Mapped[int]=mapped_column(default=200)
    cap_ratio:Mapped[float]=mapped_column(Float,default=8)
    status:Mapped[str]=mapped_column(String(20),default='queued')
    input_snapshot:Mapped[dict|None]=mapped_column(JSON,nullable=True)
    result:Mapped[dict]=mapped_column(JSON,default=dict)
    error:Mapped[str|None]=mapped_column(String(500),nullable=True)
    created_by:Mapped[int]=mapped_column(ForeignKey('users.id'))
    created_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow)

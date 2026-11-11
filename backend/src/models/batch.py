from sqlalchemy import String
from sqlalchemy.orm import Mapped,mapped_column
from src.config.database import Base
class SampleBatch(Base):
    __tablename__='sample_batches'
    id:Mapped[int]=mapped_column(primary_key=True)
    code:Mapped[str]=mapped_column(String(60),unique=True)
    name:Mapped[str]=mapped_column(String(100))
    source_file:Mapped[str]=mapped_column(String(120))
    description:Mapped[str]=mapped_column(String(500),default='')

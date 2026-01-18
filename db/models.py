from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Text, DateTime, func, ForeignKey, String, Float, Integer
import uuid
from sqlalchemy.dialects.postgresql import UUID

class Base(DeclarativeBase):
    pass

class CaseRow(Base):
    __tablename__ = "CaseRow"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner_id: Mapped[str | None] = mapped_column(nullable=True)

    original_text: Mapped[str] = mapped_column(Text, nullable=False)
    tokenized_text: Mapped[str] = mapped_column(Text, nullable=False)

    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now())


class PiiMappingRow(Base):
    table_name = "PiiMappingRow"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    case_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("cases.id"), index=True)

    token: Mapped[str] = mapped_column(String(64), nullable=False)  # {{EMAIL_1}}
    entity_type: Mapped[str] = mapped_column(String(32), nullable=False)  # EMAIL
    original_value: Mapped[str] = mapped_column(Text, nullable=False)  # consider encrypting later
    score: Mapped[float | None] = mapped_column(Float, nullable=True)

    start: Mapped[int | None] = mapped_column(Integer, nullable=True)
    end: Mapped[int | None] = mapped_column(Integer, nullable=True)

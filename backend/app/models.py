from __future__ import annotations

from datetime import datetime
from typing import Any, Literal, Optional

from pydantic import BaseModel, Field, constr, condecimal


CurrencyCode = Literal["USD", "GBP", "EUR"]
EventStatus = Literal["prematch", "live", "finished"]
CustomerStatus = Literal["active", "disabled"]
BalanceChangeType = Literal["top_up", "bet_placed", "bet_settled", "withdrawal", "adjustment"]
PlacementStatus = Literal["pending", "placed", "failed"]
BetOutcome = Literal["win", "lose", "void"]


class MoneyAmount(BaseModel):
    amount: condecimal(max_digits=20, decimal_places=4) = Field(..., gt=-10_000_000_000, lt=10_000_000_000)
    currency: CurrencyCode


class Sport(BaseModel):
    name: constr(min_length=1)


class TeamCreate(BaseModel):
    name: str
    country: str
    sport: str


class Team(TeamCreate):
    id: int
    created_at: datetime
    updated_at: datetime


class CompetitionCreate(BaseModel):
    name: str
    country: str
    sport: str
    active: bool = True


class Competition(CompetitionCreate):
    id: int


class EventCreate(BaseModel):
    date: datetime
    competition_id: int
    team_a_id: int
    team_b_id: int
    status: EventStatus


class Event(EventCreate):
    id: int
    created_at: datetime
    updated_at: datetime


class ResultCreate(BaseModel):
    event_id: int
    score_a: int
    score_b: int


class Result(ResultCreate):
    created_at: datetime
    updated_at: datetime


class CustomerCreate(BaseModel):
    username: str
    password: str
    real_name: str
    currency: CurrencyCode
    status: CustomerStatus
    balance: MoneyAmount
    preferences: dict[str, Any] | None = Field(default_factory=dict)


class Customer(CustomerCreate):
    id: int
    created_at: datetime
    updated_at: datetime


class BookieCreate(BaseModel):
    name: str
    description: str
    preferences: dict[str, Any] | None = Field(default_factory=dict)


class Bookie(BookieCreate):
    pass


class BetCreate(BaseModel):
    bookie: str
    customer_id: int
    bookie_bet_id: str
    bet_type: str
    event_id: int
    sport: str
    placement_status: PlacementStatus = "pending"
    outcome: Optional[BetOutcome] = None
    stake: MoneyAmount
    odds: condecimal(max_digits=20, decimal_places=10) = Field(..., ge=1.01, le=999.0)
    placement_data: dict[str, Any]


class Bet(BetCreate):
    id: int
    created_at: datetime
    updated_at: datetime


class BalanceChangeCreate(BaseModel):
    customer_id: int
    change_type: BalanceChangeType
    delta: MoneyAmount
    reference_id: Optional[str] = None
    description: Optional[str] = None


class BalanceChange(BalanceChangeCreate):
    id: int
    created_at: datetime


class AuditLog(BaseModel):
    id: int
    table_name: str
    operation: Literal["INSERT", "UPDATE", "DELETE"]
    username: str
    changed_at: datetime
    row_id: Optional[int] = None
    old_data: Optional[dict[str, Any]] = None
    new_data: Optional[dict[str, Any]] = None


class CustomerStats(BaseModel):
    customer_id: int
    username: str
    currency: CurrencyCode
    total_bets: int
    won_bets: int
    lost_bets: int
    void_bets: int
    total_staked: float
    total_won: float
    net_profit: float
    current_balance: float



from __future__ import annotations

from typing import Any, Iterable

from fastapi import APIRouter, HTTPException, Query

from .db import db
from .models import (
    AuditLog,
    BalanceChange,
    BalanceChangeCreate,
    Bet,
    BetCreate,
    Bookie,
    BookieCreate,
    Competition,
    CompetitionCreate,
    Customer,
    CustomerCreate,
    CustomerStats,
    Event,
    EventCreate,
    Result,
    ResultCreate,
    Sport,
    Team,
    TeamCreate,
)


router = APIRouter()


def _row_to_money(row: Any, field: str) -> dict[str, Any]:
    amount, currency = row[field]
    return {"amount": float(amount), "currency": currency}


def _convert_money_fields(row: dict[str, Any], fields: Iterable[str]) -> dict[str, Any]:
    for f in fields:
        if f in row and row[f] is not None:
            amount, currency = row[f]
            row[f] = {"amount": float(amount), "currency": currency}
    return row


# Sports
@router.get("/sports", response_model=list[Sport])
async def list_sports() -> list[Sport]:
    async for conn in db.acquire():
        rows = await conn.fetch("SELECT name FROM sports ORDER BY name")
    return [Sport(name=r["name"]) for r in rows]


@router.post("/sports", response_model=Sport, status_code=201)
async def create_sport(sport: Sport) -> Sport:
    async for conn in db.acquire():
        await conn.execute("INSERT INTO sports(name) VALUES($1)", sport.name)
    return sport


@router.delete("/sports/{name}", status_code=204)
async def delete_sport(name: str) -> None:
    async for conn in db.acquire():
        await conn.execute("DELETE FROM sports WHERE name=$1", name)


# Teams
@router.get("/teams", response_model=list[Team])
async def list_teams() -> list[Team]:
    async for conn in db.acquire():
        rows = await conn.fetch(
            """
            SELECT id, name, country, sport, created_at, updated_at
            FROM teams ORDER BY id
            """
        )
    return [Team(**dict(r)) for r in rows]


@router.post("/teams", response_model=Team, status_code=201)
async def create_team(payload: TeamCreate) -> Team:
    async for conn in db.acquire():
        row = await conn.fetchrow(
            """
            INSERT INTO teams(name, country, sport)
            VALUES($1, $2, $3)
            RETURNING id, name, country, sport, created_at, updated_at
            """,
            payload.name,
            payload.country,
            payload.sport,
        )
    return Team(**dict(row))


@router.put("/teams/{team_id}", response_model=Team)
async def update_team(team_id: int, payload: TeamCreate) -> Team:
    async for conn in db.acquire():
        row = await conn.fetchrow(
            """
            UPDATE teams SET name=$1, country=$2, sport=$3
            WHERE id=$4
            RETURNING id, name, country, sport, created_at, updated_at
            """,
            payload.name,
            payload.country,
            payload.sport,
            team_id,
        )
    if not row:
        raise HTTPException(404, "Team not found")
    return Team(**dict(row))


@router.delete("/teams/{team_id}", status_code=204)
async def delete_team(team_id: int) -> None:
    async for conn in db.acquire():
        await conn.execute("DELETE FROM teams WHERE id=$1", team_id)


# Competitions
@router.get("/competitions", response_model=list[Competition])
async def list_competitions(active: bool | None = Query(None)) -> list[Competition]:
    async for conn in db.acquire():
        if active is None:
            rows = await conn.fetch(
                "SELECT id, name, country, sport, active FROM competitions ORDER BY id"
            )
        else:
            rows = await conn.fetch(
                "SELECT id, name, country, sport, active FROM competitions WHERE active=$1 ORDER BY id",
                active,
            )
    return [Competition(**dict(r)) for r in rows]


@router.post("/competitions", response_model=Competition, status_code=201)
async def create_competition(payload: CompetitionCreate) -> Competition:
    async for conn in db.acquire():
        row = await conn.fetchrow(
            """
            INSERT INTO competitions(name, country, sport, active)
            VALUES($1, $2, $3, $4)
            RETURNING id, name, country, sport, active
            """,
            payload.name,
            payload.country,
            payload.sport,
            payload.active,
        )
    return Competition(**dict(row))


@router.put("/competitions/{competition_id}", response_model=Competition)
async def update_competition(competition_id: int, payload: CompetitionCreate) -> Competition:
    async for conn in db.acquire():
        row = await conn.fetchrow(
            """
            UPDATE competitions SET name=$1, country=$2, sport=$3, active=$4
            WHERE id=$5
            RETURNING id, name, country, sport, active
            """,
            payload.name,
            payload.country,
            payload.sport,
            payload.active,
            competition_id,
        )
    if not row:
        raise HTTPException(404, "Competition not found")
    return Competition(**dict(row))


@router.delete("/competitions/{competition_id}", status_code=204)
async def delete_competition(competition_id: int) -> None:
    async for conn in db.acquire():
        await conn.execute("DELETE FROM competitions WHERE id=$1", competition_id)


# Events
@router.get("/events", response_model=list[Event])
async def list_events() -> list[Event]:
    async for conn in db.acquire():
        rows = await conn.fetch(
            """
            SELECT id, date, competition_id, team_a_id, team_b_id, status, created_at, updated_at
            FROM events ORDER BY date DESC
            """
        )
    return [Event(**dict(r)) for r in rows]


@router.post("/events", response_model=Event, status_code=201)
async def create_event(payload: EventCreate) -> Event:
    async for conn in db.acquire():
        row = await conn.fetchrow(
            """
            INSERT INTO events(date, competition_id, team_a_id, team_b_id, status)
            VALUES($1, $2, $3, $4, $5)
            RETURNING id, date, competition_id, team_a_id, team_b_id, status, created_at, updated_at
            """,
            payload.date,
            payload.competition_id,
            payload.team_a_id,
            payload.team_b_id,
            payload.status,
        )
    return Event(**dict(row))


@router.put("/events/{event_id}", response_model=Event)
async def update_event(event_id: int, payload: EventCreate) -> Event:
    async for conn in db.acquire():
        row = await conn.fetchrow(
            """
            UPDATE events SET date=$1, competition_id=$2, team_a_id=$3, team_b_id=$4, status=$5
            WHERE id=$6
            RETURNING id, date, competition_id, team_a_id, team_b_id, status, created_at, updated_at
            """,
            payload.date,
            payload.competition_id,
            payload.team_a_id,
            payload.team_b_id,
            payload.status,
            event_id,
        )
    if not row:
        raise HTTPException(404, "Event not found")
    return Event(**dict(row))


@router.delete("/events/{event_id}", status_code=204)
async def delete_event(event_id: int) -> None:
    async for conn in db.acquire():
        await conn.execute("DELETE FROM events WHERE id=$1", event_id)


# Results
@router.get("/results", response_model=list[Result])
async def list_results() -> list[Result]:
    async for conn in db.acquire():
        rows = await conn.fetch(
            "SELECT event_id, score_a, score_b, created_at, updated_at FROM results ORDER BY event_id"
        )
    return [Result(**dict(r)) for r in rows]


@router.post("/results", response_model=Result, status_code=201)
async def create_result(payload: ResultCreate) -> Result:
    async for conn in db.acquire():
        row = await conn.fetchrow(
            """
            INSERT INTO results(event_id, score_a, score_b)
            VALUES($1, $2, $3)
            RETURNING event_id, score_a, score_b, created_at, updated_at
            """,
            payload.event_id,
            payload.score_a,
            payload.score_b,
        )
    return Result(**dict(row))


@router.put("/results/{event_id}", response_model=Result)
async def update_result(event_id: int, payload: ResultCreate) -> Result:
    async for conn in db.acquire():
        row = await conn.fetchrow(
            """
            UPDATE results SET score_a=$1, score_b=$2
            WHERE event_id=$3
            RETURNING event_id, score_a, score_b, created_at, updated_at
            """,
            payload.score_a,
            payload.score_b,
            event_id,
        )
    if not row:
        raise HTTPException(404, "Result not found")
    return Result(**dict(row))


@router.delete("/results/{event_id}", status_code=204)
async def delete_result(event_id: int) -> None:
    async for conn in db.acquire():
        await conn.execute("DELETE FROM results WHERE event_id=$1", event_id)


# Customers
@router.get("/customers", response_model=list[Customer])
async def list_customers() -> list[Customer]:
    async for conn in db.acquire():
        rows = await conn.fetch(
            """
            SELECT id, username, password, real_name, currency, status, balance, preferences, created_at, updated_at
            FROM customers ORDER BY id
            """
        )
    result: list[Customer] = []
    for r in rows:
        data = dict(r)
        data = _convert_money_fields(data, ["balance"])
        result.append(Customer(**data))
    return result


@router.post("/customers", response_model=Customer, status_code=201)
async def create_customer(payload: CustomerCreate) -> Customer:
    async for conn in db.acquire():
        row = await conn.fetchrow(
            """
            INSERT INTO customers(username, password, real_name, currency, status, balance, preferences)
            VALUES($1, $2, $3, $4, $5, ROW($6::decimal, $4)::money_amount, $7)
            RETURNING id, username, password, real_name, currency, status, balance, preferences, created_at, updated_at
            """,
            payload.username,
            payload.password,
            payload.real_name,
            payload.currency,
            payload.status,
            payload.balance.amount,
            payload.preferences or {},
        )
    data = dict(row)
    data = _convert_money_fields(data, ["balance"])
    return Customer(**data)


@router.put("/customers/{customer_id}", response_model=Customer)
async def update_customer(customer_id: int, payload: CustomerCreate) -> Customer:
    async for conn in db.acquire():
        row = await conn.fetchrow(
            """
            UPDATE customers SET
              username=$1, password=$2, real_name=$3,
              currency=$4, status=$5, balance=ROW($6::decimal, $4)::money_amount, preferences=$7
            WHERE id=$8
            RETURNING id, username, password, real_name, currency, status, balance, preferences, created_at, updated_at
            """,
            payload.username,
            payload.password,
            payload.real_name,
            payload.currency,
            payload.status,
            payload.balance.amount,
            payload.preferences or {},
            customer_id,
        )
    if not row:
        raise HTTPException(404, "Customer not found")
    data = dict(row)
    data = _convert_money_fields(data, ["balance"])
    return Customer(**data)


@router.delete("/customers/{customer_id}", status_code=204)
async def delete_customer(customer_id: int) -> None:
    async for conn in db.acquire():
        await conn.execute("DELETE FROM customers WHERE id=$1", customer_id)


# Bookies
@router.get("/bookies", response_model=list[Bookie])
async def list_bookies() -> list[Bookie]:
    async for conn in db.acquire():
        rows = await conn.fetch(
            "SELECT name, description, preferences FROM bookies ORDER BY name"
        )
    return [Bookie(**dict(r)) for r in rows]


@router.post("/bookies", response_model=Bookie, status_code=201)
async def create_bookie(payload: BookieCreate) -> Bookie:
    async for conn in db.acquire():
        await conn.execute(
            "INSERT INTO bookies(name, description, preferences) VALUES($1, $2, $3)",
            payload.name,
            payload.description,
            payload.preferences or {},
        )
    return Bookie(**payload.model_dump())


@router.put("/bookies/{name}", response_model=Bookie)
async def update_bookie(name: str, payload: BookieCreate) -> Bookie:
    async for conn in db.acquire():
        cmd = await conn.execute(
            "UPDATE bookies SET name=$1, description=$2, preferences=$3 WHERE name=$4",
            payload.name,
            payload.description,
            payload.preferences or {},
            name,
        )
    if cmd.endswith("UPDATE 0"):
        raise HTTPException(404, "Bookie not found")
    return Bookie(**payload.model_dump())


@router.delete("/bookies/{name}", status_code=204)
async def delete_bookie(name: str) -> None:
    async for conn in db.acquire():
        await conn.execute("DELETE FROM bookies WHERE name=$1", name)


# Bets
@router.get("/bets", response_model=list[Bet])
async def list_bets() -> list[Bet]:
    async for conn in db.acquire():
        rows = await conn.fetch(
            """
            SELECT id, bookie, customer_id, bookie_bet_id, bet_type, event_id, sport,
                   placement_status, outcome, stake, odds, placement_data, created_at, updated_at
            FROM bets ORDER BY created_at DESC
            """
        )
    result: list[Bet] = []
    for r in rows:
        data = dict(r)
        data = _convert_money_fields(data, ["stake"])
        result.append(Bet(**data))
    return result


@router.post("/bets", response_model=Bet, status_code=201)
async def create_bet(payload: BetCreate) -> Bet:
    async for conn in db.acquire():
        row = await conn.fetchrow(
            """
            INSERT INTO bets(
                bookie, customer_id, bookie_bet_id, bet_type, event_id, sport,
                placement_status, outcome, stake, odds, placement_data
            ) VALUES(
                $1, $2, $3, $4, $5, $6, $7, $8, ROW($9::decimal, $10)::money_amount, $11, $12
            )
            RETURNING id, bookie, customer_id, bookie_bet_id, bet_type, event_id, sport,
                      placement_status, outcome, stake, odds, placement_data, created_at, updated_at
            """,
            payload.bookie,
            payload.customer_id,
            payload.bookie_bet_id,
            payload.bet_type,
            payload.event_id,
            payload.sport,
            payload.placement_status,
            payload.outcome,
            payload.stake.amount,
            payload.stake.currency,
            payload.odds,
            payload.placement_data,
        )
    data = dict(row)
    data = _convert_money_fields(data, ["stake"])
    return Bet(**data)


@router.put("/bets/{bet_id}", response_model=Bet)
async def update_bet(bet_id: int, payload: BetCreate) -> Bet:
    async for conn in db.acquire():
        row = await conn.fetchrow(
            """
            UPDATE bets SET
                bookie=$1, customer_id=$2, bookie_bet_id=$3, bet_type=$4, event_id=$5, sport=$6,
                placement_status=$7, outcome=$8, stake=ROW($9::decimal, $10)::money_amount, odds=$11, placement_data=$12
            WHERE id=$13
            RETURNING id, bookie, customer_id, bookie_bet_id, bet_type, event_id, sport,
                      placement_status, outcome, stake, odds, placement_data, created_at, updated_at
            """,
            payload.bookie,
            payload.customer_id,
            payload.bookie_bet_id,
            payload.bet_type,
            payload.event_id,
            payload.sport,
            payload.placement_status,
            payload.outcome,
            payload.stake.amount,
            payload.stake.currency,
            payload.odds,
            payload.placement_data,
            bet_id,
        )
    if not row:
        raise HTTPException(404, "Bet not found")
    data = dict(row)
    data = _convert_money_fields(data, ["stake"])
    return Bet(**data)


@router.delete("/bets/{bet_id}", status_code=204)
async def delete_bet(bet_id: int) -> None:
    async for conn in db.acquire():
        await conn.execute("DELETE FROM bets WHERE id=$1", bet_id)


# Balance changes
@router.get("/balance_changes", response_model=list[BalanceChange])
async def list_balance_changes() -> list[BalanceChange]:
    async for conn in db.acquire():
        rows = await conn.fetch(
            "SELECT id, customer_id, change_type, delta, reference_id, description, created_at FROM balance_changes ORDER BY created_at DESC"
        )
    result: list[BalanceChange] = []
    for r in rows:
        data = dict(r)
        data = _convert_money_fields(data, ["delta"])
        result.append(BalanceChange(**data))
    return result


@router.post("/balance_changes", response_model=BalanceChange, status_code=201)
async def create_balance_change(payload: BalanceChangeCreate) -> BalanceChange:
    async for conn in db.acquire():
        row = await conn.fetchrow(
            """
            INSERT INTO balance_changes(customer_id, change_type, delta, reference_id, description)
            VALUES($1, $2, ROW($3::decimal, $4)::money_amount, $5, $6)
            RETURNING id, customer_id, change_type, delta, reference_id, description, created_at
            """,
            payload.customer_id,
            payload.change_type,
            payload.delta.amount,
            payload.delta.currency,
            payload.reference_id,
            payload.description,
        )
    data = dict(row)
    data = _convert_money_fields(data, ["delta"])
    return BalanceChange(**data)


# Audit and stats
@router.get("/audit", response_model=list[AuditLog])
async def list_audit(table: str | None = Query(None)) -> list[AuditLog]:
    async for conn in db.acquire():
        if table:
            rows = await conn.fetch(
                """
                SELECT id, table_name, operation, username, changed_at, row_id, old_data, new_data
                FROM audit_log WHERE table_name=$1 ORDER BY changed_at DESC
                """,
                table,
            )
        else:
            rows = await conn.fetch(
                """
                SELECT id, table_name, operation, username, changed_at, row_id, old_data, new_data
                FROM audit_log ORDER BY changed_at DESC
                """
            )
    return [AuditLog(**dict(r)) for r in rows]


@router.get("/customer_stats", response_model=list[CustomerStats])
async def list_customer_stats() -> list[CustomerStats]:
    async for conn in db.acquire():
        rows = await conn.fetch(
            """
            SELECT customer_id, username, currency, total_bets, won_bets, lost_bets, void_bets,
                   total_staked, total_won, net_profit, current_balance
            FROM customer_stats ORDER BY customer_id
            """
        )
    return [CustomerStats(**dict(r)) for r in rows]



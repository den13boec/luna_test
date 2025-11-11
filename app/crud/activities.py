from typing import Sequence
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.activity import Activity


def get_activity(db: Session, activity_id: int) -> Activity | None:
    """Один вид деятельности по ID."""
    return db.get_one(Activity, activity_id)


def list_activities(db: Session) -> Sequence[Activity]:
    """Все виды деятельности (плоский список)."""
    return db.execute(select(Activity).order_by(Activity.id)).scalars().all()


def get_activity_by_name(db: Session, name: str) -> Activity | None:
    """Вид деятельности по точному названию."""
    stmt = select(Activity).where(Activity.name == name).limit(1)
    return db.execute(stmt).scalar_one_or_none()


def get_descendant_ids(db: Session, root_id: int) -> list[int]:
    """
    ID корня + всех потомков (рекурсивный CTE).
    В БД у нас depth ограничен 1..3, так что глубже не уйдёт.
    """

    activity = Activity.__table__
    cte = select(activity.c.id).where(activity.c.id == root_id).cte(recursive=True)
    child = select(activity.c.id).where(activity.c.parent_id == cte.c.id)
    cte = cte.union_all(child)
    return list(set(db.execute(select(cte.c.id)).scalars().all()))


def build_activity_tree(db: Session, root_id: int | None = None) -> list[dict]:
    """
    Дерево для /activities/tree.
    Возвращаем список словарей {id, name, parent_id, depth, children:[...]}
    - Pydantic сам приведёт к ActivityTree.
    """
    items = list_activities(db)
    by_id: dict[int, dict] = {
        a.id: {
            "id": a.id,
            "name": a.name,
            "parent_id": a.parent_id,
            "depth": a.depth,
            "children": [],
        }
        for a in items
    }
    roots: list[dict] = []
    for a in items:
        node = by_id[a.id]
        if a.parent_id and a.parent_id in by_id:
            by_id[a.parent_id]["children"].append(node)
        else:
            roots.append(node)
    if root_id is not None:
        return [by_id[root_id]] if root_id in by_id else []
    return roots

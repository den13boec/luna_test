from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.activity import Activity


def get_activity(db: Session, activity_id: int) -> Activity | None:
    return db.get(Activity, activity_id)


def list_activities(db: Session):
    return db.execute(select(Activity).order_by(Activity.id)).scalars().all()


def get_descendant_ids(db: Session, root_id: int) -> list[int]:
    from sqlalchemy import select

    activity = Activity.__table__
    cte = select(activity.c.id).where(activity.c.id == root_id).cte(recursive=True)
    child = select(activity.c.id).where(activity.c.parent_id == cte.c.id)
    cte = cte.union_all(child)
    return list(set(db.execute(select(cte.c.id)).scalars().all()))


def build_tree(items: list[Activity]) -> list[dict]:
    by_id = {
        a.id: {
            "id": a.id,
            "name": a.name,
            "parent_id": a.parent_id,
            "depth": a.depth,
            "children": [],
        }
        for a in items
    }
    roots = []
    for a in items:
        node = by_id[a.id]
        if a.parent_id and a.parent_id in by_id:
            by_id[a.parent_id]["children"].append(node)
        else:
            roots.append(node)
    return roots

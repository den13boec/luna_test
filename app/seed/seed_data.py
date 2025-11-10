from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.session import SessionLocal
from app.models.building import Building
from app.models.activity import Activity
from app.models.organization import Organization
from app.models.phone import Phone


def upsert_activity(
    db: Session, name: str, parent: Activity | None, depth: int
) -> Activity:
    """Creates an activity if it doesn't exist; returns an existing one by (name, parent_id)."""
    stmt = (
        select(Activity)
        .where(
            Activity.name == name,
            Activity.parent_id == (parent.id if parent else None),
        )
        .limit(1)
    )
    found = db.execute(stmt).scalar_one_or_none()
    if found:
        return found
    a = Activity(name=name, parent_id=(parent.id if parent else None), depth=depth)
    db.add(a)
    db.flush()
    return a


def upsert_building(db: Session, address: str, lat: float, lon: float) -> Building:
    stmt = (
        select(Building)
        .where(
            Building.address == address,
            Building.latitude == lat,
            Building.longitude == lon,
        )
        .limit(1)
    )
    found = db.execute(stmt).scalar_one_or_none()
    if found:
        return found
    b = Building(address=address, latitude=lat, longitude=lon)
    db.add(b)
    db.flush()
    return b


def upsert_org(db: Session, name: str, building: Building) -> Organization:
    stmt = (
        select(Organization)
        .where(
            Organization.name == name,
            Organization.building_id == building.id,
        )
        .limit(1)
    )
    found = db.execute(stmt).scalar_one_or_none()
    if found:
        return found
    o = Organization(name=name, building_id=building.id)
    db.add(o)
    db.flush()
    return o


def upsert_phone(db: Session, org: Organization, phone: str) -> Phone:
    stmt = (
        select(Phone)
        .where(
            Phone.organization_id == org.id,
            Phone.phone == phone,
        )
        .limit(1)
    )
    found = db.execute(stmt).scalar_one_or_none()
    if found:
        return found
    p = Phone(organization_id=org.id, phone=phone)
    db.add(p)
    db.flush()
    return p


def ensure_data(db: Session):
    # If something already exists, skip the seed
    if db.query(Activity).count() > 0 or db.query(Organization).count() > 0:
        return

    # === Activities (3 levels) ===
    # 1) tech
    tech = upsert_activity(db, "Технологии", None, 1)
    dev = upsert_activity(db, "Разработка ПО", tech, 2)
    infra = upsert_activity(db, "Инфраструктура", tech, 2)
    web = upsert_activity(db, "Веб-разработка", dev, 3)
    mobile = upsert_activity(db, "Мобильная разработка", dev, 3)
    devops = upsert_activity(db, "DevOps", infra, 3)
    sre = upsert_activity(db, "SRE", infra, 3)

    # 2) healthcare
    health = upsert_activity(db, "Здоровье", None, 1)
    dental = upsert_activity(db, "Стоматология", health, 2)
    pharmacy = upsert_activity(db, "Аптеки", health, 2)

    # 3) education
    edu = upsert_activity(db, "Образование", None, 1)
    langs = upsert_activity(db, "Языковые курсы", edu, 2)
    online = upsert_activity(db, "Онлайн-школы", edu, 2)

    # === Buildings (different cities/coordinates) ===
    b_spb = upsert_building(
        db, "Санкт-Петербург, Невский проспект, 28", 59.9343, 30.3351
    )
    b_kzn = upsert_building(db, "Казань, ул. Баумана, 15", 55.7963, 49.1088)
    b_nsk = upsert_building(db, "Новосибирск, Красный проспект, 50", 55.0415, 82.9346)
    b_ekb = upsert_building(db, "Екатеринбург, пр. Ленина, 24", 56.8380, 60.5975)
    b_hki = upsert_building(db, "Helsinki, Aleksanterinkatu 17", 60.1699, 24.9384)

    # === Organizations ===
    o_nord = upsert_org(db, "ООО НордСофт", b_spb)
    o_kzph = upsert_org(db, "ООО КазаньФарм", b_kzn)
    o_sibd = upsert_org(db, "АО СибСтом", b_nsk)
    o_devx = upsert_org(db, "ИП Петров DevOps-аутсорс", b_ekb)
    o_finedu = upsert_org(db, "FinEd Tutor Oy", b_hki)

    # Phone number
    for ph in ("+7 (812) 200-45-45", "+7 931 000-77-88"):
        upsert_phone(db, o_nord, ph)
    upsert_phone(db, o_kzph, "+7 (843) 555-33-22")
    upsert_phone(db, o_sibd, "+7 (383) 201-10-10")
    upsert_phone(db, o_devx, "+7 (343) 900-00-01")
    upsert_phone(db, o_finedu, "+358 44 123 45 67")

    # Link activities to organizations
    o_nord.activities.extend([web])
    o_kzph.activities.extend([pharmacy])
    o_sibd.activities.extend([dental])
    o_devx.activities.extend([devops, sre])
    o_finedu.activities.extend([langs, online])

    db.commit()


if __name__ == "__main__":
    db = SessionLocal()
    try:
        ensure_data(db)
    finally:
        db.close()

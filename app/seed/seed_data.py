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


def ensure_data(db: Session) -> None:
    # If something already exists, skip the seed
    if db.query(Activity).count() > 0 or db.query(Organization).count() > 0:
        return

    # === Activities ===
    # 1) tech
    tech = upsert_activity(db, "Технологии", None, 1)
    dev = upsert_activity(db, "Разработка ПО", tech, 2)
    infra = upsert_activity(db, "Инфраструктура", tech, 2)
    anal = upsert_activity(db, "Аналитика", tech, 2)

    a_web = upsert_activity(db, "Веб-разработка", dev, 3)
    a_mob = upsert_activity(db, "Мобильная разработка", dev, 3)
    a_devops = upsert_activity(db, "DevOps", infra, 3)
    a_sre = upsert_activity(db, "SRE", infra, 3)
    a_bi = upsert_activity(db, "BI", anal, 3)
    a_ds = upsert_activity(db, "Data Science", anal, 3)

    # 2) healthcare
    health = upsert_activity(db, "Здоровье", None, 1)
    a_dental = upsert_activity(db, "Стоматология", health, 2)
    a_pharmacy = upsert_activity(db, "Аптеки", health, 2)

    # 3) education
    edu = upsert_activity(db, "Образование", None, 1)
    a_langs = upsert_activity(db, "Языковые курсы", edu, 2)
    a_online = upsert_activity(db, "Онлайн-школы", edu, 2)
    a_univ = upsert_activity(db, "ВУЗы", edu, 2)

    # 4) food
    food = upsert_activity(db, "Еда", None, 1)
    a_rest = upsert_activity(db, "Рестораны", food, 2)
    a_coffee = upsert_activity(db, "Кофейни", food, 2)
    a_meat = upsert_activity(db, "Мясная продукция", food, 2)
    a_milk = upsert_activity(db, "Молочная продукция", food, 2)

    # 5) retail
    retail = upsert_activity(db, "Ритейл", None, 1)
    a_elec = upsert_activity(db, "Электроника", retail, 2)
    a_cloth = upsert_activity(db, "Одежда", retail, 2)

    # 6) services
    services = upsert_activity(db, "Услуги", None, 1)
    a_logi = upsert_activity(db, "Логистика", services, 2)
    a_clean = upsert_activity(db, "Клининг", services, 2)
    a_mkt = upsert_activity(db, "Маркетинг", services, 2)

    # dict for binding by name
    ACT = {
        "web": a_web,
        "mobile": a_mob,
        "devops": a_devops,
        "sre": a_sre,
        "bi": a_bi,
        "ds": a_ds,
        "dental": a_dental,
        "pharmacy": a_pharmacy,
        "langs": a_langs,
        "online": a_online,
        "univ": a_univ,
        "rest": a_rest,
        "coffee": a_coffee,
        "meat": a_meat,
        "milk": a_milk,
        "elec": a_elec,
        "cloth": a_cloth,
        "logi": a_logi,
        "clean": a_clean,
        "mkt": a_mkt,
    }

    # === Buildings (20+) ===
    buildings_data = [
        ("Санкт-Петербург, Невский проспект, 28", 59.9343, 30.3351),
        ("Москва, Тверская ул., 7", 55.7577, 37.6139),
        ("Казань, ул. Баумана, 15", 55.7963, 49.1088),
        ("Новосибирск, Красный проспект, 50", 55.0415, 82.9346),
        ("Екатеринбург, пр. Ленина, 24", 56.8380, 60.5975),
        ("Нижний Новгород, Большая Покровская, 10", 56.3269, 44.0059),
        ("Самара, ул. Ленинградская, 45", 53.1959, 50.1000),
        ("Уфа, ул. Ленина, 3", 54.7388, 55.9721),
        ("Пермь, Комсомольский пр., 20", 58.0105, 56.2294),
        ("Ростов-на-Дону, ул. Садовая, 12", 47.2357, 39.7015),
        ("Воронеж, пр-т Революции, 6", 51.6755, 39.2089),
        ("Краснодар, ул. Красная, 120", 45.0355, 38.9753),
        ("Сочи, ул. Навагинская, 9", 43.6028, 39.7342),
        ("Калининград, ул. Ленинский пр., 29", 54.7104, 20.4522),
        ("Мурманск, пр-т Ленина, 32", 68.9585, 33.0827),
        ("Владивосток, Светланская ул., 15", 43.1155, 131.8855),
        ("Омск, ул. Ленина, 5", 54.9885, 73.3242),
        ("Томск, пр. Ленина, 50", 56.5010, 84.9925),
        ("Тула, пр-т Ленина, 14", 54.1961, 37.6182),
        ("Helsinki, Aleksanterinkatu 17", 60.1699, 24.9384),
        ("Tallinn, Viru väljak 4", 59.4370, 24.7536),
    ]
    buildings: list[Building] = [upsert_building(db, *b) for b in buildings_data]

    # Удобные псевдонимы на используемые индексы
    bi = lambda i: buildings[i]

    # === Organizations (~45 штук, часть с 2мя телефонами и/или 2мя активностями) ===
    # name, building_idx, activities(keys from ACT), phones_count
    plan = [
        # b0 СПб (3)
        ("ООО НордСофт", 0, ["web"], 2),
        ("ООО ПитерКофе", 0, ["coffee"], 1),
        ("ООО Питер-Электро", 0, ["elec"], 1),
        # b1 Москва (4)
        ("ООО МосТех Аналитика", 1, ["bi", "ds"], 2),
        ("АО СтолицаФарм", 1, ["pharmacy"], 1),
        ("ООО Москва-Ресторан", 1, ["rest"], 1),
        ("ООО Москва-Одежда", 1, ["cloth"], 1),
        # b2 Казань (3)
        ("ИП Бауман Дев", 2, ["mobile", "web"], 1),
        ("ОАО КазаньМолоко", 2, ["milk"], 1),
        ("ООО Казань-Кофе", 2, ["coffee"], 1),
        # b3 Новосибирск (2)
        ("АО СибСтом", 3, ["dental"], 1),
        ("ООО Новосиб-Онлайн", 3, ["online"], 1),
        # b4 Екатеринбург (2)
        ("ИП Петров DevOps-аутсорс", 4, ["devops", "sre"], 1),
        ("ООО Екатеринбург-Аптека", 4, ["pharmacy"], 1),
        # b5 Нижний (2)
        ("ООО Умный Дом", 5, ["elec"], 1),
        ("ООО NN University Labs", 5, ["univ", "ds"], 2),
        # b6 Самара (2)
        ("ООО Самарская Логистика", 6, ["logi"], 1),
        ("ООО СамараМаркет", 6, ["mkt"], 1),
        # b7 Уфа (2)
        ("ИП УфаКлининг", 7, ["clean"], 1),
        ("ООО УфаКофе", 7, ["coffee"], 1),
        # b8 Пермь (1)
        ("ООО ПермьТехСервис", 8, ["devops"], 1),
        # b9 Ростов (3)
        ("ООО РостовРесторан", 9, ["rest"], 1),
        ("ООО РостовОдежда", 9, ["cloth"], 1),
        ("ООО Ростов-Логистика", 9, ["logi"], 1),
        # b10 Воронеж (2)
        ("ИП Воронеж-Мясо", 10, ["meat"], 1),
        ("ООО Воронеж-DS", 10, ["ds"], 1),
        # b11 Краснодар (2)
        ("ООО Краснодар Электро", 11, ["elec"], 1),
        ("ООО Краснодар-Доставка", 11, ["logi"], 1),
        # b12 Сочи (2)
        ("ООО Сочи-Ривьера", 12, ["rest", "coffee"], 2),
        ("ООО Сочи-Klin", 12, ["clean"], 1),
        # b13 Калининград (2)
        ("ООО Кёниг Аптека", 13, ["pharmacy"], 1),
        ("ООО КёнигМаркет", 13, ["mkt"], 1),
        # b14 Мурманск (1)
        ("ООО МурманМолоко", 14, ["milk"], 1),
        # b15 Владивосток (2)
        ("ООО ВладивостокТех", 15, ["web", "devops"], 1),
        ("ООО ВладКофе", 15, ["coffee"], 1),
        # b16 Омск (1)
        ("ООО ОмскОдежда", 16, ["cloth"], 1),
        # b17 Томск (2)
        ("ООО ТомскУнивер", 17, ["univ"], 1),
        ("ООО ТомскОнлайн", 17, ["online"], 1),
        # b18 Тула (1)
        ("ООО ТулаЛогистика", 18, ["logi"], 1),
        # b19 Хельсинки (3)
        ("FinEd Tutor Oy", 19, ["langs", "online"], 1),
        ("Helsinki Coffee Roasters", 19, ["coffee"], 1),
        ("Helsinki Analytics Oy", 19, ["bi"], 1),
        # b20 Таллин (3)
        ("Tallinn Tech OÜ", 20, ["web", "sre"], 1),
        ("Tallinn Dental OÜ", 20, ["dental"], 1),
        ("Tallinn Market OÜ", 20, ["mkt"], 1),
    ]

    # range of acceptable prefixes
    PHONE_PREFIX_RANGE = (900, 999)

    _seen_phones: set[str] = set()

    def make_phone(i: int, j: int = 0) -> str:
        """
        Генерит номер вида: +7 PPP XXX-YY-ZZ
        - PPP — псевдослучайный в заданном диапазоне (по умолчанию 900..999)
        - Уникальность гарантируется глобально (через _seen_phones)
        - Детерминированно от (i, j), чтобы сиды были стабильными между запусками
        """
        lo, hi = PHONE_PREFIX_RANGE
        span = hi - lo + 1

        # just in case, if we suddenly collide
        for salt in range(100):
            # without random library
            pref = lo + ((i * 41 + j * 13 + salt) % span)  # 900...999
            block = (i * 137 + j * 97 + salt) % 1000  # 000...999
            yy = (i * 53 + j * 31 + salt) % 100  # 00...99
            zz = (i * 71 + j * 11 + salt) % 100  # 00...99

            cand = f"+7 {pref} {block:03d}-{yy:02d}-{zz:02d}"
            if cand not in _seen_phones:
                _seen_phones.add(cand)
                return cand

        raise RuntimeError(
            "Не удалось сгенерить уникальный телефон - увеличь диапазон/соль"
        )

    created_orgs: list[Organization] = []
    for idx, (name, bidx, act_keys, phones_cnt) in enumerate(plan, start=1):
        org = upsert_org(db, name, bi(bidx))
        # activities
        for k in dict.fromkeys(act_keys):
            org.activities.append(ACT[k]) if ACT[k] not in org.activities else None
        # phones
        for j in range(phones_cnt):
            upsert_phone(db, org, make_phone(idx, j))
        created_orgs.append(org)

    db.commit()


if __name__ == "__main__":
    db = SessionLocal()
    try:
        ensure_data(db)
    finally:
        db.close()

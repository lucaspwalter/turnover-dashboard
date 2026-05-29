from datetime import date, timedelta
import random

from app.db.database import Base, SessionLocal, engine
from app.models.employee import Employee
from app.models.employee_event import EmployeeEvent
from app.models.turnover_score import TurnoverScore
from app.services.score_service import recalculate_all


random.seed()

DEPARTMENTS = {
    "Tecnologia": {
        "Desenvolvedor": (6000, 12000),
        "Analista de Dados": (5500, 11000),
        "DevOps": (7500, 14000),
        "QA": (4500, 9000),
    },
    "RH": {
        "Analista de RH": (3500, 7000),
        "Business Partner": (7000, 12000),
        "Recrutador": (4000, 8000),
    },
    "Financeiro": {
        "Analista Financeiro": (4500, 9000),
        "Controller": (9000, 16000),
        "Assistente Financeiro": (2500, 5000),
    },
    "Comercial": {
        "Executivo de Contas": (5000, 12000),
        "SDR": (3000, 6500),
        "Gerente Comercial": (10000, 18000),
    },
    "Operações": {
        "Analista de Operações": (4000, 8000),
        "Coordenador de Operações": (7000, 13000),
        "Supervisor de Atendimento": (4500, 8500),
    },
}

NAMES = [
    "Ana Beatriz Santos",
    "Bruno Oliveira",
    "Carla Mendes",
    "Diego Almeida",
    "Eduarda Costa",
    "Felipe Rodrigues",
    "Gabriela Lima",
    "Henrique Martins",
    "Isabela Ferreira",
    "Joao Pedro Souza",
    "Juliana Rocha",
    "Lucas Barbosa",
    "Mariana Araujo",
    "Nicolas Ribeiro",
    "Patricia Gomes",
    "Rafael Cardoso",
    "Sabrina Teixeira",
    "Thiago Carvalho",
    "Vanessa Moreira",
    "William Nunes",
    "Amanda Freitas",
    "Caio Pereira",
    "Daniela Castro",
    "Erick Fernandes",
    "Fernanda Dias",
    "Gustavo Lopes",
    "Helena Batista",
    "Igor Monteiro",
    "Larissa Campos",
    "Marcelo Vieira",
    "Natália Alves",
    "Otavio Correia",
    "Priscila Martins",
    "Renato Moura",
    "Simone Barros",
    "Vinicius Tavares",
    "Bianca Pires",
    "Cesar Azevedo",
    "Debora Farias",
    "Enzo Machado",
    "Flavia Rezende",
    "Leandro Cunha",
    "Mirela Duarte",
    "Paulo Henrique Melo",
    "Raquel Silveira",
    "Samuel Brito",
    "Tatiane Matos",
    "Vitor Hugo Sales",
    "Yasmin Cavalcante",
    "Andre Luiz Pinto",
]


def random_date(start: date, end: date) -> date:
    days = (end - start).days
    return start + timedelta(days=random.randint(0, days))


def months_ago(months: int) -> date:
    return date.today() - timedelta(days=months * 30)


def salary_for_role(role: str, profile: str) -> float:
    for roles in DEPARTMENTS.values():
        if role in roles:
            minimum, maximum = roles[role]
            break

    if profile == "LOW":
        salary = random.uniform(minimum + (maximum - minimum) * 0.60, maximum)
    elif profile == "MEDIUM":
        salary = random.uniform(minimum + (maximum - minimum) * 0.25, maximum * 0.88)
    else:
        salary = random.uniform(minimum, minimum + (maximum - minimum) * 0.38)

    return round(salary / 100) * 100


def hire_date_for_profile(profile: str) -> date:
    if profile == "LOW":
        return random_date(date(2019, 1, 1), date(2023, 12, 31))
    if profile == "MEDIUM":
        return random_date(date(2021, 1, 1), date(2025, 12, 31))
    return random_date(date(2018, 1, 1), date(2023, 12, 31))


def employee_event_date(employee: Employee, start: date, end: date) -> date:
    start = max(start, employee.hire_date + timedelta(days=30))
    if start > end:
        end = min(date.today(), employee.hire_date + timedelta(days=180))
        return random_date(employee.hire_date + timedelta(days=30), end)
    return random_date(start, end)


def add_event(events: list[EmployeeEvent], employee_id: int, event_type: str, event_date: date):
    events.append(
        EmployeeEvent(
            employee_id=employee_id,
            event_type=event_type,
            event_date=event_date,
            notes=random.choice(
                [
                    "Registro importado pelo seed.",
                    "Evento registrado pelo RH.",
                    "Historico interno do funcionario.",
                    None,
                ]
            ),
        )
    )


def create_events_for_profile(employee: Employee, profile: str) -> list[EmployeeEvent]:
    events = []
    today = date.today()

    if profile == "LOW":
        add_event(
            events,
            employee.id,
            "PROMOTION",
            employee_event_date(employee, months_ago(20), months_ago(4)),
        )
        add_event(
            events,
            employee.id,
            "RAISE",
            employee_event_date(employee, months_ago(10), months_ago(1)),
        )
        for _ in range(random.randint(0, 2)):
            add_event(
                events,
                employee.id,
                "ABSENCE",
                employee_event_date(employee, months_ago(11), today),
            )
        if random.random() < 0.15:
            add_event(
                events,
                employee.id,
                "WARNING",
                employee_event_date(employee, months_ago(24), months_ago(13)),
            )

    elif profile == "MEDIUM":
        if random.random() < 0.55:
            add_event(
                events,
                employee.id,
                "PROMOTION",
                employee_event_date(employee, months_ago(36), months_ago(25)),
            )
        else:
            add_event(
                events,
                employee.id,
                "PROMOTION",
                employee_event_date(employee, months_ago(20), months_ago(6)),
            )

        if random.random() < 0.50:
            add_event(
                events,
                employee.id,
                "RAISE",
                employee_event_date(employee, months_ago(24), months_ago(13)),
            )
        else:
            add_event(
                events,
                employee.id,
                "RAISE",
                employee_event_date(employee, months_ago(10), months_ago(2)),
            )

        absence_count = random.choice([1, 2, 3, 4])
        for _ in range(absence_count):
            add_event(
                events,
                employee.id,
                "ABSENCE",
                employee_event_date(employee, months_ago(11), today),
            )

        if random.random() < 0.45:
            add_event(
                events,
                employee.id,
                "WARNING",
                employee_event_date(employee, months_ago(11), today),
            )

    else:
        if random.random() < 0.35:
            add_event(
                events,
                employee.id,
                "PROMOTION",
                employee_event_date(employee, date(2018, 1, 1), months_ago(25)),
            )

        if random.random() < 0.25:
            add_event(
                events,
                employee.id,
                "RAISE",
                employee_event_date(employee, date(2018, 1, 1), months_ago(13)),
            )

        for _ in range(random.randint(4, 7)):
            add_event(
                events,
                employee.id,
                "ABSENCE",
                employee_event_date(employee, months_ago(11), today),
            )

        for _ in range(random.randint(1, 2)):
            add_event(
                events,
                employee.id,
                "WARNING",
                employee_event_date(employee, months_ago(11), today),
            )

    return events


def clear_database(db):
    db.query(TurnoverScore).delete()
    db.query(EmployeeEvent).delete()
    db.query(Employee).delete()
    db.commit()


def build_employees():
    profiles = ["HIGH"] * 15 + ["MEDIUM"] * 18 + ["LOW"] * 17
    random.shuffle(profiles)

    employee_records = []
    for name, profile in zip(NAMES, profiles):
        department = random.choice(list(DEPARTMENTS.keys()))
        role = random.choice(list(DEPARTMENTS[department].keys()))
        employee = Employee(
            name=name,
            department=department,
            role=role,
            salary=salary_for_role(role, profile),
            hire_date=hire_date_for_profile(profile),
        )
        employee_records.append((employee, profile))

    return employee_records


def main():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        clear_database(db)

        employee_records = build_employees()
        employees = [employee for employee, _profile in employee_records]
        db.add_all(employees)
        db.commit()

        events = []
        for employee, profile in employee_records:
            db.refresh(employee)
            events.extend(create_events_for_profile(employee, profile))

        db.add_all(events)
        db.commit()

        results = recalculate_all(db)
        summary = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
        for result in results:
            summary[result["risk_level"]] += 1

        print("Seed concluido.")
        print(f"Total de funcionarios: {len(employees)}")
        print(f"HIGH: {summary['HIGH']}")
        print(f"MEDIUM: {summary['MEDIUM']}")
        print(f"LOW: {summary['LOW']}")

    finally:
        db.close()


if __name__ == "__main__":
    main()

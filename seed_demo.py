"""
SkillTrack 360°
Synthetic Demo Data Generator

IMPORTANT:
This script creates DEMO/SYNTHETIC data only.
It does not represent real government statistics.

It preserves existing database records.
"""

import random
from datetime import date, timedelta

from werkzeug.security import generate_password_hash

from app import app
from models import db
from models.user import User
from models.trainee import Trainee
from models.outcome import Outcome


# ============================================================
# SETTINGS
# ============================================================

DEMO_TRAINEES = 120

RANDOM_SEED = 360

random.seed(RANDOM_SEED)


# ============================================================
# MASTER DATA
# ============================================================

FIRST_NAMES = [
    "Aarav",
    "Vivaan",
    "Aditya",
    "Arjun",
    "Rohan",
    "Rahul",
    "Karan",
    "Yash",
    "Aman",
    "Sahil",
    "Ankit",
    "Vivek",
    "Neha",
    "Priya",
    "Ananya",
    "Sneha",
    "Kavya",
    "Pooja",
    "Riya",
    "Aditi",
]


LAST_NAMES = [
    "Patil",
    "Shinde",
    "Jadhav",
    "Pawar",
    "Verma",
    "Kulkarni",
    "Deshmukh",
    "Joshi",
    "More",
    "Gaikwad",
    "Chavan",
    "Kadam",
    "Bhosale",
    "Mishra",
    "Yadav",
]


DISTRICTS = [
    "Mumbai",
    "Pune",
    "Nagpur",
    "Nashik",
    "Thane",
    "Aurangabad",
    "Kolhapur",
    "Navi Mumbai",
    "Solapur",
    "Amravati",
]


EDUCATION_LEVELS = [
    "10th",
    "12th",
    "ITI",
    "Diploma",
    "Graduate",
]


# ============================================================
# PROVIDERS
#
# Performance is intentionally different so the dashboard
# can demonstrate comparison and intervention logic.
# ============================================================

PROVIDERS = [

    {
        "name": "Maharashtra Skill Centre",
        "quality": 0.88,
    },

    {
        "name": "TechPath Training Institute",
        "quality": 0.82,
    },

    {
        "name": "Pune Digital Skills Academy",
        "quality": 0.76,
    },

    {
        "name": "Maharashtra Employment Hub",
        "quality": 0.68,
    },

    {
        "name": "SkillBridge Foundation",
        "quality": 0.59,
    },

    {
        "name": "Rural Skills Development Centre",
        "quality": 0.51,
    },

]


# ============================================================
# TRAINING PROGRAMS
#
# Each program has:
# - base employment probability
# - salary range
# - relevance probability
# ============================================================

PROGRAMS = [

    {
        "name": "Full Stack Web Development",
        "employment": 0.82,
        "salary_min": 22000,
        "salary_max": 42000,
        "relevance": 0.86,
    },

    {
        "name": "Data Analytics",
        "employment": 0.78,
        "salary_min": 23000,
        "salary_max": 40000,
        "relevance": 0.83,
    },

    {
        "name": "Cloud Computing",
        "employment": 0.80,
        "salary_min": 25000,
        "salary_max": 45000,
        "relevance": 0.87,
    },

    {
        "name": "Digital Marketing",
        "employment": 0.69,
        "salary_min": 18000,
        "salary_max": 32000,
        "relevance": 0.74,
    },

    {
        "name": "Graphic Design",
        "employment": 0.65,
        "salary_min": 16000,
        "salary_max": 28000,
        "relevance": 0.71,
    },

    {
        "name": "Retail Operations",
        "employment": 0.61,
        "salary_min": 14000,
        "salary_max": 24000,
        "relevance": 0.66,
    },

    {
        "name": "Electrical Technician",
        "employment": 0.64,
        "salary_min": 15000,
        "salary_max": 26000,
        "relevance": 0.70,
    },

    {
        "name": "Basic IT Support",
        "employment": 0.55,
        "salary_min": 13000,
        "salary_max": 22000,
        "relevance": 0.58,
    },

]


# ============================================================
# JOB ROLES
# ============================================================

JOB_ROLES = {

    "Full Stack Web Development": [
        "Junior Software Developer",
        "Web Developer",
        "Frontend Developer",
        "Backend Developer",
    ],

    "Data Analytics": [
        "Junior Data Analyst",
        "Business Analyst Intern",
        "Data Associate",
    ],

    "Cloud Computing": [
        "Cloud Support Associate",
        "Cloud Operations Trainee",
        "Junior Cloud Engineer",
    ],

    "Digital Marketing": [
        "Digital Marketing Executive",
        "SEO Executive",
        "Social Media Executive",
    ],

    "Graphic Design": [
        "Graphic Designer",
        "Junior Visual Designer",
        "Creative Associate",
    ],

    "Retail Operations": [
        "Retail Associate",
        "Store Executive",
        "Operations Assistant",
    ],

    "Electrical Technician": [
        "Electrical Technician",
        "Maintenance Technician",
        "Service Technician",
    ],

    "Basic IT Support": [
        "IT Support Executive",
        "Helpdesk Associate",
        "Technical Support Assistant",
    ],

}


COMPANIES = [
    "TCS",
    "Infosys",
    "Wipro",
    "Tech Mahindra",
    "HCLTech",
    "Capgemini",
    "Local Business",
    "SME Partner",
    "Startup Partner",
]


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def random_name():

    return (
        random.choice(FIRST_NAMES)
        + " "
        + random.choice(LAST_NAMES)
    )


def random_email(index):

    return (
        f"demo_trainee_{index}_"
        f"{random.randint(1000, 9999)}"
        f"@skilltrack.demo"
    )


def random_training_dates():

    completion_date = (
        date.today()
        - timedelta(
            days=random.randint(120, 900)
        )
    )

    start_date = (
        completion_date
        - timedelta(
            days=random.randint(45, 120)
        )
    )

    return start_date, completion_date


def choose_provider():

    return random.choice(PROVIDERS)


def choose_program():

    return random.choice(PROGRAMS)


def choose_employment_status(
    employment_probability
):

    roll = random.random()

    if roll < employment_probability:

        return "Employed"

    elif roll < employment_probability + 0.08:

        return "Self-employed"

    elif roll < employment_probability + 0.18:

        return "Further Education"

    else:

        return "Unemployed"


def choose_relevance(
    relevance_probability,
    employment_status
):

    if employment_status not in [
        "Employed",
        "Self-employed"
    ]:

        return None

    roll = random.random()

    if roll < relevance_probability:

        return "Highly Relevant"

    elif roll < relevance_probability + 0.15:

        return "Partially Relevant"

    else:

        return "Not Relevant"


def calculate_salary(
    program,
    provider_quality
):

    minimum = program["salary_min"]

    maximum = program["salary_max"]

    salary = random.randint(
        minimum,
        maximum
    )

    # Higher-performing providers get a modest
    # salary advantage in the synthetic dataset.

    salary += int(
        (provider_quality - 0.60)
        * 6000
    )

    return max(
        10000,
        salary
    )


def outcome_date(
    completion_date,
    months
):

    return completion_date + timedelta(
        days=30 * months
    )


# ============================================================
# MAIN SEED FUNCTION
# ============================================================

def seed_demo_data():

    print()
    print("=" * 60)
    print("SkillTrack 360° — Synthetic Demo Data Generator")
    print("=" * 60)
    print()

    print(
        "This will ADD synthetic demo records."
    )

    print(
        "Existing records will NOT be deleted."
    )

    print()


    # --------------------------------------------------------
    # Existing demo accounts
    # --------------------------------------------------------

    existing_demo_users = (
        User.query
        .filter(
            User.email.like("demo_trainee_%")
        )
        .count()
    )


    if existing_demo_users > 0:

        print(
            f"Found {existing_demo_users} "
            "existing demo users."
        )

        print(
            "To avoid duplicates, the generator "
            "will stop."
        )

        return


    created_trainees = 0
    created_outcomes = 0


    # --------------------------------------------------------
    # Create trainees
    # --------------------------------------------------------

    for index in range(
        1,
        DEMO_TRAINEES + 1
    ):

        name = random_name()

        email = random_email(index)

        password = "Demo@123"


        # ================================================
        # USER
        # ================================================

        user = User(

            email=email,

            password_hash=
                generate_password_hash(
                    password
                )

        )


        # ------------------------------------------------
        # TRAINING
        # ------------------------------------------------

        provider = choose_provider()

        program = choose_program()

        start_date, completion_date = (
            random_training_dates()
        )


        # ------------------------------------------------
        # TRAINEE
        # ------------------------------------------------

        trainee = Trainee(

            user=user,

            skilltrack_id=
                "ST-MH-DEMO-"
                + f"{index:04d}",

            full_name=name,

            consent_status=True,

            age=random.randint(
                18,
                35
            ),

            gender=random.choice(
                [
                    "Male",
                    "Female",
                    "Other"
                ]
            ),

            district=random.choice(
                DISTRICTS
            ),

            education=random.choice(
                EDUCATION_LEVELS
            ),

            training_program=
                program["name"],

            training_provider=
                provider["name"],

            training_start_date=
                start_date,

            training_completion_date=
                completion_date,

            certificate_status=
                "Certified"

        )


        db.session.add(user)

        db.session.add(trainee)

        db.session.flush()


        created_trainees += 1


        # ------------------------------------------------
        # Provider quality influences outcome.
        # ------------------------------------------------

        provider_quality = (
            provider["quality"]
        )


        # Higher provider quality slightly
        # improves employment probability.

        employment_probability = min(

            0.92,

            program["employment"]
            + (
                provider_quality
                - 0.65
            ) * 0.30

        )


        # ------------------------------------------------
        # 3 / 6 / 12 MONTH OUTCOMES
        # ------------------------------------------------

        for months in [
            3,
            6,
            12
        ]:


            # Not every trainee responds at every stage.

            if months == 3:

                response_probability = 0.92

            elif months == 6:

                response_probability = 0.76

            else:

                response_probability = 0.61


            if random.random() > response_probability:

                continue


            # ------------------------------------------------
            # Employment
            #
            # Later follow-ups slightly improve the chance
            # that an employed trainee remains employed.
            # ------------------------------------------------

            adjusted_probability = (
                employment_probability
            )


            if months == 6:

                adjusted_probability += 0.02

            elif months == 12:

                adjusted_probability += 0.03


            adjusted_probability = min(
                adjusted_probability,
                0.95
            )


            status = choose_employment_status(
                adjusted_probability
            )


            # ------------------------------------------------
            # Salary
            # ------------------------------------------------

            salary = None

            company = None

            job_role = None

            joining_date = None


            if status in [
                "Employed",
                "Self-employed"
            ]:

                salary = calculate_salary(
                    program,
                    provider_quality
                )

                company = random.choice(
                    COMPANIES
                )

                job_role = random.choice(
                    JOB_ROLES[
                        program["name"]
                    ]
                )

                joining_date = (
                    completion_date
                    + timedelta(
                        days=random.randint(
                            7,
                            90
                        )
                    )
                )


            # ------------------------------------------------
            # Relevance
            # ------------------------------------------------

            relevance = choose_relevance(

                program["relevance"]
                + (
                    provider_quality
                    - 0.65
                ) * 0.20,

                status

            )


            # ------------------------------------------------
            # OUTCOME
            # ------------------------------------------------

            outcome = Outcome(

                trainee_id=trainee.id,

                followup_period=
                    f"{months}-Month",

                employment_status=status,

                company_name=company,

                job_role=job_role,

                monthly_salary=salary,

                joining_date=joining_date,

                job_relevance=relevance

            )


            db.session.add(outcome)

            created_outcomes += 1


        # ------------------------------------------------
        # Commit every 25 trainees
        # ------------------------------------------------

        if index % 25 == 0:

            db.session.commit()

            print(
                f"Created {index}/"
                f"{DEMO_TRAINEES} trainees..."
            )


    # ========================================================
    # FINAL COMMIT
    # ========================================================

    db.session.commit()


    print()
    print("=" * 60)

    print(
        "DEMO DATA GENERATION COMPLETE"
    )

    print("=" * 60)

    print()

    print(
        f"Trainees created : "
        f"{created_trainees}"
    )

    print(
        f"Outcomes created : "
        f"{created_outcomes}"
    )

    print()

    print(
        "Demo login password:"
    )

    print(
        "Demo@123"
    )

    print()

    print(
        "Synthetic data only — "
        "not real government statistics."
    )

    print()


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    with app.app_context():

        seed_demo_data()
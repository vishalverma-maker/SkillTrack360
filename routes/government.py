from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask_login import (
    login_required,
    current_user
)
from flask import Blueprint, render_template, request
from flask_login import login_required

from models.trainee import Trainee
from models.outcome import Outcome
from ai.advisor import generate_ai_insights

government_bp = Blueprint(
    "government",
    __name__,
    url_prefix="/government"
)

@government_bp.route("/dashboard")
@login_required
def dashboard():
    if current_user.role != "government":
        flash("Government access is restricted.")
        return redirect(url_for("trainee.dashboard"))
    # =========================================================
    # BASIC DATA
    # =========================================================

    trainees = Trainee.query.all()

    outcomes = (
        Outcome.query
        .order_by(Outcome.created_at.desc())
        .all()
    )

    total_trainees = len(trainees)
    total_outcomes = len(outcomes)


    # =========================================================
    # EMPLOYMENT OUTCOMES
    # =========================================================

    employed = 0
    self_employed = 0
    unemployed = 0
    further_education = 0

    for outcome in outcomes:

        status = (
            outcome.employment_status or ""
        ).strip().lower()

        if status == "employed":
            employed += 1

        elif status in [
            "self-employed",
            "self employed"
        ]:
            self_employed += 1

        elif status == "unemployed":
            unemployed += 1

        elif status in [
            "further education",
            "further_education"
        ]:
            further_education += 1


    # =========================================================
    # EMPLOYMENT RATE
    # =========================================================

    if total_outcomes > 0:

        employment_rate = round(
            (
                (employed + self_employed)
                / total_outcomes
            ) * 100,
            1
        )

    else:

        employment_rate = 0


    # =========================================================
    # SALARY
    # =========================================================

    salaries = [
        outcome.monthly_salary
        for outcome in outcomes
        if outcome.monthly_salary is not None
        and outcome.monthly_salary > 0
    ]

    if salaries:

        average_salary = round(
            sum(salaries) / len(salaries)
        )

    else:

        average_salary = 0


    # =========================================================
    # JOB RELEVANCE
    # =========================================================

    highly_relevant = 0
    partially_relevant = 0
    not_relevant = 0

    for outcome in outcomes:

        relevance = (
            outcome.job_relevance or ""
        ).strip().lower()

        if relevance == "highly relevant":
            highly_relevant += 1

        elif relevance == "partially relevant":
            partially_relevant += 1

        elif relevance == "not relevant":
            not_relevant += 1


    # =========================================================
    # FOLLOW-UP COUNTS
    # =========================================================

    three_month = 0
    six_month = 0
    twelve_month = 0

    for outcome in outcomes:

        period = (
            outcome.followup_period or ""
        ).strip().lower()

        if period in [
            "3-month",
            "3 months",
            "3 month"
        ]:
            three_month += 1

        elif period in [
            "6-month",
            "6 months",
            "6 month"
        ]:
            six_month += 1

        elif period in [
            "12-month",
            "12 months",
            "12 month"
        ]:
            twelve_month += 1


    # =========================================================
    # FOLLOW-UP COVERAGE
    # =========================================================

    if total_trainees > 0:

        three_month_coverage = round(
            (three_month / total_trainees) * 100,
            1
        )

        six_month_coverage = round(
            (six_month / total_trainees) * 100,
            1
        )

        twelve_month_coverage = round(
            (twelve_month / total_trainees) * 100,
            1
        )

    else:

        three_month_coverage = 0
        six_month_coverage = 0
        twelve_month_coverage = 0


    # =========================================================
    # TRAINEE LOOKUP
    #
    # Connects Outcome records with trainee information.
    # =========================================================

    trainee_lookup = {
        trainee.id: trainee
        for trainee in trainees
    }


    # =========================================================
    # PROVIDER ANALYTICS
    # =========================================================

    provider_data = {}

    for trainee in trainees:

        provider = (
            trainee.training_provider
            or "Unknown Provider"
        ).strip()

        if provider not in provider_data:

            provider_data[provider] = {

                "provider": provider,
                "trainees": 0,
                "outcomes": 0,

                "employed": 0,
                "self_employed": 0,
                "unemployed": 0,

                "salaries": [],

                "highly_relevant": 0,
                "partially_relevant": 0,
                "not_relevant": 0
            }

        provider_data[provider]["trainees"] += 1


    # Add outcome information

    for outcome in outcomes:

        trainee = trainee_lookup.get(
            outcome.trainee_id
        )

        if trainee is None:
            continue

        provider = (
            trainee.training_provider
            or "Unknown Provider"
        ).strip()

        stats = provider_data[provider]

        stats["outcomes"] += 1


        # Employment

        status = (
            outcome.employment_status or ""
        ).strip().lower()

        if status == "employed":

            stats["employed"] += 1

        elif status in [
            "self-employed",
            "self employed"
        ]:

            stats["self_employed"] += 1

        elif status == "unemployed":

            stats["unemployed"] += 1


        # Salary

        if (
            outcome.monthly_salary is not None
            and outcome.monthly_salary > 0
        ):

            stats["salaries"].append(
                outcome.monthly_salary
            )


        # Relevance

        relevance = (
            outcome.job_relevance or ""
        ).strip().lower()

        if relevance == "highly relevant":

            stats["highly_relevant"] += 1

        elif relevance == "partially relevant":

            stats["partially_relevant"] += 1

        elif relevance == "not relevant":

            stats["not_relevant"] += 1


    # =========================================================
    # FORMAT PROVIDER ANALYTICS
    # =========================================================

    provider_stats = []

    for provider, stats in provider_data.items():

        outcome_count = stats["outcomes"]

        if outcome_count > 0:

            provider_employment_rate = round(
                (
                    (
                        stats["employed"]
                        + stats["self_employed"]
                    )
                    / outcome_count
                ) * 100,
                1
            )

            provider_relevance_rate = round(
                (
                    stats["highly_relevant"]
                    / outcome_count
                ) * 100,
                1
            )

        else:

            provider_employment_rate = 0
            provider_relevance_rate = 0


        if stats["salaries"]:

            provider_average_salary = round(
                sum(stats["salaries"])
                / len(stats["salaries"])
            )

        else:

            provider_average_salary = 0


        # -----------------------------------------------------
        # PERFORMANCE SCORE
        #
        # 60% employment
        # 25% relevance
        # 15% salary index
        # -----------------------------------------------------

        salary_score = min(
            (provider_average_salary / 50000) * 100,
            100
        )

        performance_score = round(
            (
                provider_employment_rate * 0.60
                + provider_relevance_rate * 0.25
                + salary_score * 0.15
            ),
            1
        )


        provider_stats.append({

            "provider": provider,

            "trainees": stats["trainees"],

            "outcomes": stats["outcomes"],

            "employed": stats["employed"],

            "self_employed": stats["self_employed"],

            "unemployed": stats["unemployed"],

            "employment_rate":
                provider_employment_rate,

            "average_salary":
                provider_average_salary,

            "relevance_rate":
                provider_relevance_rate,

            "highly_relevant":
                stats["highly_relevant"],

            "partially_relevant":
                stats["partially_relevant"],

            "not_relevant":
                stats["not_relevant"],

            "performance_score":
                performance_score
        })


    # Best providers first

    provider_stats.sort(
        key=lambda x: x["performance_score"],
        reverse=True
    )


    # =========================================================
    # TRAINING PROGRAM ANALYTICS
    # =========================================================

    program_data = {}

    for trainee in trainees:

        program = (
            trainee.training_program
            or "Unknown Program"
        ).strip()

        if program not in program_data:

            program_data[program] = {

                "program": program,

                "trainees": 0,

                "outcomes": 0,

                "employed": 0,

                "self_employed": 0,

                "unemployed": 0,

                "salaries": [],

                "highly_relevant": 0,

                "partially_relevant": 0,

                "not_relevant": 0
            }

        program_data[program]["trainees"] += 1


    # Add outcome information

    for outcome in outcomes:

        trainee = trainee_lookup.get(
            outcome.trainee_id
        )

        if trainee is None:
            continue

        program = (
            trainee.training_program
            or "Unknown Program"
        ).strip()

        stats = program_data[program]

        stats["outcomes"] += 1


        # Employment

        status = (
            outcome.employment_status or ""
        ).strip().lower()

        if status == "employed":

            stats["employed"] += 1

        elif status in [
            "self-employed",
            "self employed"
        ]:

            stats["self_employed"] += 1

        elif status == "unemployed":

            stats["unemployed"] += 1


        # Salary

        if (
            outcome.monthly_salary is not None
            and outcome.monthly_salary > 0
        ):

            stats["salaries"].append(
                outcome.monthly_salary
            )


        # Relevance

        relevance = (
            outcome.job_relevance or ""
        ).strip().lower()

        if relevance == "highly relevant":

            stats["highly_relevant"] += 1

        elif relevance == "partially relevant":

            stats["partially_relevant"] += 1

        elif relevance == "not relevant":

            stats["not_relevant"] += 1


    # =========================================================
    # FORMAT PROGRAM ANALYTICS
    # =========================================================

    program_stats = []

    for program, stats in program_data.items():

        outcome_count = stats["outcomes"]

        if outcome_count > 0:

            program_employment_rate = round(
                (
                    (
                        stats["employed"]
                        + stats["self_employed"]
                    )
                    / outcome_count
                ) * 100,
                1
            )

            program_relevance_rate = round(
                (
                    stats["highly_relevant"]
                    / outcome_count
                ) * 100,
                1
            )

        else:

            program_employment_rate = 0
            program_relevance_rate = 0


        if stats["salaries"]:

            program_average_salary = round(
                sum(stats["salaries"])
                / len(stats["salaries"])
            )

        else:

            program_average_salary = 0


        salary_score = min(
            (program_average_salary / 50000) * 100,
            100
        )


        program_performance_score = round(
            (
                program_employment_rate * 0.60
                + program_relevance_rate * 0.25
                + salary_score * 0.15
            ),
            1
        )


        program_stats.append({

            "program": program,

            "trainees": stats["trainees"],

            "outcomes": stats["outcomes"],

            "employed": stats["employed"],

            "self_employed": stats["self_employed"],

            "unemployed": stats["unemployed"],

            "employment_rate":
                program_employment_rate,

            "average_salary":
                program_average_salary,

            "relevance_rate":
                program_relevance_rate,

            "highly_relevant":
                stats["highly_relevant"],

            "partially_relevant":
                stats["partially_relevant"],

            "not_relevant":
                stats["not_relevant"],

            "performance_score":
                program_performance_score
        })


    # Best programs first

    program_stats.sort(
        key=lambda x: x["performance_score"],
        reverse=True
    )


    # =========================================================
    # =========================================================
    # DISTRICT ANALYTICS
    # =========================================================
    district_data = {}

    for trainee in trainees:
        district = (trainee.district or "Unknown District").strip()
        if district not in district_data:
            district_data[district] = {"district": district, "trainees": 0, "outcomes": 0, "employed": 0, "self_employed": 0, "unemployed": 0, "salaries": [], "highly_relevant": 0, "partially_relevant": 0, "not_relevant": 0}
        district_data[district]["trainees"] += 1

    for outcome in outcomes:
        trainee = trainee_lookup.get(outcome.trainee_id)
        if trainee is None:
            continue
        district = (trainee.district or "Unknown District").strip()
        stats = district_data[district]
        stats["outcomes"] += 1
        status = (outcome.employment_status or "").strip().lower()
        if status == "employed":
            stats["employed"] += 1
        elif status in ["self-employed", "self employed"]:
            stats["self_employed"] += 1
        elif status == "unemployed":
            stats["unemployed"] += 1
        if outcome.monthly_salary is not None and outcome.monthly_salary > 0:
            stats["salaries"].append(outcome.monthly_salary)
        relevance = (outcome.job_relevance or "").strip().lower()
        if relevance == "highly relevant":
            stats["highly_relevant"] += 1
        elif relevance == "partially relevant":
            stats["partially_relevant"] += 1
        elif relevance == "not relevant":
            stats["not_relevant"] += 1

    district_stats = []
    for district, stats in district_data.items():
        outcome_count = stats["outcomes"]
        if outcome_count > 0:
            district_employment_rate = round(((stats["employed"] + stats["self_employed"]) / outcome_count) * 100, 1)
            district_relevance_rate = round((stats["highly_relevant"] / outcome_count) * 100, 1)
        else:
            district_employment_rate = 0
            district_relevance_rate = 0
        district_average_salary = round(sum(stats["salaries"]) / len(stats["salaries"])) if stats["salaries"] else 0
        salary_score = min((district_average_salary / 50000) * 100, 100)
        district_performance_score = round(district_employment_rate * 0.60 + district_relevance_rate * 0.25 + salary_score * 0.15, 1)
        if outcome_count == 0:
            district_priority = "DATA NEEDED"
            district_action = "Collect outcome data"
        elif district_performance_score >= 75:
            district_priority = "LOW"
            district_action = "Maintain and scale effective programs"
        elif district_performance_score >= 55:
            district_priority = "MEDIUM"
            district_action = "Improve employer alignment"
        else:
            district_priority = "HIGH"
            district_action = "Priority intervention recommended"
        district_stats.append({"district": district, "trainees": stats["trainees"], "outcomes": stats["outcomes"], "employed": stats["employed"], "self_employed": stats["self_employed"], "unemployed": stats["unemployed"], "employment_rate": district_employment_rate, "average_salary": district_average_salary, "relevance_rate": district_relevance_rate, "highly_relevant": stats["highly_relevant"], "partially_relevant": stats["partially_relevant"], "not_relevant": stats["not_relevant"], "performance_score": district_performance_score, "priority": district_priority, "action": district_action})

    district_stats.sort(key=lambda x: x["performance_score"], reverse=True)

    # SKILL GAP INTELLIGENCE
    #
    # These are SYNTHETIC DEMO labour-market indicators.
    #
    # In a production system, demand would come from:
    # job postings / employer surveys / labour-market datasets.
    #
    # supply represents the current training capacity indicator.
    # =========================================================

    skill_gap_data = [

        {
            "skill": "Cloud Computing",
            "demand": 92,
            "supply": 41
        },

        {
            "skill": "Data Analytics",
            "demand": 92,
            "supply": 42
        },

        {
            "skill": "Full Stack Web Development",
            "demand": 87,
            "supply": 68
        },

        {
            "skill": "Electrical Technician",
            "demand": 81,
            "supply": 79
        },

        {
            "skill": "Digital Marketing",
            "demand": 74,
            "supply": 61
        },

        {
            "skill": "Graphic Design",
            "demand": 68,
            "supply": 72
        },

        {
            "skill": "Basic IT Support",
            "demand": 65,
            "supply": 78
        },

        {
            "skill": "Retail Operations",
            "demand": 60,
            "supply": 85
        }
    ]


    # =========================================================
    # CALCULATE GAP + GOVERNMENT ACTION
    # =========================================================

    for skill in skill_gap_data:

        skill["gap"] = round(
            skill["demand"] - skill["supply"],
            1
        )

        gap = skill["gap"]


        if gap >= 20:

            skill["status"] = "High Gap"

            skill["priority"] = "HIGH"

            skill["action"] = (
                "Increase training capacity"
            )


        elif gap >= 8:

            skill["status"] = "Moderate Gap"

            skill["priority"] = "MEDIUM"

            skill["action"] = (
                "Expand targeted training"
            )


        elif gap >= -8:

            skill["status"] = "Balanced"

            skill["priority"] = "LOW"

            skill["action"] = (
                "Maintain current capacity"
            )


        else:

            skill["status"] = "Oversupply"

            skill["priority"] = "REVIEW"

            skill["action"] = (
                "Review training capacity"
            )


    # Highest priority gaps first

    skill_gap_data.sort(
        key=lambda x: x["gap"],
        reverse=True
    )


    # =========================================================
    # DASHBOARD
    # =========================================================
    ai_insights = generate_ai_insights()
    
    return render_template(

        "government/dashboard.html",

        # Basic KPIs

        total_trainees=total_trainees,

        total_outcomes=total_outcomes,

        employed=employed,

        self_employed=self_employed,

        unemployed=unemployed,

        further_education=further_education,

        employment_rate=employment_rate,

        average_salary=average_salary,
        ai_insights=ai_insights,

        # Relevance

        highly_relevant=highly_relevant,

        partially_relevant=partially_relevant,

        not_relevant=not_relevant,


        # Follow-up

        three_month=three_month,

        six_month=six_month,

        twelve_month=twelve_month,

        three_month_coverage=
            three_month_coverage,

        six_month_coverage=
            six_month_coverage,

        twelve_month_coverage=
            twelve_month_coverage,


        # Raw outcomes

        outcomes=outcomes,


        # Provider intelligence

        provider_stats=provider_stats,


        # Program intelligence

        program_stats=program_stats,


        # Skill Gap Intelligence

        skill_gap_data=skill_gap_data,

        # District intelligence
        district_stats=district_stats

    )
    # =========================================================
# GOVERNMENT TRAINEE OUTCOME LOOKUP
# =========================================================

@government_bp.route("/lookup")
@login_required
def trainee_lookup_page():

    skilltrack_id = request.args.get(
        "skilltrack_id",
        ""
    ).strip()

    trainee = None
    outcomes = []

    # ---------------------------------------------------------
    # SEARCH TRAINEE
    # ---------------------------------------------------------

    if skilltrack_id:

        trainee = Trainee.query.filter_by(
            skilltrack_id=skilltrack_id
        ).first()

        if trainee:

            outcomes = (
                Outcome.query
                .filter_by(trainee_id=trainee.id)
                .all()
            )

            # Display follow-ups in logical order
            followup_order = {
                "3-month": 1,
                "3 months": 1,
                "3 month": 1,
                "6-month": 2,
                "6 months": 2,
                "6 month": 2,
                "12-month": 3,
                "12 months": 3,
                "12 month": 3
            }

            outcomes.sort(
                key=lambda outcome:
                followup_order.get(
                    (outcome.followup_period or "").lower(),
                    99
                )
            )

    return render_template(
        "government/trainee_lookup.html",
        trainee=trainee,
        outcomes=outcomes,
        skilltrack_id=skilltrack_id
    )
from models import db
from models.trainee import Trainee
from models.outcome import Outcome


def generate_ai_insights():
    """
    SkillTrack AI Policy Advisor

    Uses existing SkillTrack outcome data to generate
    transparent, explainable policy recommendations.

    This is a rule-based AI/analytics engine for the MVP.
    It can later be replaced or enhanced with ML/LLM models.
    """

    trainees = Trainee.query.all()
    outcomes = Outcome.query.all()

    insights = []

    # ---------------------------------------------------------
    # 1. BASIC DATA CHECK
    # ---------------------------------------------------------

    if not trainees:
        return [{
            "type": "info",
            "title": "Insufficient Data",
            "message": (
                "No trainee records are available yet. "
                "Collect trainee and training information "
                "before generating policy insights."
            ),
            "action": "Collect trainee data"
        }]

    if not outcomes:
        return [{
            "type": "info",
            "title": "Outcome Data Needed",
            "message": (
                "Trainees are registered, but no employment "
                "outcomes have been recorded yet."
            ),
            "action": "Begin 3-month outcome tracking"
        }]

    # ---------------------------------------------------------
    # 2. EMPLOYMENT ANALYSIS
    # ---------------------------------------------------------

    employed = 0
    unemployed = 0
    self_employed = 0

    for outcome in outcomes:

        status = (outcome.employment_status or "").lower()

        if status == "employed":
            employed += 1

        elif status == "self-employed":
            self_employed += 1

        elif status == "unemployed":
            unemployed += 1

    employment_count = employed + self_employed

    employment_rate = (
        employment_count / len(outcomes) * 100
        if outcomes else 0
    )

    # ---------------------------------------------------------
    # 3. EMPLOYMENT INSIGHT
    # ---------------------------------------------------------

    if employment_rate >= 70:

        insights.append({
            "type": "success",
            "title": "Strong Employment Outcomes",
            "message": (
                f"Recorded employment outcomes are strong at "
                f"{employment_rate:.1f}%."
            ),
            "action": (
                "Identify high-performing programs and "
                "consider scaling them."
            )
        })

    elif employment_rate >= 50:

        insights.append({
            "type": "warning",
            "title": "Moderate Employment Outcomes",
            "message": (
                f"Recorded employment rate is "
                f"{employment_rate:.1f}%, indicating room "
                f"for improvement."
            ),
            "action": (
                "Review employer alignment and strengthen "
                "job-placement support."
            )
        })

    else:

        insights.append({
            "type": "danger",
            "title": "Low Employment Outcomes",
            "message": (
                f"Recorded employment rate is only "
                f"{employment_rate:.1f}%."
            ),
            "action": (
                "Prioritize program review, employer "
                "partnerships and targeted interventions."
            )
        })

    # ---------------------------------------------------------
    # 4. UNEMPLOYMENT ALERT
    # ---------------------------------------------------------

    unemployment_rate = (
        unemployed / len(outcomes) * 100
        if outcomes else 0
    )

    if unemployment_rate >= 30:

        insights.append({
            "type": "danger",
            "title": "High Unemployment Signal",
            "message": (
                f"{unemployment_rate:.1f}% of recorded outcomes "
                "are currently marked unemployed."
            ),
            "action": (
                "Investigate affected programs and districts "
                "and strengthen placement support."
            )
        })

    # ---------------------------------------------------------
    # 5. JOB RELEVANCE ANALYSIS
    # ---------------------------------------------------------

    relevance_values = []

    for outcome in outcomes:

        relevance = (
            outcome.job_relevance or ""
        ).lower()

        if relevance == "highly relevant":
            relevance_values.append(100)

        elif relevance == "relevant":
            relevance_values.append(70)

        elif relevance == "partially relevant":
            relevance_values.append(40)

        elif relevance == "not relevant":
            relevance_values.append(0)

    if relevance_values:

        relevance_rate = (
            sum(relevance_values) /
            len(relevance_values)
        )

        if relevance_rate < 50:

            insights.append({
                "type": "warning",
                "title": "Training–Job Alignment Risk",
                "message": (
                    f"Average training-to-job alignment is "
                    f"{relevance_rate:.1f}%."
                ),
                "action": (
                    "Review curriculum relevance and employer "
                    "skill requirements."
                )
            })

        elif relevance_rate >= 75:

            insights.append({
                "type": "success",
                "title": "Strong Training Alignment",
                "message": (
                    f"Training-to-job alignment is strong at "
                    f"{relevance_rate:.1f}%."
                ),
                "action": (
                    "Identify successful curricula that can "
                    "be replicated across programs."
                )
            })

    # ---------------------------------------------------------
    # 6. SALARY ANALYSIS
    # ---------------------------------------------------------

    salaries = [
        outcome.monthly_salary
        for outcome in outcomes
        if outcome.monthly_salary
        and outcome.monthly_salary > 0
    ]

    if salaries:

        average_salary = sum(salaries) / len(salaries)

        if average_salary < 15000:

            insights.append({
                "type": "warning",
                "title": "Low Salary Signal",
                "message": (
                    f"Average recorded monthly salary is "
                    f"₹{average_salary:,.0f}."
                ),
                "action": (
                    "Evaluate whether training is leading to "
                    "higher-value employment opportunities."
                )
            })

        elif average_salary >= 25000:

            insights.append({
                "type": "success",
                "title": "Strong Salary Outcomes",
                "message": (
                    f"Average recorded monthly salary is "
                    f"₹{average_salary:,.0f}."
                ),
                "action": (
                    "Identify programs producing higher-value "
                    "employment outcomes."
                )
            })

    # ---------------------------------------------------------
    # 7. FOLLOW-UP COVERAGE
    # ---------------------------------------------------------

    followup_3 = sum(
        1 for o in outcomes
        if (o.followup_period or "").lower() == "3-month"
    )

    followup_6 = sum(
        1 for o in outcomes
        if (o.followup_period or "").lower() == "6-month"
    )

    followup_12 = sum(
        1 for o in outcomes
        if (o.followup_period or "").lower() == "12-month"
    )

    # Missing later follow-ups can indicate tracking gaps.

    if followup_3 > 0 and followup_6 == 0:

        insights.append({
            "type": "info",
            "title": "Longitudinal Tracking Gap",
            "message": (
                "3-month outcomes are available, but "
                "6-month outcomes are not yet recorded."
            ),
            "action": (
                "Prioritize the next follow-up cycle to "
                "measure employment retention."
            )
        })

    elif followup_6 > 0 and followup_12 == 0:

        insights.append({
            "type": "info",
            "title": "12-Month Follow-up Pending",
            "message": (
                "6-month outcomes are available, but "
                "12-month outcomes are not yet recorded."
            ),
            "action": (
                "Continue longitudinal tracking to measure "
                "long-term career outcomes."
            )
        })

    # ---------------------------------------------------------
    # 8. DISTRICT RISK DETECTION
    # ---------------------------------------------------------

    district_data = {}

    for outcome in outcomes:

        trainee = db.session.get(
            Trainee,
            outcome.trainee_id
        )

        if not trainee:
            continue

        district = (
            trainee.district
            or "Unknown District"
        )

        if district not in district_data:

            district_data[district] = {
                "total": 0,
                "employed": 0
            }

        district_data[district]["total"] += 1

        status = (
            outcome.employment_status
            or ""
        ).lower()

        if status in ["employed", "self-employed"]:
            district_data[district]["employed"] += 1

    for district, data in district_data.items():

        if data["total"] < 3:
            continue

        rate = (
            data["employed"] /
            data["total"] *
            100
        )

        if rate < 50:

            insights.append({
                "type": "danger",
                "title": f"District Risk — {district}",
                "message": (
                    f"Employment outcome rate in {district} "
                    f"is {rate:.1f}%."
                ),
                "action": (
                    "Review local training programs and "
                    "strengthen employer connections."
                )
            })

    # ---------------------------------------------------------
    # 9. PROVIDER PERFORMANCE SIGNAL
    # ---------------------------------------------------------

    provider_data = {}

    for outcome in outcomes:

        trainee = db.session.get(
            Trainee,
            outcome.trainee_id
        )

        if not trainee:
            continue

        provider = (
            trainee.training_provider
            or "Unknown Provider"
        )

        if provider not in provider_data:

            provider_data[provider] = {
                "total": 0,
                "employed": 0
            }

        provider_data[provider]["total"] += 1

        status = (
            outcome.employment_status
            or ""
        ).lower()

        if status in ["employed", "self-employed"]:
            provider_data[provider]["employed"] += 1

    for provider, data in provider_data.items():

        if data["total"] < 3:
            continue

        rate = (
            data["employed"] /
            data["total"] *
            100
        )

        if rate < 40:

            insights.append({
                "type": "warning",
                "title": f"Provider Review — {provider}",
                "message": (
                    f"Recorded employment rate is "
                    f"{rate:.1f}%."
                ),
                "action": (
                    "Review provider performance, curriculum "
                    "alignment and placement support."
                )
            })
        # ---------------------------------------------------------
    # 10. PRIORITY INTERVENTION
    # ---------------------------------------------------------

    priority_insight = None

    for insight in insights:

        if insight["type"] == "danger":
            priority_insight = insight
            break

    if priority_insight is None:

        for insight in insights:

            if insight["type"] == "warning":
                priority_insight = insight
                break

    if priority_insight:

        insights.append({
            "type": "danger",
            "title": "Priority Intervention",
            "message": (
                f"The AI has identified a priority area: "
                f"{priority_insight['title']}."
            ),
            "action": (
                priority_insight["action"]
            )
        })

    else:

        insights.append({
            "type": "success",
            "title": "No Immediate High-Risk Signal",
            "message": (
                "Current recorded outcome data does not show "
                "a major high-risk signal requiring immediate intervention."
            ),
            "action": (
                "Continue longitudinal tracking and scale programs "
                "that demonstrate strong employment outcomes."
            )
        })


    # ---------------------------------------------------------
    # 11. FINAL AI SUMMARY
    # ---------------------------------------------------------
    
    insights.append({
        "type": "info",
        "title": "AI Policy Summary",
        "message": (
            "SkillTrack AI combines employment, salary, "
            "job relevance, follow-up, district and provider "
            "signals to identify areas requiring attention."
        ),
        "action": (
            "Use these signals to prioritize evidence-based "
            "training and employment interventions."
        )
    })

    return insights
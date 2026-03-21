HIGH_RISK_COUNTRIES = [
    'Iran', 'North Korea', 'Syria', 'Yemen',
    'Libya', 'Sudan', 'Somalia', 'Myanmar'
]

MEDIUM_RISK_COUNTRIES = [
    'Russia', 'Pakistan', 'Nigeria', 'Kenya',
    'Vietnam', 'Philippines', 'Egypt', 'Turkey'
]

def calculate_risk_score(nationality, is_pep, age, documents_submitted):
    score = 0
    breakdown = []

    if nationality in HIGH_RISK_COUNTRIES:
        score += 40
        breakdown.append(f'High-risk nationality ({nationality}): +40')
    elif nationality in MEDIUM_RISK_COUNTRIES:
        score += 20
        breakdown.append(f'Medium-risk nationality ({nationality}): +20')
    else:
        breakdown.append(f'Standard nationality ({nationality}): +0')

    if is_pep:
        score += 30
        breakdown.append('Politically Exposed Person (PEP): +30')

    if age < 25:
        score += 10
        breakdown.append(f'Young customer (age {age}): +10')
    elif age > 70:
        score += 10
        breakdown.append(f'Elderly customer (age {age}): +10')

    if documents_submitted >= 2:
        score -= 10
        breakdown.append(f'{documents_submitted} documents submitted: -10')
    elif documents_submitted == 0:
        score += 20
        breakdown.append('No documents submitted: +20')

    return score, breakdown


def get_risk_level(score):
    if score <= 30:
        return 'low'
    elif score <= 60:
        return 'medium'
    else:
        return 'high'


def assess_customer(nationality, is_pep, age, documents_submitted):
    score, breakdown = calculate_risk_score(
        nationality, is_pep, age, documents_submitted
    )
    risk_level = get_risk_level(score)

    return {
        'score': score,
        'risk_level': risk_level,
        'breakdown': breakdown
    }
"""
Database Seed and Machine Learning Initialization Script for CrimeGuard AI.
Populates standard categories, districts, historical incidents, safety alerts,
trains the ML classifier, and configures the default administrator.
"""

import os
import sys
import random
from datetime import datetime, timedelta

# Initialize Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crime_analysis.settings')
import django
django.setup()

from django.contrib.auth.models import User
from django.utils import timezone
from application.models import CrimeCategory, District, CrimeReport, SafetyAlert, PredictionLog
from application.ml_engine import train_and_save_model


def seed_database():
    print("[1/6] Seeding Crime Categories...")
    categories_data = [
        {'name': 'Theft', 'code': 'CAT-01', 'default_severity': 'Low', 'icon': 'fa-mask', 'description': 'Petty theft, pickpocketing, bag snatching without weapons.'},
        {'name': 'Burglary', 'code': 'CAT-02', 'default_severity': 'Medium', 'icon': 'fa-house-chimney-crack', 'description': 'Unlawful entry into residential or commercial premises to commit felony.'},
        {'name': 'Robbery', 'code': 'CAT-03', 'default_severity': 'High', 'icon': 'fa-hand-holding-dollar', 'description': 'Taking property by force, intimidation, or weapon brandishing.'},
        {'name': 'Assault', 'code': 'CAT-04', 'default_severity': 'High', 'icon': 'fa-hand-fist', 'description': 'Physical attack or grievous injury inflicted on individuals.'},
        {'name': 'Cybercrime', 'code': 'CAT-05', 'default_severity': 'Medium', 'icon': 'fa-laptop-code', 'description': 'Phishing, unauthorized fund transfers, identity spoofing, and extortion.'},
        {'name': 'Fraud', 'code': 'CAT-06', 'default_severity': 'Medium', 'icon': 'fa-file-invoice-dollar', 'description': 'Commercial deception, counterfeit instruments, financial cheating.'},
        {'name': 'Vandalism', 'code': 'CAT-07', 'default_severity': 'Low', 'icon': 'fa-spray-can', 'description': 'Willful destruction of municipal or public utility property.'},
        {'name': 'Vehicle Theft', 'code': 'CAT-08', 'default_severity': 'Medium', 'icon': 'fa-motorcycle', 'description': 'Stolen two-wheelers, four-wheelers, and vehicle part trafficking.'},
        {'name': 'Drug Offense', 'code': 'CAT-09', 'default_severity': 'Critical', 'icon': 'fa-pills', 'description': 'Narcotic peddling, contraband possession, illicit synthetic substances.'},
    ]

    category_objs = {}
    for data in categories_data:
        cat, _ = CrimeCategory.objects.get_or_create(
            name=data['name'],
            defaults=data
        )
        category_objs[data['name']] = cat

    print(f" -> {len(category_objs)} categories initialized.")

    print("\n[2/6] Seeding Districts and Police Precincts...")
    districts_data = [
        {
            'name': 'Downtown Central', 'code': 'DST-01', 'city': 'Metropolis',
            'latitude': 12.9716, 'longitude': 77.5946, 'population_density': 'Dense Urban',
            'police_station': 'Central Division Police Station', 'helpline_number': '+91 80 2294 2111',
            'current_risk_level': 'High'
        },
        {
            'name': 'North Industrial Zone', 'code': 'DST-02', 'city': 'Metropolis',
            'latitude': 13.0358, 'longitude': 77.5970, 'population_density': 'Medium',
            'police_station': 'Peenya Industrial Precinct', 'helpline_number': '+91 80 2294 2222',
            'current_risk_level': 'Critical'
        },
        {
            'name': 'Tech Corridor', 'code': 'DST-03', 'city': 'Metropolis',
            'latitude': 12.9279, 'longitude': 77.6271, 'population_density': 'High',
            'police_station': 'Electronic City Cyber Precinct', 'helpline_number': '+91 80 2294 2333',
            'current_risk_level': 'Medium'
        },
        {
            'name': 'West End Suburbs', 'code': 'DST-04', 'city': 'Metropolis',
            'latitude': 12.9815, 'longitude': 77.5255, 'population_density': 'Medium',
            'police_station': 'Rajajinagar Sub-divisional Station', 'helpline_number': '+91 80 2294 2444',
            'current_risk_level': 'Low'
        },
        {
            'name': 'Riverfront Port', 'code': 'DST-05', 'city': 'Metropolis',
            'latitude': 12.9150, 'longitude': 77.5850, 'population_density': 'High',
            'police_station': 'Docklands & Riverfront Station', 'helpline_number': '+91 80 2294 2555',
            'current_risk_level': 'High'
        },
        {
            'name': 'Metro Transit Hub', 'code': 'DST-06', 'city': 'Metropolis',
            'latitude': 12.9778, 'longitude': 77.5726, 'population_density': 'Dense Urban',
            'police_station': 'Majestic Railway & Transit Police', 'helpline_number': '+91 80 2294 2666',
            'current_risk_level': 'Critical'
        },
        {
            'name': 'University District', 'code': 'DST-07', 'city': 'Metropolis',
            'latitude': 12.9600, 'longitude': 77.5300, 'population_density': 'Medium',
            'police_station': 'Jnanabharati Campus Precinct', 'helpline_number': '+91 80 2294 2777',
            'current_risk_level': 'Low'
        },
        {
            'name': 'South Commercial Plaza', 'code': 'DST-08', 'city': 'Metropolis',
            'latitude': 12.9352, 'longitude': 77.6245, 'population_density': 'High',
            'police_station': 'Koramangala Commercial Division', 'helpline_number': '+91 80 2294 2888',
            'current_risk_level': 'Medium'
        },
    ]

    district_objs = {}
    for d_data in districts_data:
        dist, _ = District.objects.get_or_create(
            code=d_data['code'],
            defaults=d_data
        )
        district_objs[d_data['name']] = dist

    print(f" -> {len(district_objs)} districts initialized.")

    print("\n[3/6] Seeding Historical Crime Incident Reports...")
    sample_incidents = [
        ("Bag snatching near platform 2 exit", "Theft", "Metro Transit Hub", "Low", "Solved", False, "Platform 2 Escalator Junction", "Two individuals on a black pulsar without number plate.", "Insp. S. Rao"),
        ("Midnight electronics showroom break-in", "Burglary", "Downtown Central", "High", "Under Investigation", False, "Brigade Road, 4th Cross", "Cut glass pane and disabled security sensor.", "Sub-Insp. M. Patel"),
        ("Armed robbery at 24/7 ATM kiosk", "Robbery", "North Industrial Zone", "Critical", "Patrol Dispatched", True, "Phase 2 Ring Road ATM", "Two males brandishing short firearms, wearing helmets.", "Insp. V. Kumar"),
        ("Physical altercation outside pub complex", "Assault", "South Commercial Plaza", "High", "Solved", True, "80 Feet Road Pub Hub", "Crowd brawl following disagreement; victim admitted to hospital.", "Insp. R. Sharma"),
        ("UPI Phishing Scam targeting pensioners", "Cybercrime", "Tech Corridor", "Medium", "Under Investigation", False, "Cyber City Tower 4", "Fake utility bill disconnection warning link via SMS.", "Cyber Cell Insp. Anita"),
        ("Commercial check forgery and invoice tampering", "Fraud", "Downtown Central", "Medium", "Solved", False, "Commercial Street Banking Enclave", "Altered recipient account credentials.", "Insp. A. Deshmukh"),
        ("Bus terminal ticket counter vandalism", "Vandalism", "Metro Transit Hub", "Low", "Solved", False, "Bay 4 Intercity Terminal", "Broken display monitors and spray-painted signage.", "Sub-Insp. M. Khan"),
        ("Motorcycle theft from apartment basement", "Vehicle Theft", "West End Suburbs", "Medium", "Reported", False, "Greenwood Towers Basement B2", "Royal Enfield 350 cc registered KA-04-EK-9921 stolen.", "Pending Officer Assignment"),
        ("Narcotics trafficking at cargo terminus", "Drug Offense", "Riverfront Port", "Critical", "Under Investigation", True, "Shed 14 Freight Terminal", "Interstate syndicate consignment intercepted.", "Narcotics Bureau Insp. D. Sen"),
        ("Smartphone snatched while waiting for auto", "Theft", "University District", "Low", "Solved", False, "Outer Ring University Gate", "Snatcher fled on foot towards railway culvert.", "Sub-Insp. T. Gowda"),
        ("Jewelry store nighttime forced entry", "Burglary", "South Commercial Plaza", "Critical", "Under Investigation", True, "5th Block Market Square", "Rear ventilation grill dismantled; lock broken.", "Insp. R. Sharma"),
        ("Purse snatching at vegetable market", "Theft", "West End Suburbs", "Low", "Solved", False, "Sunday Market Main Road", "Perpetrator apprehended by bystanders.", "Sub-Insp. K. Murthy"),
        ("Warehouse copper wire theft", "Burglary", "North Industrial Zone", "High", "Patrol Dispatched", False, "Plot 42 Heavy Machinery Estate", "Security guard tied up during 3 AM shift.", "Insp. V. Kumar"),
        ("Online matrimonial financial deception", "Fraud", "Tech Corridor", "Medium", "Under Investigation", False, "Koramangala 1st Block", "Fraudulent identity extracted funds over 6 months.", "Cyber Cell Insp. Anita"),
        ("Motor vehicle theft outside hospital emergency", "Vehicle Theft", "Downtown Central", "Medium", "Under Investigation", False, "City General Hospital Entry Gate", "Hyundai i20 white color driven away.", "Sub-Insp. M. Patel"),
    ]

    base_time = timezone.now()
    created_count = 0

    for idx, inc in enumerate(sample_incidents):
        title, cat_name, dist_name, severity, status, weapon, address, suspects, officer = inc
        dist = district_objs.get(dist_name)
        cat = category_objs.get(cat_name)

        if not dist or not cat:
            continue

        days_ago = random.randint(1, 45)
        incident_date = (base_time - timedelta(days=days_ago)).date()
        incident_time = datetime.strptime(f"{random.randint(0,23):02d}:{random.randint(0,59):02d}", "%H:%M").time()

        lat_jitter = dist.latitude + random.uniform(-0.012, 0.012)
        lng_jitter = dist.longitude + random.uniform(-0.012, 0.012)

        report, created = CrimeReport.objects.get_or_create(
            title=title,
            district=dist,
            defaults={
                'category': cat,
                'location_address': address,
                'latitude': lat_jitter,
                'longitude': lng_jitter,
                'incident_date': incident_date,
                'incident_time': incident_time,
                'description': f"Incident recorded in {dist.name}. {title}. Complete witness statements recorded at precinct station.",
                'suspect_details': suspects,
                'weapon_involved': weapon,
                'severity': severity,
                'status': status,
                'reporter_name': f"Citizen #{random.randint(100, 999)}",
                'reporter_phone': f"+91 98{random.randint(10000000, 99999999)}",
                'officer_in_charge': officer,
                'investigation_notes': f"Case initiated on {incident_date}. Action status: {status}."
            }
        )
        if created:
            created_count += 1

    print(f" -> {created_count} crime reports generated and verified.")

    print("\n[4/6] Seeding Active Safety Alerts...")
    alerts = [
        {
            'title': 'Heightened Night Patrol in Metro Transit Corridor',
            'district': district_objs.get('Metro Transit Hub'),
            'alert_type': 'Warning',
            'message': 'Increased incidences of pickpocketing reported between 10 PM and 1 AM near south terminal escalators. Extra foot patrol teams deployed.'
        },
        {
            'title': 'Advisory on Fraudulent Electricity Bill Disconnection Calls',
            'district': district_objs.get('Tech Corridor'),
            'alert_type': 'Info',
            'message': 'Citizens are advised not to open APK files or click SMS links threatening power outage. The electricity board never requests instant payments via APK downloads.'
        },
        {
            'title': 'High Security Vigilance in Industrial Logistics Belt',
            'district': district_objs.get('North Industrial Zone'),
            'alert_type': 'Urgent',
            'message': 'Cargo vehicles entering between 11 PM and 5 AM must undergo checkpoint document verification following recent warehouse break-in attempts.'
        }
    ]

    for a in alerts:
        SafetyAlert.objects.get_or_create(
            title=a['title'],
            defaults=a
        )
    print(" -> Safety alerts registered.")

    print("\n[5/6] Training & Caching Scikit-Learn Machine Learning Model...")
    train_and_save_model()
    print(" -> Machine Learning RandomForest pipeline trained and saved to 'crime_model.joblib'.")

    print("\n[6/6] Creating Superuser Admin...")
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@crimeguard.gov', 'admin123')
        print(" -> Created superuser: 'admin' (Password: 'admin123').")
    else:
        print(" -> Superuser 'admin' already exists.")

    print("\n=========================================================")
    print(" CrimeGuard AI Database & ML Engine Setup Complete! ")
    print("=========================================================")


if __name__ == '__main__':
    seed_database()

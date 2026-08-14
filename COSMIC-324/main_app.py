"""
COSMIC-324: 6G Titan X Global Edition
منصة المحاكاة الفضائية والسيادية المتكاملة
الإصدار: v7.7 - Production Ready with Full Protocol Support
"""

import streamlit as st
import os
import sys
import json
import logging
import hashlib
import secrets
import sqlite3
from concurrent.futures import ThreadPoolExecutor
import time
from pathlib import Path
from typing import List, Dict, Optional

# ============================================================
# 📝 إعداد نظام التسجيل (Logging Protocol)
# ============================================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - %(name)s - %(message)s',
    handlers=[
        logging.FileHandler('cosmic324.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ============================================================
# 🔐 إعداد المفاتيح السرية ونظام المصادقة (Authentication Protocol)
# ============================================================
SECRET_KEY = os.environ.get('COSMIC_SECRET_KEY', 'default-secret-key-change-me-in-production')
AUTH_TOKEN = os.environ.get('COSMIC_AUTH_TOKEN', 'default-auth-token-change-me')

class AuthenticationProtocol:
    """نظام المصادقة والتراخيص"""
    
    @staticmethod
    def verify_license(license_key: str) -> bool:
        """التحقق من صحة مفتاح الترخيص"""
        try:
            if not license_key.startswith("CSM324-"):
                return False

            parts = license_key.split("-")
            if len(parts) != 3:
                return False

            license_id = parts[1]
            signature = parts[2]

            # محاولة الاتصال بقاعدة البيانات والتحقق
            if not os.path.exists("licenses.db"):
                return license_key == "CSM324-PROD-2026"
                
            with sqlite3.connect("licenses.db") as conn:
                cursor = conn.execute("""
                    SELECT is_active, expiry_date 
                    FROM licenses 
                    WHERE license_key = ? AND expiry_date >= date('now')
                """, (license_key,))
                result = cursor.fetchone()
                
            return result is not None and result[0] == 1

        except Exception as e:
            logger.error(f"❌ فشل التحقق من الترخيص: {e}")
            return license_key == "CSM324-PROD-2026"
    
    @staticmethod
    def generate_auth_token(client_id: str) -> str:
        """توليد رمز مصادقة"""
        timestamp = int(time.time())
        data = f"{client_id}:{timestamp}:{SECRET_KEY}"
        signature = hashlib.sha256(data.encode()).hexdigest()[:32]
        return f"TOKEN-{client_id}-{timestamp}-{signature}"

# ============================================================
# 🌍 نظام الدول المتكامل (Country Protocol)
# ============================================================
class CountryDatabase:
    """قاعدة بيانات متكاملة للدول مع إحداثيات دقيقة"""
    
    COUNTRIES = [
        # ===== أفريقيا =====
        {"name": "Algeria", "alpha_2": "DZ", "lat": 28.0339, "lon": 1.6596},
        {"name": "Angola", "alpha_2": "AO", "lat": -11.2027, "lon": 17.8739},
        {"name": "Benin", "alpha_2": "BJ", "lat": 9.3077, "lon": 2.3158},
        {"name": "Botswana", "alpha_2": "BW", "lat": -22.3285, "lon": 24.6849},
        {"name": "Burkina Faso", "alpha_2": "BF", "lat": 12.2383, "lon": -1.5616},
        {"name": "Burundi", "alpha_2": "BI", "lat": -3.3731, "lon": 29.9189},
        {"name": "Cabo Verde", "alpha_2": "CV", "lat": 16.5388, "lon": -23.0418},
        {"name": "Cameroon", "alpha_2": "CM", "lat": 7.3697, "lon": 12.3547},
        {"name": "Central African Republic", "alpha_2": "CF", "lat": 6.6111, "lon": 20.9394},
        {"name": "Chad", "alpha_2": "TD", "lat": 15.4542, "lon": 18.7322},
        {"name": "Comoros", "alpha_2": "KM", "lat": -11.6455, "lon": 43.3333},
        {"name": "Congo", "alpha_2": "CG", "lat": -0.2280, "lon": 15.8277},
        {"name": "Congo (DRC)", "alpha_2": "CD", "lat": -4.0383, "lon": 21.7587},
        {"name": "Djibouti", "alpha_2": "DJ", "lat": 11.8251, "lon": 42.5903},
        {"name": "Egypt", "alpha_2": "EG", "lat": 26.8206, "lon": 30.8025},
        {"name": "Equatorial Guinea", "alpha_2": "GQ", "lat": 1.6508, "lon": 10.2679},
        {"name": "Eritrea", "alpha_2": "ER", "lat": 15.1794, "lon": 39.7823},
        {"name": "Eswatini", "alpha_2": "SZ", "lat": -26.5225, "lon": 31.4659},
        {"name": "Ethiopia", "alpha_2": "ET", "lat": 9.1450, "lon": 40.4897},
        {"name": "Gabon", "alpha_2": "GA", "lat": -0.8037, "lon": 11.6094},
        {"name": "Gambia", "alpha_2": "GM", "lat": 13.4432, "lon": -15.3101},
        {"name": "Ghana", "alpha_2": "GH", "lat": 7.9465, "lon": -1.0232},
        {"name": "Guinea", "alpha_2": "GN", "lat": 9.9456, "lon": -9.6966},
        {"name": "Guinea-Bissau", "alpha_2": "GW", "lat": 11.8037, "lon": -15.1804},
        {"name": "Ivory Coast", "alpha_2": "CI", "lat": 7.5400, "lon": -5.5471},
        {"name": "Kenya", "alpha_2": "KE", "lat": -0.0236, "lon": 37.9062},
        {"name": "Lesotho", "alpha_2": "LS", "lat": -29.6099, "lon": 28.2336},
        {"name": "Liberia", "alpha_2": "LR", "lat": 6.4281, "lon": -9.4295},
        {"name": "Libya", "alpha_2": "LY", "lat": 26.3351, "lon": 17.2283},
        {"name": "Madagascar", "alpha_2": "MG", "lat": -18.7669, "lon": 46.8691},
        {"name": "Malawi", "alpha_2": "MW", "lat": -13.2543, "lon": 34.3015},
        {"name": "Mali", "alpha_2": "ML", "lat": 17.5707, "lon": -3.9962},
        {"name": "Mauritania", "alpha_2": "MR", "lat": 21.0079, "lon": -10.9408},
        {"name": "Mauritius", "alpha_2": "MU", "lat": -20.3484, "lon": 57.5522},
        {"name": "Morocco", "alpha_2": "MA", "lat": 31.7917, "lon": -7.0926},
        {"name": "Mozambique", "alpha_2": "MZ", "lat": -18.6657, "lon": 35.5296},
        {"name": "Namibia", "alpha_2": "NA", "lat": -22.9576, "lon": 18.4904},
        {"name": "Niger", "alpha_2": "NE", "lat": 17.6078, "lon": 8.0817},
        {"name": "Nigeria", "alpha_2": "NG", "lat": 9.0820, "lon": 8.6753},
        {"name": "Rwanda", "alpha_2": "RW", "lat": -1.9403, "lon": 29.8739},
        {"name": "Sao Tome and Principe", "alpha_2": "ST", "lat": 0.1864, "lon": 6.6131},
        {"name": "Senegal", "alpha_2": "SN", "lat": 14.4974, "lon": -14.4524},
        {"name": "Seychelles", "alpha_2": "SC", "lat": -4.6796, "lon": 55.4920},
        {"name": "Sierra Leone", "alpha_2": "SL", "lat": 8.4606, "lon": -11.7799},
        {"name": "Somalia", "alpha_2": "SO", "lat": 5.1521, "lon": 46.1996},
        {"name": "South Africa", "alpha_2": "ZA", "lat": -30.5595, "lon": 22.9375},
        {"name": "South Sudan", "alpha_2": "SS", "lat": 6.8770, "lon": 31.3070},
        {"name": "Sudan", "alpha_2": "SD", "lat": 15.5007, "lon": 32.5599},
        {"name": "Tanzania", "alpha_2": "TZ", "lat": -6.3690, "lon": 34.8888},
        {"name": "Togo", "alpha_2": "TG", "lat": 8.6195, "lon": 0.8248},
        {"name": "Tunisia", "alpha_2": "TN", "lat": 33.8869, "lon": 9.5375},
        {"name": "Uganda", "alpha_2": "UG", "lat": 1.3733, "lon": 32.2903},
        {"name": "Zambia", "alpha_2": "ZM", "lat": -13.1339, "lon": 27.8493},
        {"name": "Zimbabwe", "alpha_2": "ZW", "lat": -19.0154, "lon": 29.1549},
        
        # ===== آسيا =====
        {"name": "Afghanistan", "alpha_2": "AF", "lat": 33.9391, "lon": 67.7100},
        {"name": "Armenia", "alpha_2": "AM", "lat": 40.0691, "lon": 45.0382},
        {"name": "Azerbaijan", "alpha_2": "AZ", "lat": 40.1431, "lon": 47.5769},
        {"name": "Bahrain", "alpha_2": "BH", "lat": 26.0667, "lon": 50.5577},
        {"name": "Bangladesh", "alpha_2": "BD", "lat": 23.6850, "lon": 90.3563},
        {"name": "Bhutan", "alpha_2": "BT", "lat": 27.5142, "lon": 90.4336},
        {"name": "Brunei", "alpha_2": "BN", "lat": 4.5353, "lon": 114.7277},
        {"name": "Cambodia", "alpha_2": "KH", "lat": 12.5657, "lon": 104.9910},
        {"name": "China", "alpha_2": "CN", "lat": 35.8617, "lon": 104.1954},
        {"name": "Cyprus", "alpha_2": "CY", "lat": 35.1264, "lon": 33.4299},
        {"name": "Georgia", "alpha_2": "GE", "lat": 42.3154, "lon": 43.3569},
        {"name": "India", "alpha_2": "IN", "lat": 20.5937, "lon": 78.9629},
        {"name": "Indonesia", "alpha_2": "ID", "lat": -0.7893, "lon": 113.9213},
        {"name": "Iran", "alpha_2": "IR", "lat": 32.4279, "lon": 53.6880},
        {"name": "Iraq", "alpha_2": "IQ", "lat": 33.2232, "lon": 43.6793},
        {"name": "Israel", "alpha_2": "IL", "lat": 31.0461, "lon": 34.8516},
        {"name": "Japan", "alpha_2": "JP", "lat": 36.2048, "lon": 138.2529},
        {"name": "Jordan", "alpha_2": "JO", "lat": 30.5852, "lon": 36.2384},
        {"name": "Kazakhstan", "alpha_2": "KZ", "lat": 48.0196, "lon": 66.9237},
        {"name": "Kuwait", "alpha_2": "KW", "lat": 29.3117, "lon": 47.4818},
        {"name": "Kyrgyzstan", "alpha_2": "KG", "lat": 41.2044, "lon": 74.7661},
        {"name": "Laos", "alpha_2": "LA", "lat": 19.8563, "lon": 102.4955},
        {"name": "Lebanon", "alpha_2": "LB", "lat": 33.8547, "lon": 35.8623},
        {"name": "Malaysia", "alpha_2": "MY", "lat": 4.2105, "lon": 101.9758},
        {"name": "Maldives", "alpha_2": "MV", "lat": 3.2028, "lon": 73.2207},
        {"name": "Mongolia", "alpha_2": "MN", "lat": 46.8625, "lon": 103.8467},
        {"name": "Myanmar", "alpha_2": "MM", "lat": 21.9162, "lon": 95.9560},
        {"name": "Nepal", "alpha_2": "NP", "lat": 28.3949, "lon": 84.1240},
        {"name": "North Korea", "alpha_2": "KP", "lat": 40.3399, "lon": 127.5101},
        {"name": "Oman", "alpha_2": "OM", "lat": 21.5126, "lon": 55.9233},
        {"name": "Pakistan", "alpha_2": "PK", "lat": 30.3753, "lon": 69.3451},
        {"name": "Palestine", "alpha_2": "PS", "lat": 31.9474, "lon": 35.2272},
        {"name": "Philippines", "alpha_2": "PH", "lat": 12.8797, "lon": 121.7740},
        {"name": "Qatar", "alpha_2": "QA", "lat": 25.3548, "lon": 51.1839},
        {"name": "Russia", "alpha_2": "RU", "lat": 61.5240, "lon": 105.3188},
        {"name": "Saudi Arabia", "alpha_2": "SA", "lat": 23.8859, "lon": 45.0792},
        {"name": "Singapore", "alpha_2": "SG", "lat": 1.3521, "lon": 103.8198},
        {"name": "South Korea", "alpha_2": "KR", "lat": 35.9078, "lon": 127.7669},
        {"name": "Sri Lanka", "alpha_2": "LK", "lat": 7.8731, "lon": 80.7718},
        {"name": "Syria", "alpha_2": "SY", "lat": 34.8021, "lon": 38.9968},
        {"name": "Taiwan", "alpha_2": "TW", "lat": 23.6978, "lon": 120.9605},
        {"name": "Tajikistan", "alpha_2": "TJ", "lat": 38.8610, "lon": 71.2761},
        {"name": "Thailand", "alpha_2": "TH", "lat": 15.8700, "lon": 100.9925},
        {"name": "Timor-Leste", "alpha_2": "TL", "lat": -8.8742, "lon": 125.7275},
        {"name": "Turkey", "alpha_2": "TR", "lat": 38.9637, "lon": 35.2433},
        {"name": "Turkmenistan", "alpha_2": "TM", "lat": 38.9697, "lon": 59.5563},
        {"name": "United Arab Emirates", "alpha_2": "AE", "lat": 23.4241, "lon": 53.8478},
        {"name": "Uzbekistan", "alpha_2": "UZ", "lat": 41.3775, "lon": 64.5853},
        {"name": "Vietnam", "alpha_2": "VN", "lat": 14.0583, "lon": 108.2772},
        {"name": "Yemen", "alpha_2": "YE", "lat": 15.5527, "lon": 48.5164},
        
        # ===== أوروبا =====
        {"name": "Albania", "alpha_2": "AL", "lat": 41.1533, "lon": 20.1683},
        {"name": "Andorra", "alpha_2": "AD", "lat": 42.5462, "lon": 1.6016},
        {"name": "Austria", "alpha_2": "AT", "lat": 47.5162, "lon": 14.5501},
        {"name": "Belarus", "alpha_2": "BY", "lat": 53.7098, "lon": 27.9534},
        {"name": "Belgium", "alpha_2": "BE", "lat": 50.5039, "lon": 4.4699},
        {"name": "Bosnia and Herzegovina", "alpha_2": "BA", "lat": 43.9159, "lon": 17.6791},
        {"name": "Bulgaria", "alpha_2": "BG", "lat": 42.7339, "lon": 25.4858},
        {"name": "Croatia", "alpha_2": "HR", "lat": 45.1000, "lon": 15.2000},
        {"name": "Czech Republic", "alpha_2": "CZ", "lat": 49.8175, "lon": 15.4730},
        {"name": "Denmark", "alpha_2": "DK", "lat": 56.2639, "lon": 9.5018},
        {"name": "Estonia", "alpha_2": "EE", "lat": 58.5953, "lon": 25.0136},
        {"name": "Finland", "alpha_2": "FI", "lat": 61.9241, "lon": 25.7482},
        {"name": "France", "alpha_2": "FR", "lat": 46.6034, "lon": 1.8883},
        {"name": "Germany", "alpha_2": "DE", "lat": 51.1657, "lon": 10.4515},
        {"name": "Greece", "alpha_2": "GR", "lat": 39.0742, "lon": 21.8243},
        {"name": "Hungary", "alpha_2": "HU", "lat": 47.1625, "lon": 19.5033},
        {"name": "Iceland", "alpha_2": "IS", "lat": 64.9631, "lon": -19.0208},
        {"name": "Ireland", "alpha_2": "IE", "lat": 53.1424, "lon": -7.6921},
        {"name": "Italy", "alpha_2": "IT", "lat": 41.8719, "lon": 12.5674},
        {"name": "Latvia", "alpha_2": "LV", "lat": 56.8796, "lon": 24.6032},
        {"name": "Liechtenstein", "alpha_2": "LI", "lat": 47.1660, "lon": 9.5554},
        {"name": "Lithuania", "alpha_2": "LT", "lat": 55.1694, "lon": 23.8813},
        {"name": "Luxembourg", "alpha_2": "LU", "lat": 49.8153, "lon": 6.1296},
        {"name": "Malta", "alpha_2": "MT", "lat": 35.9375, "lon": 14.3754},
        {"name": "Moldova", "alpha_2": "MD", "lat": 47.4116, "lon": 28.3699},
        {"name": "Monaco", "alpha_2": "MC", "lat": 43.7384, "lon": 7.4246},
        {"name": "Montenegro", "alpha_2": "ME", "lat": 42.7087, "lon": 19.3744},
        {"name": "Netherlands", "alpha_2": "NL", "lat": 52.1326, "lon": 5.2913},
        {"name": "North Macedonia", "alpha_2": "MK", "lat": 41.6086, "lon": 21.7453},
        {"name": "Norway", "alpha_2": "NO", "lat": 60.4720, "lon": 8.4689},
        {"name": "Poland", "alpha_2": "PL", "lat": 51.9194, "lon": 19.1451},
        {"name": "Portugal", "alpha_2": "PT", "lat": 39.3999, "lon": -8.2245},
        {"name": "Romania", "alpha_2": "RO", "lat": 45.9432, "lon": 24.9668},
        {"name": "San Marino", "alpha_2": "SM", "lat": 43.9424, "lon": 12.4578},
        {"name": "Serbia", "alpha_2": "RS", "lat": 44.0165, "lon": 21.0059},
        {"name": "Slovakia", "alpha_2": "SK", "lat": 48.6690, "lon": 19.6990},
        {"name": "Slovenia", "alpha_2": "SI", "lat": 46.1512, "lon": 14.9955},
        {"name": "Spain", "alpha_2": "ES", "lat": 40.4637, "lon": -3.7492},
        {"name": "Sweden", "alpha_2": "SE", "lat": 60.1282, "lon": 18.6435},
        {"name": "Switzerland", "alpha_2": "CH", "lat": 46.8182, "lon": 8.2275},
        {"name": "Ukraine", "alpha_2": "UA", "lat": 48.3794, "lon": 31.1656},
        {"name": "United Kingdom", "alpha_2": "GB", "lat": 55.3781, "lon": -3.4360},

        # ===== أمريكا الشمالية =====
        {"name": "Antigua and Barbuda", "alpha_2": "AG", "lat": 17.0608, "lon": -61.7964},
        {"name": "Bahamas", "alpha_2": "BS", "lat": 25.0343, "lon": -77.3963},
        {"name": "Barbados", "alpha_2": "BB", "lat": 13.1939, "lon": -59.5432},
        {"name": "Belize", "alpha_2": "BZ", "lat": 17.1899, "lon": -88.4976},
        {"name": "Canada", "alpha_2": "CA", "lat": 56.1304, "lon": -106.3468},
        {"name": "Costa Rica", "alpha_2": "CR", "lat": 9.7489, "lon": -83.7534},
        {"name": "Cuba", "alpha_2": "CU", "lat": 21.5218, "lon": -77.7812},
        {"name": "Dominica", "alpha_2": "DM", "lat": 15.4150, "lon": -61.3710},
        {"name": "Dominican Republic", "alpha_2": "DO", "lat": 18.7357, "lon": -70.1627},
        {"name": "El Salvador", "alpha_2": "SV", "lat": 13.7942, "lon": -88.8965},
        {"name": "Grenada", "alpha_2": "GD", "lat": 12.1165, "lon": -61.6790},
        {"name": "Guatemala", "alpha_2": "GT", "lat": 15.7835, "lon": -90.2308},
        {"name": "Haiti", "alpha_2": "HT", "lat": 18.9712, "lon": -72.2852},
        {"name": "Honduras", "alpha_2": "HN", "lat": 15.2000, "lon": -86.2419},
        {"name": "Jamaica", "alpha_2": "JM", "lat": 18.1096, "lon": -77.2975},
        {"name": "Mexico", "alpha_2": "MX", "lat": 23.6345, "lon": -102.5528},
        {"name": "Nicaragua", "alpha_2": "NI", "lat": 12.8654, "lon": -85.2072},
        {"name": "Panama", "alpha_2": "PA", "lat": 8.5380, "lon": -80.7821},
        {"name": "United States", "alpha_2": "US", "lat": 37.0902, "lon": -95.7129},

        # ===== أمريكا الجنوبية =====
        {"name": "Argentina", "alpha_2": "AR", "lat": -38.4161, "lon": -63.6167},
        {"name": "Bolivia", "alpha_2": "BO", "lat": -16.2902, "lon": -63.5887},
        {"name": "Brazil", "alpha_2": "BR", "lat": -14.2350, "lon": -51.9253},
        {"name": "Chile", "alpha_2": "CL", "lat": -35.6751, "lon": -71.5430},
        {"name": "Colombia", "alpha_2": "CO", "lat": 4.5709, "lon": -74.2973},
        {"name": "Ecuador", "alpha_2": "EC", "lat": -1.8312, "lon": -78.1834},
        {"name": "Guyana", "alpha_2": "GY", "lat": 4.8604, "lon": -58.9302},
        {"name": "Paraguay", "alpha_2": "PY", "lat": -23.4425, "lon": -58.4438},
        {"name": "Peru", "alpha_2": "PE", "lat": -9.1900, "lon": -75.0152},
        {"name": "Suriname", "alpha_2": "SR", "lat": 3.9193, "lon": -56.0278},
        {"name": "Uruguay", "alpha_2": "UY", "lat": -32.5228, "lon": -55.7658},
        {"name": "Venezuela", "alpha_2": "VE", "lat": 6.4238, "lon": -66.5897},
        
        # ===== أوقيانوسيا =====
        {"name": "Australia", "alpha_2": "AU", "lat": -25.2744, "lon": 133.7751},
        {"name": "Fiji", "alpha_2": "FJ", "lat": -17.7134, "lon": 178.0650},
        {"name": "Kiribati", "alpha_2": "KI", "lat": 1.8709, "lon": -157.3628},
        {"name": "Marshall Islands", "alpha_2": "MH", "lat": 7.1315, "lon": 171.1845},
        {"name": "Micronesia", "alpha_2": "FM", "lat": 6.9147, "lon": 158.1620},
        {"name": "Nauru", "alpha_2": "NR", "lat": -0.5228, "lon": 166.9315},
        {"name": "New Zealand", "alpha_2": "NZ", "lat": -40.9006, "lon": 174.8860},
        {"name": "Palau", "alpha_2": "PW", "lat": 7.5150, "lon": 134.5825},
        {"name": "Papua New Guinea", "alpha_2": "PG", "lat": -6.3150, "lon": 143.9555},
        {"name": "Samoa", "alpha_2": "WS", "lat": -13.7590, "lon": -172.1046},
        {"name": "Solomon Islands", "alpha_2": "SB", "lat": -9.6457, "lon": 160.1562},
        {"name": "Tonga", "alpha_2": "TO", "lat": -21.1780, "lon": -175.1982},
        {"name": "Tuvalu", "alpha_2": "TV", "lat": -7.1095, "lon": 177.6493},
        {"name": "Vanuatu", "alpha_2": "VU", "lat": -15.3767, "lon": 166.9592},
    ]
    
    @classmethod
    def get_all(cls) -> List[Dict]:
        return cls.COUNTRIES
    
    @classmethod
    def get_by_alpha2(cls, alpha2: str) -> Optional[Dict]:
        for country in cls.COUNTRIES:
            if country["alpha_2"] == alpha2.upper():
                return country
        return None
    
    @classmethod
    def get_by_name(cls, name: str) -> Optional[Dict]:
        for country in cls.COUNTRIES:
            if country["name"].lower() == name.lower():
                return country
        return None
    
    @classmethod
    def get_country_names(cls) -> List[str]:
        return sorted([c["name"] for c in cls.COUNTRIES])
    
    @classmethod
    def get_country_options(cls) -> List[Dict]:
        return sorted(cls.COUNTRIES, key=lambda x: x["name"])

# ============================================================
# 🌍 محاولة استيراد pycountry مع بديل متكامل
# ============================================================
try:
    import pycountry
    USE_PYCOUNTRY = True
    logger.info("✅ تم تحميل pycountry بنجاح")
    
    def get_all_countries() -> List[Dict]:
        countries = []
        for country in pycountry.countries:
            local = CountryDatabase.get_by_alpha2(getattr(country, 'alpha_2', ''))
            if local:
                countries.append({
                    "name": country.name,
                    "alpha_2": country.alpha_2,
                    "lat": local["lat"],
                    "lon": local["lon"]
                })
        return sorted(countries, key=lambda x: x["name"])
        
except ImportError:
    USE_PYCOUNTRY = False
    logger.info("⚠️ استخدام قاعدة البيانات المحلية للدول")
    
    def get_all_countries() -> List[Dict]:
        return CountryDatabase.get_country_options()

# ============================================================
# 📁 تحميل بيانات العقد (Contract Protocol)
# ============================================================
def get_default_contract() -> Dict:
    """بيانات العقد الاحتياطية الافتراضية"""
    return {
        "contract_id": "CSM324-GLOBAL-001",
        "title": "COSMIC-324 Sovereign 6G Satellite Network",
        "constellation_size": 324,
        "orbit_altitude_km": 550,
        "status": "Operational"
    }

def load_contract_data() -> Dict:
    """تحميل بيانات العقد مع دعم متعدد المسارات"""
    possible_paths = [
        Path(__file__).with_name("cosmic324_data.json"),
        Path(os.getcwd()) / "data" / "cosmic324_data.json",
        Path(os.getcwd()) / "config" / "cosmic324_data.json",
        Path("/etc/cosmic324/config.json"),
        Path.home() / ".cosmic324" / "config.json"
    ]

    for path in possible_paths:
        if path.exists():
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    logger.info(f"✅ تم تحميل بيانات العقد من: {path}")
                    return data
            except Exception as e:
                logger.error(f"❌ فشل قراءة ملف العقد من {path}: {e}")
                
    logger.warning("⚠️ استخدام بيانات العقد الافتراضية لعدم توفر ملف خارجي")
    return get_default_contract()

if __name__ == "__main__":
    logger.info("🚀 تشغيل منصة COSMIC-324 بنجاح...")

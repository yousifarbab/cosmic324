import hmac
import hashlib
import base64
import json
import time

class SovereignLicensing:
    def __init__(self, secret_key: str):
        """
        مهندس التراخيص السيادية لمشروع COSMIC-324
        يستخدم المفتاح السري الخاص بك لتوقيع التراخيص رقمياً.
        """
        self.secret_key = secret_key.encode('utf-8')

    def generate_license(self, company_name: str, validity_days: int, max_satellites: int) -> str:
        """
        توليد رخصة تشغيل تجارية مشفرة للعميل
        """
        expiration_timestamp = int(time.time()) + (validity_days * 86400)
        
        payload = {
            "company": company_name,
            "expires_at": expiration_timestamp,
            "max_satellites": max_satellites,
            "version": "V17.0-Enterprise"
        }
        
        # تحويل البيانات إلى نص JSON ثم ترميزها بـ Base64
        payload_json = json.dumps(payload, sort_keys=True)
        payload_encoded = base64.urlsafe_b64encode(payload_json.encode('utf-8')).decode('utf-8')
        
        # توليد التوقيع المشفر لمنع التلاعب
        signature = hmac.new(
            self.secret_key,
            payload_encoded.encode('utf-8'),
            hashlib.sha256
        ).digest()
        signature_encoded = base64.urlsafe_b64encode(signature).decode('utf-8')
        
        # دمج الحمولة مع التوقيع لتشكيل مفتاح الرخصة النهائي
        full_license_key = f"{payload_encoded}.{signature_encoded}"
        return full_license_key

    def verify_license(self, license_key: str) -> dict:
        """
        التحقق من صحة وصلاحية الرخصة المقدمة من العميل
        """
        try:
            parts = license_key.split('.')
            if len(parts) != 2:
                return {"valid": False, "reason": "مفتاح الرخصة غير صالح هيكلياً."}
            
            payload_encoded, signature_encoded = parts
            
            # إعادة حساب التوقيع والتحقق منه
            expected_signature = hmac.new(
                self.secret_key,
                payload_encoded.encode('utf-8'),
                hashlib.sha256
            ).digest()
            expected_signature_encoded = base64.urlsafe_b64encode(expected_signature).decode('utf-8')
            
            if not hmac.compare_digest(expected_signature_encoded, signature_encoded):
                return {"valid": False, "reason": "التوقيع الرقمي غير مطابق (رخصة مزيفة أو معدلة)."}
            
            # فك تشفير البيانات
            payload_json = base64.urlsafe_b64decode(payload_encoded.encode('utf-8')).decode('utf-8')
            payload = json.loads(payload_json)
            
            # التحقق من تاريخ الانتهاء
            if int(time.time()) > payload["expires_at"]:
                return {"valid": False, "reason": "انتهت صلاحية هذه الرخصة."}
            
            return {"valid": True, "data": payload}
                
        except Exception as e:
            return {"valid": False, "reason": f"خطأ في معالجة الرخصة: {str(e)}"}

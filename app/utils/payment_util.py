import uuid
from datetime import datetime, timedelta


class PaymentUtil:
    @classmethod
    async def create_uuid_to_sting(cls) -> str:
        now = datetime.utcnow() + timedelta(hours=9)
        now_date_stripe = now.strftime("%Y-%m-%d")
        now_date = now_date_stripe.replace("-", "")
        order_unique_uuid = str(uuid.uuid4()).replace("-", "")
        return now_date + "--" + order_unique_uuid

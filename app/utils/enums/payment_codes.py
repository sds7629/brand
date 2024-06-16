from enum import Enum

class PaymentMethodCode(str, Enum):
    CARD = "card"
    VIRTUAL_ACCOUNT = "virtual_account"
    TRANSFER = "transfer"
    MOBILE = "mobile"
    GIFT_CERTIFICATE = "gift_certificate"
    EASY_PAY = "easy_pay"
from enum import Enum


class StatusCode(str, Enum):
    ORDER_PLACED = "주문 접수"
    PREPARING_FOR_SHIPMENT = "상품 준비 중"
    READY_FOR_DELIVERY = "배송 준비 중"
    SHIPPED = "배송 중"
    DELIVERED = "배송 완료"
    ORDER_CANCELLED = "주문 취소"

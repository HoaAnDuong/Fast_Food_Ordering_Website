from .models import Product_Status

PRODUCT_PENDING_STATUS = Product_Status.objects.get(code = "pending")
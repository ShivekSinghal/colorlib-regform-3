from cashfree_sdk.payouts import Payouts

api = "https://sandbox.cashfree.com/pg/api/v1/order/create"
# Your Cashfree API credentials
cashfree_app_id = 'TEST43522824da29604a286cb40521822534'
cashfree_secret_key = 'TEST613bfce859f23cd24f50d9664812fb224423c712'



Payouts.init(cashfree_app_id, cashfree_secret_key, "TEST")

from cashfree_sdk import verification
webhook_data = '{"cashgramId": "5b8283182e0711eaa4c531df6a4f439b-28", "event": "CASHGRAM_EXPIRED", "eventTime": "2020-01-03 15:01:06", "reason": "OTP_ATTEMPTS_EXCEEDED", "signature": "TBpM+4nr1DsWsov7QiHSTfRJP4Z9BD8XrDgEhBlf9ss="}'
verification.verify_webhook(webhook_data, 'JSON')

from cashfree_sdk.payouts.beneficiary import Beneficiary
bene_add = Beneficiary.add("kit_test6", "Shivek", "singhalshivek24@gmail.com", "8527805203", "ehohfhbjre fh")
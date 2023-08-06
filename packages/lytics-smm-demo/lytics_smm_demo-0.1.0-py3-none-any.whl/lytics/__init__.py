from .main import Lytics

'''
     Initiate Lytics with your api key
----------------------------------------

lytics = Lytics(api_key)

            FUNCTIONS
----------------------------------------

* SERVICES *

services = lytics.services()
print(services)

----------------------------------------

* CHECK BALANCE *

balance = lytics.balance()
print(balance)
----------------------------------------

* CREATE NEW ORDER *

# Default
order_response = order(service_id=1, link='http://example.com/username', quantity=100, runs=2, interval=5)
print(order_response)

# Custom Comments
order_response = order(service_id=1, link='http://example.com/username', comments="good pic\ngreat photo\n:)\n;)")
print(order_response)

# Mentions with Hashtags
order_response = order(service_id=1, link='http://example.com/username', quantity=100, usernames="test, testing", hashtags="#goodphoto")
print(order_response)

# Mentions User Followers
order_response = order(service_id=1, link='http://example.com/username', quantity=1000, username="test")
print(order_response)

# Package
order_response = order(service_id=1, link='http://example.com/username')
print(order_response)

# Subscriptions (Old posts only)
order_response = order(service_id=1, username='username', min=100, max=110, posts=0, delay=30, expiry='11/11/2022')
print(order_response)

# Subscriptions (Unlimited new posts and 5 old posts)
order_response = order(service_id=1, username='username', min=100, max=110, old_posts=5, delay=30, expiry='11/11/2022')
print(order_response)

# Poll
order_response = order(service_id=1, link='http://example.com/test', quantity=100, answer_number='7')
print(order_response)

# Invites from Groups
order_response = order(service_id=1, link='http://example.com/test', quantity=100, groups="group1\ngroup2")
print(order_response)


----------------------------------------

* CHECK ORDER STATUS *

status = lytics.status(order_id=11234)
print(status)

* CHECK MULTIPLE ORDER STATUS'S *

multi_status = lytics.multi_status(order_ids=[12342, 34634, 12301, 34453])
print(multi_status)

----------------------------------------

* CREATE REFILL *

refill = lytics.refill(order_id=12345)
print(refill)

* CREATE MULTIPLE REFILLS *

multi_refill = lytics.multi_refill(order_ids=[12342, 34634, 12983, 23443])
print(multi_refill)

----------------------------------------

* CHECK REFILL STATUS *

status = lytics.refill_status(refill_id=23423)
print(status)

* CHECK MULTIPLE REFILL STATUS'S *

multi_status = lytics.multi_refill_status(refill_ids=[23423, 12344, 91818, 12311])
print(status)

'''
# lytics-smm-demo

A Python package for interacting with the [Lytics.lol](https://lyticss.lol) SMM API.

## Installation

Install the package using pip:

```shell
pip install lytics-smm-demo
```
\* currently demo *

## Usage
To use the functions in this package, import the Lytics class from lytics, and create an instance with your API key.

```python
from lytics import Lytics

api_key = 'API_Key_Here'
lytics = Lytics(api_key)

```
you can then use any of the functions below using the 'lytics' object.

## Functions
### For a list of availible services: 
```python
services = lytics.services()
print(services)
```

### To check your balance:
```python
balance = lytics.balance()
print(balance)
```

### To create a new order, there is multiple options:
```python
# Default
order = lytics.order(service_id=1, link='http://example.com/username', quantity=100, runs=2, interval=5)
print(order)

# Custom Comments
order = lytics.order(service_id=1, link='http://example.com/username', comments="good pic\ngreat photo\n:)\n;)")
print(order)

# Mentions with Hashtags
order = lytics.order(service_id=1, link='http://example.com/username', quantity=100, usernames="test, testing", hashtags="#goodphoto")
print(order)

# Mentions User Followers
order = lytics.order(service_id=1, link='http://example.com/username', quantity=1000, username="test")
print(order)

# Package
order = lytics.order(service_id=1, link='http://example.com/username')
print(order)

# Subscriptions (Old posts only)
order = lytics.order(service_id=1, username='username', min=100, max=110, posts=0, delay=30, expiry='11/11/2022')
print(order)

# Subscriptions (Unlimited new posts and 5 old posts)
order = lytics.order(service_id=1, username='username', min=100, max=110, old_posts=5, delay=30, expiry='11/11/2022')
print(order)

# Poll
order = lytics.order(service_id=1, link='http://example.com/test', quantity=100, answer_number='7')
print(order)

# Invites from Groups
order = lytics.order(service_id=1, link='http://example.com/test', quantity=100, groups="group1\ngroup2")
print(order)
```

### To check the status of a order / multiple orders: 
```python
status = lytics.status(order_id=11234)
print(status)

# check multiple order status's
multi_status = lytics.multi_status(order_ids=[12342, 34634, 12301, 34453])
print(multi_status)

```

### To create a new refill / multiple refills:
```python
refill = lytics.refill(order_id=12345)
print(refill)

# create multiple refills
multi_refill = lytics.multi_refill(order_ids=[12342, 34634, 12983, 23443])
print(multi_refill)
```

### To check the status of a refill / multiple refills:
```python
status = lytics.refill_status(refill_id=23423)
print(status)

# check multiple refill status's
multi_status = lytics.multi_refill_status(refill_ids=[23423, 12344, 91818, 12311])
print(status)
``` 
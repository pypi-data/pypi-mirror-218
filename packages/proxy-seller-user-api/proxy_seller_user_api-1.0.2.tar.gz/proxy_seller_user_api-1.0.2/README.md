# proxy-seller python api

Install from [pypi.org](https://pypi.org/project/proxy-seller-user-api)
```sh
pip3 install proxy-seller-user-api
```

Or manual install from [proxy-seller/user-api-python](https://bitbucket.org/proxy-seller/user-api-python) repository
```sh
pip3 install git+https://bitbucket.org/proxy-seller/user-api-python
```

## Quick start
Get API key [here](https://proxy-seller.com/personal/api/)
```py
from proxy_seller_user_api import Api
api = Api({'key':'YOUR_API_KEY'})
print(api.balance())
```

## Methods available:
* balance
* balanceAdd
* balancePaymentsList
* referenceList
* orderCalcIpv4
* orderCalcIsp
* orderCalcMix
* orderCalcIpv6
* orderCalcMobile
* orderMakeIpv4
* orderMakeIsp
* orderMakeMix
* orderMakeIpv6
* orderMakeMobile
* prolongCalc
* prolongMake
* proxyList
* proxyDownload
* proxyCommentSet
* proxyCheck
* ping
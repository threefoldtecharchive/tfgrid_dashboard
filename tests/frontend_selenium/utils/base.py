class Base:
    port = 3060
    net = 'dev'
    base_url = 'http://localhost:' + str(port) + '/'
    gridproxy_url = 'https://gridproxy.' + net + '.grid.tf/'
    extension_url = 'chrome-extension://mopnmbcafieddcagagdcbnhejhlodfdd/index.html#/'
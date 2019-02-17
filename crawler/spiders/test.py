import hashlib

temp = "数加".encode("utf-8")

m = hashlib.md5()
m.update(temp)
sign = m.hexdigest().upper()




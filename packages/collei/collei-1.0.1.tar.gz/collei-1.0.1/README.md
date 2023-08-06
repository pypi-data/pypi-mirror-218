# collei

🍂 An unofficial [_Waifu.pics API_](https://waifu.pics) wrapper for Python

# 📦 Packages

## 🐍 PyPi

```sh
pip install collei
```

# 🔎 Examples

[_examples/basic.py_](https://github.com/elaresai/collei/blob/main/examples/basic.py)

```py
import collei

client = collei.Client()

print(client.sfw.get(collei.SfwCategory.HUG))
print(client.sfw.get(collei.SfwCategory.KISS))
print(client.sfw.get(collei.SfwCategory.LICK))
print(client.sfw.get(collei.SfwCategory.BITE))
```

# ✨ Links

[🐍 _PyPI_](https://pypi.org/project/collei/)\
[🏠 _Homepage_](https://github.com/elaresai/collei)\
[🐱 _Repository_](https://github.com/elaresai/collei)

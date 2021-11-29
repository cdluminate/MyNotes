from pathlib import Path

p = Path('.')
print([x for x in p.iterdir() if x.is_dir()])

p = Path('a')
print('/usr/' / p / 'asdf' / 'asdf')
print(p.exists())

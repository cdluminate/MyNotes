from configparser import ConfigParser

config = ConfigParser()
config['DEFAULT'] = {'alpha': 0.1, 'beta': 1.0, 'type': 'default'}
with open('config.ini', 'w') as f:
    config.write(f)

config.read('config.ini')
print(config['DEFAULT']['alpha'])
print(config.get('DEFAULT', 'alphax', fallback=100))

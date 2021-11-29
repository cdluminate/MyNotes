#import pretty_errors
import rich
from rich.panel import Panel
from rich.progress import track
import time
c = rich.get_console()

for n in track(range(10), description='processing...', transient=True):
    c.log(n)
    time.sleep(0.1)

example = {'a': 123, 'b': 29.0, 'c': {1:1, 2:2}}

c.print("[italic red]Hello[/italic red] World!", locals())
c.print(example)
rich.inspect(example)

c.print([1, 2, 3])
c.print("[blue underline]Looks like a link")
c.print("FOO", style="white on blue")
c.log('hello world')
c.rule("[bold red]Chapter 2")

with c.status('working ...'):
    time.sleep(0.5)
    c.log('asdfasdf')
    time.sleep(0.5)
    c.log('asdf')
c.print('Rich', justify='right')
c.print(Panel('hello'))
c.print(Panel.fit('hello'))

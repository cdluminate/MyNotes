import io
import pandas as pd
import matplotlib.pyplot as plt

# data source: Kyunghyun Cho @kchonyc from Twitter (keyword: ICML2023)
CSV = io.StringIO('''Overdue_(days) ICML_Review_Progress
7 90.58
6 86.95
0 64.98
-1 35.00
-2 22.16
-3 14.12
-4 12.33
-5 9.61
-6 7.81
''')

df = pd.read_csv(CSV, sep=' ')
print(df)

plt.figure()
ax = plt.gca()

ax.plot([-7, 8], [100, 100], color='black')
df.plot(0, 1, style='o-', color='red', ax=ax)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
#ax.spines['left'].set_visible(False)
ax.grid(True, linestyle=':')

plt.show()

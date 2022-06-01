import re
import math
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# Opening extracted text file
File = "Rewe_sample.txt"
Text = str(open(File, "r").read())

# Text sorting, RegEx method
# Common words pattern
Com_words = re.compile(
    r"\bREWE\b|\bEUR\b|\bPAYBACK\b|\bBAR\b|\bSUMME\b|\bA\b|\bB\b|\bUID\b"
)

# Bought items pattern
W_Pattern = re.compile(
   r"\b[A-Z]+[-.!]?\d?[.+!%]?[ ]?[A-Z]*[-.+!]?\d*,?\d*[%]?[ ]?[%]?[A-Z]*[-.+!]?\d*,?\d*[%]?[ ]?[A-Z]*[ ]?[A-Z]*\b"
)

# Items price pattern
D_Pattern = re.compile(r"[-]?\d{1,2},\d{2}[ ]*[AB]")

# Sorting text file
Words = W_Pattern.findall(Text)
Digits = D_Pattern.findall(Text)
Digits_filt = []
Words_filt = []
for w in Words:
    if not Com_words.match(w):
        Words_filt.append(w)
for d in Digits:
    d = float(d.strip(" ABEUR").replace(",", "."))
    Digits_filt.append(d)

# Dataframe Building
df_items = pd.DataFrame(Words_filt, columns=["Items"])
df_items["Price"] = pd.DataFrame(Digits_filt)

# Filename spacing
print("\n", File, "\n", df_items, "\n")
print("Item Count : ", (df_items.index.max() + 1))
print("Average item price : ", round(df_items["Price"].mean(), 2))

# Seaborn Horizontal bar chart
df_items = df_items.sort_values(by=["Price"], ascending=False).reset_index()

sns.set_theme(style="whitegrid")
fig, ax1 = plt.subplots(figsize=[8, 6], constrained_layout=True)
g = sns.barplot(
    y="Items", x="Price", color="#CC071E", data=df_items, orient="h", ax=ax1
)
ax1.set(title=File, xlabel="Price (€)", ylabel="Item")
for index, row in df_items.iterrows():
    if row.Price > 0:
        g.text(
            row.Price - 0.05,
            row.name,
            df_items.loc[index, "Price"],
            color="white",
            ha="right",
            va="center",
        )
    else:
        g.text(
            row.Price + 0.35,
            row.name,
            df_items.loc[index, "Price"],
            color="white",
            ha="right",
            va="center",
        )
plt.show()
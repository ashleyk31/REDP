import pandas as pd
pd.set_option("display.max_colwidth", None)
df = pd.read_csv("../result_files/ballot_analysis.csv")

# format data
# print(df["debate"])
# print(df.columns)
conversation = df["debate"]
split_list = conversation.iloc[0].split("<br><br>")
df_split = pd.DataFrame([split_list])
# print(df_split)

df_transpose = df_split.T
# print(df_transpose.shape)
# print(df_transpose)

# new dataframe for the conversation only
df_conversation = pd.DataFrame({
    "Voter 1 [FOR]": df_transpose.iloc[::2, 0].reset_index(drop=True),
    "Voter 2 [AGAINST]": df_transpose.iloc[1::2, 0].reset_index(drop=True)
})


df_conversation["Voter 1 [FOR]"] = df_conversation["Voter 1 [FOR]"].str.split(": ", n=1).str[1]
df_conversation["Voter 2 [AGAINST]"] = df_conversation["Voter 2 [AGAINST]"].str.split(": ", n=1).str[1]


print(df_conversation)
html_string = """
<html>
<head>
<style>
body { font-family: Arial, sans-serif; }
h2 { font-size: 2em; } 
table { width: 80%; border-collapse: collapse; margin: 20px auto; }
th { padding: 20px; text-align: center; font-size: 1em; }
th.voter1 { text-align: left; }
th.voter2 { text-align: right; }
td { width: 50%; vertical-align: top; padding: 20px; word-wrap: break-word; font-size: 0.6em; gap: 10px; }
td.voter1 { background-color: #e6f7ff; text-align: left; border-radius: 15px; }
td.voter2 { background-color: #e8ffc6; text-align: right; border-radius: 15px; }

/* Responsive font sizing */
@media (max-width: 768px) {
  th, td {
    font-size: 0.8em;
  }
}
@media (min-width: 769px) {
  th, td {
    font-size: 1.3em;
  }
}
</style>
</head>
<body>
<h2 style="text-align:center;">Voter Debate</h2>
<table>
<tr><th class='voter1'>Voter 1 [FOR]</th><th class='voter2'>Voter 2 [AGAINST]</th></tr>
"""


# loop through the conversation
for idx, row in df_conversation.iterrows():
    # Voter 1
    html_string += f"<tr><td class='voter1'>{row['Voter 1 [FOR]']}</td><td></td></tr>\n"

    # Voter 2
    html_string += f"<tr><td></td><td class='voter2'>{row['Voter 2 [AGAINST]']}</td></tr>\n"

html_string += """
</table>
</body>
</html>
"""


# write file
with open("conversation.html", "w") as f:
    f.write(html_string)

print("HTML file created: conversation.html")
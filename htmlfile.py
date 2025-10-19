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
body {
  font-family: Arial, sans-serif;
  font-size: clamp(14px, 1vw + 0.4rem, 18px);
  margin: 30px;
  background-color: #fafafa;
}

h2 {
  text-align: center;
  font-size: clamp(24px, 3vw + 0.5rem, 36px);
}

/* Container for the entire debate */
.debate {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-top: 20px;
}

/* Each message bubble */
.message {
  display: flex;
  max-width: 60%;
  padding: 12px 18px;
  border-radius: 15px;
  word-wrap: break-word;
  font-size: clamp(13px, 1vw + 0.3rem, 16px);
}

/* Voter 1: aligned left */
.voter1 {
  background-color: #e6f7ff;
  align-self: flex-start;
  text-align: left;
}

/* Voter 2: aligned right */
.voter2 {
  background-color: #e8ffc6;
  align-self: flex-end;
  text-align: right;
}

/* Responsive font tweaks */
@media (max-width: 768px) {
  body { font-size: 1.3em; }
  .message { max-width: 100%; }
}
</style>
</head>
<body>
<h2>Voter Debate</h2>
<div class="debate">
"""


# Loop through conversation rows
# Loop through conversation rows
for idx, row in df_conversation.iterrows():
    if pd.notna(row['Voter 1 [FOR]']):
        html_string += f"<div class='message voter1'>{row['Voter 1 [FOR]']}</div>\n"
    if pd.notna(row['Voter 2 [AGAINST]']):
        html_string += f"<div class='message voter2'>{row['Voter 2 [AGAINST]']}</div>\n"

html_string += """
</div>
</body>
</html>
"""



# write file
with open("conversation.html", "w") as f:
    f.write(html_string)

print("HTML file created: conversation.html")
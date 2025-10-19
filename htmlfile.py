import pandas as pd
pd.set_option("display.max_colwidth", None)
df = pd.read_csv("../result_files/ballot_analysis.csv")

# format data
conversation = df["debate"]
split_list = conversation.iloc[0].split("<br><br>")
df_split = pd.DataFrame([split_list])
df_transpose = df_split.T

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
<meta charset="UTF-8">
<style>
body {
  font-family: Arial, sans-serif;
  font-size: clamp(12px, 1.5vw + 0.4rem, 22px);
  margin: 20px;
  background-color: #fafafa;
}

h2 {
  text-align: center;
  font-size: clamp(20px, 3vw + 0.5rem, 40px);
}

.debate {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-top: 20px;
}

.message {
  display: inline-block;
  position: relative;
  max-width: 70%;
  padding: 14px 18px;
  border-radius: 20px;
  font-size: clamp(13px, 1vw + 0.3rem, 16px);
  word-wrap: break-word;
  margin: 8px 0;
  border: 2px solid #b7c2cc; 
}

/* Left bubble (Voter 1) */
.voter1 {
  background-color: #e8ffc6;
  align-self: flex-start;
  text-align: left;
}

/* Border layer for tail */
.voter1::before {
  content: "";
  position: absolute;
  bottom: 0;
  left: 25px;
  width: 0;
  height: 0;
  border: 13px solid transparent;
  border-top-color: #b7c2cc;
  border-bottom: 0;
  border-left: 0;
  margin-bottom: -13px;
}

/* Fill layer for tail */
.voter1::after {
  content: "";
  position: absolute;
  bottom: 2px; /* slightly higher to show border below */
  left: 27px;  /* offset inward so the border shows */
  width: 0;
  height: 0;
  border: 11px solid transparent;
  border-top-color: #e8ffc6;
  border-bottom: 0;
  border-left: 0;
  margin-bottom: -11px;
}

/* Right bubble (Voter 2) */
.voter2 {
  background-color: #ffc6c6;
  align-self: flex-end;
  text-align: right;
}

/* Border layer for tail */
.voter2::before {
  content: "";
  position: absolute;
  bottom: 0;
  right: 25px;
  width: 0;
  height: 0;
  border: 13px solid transparent;
  border-top-color: #b7c2cc;
  border-bottom: 0;
  border-right: 0;
  margin-bottom: -13px;
}

/* Fill layer for tail */
.voter2::after {
  content: "";
  position: absolute;
  bottom: 2px;
  right: 27px;
  width: 0;
  height: 0;
  border: 11px solid transparent;
  border-top-color: #ffc6c6; /* bubble color */
  border-bottom: 0;
  border-right: 0;
  margin-bottom: -11px;
}


/* Mobile view adjustments */
@media (max-width: 768px) {
  body { font-size: 1.3em; }
  .message { max-width: 80%; }
}

</style>
</head>
<body>
<h2>Voter Debate</h2>
<div class="debate">
"""



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
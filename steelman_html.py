import pandas as pd
pd.set_option("display.max_colwidth", None)
df = pd.read_csv("../result_files/ballot_analysis.csv")

# format data for steelman for
steelman_for = df["steelman_for"]
split_list_for = steelman_for.iloc[0].split("<br><br>")
df_split_for = pd.DataFrame([split_list_for])
df_transpose_for = df_split_for.T

# new dataframe for the conversation only
df_conversation_for = pd.DataFrame({
    "PRO ARGUMENT": df_transpose_for.iloc[::2, 0].reset_index(drop=True),
    "PRO COUNTER ARGUMENT": df_transpose_for.iloc[1::2, 0].reset_index(drop=True)
})

df_conversation_for["PRO ARGUMENT"] = df_conversation_for["PRO ARGUMENT"].str.split(": ", n=1).str[1]
df_conversation_for["PRO COUNTER ARGUMENT"] = df_conversation_for["PRO COUNTER ARGUMENT"].str.split(": ", n=1).str[1]

# format data for steelman against
steelman_against = df["steelman_against"]
split_list_against = steelman_against.iloc[0].split("<br><br>")
df_split_against = pd.DataFrame([split_list_against])
df_transpose_against = df_split_against.T

# new dataframe for the conversation only
df_conversation_against = pd.DataFrame({
    "PRO ARGUMENT": df_transpose_against.iloc[::2, 0].reset_index(drop=True),
    "PRO COUNTER ARGUMENT": df_transpose_against.iloc[1::2, 0].reset_index(drop=True)
})

df_conversation_against["PRO ARGUMENT"] = df_conversation_against["PRO ARGUMENT"].str.split(": ", n=1).str[1]
df_conversation_against["PRO COUNTER ARGUMENT"] = df_conversation_against["PRO COUNTER ARGUMENT"].str.split(": ", n=1).str[1]



print(df_conversation_against)
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
  margin-bottom: 10px;
}

h3 {
  text-align: center;
  font-size: clamp(16px, 2vw + 0.3rem, 24px);
  margin-bottom: 12px;
}

.steelman {
  display: flex;
  gap: 20px;
  margin-top: 20px;
}

/* Left and right columns */
.column {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

/* Argument + counter block */
.block {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  gap: 6px;
  padding: 12px;
  border: 2px solid #b7c2cc;  
  border-radius: 16px;
  background-color: #f5f5f5;  
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
  justify-content: center;
}

.bubble-label {
  font-weight: bold;
  margin-bottom: 4px;
  font-size: clamp(12px, 1vw + 0.3rem, 14px);
}

/* Right-aligned labels for AGAINST bubbles */
.bubble-label.right {
  text-align: right;
}

/* Message bubbles */
.message {
  padding: 10px 14px;
  border-radius: 12px;
  font-size: clamp(13px, 1vw + 0.3rem, 16px);
  word-wrap: break-word;
  border: 1px solid #b7c2cc;
}

/* PRO side */
.pro { background-color: #e8ffc6; }
.p_counter { background-color: #b7e4c7; }

/* AGAINST side */
.against { background-color: #ffc6c6; }
.a_counter { background-color: #ff9999; }

/* Mobile adjustments */
@media (max-width: 768px) {
  .steelman { flex-direction: column; }
}
</style>
</head>
<body>
<h2>Voter Debate</h2>
<div class="steelman">

<div class="column">
<h3>Steelman For</h3>
"""

# Left column: PRO argument + counter
pro_count = 1
for idx, row in df_conversation_for.iterrows():
    html_string += "<div class='block'>\n"

    # PRO argument label + bubble
    if pd.notna(row['PRO ARGUMENT']):
        html_string += f"<div class='bubble-label'>Argument {pro_count}</div>\n"
        html_string += f"<div class='message pro'>{row['PRO ARGUMENT']}</div>\n"

    # PRO counter label + bubble
    if pd.notna(row['PRO COUNTER ARGUMENT']):
        html_string += f"<div class='bubble-label'>Counter {pro_count}</div>\n"
        html_string += f"<div class='message pro p_counter'>{row['PRO COUNTER ARGUMENT']}</div>\n"

    html_string += "</div>\n"
    pro_count += 1

html_string += "</div>\n<div class='column'>\n<h3>Steelman Against</h3>\n"

# Right column: AGAINST argument + counter
con_count = 1
for idx, row in df_conversation_against.iterrows():
    html_string += "<div class='block'>\n"

    # AGAINST argument label + bubble (right-aligned)
    if pd.notna(row['PRO ARGUMENT']):
        html_string += f"<div class='bubble-label right'>Argument {con_count}</div>\n"
        html_string += f"<div class='message against'>{row['PRO ARGUMENT']}</div>\n"

    # AGAINST counter label + bubble (right-aligned)
    if pd.notna(row['PRO COUNTER ARGUMENT']):
        html_string += f"<div class='bubble-label right'>Counter {con_count}</div>\n"
        html_string += f"<div class='message against a_counter'>{row['PRO COUNTER ARGUMENT']}</div>\n"

    html_string += "</div>\n"
    con_count += 1

html_string += """
</div>
</div>
</body>
</html>
"""

# write file
with open("steelman_conversation.html", "w") as f:
    f.write(html_string)

print("HTML file created: steelman_conversation.html")
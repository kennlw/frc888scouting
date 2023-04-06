import pandas as pd
import streamlit as st

def convert_to_export_url(url):
    return url.replace("edit#gid","export?format=csv&gid")
def download_sheet(url):
    sheet_url = convert_to_export_url(url)
    df = pd.read_csv(sheet_url)
    df.to_csv('Prematch Data.csv')

#user input
sheet_url_input = st.text_input("Google Sheet URL:")
tn = st.text_input("Input Team #: ")

if sheet_url_input != '' and tn != '':
    download_sheet(sheet_url_input)
    df = pd.read_csv('Prematch Data.csv', index_col="Team") # use Prematch Data.csv

    x = df.loc[int(tn)]

    # Auto
    st.write(f"Team *{tn}* starts auto *", end="")

    pos_dict = {
        "left":float(x["Start position Left %"].replace("%", "")),
        "center":float(x["Start position Center %"].replace("%", "")),
        "right":float(x["Start position Right %"].replace("%", ""))
    }

    pos_maxes = [key for key, value in pos_dict.items() if value == max(pos_dict.values())]
    if len(pos_maxes) == 1:
        st.write(pos_maxes[0], end = " ")
    else:
        for i in pos_maxes:
            st.write(i, end = ", ")

    st.write("*of the charge station. ", end="")

    als = ["Low", "Mid", "High"]
    c = 3
    st.write("On average, ", end="")
    try:
        for i in als:
            if int(x[f"Avg # of Pieces {i} Auto"]) != 0:
                st.write(f"they place *" + str(x[f"Avg # of Pieces {i} Auto"]) + f"* pieces on the *{i}* node", end="; ")
                c -= 1
        if c == 3:
            st.write("No pieces in Auto", end="")
    except ValueError:
        st.write("NaN, ", end="")

    auto_dict = {
        "*mobility*":float(x["AUTO % Mobility"].replace("%", "")),
        "*dock*":float(x["AUTO % Dock"].replace("%", "")),
        "*engage*":float(x["AUTO % Engage"].replace("%", "")),
        "*mobility + dock*":float(x["AUTO % Mob + Dock"].replace("%", "")),
        "*mobility + engage*":float(x["AUTO % Mob + Engage"].replace("%", "")),
    }

    st.write("then they get " + str(max(auto_dict, key = auto_dict.get)) + ".")

    # teleop
    try:
        st.write("\n\nThey score *" + str(x["Avg # Game Pieces"]) + "* pieces in teleop, mainly going for ", end="")
    except ValueError:
        st.write("\n\nTeleop: NaN Error")

    teleop_dict = {
        "Low":float(x["Avg Low # Cones"]) + float(x["Avg Low # Cubes"]),
        "Mid":float(x["Avg Mid # Cones"]) + float(x["Avg Mid # Cubes"]),
        "High":float(x["Avg High # Cones"]) + float(x["Avg High # Cubes"])
    }

    teleop_maxes = [key for key, value in teleop_dict.items() if value == max(teleop_dict.values())]
    if len(teleop_maxes)==1:
        st.write("*"+teleop_maxes[0]+"*")
    else:
        for i in teleop_maxes:
            st.write(f"*{i}*", end=", ")

    cc = { 
        "Cones":float(x["Avg High # Cones"])+float(x["Avg Mid # Cones"])+float(x["Avg Low # Cones"]),
        "Cubes":float(x["Avg High # Cubes"])+float(x["Avg Mid # Cubes"])+float(x["Avg Low # Cubes"])
    }

    if cc["Cones"]!=cc["Cubes"]:
        st.write("and prefering to score *" + str(max(cc, key = cc.get)) + "*.")
    else:
        st.write("and prefering to score *Both*.")

    # defense?
    try:
        st.write("\nThey are known to *play defense*, ", end = "") if float(x["Defense Performance"]) > 5.0 else st.write("They are known to *not play defense*, ", end="")
    except ValueError:
        st.write("\nDefense: NaN Error")

    #drivebase
    st.write("with a *" + x["Drive Train"] + "* drivebase.")
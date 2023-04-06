import pandas as pd

df = pd.read_csv("Prematch Data.csv", index_col="Team")

tn = int(input("Input Team #: "))

x = df.loc[int(tn)]

# Auto
print(f"Team *{tn}* starts auto *", end="")

pos_dict = {
    "left":float(x["Start position Left %"].replace("%", "")),
    "center":float(x["Start position Center %"].replace("%", "")),
    "right":float(x["Start position Right %"].replace("%", ""))
}

pos_maxes = [key for key, value in pos_dict.items() if value == max(pos_dict.values())]
if len(pos_maxes) == 1:
    print(pos_maxes[0], end = " ")
else:
    for i in pos_maxes:
        print(i, end = ", ")

print("*of the charge station. ", end="")

als = ["Low", "Mid", "High"]
c = 3
print("On average, ", end="")
try:
    for i in als:
        if int(x[f"Avg # of Pieces {i} Auto"]) != 0:
            print(f"they place *" + str(x[f"Avg # of Pieces {i} Auto"]) + f"* pieces on the *{i}* node", end="; ")
            c -= 1
    if c == 3:
        print("No pieces in Auto", end="")
except ValueError:
    print("NaN, ", end="")

auto_dict = {
    "*mobility*":float(x["AUTO % Mobility"].replace("%", "")),
    "*dock*":float(x["AUTO % Dock"].replace("%", "")),
    "*engage*":float(x["AUTO % Engage"].replace("%", "")),
    "*mobility + dock*":float(x["AUTO % Mob + Dock"].replace("%", "")),
    "*mobility + engage*":float(x["AUTO % Mob + Engage"].replace("%", "")),
}

print("then they get " + str(max(auto_dict, key = auto_dict.get)) + ".")

# teleop
try:
    print("\n\nThey score *" + str(x["Avg # Game Pieces"]) + "* pieces in teleop, mainly going for ", end="")
except ValueError:
    print("\n\nTeleop: NaN Error")

teleop_dict = {
    "Low":float(x["Avg Low # Cones"]) + float(x["Avg Low # Cubes"]),
    "Mid":float(x["Avg Mid # Cones"]) + float(x["Avg Mid # Cubes"]),
    "High":float(x["Avg High # Cones"]) + float(x["Avg High # Cubes"])
}

teleop_maxes = [key for key, value in teleop_dict.items() if value == max(teleop_dict.values())]
if len(teleop_maxes)==1:
    print("*"+teleop_maxes[0]+"*")
else:
    for i in teleop_maxes:
        print(f"*{i}*", end=", ")

cc = { 
    "Cones":float(x["Avg High # Cones"])+float(x["Avg Mid # Cones"])+float(x["Avg Low # Cones"]),
    "Cubes":float(x["Avg High # Cubes"])+float(x["Avg Mid # Cubes"])+float(x["Avg Low # Cubes"])
}

if cc["Cones"]!=cc["Cubes"]:
    print("and prefering to score *" + str(max(cc, key = cc.get)) + "*.")
else:
    print("and prefering to score *Both*.")

# defense?
try:
    print("\nThey are known to *play defense*, ", end = "") if float(x["Defense Performance"]) > 5.0 else print("They are known to *not play defense*, ", end="")
except ValueError:
    print("\nDefense: NaN Error")

#drivebase
print("with a *" + x["Drive Train"] + "* drivebase.")
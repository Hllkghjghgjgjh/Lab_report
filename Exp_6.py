import numpy as np
import matplotlib.pyplot as plt
import json




# Constants

C0= 364 # in pF
C2= 1000 # in pF
R3= 3 # in kohms


# Formulas Used

def C1_(R4):
    R4=float(R4)
    return (C2 * R4)/R3

def R1_(C4):
    C4=float(C4)
    return (R3 * C4)/C2

def E_(C1):
    C1=float(C1)
    return C1/C0

def Tan_(f,C1,R1):
    R1=float(R1)
    C1=float(C1)
    f=float(f)
    return 2*(np.pi)*float(f)*C1*R1


# Frequency Dependence
with open("Exp_6_data_1.json", "r") as f:
    d1 = json.load(f)

## For BaTiO3


DC=[]
DF=[]
F=[]

for f in d1["BaTiO3"]:
    F.append(float(f))
    C4=d1["BaTiO3"][f]["C4"]
    R4=d1["BaTiO3"][f]["R4"]
    C1= C1_(R4)
    R1= R1_(C4)
    E= E_(C1)

    DC.append(float(E))
    Tan= Tan_(f,C1,R1)
    DF.append(float(Tan))

    d1["BaTiO3"][f]["C1"]=C1
    d1["BaTiO3"][f]["R1"]=R1
    d1["BaTiO3"][f]["E"]=E
    d1["BaTiO3"][f]["Tan(d)"]=Tan

with open("Exp_6_data_1.json", "w") as f:
    json.dump(d1, f, indent=2)


### Plots of BaTiO3

plt.plot(F,DC,marker='o')
plt.xlabel("Frequency in kHz")
plt.ylabel("Dielectric Constant of BaTiO3")
plt.grid(True)
plt.title("Fig-2: Dielectric Constant of BaTiO3 Vs Frequency (in kHz)")
plt.savefig("Fig-2_Dielectric Constant of BaTiO3 Vs Frequency (in kHz)")
plt.close()






## For MLCC

C=[]
F=[]

for f in d1["MLCC"]:
    F.append(float(f))
    C.append(float(d1["MLCC"][f]["C1"]))



### Plots of MLCC

plt.figure(figsize=(8, 6))
plt.plot(F,C,marker='o')
plt.xlabel("Frequency in kHz")
plt.ylabel("Capcitance in pF")
plt.grid(True)
plt.title("Fig-3: Capcitance Vs Frequency for MLCC")
plt.savefig("Fig-3_Capcitance Vs Frequency (in kHz) for MLCC.png")
plt.close()


## For Disc-Ceramic capcitor

C=[]
F=[]

for f in d1["ceramic"]:
    F.append(float(f))
    C.append(float(d1["ceramic"][f]["C1"]))


### Plots of ceramic

plt.figure(figsize=(8, 6))
plt.plot(F,C,marker='o')
plt.xlabel("Frequency in kHz")
plt.ylabel("Capcitance in pF")
plt.grid(True)
plt.title("Fig-4: Capcitance Vs Frequency for Disc-Ceramic capacitor")
plt.savefig("Fig-4_Capcitance Vs Frequency (in kHz) for Disc-Ceramic capacitor.png")
plt.close()





# For Temperature dependence of Dieclctic constant of BaTiO3


with open("Exp_6_data_2.json", "r") as f:
    d2 = json.load(f)



for temp in d2:
    for f in d2[temp]:
        C4=d2[temp][f]["C4"]
        R4=d2[temp][f]["R4"]
        C1= C1_(R4)
        E= E_(C1)

        d2[temp][f]["C1"]=C1
        d2[temp][f]["E"]=E

with open("Exp_6_data_2.json", "w") as f:
    json.dump(d2, f, indent=2)

## Plot of temperatue vs dilectric constant at different frequencies

T=[]
F=[]

for temp in d2:
    T.append(int(temp))



plt.figure(figsize=(10, 6))

for f in d2[str(T[0])]:
    F.append(float(f))
    E_f=[]

    for temp in d2:
        E_f.append(d2[temp][f]["E"])
    
    plt.plot(T,E_f,marker='o', label=str(f"{f} kHz"))

    
plt.xlabel("Temperature (in C)")
plt.xticks(T)
plt.ylabel("Dielectric Constant")
plt.title("Fig-5: Dielectric Vs Temperature for BaTiO3")
plt.grid(True)
plt.legend()
plt.savefig("Fig-5_Dielectric Vs Temperature for BaTiO3.png")
plt.close()


import numpy as np
import matplotlib.pyplot as plt

# ===============================
# Diffuseness parameter (δ)
# ===============================

# --- INPUTS (as per manual page 16) ---
Tc = 130          # Curie temperature in °C (from dielectric peak)
freq = "5"        # choose ONE frequency in kHz (e.g. "5", "15", "25", "35")

# --- Extract temperature and dielectric constant ---
T = []
E = []

for temp in d2:
    if float(temp) > Tc:                  # paraelectric phase only
        T.append(float(temp))
        E.append(d2[temp][f]["E"])

T = np.array(T)
E = np.array(E)

# --- ε_max at Tc ---
E_max = max([d2[str(Tc)][f]["E"] for f in d2[str(Tc)]])

# --- Log variables (manual definition) ---
x = np.log(T - Tc)
y = np.log((1/E) - (1/E_max))

# --- Linear fit ---
coeff = np.polyfit(x, y, 1)
delta = coeff[0]

# --- Plot ---
plt.figure(figsize=(8, 6))
plt.scatter(x, y, label="Experimental data")
plt.plot(x, np.polyval(coeff, x), 'r--',
         label=f"Fit: slope δ = {delta:.4f}")

plt.xlabel(r"$\ln(T - T_c)$")
plt.ylabel(r"$\ln\left(\frac{1}{\varepsilon} - \frac{1}{\varepsilon_{max}}\right)$")
plt.title("Fig-6: Diffuseness Parameter Plot (BaTiO$_3$)")
plt.grid(True)
plt.legend()

plt.savefig("Fig-6_Diffuseness_Parameter.png")
plt.close()

print(f"Diffuseness parameter δ = {delta:.4f}")

"""
Result: Diffuseness parameter δ = 0.2682

"""

#Originally coded in Jupyter Notebooks
%matplotlib inline

# Dependencies and Setup
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy import stats
import random

# Hide warning messages in notebook
import warnings
warnings.filterwarnings('ignore')

# File to Load (Remember to Change These)
mouse_drug_data_to_load = "data/mouse_drug_data.csv"
clinical_trial_data_to_load = "data/clinicaltrial_data.csv"

# Read the Mouse and Drug Data and the Clinical Trial Data
mouse_df = pd.read_csv(mouse_drug_data_to_load)
clinical_df = pd.read_csv(clinical_trial_data_to_load)

# Combine the data into a single dataset
combined_df = pd.merge(mouse_df, clinical_df, on='Mouse ID', how='outer')

# Display the data table for preview
combined_df.head()

combined_df.describe()

# Store the Mean Tumor Volume Data Grouped by Drug and Timepoint
grouped_df_mean = combined_df.groupby(['Drug', 'Timepoint']).mean()
# Convert to DataFrame
mean_tumor_volume_df = pd.DataFrame(grouped_df_mean)
# Preview DataFrame
mean_tumor_volume_df.head()

mean_tumor_vol_df = pd.pivot_table(combined_df, index = ["Timepoint"], columns =['Drug'],
                                   values = "Tumor Volume (mm3)", aggfunc = np.mean)
mean_tumor_vol_df

# Store the Standard Error of Tumor Volumes Grouped by Drug and Timepoint
sem_calculation = {"Tumor Volume (mm3)": stats.sem, "Metastatic Sites": stats.sem}
grouped_df_sem = combined_df.groupby(["Drug", "Timepoint"]).agg(sem_calculation)
# Convert to DataFrame
sem_tumor_volume = pd.DataFrame(grouped_df_sem)
# Preview DataFrame
sem_tumor_volume.head()

sem_tumor_vol_df = pd.pivot_table(combined_df, index = ["Timepoint"], columns =['Drug'],
                                  values = "Tumor Volume (mm3)", aggfunc = stats.sem)
sem_tumor_vol_df


# Generate the Plot (with Error Bars)
x_axis = [mean_tumor_vol_df[num].index.tolist() for num in mean_tumor_vol_df.columns]
y_axis = [mean_tumor_vol_df[num].tolist() for num in mean_tumor_vol_df.columns]
s_error = [sem_tumor_vol_df[num].tolist() for num in sem_tumor_vol_df.columns]


plt.figure(figsize=(15,10))
markers = ["o", "v", "s","d",".","^","<",">","8"]
for num in range(len(s_error)):
    plt.errorbar(x_axis[num], y_axis[num], yerr = s_error[num],
                 marker = random.choice(markers),
                 linestyle = "--",
                 markersize='6', linewidth = 1)
plt.grid(True)
plt.xlabel("Time (Days)", fontsize = 12)
plt.ylabel("Tumor Volume (mm3)", fontsize = 12)
plt.title("Tumor Response to Treatment", fontsize = 14)
plt.legend(("Capomulin","Ceftamin","Infubinol","Ketapril","Naftisol","Placebo","Propriva","Ramicane	Stelasyn","Zoniferol"),loc="upper left")

# Save the Figure
#plt.savefig("../Images/tumnor_response_to_treatment.png")

plt.show()

# Store the Mean Met. Site Data Grouped by Drug and Timepoint
metastic_response_mean = pd.pivot_table(combined_df, index = ["Timepoint"], columns =["Drug"],
                                        values = "Metastatic Sites", aggfunc = np.mean)

# Preview DataFrame
metastic_response_mean

# Store the SEM Met. Site Data Grouped by Drug and Timepoint
metastic_response_sem = pd.pivot_table(combined_df, index = ['Timepoint'], columns =['Drug'],
                                       values = 'Metastatic Sites', aggfunc = stats.sem)
metastic_response_sem

# Generate the Plot (with Error Bars)
metastic_x_axis = [metastic_response_mean[num].index.tolist() for num in metastic_response_mean.columns]
metastic_y_axis = [metastic_response_mean[num].tolist() for num in metastic_response_mean.columns]
metastic_s_error = [metastic_response_sem[num].tolist() for num in metastic_response_sem.columns]

plt.figure(figsize=(15,10))
markers = ["o", "v", "s","d",".","^","<",">","8"]
for num in range(len(s_error)):
    plt.errorbar(metastic_x_axis[num], metastic_y_axis[num], yerr = metastic_s_error[num],
                 marker = random.choice(markers),
                 linestyle = "--",
                 markersize='6', linewidth = 1)
plt.grid(True)
plt.xlabel("Treatment Duration (Days)", fontsize = 12)
plt.ylabel("Met. Sites", fontsize = 12)
plt.title("Metastic Spread During Treatment", fontsize = 14)
plt.legend(("Capomulin","Ceftamin","Infubinol","Ketapril","Naftisol","Placebo","Propriva","Ramicane	Stelasyn","Zoniferol"),loc="upper left")

# Save the Figure
#plt.savefig("../Images/metastic_spread_during_treatment.png")

plt.show()

# Store the Count of Mice Grouped by Drug and Timepoint (W can pass any metric)
survival_rate_df = pd.pivot_table(combined_df, index = ['Timepoint'],columns =['Drug'], values = 'Metastatic Sites',
                               aggfunc='count')

# Preview DataFrame
survival_rate_df

survival_rate_df.describe()

# Generate the Plot (Accounting for percentages)
survival_x_axis = [survival_rate_df[num].index.tolist() for num in survival_rate_df.columns]
survival_y_axis = [survival_rate_df[num].tolist() for num in survival_rate_df.columns]
survival_pct = [[(num_j/max(num_i) * 100) for num_j in num_i] for num_i in survival_y_axis]

plt.figure(figsize=(15,10))
markers = ["o", "v", "s","d",".","^","<",">","8"]
for num in range(len(s_error)):
    plt.errorbar(survival_x_axis[num], survival_pct[num],
                 marker = random.choice(markers),
                 linestyle = "--",
                 markersize='6', linewidth = 1)
plt.grid(True)
plt.xlabel("Time (Days)", fontsize = 12)
plt.ylabel("Survival Rate (%)", fontsize = 12)
plt.title("Surviving During Treatment", fontsize = 14)
plt.legend(("Capomulin","Ceftamin","Infubinol","Ketapril","Naftisol","Placebo","Propriva","Ramicane	Stelasyn","Zoniferol"),loc="lower left")
plt.xlim(-5, 50, 5)
plt.ylim(0, 110, 5)
plt.show()

# Save the Figure
plt.savefig("../Images/survival_rate.png")
# Show the Figure
plt.show()


summary_x = [mean_tumor_vol_df[num].index.tolist() for num in mean_tumor_vol_df.columns]
mean_y = [mean_tumor_vol_df[num].tolist() for num in mean_tumor_vol_df.columns]
mean_vol_y_pct = [[(num_j/max(num_i) * 100) for num_j in num_i] for num_i in mean_y]
vol_pct = [((mean_vol_y_pct[i][9] - mean_vol_y_pct[i][0]) / mean_vol_y_pct[i][0]) * 100 for i in range(10)]

plt.figure(figsize=(15,10))
bars = mean_tumor_vol_df.columns.tolist()
y_axis = np.arange(len(bars))

summary = plt.bar(y_axis, vol_pct)
summary[0].set_color("g")
summary[1].set_color("r")
summary[2].set_color("r")
summary[3].set_color("r")
summary[4].set_color("r")
summary[5].set_color("r")
summary[6].set_color("r")
summary[7].set_color("g")
summary[8].set_color("r")
summary[9].set_color("r")
plt.xticks(y_axis, bars, rotation='vertical', fontsize=14)
plt.ylabel("% Tumor Volume Change", fontsize=14)
plt.title("Tumor Change Over 45 Day Treatment", fontsize=14)
plt.grid(True)


# Save the Figure
plt.savefig("../Images/tumor_change.png")
# Show the Figure
plt.show()
plt.tight_layout()

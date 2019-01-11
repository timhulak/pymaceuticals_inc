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

mean_tumor_vol_df = pd.pivot_table(combined_df, index = ["Timepoint"],
                               columns =['Drug'], values = "Tumor Volume (mm3)",
                               aggfunc = np.mean)
mean_tumor_vol_df

# Store the Standard Error of Tumor Volumes Grouped by Drug and Timepoint
sem_calculation = {"Tumor Volume (mm3)": stats.sem, "Metastatic Sites": stats.sem}
grouped_df_sem = combined_df.groupby(["Drug", "Timepoint"]).agg(sem_calculation)
# Convert to DataFrame
sem_tumor_volume = pd.DataFrame(grouped_df_sem)
# Preview DataFrame
sem_tumor_volume.head()

sem_tumor_vol_df = pd.pivot_table(combined_df, index = ["Timepoint"],
                               columns =['Drug'], values = "Tumor Volume (mm3)",
                               aggfunc = stats.sem)
sem_tumor_vol_df

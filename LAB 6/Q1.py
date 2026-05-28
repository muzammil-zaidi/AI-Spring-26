import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import (classification_report, confusion_matrix, accuracy_score, mean_squared_error, r2_score)
from sklearn.utils import resample
import warnings
warnings.filterwarnings('ignore')
import os

FIGURES = r'C:\Users\PMLS\Downloads\figures'
os.makedirs(FIGURES, exist_ok=True)

df = pd.read_csv(r'C:\Users\PMLS\Downloads\bank_data.csv')
df.columns = df.columns.str.strip().str.lower()
df = df.map(lambda x: x.strip() if isinstance(x, str) else x)

print("\n[1] DATA UNDERSTANDING")
print(f"Shape (rows, cols): {df.shape}")
print(f"\nData Types:\n{df.dtypes}")
print(f"\nSummary Statistics:\n{df.describe(include='all').T[['count','mean','std','min','max']].to_string()}")

TARGET_CLASS = 'approved'   
TARGET_REG   = 'approved_loan_amount'
DROP_COLS    = ['user_id', 'address', 'email'] 

numeric_cols     = df.select_dtypes(include=[np.number]).columns.tolist()
categorical_cols = df.select_dtypes(include='object').columns.tolist()

print(f"\n[2] ATTRIBUTE TYPES")
print(f"  Numeric     : {numeric_cols}")
print(f"  Categorical : {categorical_cols}")
print(f"  Target (Cls): {TARGET_CLASS}")
print(f"  Target (Reg): {TARGET_REG}")

print(f"\n[3] MISSING VALUES (before):\n{df.isnull().sum()[df.isnull().sum() > 0]}")

for col in df.columns:
    if col in DROP_COLS + [TARGET_CLASS, TARGET_REG]:
        continue
    if df[col].dtype in [np.float64, np.int64]:
        df[col].fillna(df[col].median(), inplace=True)
    else:
        df[col].fillna(df[col].mode()[0], inplace=True)

print("  Numeric missing values filled with MEDIAN")
print("  Categorical missing values filled with MODE")

print(f"\n[4] INVALID / INCONSISTENT DATA")
for col in ['capital_gain', 'capital_loss']:
    if col in df.columns:
        neg = (df[col] < 0).sum()
        df[col] = df[col].clip(lower=0)
        print(f"  {col}: clipped {neg} negative values to 0")

if 'hours_per_week' in df.columns:
    inv = ((df['hours_per_week'] < 1) | (df['hours_per_week'] > 168)).sum()
    df['hours_per_week'] = df['hours_per_week'].clip(1, 168)
    print(f"  hours_per_week: clipped {inv} out-of-range values")

dupes = df.duplicated().sum()
print(f"\n[5] DUPLICATE ROWS: {dupes} found → removed")
df.drop_duplicates(inplace=True)

df['date_of_birth'] = pd.to_datetime(df['date_of_birth'], errors='coerce')
df['age'] = (pd.Timestamp('today') - df['date_of_birth']).dt.days // 365
df['age'].fillna(df['age'].median(), inplace=True)
df.drop(columns=['date_of_birth'], inplace=True)
print(f"\n[6] date_of_birth → age  |  min={df['age'].min():.0f}  mean={df['age'].mean():.1f}  max={df['age'].max():.0f}")

df.drop(columns=[c for c in DROP_COLS if c in df.columns], inplace=True)

print("\n[7] EDA GRAPHS …")

fig, axes = plt.subplots(2, 3, figsize=(18, 10))
fig.suptitle("EDA – Loan Dataset", fontsize=16, fontweight='bold')

vc = df[TARGET_CLASS].value_counts().sort_index()
axes[0, 0].bar(['Rejected (0)', 'Approved (1)'], vc.values, color=['#e74c3c', '#2ecc71'], edgecolor='white')
axes[0, 0].set_title("Loan Approval Distribution (Bar)")
axes[0, 0].set_ylabel("Count")
for i, v in enumerate(vc.values):
    axes[0, 0].text(i, v + 30, str(v), ha='center', fontweight='bold')

gvc = df['gender'].value_counts()
axes[0, 1].pie(gvc.values, labels=gvc.index, autopct='%1.1f%%',
               colors=['#3498db', '#e91e8c', '#f39c12'], startangle=90)
axes[0, 1].set_title("Gender Distribution (Pie)")

approved_ages  = df[df[TARGET_CLASS] == 1]['age']
rejected_ages  = df[df[TARGET_CLASS] == 0]['age']
axes[0, 2].boxplot([rejected_ages, approved_ages], labels=['Rejected (0)', 'Approved (1)'],
                   patch_artist=True,
                   boxprops=dict(facecolor='#AED6F1'),
                   medianprops=dict(color='red', linewidth=2))
axes[0, 2].set_title("Age by Loan Approval (Boxplot)")
axes[0, 2].set_ylabel("Age")

axes[1, 0].hist(df['hours_per_week'].dropna(), bins=30, color='#9b59b6', edgecolor='white')
axes[1, 0].set_title("Hours Per Week Distribution (Histogram)")
axes[1, 0].set_xlabel("Hours"); axes[1, 0].set_ylabel("Frequency")

samp = df[df[TARGET_REG] > 0].sample(min(500, len(df)), random_state=42)
axes[1, 1].scatter(samp['capital_loss'], samp[TARGET_REG],
                   alpha=0.4, color='#1abc9c', s=15, edgecolors='none')
axes[1, 1].set_title("Capital Loss vs Loan Amount (Scatter)")
axes[1, 1].set_xlabel("Capital Loss"); axes[1, 1].set_ylabel("Approved Loan Amount")

edu = df.groupby('education_level')[TARGET_CLASS].mean().sort_values(ascending=False)
axes[1, 2].barh(edu.index, edu.values, color='#e67e22', edgecolor='white')
axes[1, 2].set_title("Approval Rate by Education (Bar)")
axes[1, 2].set_xlabel("Approval Rate")

plt.tight_layout()
plt.savefig(os.path.join(FIGURES, 'eda.png'), dpi=130, bbox_inches='tight')
plt.close()
print("  eda.png saved  (bar, pie, boxplot, histogram, scatter)")

num_df = df.select_dtypes(include=[np.number])
plt.figure(figsize=(12, 8))
sns.heatmap(num_df.corr(), annot=True, fmt='.2f', cmap='coolwarm',
            center=0, linewidths=0.5, square=True)
plt.title("Correlation Matrix (Pearson)", fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig(os.path.join(FIGURES, 'correlation.png'), dpi=130, bbox_inches='tight')
plt.close()
print("  correlation.png saved")

cat_cols    = df.select_dtypes(include='object').columns.tolist()
cat_cols    = [c for c in cat_cols if c not in [TARGET_CLASS, TARGET_REG]]
binary_cats = [c for c in cat_cols if df[c].nunique() <= 2]
multi_cats  = [c for c in cat_cols if df[c].nunique() > 2]

le = LabelEncoder()
for col in binary_cats:
    df[col] = le.fit_transform(df[col].astype(str))

df = pd.get_dummies(df, columns=multi_cats, drop_first=True)

print(f"\n[9] ENCODING")
print(f"  Label Encoding (binary)  : {binary_cats if binary_cats else 'None'}")
print(f"  One-Hot Encoding (multi) : {multi_cats}")
print(f"  Shape after encoding     : {df.shape}")

feature_cols = [c for c in df.columns if c not in [TARGET_CLASS, TARGET_REG]]
num_feats    = df[feature_cols].select_dtypes(include=[np.number]).columns.tolist()
scaler = MinMaxScaler()
df[num_feats] = scaler.fit_transform(df[num_feats])
print(f"\n[10] NORMALIZATION: Min-Max Scaling applied to {len(num_feats)} numeric features")

df_model = df.dropna(subset=[TARGET_CLASS, TARGET_REG])
X     = df_model[feature_cols]
y_cls = df_model[TARGET_CLASS].astype(int)
y_reg = df_model[TARGET_REG]

X_train, X_test, yc_train, yc_test = train_test_split(
    X, y_cls, test_size=0.2, random_state=42, stratify=y_cls)

print(f"\n  Train size: {len(X_train)} | Test size: {len(X_test)}")

print("\n" + "=" * 60)
print("[11] CLASSIFICATION – IMBALANCED DATASET")
print("=" * 60)
print(f"Class distribution:\n{y_cls.value_counts().to_string()}")

rf_cls = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
rf_cls.fit(X_train, yc_train)
yc_pred = rf_cls.predict(X_test)

acc_imb = accuracy_score(yc_test, yc_pred)
print(f"\nModel        : Random Forest Classifier")
print(f"Accuracy     : {acc_imb:.4f}")
print(f"\nClassification Report:\n{classification_report(yc_test, yc_pred, target_names=['Rejected','Approved'])}")

fig, ax = plt.subplots(figsize=(6, 5))
cm_imb = confusion_matrix(yc_test, yc_pred)
sns.heatmap(cm_imb, annot=True, fmt='d', cmap='Blues',
            xticklabels=['Rejected', 'Approved'],
            yticklabels=['Rejected', 'Approved'], ax=ax,
            linewidths=0.5, linecolor='gray')
ax.set_title(f"Confusion Matrix – Imbalanced Dataset\nAccuracy = {acc_imb:.3f}", fontsize=12)
ax.set_ylabel("Actual"); ax.set_xlabel("Predicted")
plt.tight_layout()
plt.savefig(os.path.join(FIGURES, 'cm_imbalanced.png'), dpi=130, bbox_inches='tight')
plt.close()
print("  cm_imbalanced.png saved")

print("\n[12] REGRESSION – IMBALANCED DATASET")
mask   = y_reg > 0
X_reg  = X[mask]; y_reg_f = y_reg[mask]
Xr_tr, Xr_te, yr_tr, yr_te = train_test_split(X_reg, y_reg_f, test_size=0.2, random_state=42)

rf_reg = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
rf_reg.fit(Xr_tr, yr_tr)
yr_pred  = rf_reg.predict(Xr_te)
rmse_imb = np.sqrt(mean_squared_error(yr_te, yr_pred))
r2_imb   = r2_score(yr_te, yr_pred)

print(f"Model : Random Forest Regressor")
print(f"RMSE  : {rmse_imb:,.0f}")
print(f"R²    : {r2_imb:.4f}")

print("\n" + "=" * 60)
print("[13] CLASSIFICATION – BALANCED DATASET (500 + 500)")
print("=" * 60)

approved_b = resample(df_model[df_model[TARGET_CLASS] == 1],
                      replace=True, n_samples=500, random_state=42)
rejected_b = resample(df_model[df_model[TARGET_CLASS] == 0],
                      replace=False, n_samples=min(500, (df_model[TARGET_CLASS] == 0).sum()),
                      random_state=42)
df_bal = pd.concat([approved_b, rejected_b]).sample(frac=1, random_state=42)

Xb     = df_bal[feature_cols]
yb_cls = df_bal[TARGET_CLASS].astype(int)
yb_reg = df_bal[TARGET_REG]

Xb_tr, Xb_te, ybc_tr, ybc_te = train_test_split(
    Xb, yb_cls, test_size=0.2, random_state=42, stratify=yb_cls)

rf_cls_b = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
rf_cls_b.fit(Xb_tr, ybc_tr)
ybc_pred = rf_cls_b.predict(Xb_te)

acc_bal = accuracy_score(ybc_te, ybc_pred)
print(f"Model        : Random Forest Classifier")
print(f"Accuracy     : {acc_bal:.4f}")
print(f"\nClassification Report:\n{classification_report(ybc_te, ybc_pred, target_names=['Rejected','Approved'])}")

fig, ax = plt.subplots(figsize=(6, 5))
cm_bal = confusion_matrix(ybc_te, ybc_pred)
sns.heatmap(cm_bal, annot=True, fmt='d', cmap='Greens',
            xticklabels=['Rejected', 'Approved'],
            yticklabels=['Rejected', 'Approved'], ax=ax,
            linewidths=0.5, linecolor='gray')
ax.set_title(f"Confusion Matrix – Balanced Dataset\nAccuracy = {acc_bal:.3f}", fontsize=12)
ax.set_ylabel("Actual"); ax.set_xlabel("Predicted")
plt.tight_layout()
plt.savefig(os.path.join(FIGURES, 'cm_balanced.png'), dpi=130, bbox_inches='tight')
plt.close()
print("  cm_balanced.png saved")

print("\n[14] REGRESSION – BALANCED DATASET")
mask_b = yb_reg > 0
Xbr = Xb[mask_b]; ybr = yb_reg[mask_b]
Xbr_tr, Xbr_te, ybr_tr, ybr_te = train_test_split(Xbr, ybr, test_size=0.2, random_state=42)

rf_reg_b = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
rf_reg_b.fit(Xbr_tr, ybr_tr)
ybr_pred = rf_reg_b.predict(Xbr_te)
rmse_bal = np.sqrt(mean_squared_error(ybr_te, ybr_pred))
r2_bal   = r2_score(ybr_te, ybr_pred)

print(f"Model : Random Forest Regressor")
print(f"RMSE  : {rmse_bal:,.0f}")
print(f"R²    : {r2_bal:.4f}")

print("\n" + "=" * 60)
print("[15] MODEL COMPARISON – IMBALANCED vs BALANCED")
print("=" * 60)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle("Model Performance: Imbalanced vs Balanced Dataset", fontsize=14, fontweight='bold')

cls_metrics  = ['Accuracy']
imb_cls_vals = [acc_imb]
bal_cls_vals = [acc_bal]
x = np.arange(len(cls_metrics))
w = 0.3
bars1 = axes[0].bar(x - w/2, imb_cls_vals, w, label='Imbalanced', color='#e74c3c', alpha=0.85)
bars2 = axes[0].bar(x + w/2, bal_cls_vals,  w, label='Balanced',   color='#2ecc71', alpha=0.85)
axes[0].set_ylim(0, 1.15)
axes[0].set_xticks(x); axes[0].set_xticklabels(cls_metrics, fontsize=12)
axes[0].set_title("Classification – Accuracy")
axes[0].legend()
for bar in bars1 + bars2:
    axes[0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                 f'{bar.get_height():.3f}', ha='center', fontsize=11, fontweight='bold')

reg_labels = ['Imbalanced', 'Balanced']
r2_vals    = [r2_imb, r2_bal]
rmse_vals  = [rmse_imb, rmse_bal]
ax2 = axes[1]
color_r2 = ['#e74c3c', '#2ecc71']
b = ax2.bar(reg_labels, r2_vals, color=color_r2, alpha=0.85, width=0.4)
ax2.set_title("Regression – R² Score")
ax2.set_ylabel("R² Score")
ax2.axhline(0, color='black', linewidth=0.8, linestyle='--')
for bar in b:
    ax2.text(bar.get_x() + bar.get_width()/2,
             bar.get_height() + 0.005 if bar.get_height() >= 0 else bar.get_height() - 0.02,
             f'{bar.get_height():.4f}', ha='center', fontsize=11, fontweight='bold')

plt.tight_layout()
plt.savefig(os.path.join(FIGURES, 'comparison.png'), dpi=130, bbox_inches='tight')
plt.close()
print("  → comparison.png saved")

print("\n" + "=" * 60)
print("SUMMARY & BEST MODEL RECOMMENDATION")
print("=" * 60)
print(f"{'Metric':<40} {'Imbalanced':>12} {'Balanced':>12}")
print("-" * 66)
print(f"{'Classification Accuracy':<40} {acc_imb:>12.4f} {acc_bal:>12.4f}")
print(f"{'Regression R² Score':<40} {r2_imb:>12.4f} {r2_bal:>12.4f}")
print(f"{'Regression RMSE':<40} {rmse_imb:>12,.0f} {rmse_bal:>12,.0f}")

print("""
BEST MODEL: Random Forest on Balanced Dataset

REASONS:
  1. Classification: Balanced dataset gives equal precision/recall
     for both classes, avoiding bias toward 'Rejected' majority.
  2. Regression: Positive R² (balanced) vs negative R² (imbalanced)
     shows balanced training significantly improves loan amount prediction.
  3. Strategy: Resampling (oversample minority, undersample majority)
     is a reliable technique when class imbalance is present.

CONCLUSION: Always balance data before training when class imbalance
exists. Evaluate with F1-score and recall, not just accuracy.
""")

print(f"All figures saved to: {FIGURES}")
print("Done.")

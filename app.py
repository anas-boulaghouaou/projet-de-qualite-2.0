import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# ==========================================
# CONFIGURATION DE LA PAGE
# ==========================================
st.set_page_config(
    page_title="QualiControl Pro - Contrôle Qualité",
    page_icon="https://cdn-icons-png.flaticon.com/512/921/921591.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# CSS SUR MESURE & ANIMATIONS
# ==========================================
custom_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    color: #0f172a;
}

.stApp {
    background: #f8fafc;
}

@keyframes slideDown {
    from { opacity: 0; transform: translateY(-20px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(25px); }
    to { opacity: 1; transform: translateY(0); }
}

.app-header {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0284c7 100%);
    padding: 32px 40px;
    border-radius: 20px;
    color: white;
    box-shadow: 0 20px 25px -5px rgba(15, 23, 42, 0.15), 0 8px 10px -6px rgba(15, 23, 42, 0.1);
    display: flex;
    align-items: center;
    gap: 24px;
    margin-bottom: 30px;
    animation: slideDown 0.7s cubic-bezier(0.16, 1, 0.3, 1);
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.app-header-icon {
    width: 64px;
    height: 64px;
    background: rgba(255, 255, 255, 0.1);
    padding: 12px;
    border-radius: 16px;
    backdrop-filter: blur(8px);
    border: 1px solid rgba(255, 255, 255, 0.2);
}

.app-header h1 {
    color: #ffffff !important;
    font-weight: 800;
    letter-spacing: -0.025em;
    font-size: 2rem;
    margin: 0;
}

.app-header p {
    color: #94a3b8;
    margin: 4px 0 0 0;
    font-size: 1rem;
    font-weight: 400;
}

.kpi-card {
    background: #ffffff;
    border-radius: 16px;
    padding: 22px 24px;
    border: 1px solid #e2e8f0;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.03), 0 2px 4px -2px rgba(0, 0, 0, 0.03);
    transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
    animation: fadeInUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) ease-out;
    position: relative;
    overflow: hidden;
}

.kpi-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 4px;
    background: linear-gradient(90deg, #2563eb, #06b6d4);
}

.kpi-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.08), 0 8px 10px -6px rgba(0, 0, 0, 0.04);
    border-color: #cbd5e1;
}

.kpi-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
}

.kpi-title {
    font-size: 0.825rem;
    font-weight: 700;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.kpi-value {
    font-size: 2rem;
    font-weight: 800;
    color: #0f172a;
    letter-spacing: -0.02em;
}

.kpi-icon {
    width: 42px;
    height: 42px;
    padding: 8px;
    background: #f1f5f9;
    border-radius: 12px;
}

.login-card {
    background: #ffffff;
    border-radius: 24px;
    padding: 40px;
    width: 100%;
    max-width: 440px;
    border: 1px solid #e2e8f0;
    box-shadow: 0 25px 50px -12px rgba(15, 23, 42, 0.12);
    text-align: center;
    animation: fadeInUp 0.5s ease-out;
}

.login-icon {
    width: 72px;
    height: 72px;
    margin-bottom: 20px;
    background: #eff6ff;
    padding: 14px;
    border-radius: 20px;
    display: inline-block;
}

.stButton > button {
    border-radius: 12px !important;
    font-weight: 600 !important;
    padding: 12px 24px !important;
    transition: all 0.2s ease !important;
}

.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.25);
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

DATA_FILE = "dataset.csv"

def load_data():
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        df['Date'] = pd.to_datetime(df['Date'])
        return df
    return pd.DataFrame(columns=["ID", "Date", "Ligne_Production", "Produit", "Quantite_Inspectee", "Defauts_Trouves", "Statut", "Inspecteur"])

def save_data(df):
    df_to_save = df.copy()
    if 'Date' in df_to_save.columns:
        df_to_save['Date'] = df_to_save['Date'].dt.strftime('%Y-%m-%d')
    df_to_save.to_csv(DATA_FILE, index=False)

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.3, 1])
    
    with col2:
        st.markdown("""
        <div class="login-card">
            <img src="https://cdn-icons-png.flaticon.com/512/921/921591.png" class="login-icon"/>
            <h2 style="margin: 0 0 8px 0; color: #0f172a; font-weight: 800; font-size: 1.75rem;">QualiControl Pro</h2>
            <p style="color: #64748b; font-size: 0.95rem; margin-bottom: 28px;">Plateforme d'inspection et de contrôle qualité</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form"):
            username = st.text_input("Identifiant", placeholder="admin")
            password = st.text_input("Mot de passe", type="password", placeholder="admin")
            submit = st.form_submit_button("Connexion au Système", use_container_width=True, type="primary")
            
            if submit:
                if username == "admin" and password == "admin":
                    st.session_state.authenticated = True
                    st.success("Connexion réussie.")
                    st.rerun()
                else:
                    st.error("Identifiants invalides.")

else:
    df = load_data()

    with st.sidebar:
        st.markdown("""
        <div style="display: flex; align-items: center; gap: 12px; padding: 10px 0 20px 0;">
            <img src="https://cdn-icons-png.flaticon.com/512/921/921591.png" width="38"/>
            <div>
                <h3 style="margin:0; color: #0f172a; font-weight: 800; font-size: 1.15rem;">QualiControl</h3>
                <span style="color: #64748b; font-size: 0.8rem; font-weight: 500;">Version 2.4 Pro</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        menu = st.radio("NAVIGATION", ["Tableau de Bord", "Saisie & Modification", "Rapports & Exportation"])
        
        st.divider()
        st.markdown("<p style='font-weight: 700; font-size: 0.8rem; color: #64748b; letter-spacing: 0.05em;'>FILTRES D'ANALYSE</p>", unsafe_allow_html=True)
        
        lignes = ["Toutes les Lignes"] + list(df["Ligne_Production"].unique()) if not df.empty else ["Toutes les Lignes"]
        selected_ligne = st.selectbox("Ligne de Production", lignes)
        
        statuts = ["Tous les Statuts"] + list(df["Statut"].unique()) if not df.empty else ["Tous les Statuts"]
        selected_statut = st.selectbox("Statut du Contrôle", statuts)
        
        st.divider()
        if st.button("Déconnexion", use_container_width=True):
            st.session_state.authenticated = False
            st.rerun()

    df_filtered = df.copy()
    if selected_ligne != "Toutes les Lignes":
        df_filtered = df_filtered[df_filtered["Ligne_Production"] == selected_ligne]
    if selected_statut != "Tous les Statuts":
        df_filtered = df_filtered[df_filtered["Statut"] == selected_statut]

    st.markdown("""
    <div class="app-header">
        <img src="https://cdn-icons-png.flaticon.com/512/1541/1541402.png" class="app-header-icon"/>
        <div>
            <h1>Dashboard de Contrôle Qualité</h1>
            <p>Supervision de la conformité de la chaîne de production</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

     == "Tableau de Bord":
        total_inspecte = df_filtered["Quantite_Inspectee"].sum() if not df_filtered.empty else 0
        total_defauts = df_filtered["Defauts_Trouves"].sum() if not df_filtered.empty else 0
        taux_defaut = (total_defauts / total_inspecte * 100) if total_inspecte > 0 else 0
        conformes = len(df_filtered[df_filtered["Statut"] == "Conforme"]) if not df_filtered.empty else 0
        taux_conformite = (conformes / len(df_filtered) * 100) if not df_filtered.empty else 0
if menu == "Tableau de Bord":
        total_inspecte = df_filtered["Quantite_Inspectee"].sum() if not df_filtered.empty else 0
        total_defauts = df_filtered["Defauts_Trouves"].sum() if not df_filtered.empty else 0
        taux_defaut = (total_defauts / total_inspecte * 100) if total_inspecte > 0 else 0
        conformes = len(df_filtered[df_filtered["Statut"] == "Conforme"]) if not df_filtered.empty else 0
        taux_conformite = (conformes / len(df_filtered) * 100) if not df_filtered.empty else 0

        # KPI Cards
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        with kpi1:
            st.markdown(f'''
            <div class="kpi-card">
                <div class="kpi-header">
                    <span class="kpi-title">Total Inspecté</span>
                    <img src="https://cdn-icons-png.flaticon.com/512/3121/3121768.png" class="kpi-icon"/>
                </div>
                <div class="kpi-value">{total_inspecte:,}</div>
            </div>
            ''', unsafe_allow_html=True)

        with kpi2:
            st.markdown(f'''
            <div class="kpi-card">
                <div class="kpi-header">
                    <span class="kpi-title">Défectueux</span>
                    <img src="https://cdn-icons-png.flaticon.com/512/595/595067.png" class="kpi-icon"/>
                </div>
                <div class="kpi-value" style="color: #e11d48;">{total_defauts}</div>
            </div>
            ''', unsafe_allow_html=True)

        with kpi3:
            st.markdown(f'''
            <div class="kpi-card">
                <div class="kpi-header">
                    <span class="kpi-title">Taux de Défaut</span>
                    <img src="https://cdn-icons-png.flaticon.com/512/4301/4301566.png" class="kpi-icon"/>
                </div>
                <div class="kpi-value">{taux_defaut:.2f}%</div>
            </div>
            ''', unsafe_allow_html=True)

        with kpi4:
            st.markdown(f'''
            <div class="kpi-card">
                <div class="kpi-header">
                    <span class="kpi-title">Conformité Global</span>
                    <img src="https://cdn-icons-png.flaticon.com/512/190/190411.png" class="kpi-icon"/>
                </div>
                <div class="kpi-value" style="color: #16a34a;">{taux_conformite:.1f}%</div>
            </div>
            ''', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Vérification si des données existent après filtrage
        if df_filtered.empty:
            st.warning("Aucune donnée disponible pour les filtres sélectionnés.")
        else:
            col_g1, col_g2 = st.columns(2)
            
            plt.rcParams['font.family'] = 'sans-serif'
            plt.rcParams['axes.edgecolor'] = '#e2e8f0'
            plt.rcParams['axes.linewidth'] = 1.2

            with col_g1:
                st.markdown("##### Performance par Ligne de Production")
                fig1, ax1 = plt.subplots(figsize=(6, 3.8), facecolor='none')
                ax1.set_facecolor('none')
                
                defauts_ligne = df_filtered.groupby("Ligne_Production")["Defauts_Trouves"].sum().reset_index()
                sns.barplot(
                    data=defauts_ligne,
                    x="Ligne_Production",
                    y="Defauts_Trouves",
                    ax=ax1,
                    palette=["#2563eb", "#0284c7", "#0d9488", "#059669"]
                )
                ax1.set_xlabel("", fontsize=10, fontweight='bold', color='#64748b')
                ax1.set_ylabel("Nombre de Défauts", fontsize=10, fontweight='bold', color='#64748b')
                ax1.grid(axis='y', linestyle='--', alpha=0.5)
                sns.despine()
                st.pyplot(fig1, use_container_width=True)

            with col_g2:
                st.markdown("##### Répartition des Statuts de Contrôle")
                fig2, ax2 = plt.subplots(figsize=(6, 3.8), facecolor='none')
                ax2.set_facecolor('none')
                
                statut_counts = df_filtered['Statut'].value_counts()
                colors = {'Conforme': '#16a34a', 'Alerte': '#d97706', 'Non Conforme': '#dc2626'}
                palette = [colors.get(x, '#2563eb') for x in statut_counts.index]
                
                wedges, texts, autotexts = ax2.pie(
                    statut_counts,
                    labels=statut_counts.index,
                    autopct='%1.1f%%',
                    startangle=140,
                    colors=palette,
                    wedgeprops=dict(width=0.4, edgecolor='white', linewidth=3)
                )
                plt.setp(autotexts, size=9, weight="bold", color="white")
                plt.setp(texts, size=10, color="#0f172a", weight="500")
                st.pyplot(fig2, use_container_width=True)

            st.markdown("<br>##### Données Récentes d'Inspection", unsafe_allow_html=True)
            st.dataframe(
                df_filtered.sort_values(by="Date", ascending=False),
                use_container_width=True,
                hide_index=True
            )
        

    elif menu == "Saisie & Modification":
        st.markdown("### Gestion des Contrôles Qualité")
        
        tab_add, tab_edit, tab_del = st.tabs(["Ajouter un Contrôle", "Modifier une Saisie", "Supprimer un Enregistrement"])
        
        with tab_add:
            st.markdown("<br>", unsafe_allow_html=True)
            with st.form("add_form", clear_on_submit=True):
                c1, c2 = st.columns(2)
                with c1:
                    date_val = st.date_input("Date du contrôle", datetime.now())
                    ligne_val = st.selectbox("Ligne de Production", ["Ligne A", "Ligne B", "Ligne C", "Ligne D"])
                    produit_val = st.text_input("Désignation du Produit", placeholder="Ex: Bloc Moteur V6")
                    quantite_val = st.number_input("Quantité Inspectée", min_value=1, value=100)
                with c2:
                    defauts_val = st.number_input("Nombre de Défauts Trouvés", min_value=0, value=0)
                    statut_val = st.selectbox("Statut de Conformité", ["Conforme", "Alerte", "Non Conforme"])
                    inspecteur_val = st.text_input("Nom de l'Inspecteur", placeholder="Ex: Karim Bennani")

                if st.form_submit_button("Enregistrer le Contrôle", type="primary", use_container_width=True):
                    new_id = int(df["ID"].max() + 1) if not df.empty else 1
                    new_row = {
                        "ID": new_id,
                        "Date": pd.to_datetime(date_val),
                        "Ligne_Production": ligne_val,
                        "Produit": produit_val,
                        "Quantite_Inspectee": quantite_val,
                        "Defauts_Trouves": defauts_val,
                        "Statut": statut_val,
                        "Inspecteur": inspecteur_val
                    }
                    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                    save_data(df)
                    st.success("Saisie enregistrée avec succès.")
                    st.rerun()

        with tab_edit:
            st.markdown("<br>", unsafe_allow_html=True)
            if not df.empty:
                edit_id = st.selectbox("Sélectionner l'ID à modifier", df["ID"].tolist(), key="edit_select")
                row_to_edit = df[df["ID"] == edit_id].iloc[0]

                with st.form("edit_form"):
                    c1, c2 = st.columns(2)
                    with c1:
                        edit_date = st.date_input("Date", row_to_edit["Date"])
                        edit_ligne = st.selectbox("Ligne", ["Ligne A", "Ligne B", "Ligne C", "Ligne D"], index=["Ligne A", "Ligne B", "Ligne C", "Ligne D"].index(row_to_edit["Ligne_Production"]))
                        edit_produit = st.text_input("Produit", row_to_edit["Produit"])
                        edit_quantite = st.number_input("Quantité", min_value=1, value=int(row_to_edit["Quantite_Inspectee"]))
                    with c2:
                        edit_defauts = st.number_input("Défauts", min_value=0, value=int(row_to_edit["Defauts_Trouves"]))
                        edit_statut = st.selectbox("Statut", ["Conforme", "Alerte", "Non Conforme"], index=["Conforme", "Alerte", "Non Conforme"].index(row_to_edit["Statut"]))
                        edit_inspecteur = st.text_input("Inspecteur", row_to_edit["Inspecteur"])

                    if st.form_submit_button("Mettre à jour", type="primary", use_container_width=True):
                        df.loc[df["ID"] == edit_id, ["Date", "Ligne_Production", "Produit", "Quantite_Inspectee", "Defauts_Trouves", "Statut", "Inspecteur"]] = [
                            pd.to_datetime(edit_date), edit_ligne, edit_produit, edit_quantite, edit_defauts, edit_statut, edit_inspecteur
                        ]
                        save_data(df)
                        st.success("Enregistrement mis à jour.")
                        st.rerun()

        with tab_del:
            st.markdown("<br>", unsafe_allow_html=True)
            if not df.empty:
                del_id = st.selectbox("Sélectionner l'ID à supprimer", df["ID"].tolist(), key="del_select")
                if st.button("Confirmer la suppression", type="primary", use_container_width=True):
                    df = df[df["ID"] != del_id]
                    save_data(df)
                    st.success("Enregistrement supprimé.")
                    st.rerun()

    elif menu == "Rapports & Exportation":
        st.markdown("### Exporter les Données d'Inspection")
        st.markdown("Téléchargez les rapports complets filtrés selon vos critères sous format CSV pour une analyse externe.")
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.dataframe(df_filtered, use_container_width=True, hide_index=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        csv_data = df_filtered.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Exporter les données en CSV",
            data=csv_data,
            file_name=f"rapport_qualite_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True,
            type="primary"
        )

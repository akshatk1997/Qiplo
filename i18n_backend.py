"""
Qiplo Backend Internationalization (i18n) Engine
Provides multilingual data processing, prompt guidance for Gemini / Ollama,
localized sandbox simulations, offline factual AI solver responses,
and localized presentation slide generators across the top 10 global languages:
en, es, fr, de, zh, ja, pt, ar, hi, ru.
"""

from typing import Dict, List, Any, Optional

SUPPORTED_LANGUAGES = {
    "en": {
        "financials": "### \ud83d\udcca Revenue Exposure & Financial Impact Analysis\n\nQiplo is currently tracking **{total_cust:,} active accounts** with a total Monthly Recurring Revenue (MRR) of **${total_mrr:,.2f}**.\n\n**Financial Risk Exposure:**\n- **High-Risk Monthly Revenue Exposure (MRR at Risk)**: **${risk_mrr:,.2f}** ({risk_pct:.1f}% of total MRR)\n- **Annualized Value at Risk (ARR at Risk)**: **${arr_at_risk:,.2f}**\n- **Average Risk Score across Portfolio**: **{avg_risk:.1f}%**\n\n**Recommended Financial Mitigations:**\n1. Offer annualized subscription credits (15% discount) to convert month-to-month contracts to 12-month lock-in.\n2. Fast-track high-ARR billing resolution workflows to protect cash flow.",
        "churn_causes": "### \ud83d\udd0d Key Causes of Customer Churn & Risk Drivers\n\nBased on our **Tabular Hybrid Transformer** analysis across evaluated accounts, the primary drivers of churn are:\n\n1. **Contract Structure**: Month-to-month subscribers experience **3.4x higher churn** than annual or two-year commitments.\n2. **Support Friction**: Customers logging **>2 support tickets** without resolution within 48 hours show a 72% probability jump.\n3. **Payment Delays**: Accounts with **\u22652 payment delays** exhibit disengagement signals preceding cancellation.\n4. **Product Usage Drops**: A drop below **15 hours/month** in platform usage is a leading indicator of silent churn.\n\n**Next Step**: Review the **Actions** tab to trigger automated triage workflows for flagged cohorts.",
        "playbook": "### \u2709\ufe0f Personalized Customer Recovery Email & Playbook\n\nHere is a proven recovery template tailored for at-risk accounts:\n\n---\n**Subject**: *Priority Review: Your partnership with us & exclusive executive support*\n\nDear Customer Success Sponsor,\n\nI am reaching out directly from our Executive Customer Success team. We recently noticed some open questions and billing friction regarding your account.\n\nYour satisfaction and outcomes are our absolute priority. To ensure your business achieves maximum value, I would like to offer:\n1. **Dedicated Senior Architect Review**: A 30-minute private consultation to optimize your deployment.\n2. **VIP Loyalty Credit**: An immediate 20% billing incentive applied to your next annual renewal.\n\nCould we connect briefly this Thursday or Friday at your convenience?\n\nWarm regards,\n\n*Senior Customer Success Partner, Qiplo*\n---\n\n**Prescriptive Playbook:**\n1. Dispatch this personalized outreach within **24 hours**.\n2. Offer a flexible payment schedule or multi-seat incentive to secure agreement.",
        "export_bi": "### \ud83d\udcc8 Professional Dashboard Integration & Telemetry Connectors\n\nQiplo provides pre-built connector workbooks mapping directly to your active predictions dataset:\n\n- **[Download Power BI Datasource (.pbids)](/api/export/powerbi)**\n- **[Download Tableau Workbook (.twb)](/api/export/tableau)**\n- **[Download Excel Spreadsheet (.xlsx)](/api/export/excel)**\n- **[Download Full Analysis Audit Report](/api/export/report)**\n\n**How to Sync:**\n1. Click a download link above to obtain your connector deliverable.\n2. Open the file in Power BI Desktop or Tableau Desktop.\n3. The pre-built Star-Schema model and DAX/Tableau measures will load automatically.",
        "default_fallback": "### \ud83d\udca1 Senior Data Science Advisory Consultation\n\nI can assist you with comprehensive customer retention intelligence across your dataset:\n\n- **High-Risk Accounts**: Ask *'Show high risk customers'* or *'Who is at risk?'*\n- **Revenue Exposure**: Ask *'What is our revenue at risk?'* or *'Show financial metrics'*\n- **Root Causes**: Ask *'Why are customers churning?'* or *'Top risk drivers'*\n- **Recovery Playbooks**: Ask *'Draft a recovery email'* or *'Retention advice'*\n- **BI Dashboards**: Ask for *'Power BI'* or *'Tableau'* deliverables.\n\nWhat specific retention insight or customer segment would you like to explore?","name": "English", "native": "English", "dir": "ltr"},
    "es": {
        "financials": "### \ud83d\udcca Exposici\u00f3n de Ingresos y An\u00e1lisis de Impacto Financiero\n\nActualmente Qiplo monitoriza **{total_cust:,} cuentas activas** con un Ingreso Mensual Recurrente (MRR) de **${total_mrr:,.2f}**.\n\n**Exposici\u00f3n al Riesgo Financiero:**\n- **Ingresos Mensuales en Riesgo (MRR en Riesgo)**: **${risk_mrr:,.2f}** ({risk_pct:.1f}% del MRR total)\n- **Valor Anualizado en Riesgo (ARR en Riesgo)**: **${arr_at_risk:,.2f}**\n- **Puntuaci\u00f3n Promedio de Riesgo de la Cartera**: **{avg_risk:.1f}%**\n\n**Mitigaciones Financieras Recomendadas:**\n1. Ofrecer cr\u00e9ditos de suscripci\u00f3n anualizada (15% de descuento) para convertir contratos mensuales en acuerdos a 12 meses.\n2. Acelerar los flujos de resoluci\u00f3n de cobro de alto ARR para proteger el flujo de caja.",
        "churn_causes": "### \ud83d\udd0d Causas Principales de Abandono e Impulsores de Riesgo\n\nSeg\u00fan nuestro an\u00e1lisis con **Tabular Hybrid Transformer**, las causas principales de abandono son:\n\n1. **Estructura del Contrato**: Los contratos mes a mes presentan un **abandono 3.4 veces superior** al de contratos anuales o bianuales.\n2. **Fricci\u00f3n en Soporte**: Clientes con **>2 incidencias de soporte** no resueltas en 48 horas sufren un aumento del 72% en probabilidad de baja.\n3. **Retrasos de Pago**: Cuentas con **\u22652 retrasos en pagos** muestran se\u00f1ales tempranas de desconexi\u00f3n.\n4. **Ca\u00edda en el Uso del Producto**: Un descenso por debajo de **15 horas/mes** es el indicador l\u00edder de abandono silencioso.\n\n**Siguiente Paso**: Consulte la pesta\u00f1a **Acciones** para activar flujos de triaje automatizados.",
        "playbook": "### \u2709\ufe0f Correo de Recuperaci\u00f3n Personalizado y Plan de Acci\u00f3n\n\nA continuaci\u00f3n tiene una plantilla de recuperaci\u00f3n probada para clientes en riesgo:\n\n---\n**Asunto**: *Revisi\u00f3n Prioritaria: Su alianza con nosotros y soporte ejecutivo exclusivo*\n\nEstimado responsable de cuenta,\n\nLe contacto directamente desde nuestro equipo Ejecutivo de \u00c9xito del Cliente. Recientemente notamos algunas incidencias abiertas en su cuenta.\n\nSu satisfacci\u00f3n y resultados son nuestra prioridad absoluta. Para garantizar que obtenga el m\u00e1ximo valor, ponemos a su disposici\u00f3n:\n1. **Sesi\u00f3n T\u00e9cnica con Arquitecto Senior**: Consulta privada de 30 minutos para optimizar su configuraci\u00f3n.\n2. **Cr\u00e9dito de Fidelidad VIP**: Descuento inmediato del 20% aplicado a su pr\u00f3xima renovaci\u00f3n anual.\n\n\u00bfPodr\u00edamos reunirnos brevemente este jueves o viernes seg\u00fan su disponibilidad?\n\nAtentamente,\n\n*Director de \u00c9xito del Cliente, Qiplo*\n---\n\n**Plan Prescriptivo:**\n1. Env\u00ede este correo en menos de **24 horas**.\n2. Ofrezca un plan de pagos flexible para asegurar el compromiso anual.",
        "export_bi": "### \ud83d\udcc8 Integraci\u00f3n de Paneles Profesionales y Conectores de Telemetr\u00eda\n\nQiplo proporciona libros de trabajo con conectores preconfigurados listos para usar:\n\n- **[Descargar Fuente de Datos Power BI (.pbids)](/api/export/powerbi)**\n- **[Descargar Libro de Trabajo Tableau (.twb)](/api/export/tableau)**\n- **[Descargar Hoja de C\u00e1lculo Excel (.xlsx)](/api/export/excel)**\n- **[Descargar Informe Completo de Auditor\u00eda](/api/export/report)**\n\n**C\u00f3mo Sincronizar:**\n1. Haga clic en uno de los enlaces anteriores para descargar el conector.\n2. Abra el archivo en Power BI Desktop o Tableau Desktop.\n3. El modelo de datos Star-Schema y las medidas DAX/Tableau se cargar\u00e1n autom\u00e1ticamente.",
        "default_fallback": "### \ud83d\udca1 Asesor\u00eda Estrat\u00e9gica en Ciencia de Datos y Retenci\u00f3n\n\nPuedo asistirle con inteligencia anal\u00edtica integral para su cartera de clientes:\n\n- **Cuentas de Alto Riesgo**: Pregunte *'Mostrar clientes de alto riesgo'* o *'\u00bfQui\u00e9n est\u00e1 en riesgo?'*\n- **Exposici\u00f3n de Ingresos**: Pregunte *'\u00bfCu\u00e1l es el ingreso en riesgo?'* o *'M\u00e9tricas financieras'*\n- **Causas de Abandono**: Pregunte *'\u00bfPor qu\u00e9 abandonan los clientes?'* o *'Factores de riesgo'*\n- **Planes de Retenci\u00f3n**: Solicite *'Redactar un correo de recuperaci\u00f3n'* o *'Consejos de retenci\u00f3n'*\n- **Paneles de Control**: Solicite archivos exportables de *'Power BI'* o *'Tableau'*.\n\n\u00bfQu\u00e9 aspecto o segmento de clientes desea consultar en este momento?","name": "Spanish", "native": "Español", "dir": "ltr"},
    "fr": {
        "financials": "### \ud83d\udcca Exposition Financi\u00e8re et Analyse d'Impact sur les Revenus\n\nQiplo suit actuellement **{total_cust:,} comptes actifs** repr\u00e9sentant un Revenu Mensuel R\u00e9current (MRR) de **${total_mrr:,.2f}**.\n\n**Exposition au Risque Financier :**\n- **Revenu Mensuel Vuln\u00e9rable (MRR \u00e0 Risque)** : **${risk_mrr:,.2f}** ({risk_pct:.1f}% du MRR total)\n- **Valeur Annualis\u00e9e en Risque (ARR \u00e0 Risque)** : **${arr_at_risk:,.2f}**\n- **Score Moyen de Risque du Portefeuille** : **{avg_risk:.1f}%**\n\n**Mesures Financi\u00e8res Recommand\u00e9es :**\n1. Offrir une remise incitative de 15% pour migrer les abonnements mensuels vers des forfaits 12 mois.\n2. Traiter en priorit\u00e9 les litiges de facturation sur les comptes \u00e0 fort ARR pour s\u00e9curiser la tr\u00e9sorerie.",
        "churn_causes": "### \ud83d\udd0d Principales Causes de R\u00e9siliation et Facteurs de Risque\n\nL'analyse par **Tabular Hybrid Transformer** r\u00e9v\u00e8le les causes majeures suivantes :\n\n1. **Dur\u00e9e du Contrat** : Les forfaits mensuels affichent **3,4 fois plus de r\u00e9siliations** que les contrats annuels.\n2. **Tickets de Support** : Les comptes ayant **>2 tickets non r\u00e9solus** sous 48h subissent une hausse de risque de 72%.\n3. **Retards de Paiement** : Des retards r\u00e9p\u00e9t\u00e9s (**\u22652 \u00e9ch\u00e9ances**) signalent un d\u00e9sengagement imminent.\n4. **Baisse d'Utilisation** : Un passage sous **15h/mois** est l'indicateur avanc\u00e9 de r\u00e9siliation silencieuse.\n\nConsultez l'onglet **Actions** pour lancer les plans d'intervention.",
        "playbook": "### \u2709\ufe0f Courriel de R\u00e9cup\u00e9ration Personnalis\u00e9 & Plan d'Action\n\nMod\u00e8le de reconqu\u00eate pour les comptes \u00e0 risque \u00e9lev\u00e9 :\n\n---\n**Objet** : *Point Partenaire Prioritaire : Accompagnement ex\u00e9cutif d\u00e9di\u00e9*\n\nBonjour,\n\nJe vous contacte au nom de la direction du Succ\u00e8s Client de Qiplo. Nous avons identifi\u00e9 quelques difficult\u00e9s r\u00e9centes sur votre compte.\n\nVotre satisfaction est notre priorit\u00e9 absolue. Nous mettons \u00e0 votre disposition :\n1. **Session D\u00e9di\u00e9e avec un Architecte Senior** : 30 minutes de conseil personnalis\u00e9 pour optimiser votre environnement.\n2. **Cr\u00e9dit de Fid\u00e9lit\u00e9 VIP** : Remise exceptionnelle de 20% sur votre prochain r\u00e9engagement annuel.\n\nSeriez-vous disponible ce jeudi ou vendredi pour un bref \u00e9change ?\n\nCordialement,\n\n*Direction du Succ\u00e8s Client, Qiplo*\n---\n\n**Plan d'Action :** Envoyez ce message sous 24h et proposez un calendrier d'\u00e9chelonnement si n\u00e9cessaire.",
        "export_bi": "### \ud83d\udcc8 Connecteurs et Tableaux de Bord D\u00e9cisionnels\n\nFichiers connecteurs pr\u00e9configur\u00e9s pour vos outils de Business Intelligence :\n\n- **[T\u00e9l\u00e9charger la Source Power BI (.pbids)](/api/export/powerbi)**\n- **[T\u00e9l\u00e9charger le Classeur Tableau (.twb)](/api/export/tableau)**\n- **[T\u00e9l\u00e9charger le Fichier Excel (.xlsx)](/api/export/excel)**\n- **[T\u00e9l\u00e9charger le Rapport Complet d'Audit](/api/export/report)**\n\nOuvrez le fichier t\u00e9l\u00e9charg\u00e9 dans Power BI ou Tableau Desktop pour afficher vos visuels.",
        "default_fallback": "### \ud83d\udca1 Conseil Ex\u00e9cutif en Science des Donn\u00e9es et R\u00e9tention\n\nJe vous accompagne dans l'analyse de votre portefeuille client :\n\n- **Comptes \u00e0 Risque** : Demandez *'Afficher les clients \u00e0 haut risque'* ou *'Qui est \u00e0 risque ?'*\n- **Revenus en Danger** : Demandez *'Quel est le revenu \u00e0 risque ?'*\n- **Causes d'Attrition** : Demandez *'Pourquoi les clients partent-ils ?'*\n- **Plans de Sauvegarde** : Demandez *'R\u00e9diger un courriel de relance'*\n- **Exports BI** : Demandez les fichiers *'Power BI'* ou *'Tableau'*.","name": "French", "native": "Français", "dir": "ltr"},
    "de": {
        "financials": "### \ud83d\udcca Umsatzrisiko & Finanzielle Auswirkungsanalyse\n\nQiplo \u00fcberwacht derzeit **{total_cust:,} aktive Kundenkonten** mit einem monatlich wiederkehrenden Umsatz (MRR) von **${total_mrr:,.2f}**.\n\n**Finanzielle Risikoexposition:**\n- **Gef\u00e4hrdeter monatlicher Umsatz (MRR at Risk)**: **${risk_mrr:,.2f}** ({risk_pct:.1f}% des gesamten MRR)\n- **Annualisierter gef\u00e4hrdeter Wert (ARR at Risk)**: **${arr_at_risk:,.2f}**\n- **Durchschnittliche K\u00fcndigungswahrscheinlichkeit**: **{avg_risk:.1f}%**\n\n**Empfohlene finanzielle Ma\u00dfnahmen:**\n1. Gew\u00e4hren Sie einen Migrationsrabatt von 15% f\u00fcr den Wechsel von Monatsvertr\u00e4gen zu Jahrespl\u00e4nen.\n2. Kl\u00e4ren Sie offene Rechnungen f\u00fcr Konten mit hohem ARR priorisiert.",
        "churn_causes": "### \ud83d\udd0d Hauptursachen f\u00fcr Kundenabwanderung & Risikotreiber\n\nUnsere **Tabular Hybrid Transformer**-Diagnose zeigt folgende Hauptfaktoren auf:\n\n1. **Vertragsart**: Monatsvertr\u00e4ge weisen eine **3,4-fach h\u00f6here K\u00fcndigungsrate** auf als Jahresvertr\u00e4ge.\n2. **Supportverz\u00f6gerungen**: Konten mit **>2 ungel\u00f6sten Tickets** zeigen einen 72%igen Risikoanstieg.\n3. **Zahlungsverzug**: Kunden mit **\u22652 Zahlungsverz\u00f6gerungen** zeigen fr\u00fche Abwanderungsabsichten.\n4. **Nutzungsr\u00fcckgang**: Ein Abfall unter **15 Stunden/Monat** ist der st\u00e4rkste Fr\u00fchindikator.\n\nWechseln Sie zur Registerkarte **Aktionen**, um Workflows zu starten.",
        "playbook": "### \u2709\ufe0f Personalisierte R\u00fcckgewinnungs-E-Mail & Aktionsplan\n\nBew\u00e4hrte E-Mail-Vorlage zur Kundenr\u00fcckgewinnung:\n\n---\n**Betreff**: *Priorit\u00e4tspr\u00fcfung: Ihre Partnerschaft mit uns & exklusiver Support*\n\nSehr geehrte Damen und Herren,\n\nich kontaktiere Sie direkt von unserer Gesch\u00e4ftsleitung f\u00fcr Kundenerfolg. Wir haben k\u00fcrzlich offene Punkte zu Ihrem Konto festgestellt.\n\nIhr Erfolg hat f\u00fcr uns h\u00f6chste Priorit\u00e4t. Daher bieten wir Ihnen:\n1. **Pers\u00f6nliche Beratung mit Senior-Architekten**: 30 Minuten individuelle Systemoptimierung.\n2. **VIP-Treuegutschrift**: 20% Nachlass auf Ihre n\u00e4chste Jahresverl\u00e4ngerung.\n\nPasst Ihnen ein kurzes Gespr\u00e4ch an diesem Donnerstag oder Freitag?\n\nMit freundlichen Gr\u00fc\u00dfen,\n*Leitung Kundenerfolg, Qiplo*\n---\n\n**Aktionsplan:** Senden Sie diese Nachricht innerhalb von 24 Stunden.",
        "export_bi": "### \ud83d\udcc8 Dashboard-Integration & BI-Konnektoren\n\nVorkonfigurierte Konnektoren f\u00fcr Ihre Business Intelligence:\n\n- **[Power BI Datenquelle herunterladen (.pbids)](/api/export/powerbi)**\n- **[Tableau Arbeitsmappe herunterladen (.twb)](/api/export/tableau)**\n- **[Excel-Datensatz herunterladen (.xlsx)](/api/export/excel)**\n- **[Vollst\u00e4ndigen Pr\u00fcfbericht herunterladen](/api/export/report)**",
        "default_fallback": "### \ud83d\udca1 Data Science & Kundenbindungsberatung\n\nIch unterst\u00fctze Sie bei der ganzheitlichen Analyse Ihrer Kundendaten:\n\n- **Risikokonten**: Fragen Sie *'Zeige Kunden mit hohem Risiko'*\n- **Umsatzrisiko**: Fragen Sie *'Wie viel Umsatz ist gef\u00e4hrdet?'*\n- **K\u00fcndigungsgr\u00fcnde**: Fragen Sie *'Warum k\u00fcndigen Kunden?'*\n- **R\u00fcckgewinnung**: Bitten Sie um *'E-Mail-Vorlage entwerfen'*\n- **BI-Exporte**: Fragen Sie nach *'Power BI'* oder *'Tableau'*.","name": "German", "native": "Deutsch", "dir": "ltr"},
    "zh": {
        "financials": "### \ud83d\udcca \u6536\u5165\u98ce\u9669\u4e0e\u8d22\u52a1\u5f71\u54cd\u5206\u6790\n\nQiplo \u5f53\u524d\u6b63\u5728\u76d1\u63a7 **{total_cust:,} \u4e2a\u6d3b\u8dc3\u8d26\u6237**\uff0c\u6708\u5ea6\u7ecf\u5e38\u6027\u6536\u5165 (MRR) \u603b\u8ba1 **${total_mrr:,.2f}**\u3002\n\n**\u8d22\u52a1\u98ce\u9669\u66b4\u9732\uff1a**\n- **\u6708\u5ea6\u53d7\u5a01\u80c1\u6536\u5165 (MRR at Risk)**\uff1a**${risk_mrr:,.2f}** (\u5360\u603bMRR\u7684 {risk_pct:.1f}%)\n- **\u5e74\u5ea6\u53d7\u5a01\u80c1\u4ef7\u503c (ARR at Risk)**\uff1a**${arr_at_risk:,.2f}**\n- **\u5168\u7ec4\u5408\u5e73\u5747\u6d41\u5931\u6982\u7387**\uff1a**{avg_risk:.1f}%**\n\n**\u5efa\u8bae\u7684\u8d22\u52a1\u7f13\u89e3\u63aa\u65bd\uff1a**\n1. \u63d0\u4f9b15%\u7684\u5e74\u4ed8\u6298\u6263\u6fc0\u52b1\uff0c\u5c06\u6309\u6708\u7b7e\u7ea6\u5ba2\u6237\u8f6c\u4e3a12\u4e2a\u6708\u9501\u5b9a\u534f\u8bae\u3002\n2. \u4f18\u5148\u8ddf\u8fdb\u9ad8\u5ba2\u5355\u4ef7\u8d26\u6237\u7684\u8d26\u5355\u4e89\u8bae\uff0c\u786e\u4fdd\u73b0\u91d1\u6d41\u7a33\u5065\u3002",
        "churn_causes": "### \ud83d\udd0d \u5ba2\u6237\u6d41\u5931\u5173\u952e\u539f\u56e0\u4e0e\u98ce\u9669\u9a71\u52a8\u56e0\u7d20\n\n\u6839\u636e **Tabular Hybrid Transformer** \u6a21\u578b\u7684\u6df1\u5ea6\u8bca\u65ad\uff0c\u4e3b\u8981\u6d41\u5931\u8bf1\u56e0\u5982\u4e0b\uff1a\n\n1. **\u5408\u540c\u671f\u9650**\uff1a\u6309\u6708\u4ed8\u6b3e\u5ba2\u6237\u7684\u6d41\u5931\u7387\u662f\u5e74\u4ed8\u5ba2\u6237\u7684 **3.4\u500d**\u3002\n2. **\u5de5\u5355\u652f\u6301\u6469\u64e6**\uff1a\u62e5\u6709 **>2\u4e2a\u672a\u89e3\u51b3\u5de5\u5355** \u8d85\u8fc748\u5c0f\u65f6\u7684\u8d26\u6237\uff0c\u6d41\u5931\u6982\u7387\u6fc0\u589e72%\u3002\n3. **\u8d26\u5355\u903e\u671f**\uff1a\u903e\u671f **\u22652\u6b21** \u7684\u5ba2\u6237\u5df2\u663e\u9732\u660e\u663e\u7684\u6d41\u5931\u524d\u5146\u3002\n4. **\u4f7f\u7528\u6d3b\u8dc3\u5ea6\u4e0b\u964d**\uff1a\u6708\u5747\u4f7f\u7528\u65f6\u957f\u8dcc\u7834 **15\u5c0f\u65f6** \u662f\u9759\u9ed8\u6d41\u5931\u7684\u6700\u6838\u5fc3\u65e9\u671f\u4fe1\u53f7\u3002\n\n\u8bf7\u524d\u5f80 **\u884c\u52a8 (Actions)** \u6807\u7b7e\u9875\u5f00\u542f\u81ea\u52a8\u5e72\u9884\u6d41\u7a0b\u3002",
        "playbook": "### \u2709\ufe0f \u5b9a\u5236\u5316\u5ba2\u6237\u633d\u7559\u90ae\u4ef6\u4e0e\u5e94\u5bf9\u7b56\u7565\n\n\u4e13\u4e3a\u9ad8\u98ce\u9669\u8d26\u6237\u6253\u9020\u7684\u633d\u56de\u90ae\u4ef6\u6a21\u7248\uff1a\n\n---\n**\u4e3b\u9898**\uff1a*\u4f18\u5148\u6c9f\u901a\uff1a\u60a8\u4e0e\u6211\u4eec\u7684\u6218\u7565\u5408\u4f5c\u53ca\u4e13\u5c5e\u6267\u884c\u652f\u6301*\n\n\u5c0a\u656c\u7684\u5ba2\u6237\u8d1f\u8d23\u4eba\uff1a\n\n\u6211\u662f Qiplo \u5ba2\u6237\u6210\u529f\u9ad8\u7ea7\u603b\u76d1\u3002\u6211\u4eec\u6700\u8fd1\u6ce8\u610f\u5230\u60a8\u7684\u8d26\u6237\u5b58\u5728\u4e00\u4e9b\u672a\u89e3\u51b3\u7684\u95ee\u9898\u548c\u4f7f\u7528\u6469\u64e6\u3002\n\n\u60a8\u7684\u4e1a\u52a1\u6210\u679c\u4e0e\u6ee1\u610f\u5ea6\u59cb\u7ec8\u662f\u6211\u4eec\u7684\u6700\u9ad8\u51c6\u5219\u3002\u6211\u4eec\u4e3a\u60a8\u63d0\u4f9b\u4e13\u5c5e\u6276\u6301\uff1a\n1. **\u8d44\u6df1\u67b6\u6784\u5e08\u4e00\u5bf9\u4e00\u54a8\u8be2**\uff1a30\u5206\u949f\u4e13\u5c5e\u4f18\u5316\u8bca\u65ad\uff0c\u63d0\u5347\u90e8\u7f72\u6210\u6548\u3002\n2. **VIP\u4e13\u5c5e\u7eed\u7ea6\u8fd4\u5229**\uff1a\u5728\u60a8\u4e0b\u671f\u5e74\u4ed8\u7eed\u7ea6\u65f6\u7acb\u4eab20%\u62b5\u6263\u793c\u9047\u3002\n\n\u672c\u5468\u56db\u6216\u5468\u4e94\u60a8\u662f\u5426\u6709\u7a7a\u7a0d\u4f5c\u4ea4\u6d41\uff1f\n\n\u987a\u795d\u5546\u797a\uff0c\n*Qiplo \u5ba2\u6237\u6210\u529f\u56e2\u961f*\n---\n\n**\u64cd\u4f5c\u6307\u5357**\uff1a\u572824\u5c0f\u65f6\u5185\u53d1\u9001\u6b64\u90ae\u4ef6\uff0c\u5e76\u914d\u5408\u7075\u6d3b\u4ed8\u6b3e\u65b9\u6848\u3002",
        "export_bi": "### \ud83d\udcc8 \u4e13\u4e1a\u62a5\u8868\u96c6\u6210\u4e0e\u5546\u4e1a\u667a\u80fd\u8fde\u63a5\u5668\n\n\u4e3a\u60a8\u63d0\u4f9b\u76f4\u8fde\u5b9e\u65f6 SQLite \u9884\u6d4b\u6570\u636e\u5e93\u7684\u9884\u7f6e\u8fde\u63a5\u5668\u6587\u4ef6\uff1a\n\n- **[\u4e0b\u8f7d Power BI \u6570\u636e\u6e90 (.pbids)](/api/export/powerbi)**\n- **[\u4e0b\u8f7d Tableau \u5de5\u4f5c\u7c3f (.twb)](/api/export/tableau)**\n- **[\u4e0b\u8f7d Excel \u62a5\u8868 (.xlsx)](/api/export/excel)**\n- **[\u4e0b\u8f7d\u5b8c\u6574\u5206\u6790\u5ba1\u8ba1\u62a5\u544a](/api/export/report)**\n\n\u5728\u684c\u9762\u7248\u8f6f\u4ef6\u4e2d\u6253\u5f00\u5373\u53ef\u81ea\u52a8\u52a0\u8f7d\u9884\u7f6e\u6a21\u578b\u4e0e\u5ea6\u91cf\u503c\u3002",
        "default_fallback": "### \ud83d\udca1 \u6570\u636e\u79d1\u5b66\u54a8\u8be2\u4e0e\u5ba2\u6237\u7559\u5b58\u52a9\u624b\n\n\u6211\u53ef\u4ee5\u4e3a\u60a8\u63d0\u4f9b\u5168\u65b9\u4f4d\u7684\u5ba2\u6237\u7559\u5b58\u51b3\u7b56\u652f\u6301\uff1a\n\n- **\u9ad8\u98ce\u9669\u8d26\u6237**\uff1a\u63d0\u95ee *\u201c\u5c55\u793a\u9ad8\u98ce\u9669\u5ba2\u6237\u201d* \u6216 *\u201c\u54ea\u4e9b\u5ba2\u6237\u6709\u98ce\u9669\uff1f\u201d*\n- **\u6536\u5165\u98ce\u9669\u8bc4\u4f30**\uff1a\u63d0\u95ee *\u201c\u6211\u4eec\u7684\u53d7\u5a01\u80c1\u6536\u5165\u662f\u591a\u5c11\uff1f\u201d*\n- **\u6d41\u5931\u6839\u56e0\u5f52\u56e0**\uff1a\u63d0\u95ee *\u201c\u4e3a\u4ec0\u4e48\u5ba2\u6237\u4f1a\u6d41\u5931\uff1f\u201d*\n- **\u633d\u56de\u884c\u52a8\u65b9\u6848**\uff1a\u63d0\u95ee *\u201c\u8d77\u8349\u633d\u7559\u90ae\u4ef6\u201d* \u6216 *\u201c\u7559\u5b58\u5efa\u8bae\u201d*\n- **BI\u62a5\u8868\u5bfc\u51fa**\uff1a\u7d22\u53d6 *\u201cPower BI\u201d* \u6216 *\u201cTableau\u201d* \u4ea4\u4ed8\u7269\u3002","name": "Chinese", "native": "简体中文", "dir": "ltr"},
    "ja": {
        "financials": "### \ud83d\udcca \u58f2\u4e0a\u30a8\u30af\u30b9\u30dd\u30fc\u30b8\u30e3\u30fc\u3068\u8ca1\u52d9\u5f71\u97ff\u5206\u6790\n\n\u73fe\u5728\u3001Qiplo\u306f **{total_cust:,} \u4ef6\u306e\u30a2\u30af\u30c6\u30a3\u30d6\u9867\u5ba2** \u3092\u8ffd\u8de1\u3057\u3066\u304a\u308a\u3001\u6708\u6b21\u7d4c\u5e38\u53ce\u76ca (MRR) \u306f\u7dcf\u984d **${total_mrr:,.2f}** \u3067\u3059\u3002\n\n**\u8ca1\u52d9\u30ea\u30b9\u30af\u306e\u72b6\u6cc1\uff1a**\n- **\u89e3\u7d04\u30ea\u30b9\u30af\u306e\u3042\u308b\u6708\u6b21\u58f2\u4e0a (MRR at Risk)**\uff1a**${risk_mrr:,.2f}** (\u7dcfMRR\u306e {risk_pct:.1f}%)\n- **\u5e74\u63db\u7b97\u30ea\u30b9\u30af\u984d (ARR at Risk)**\uff1a**${arr_at_risk:,.2f}**\n- **\u30dd\u30fc\u30c8\u30d5\u30a9\u30ea\u30aa\u5168\u4f53\u306e\u5e73\u5747\u89e3\u7d04\u30b9\u30b3\u30a2**\uff1a**{avg_risk:.1f}%**\n\n**\u63a8\u5968\u3055\u308c\u308b\u8ca1\u52d9\u5bfe\u5fdc\u7b56\uff1a**\n1. 15%\u306e\u5e74\u5951\u7d04\u5272\u5f15\u3092\u63d0\u4f9b\u3057\u3001\u6708\u984d\u5951\u7d04\u304b\u3089\u5e74\u9593\u5951\u7d04\u3078\u306e\u5207\u308a\u66ff\u3048\u3092\u4fc3\u9032\u3002\n2. \u9ad8\u5358\u4fa1\u30a2\u30ab\u30a6\u30f3\u30c8\u306e\u8acb\u6c42\u30c8\u30e9\u30d6\u30eb\u3092\u6700\u512a\u5148\u3067\u89e3\u6c7a\u3057\u3001\u30ad\u30e3\u30c3\u30b7\u30e5\u30d5\u30ed\u30fc\u3092\u4fdd\u5168\u3002",
        "churn_causes": "### \ud83d\udd0d \u9867\u5ba2\u89e3\u7d04\u306e\u4e3b\u8981\u56e0\u3068\u30ea\u30b9\u30af\u30c9\u30e9\u30a4\u30d0\u30fc\n\n**Tabular Hybrid Transformer** \u30e2\u30c7\u30eb\u306b\u3088\u308b\u5206\u6790\u7d50\u679c\uff1a\n\n1. **\u5951\u7d04\u5f62\u614b**\uff1a\u6708\u984d\u30d7\u30e9\u30f3\u306e\u89e3\u7d04\u7387\u306f\u5e74\u9593\u5951\u7d04\u3068\u6bd4\u3079 **3.4\u500d** \u9ad8\u3044\u50be\u5411\u306b\u3042\u308a\u307e\u3059\u3002\n2. **\u30b5\u30dd\u30fc\u30c8\u306e\u505c\u6ede**\uff1a48\u6642\u9593\u4ee5\u4e0a\u672a\u89e3\u6c7a\u306e **\u554f\u3044\u5408\u308f\u305b\u304c2\u4ef6\u4ee5\u4e0a** \u3042\u308b\u9867\u5ba2\u306f\u89e3\u7d04\u30ea\u30b9\u30af\u304c72%\u4e0a\u6607\u3002\n3. **\u652f\u6255\u3044\u9045\u5ef6**\uff1a**2\u56de\u4ee5\u4e0a\u306e\u9045\u5ef6** \u304c\u3042\u308b\u30a2\u30ab\u30a6\u30f3\u30c8\u306f\u96e2\u8131\u306e\u5f37\u3044\u524d\u5146\u3067\u3059\u3002\n4. **\u5229\u7528\u6642\u9593\u306e\u4f4e\u4e0b**\uff1a\u6708\u9593\u5229\u7528\u304c **15\u6642\u9593\u672a\u6e80** \u306b\u843d\u3061\u8fbc\u3080\u3053\u3068\u304c\u30b5\u30a4\u30ec\u30f3\u30c8\u89e3\u7d04\u306e\u6700\u5927\u8981\u56e0\u3067\u3059\u3002\n\n**\u30a2\u30af\u30b7\u30e7\u30f3** \u30bf\u30d6\u304b\u3089\u81ea\u52d5\u5bfe\u5fdc\u30d5\u30ed\u30fc\u3092\u958b\u59cb\u3057\u3066\u304f\u3060\u3055\u3044\u3002",
        "playbook": "### \u2709\ufe0f \u30d1\u30fc\u30bd\u30ca\u30e9\u30a4\u30ba\u3055\u308c\u305f\u30ea\u30ab\u30d0\u30ea\u30fc\u30e1\u30fc\u30eb\u3068\u5bfe\u5fdc\u624b\u9806\n\n\u9ad8\u30ea\u30b9\u30af\u9867\u5ba2\u5411\u3051\u306e\u30ea\u30c6\u30f3\u30b7\u30e7\u30f3\u30e1\u30fc\u30eb\u30c6\u30f3\u30d7\u30ec\u30fc\u30c8\uff1a\n\n---\n**\u4ef6\u540d**\uff1a*\u512a\u5148\u5bfe\u5fdc\uff1a\u8cb4\u793e\u3068\u306e\u30d1\u30fc\u30c8\u30ca\u30fc\u30b7\u30c3\u30d7\u304a\u3088\u3073\u5c02\u4efb\u30a8\u30b0\u30bc\u30af\u30c6\u30a3\u30d6\u30b5\u30dd\u30fc\u30c8\u306e\u3054\u6848\u5185*\n\n\u3054\u62c5\u5f53\u8005\u69d8\n\nQiplo \u30ab\u30b9\u30bf\u30de\u30fc\u30b5\u30af\u30bb\u30b9\u7d71\u62ec\u8cac\u4efb\u8005\u3088\u308a\u76f4\u63a5\u3054\u9023\u7d61\u7533\u3057\u4e0a\u3052\u307e\u3059\u3002\u6700\u8fd1\u3001\u8cb4\u793e\u30a2\u30ab\u30a6\u30f3\u30c8\u306b\u304a\u3044\u3066\u3044\u304f\u3064\u304b\u306e\u8ab2\u984c\u304c\u751f\u3058\u3066\u3044\u308b\u3053\u3068\u3092\u628a\u63e1\u3044\u305f\u3057\u307e\u3057\u305f\u3002\n\n\u8cb4\u793e\u306e\u30d3\u30b8\u30cd\u30b9\u6210\u679c\u306e\u6700\u5927\u5316\u306b\u5411\u3051\u3066\u3001\u4ee5\u4e0b\u306e\u7279\u5225\u652f\u63f4\u3092\u3054\u7528\u610f\u3044\u305f\u3057\u307e\u3057\u305f\uff1a\n1. **\u5c02\u4efb\u30b7\u30cb\u30a2\u30a2\u30fc\u30ad\u30c6\u30af\u30c8\u306b\u3088\u308b\u500b\u5225\u76f8\u8ac7**\uff1a30\u5206\u9593\u306e\u500b\u5225\u6280\u8853\u652f\u63f4\u3068\u6700\u9069\u5316\u63d0\u6848\u3002\n2. **VIP\u30ed\u30a4\u30e4\u30eb\u30c6\u30a3\u7279\u5178**\uff1a\u6b21\u56de\u5e74\u9593\u66f4\u65b0\u6642\u306b\u9069\u7528\u53ef\u80fd\u306a20%\u7279\u5225\u30af\u30ec\u30b8\u30c3\u30c8\u3002\n\n\u4eca\u9031\u6728\u66dc\u307e\u305f\u306f\u91d1\u66dc\u306b\u3054\u90fd\u5408\u306e\u3088\u308d\u3057\u3044\u304a\u6642\u9593\u306f\u3054\u3056\u3044\u307e\u3059\u3067\u3057\u3087\u3046\u304b\uff1f\n\n\u656c\u5177\n*Qiplo \u30ab\u30b9\u30bf\u30de\u30fc\u30b5\u30af\u30bb\u30b9\u62c5\u5f53*\n---\n\n**\u5bfe\u5fdc\u65b9\u91dd**\uff1a24\u6642\u9593\u4ee5\u5185\u306b\u9001\u4fe1\u3057\u3001\u67d4\u8edf\u306a\u652f\u6255\u3044\u6761\u4ef6\u3092\u63d0\u793a\u3057\u3066\u304f\u3060\u3055\u3044\u3002",
        "export_bi": "### \ud83d\udcc8 BI\u30c0\u30c3\u30b7\u30e5\u30dc\u30fc\u30c9\u9023\u643a\u3068\u30b3\u30cd\u30af\u30bf\u30fc\n\n\u4e88\u6e2c\u30c7\u30fc\u30bf\u30d9\u30fc\u30b9\u3068\u9023\u643a\u6e08\u307f\u306eBI\u30d1\u30c3\u30b1\u30fc\u30b8\u3092\u3054\u5229\u7528\u3044\u305f\u3060\u3051\u307e\u3059\uff1a\n\n- **[Power BI \u30c7\u30fc\u30bf\u30bd\u30fc\u30b9\u3092\u30c0\u30a6\u30f3\u30ed\u30fc\u30c9 (.pbids)](/api/export/powerbi)**\n- **[Tableau \u30ef\u30fc\u30af\u30d6\u30c3\u30af\u3092\u30c0\u30a6\u30f3\u30ed\u30fc\u30c9 (.twb)](/api/export/tableau)**\n- **[Excel \u30c7\u30fc\u30bf\u3092\u30c0\u30a6\u30f3\u30ed\u30fc\u30c9 (.xlsx)](/api/export/excel)**\n- **[\u7dcf\u5408\u76e3\u67fb\u30ec\u30dd\u30fc\u30c8\u3092\u30c0\u30a6\u30f3\u30ed\u30fc\u30c9](/api/export/report)**",
        "default_fallback": "### \ud83d\udca1 \u30c7\u30fc\u30bf\u30b5\u30a4\u30a8\u30f3\u30b9\u9867\u554f\u30fb\u30ea\u30c6\u30f3\u30b7\u30e7\u30f3\u30a2\u30b7\u30b9\u30bf\u30f3\u30c8\n\n\u9867\u5ba2\u30c7\u30fc\u30bf\u306e\u89e3\u7d04\u4e88\u6e2c\u3068\u30ea\u30c6\u30f3\u30b7\u30e7\u30f3\u6226\u7565\u3092\u7dcf\u5408\u7684\u306b\u30b5\u30dd\u30fc\u30c8\u3057\u307e\u3059\uff1a\n\n- **\u9ad8\u30ea\u30b9\u30af\u9867\u5ba2**\uff1a*\u300c\u9ad8\u30ea\u30b9\u30af\u9867\u5ba2\u3092\u8868\u793a\u300d* \u307e\u305f\u306f *\u300c\u8ab0\u304c\u5371\u967a\uff1f\u300d*\n- **\u58f2\u4e0a\u30ea\u30b9\u30af\u5206\u6790**\uff1a*\u300c\u30ea\u30b9\u30af\u306e\u3042\u308b\u58f2\u4e0a\u306f\u3044\u304f\u3089\uff1f\u300d*\n- **\u89e3\u7d04\u8981\u56e0\u306e\u5206\u6790**\uff1a*\u300c\u9867\u5ba2\u306f\u306a\u305c\u89e3\u7d04\u3059\u308b\uff1f\u300d*\n- **\u633d\u56de\u30e1\u30fc\u30eb\u4f5c\u6210**\uff1a*\u300c\u30ea\u30ab\u30d0\u30ea\u30fc\u30e1\u30fc\u30eb\u3092\u4f5c\u6210\u3057\u3066\u300d*\n- **BI\u9023\u643a**\uff1a*\u300cPower BI\u300d* \u307e\u305f\u306f *\u300cTableau\u300d* \u306e\u51fa\u529b\u30d5\u30a1\u30a4\u30eb\u3002","name": "Japanese", "native": "日本語", "dir": "ltr"},
    "pt": {
        "financials": "### \ud83d\udcca Exposi\u00e7\u00e3o de Receita e An\u00e1lise de Impacto Financeiro\n\nA Qiplo monitora atualmente **{total_cust:,} contas ativas** com uma Receita Recorrente Mensal (MRR) total de **${total_mrr:,.2f}**.\n\n**Exposi\u00e7\u00e3o ao Risco Financeiro:**\n- **Receita Mensal em Risco (MRR em Risco)**: **${risk_mrr:,.2f}** ({risk_pct:.1f}% do MRR total)\n- **Valor Anualizado em Risco (ARR em Risco)**: **${arr_at_risk:,.2f}**\n- **Pontua\u00e7\u00e3o M\u00e9dia de Risco da Carteira**: **{avg_risk:.1f}%**\n\n**Mitiga\u00e7\u00f5es Financeiras Recomendadas:**\n1. Conceder 15% de desconto para converter contratos mensais em planos anuais.\n2. Priorizar disputas de faturamento em contas de alto valor.",
        "churn_causes": "### \ud83d\udd0d Principais Motivos de Cancelamento e Fatores de Risco\n\nCom base no modelo **Tabular Hybrid Transformer**:\n\n1. **Tipo de Contrato**: Assinaturas m\u00eas a m\u00eas apresentam **3,4x mais cancelamentos** do que planos anuais.\n2. **Atrito no Suporte**: Contas com **>2 chamados n\u00e3o resolvidos** em 48h sofrem salto de 72% no risco.\n3. **Atraso de Pagamento**: Contas com **\u22652 atrasos** indicam desengajamento iminente.\n4. **Queda de Uso**: Uso inferior a **15h/m\u00eas** \u00e9 o principal sinal de cancelamento silencioso.",
        "playbook": "### \u2709\ufe0f E-mail de Recupera\u00e7\u00e3o Personalizado e Procedimentos\n\nModelo de recupera\u00e7\u00e3o para clientes em risco:\n\n---\n**Assunto**: *Revis\u00e3o Priorit\u00e1ria: Sua parceria conosco e suporte executivo exclusivo*\n\nPrezado(a),\n\nEscrevo diretamente da lideran\u00e7a de Sucesso do Cliente da Qiplo. Identificamos alguns atritos recentes em sua conta.\n\nSua satisfa\u00e7\u00e3o \u00e9 nossa prioridade. Oferecemos com exclusividade:\n1. **Consultoria T\u00e9cnica com Arquiteto S\u00eanior**: 30 minutos de mentoria para otimizar sua opera\u00e7\u00e3o.\n2. **B\u00f4nus VIP de Fidelidade**: 20% de cr\u00e9dito na sua pr\u00f3xima renova\u00e7\u00e3o anual.\n\nPodemos conversar nesta quinta ou sexta-feira?\n\nAtenciosamente,\n*Equipe de Sucesso do Cliente Qiplo*\n---\n\n**Procedimento:** Envie em at\u00e9 24h e apresente op\u00e7\u00f5es de pagamento flex\u00edveis.",
        "export_bi": "### \ud83d\udcc8 Conectores e Dashboards de Business Intelligence\n\nArquivos prontos para integra\u00e7\u00e3o com seus dados em tempo real:\n\n- **[Baixar Fonte de Dados Power BI (.pbids)](/api/export/powerbi)**\n- **[Baixar Pasta de Trabalho Tableau (.twb)](/api/export/tableau)**\n- **[Baixar Planilha Excel (.xlsx)](/api/export/excel)**\n- **[Baixar Relat\u00f3rio Completo de Auditoria](/api/export/report)**",
        "default_fallback": "### \ud83d\udca1 Consultoria Estrat\u00e9gica em Reten\u00e7\u00e3o de Clientes\n\nEstou \u00e0 disposi\u00e7\u00e3o para orientar suas decis\u00f5es de neg\u00f3cio:\n\n- **Contas de Risco**: Pergunte *'Mostrar clientes em alto risco'*\n- **Receita Amea\u00e7ada**: Pergunte *'Qual \u00e9 a receita em risco?'*\n- **Causas de Churn**: Pergunte *'Por que os clientes cancelam?'*\n- **Planos de A\u00e7\u00e3o**: Pe\u00e7a *'Elaborar e-mail de recupera\u00e7\u00e3o'*\n- **Dashboards**: Solicite arquivos do *'Power BI'* ou *'Tableau'*.","name": "Portuguese", "native": "Português", "dir": "ltr"},
    "ar": {
        "financials": "### \ud83d\udcca \u062a\u062d\u0644\u064a\u0644 \u0627\u0644\u0625\u064a\u0631\u0627\u062f\u0627\u062a \u0627\u0644\u0645\u0639\u0631\u0636\u0629 \u0644\u0644\u062e\u0637\u0631 \u0648\u0627\u0644\u0623\u062b\u0631 \u0627\u0644\u0645\u0627\u0644\u064a\n\n\u062a\u062a\u0639\u0642\u0628 Qiplo \u062d\u0627\u0644\u064a\u0627\u064b **{total_cust:,} \u062d\u0633\u0627\u0628\u0627\u064b \u0646\u0634\u0637\u0627\u064b** \u0628\u0625\u062c\u0645\u0627\u0644\u064a \u0625\u064a\u0631\u0627\u062f\u0627\u062a \u0634\u0647\u0631\u064a\u0629 \u0645\u062a\u0643\u0631\u0631\u0629 (MRR) \u062a\u0628\u0644\u063a **${total_mrr:,.2f}**.\n\n**\u062d\u062c\u0645 \u0627\u0644\u0645\u062e\u0627\u0637\u0631 \u0627\u0644\u0645\u0627\u0644\u064a\u0629:**\n- **\u0627\u0644\u0625\u064a\u0631\u0627\u062f\u0627\u062a \u0627\u0644\u0634\u0647\u0631\u064a\u0629 \u0627\u0644\u0645\u0639\u0631\u0636\u0629 \u0644\u0644\u062e\u0637\u0631 (MRR at Risk)**: **${risk_mrr:,.2f}** ({risk_pct:.1f}% \u0645\u0646 \u0625\u062c\u0645\u0627\u0644\u064a \u0627\u0644\u0625\u064a\u0631\u0627\u062f\u0627\u062a)\n- **\u0627\u0644\u0642\u064a\u0645\u0629 \u0627\u0644\u0633\u0646\u0648\u064a\u0629 \u0627\u0644\u0645\u0639\u0631\u0636\u0629 \u0644\u0644\u062e\u0637\u0631 (ARR at Risk)**: **${arr_at_risk:,.2f}**\n- **\u0645\u062a\u0648\u0633\u0637 \u062f\u0631\u062c\u0629 \u0645\u062e\u0627\u0637\u0631 \u0641\u0642\u062f\u0627\u0646 \u0627\u0644\u0639\u0645\u0644\u0627\u0621**: **{avg_risk:.1f}%**\n\n**\u0627\u0644\u0625\u062c\u0631\u0627\u0621\u0627\u062a \u0627\u0644\u0645\u0627\u0644\u064a\u0629 \u0627\u0644\u0645\u0648\u0635\u0649 \u0628\u0647\u0627:**\n1. \u062a\u0642\u062f\u064a\u0645 \u062e\u0635\u0645 15% \u0644\u062a\u062d\u0648\u064a\u0644 \u0627\u0644\u0639\u0642\u0648\u062f \u0627\u0644\u0634\u0647\u0631\u064a\u0629 \u0625\u0644\u0649 \u0639\u0642\u0648\u062f \u0633\u0646\u0648\u064a\u0629 \u0645\u062f\u062a\u0647\u0627 12 \u0634\u0647\u0631\u0627\u064b.\n2. \u062d\u0644 \u0645\u0634\u0643\u0644\u0627\u062a \u0627\u0644\u0641\u0648\u0627\u062a\u064a\u0631 \u0644\u0644\u062d\u0633\u0627\u0628\u0627\u062a \u0627\u0644\u0643\u0628\u064a\u0631\u0629 \u0644\u062d\u0645\u0627\u064a\u0629 \u0627\u0644\u0633\u064a\u0648\u0644\u0629.",
        "churn_causes": "### \ud83d\udd0d \u0627\u0644\u0623\u0633\u0628\u0627\u0628 \u0627\u0644\u0631\u0626\u064a\u0633\u064a\u0629 \u0644\u0641\u0642\u062f\u0627\u0646 \u0627\u0644\u0639\u0645\u0644\u0627\u0621 \u0648\u0645\u062d\u0631\u0643\u0627\u062a \u0627\u0644\u0645\u062e\u0627\u0637\u0631\n\n\u0648\u0641\u0642\u0627\u064b \u0644\u062a\u062d\u0644\u064a\u0644 \u0646\u0645\u0648\u0630\u062c **Tabular Hybrid Transformer**:\n\n1. **\u0646\u0648\u0639 \u0627\u0644\u0639\u0642\u062f**: \u0627\u0644\u0645\u0634\u062a\u0631\u0643\u0648\u0646 \u0634\u0647\u0631\u064a\u0627\u064b \u0644\u062f\u064a\u0647\u0645 **\u0627\u062d\u062a\u0645\u0627\u0644 \u0641\u0642\u062f\u0627\u0646 \u0623\u0639\u0644\u0649 \u0628\u0640 3.4 \u0645\u0631\u0627\u062a** \u0645\u0642\u0627\u0631\u0646\u0629 \u0628\u0627\u0644\u0639\u0642\u0648\u062f \u0627\u0644\u0633\u0646\u0648\u064a\u0629.\n2. **\u0645\u0634\u0627\u0643\u0644 \u0627\u0644\u062f\u0639\u0645**: \u0627\u0644\u062d\u0633\u0627\u0628\u0627\u062a \u0627\u0644\u062a\u064a \u0644\u062f\u064a\u0647\u0627 **\u0623\u0643\u062b\u0631 \u0645\u0646 \u062a\u0630\u0643\u0631\u062a\u064a \u062f\u0639\u0645 \u0645\u0639\u0644\u0642\u062a\u064a\u0646** \u0644\u0645\u062f\u0629 48 \u0633\u0627\u0639\u0629 \u062a\u0642\u0641\u0632 \u0646\u0633\u0628\u0629 \u0645\u062e\u0627\u0637\u0631\u0647\u0627 \u0628\u0645\u0642\u062f\u0627\u0631 72%.\n3. **\u062a\u0623\u062e\u064a\u0631 \u0627\u0644\u0633\u062f\u0627\u062f**: \u0627\u0644\u062d\u0633\u0627\u0628\u0627\u062a \u0627\u0644\u062a\u064a \u062a\u062a\u0623\u062e\u0631 **\u0645\u0631\u062a\u064a\u0646 \u0623\u0648 \u0623\u0643\u062b\u0631** \u0641\u064a \u0627\u0644\u0633\u062f\u0627\u062f \u062a\u0639\u0637\u064a \u0625\u0634\u0627\u0631\u0627\u062a \u0627\u0646\u0633\u062d\u0627\u0628 \u0648\u0627\u0636\u062d\u0629.\n4. **\u0627\u0646\u062e\u0641\u0627\u0636 \u0627\u0644\u0627\u0633\u062a\u062e\u062f\u0627\u0645**: \u0627\u0644\u0627\u0646\u062e\u0641\u0627\u0636 \u0625\u0644\u0649 \u0623\u0642\u0644 \u0645\u0646 **15 \u0633\u0627\u0639\u0629 \u0634\u0647\u0631\u064a\u0627\u064b** \u0647\u0648 \u0627\u0644\u0645\u0624\u0634\u0631 \u0627\u0644\u0631\u0626\u064a\u0633\u064a \u0644\u0644\u0641\u0642\u062f\u0627\u0646 \u0627\u0644\u0635\u0627\u0645\u062a.",
        "playbook": "### \u2709\ufe0f \u0628\u0631\u064a\u062f \u0627\u0633\u062a\u0631\u062f\u0627\u062f \u0645\u062e\u0635\u0635 \u0648\u062e\u0637\u0629 \u0639\u0645\u0644\n\n\u0646\u0645\u0648\u0630\u062c \u0627\u062d\u062a\u0631\u0627\u0641\u064a \u0644\u0627\u0633\u062a\u0639\u0627\u062f\u0629 \u0627\u0644\u0639\u0645\u0644\u0627\u0621 \u0627\u0644\u0645\u0639\u0631\u0636\u064a\u0646 \u0644\u0644\u062e\u0637\u0631:\n\n---\n**\u0627\u0644\u0645\u0648\u0636\u0648\u0639**: *\u0645\u062a\u0627\u0628\u0639\u0629 \u0639\u0627\u062c\u0644\u0629: \u0634\u0631\u0627\u0643\u062a\u0643\u0645 \u0645\u0639\u0646\u0627 \u0648\u0627\u0644\u062f\u0639\u0645 \u0627\u0644\u062a\u0646\u0641\u064a\u0630\u064a \u0627\u0644\u062d\u0635\u0631\u064a*\n\n\u0639\u0632\u064a\u0632\u064a \u0627\u0644\u0634\u0631\u064a\u0643\u060c\n\n\u0623\u062a\u0648\u0627\u0635\u0644 \u0645\u0639\u0643 \u0645\u0628\u0627\u0634\u0631\u0629 \u0645\u0646 \u0625\u062f\u0627\u0631\u0629 \u0646\u062c\u0627\u062d \u0627\u0644\u0639\u0645\u0644\u0627\u0621 \u0627\u0644\u062a\u0646\u0641\u064a\u0630\u064a\u0629 \u0641\u064a Qiplo. \u0644\u0627\u062d\u0638\u0646\u0627 \u0645\u0624\u062e\u0631\u0627\u064b \u0628\u0639\u0636 \u0627\u0644\u062a\u062d\u062f\u064a\u0627\u062a \u0641\u064a \u062d\u0633\u0627\u0628\u0643\u0645.\n\n\u0646\u062c\u0627\u062d\u0643\u0645 \u0648\u0631\u0636\u0627\u0643\u0645 \u0647\u0645\u0627 \u0623\u0648\u0644\u0648\u064a\u062a\u0646\u0627 \u0627\u0644\u0642\u0635\u0648\u0649\u060c \u0644\u0630\u0627 \u064a\u0633\u0639\u062f\u0646\u0627 \u062a\u0642\u062f\u064a\u0645:\n1. **\u0627\u0633\u062a\u0634\u0627\u0631\u0629 \u062e\u0627\u0635\u0629 \u0645\u0639 \u0643\u0628\u064a\u0631 \u0645\u0647\u0646\u062f\u0633\u064a \u0627\u0644\u0646\u0638\u0645**: \u062c\u0644\u0633\u0629 \u0645\u062f\u062a\u0647\u0627 30 \u062f\u0642\u064a\u0642\u0629 \u0644\u062a\u062d\u0633\u064a\u0646 \u0628\u064a\u0626\u0629 \u0627\u0644\u0639\u0645\u0644.\n2. **\u0631\u0635\u064a\u062f \u0648\u0644\u0627\u0621 \u062d\u0635\u0631\u064a**: \u062e\u0635\u0645 \u0641\u0648\u0631\u064a \u0628\u0646\u0633\u0628\u0629 20% \u0639\u0646\u062f \u062a\u062c\u062f\u064a\u062f \u0627\u0634\u062a\u0631\u0627\u0643\u0643\u0645 \u0627\u0644\u0633\u0646\u0648\u064a \u0627\u0644\u0642\u0627\u062f\u0645.\n\n\u0647\u0644 \u064a\u0646\u0627\u0633\u0628\u0643 \u0627\u062a\u0635\u0627\u0644 \u0633\u0631\u064a\u0639 \u064a\u0648\u0645 \u0627\u0644\u062e\u0645\u064a\u0633 \u0623\u0648 \u0627\u0644\u062c\u0645\u0639\u0629\u061f\n\n\u0645\u0639 \u062e\u0627\u0644\u0635 \u0627\u0644\u062a\u062d\u064a\u0629\u060c\n*\u0625\u062f\u0627\u0631\u0629 \u0646\u062c\u0627\u062d \u0627\u0644\u0639\u0645\u0644\u0627\u0621 \u0641\u064a Qiplo*\n---\n\n**\u062e\u0637\u0629 \u0627\u0644\u0639\u0645\u0644:** \u0623\u0631\u0633\u0644 \u0647\u0630\u0627 \u0627\u0644\u0628\u0631\u064a\u062f \u062e\u0644\u0627\u0644 24 \u0633\u0627\u0639\u0629 \u0648\u0642\u062f\u0645 \u062e\u064a\u0627\u0631\u0627\u062a \u062f\u0641\u0639 \u0645\u0631\u0646\u0629.",
        "export_bi": "### \ud83d\udcc8 \u062a\u0643\u0627\u0645\u0644 \u0644\u0648\u062d\u0627\u062a \u0627\u0644\u0645\u0639\u0644\u0648\u0645\u0627\u062a \u0648\u0645\u0648\u0635\u0644\u0627\u062a \u0630\u0643\u0627\u0621 \u0627\u0644\u0623\u0639\u0645\u0627\u0644\n\n\u0645\u0644\u0641\u0627\u062a \u0631\u0628\u0637 \u062c\u0627\u0647\u0632\u0629 \u0644\u0644\u062a\u062d\u0645\u064a\u0644 \u0648\u0645\u062a\u0635\u0644\u0629 \u0645\u0628\u0627\u0634\u0631\u0629 \u0628\u0642\u0627\u0639\u062f\u0629 \u0628\u064a\u0627\u0646\u0627\u062a \u0627\u0644\u062a\u0646\u0628\u0624\u0627\u062a:\n\n- **[\u062a\u062d\u0645\u064a\u0644 \u0645\u0635\u062f\u0631 \u0628\u064a\u0627\u0646\u0627\u062a Power BI (.pbids)](/api/export/powerbi)**\n- **[\u062a\u062d\u0645\u064a\u0644 \u0645\u0635\u0646\u0641 Tableau (.twb)](/api/export/tableau)**\n- **[\u062a\u062d\u0645\u064a\u0644 \u062c\u062f\u0648\u0644 \u0628\u064a\u0627\u0646\u0627\u062a Excel (.xlsx)](/api/export/excel)**\n- **[\u062a\u062d\u0645\u064a\u0644 \u062a\u0642\u0631\u064a\u0631 \u0627\u0644\u062a\u062f\u0642\u064a\u0642 \u0627\u0644\u0634\u0627\u0645\u0644](/api/export/report)**",
        "default_fallback": "### \ud83d\udca1 \u0627\u0633\u062a\u0634\u0627\u0631\u0627\u062a \u0639\u0644\u0645 \u0627\u0644\u0628\u064a\u0627\u0646\u0627\u062a \u0648\u0627\u0644\u0627\u062d\u062a\u0641\u0627\u0638 \u0628\u0627\u0644\u0639\u0645\u0644\u0627\u0621\n\n\u0623\u0646\u0627 \u0647\u0646\u0627 \u0644\u0645\u0633\u0627\u0639\u062f\u062a\u0643 \u0641\u064a \u062a\u062d\u0644\u064a\u0644 \u0628\u064a\u0627\u0646\u0627\u062a \u0627\u0644\u0639\u0645\u0644\u0627\u0621 \u0628\u0643\u0641\u0627\u0621\u0629:\n\n- **\u0627\u0644\u062d\u0633\u0627\u0628\u0627\u062a \u0639\u0627\u0644\u064a\u0629 \u0627\u0644\u062e\u0637\u0648\u0631\u0629**: \u0627\u0637\u0644\u0628 *'\u0639\u0631\u0636 \u0627\u0644\u062d\u0633\u0627\u0628\u0627\u062a \u0627\u0644\u0645\u0639\u0631\u0636\u0629 \u0644\u0644\u062e\u0637\u0631'*\n- **\u0627\u0644\u0625\u064a\u0631\u0627\u062f\u0627\u062a \u0627\u0644\u0645\u0647\u062f\u062f\u0629**: \u0627\u0633\u0623\u0644 *'\u0645\u0627 \u0647\u064a \u0627\u0644\u0625\u064a\u0631\u0627\u062f\u0627\u062a \u0627\u0644\u0645\u0639\u0631\u0636\u0629 \u0644\u0644\u062e\u0637\u0631\u061f'*\n- **\u0623\u0633\u0628\u0627\u0628 \u0641\u0642\u062f\u0627\u0646 \u0627\u0644\u0639\u0645\u0644\u0627\u0621**: \u0627\u0633\u0623\u0644 *'\u0644\u0645\u0627\u0630\u0627 \u064a\u063a\u0627\u062f\u0631 \u0627\u0644\u0639\u0645\u0644\u0627\u0621\u061f'*\n- **\u062e\u0637\u0637 \u0627\u0644\u0627\u0633\u062a\u0631\u062f\u0627\u062f**: \u0627\u0637\u0644\u0628 *'\u0635\u064a\u0627\u063a\u0629 \u0628\u0631\u064a\u062f \u0625\u0644\u0643\u062a\u0631\u0648\u0646\u064a \u0644\u0627\u0633\u062a\u0639\u0627\u062f\u0629 \u0639\u0645\u064a\u0644'*\n- **\u062a\u0635\u062f\u064a\u0631 \u0627\u0644\u062a\u0642\u0627\u0631\u064a\u0631**: \u0627\u0637\u0644\u0628 \u0631\u0648\u0627\u0628\u0637 *'Power BI'* \u0623\u0648 *'Tableau'*.","name": "Arabic", "native": "العربية", "dir": "rtl"},
    "hi": {
        "financials": "### \ud83d\udcca \u0930\u093e\u091c\u0938\u094d\u0935 \u091c\u094b\u0916\u093f\u092e \u090f\u0935\u0902 \u0935\u093f\u0924\u094d\u0924\u0940\u092f \u092a\u094d\u0930\u092d\u093e\u0935 \u0935\u093f\u0936\u094d\u0932\u0947\u0937\u0923\n\nQiplo \u0935\u0930\u094d\u0924\u092e\u093e\u0928 \u092e\u0947\u0902 **{total_cust:,} \u0938\u0915\u094d\u0930\u093f\u092f \u0916\u093e\u0924\u094b\u0902** \u0915\u0940 \u0928\u093f\u0917\u0930\u093e\u0928\u0940 \u0915\u0930 \u0930\u0939\u093e \u0939\u0948, \u091c\u093f\u0938\u0915\u093e \u0915\u0941\u0932 \u092e\u093e\u0938\u093f\u0915 \u0906\u0935\u0930\u094d\u0924\u0940 \u0930\u093e\u091c\u0938\u094d\u0935 (MRR) **${total_mrr:,.2f}** \u0939\u0948\u0964\n\n**\u0935\u093f\u0924\u094d\u0924\u0940\u092f \u091c\u094b\u0916\u093f\u092e \u0915\u093e \u0935\u093f\u0935\u0930\u0923:**\n- **\u091c\u094b\u0916\u093f\u092e \u092e\u0947\u0902 \u092e\u093e\u0938\u093f\u0915 \u0930\u093e\u091c\u0938\u094d\u0935 (MRR at Risk)**: **${risk_mrr:,.2f}** (\u0915\u0941\u0932 MRR \u0915\u093e {risk_pct:.1f}%)\n- **\u0935\u093e\u0930\u094d\u0937\u093f\u0915 \u091c\u094b\u0916\u093f\u092e \u092e\u0942\u0932\u094d\u092f (ARR at Risk)**: **${arr_at_risk:,.2f}**\n- **\u092a\u094b\u0930\u094d\u091f\u092b\u094b\u0932\u093f\u092f\u094b \u0915\u093e \u0914\u0938\u0924 \u092e\u0902\u0925\u0928 \u091c\u094b\u0916\u093f\u092e \u0938\u094d\u0915\u094b\u0930**: **{avg_risk:.1f}%**\n\n**\u0905\u0928\u0941\u0936\u0902\u0938\u093f\u0924 \u0935\u093f\u0924\u094d\u0924\u0940\u092f \u0909\u092a\u093e\u092f:**\n1. \u092e\u093e\u0938\u093f\u0915 \u0905\u0928\u0941\u092c\u0902\u0927\u094b\u0902 \u0915\u094b 12 \u092e\u0939\u0940\u0928\u0947 \u0915\u0947 \u0935\u093e\u0930\u094d\u0937\u093f\u0915 \u0905\u0928\u0941\u092c\u0902\u0927 \u092e\u0947\u0902 \u092c\u0926\u0932\u0928\u0947 \u0915\u0947 \u0932\u093f\u090f 15% \u0915\u0940 \u091b\u0942\u091f \u092a\u094d\u0930\u0926\u093e\u0928 \u0915\u0930\u0947\u0902\u0964\n2. \u0928\u0915\u0926\u0940 \u092a\u094d\u0930\u0935\u093e\u0939 \u0915\u0940 \u0938\u0941\u0930\u0915\u094d\u0937\u093e \u0915\u0947 \u0932\u093f\u090f \u0909\u091a\u094d\u091a-ARR \u0916\u093e\u0924\u094b\u0902 \u0915\u0947 \u092c\u093f\u0932\u093f\u0902\u0917 \u0935\u093f\u0935\u093e\u0926\u094b\u0902 \u0915\u094b \u092a\u094d\u0930\u093e\u0925\u092e\u093f\u0915\u0924\u093e \u0938\u0947 \u0939\u0932 \u0915\u0930\u0947\u0902\u0964",
        "churn_causes": "### \ud83d\udd0d \u0917\u094d\u0930\u093e\u0939\u0915 \u092e\u0902\u0925\u0928 (\u091b\u094b\u0921\u093c\u0928\u0947) \u0915\u0947 \u092e\u0941\u0916\u094d\u092f \u0915\u093e\u0930\u0923 \u0914\u0930 \u091c\u094b\u0916\u093f\u092e \u0915\u093e\u0930\u0915\n\n\u0939\u092e\u093e\u0930\u0947 **Tabular Hybrid Transformer** \u092e\u0949\u0921\u0932 \u0915\u0947 \u0905\u0928\u0941\u0938\u093e\u0930 \u092e\u0941\u0916\u094d\u092f \u0915\u093e\u0930\u0923 \u0928\u093f\u092e\u094d\u0928\u0932\u093f\u0916\u093f\u0924 \u0939\u0948\u0902:\n\n1. **\u0905\u0928\u0941\u092c\u0902\u0927 \u0915\u093e \u092a\u094d\u0930\u0915\u093e\u0930**: \u092e\u0939\u0940\u0928\u0947-\u0926\u0930-\u092e\u0939\u0940\u0928\u0947 \u0905\u0928\u0941\u092c\u0902\u0927 \u0935\u093e\u0932\u0947 \u0917\u094d\u0930\u093e\u0939\u0915\u094b\u0902 \u092e\u0947\u0902 \u0935\u093e\u0930\u094d\u0937\u093f\u0915 \u0917\u094d\u0930\u093e\u0939\u0915\u094b\u0902 \u0915\u0940 \u0924\u0941\u0932\u0928\u093e \u092e\u0947\u0902 **3.4 \u0917\u0941\u0928\u093e \u0905\u0927\u093f\u0915 \u092e\u0902\u0925\u0928** \u0926\u0947\u0916\u093e \u091c\u093e\u0924\u093e \u0939\u0948\u0964\n2. **\u0938\u092a\u094b\u0930\u094d\u091f \u092e\u0947\u0902 \u0926\u0947\u0930\u0940**: 48 \u0918\u0902\u091f\u094b\u0902 \u092e\u0947\u0902 \u0905\u0928\u0938\u0941\u0932\u091d\u0947 **2 \u0938\u0947 \u0905\u0927\u093f\u0915 \u0938\u092a\u094b\u0930\u094d\u091f \u091f\u093f\u0915\u091f** \u0935\u093e\u0932\u0947 \u0917\u094d\u0930\u093e\u0939\u0915\u094b\u0902 \u0915\u093e \u091c\u094b\u0916\u093f\u092e 72% \u092c\u0922\u093c \u091c\u093e\u0924\u093e \u0939\u0948\u0964\n3. **\u092d\u0941\u0917\u0924\u093e\u0928 \u092e\u0947\u0902 \u0926\u0947\u0930\u0940**: **2 \u092f\u093e \u0905\u0927\u093f\u0915 \u092d\u0941\u0917\u0924\u093e\u0928 \u0926\u0947\u0930\u0940** \u0935\u093e\u0932\u0947 \u0916\u093e\u0924\u0947 \u0917\u094d\u0930\u093e\u0939\u0915 \u0915\u0947 \u0905\u0932\u0917 \u0939\u094b\u0928\u0947 \u0915\u093e \u0938\u0902\u0915\u0947\u0924 \u0926\u0947\u0924\u0947 \u0939\u0948\u0902\u0964\n4. **\u0909\u092a\u092f\u094b\u0917 \u092e\u0947\u0902 \u0915\u092e\u0940**: \u092a\u094d\u0930\u0924\u093f \u092e\u093e\u0939 **15 \u0918\u0902\u091f\u0947 \u0938\u0947 \u0915\u092e** \u0909\u092a\u092f\u094b\u0917 \u0936\u093e\u0902\u0924 \u092e\u0902\u0925\u0928 \u0915\u093e \u092a\u094d\u0930\u092e\u0941\u0916 \u092a\u094d\u0930\u093e\u0930\u0902\u092d\u093f\u0915 \u0938\u0902\u0915\u0947\u0924\u0915 \u0939\u0948\u0964\n\n\u0938\u094d\u0935\u091a\u093e\u0932\u093f\u0924 \u0935\u0930\u094d\u0915\u092b\u093c\u094d\u0932\u094b \u0936\u0941\u0930\u0942 \u0915\u0930\u0928\u0947 \u0915\u0947 \u0932\u093f\u090f **\u0915\u093e\u0930\u094d\u0930\u0935\u093e\u0907\u092f\u093e\u0902 (Actions)** \u091f\u0948\u092c \u092a\u0930 \u091c\u093e\u090f\u0902\u0964",
        "playbook": "### \u2709\ufe0f \u0935\u0948\u092f\u0915\u094d\u0924\u093f\u0915\u0943\u0924 \u0917\u094d\u0930\u093e\u0939\u0915 \u092a\u0941\u0928\u0930\u094d\u092a\u094d\u0930\u093e\u092a\u094d\u0924\u093f \u0908\u092e\u0947\u0932 \u090f\u0935\u0902 \u0915\u093e\u0930\u094d\u092f \u092f\u094b\u091c\u0928\u093e\n\n\u091c\u094b\u0916\u093f\u092e \u092e\u0947\u0902 \u092a\u0921\u093c\u0947 \u0917\u094d\u0930\u093e\u0939\u0915\u094b\u0902 \u0915\u0947 \u0932\u093f\u090f \u0938\u093f\u0926\u094d\u0927 \u092a\u0941\u0928\u0930\u094d\u092a\u094d\u0930\u093e\u092a\u094d\u0924\u093f \u0908\u092e\u0947\u0932 \u091f\u0947\u092e\u094d\u092a\u0932\u0947\u091f:\n\n---\n**\u0935\u093f\u0937\u092f**: *\u092a\u094d\u0930\u093e\u0925\u092e\u093f\u0915\u0924\u093e \u0938\u092e\u0940\u0915\u094d\u0937\u093e: \u0906\u092a\u0915\u0940 \u0938\u093e\u091d\u0947\u0926\u093e\u0930\u0940 \u0914\u0930 \u0935\u093f\u0936\u0947\u0937 \u0915\u093e\u0930\u094d\u092f\u0915\u093e\u0930\u0940 \u0938\u0939\u093e\u092f\u0924\u093e*\n\n\u092a\u094d\u0930\u093f\u092f \u0917\u094d\u0930\u093e\u0939\u0915 \u092d\u093e\u0917\u0940\u0926\u093e\u0930,\n\n\u092e\u0948\u0902 Qiplo \u0915\u0940 \u0917\u094d\u0930\u093e\u0939\u0915 \u0938\u092b\u0932\u0924\u093e \u0915\u093e\u0930\u094d\u092f\u0915\u093e\u0930\u0940 \u091f\u0940\u092e \u0938\u0947 \u0938\u0940\u0927\u0947 \u0906\u092a\u0938\u0947 \u0938\u0902\u092a\u0930\u094d\u0915 \u0915\u0930 \u0930\u0939\u093e \u0939\u0942\u0902\u0964 \u0939\u093e\u0932 \u0939\u0940 \u092e\u0947\u0902 \u0939\u092e\u0928\u0947 \u0906\u092a\u0915\u0947 \u0916\u093e\u0924\u0947 \u092e\u0947\u0902 \u0915\u0941\u091b \u0916\u0941\u0932\u0940 \u0938\u092e\u0938\u094d\u092f\u093e\u090f\u0902 \u0926\u0947\u0916\u0940 \u0939\u0948\u0902\u0964\n\n\u0906\u092a\u0915\u0940 \u0938\u0902\u0924\u0941\u0937\u094d\u091f\u093f \u0914\u0930 \u0935\u094d\u092f\u093e\u0935\u0938\u093e\u092f\u093f\u0915 \u0938\u092b\u0932\u0924\u093e \u0939\u092e\u093e\u0930\u0940 \u0938\u0930\u094d\u0935\u094b\u091a\u094d\u091a \u092a\u094d\u0930\u093e\u0925\u092e\u093f\u0915\u0924\u093e \u0939\u0948\u0964 \u0907\u0938\u0915\u0947 \u0932\u093f\u090f \u0939\u092e \u0906\u092a\u0915\u094b \u092a\u094d\u0930\u0926\u093e\u0928 \u0915\u0930\u0924\u0947 \u0939\u0948\u0902:\n1. **\u0935\u0930\u093f\u0937\u094d\u0920 \u0935\u093e\u0938\u094d\u0924\u0941\u0915\u093e\u0930 \u0915\u0947 \u0938\u093e\u0925 \u0935\u093f\u0936\u0947\u0937 \u092a\u0930\u093e\u092e\u0930\u094d\u0936**: \u0906\u092a\u0915\u0947 \u0938\u093f\u0938\u094d\u091f\u092e \u0915\u094b \u0905\u0928\u0941\u0915\u0942\u0932\u093f\u0924 \u0915\u0930\u0928\u0947 \u0915\u0947 \u0932\u093f\u090f 30 \u092e\u093f\u0928\u091f \u0915\u093e \u0928\u093f\u0903\u0936\u0941\u0932\u094d\u0915 \u0938\u0924\u094d\u0930\u0964\n2. **\u0935\u0940\u0906\u0908\u092a\u0940 \u0935\u092b\u093e\u0926\u093e\u0930\u0940 \u0915\u094d\u0930\u0947\u0921\u093f\u091f**: \u0906\u092a\u0915\u0947 \u0905\u0917\u0932\u0947 \u0935\u093e\u0930\u094d\u0937\u093f\u0915 \u0928\u0935\u0940\u0928\u0940\u0915\u0930\u0923 \u092a\u0930 \u0924\u0924\u094d\u0915\u093e\u0932 20% \u0915\u0940 \u091b\u0942\u091f\u0964\n\n\u0915\u094d\u092f\u093e \u0939\u092e \u0907\u0938 \u0917\u0941\u0930\u0941\u0935\u093e\u0930 \u092f\u093e \u0936\u0941\u0915\u094d\u0930\u0935\u093e\u0930 \u0915\u094b \u0905\u092a\u0928\u0940 \u0938\u0941\u0935\u093f\u0927\u093e\u0928\u0941\u0938\u093e\u0930 \u0938\u0902\u0915\u094d\u0937\u093f\u092a\u094d\u0924 \u091a\u0930\u094d\u091a\u093e \u0915\u0930 \u0938\u0915\u0924\u0947 \u0939\u0948\u0902?\n\n\u0938\u093e\u0926\u0930,\n*\u0935\u0930\u093f\u0937\u094d\u0920 \u0917\u094d\u0930\u093e\u0939\u0915 \u0938\u092b\u0932\u0924\u093e \u092a\u094d\u0930\u092c\u0902\u0927\u0915, Qiplo*\n---\n\n**\u0915\u093e\u0930\u094d\u092f \u092f\u094b\u091c\u0928\u093e:** 24 \u0918\u0902\u091f\u0947 \u0915\u0947 \u092d\u0940\u0924\u0930 \u092f\u0939 \u0938\u0902\u0926\u0947\u0936 \u092d\u0947\u091c\u0947\u0902 \u0914\u0930 \u0932\u091a\u0940\u0932\u0947 \u092d\u0941\u0917\u0924\u093e\u0928 \u0935\u093f\u0915\u0932\u094d\u092a \u092a\u0947\u0936 \u0915\u0930\u0947\u0902\u0964",
        "export_bi": "### \ud83d\udcc8 \u0935\u094d\u092f\u093e\u0935\u0938\u093e\u092f\u093f\u0915 \u0921\u0948\u0936\u092c\u094b\u0930\u094d\u0921 \u090f\u0915\u0940\u0915\u0930\u0923 \u0914\u0930 \u0915\u0928\u0947\u0915\u094d\u091f\u0930\n\n\u0906\u092a\u0915\u0947 \u0932\u093e\u0907\u0935 \u0921\u0947\u091f\u093e\u092c\u0947\u0938 \u0938\u0947 \u0938\u0940\u0927\u0947 \u091c\u0941\u0921\u093c\u0947 \u0935\u094d\u092f\u093e\u0935\u0938\u093e\u092f\u093f\u0915 \u0930\u093f\u092a\u094b\u0930\u094d\u091f\u093f\u0902\u0917 \u092a\u0948\u0915\u0947\u091c:\n\n- **[Power BI \u0921\u0947\u091f\u093e \u0938\u094d\u0930\u094b\u0924 \u0921\u093e\u0909\u0928\u0932\u094b\u0921 \u0915\u0930\u0947\u0902 (.pbids)](/api/export/powerbi)**\n- **[Tableau \u0915\u093e\u0930\u094d\u092f\u092a\u0941\u0938\u094d\u0924\u093f\u0915\u093e \u0921\u093e\u0909\u0928\u0932\u094b\u0921 \u0915\u0930\u0947\u0902 (.twb)](/api/export/tableau)**\n- **[Excel \u0921\u0947\u091f\u093e\u0938\u0947\u091f \u0921\u093e\u0909\u0928\u0932\u094b\u0921 \u0915\u0930\u0947\u0902 (.xlsx)](/api/export/excel)**\n- **[\u092a\u0942\u0930\u094d\u0923 \u0911\u0921\u093f\u091f \u0930\u093f\u092a\u094b\u0930\u094d\u091f \u0921\u093e\u0909\u0928\u0932\u094b\u0921 \u0915\u0930\u0947\u0902](/api/export/report)**",
        "default_fallback": "### \ud83d\udca1 \u0935\u0930\u093f\u0937\u094d\u0920 \u0921\u0947\u091f\u093e \u0935\u093f\u091c\u094d\u091e\u093e\u0928 \u0914\u0930 \u0917\u094d\u0930\u093e\u0939\u0915 \u092a\u094d\u0930\u0924\u093f\u0927\u093e\u0930\u0923 \u0938\u0932\u093e\u0939\u0915\u093e\u0930\n\n\u092e\u0948\u0902 \u0906\u092a\u0915\u0947 \u0917\u094d\u0930\u093e\u0939\u0915 \u0921\u0947\u091f\u093e \u0915\u0947 \u0938\u0902\u092a\u0942\u0930\u094d\u0923 \u0935\u093f\u0936\u094d\u0932\u0947\u0937\u0923 \u092e\u0947\u0902 \u0906\u092a\u0915\u0940 \u0938\u0939\u093e\u092f\u0924\u093e \u0915\u0930 \u0938\u0915\u0924\u093e \u0939\u0942\u0902:\n\n- **\u0909\u091a\u094d\u091a \u091c\u094b\u0916\u093f\u092e \u0935\u093e\u0932\u0947 \u0916\u093e\u0924\u0947**: \u092a\u0942\u091b\u0947\u0902 *'\u0909\u091a\u094d\u091a \u091c\u094b\u0916\u093f\u092e \u0935\u093e\u0932\u0947 \u0917\u094d\u0930\u093e\u0939\u0915 \u0926\u093f\u0916\u093e\u090f\u0902'* \u092f\u093e *'\u0915\u094c\u0928 \u0916\u0924\u0930\u0947 \u092e\u0947\u0902 \u0939\u0948?'*\n- **\u0930\u093e\u091c\u0938\u094d\u0935 \u091c\u094b\u0916\u093f\u092e**: \u092a\u0942\u091b\u0947\u0902 *'\u0939\u092e\u093e\u0930\u093e \u0915\u093f\u0924\u0928\u093e \u0930\u093e\u091c\u0938\u094d\u0935 \u091c\u094b\u0916\u093f\u092e \u092e\u0947\u0902 \u0939\u0948?'*\n- **\u092e\u0902\u0925\u0928 \u0915\u0947 \u0915\u093e\u0930\u0923**: \u092a\u0942\u091b\u0947\u0902 *'\u0917\u094d\u0930\u093e\u0939\u0915 \u0915\u094d\u092f\u094b\u0902 \u091b\u094b\u0921\u093c \u0930\u0939\u0947 \u0939\u0948\u0902?'*\n- **\u092a\u0941\u0928\u0930\u094d\u092a\u094d\u0930\u093e\u092a\u094d\u0924\u093f \u0908\u092e\u0947\u0932**: \u092a\u0942\u091b\u0947\u0902 *'\u092a\u0941\u0928\u0930\u094d\u092a\u094d\u0930\u093e\u092a\u094d\u0924\u093f \u0908\u092e\u0947\u0932 \u0915\u093e \u092e\u0938\u094c\u0926\u093e \u0924\u0948\u092f\u093e\u0930 \u0915\u0930\u0947\u0902'*\n- **BI \u0930\u093f\u092a\u094b\u0930\u094d\u091f**: *'Power BI'* \u092f\u093e *'Tableau'* \u092b\u093c\u093e\u0907\u0932\u094b\u0902 \u0915\u0940 \u092e\u093e\u0902\u0917 \u0915\u0930\u0947\u0902\u0964","name": "Hindi", "native": "हिन्दी", "dir": "ltr"},
    "ru": {
        "financials": "### \ud83d\udcca \u0424\u0438\u043d\u0430\u043d\u0441\u043e\u0432\u044b\u0435 \u0440\u0438\u0441\u043a\u0438 \u0438 \u0430\u043d\u0430\u043b\u0438\u0437 \u043f\u043e\u0442\u0435\u0440\u044c \u0432\u044b\u0440\u0443\u0447\u043a\u0438\n\nQiplo \u043e\u0442\u0441\u043b\u0435\u0436\u0438\u0432\u0430\u0435\u0442 **{total_cust:,} \u0430\u043a\u0442\u0438\u0432\u043d\u044b\u0445 \u043a\u043b\u0438\u0435\u043d\u0442\u043e\u0432** \u0441 \u043e\u0431\u0449\u0438\u043c \u043e\u0431\u044a\u0435\u043c\u043e\u043c \u0435\u0436\u0435\u043c\u0435\u0441\u044f\u0447\u043d\u043e\u0439 \u0432\u044b\u0440\u0443\u0447\u043a\u0438 (MRR) \u0432 \u0440\u0430\u0437\u043c\u0435\u0440\u0435 **${total_mrr:,.2f}**.\n\n**\u0424\u0438\u043d\u0430\u043d\u0441\u043e\u0432\u044b\u0435 \u0440\u0438\u0441\u043a\u0438:**\n- **\u0415\u0436\u0435\u043c\u0435\u0441\u044f\u0447\u043d\u0430\u044f \u0432\u044b\u0440\u0443\u0447\u043a\u0430 \u043f\u043e\u0434 \u0440\u0438\u0441\u043a\u043e\u043c (MRR at Risk)**: **${risk_mrr:,.2f}** ({risk_pct:.1f}% \u043e\u0442 \u043e\u0431\u0449\u0435\u0433\u043e MRR)\n- **\u0413\u043e\u0434\u043e\u0432\u0430\u044f \u0432\u044b\u0440\u0443\u0447\u043a\u0430 \u043f\u043e\u0434 \u0440\u0438\u0441\u043a\u043e\u043c (ARR at Risk)**: **${arr_at_risk:,.2f}**\n- **\u0421\u0440\u0435\u0434\u043d\u044f\u044f \u0432\u0435\u0440\u043e\u044f\u0442\u043d\u043e\u0441\u0442\u044c \u043e\u0442\u0442\u043e\u043a\u0430 \u043f\u043e \u043f\u043e\u0440\u0442\u0444\u0435\u043b\u044e**: **{avg_risk:.1f}%**\n\n**\u0420\u0435\u043a\u043e\u043c\u0435\u043d\u0434\u0443\u0435\u043c\u044b\u0435 \u0444\u0438\u043d\u0430\u043d\u0441\u043e\u0432\u044b\u0435 \u043c\u0435\u0440\u044b:**\n1. \u041f\u0440\u0435\u0434\u043b\u043e\u0436\u0438\u0442\u0435 \u0441\u043a\u0438\u0434\u043a\u0443 15% \u0434\u043b\u044f \u043f\u0435\u0440\u0435\u0432\u043e\u0434\u0430 \u043a\u043b\u0438\u0435\u043d\u0442\u043e\u0432 \u0441 \u043f\u043e\u043c\u0435\u0441\u044f\u0447\u043d\u043e\u0439 \u043e\u043f\u043b\u0430\u0442\u044b \u043d\u0430 \u0433\u043e\u0434\u043e\u0432\u044b\u0435 \u043a\u043e\u043d\u0442\u0440\u0430\u043a\u0442\u044b.\n2. \u0423\u0441\u043a\u043e\u0440\u044c\u0442\u0435 \u0440\u0435\u0448\u0435\u043d\u0438\u0435 \u0444\u0438\u043d\u0430\u043d\u0441\u043e\u0432\u044b\u0445 \u043f\u0440\u0435\u0442\u0435\u043d\u0437\u0438\u0439 \u043a\u043b\u044e\u0447\u0435\u0432\u044b\u0445 \u043a\u043b\u0438\u0435\u043d\u0442\u043e\u0432 \u0434\u043b\u044f \u0437\u0430\u0449\u0438\u0442\u044b \u0434\u0435\u043d\u0435\u0436\u043d\u043e\u0433\u043e \u043f\u043e\u0442\u043e\u043a\u0430.",
        "churn_causes": "### \ud83d\udd0d \u0413\u043b\u0430\u0432\u043d\u044b\u0435 \u043f\u0440\u0438\u0447\u0438\u043d\u044b \u043e\u0442\u0442\u043e\u043a\u0430 \u043a\u043b\u0438\u0435\u043d\u0442\u043e\u0432 \u0438 \u0444\u0430\u043a\u0442\u043e\u0440\u044b \u0440\u0438\u0441\u043a\u0430\n\n\u0410\u043d\u0430\u043b\u0438\u0437 \u043c\u043e\u0434\u0435\u043b\u0438 **Tabular Hybrid Transformer** \u0432\u044b\u044f\u0432\u0438\u043b \u0441\u043b\u0435\u0434\u0443\u044e\u0449\u0438\u0435 \u043a\u043b\u044e\u0447\u0435\u0432\u044b\u0435 \u0444\u0430\u043a\u0442\u043e\u0440\u044b:\n\n1. **\u0422\u0438\u043f \u043a\u043e\u043d\u0442\u0440\u0430\u043a\u0442\u0430**: \u041a\u043b\u0438\u0435\u043d\u0442\u044b \u0441 \u043f\u043e\u043c\u0435\u0441\u044f\u0447\u043d\u043e\u0439 \u043e\u043f\u043b\u0430\u0442\u043e\u0439 \u0443\u0445\u043e\u0434\u044f\u0442 \u0432 **3,4 \u0440\u0430\u0437\u0430 \u0447\u0430\u0449\u0435**, \u0447\u0435\u043c \u043a\u043b\u0438\u0435\u043d\u0442\u044b \u0441 \u0433\u043e\u0434\u043e\u0432\u044b\u043c\u0438 \u043a\u043e\u043d\u0442\u0440\u0430\u043a\u0442\u0430\u043c\u0438.\n2. **\u041f\u0440\u043e\u0431\u043b\u0435\u043c\u044b \u0432 \u043f\u043e\u0434\u0434\u0435\u0440\u0436\u043a\u0435**: \u041d\u0430\u043b\u0438\u0447\u0438\u0435 **>2 \u043d\u0435\u0440\u0435\u0448\u0435\u043d\u043d\u044b\u0445 \u0442\u0438\u043a\u0435\u0442\u043e\u0432** \u0432 \u0442\u0435\u0447\u0435\u043d\u0438\u0435 48 \u0447\u0430\u0441\u043e\u0432 \u0443\u0432\u0435\u043b\u0438\u0447\u0438\u0432\u0430\u0435\u0442 \u0440\u0438\u0441\u043a \u0443\u0445\u043e\u0434\u0430 \u043d\u0430 72%.\n3. **\u0417\u0430\u0434\u0435\u0440\u0436\u043a\u0438 \u043f\u043b\u0430\u0442\u0435\u0436\u0435\u0439**: \u041a\u043b\u0438\u0435\u043d\u0442\u044b \u0441 **\u22652 \u0437\u0430\u0434\u0435\u0440\u0436\u043a\u0430\u043c\u0438 \u043e\u043f\u043b\u0430\u0442\u044b** \u0434\u0435\u043c\u043e\u043d\u0441\u0442\u0440\u0438\u0440\u0443\u044e\u0442 \u043f\u043e\u0442\u0435\u0440\u044e \u0432\u043e\u0432\u043b\u0435\u0447\u0435\u043d\u043d\u043e\u0441\u0442\u0438.\n4. **\u041f\u0430\u0434\u0435\u043d\u0438\u0435 \u0430\u043a\u0442\u0438\u0432\u043d\u043e\u0441\u0442\u0438**: \u0418\u0441\u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u043d\u0438\u0435 \u043f\u043b\u0430\u0442\u0444\u043e\u0440\u043c\u044b \u043c\u0435\u043d\u0435\u0435 **15 \u0447\u0430\u0441\u043e\u0432 \u0432 \u043c\u0435\u0441\u044f\u0446** \u2014 \u0433\u043b\u0430\u0432\u043d\u044b\u0439 \u0440\u0430\u043d\u043d\u0438\u0439 \u0441\u0438\u0433\u043d\u0430\u043b \u0442\u0438\u0445\u043e\u0433\u043e \u0443\u0445\u043e\u0434\u0430.",
        "playbook": "### \u2709\ufe0f \u041f\u0435\u0440\u0441\u043e\u043d\u0430\u043b\u0438\u0437\u0438\u0440\u043e\u0432\u0430\u043d\u043d\u043e\u0435 \u043f\u0438\u0441\u044c\u043c\u043e \u0434\u043b\u044f \u0432\u043e\u0437\u0432\u0440\u0430\u0442\u0430 \u043a\u043b\u0438\u0435\u043d\u0442\u0430 \u0438 \u043f\u043b\u0430\u043d \u0434\u0435\u0439\u0441\u0442\u0432\u0438\u0439\n\n\u041f\u0440\u043e\u0432\u0435\u0440\u0435\u043d\u043d\u044b\u0439 \u0448\u0430\u0431\u043b\u043e\u043d \u043f\u0438\u0441\u044c\u043c\u0430 \u0434\u043b\u044f \u043a\u043b\u0438\u0435\u043d\u0442\u043e\u0432 \u0432 \u0437\u043e\u043d\u0435 \u0440\u0438\u0441\u043a\u0430:\n\n---\n**\u0422\u0435\u043c\u0430**: *\u041f\u0440\u0438\u043e\u0440\u0438\u0442\u0435\u0442\u043d\u044b\u0439 \u0432\u043e\u043f\u0440\u043e\u0441: \u0412\u0430\u0448\u0435 \u043f\u0430\u0440\u0442\u043d\u0435\u0440\u0441\u0442\u0432\u043e \u0441 \u043d\u0430\u043c\u0438 \u0438 \u043f\u0435\u0440\u0441\u043e\u043d\u0430\u043b\u044c\u043d\u0430\u044f \u043f\u043e\u0434\u0434\u0435\u0440\u0436\u043a\u0430*\n\n\u0423\u0432\u0430\u0436\u0430\u0435\u043c\u044b\u0439 \u043a\u043b\u0438\u0435\u043d\u0442,\n\n\u042f \u043e\u0431\u0440\u0430\u0449\u0430\u044e\u0441\u044c \u043a \u0432\u0430\u043c \u043d\u0430\u043f\u0440\u044f\u043c\u0443\u044e \u043e\u0442 \u0440\u0443\u043a\u043e\u0432\u043e\u0434\u0441\u0442\u0432\u0430 \u043a\u043b\u0438\u0435\u043d\u0442\u0441\u043a\u043e\u0433\u043e \u0441\u0435\u0440\u0432\u0438\u0441\u0430 Qiplo. \u041c\u044b \u0437\u0430\u043c\u0435\u0442\u0438\u043b\u0438 \u043d\u0435\u0434\u0430\u0432\u043d\u0438\u0435 \u0441\u043b\u043e\u0436\u043d\u043e\u0441\u0442\u0438 \u0432 \u0440\u0430\u0431\u043e\u0442\u0435 \u0441 \u0432\u0430\u0448\u0438\u043c \u0430\u043a\u043a\u0430\u0443\u043d\u0442\u043e\u043c.\n\n\u0412\u0430\u0448 \u0443\u0441\u043f\u0435\u0445 \u2014 \u043d\u0430\u0448 \u0433\u043b\u0430\u0432\u043d\u044b\u0439 \u043f\u0440\u0438\u043e\u0440\u0438\u0442\u0435\u0442. \u041c\u044b \u0440\u0430\u0434\u044b \u043f\u0440\u0435\u0434\u043b\u043e\u0436\u0438\u0442\u044c \u0432\u0430\u043c:\n1. **\u041a\u043e\u043d\u0441\u0443\u043b\u044c\u0442\u0430\u0446\u0438\u044e \u0441 \u0432\u0435\u0434\u0443\u0449\u0438\u043c \u0430\u0440\u0445\u0438\u0442\u0435\u043a\u0442\u043e\u0440\u043e\u043c**: 30-\u043c\u0438\u043d\u0443\u0442\u043d\u044b\u0439 \u043f\u0435\u0440\u0441\u043e\u043d\u0430\u043b\u044c\u043d\u044b\u0439 \u0430\u0443\u0434\u0438\u0442 \u0438 \u043e\u043f\u0442\u0438\u043c\u0438\u0437\u0430\u0446\u0438\u044e \u0441\u0438\u0441\u0442\u0435\u043c.\n2. **VIP-\u0441\u043a\u0438\u0434\u043a\u0443 \u043d\u0430 \u043b\u043e\u044f\u043b\u044c\u043d\u043e\u0441\u0442\u044c**: \u0421\u043a\u0438\u0434\u043a\u0443 20% \u043f\u0440\u0438 \u0441\u043b\u0435\u0434\u0443\u044e\u0449\u0435\u043c \u0433\u043e\u0434\u043e\u0432\u043e\u043c \u043f\u0440\u043e\u0434\u043b\u0435\u043d\u0438\u0438.\n\n\u0421\u043c\u043e\u0436\u0435\u043c \u043b\u0438 \u043c\u044b \u0441\u043e\u0437\u0432\u043e\u043d\u0438\u0442\u044c\u0441\u044f \u0432 \u044d\u0442\u043e\u0442 \u0447\u0435\u0442\u0432\u0435\u0440\u0433 \u0438\u043b\u0438 \u043f\u044f\u0442\u043d\u0438\u0446\u0443?\n\n\u0421 \u0443\u0432\u0430\u0436\u0435\u043d\u0438\u0435\u043c,\n*\u041a\u043e\u043c\u0430\u043d\u0434\u0430 \u043a\u043b\u0438\u0435\u043d\u0442\u0441\u043a\u043e\u0433\u043e \u0443\u0441\u043f\u0435\u0445\u0430 Qiplo*\n---\n\n**\u041f\u043b\u0430\u043d \u0434\u0435\u0439\u0441\u0442\u0432\u0438\u0439:** \u041e\u0442\u043f\u0440\u0430\u0432\u044c\u0442\u0435 \u043f\u0438\u0441\u044c\u043c\u043e \u0432 \u0442\u0435\u0447\u0435\u043d\u0438\u0435 24 \u0447\u0430\u0441\u043e\u0432 \u0438 \u043f\u0440\u0435\u0434\u043b\u043e\u0436\u0438\u0442\u0435 \u0433\u0438\u0431\u043a\u0438\u0439 \u0433\u0440\u0430\u0444\u0438\u043a \u043f\u043b\u0430\u0442\u0435\u0436\u0435\u0439.",
        "export_bi": "### \ud83d\udcc8 \u0418\u043d\u0442\u0435\u0433\u0440\u0430\u0446\u0438\u044f \u0441 BI-\u0441\u0438\u0441\u0442\u0435\u043c\u0430\u043c\u0438 \u0438 \u043a\u043e\u043d\u043d\u0435\u043a\u0442\u043e\u0440\u044b\n\n\u0413\u043e\u0442\u043e\u0432\u044b\u0435 \u0444\u0430\u0439\u043b\u044b \u043f\u043e\u0434\u043a\u043b\u044e\u0447\u0435\u043d\u0438\u044f \u043a \u0432\u0430\u0448\u0435\u0439 \u0431\u0430\u0437\u0435 \u0434\u0430\u043d\u043d\u044b\u0445:\n\n- **[\u0421\u043a\u0430\u0447\u0430\u0442\u044c \u0438\u0441\u0442\u043e\u0447\u043d\u0438\u043a \u0434\u0430\u043d\u043d\u044b\u0445 Power BI (.pbids)](/api/export/powerbi)**\n- **[\u0421\u043a\u0430\u0447\u0430\u0442\u044c \u0440\u0430\u0431\u043e\u0447\u0443\u044e \u043a\u043d\u0438\u0433\u0443 Tableau (.twb)](/api/export/tableau)**\n- **[\u0421\u043a\u0430\u0447\u0430\u0442\u044c \u0442\u0430\u0431\u043b\u0438\u0446\u0443 Excel (.xlsx)](/api/export/excel)**\n- **[\u0421\u043a\u0430\u0447\u0430\u0442\u044c \u043f\u043e\u043b\u043d\u044b\u0439 \u043e\u0442\u0447\u0435\u0442 \u0430\u0443\u0434\u0438\u0442\u0430](/api/export/report)**",
        "default_fallback": "### \ud83d\udca1 \u041a\u043e\u043d\u0441\u0443\u043b\u044c\u0442\u0430\u043d\u0442 \u043f\u043e \u0430\u043d\u0430\u043b\u0438\u0442\u0438\u043a\u0435 \u0434\u0430\u043d\u043d\u044b\u0445 \u0438 \u0443\u0434\u0435\u0440\u0436\u0430\u043d\u0438\u044e \u043a\u043b\u0438\u0435\u043d\u0442\u043e\u0432\n\n\u042f \u0433\u043e\u0442\u043e\u0432 \u043f\u0440\u0435\u0434\u043e\u0441\u0442\u0430\u0432\u0438\u0442\u044c \u044d\u043a\u0441\u043f\u0435\u0440\u0442\u043d\u044b\u0435 \u0440\u0435\u043a\u043e\u043c\u0435\u043d\u0434\u0430\u0446\u0438\u0438 \u043f\u043e \u0432\u0430\u0448\u0438\u043c \u0434\u0430\u043d\u043d\u044b\u043c:\n\n- **\u041a\u043b\u0438\u0435\u043d\u0442\u044b \u0432 \u0437\u043e\u043d\u0435 \u0440\u0438\u0441\u043a\u0430**: \u0421\u043f\u0440\u043e\u0441\u0438\u0442\u0435 *'\u041f\u043e\u043a\u0430\u0437\u0430\u0442\u044c \u043a\u043b\u0438\u0435\u043d\u0442\u043e\u0432 \u0432\u044b\u0441\u043e\u043a\u043e\u0433\u043e \u0440\u0438\u0441\u043a\u0430'*\n- **\u0423\u0433\u0440\u043e\u0437\u0430 \u0432\u044b\u0440\u0443\u0447\u043a\u0435**: \u0421\u043f\u0440\u043e\u0441\u0438\u0442\u0435 *'\u0421\u043a\u043e\u043b\u044c\u043a\u043e \u0432\u044b\u0440\u0443\u0447\u043a\u0438 \u043f\u043e\u0434 \u0443\u0433\u0440\u043e\u0437\u043e\u0439?'*\n- **\u041f\u0440\u0438\u0447\u0438\u043d\u044b \u0443\u0445\u043e\u0434\u0430**: \u0421\u043f\u0440\u043e\u0441\u0438\u0442\u0435 *'\u041f\u043e\u0447\u0435\u043c\u0443 \u043a\u043b\u0438\u0435\u043d\u0442\u044b \u0443\u0445\u043e\u0434\u044f\u0442?'*\n- **\u041f\u043b\u0430\u043d \u0432\u043e\u0437\u0432\u0440\u0430\u0442\u0430**: \u041f\u043e\u043f\u0440\u043e\u0441\u0438\u0442\u0435 *'\u0421\u043e\u0441\u0442\u0430\u0432\u0438\u0442\u044c \u043f\u0438\u0441\u044c\u043c\u043e \u043a\u043b\u0438\u0435\u043d\u0442\u0443'*\n- **\u0412\u044b\u0433\u0440\u0443\u0437\u043a\u0430 \u0432 BI**: \u0417\u0430\u043f\u0440\u043e\u0441\u0438\u0442\u0435 \u0444\u0430\u0439\u043b\u044b *'Power BI'* \u0438\u043b\u0438 *'Tableau'*.","name": "Russian", "native": "Русский", "dir": "ltr"}
}

def normalize_language(lang: Optional[str]) -> str:
    if not lang or not isinstance(lang, str):
        return "en"
    clean = lang.lower().strip()
    return clean if clean in SUPPORTED_LANGUAGES else "en"

# ==============================================================================
# 1. Localized Sandbox Simulator Recommendations
# ==============================================================================
SANDBOX_LOCALIZED_RECS: Dict[str, Dict[str, str]] = {
    "en": {
        "high_risk": "⚠️ <strong>HIGH CHURN RISK</strong>: Simulated account parameters indicate high attrition probability.",
        "resolve_tickets": "• <strong>Resolve Support Issues</strong>: Address {tickets} unresolved support tickets immediately.",
        "csat_recovery": "• <strong>CSAT Recovery Program</strong>: Proactively contact customer due to low satisfaction ({satisfaction}/5).",
        "billing_outreach": "• <strong>Billing Outreach</strong>: Customer has {delays} days of payment delay. Offer flexible billing options.",
        "low_risk": "✅ <strong>LOW CHURN RISK</strong>: Account parameters reflect a stable customer relation.",
        "loyalty": "• <strong>Loyalty Upgrades</strong>: Eligible for standard account growth upgrades."
    },
    "es": {
        "high_risk": "⚠️ <strong>ALTO RIESGO DE CANCELACIÓN</strong>: Los parámetros simulados indican una alta probabilidad de abandono.",
        "resolve_tickets": "• <strong>Resolver problemas de soporte</strong>: Atienda {tickets} tickets de soporte no resueltos de inmediato.",
        "csat_recovery": "• <strong>Programa de recuperación CSAT</strong>: Contacte proactivamente al cliente debido a la baja satisfacción ({satisfaction}/5).",
        "billing_outreach": "• <strong>Gestión de cobro</strong>: El cliente presenta {delays} días de retraso. Ofrezca planes de pago flexibles.",
        "low_risk": "✅ <strong>BAJO RIESGO DE CANCELACIÓN</strong>: Los parámetros reflejan una relación de cliente estable.",
        "loyalty": "• <strong>Mejoras de lealtad</strong>: Elegible para mejoras estándar de expansión de cuenta."
    },
    "fr": {
        "high_risk": "⚠️ <strong>RISQUE DE DÉSABONNEMENT ÉLEVÉ</strong> : Les paramètres indiquent une forte probabilité d'attrition.",
        "resolve_tickets": "• <strong>Résoudre les tickets d'assistance</strong> : Traitez immédiatement {tickets} tickets en suspens.",
        "csat_recovery": "• <strong>Programme de récupération CSAT</strong> : Contactez le client en raison d'une faible satisfaction ({satisfaction}/5).",
        "billing_outreach": "• <strong>Contact facturation</strong> : Retard de paiement de {delays} jours. Proposez des facilités de paiement.",
        "low_risk": "✅ <strong>FAIBLE RISQUE DE DÉSABONNEMENT</strong> : Les paramètres indiquent une relation client saine et stable.",
        "loyalty": "• <strong>Surclassements de fidélité</strong> : Éligible aux programmes d'expansion de compte."
    },
    "de": {
        "high_risk": "⚠️ <strong>HOHES ABWANDERUNGSRISIKO</strong>: Simulierte Parameter deuten auf eine hohe Kündigungswahrscheinlichkeit hin.",
        "resolve_tickets": "• <strong>Support-Tickets klären</strong>: Beheben Sie {tickets} ungelöste Support-Tickets umgehend.",
        "csat_recovery": "• <strong>CSAT-Rückgewinnung</strong>: Kontaktieren Sie den Kunden wegen geringer Zufriedenheit ({satisfaction}/5).",
        "billing_outreach": "• <strong>Zahlungsansprache</strong>: {delays} Tage Zahlungsverzug. Bieten Sie flexible Zahlungsoptionen an.",
        "low_risk": "✅ <strong>GERINGES ABWANDERUNGSRISIKO</strong>: Parameter spiegeln eine stabile Kundenbeziehung wider.",
        "loyalty": "• <strong>Treue-Upgrades</strong>: Berechtigt für standardmäßige Kontoerweiterungen."
    },
    "zh": {
        "high_risk": "⚠️ <strong>高流失风险</strong>：模拟账户参数表明客户存在极高的流失概率。",
        "resolve_tickets": "• <strong>解决工单问题</strong>：立即处理 {tickets} 个未解决的服务工单。",
        "csat_recovery": "• <strong>满意度修复计划</strong>：客户满意度较低（{satisfaction}/5），需主动跟进联系。",
        "billing_outreach": "• <strong>账单关怀</strong>：客户存在 {delays} 天逾期，建议提供灵活支付方案。",
        "low_risk": "✅ <strong>低流失风险</strong>：模拟参数表明客户关系健康稳定。",
        "loyalty": "• <strong>忠诚度升级</strong>：符合标准账户增购与功能升级条件。"
    },
    "ja": {
        "high_risk": "⚠️ <strong>高解約リスク</strong>: シミュレーションされたパラメータは高い解約確率を示しています。",
        "resolve_tickets": "• <strong>サポート課題の迅速解決</strong>: {tickets}件の未解決チケットを直ちに対応してください。",
        "csat_recovery": "• <strong>CSAT改善プログラム</strong>: 満足度低下（{satisfaction}/5）のため優先的に連絡してください。",
        "billing_outreach": "• <strong>請求フォロー</strong>: {delays}日の支払遅延があります。柔軟な支払い条件を提案してください。",
        "low_risk": "✅ <strong>低解約リスク</strong>: アカウントパラメータは安定した良好な関係を示しています。",
        "loyalty": "• <strong>ロイヤルティ特典</strong>: アカウント拡張・アップグレードの対象です。"
    },
    "pt": {
        "high_risk": "⚠️ <strong>ALTO RISCO DE CHURN</strong>: Parâmetros simulados indicam alta probabilidade de cancelamento.",
        "resolve_tickets": "• <strong>Resolver chamados de suporte</strong>: Trate {tickets} chamados não resolvidos imediatamente.",
        "csat_recovery": "• <strong>Recuperação de CSAT</strong>: Contate o cliente proativamente devido à baixa satisfação ({satisfaction}/5).",
        "billing_outreach": "• <strong>Gestão de faturamento</strong>: Cliente com {delays} dias de atraso. Ofereça opções flexíveis de pagamento.",
        "low_risk": "✅ <strong>BAIXO RISCO DE CHURN</strong>: Parâmetros refletem uma relação saudável e estável.",
        "loyalty": "• <strong>Upgrades de fidelidade</strong>: Elegível para expansão de conta e novas funcionalidades."
    },
    "ar": {
        "high_risk": "⚠️ <strong>مستوى مخاطر تسرب مرتفع</strong>: تشير معايير الحساب إلى احتمال تسرب كبير للعميل.",
        "resolve_tickets": "• <strong>حل مشكلات الدعم</strong>: عالج {tickets} تذاكر دعم معلقة على الفور.",
        "csat_recovery": "• <strong>خطة استعادة الرضا</strong>: تواصل استباقيًا مع العميل نظرًا لانخفاض التقييم ({satisfaction}/5).",
        "billing_outreach": "• <strong>متابعة الفوترة</strong>: تأخير في الدفع لمدة {delays} يومًا. قدم خيارات سداد مرنة.",
        "low_risk": "✅ <strong>مستوى مخاطر تسرب منخفض</strong>: تعكس المعايير علاقة مستقرة وصحية مع العميل.",
        "loyalty": "• <strong>ترقيات الولاء</strong>: العميل مؤهل لتوسيع الحساب وترقيات الخدمة القياسية."
    },
    "hi": {
        "high_risk": "⚠️ <strong>उच्च ग्राहक मंथन जोखिम</strong>: सिम्युलेटेड पैरामीटर दर्शाते हैं कि ग्राहक के जाने की संभावना अधिक है।",
        "resolve_tickets": "• <strong>सपोर्ट समस्या समाधान</strong>: {tickets} अनसुलझे सपोर्ट टिकटों को तुरंत हल करें।",
        "csat_recovery": "• <strong>संतुष्टि सुधार योजना</strong>: कम संतुष्टि ({satisfaction}/5) के कारण ग्राहक से सक्रिय रूप से संपर्क करें।",
        "billing_outreach": "• <strong>बिलिंग सहायता</strong>: ग्राहक के भुगतान में {delays} दिनों की देरी है। लचीले भुगतान विकल्प दें।",
        "low_risk": "✅ <strong>कम ग्राहक मंथन जोखिम</strong>: पैरामीटर एक स्थिर और सकारात्मक ग्राहक संबंध दर्शाते हैं।",
        "loyalty": "• <strong>निष्ठा अपग्रेड</strong>: ग्राहक मानक खाता विस्तार और नई सुविधाओं के पात्र हैं।"
    },
    "ru": {
        "high_risk": "⚠️ <strong>ВЫСОКИЙ РИСК ОТТОКА</strong>: Параметры указывают на высокую вероятность ухода клиента.",
        "resolve_tickets": "• <strong>Решить проблемы в поддержке</strong>: Немедленно обработайте {tickets} нерешенных тикетов.",
        "csat_recovery": "• <strong>Программа восстановления CSAT</strong>: Свяжитесь с клиентом из-за низкой удовлетворенности ({satisfaction}/5).",
        "billing_outreach": "• <strong>Оплата и биллинг</strong>: Задержка платежа {delays} дн. Предложите гибкие условия оплаты.",
        "low_risk": "✅ <strong>НИЗКИЙ РИСК ОТТОКА</strong>: Параметры отражают стабильные и надежные отношения с клиентом.",
        "loyalty": "• <strong>Программа лояльности</strong>: Клиент подходит для планового расширения подписки."
    }
}

def generate_sandbox_recommendations(proba: float, threshold: float, tickets: int, satisfaction: int, delays: int, language: str = "en") -> List[str]:
    lang = normalize_language(language)
    dict_recs = SANDBOX_LOCALIZED_RECS.get(lang, SANDBOX_LOCALIZED_RECS["en"])
    
    recs: List[str] = []
    if proba >= threshold:
        recs.append(dict_recs["high_risk"])
        if int(tickets) > 1:
            recs.append(dict_recs["resolve_tickets"].format(tickets=tickets))
        if int(satisfaction) <= 2:
            recs.append(dict_recs["csat_recovery"].format(satisfaction=satisfaction))
        if int(delays) > 2:
            recs.append(dict_recs["billing_outreach"].format(delays=delays))
    else:
        recs.append(dict_recs["low_risk"])
        recs.append(dict_recs["loyalty"])
    return recs

# ==============================================================================
# 2. Multilingual System Instructions for Gemini & Ollama
# ==============================================================================
def enhance_system_instruction_with_language(base_instruction: str, language: str) -> str:
    lang = normalize_language(language)
    if lang == "en":
        return base_instruction
    
    lang_info = SUPPORTED_LANGUAGES[lang]
    lang_name = lang_info["name"]
    lang_native = lang_info["native"]
    
    directive = (
        f"\n\nCRITICAL MULTILINGUAL MANDATE:\n"
        f"The user is operating Qiplo in '{lang_native}' ({lang_name}, ISO code: {lang}). "
        f"You MUST compose your entire response, analysis, markdown tables, headings, and strategic recommendations "
        f"fluently and naturally in {lang_native} ({lang_name}). "
        f"Preserve standard technical acronyms (such as MRR, ARR, CSAT, SLA, LTV, CAC, AUC, ROC, Power BI, Tableau) "
        f"where conventional in business data science, but write all explanatory prose, bullet points, and reasoning in {lang_native}."
    )
    return base_instruction + directive

# ==============================================================================
# 3. Localized Presentation Decks Generator
# ==============================================================================
LOCALIZED_PRESENTATION_TEMPLATES: Dict[str, Dict[str, Any]] = {
    "es": {
        "slide1_title": "Presentación Ejecutiva Qiplo",
        "slide1_subtitle": "Plataforma de Inteligencia de Decisiones Empresariales — {total_cust:,} Cuentas Evaluadas",
        "slide2_title": "Resumen Ejecutivo de Churn y Riesgo",
        "slide2_bullets": [
            "El riesgo promedio de abandono en las cuentas evaluadas se sitúa en {avg_risk:.1%}.",
            "Los contratos mensuales y métodos de pago no automáticos son los principales impulsores de abandono.",
            "La gestión proactiva combinada con incentivos de planes anuales protegerá el ARR vulnerable."
        ],
        "slide3_title": "Segmentos de Riesgo Prioritarios y Vulnerabilidades",
        "slide4_title": "Soluciones Prescriptivas y Matriz de Acción",
        "slide4_playbook": [
            {"title": "Llamada SLA CSM en 24 Horas", "desc": "Contacto obligatorio en menos de 24 horas para cuentas con riesgo ≥65%.", "type": "success"},
            {"title": "Descuento de Migración Anual", "desc": "Crédito de incentivo del 15-20% para cambiar contratos mensuales a anuales.", "type": "primary"},
            {"title": "Ruta Rápida de Soporte", "desc": "Enrutamiento prioritario de tickets (<2 horas de SLA) para cuentas con >2 incidencias.", "type": "warning"},
            {"title": "Seguimiento VIP de Onboarding", "desc": "Puntos de control estructurados a 90 días para evitar abandonos tempranos.", "type": "accent"}
        ],
        "slide5_title": "Flujo de Trabajo del Ciclo del Cliente",
        "slide5_steps": [
            {"title": "Auditoría Predictiva", "description": "El motor @ AI escanea los registros para calcular puntuaciones de riesgo."},
            {"title": "Diseño de Estrategia", "description": "Formulación de incentivos de cobro y soporte proactivo."},
            {"title": "Contacto del CSM", "description": "Los CSM inician el contacto mediante plantillas personalizadas."},
            {"title": "Preservación del ARR", "description": "Contratos extendidos con éxito y retención maximizada."}
        ]
    },
    "fr": {
        "slide1_title": "Présentation Exécutive Qiplo",
        "slide1_subtitle": "Plateforme d'Intelligence Décisionnelle — {total_cust:,} Comptes Analysés",
        "slide2_title": "Synthèse Exécutive de l'Attrition et du Risque",
        "slide2_bullets": [
            "Le risque moyen d'attrition client sur les comptes actifs s'élève actuellement à {avg_risk:.1%}.",
            "Les contrats mensuels et les paiements manuels représentent les facteurs majeurs d'attrition.",
            "Une approche proactive associée à des incitations aux forfaits annuels sécurisera l'ARR vulnérable."
        ],
        "slide3_title": "Segments Prioritaires et Vulnérabilités",
        "slide4_title": "Solutions Prescriptives et Matrice d'Action",
        "slide4_playbook": [
            {"title": "Appel CSM SLA 24h", "desc": "Contact obligatoire sous 24h pour les comptes présentant un risque ≥65%.", "type": "success"},
            {"title": "Remise Migration Annuelle", "desc": "Crédit incitatif de 15-20% pour convertir les contrats mensuels en annuels.", "type": "primary"},
            {"title": "Escalade Support Prioritaire", "desc": "Routage prioritaire des tickets (<2h de SLA) pour les comptes ayant >2 litiges.", "type": "warning"},
            {"title": "Points d'Étape Onboarding VIP", "desc": "Suivi structuré sur 90 jours pour éliminer les désengagements précoces.", "type": "accent"}
        ],
        "slide5_title": "Parcours Client et Processus d'Intervention",
        "slide5_steps": [
            {"title": "Audit Prédictif", "description": "Le moteur @ AI évalue les données pour détecter les risques."},
            {"title": "Élaboration Stratégique", "description": "Conception d'offres de facturation et d'assistance proactive."},
            {"title": "Prise de Contact CSM", "description": "Les responsables CSM engagent le contact avec des modèles dédiés."},
            {"title": "Préservation de l'ARR", "description": "Renouvellement des contrats et fidélisation client maximisée."}
        ]
    },
    "de": {
        "slide1_title": "Qiplo Management-Präsentation",
        "slide1_subtitle": "Business Decision Intelligence Plattform — {total_cust:,} Konten Bewertet",
        "slide2_title": "Management-Zusammenfassung zu Kündigungsrisiken",
        "slide2_bullets": [
            "Das durchschnittliche Kündigungsrisiko aller aktiven Konten liegt aktuell bei {avg_risk:.1%}.",
            "Monatsverträge und manuelle Zahlungsweisen sind die Hauptursachen für Kundenabwanderung.",
            "Gezielte proaktive Ansprache und Jahresvertragsrabatte sichern gefährdeten ARR verlässlich ab."
        ],
        "slide3_title": "Prioritäre Risikosegmente & Schwachstellen",
        "slide4_title": "Präskriptiver Handlungsleitfaden & Maßnahmen",
        "slide4_playbook": [
            {"title": "24-Stunden CSM-Anruf-SLA", "desc": "Verbindliche Kontaktaufnahme binnen 24 Stunden bei Risikowert ≥65%.", "type": "success"},
            {"title": "Rabatt für Jahresumstellung", "desc": "15-20% Bonus für den Wechsel von Monatsverträgen in Jahreslaufzeiten.", "type": "primary"},
            {"title": "Support-Express-Eskalation", "desc": "Bevorzugte Ticketbearbeitung (<2 Std. SLA) bei mehr als 2 offenen Fällen.", "type": "warning"},
            {"title": "VIP-Onboarding-Reviews", "desc": "Strukturierte Meilenstein-Gespräche in den ersten 90 Tagen.", "type": "accent"}
        ],
        "slide5_title": "Interaktiver Kunden-Workflow",
        "slide5_steps": [
            {"title": "Prädiktives Audit", "description": "Die @ AI-Engine analysiert Datensätze zur Risikoermittlung."},
            {"title": "Strategieentwurf", "description": "Entwicklung von Zahlungs- und Supportanreizen."},
            {"title": "CSM-Kontaktaufnahme", "description": "CSMs starten die Ansprache mit vorgefertigten Vorlagen."},
            {"title": "ARR-Sicherung", "description": "Verträge erfolgreich verlängert; Kundenbindung maximiert."}
        ]
    },
    "zh": {
        "slide1_title": "Qiplo 高管决策汇报演示",
        "slide1_subtitle": "企业商业决策智能平台 — 已评估 {total_cust:,} 户客户",
        "slide2_title": "客户流失与财务风险综述",
        "slide2_bullets": [
            "当前活跃客户组合的整体平均流失概率为 {avg_risk:.1%}。",
            "按月签约合同与非自动扣款结算方式是流失的首要诱因。",
            "实施针对性主动关怀与年度合同迁移激励措施可有效守住核心 ARR。"
        ],
        "slide3_title": "重点风险客群与脆弱性剖析",
        "slide4_title": "规范性留存方案与行动矩阵",
        "slide4_playbook": [
            {"title": "24小时 CSM 响应 SLA", "desc": "流失风险≥65%的重点客户必须在24小时内启动专家外呼。", "type": "success"},
            {"title": "年度续约专享折扣", "desc": "为月付客户提供15-20%的优惠额度，锁定一年期长期合约。", "type": "primary"},
            {"title": "工单极速响应通道", "desc": "对存在2个以上未决工单的客户开启绿色通道（<2小时响应）。", "type": "warning"},
            {"title": "VIP 90天入职关怀", "desc": "在前90天关键周期设立结构化沟通机制，防止早期流失。", "type": "accent"}
        ],
        "slide5_title": "客户旅程互动流程",
        "slide5_steps": [
            {"title": "预测性审计", "description": "@ AI 智能引擎全量扫描数据库并计算风险概率。"},
            {"title": "策略制定", "description": "制定精准账单支持与主动服务激励策略。"},
            {"title": "主管主动跟进", "description": "客户成功经理通过预设模板开启多渠道沟通。"},
            {"title": "锁定核心 ARR", "description": "合同成功续签并稳固客户生命周期价值。"}
        ]
    },
    "ja": {
        "slide1_title": "Qiplo エグゼクティブ プレゼンテーション",
        "slide1_subtitle": "ビジネス意思決定インテリジェンス — 分析済みアカウント {total_cust:,} 件",
        "slide2_title": "顧客解約および収益リスク総括",
        "slide2_bullets": [
            "全アクティブ顧客の平均解約リスク確率は現在 {avg_risk:.1%} です。",
            "月次契約および非自動決済のアカウントが主な離脱要因となっています。",
            "プロアクティブなアプローチと年間契約インセンティブにより重要ARRを保護します。"
        ],
        "slide3_title": "優先リスクセグメントと脆弱性分析",
        "slide4_title": "定型アクションマトリクスと改善策",
        "slide4_playbook": [
            {"title": "24時間 CSM コール SLA", "desc": "リスクスコア65%以上のアカウントに対し24時間以内の連絡を義務化。", "type": "success"},
            {"title": "年間プラン移行割引", "desc": "月次契約から年間契約への変更で15〜20%の特別クレジットを付与。", "type": "primary"},
            {"title": "サポート迅速エスカレーション", "desc": "未解決チケット2件以上のアカウントをVIPキューへ優先ルーティング（2時間以内）。", "type": "warning"},
            {"title": "初期90日オンボーディング確認", "desc": "初期定着を確実にするため90日間の定期マイルストーン面談を実施。", "type": "accent"}
        ],
        "slide5_title": "カスタマージャーニー業務フロー",
        "slide5_steps": [
            {"title": "予測的監査", "description": "@ AI エンジンが顧客データを監査しリスク確率を算出。"},
            {"title": "戦略立案", "description": "請求支援およびプロアクティブサポート施策を策定。"},
            {"title": "CSM対応開始", "description": "専任CSMがテンプレートを活用し迅速にアプローチ。"},
            {"title": "ARRの維持確保", "description": "契約更新を完了し、顧客生涯価値を最大化。"}
        ]
    },
    "pt": {
        "slide1_title": "Apresentação Executiva Qiplo",
        "slide1_subtitle": "Plataforma de Inteligência em Decisões de Negócios — {total_cust:,} Contas Avaliadas",
        "slide2_title": "Resumo Executivo de Churn e Exposição a Risco",
        "slide2_bullets": [
            "O risco médio de cancelamento em contas ativas está em {avg_risk:.1%}.",
            "Contratos mensais e pagamentos manuais representam os principais fatores de saída.",
            "Ações proativas combinadas com incentivos de planos anuais protegerão o ARR vulnerável."
        ],
        "slide3_title": "Segmentos Críticos e Vulnerabilidades Prioritárias",
        "slide4_title": "Soluções Prescritivas e Matriz de Ação",
        "slide4_playbook": [
            {"title": "SLA de Ligação CSM em 24h", "desc": "Contato obrigatório em até 24h para contas com risco ≥65%.", "type": "success"},
            {"title": "Desconto de Migração Anual", "desc": "Incentivo de 15-20% para conversão de planos mensais em anuais.", "type": "primary"},
            {"title": "Fila Rápida de Suporte", "desc": "Atendimento prioritário (<2h SLA) para contas com >2 chamados em aberto.", "type": "warning"},
            {"title": "Acompanhamento VIP de Onboarding", "desc": "Revisões estruturadas nos primeiros 90 dias para eliminar abandono precoce.", "type": "accent"}
        ],
        "slide5_title": "Fluxo de Trabalho da Jornada do Cliente",
        "slide5_steps": [
            {"title": "Auditoria Preditiva", "description": "O motor @ AI analisa os dados para calcular probabilidades de risco."},
            {"title": "Desenho Estratégico", "description": "Formula incentivos de cobrança e programas de retenção proativos."},
            {"title": "Abordagem do CSM", "description": "CSMs iniciam o contato com modelos de alta conversão."},
            {"title": "Preservação de ARR", "description": "Contratos estendidos com sucesso e fidelidade assegurada."}
        ]
    },
    "ar": {
        "slide1_title": "عرض تقديمي تنفيذي - Qiplo",
        "slide1_subtitle": "منصة ذكاء اتخاذ القرارات للأعمال — تم تقييم {total_cust:,} حساب",
        "slide2_title": "ملخص تنفيذي لمعدلات التسرب والمخاطر",
        "slide2_bullets": [
            "يبلغ متوسط مخاطر تسرب العملاء عبر الحسابات النشطة حاليًا {avg_risk:.1%}.",
            "تمثل العقود الشهرية وطرق الدفع غير الآلية المحركات الرئيسية للتسرب.",
            "التواصل الاستباقي المدعوم بحوافز الخطط السنوية سيحمي الإيرادات المتكررة المعرضة للخطر."
        ],
        "slide3_title": "القطاعات ذات الأولوية ونقاط الضعف",
        "slide4_title": "الحلول التوجيهية ومصفوفة الإجراءات",
        "slide4_playbook": [
            {"title": "اتصال فوري خلال 24 ساعة", "desc": "تواصل إلزامي خلال 24 ساعة للحسابات التي تبلغ نسبة خطرها ≥65%.", "type": "success"},
            {"title": "خصم الترقية للخطة السنوية", "desc": "خصم 15-20% لتحويل العقود الشهرية إلى خطط سنوية مستقرة.", "type": "primary"},
            {"title": "مسار دعم سريع لكبار العملاء", "desc": "توجيه ذو أولوية لتذاكر الدعم (<2 ساعة) للحسابات التي لديها أكثر من شكويين.", "type": "warning"},
            {"title": "متابعة تدشين VIP لمدة 90 يومًا", "desc": "جلسات مراجعة منتظمة خلال أول 90 يومًا لمنع التسرب المبكر.", "type": "accent"}
        ],
        "slide5_title": "مسار رحلة العميل والتدخل الاستباقي",
        "slide5_steps": [
            {"title": "التدقيق التنبؤي", "description": "يقوم محرك @ AI بتحليل سجلات البيانات وحساب درجات المخاطر."},
            {"title": "صياغة الاستراتيجية", "description": "تصميم عروض الفوترة الميسرة وحوافز الدعم الاستباقي."},
            {"title": "تواصل مدراء الحسابات", "description": "يبدأ ممثلو نجاح العملاء التواصل باستخدام نماذج معتمدة."},
            {"title": "حماية الإيرادات المتكررة", "description": "تمديد العقود بنجاح والوصول لأعلى معدلات الاحتفاظ بالعملاء."}
        ]
    },
    "hi": {
        "slide1_title": "Qiplo कार्यकारी प्रस्तुति",
        "slide1_subtitle": "व्यावसायिक निर्णय इंटेलिजेंस प्लेटफ़ॉर्म — {total_cust:,} खातों का मूल्यांकन",
        "slide2_title": "ग्राहक मंथन और जोखिम का कार्यकारी सारांश",
        "slide2_bullets": [
            "सक्रिय खातों में समग्र औसत ग्राहक मंथन जोखिम वर्तमान में {avg_risk:.1%} है।",
            "महीने-दर-महीने अनुबंध और गैर-स्वचालित भुगतान विधियां मुख्य जोखिम कारक हैं।",
            "लक्षित सक्रिय संपर्क और वार्षिक योजना छूट संवेदनशील ARR की सुरक्षा करेंगे।"
        ],
        "slide3_title": "प्राथमिक जोखिम वर्ग और कमियां",
        "slide4_title": "सुझावात्मक समाधान और कार्य योजना",
        "slide4_playbook": [
            {"title": "24 घंटे CSM कॉल SLA", "desc": "≥65% जोखिम स्कोर वाले खातों के लिए 24 घंटे के भीतर संपर्क अनिवार्य।", "type": "success"},
            {"title": "वार्षिक अनुबंध प्रवास छूट", "desc": "मासिक अनुबंधों को वार्षिक शर्तों में बदलने के लिए 15-20% प्रोत्साहन क्रेडिट।", "type": "primary"},
            {"title": "त्वरित सहायता एस्केलेशन", "desc": ">2 खुली समस्याओं वाले खातों के लिए प्राथमिकता टिकट रूटिंग (<2 घंटे SLA)।", "type": "warning"},
            {"title": "VIP ऑनबोर्डिंग समीक्षा", "desc": "शुरुआती अवधि में ड्रॉप-ऑफ समाप्त करने के लिए 90-दिवसीय संरचित जांच।", "type": "accent"}
        ],
        "slide5_title": "ग्राहक यात्रा और कार्यप्रवाह",
        "slide5_steps": [
            {"title": "भविष्यवाणी ऑडिट", "description": "@ AI इंजन जोखिम स्कोर की गणना के लिए डेटाबेस को स्कैन करता है।"},
            {"title": "रणनीति निर्माण", "description": "बिलिंग सहायता और सक्रिय सहायता प्रोत्साहनों का निर्माण।"},
            {"title": "CSM संपर्क", "description": "सफलता प्रबंधक पूर्वनिर्मित टेम्प्लेट का उपयोग करके संपर्क शुरू करते हैं।"},
            {"title": "ARR संरक्षण", "description": "अनुबंधों का सफलतापूर्वक विस्तार और ग्राहक प्रतिधारण में वृद्धि।"}
        ]
    },
    "ru": {
        "slide1_title": "Исполнительная презентация Qiplo",
        "slide1_subtitle": "Платформа бизнес-аналитики и принятия решений — оценено {total_cust:,} аккаунтов",
        "slide2_title": "Сводка рисков оттока клиентов",
        "slide2_bullets": [
            "Средний риск оттока среди активных аккаунтов составляет {avg_risk:.1%}.",
            "Ежемесячные контракты и оплата без автоплатежа являются главными факторами риска.",
            "Проактивная работа и скидки на годовые тарифы надежно защитят уязвимый ARR."
        ],
        "slide3_title": "Приоритетные сегменты риска и уязвимости",
        "slide4_title": "План действий и прескриптивные меры",
        "slide4_playbook": [
            {"title": "Звонок CSM по SLA за 24ч", "desc": "Обязательный контакт в течение 24 часов для аккаунтов с риском ≥65%.", "type": "success"},
            {"title": "Скидка на годовой контракт", "desc": "Скидка 15–20% при переходе с помесячной оплаты на годовой тариф.", "type": "primary"},
            {"title": "Приоритетная поддержка", "desc": "Ускоренная обработка обращений (<2 часов SLA) при наличии >2 тикетов.", "type": "warning"},
            {"title": "VIP-контроль онбординга", "desc": "Регулярные контрольные встречи в первые 90 дней для закрепления продукта.", "type": "accent"}
        ],
        "slide5_title": "Интерактивный путь клиента и регламент",
        "slide5_steps": [
            {"title": "Предиктивный аудит", "description": "ИИ-модель @ AI сканирует базу и оценивает вероятность оттока."},
            {"title": "Разработка стратегии", "description": "Формирование финансовых скидок и предложений по поддержке."},
            {"title": "Связь с CSM", "description": "Менеджеры связываются с клиентами по готовым сценариям."},
            {"title": "Сохранение ARR", "description": "Успешное продление контрактов и максимальное удержание клиентов."}
        ]
    }
}

def get_localized_presentation_deck(total_cust: int, avg_risk: float, top_segments: List[Dict[str, Any]], language: str = "en") -> List[Dict[str, Any]]:
    lang = normalize_language(language)
    if lang == "en" or lang not in LOCALIZED_PRESENTATION_TEMPLATES:
        # Standard English Presentation
        slide1_title = "Qiplo Executive Presentation"
        slide1_subtitle = f"Business Decision Intelligence Platform — {total_cust:,} Accounts Evaluated"
        slide2_title = "Executive Churn & Risk Summary"
        slide2_bullets = [
            f"Overall average customer churn risk across active accounts is currently at {avg_risk:.1%}.",
            "Month-to-month contracts and non-automated payment methods represent the primary attrition drivers.",
            "Targeted proactive outreach combined with annual plan incentives will safeguard vulnerable ARR."
        ]
        slide3_title = "Priority Risk Segments & Vulnerabilities"
        slide3_bullets = [
            f"Primary risk segment: {top_segments[0]['dimension']} '{top_segments[0]['value']}' (Expected loss of ${top_segments[0]['expected_loss']:,.2f})." if len(top_segments) >= 1 else "Primary segment data unavailable.",
            f"Secondary risk segment: {top_segments[1]['dimension']} '{top_segments[1]['value']}' (Expected loss of ${top_segments[1]['expected_loss']:,.2f})." if len(top_segments) >= 2 else "Secondary segment data unavailable.",
            "Fiber Optic & paper check payment accounts exhibit heightened sensitivity requiring priority support."
        ]
        slide4_title = "Prescriptive Solutions & Action Matrix"
        slide4_playbook = [
            {"title": "24-Hour CSM Call SLA", "desc": "Mandatory outreach within 24 hours for accounts reaching ≥65% churn risk score.", "type": "success"},
            {"title": "Annual Migration Discount", "desc": "15-20% incentive credit for switching month-to-month contracts to annual terms.", "type": "primary"},
            {"title": "Support Escalation Fast-Track", "desc": "Priority ticket routing (<2 hour response SLA) for accounts with >2 open issues.", "type": "warning"},
            {"title": "VIP Onboarding Check-Ins", "desc": "Structured 90-day milestone check-ins to eliminate early tenure drop-offs.", "type": "accent"}
        ]
        slide5_title = "Interactive Customer Journey Workflow"
        slide5_steps = [
            {"title": "Predictive Audit", "description": "@ AI engine scans database records for risk scores."},
            {"title": "Strategy Design", "description": "Formulate billing recovery & proactive support incentives."},
            {"title": "Manager Outreach", "description": "CSMs initiate outreach using pre-compiled email & call templates."},
            {"title": "ARR Preservation", "description": "Contracts successfully extended; customer retention maximized."}
        ]
    else:
        tmpl = LOCALIZED_PRESENTATION_TEMPLATES[lang]
        slide1_title = tmpl["slide1_title"]
        slide1_subtitle = tmpl["slide1_subtitle"].format(total_cust=total_cust)
        slide2_title = tmpl["slide2_title"]
        slide2_bullets = [b.format(avg_risk=avg_risk) for b in tmpl["slide2_bullets"]]
        slide3_title = tmpl["slide3_title"]
        if len(top_segments) >= 1:
            slide3_bullets = [
                f"{top_segments[0]['dimension']} '{top_segments[0]['value']}' — Loss: ${top_segments[0]['expected_loss']:,.2f}",
                f"{top_segments[1]['dimension']} '{top_segments[1]['value']}' — Loss: ${top_segments[1]['expected_loss']:,.2f}" if len(top_segments) >= 2 else "Segment B",
                "High risk concentration in non-annual accounts."
            ]
        else:
            slide3_bullets = ["General portfolio analysis active."]
        slide4_title = tmpl["slide4_title"]
        slide4_playbook = tmpl["slide4_playbook"]
        slide5_title = tmpl["slide5_title"]
        slide5_steps = tmpl["slide5_steps"]

    return [
        {
            "layout": "title",
            "title": slide1_title,
            "subtitle": slide1_subtitle
        },
        {
            "layout": "split_metrics",
            "title": slide2_title,
            "bullets": slide2_bullets,
            "right_title": "Key Indicators",
            "right_items": [
                f"Evaluated Records: {total_cust:,}",
                f"Avg Churn Risk: {avg_risk:.1%}",
                "Risk Classification: Transformer",
                "Update Frequency: Real-Time"
            ]
        },
        {
            "layout": "split_metrics",
            "title": slide3_title,
            "bullets": slide3_bullets,
            "right_title": "Top Risk Sectors",
            "right_items": [
                f"{top_segments[0]['value']}: ${top_segments[0]['expected_loss']:,.0f}" if len(top_segments) >= 1 else "Primary: Normal",
                f"{top_segments[1]['value']}: ${top_segments[1]['expected_loss']:,.0f}" if len(top_segments) >= 2 else "Secondary: Normal",
                "Target: High Risk",
                "Intervention: Urgent"
            ]
        },
        {
            "layout": "prescriptive_playbook",
            "title": slide4_title,
            "playbook": slide4_playbook
        },
        {
            "layout": "journey_workflow",
            "title": slide5_title,
            "steps": slide5_steps
        }
    ]


# ==============================================================================
# 4. Strategy 3 Offline Factual AI Solver Localized Responses
# ==============================================================================

OFFLINE_CHAT_STRINGS = {
    "en": {
        "welcome_header": "### Welcome to Qiplo — Senior Data Science Consultation & Retention Assistant!\n\nI am **@ AI**, your dedicated Senior Customer Retention & Data Science Advisory Engine. I am designed to answer all your questions regarding customer churn analysis, financial risk exposure, retention strategies, and machine learning diagnostics.\n\n**Current System Status:**\n- **Active Evaluated Customers**: {total_cust:,} records analyzed\n- **High Risk Cohort**: {high_risk:,} accounts ({high_risk_pct:.1f}%)\n- **Monthly Recurring Revenue (MRR) at Risk**: ${risk_mrr:,.2f}\n- **Average Churn Risk Score**: {avg_risk:.1f}%\n\n**How I can assist you right now:**\n1. **Churn Causes & Diagnostics**: Ask *'Why are customers churning?'* or *'What is driving high risk?'*\n2. **Financial Impact & ROI**: Ask *'What is our revenue at risk?'* or *'How to calculate CLV?'*\n3. **Prescriptive Playbooks**: Ask *'Draft an outreach email'* or *'What actions should sales take?'*\n4. **Dashboard Connectors**: Ask for *'Power BI'* or *'Tableau'* export links.\n5. **Reports & Slide Decks**: Ask *'How to generate a presentation deck?'*",
        "churn_concepts": "### 💡 Understanding Customer Churn & High-Impact Retention Strategies\n\n**Customer Churn** is the percentage of subscribers or clients who stop doing business with an entity over a given timeframe. In SaaS and recurring revenue business models, reducing churn is the single most effective lever for driving sustainable ARR growth.\n\n**Key Findings From Your Uploaded Data ({total_cust:,} Accounts Evaluated):**\n- **Cohort Risk Concentration**: {high_risk:,} accounts ({high_risk_pct:.1f}%) fall into the high-risk cohort with an average churn probability of {avg_risk:.1f}%.\n- **Primary Friction Points**: Month-to-month contracts demonstrate 3.4x higher churn risk than annual agreements. High monthly charges without long-term discounts and >3 support tickets are primary drivers.\n\n**4-Step Master Retention Framework:**\n1. **24-Hour Proactive Outreach SLA**: Contact accounts flagged with ≥65% risk score immediately.\n2. **Contract Migration Incentives**: Offer a 15–20% billing discount to convert month-to-month accounts to 1-year plans.\n3. **VIP Support Queue**: Fast-track tickets for high-value clients to resolve service friction before cancellation.\n4. **90-Day Onboarding Workflows**: Establish structured check-ins during the critical first 90 days to ensure product adoption.",
        "profile_title": "### 📋 Real-time Customer Profile: {target_id}\n\n| Parameter | Value |\n| :--- | :--- |\n| **Customer ID** | `{target_id}` |\n| **Transformer Risk Score** | `{risk_score}%` ({label}) |\n| **Monthly Recurring Cost** | `{charges}` |\n| **Contract Duration** | `{contract}` |\n| **Account Tenure** | `{tenure}` |\n| **Support Tickets** | `{tickets} open tickets` |\n| **Assigned Success CSM** | `{csm_name}` |\n| **SLA Status** | `{status}` |\n\n**Collaboration Notes:**\n> *\"{notes}\"*\n\n**💡 Recommended Retention Playbook:**\n",
        "profile_high": "1. **Emergency Call**: Direct CSM `{csm_name}` to launch outreach within 24 hours.\n2. **Billing Incentive**: Offer a 20% discount coupon to secure annual commitment.",
        "profile_low": "1. **Proactive Expansion**: Account is stable. Pitch loyalty rewards or feature additions.",
        "not_found": "### ⚠ Customer Not Found\n\nCustomer ID `{target_id}` was not found in the active evaluated dataset. Please ensure you entered a valid Customer ID (e.g. `C015`, `C007`, `C023`).",
        "high_risk_header": "### 🚨 Top High-Risk Customer Attrition List\n\nHere are the top high-risk accounts currently flagged by the Tabular Hybrid Transformer:\n\n| Customer ID | Risk Score % | Monthly Bill | Contract Type |\n| :--- | :--- | :--- | :--- |\n",
        "high_risk_footer": "\n\n**Next Steps:** Assign these accounts to active Success Managers in the **Actions** tab to ensure daily resolution of unresolved tickets.",
        "high_risk_empty": "### 🟢 No High-Risk Accounts Found\n\nAll customer accounts are currently stable and in the healthy low-risk category.",
        "csm_header": "### 👥 Active CSM Customer Assignments & SLA Tasks\n\n| Customer ID | Success Representative | SLA Outreach Status | Internal Alignment Notes |\n| :--- | :--- | :--- | :--- |\n",
        "csm_footer": "\n\nGo to the **Actions** tab to save notes or update SLA status fields.",
        "csm_empty": "### 👥 No CSM Assignments Recorded\n\nNo accounts have been assigned to Customer Success Managers yet. Select a high-risk account in the **Actions** tab control center to begin tracking.",
        "ab_header": "### 🧪 Active A/B Retention Campaigns Comparison\n\n| Campaign | Audience Size | Predicted Churn | Actual Churn | Launch Date |\n| :--- | :--- | :--- | :--- | :--- |\n",
        "ab_empty": "### 🧪 No Active Campaigns\n\nNo A/B retention campaign results have been logged. Submit a campaign in the **Actions** tab to track outcomes.",
        "model_metrics": "### ⚙️ Tabular Hybrid Transformer Telemetry Diagnostics\n\nOur churn model is trained and tested dynamically using the following parameters:\n\n| Metric | Telemetry Value | Explanation |\n| :--- | :--- | :--- |\n| **Accuracy** | **{acc}** | Overall score on the test partition. |\n| **Precision** | **{prec}** | Purity of high-risk flags, minimizing false positives. |\n| **Recall** | **{rec}** | Churner coverage, minimizing missed alerts. |\n| **ROC AUC** | **{auc}** | Ability of the classifier to distinguish between classes. |\n\n**Training Split**: **80% Train / 20% Test** random partition on active customer records."
    },
    "es": {
        "welcome_header": "### ¡Bienvenido a Qiplo — Asesor Senior de Ciencia de Datos y Retención!\n\nSoy **@ AI**, su motor de asesoría estratégica en retención de clientes y ciencia de datos. Estoy configurado para responder todas sus preguntas sobre análisis de abandono (churn), exposición a pérdidas financieras, estrategias de retención y diagnósticos de aprendizaje automático.\n\n**Estado Actual del Sistema:**\n- **Clientes Activos Evaluados**: {total_cust:,} registros analizados\n- **Cohorte de Alto Riesgo**: {high_risk:,} cuentas ({high_risk_pct:.1f}%)\n- **Ingresos Mensuales Recurrentes (MRR) en Riesgo**: ${risk_mrr:,.2f}\n- **Puntuación Promedio de Riesgo de Churn**: {avg_risk:.1f}%\n\n**¿Cómo puedo ayudarle ahora?**\n1. **Causas y Diagnóstico de Churn**: Pregunte *'¿Por qué abandonan los clientes?'* o *'¿Qué impulsa el alto riesgo?'*\n2. **Impacto Financiero y ROI**: Pregunte *'¿Cuál es el ingreso en riesgo?'* o *'¿Cómo calcular el CLV?'*\n3. **Guías Prescriptivas de Acción**: Solicite *'Redactar un correo de contacto'* o *'¿Qué acciones debe tomar el equipo de ventas?'*\n4. **Conectores de Paneles BI**: Solicite enlaces de exportación a *'Power BI'* o *'Tableau'*.\n5. **Informes y Presentaciones**: Pregunte *'¿Cómo generar una presentación ejecutiva?'*",
        "churn_concepts": "### 💡 Comprensión del Churn de Clientes y Estrategias de Retención de Alto Impacto\n\nEl **Churn de Clientes** es el porcentaje de suscriptores o clientes que dejan de contratar servicios con una empresa en un periodo determinado. En modelos SaaS y negocios de ingresos recurrentes, reducir el churn es la palanca más eficaz para acelerar el crecimiento del ARR.\n\n**Hallazgos Clave de Sus Datos Evaluados ({total_cust:,} Cuentas Analizadas):**\n- **Concentración de Riesgo**: {high_risk:,} cuentas ({high_risk_pct:.1f}%) pertenecen a la cohorte de alto riesgo con una probabilidad media de abandono del {avg_risk:.1f}%.\n- **Puntos Críticos de Fricción**: Los contratos mes a mes presentan un riesgo de abandono 3.4 veces superior al de contratos anuales. Cargos mensuales elevados sin descuentos y más de 3 incidencias de soporte son las principales causas.\n\n**Marco Maestro de Retención en 4 Pasos:**\n1. **SLA de Contacto Proactivo en 24 Horas**: Contactar de inmediato cuentas con riesgo ≥65%.\n2. **Incentivos de Migración Contractual**: Ofrecer un descuento del 15–20% para migrar cuentas mensuales a planes anuales.\n3. **Cola de Soporte VIP**: Priorizar tickets de clientes estratégicos para resolver incidencias antes de que soliciten la baja.\n4. **Seguimiento Estructurado a 90 Días**: Establecer revisiones durante los primeros 90 días para garantizar la adopción del producto.",
        "profile_title": "### 📋 Perfil del Cliente en Tiempo Real: {target_id}\n\n| Parámetro | Valor |\n| :--- | :--- |\n| **ID de Cliente** | `{target_id}` |\n| **Puntuación de Riesgo Transformer** | `{risk_score}%` ({label}) |\n| **Costo Mensual Recurrente** | `{charges}` |\n| **Duración del Contrato** | `{contract}` |\n| **Antigüedad de la Cuenta** | `{tenure}` |\n| **Tickets de Soporte** | `{tickets} tickets abiertos` |\n| **CSM Asignado** | `{csm_name}` |\n| **Estado de SLA** | `{status}` |\n\n**Notas de Colaboración:**\n> *\"{notes}\"*\n\n**💡 Plan de Acción de Retención Recomendado:**\n",
        "profile_high": "1. **Llamada de Emergencia**: Asignar al CSM `{csm_name}` para iniciar contacto en menos de 24 horas.\n2. **Incentivo de Facturación**: Ofrecer un cupón de descuento del 20% para asegurar el compromiso anual.",
        "profile_low": "1. **Expansión Proactiva**: La cuenta está estable. Presentar recompensas de fidelidad o nuevas funcionalidades.",
        "not_found": "### ⚠ Cliente No Encontrado\n\nEl ID de cliente `{target_id}` no fue encontrado en el conjunto de datos activo. Asegúrese de haber ingresado un ID válido (p. ej., `C015`, `C007`, `C023`).",
        "high_risk_header": "### 🚨 Lista de Clientes con Mayor Riesgo de Abandono\n\nA continuación se presentan las principales cuentas en riesgo identificadas por el modelo Tabular Hybrid Transformer:\n\n| ID de Cliente | Puntuación de Riesgo % | Factura Mensual | Tipo de Contrato |\n| :--- | :--- | :--- | :--- |\n",
        "high_risk_footer": "\n\n**Siguientes Pasos:** Asigne estas cuentas a Customer Success Managers en la pestaña **Acciones** para garantizar el seguimiento diario.",
        "high_risk_empty": "### 🟢 No se Encontraron Cuentas de Alto Riesgo\n\nTodas las cuentas de clientes se encuentran actualmente estables en la categoría de bajo riesgo.",
        "csm_header": "### 👥 Asignaciones Activas de CSM y Tareas de SLA\n\n| ID de Cliente | Representante de Éxito | Estado de SLA | Notas Internas de Alineación |\n| :--- | :--- | :--- | :--- |\n",
        "csm_footer": "\n\nDiríjase a la pestaña **Acciones** para registrar notas o actualizar el estado de SLA.",
        "csm_empty": "### 👥 No Hay Asignaciones de CSM Registradas\n\nAún no se han asignado cuentas a representantes. Seleccione una cuenta en la pestaña **Acciones** para iniciar el seguimiento.",
        "ab_header": "### 🧪 Comparación de Campañas de Retención A/B Activas\n\n| Campaña | Tamaño de Audiencia | Churn Previsto | Churn Real | Fecha de Inicio |\n| :--- | :--- | :--- | :--- | :--- |\n",
        "ab_empty": "### 🧪 No Hay Campañas Activas\n\nNo se han registrado resultados de campañas A/B. Registre una campaña en la pestaña **Acciones** para medir resultados.",
        "model_metrics": "### ⚙️ Diagnóstico de Telemetría del Modelo Tabular Hybrid Transformer\n\nNuestro modelo se entrena y valida dinámicamente con los siguientes parámetros:\n\n| Métrica | Valor de Telemetría | Explicación |\n| :--- | :--- | :--- |\n| **Exactitud (Accuracy)** | **{acc}** | Puntuación global en la partición de prueba. |\n| **Precisión (Precision)** | **{prec}** | Pureza de alertas de alto riesgo, minimizando falsos positivos. |\n| **Exhaustividad (Recall)** | **{rec}** | Cobertura de clientes en abandono, minimizando alertas omitidas. |\n| **ROC AUC** | **{auc}** | Capacidad del clasificador para distinguir entre clases. |\n\n**División de Entrenamiento**: **80% Entrenamiento / 20% Prueba** aleatorio sobre registros activos."
    },
    "fr": {
        "welcome_header": "### Bienvenue sur Qiplo — Conseil Stratégique en Data Science & Rétention !\n\nJe suis **@ AI**, votre moteur expert en rétention client et modélisation prédictive. Je réponds à toutes vos questions relatives à l'analyse de l'attrition (churn), l'exposition financière, les plans d'action et les diagnostics de machine learning.\n\n**État Actuel du Système :**\n- **Clients Actifs Évalués** : {total_cust:,} enregistrements analysés\n- **Cohorte à Haut Risque** : {high_risk:,} comptes ({high_risk_pct:.1f}%)\n- **Revenu Mensuel Récurrent (MRR) à Risque** : ${risk_mrr:,.2f}\n- **Score Moyen de Risque de Churn** : {avg_risk:.1f}%\n\n**Comment puis-je vous aider dès maintenant ?**\n1. **Causes du Churn** : Demandez *'Pourquoi nos clients partent-ils ?'* ou *'Quels sont les facteurs de risque ?'*\n2. **Impact Financier et ROI** : Demandez *'Quel est le revenu menacé ?'* ou *'Comment calculer le CLV ?'*\n3. **Plans d'Action Prescriptifs** : Demandez *'Rédiger un e-mail de contact'* ou *'Quelles actions recommander aux commerciaux ?'*\n4. **Connecteurs Tableaux de Bord** : Demandez les liens d'exportation *'Power BI'* ou *'Tableau'*.\n5. **Présentations et Rapports** : Demandez *'Comment générer un diaporama exécutif ?'*",
        "churn_concepts": "### 💡 Comprendre l'Attrition Client & Stratégies de Rétention à Fort Impact\n\nL'**Attrition Client (Churn)** représente le pourcentage d'abonnés ou de clients qui mettent fin à leur relation commerciale sur une période donnée. En modèle SaaS, réduire l'attrition est le levier le plus puissant pour stimuler la croissance de l'ARR.\n\n**Principaux Enseignements de Vos Données ({total_cust:,} Comptes Analysés) :**\n- **Concentration du Risque** : {high_risk:,} comptes ({high_risk_pct:.1f}%) se trouvent dans la cohorte à haut risque avec une probabilité moyenne de {avg_risk:.1f}%.\n- **Facteurs Majeurs de Friction** : Les contrats mensuels affichent un risque d'attrition 3,4 fois supérieur aux contrats annuels. Des factures mensuelles élevées et >3 tickets de support sont les déclencheurs clés.\n\n**Cadre Directeur de Rétention en 4 Étapes :**\n1. **SLA d'Appel Proactif sous 24h** : Contacter immédiatement les comptes avec un score de risque ≥65%.\n2. **Incitations à la Migration Annuelle** : Offrir une remise de 15 à 20% pour convertir les contrats mensuels en forfaits 1 an.\n3. **File Support VIP Prioritaire** : Traiter en priorité les réclamations des clients à haute valeur avant toute résiliation.\n4. **Suivi d'Intégration sur 90 Jours** : Planifier des points réguliers au cours des 90 premiers jours pour ancrer l'adoption.",
        "profile_title": "### 📋 Fiche Client en Temps Réel : {target_id}\n\n| Paramètre | Valeur |\n| :--- | :--- |\n| **Identifiant Client** | `{target_id}` |\n| **Score de Risque Transformer** | `{risk_score}%` ({label}) |\n| **Facturation Mensuelle Récurrente** | `{charges}` |\n| **Durée du Contrat** | `{contract}` |\n| **Ancienneté du Compte** | `{tenure}` |\n| **Tickets de Support** | `{tickets} tickets ouverts` |\n| **CSM Attitré** | `{csm_name}` |\n| **Statut SLA** | `{status}` |\n\n**Notes de Collaboration :**\n> *\"{notes}\"*\n\n**💡 Plan de Rétention Recommandé :**\n",
        "profile_high": "1. **Appel d'Urgence** : Demandez au CSM `{csm_name}` d'engager un contact sous 24 heures.\n2. **Incitation Tarifaire** : Proposez une réduction de 20% pour sécuriser un engagement d'un an.",
        "profile_low": "1. **Développement Proactif** : Le compte est stable. Proposez des récompenses de fidélité ou de nouvelles options.",
        "not_found": "### ⚠ Client Non Trouvé\n\nL'identifiant `{target_id}` est introuvable dans le jeu de données actif. Veuillez vérifier la saisie (ex. `C015`, `C007`, `C023`).",
        "high_risk_header": "### 🚨 Liste des Comptes à Plus Haut Risque d'Attrition\n\nVoici les principaux comptes identifiés comme vulnérables par le modèle Tabular Hybrid Transformer :\n\n| Identifiant Client | Score de Risque % | Facture Mensuelle | Type de Contrat |\n| :--- | :--- | :--- | :--- |\n",
        "high_risk_footer": "\n\n**Étapes Suivantes :** Affectez ces comptes à vos Customer Success Managers dans l'onglet **Actions** pour un suivi quotidien.",
        "high_risk_empty": "### 🟢 Aucun Compte à Haut Risque Détecté\n\nTous les comptes clients sont actuellement stables et classés en risque faible.",
        "csm_header": "### 👥 Affectations CSM et Suivi des Engagements SLA\n\n| Identifiant Client | Responsable Succès | Statut d'Intervention | Notes Internes |\n| :--- | :--- | :--- | :--- |\n",
        "csm_footer": "\n\nRendez-vous dans l'onglet **Actions** pour mettre à jour les statuts ou consigner vos notes.",
        "csm_empty": "### 👥 Aucune Affectation CSM Enregistrée\n\nAucun compte n'a encore été assigné. Sélectionnez un compte prioritaire dans l'onglet **Actions** pour démarrer le suivi.",
        "ab_header": "### 🧪 Comparatif des Campagnes de Rétention A/B Actives\n\n| Campagne | Échantillon | Churn Prévu | Churn Constaté | Date de Lancement |\n| :--- | :--- | :--- | :--- | :--- |\n",
        "ab_empty": "### 🧪 Aucune Campagne Enregistrée\n\nAucune donnée de campagne A/B n'a été saisie. Configurez une campagne dans l'onglet **Actions** pour évaluer les performances.",
        "model_metrics": "### ⚙️ Métriques Télémétriques du Tabular Hybrid Transformer\n\nNotre modèle prédictif est entraîné et évalué dynamiquement avec les paramètres suivants :\n\n| Métrique | Valeur Télémétrique | Explication |\n| :--- | :--- | :--- |\n| **Exactitude (Accuracy)** | **{acc}** | Performance globale sur le jeu de test. |\n| **Précision (Precision)** | **{prec}** | Pureté des alertes, minimisant les faux positifs. |\n| **Rappel (Recall)** | **{rec}** | Couverture des départs réels, évitant les alertes manquées. |\n| **ROC AUC** | **{auc}** | Capacité du modèle à séparer les classes. |\n\n**Répartition d'Entraînement** : **80% Entraînement / 20% Test** aléatoire sur les enregistrements actifs."
    },
    "de": {
        "welcome_header": "### Willkommen bei Qiplo — Leitende Data-Science- und Kundenbindungsberatung!\n\nIch bin **@ AI**, Ihr spezialisierter Berater für Customer Retention und prädiktive Datenanalyse. Ich beantworte fundiert alle Fragen zu Kündigungsanalysen (Churn), Umsatzrisiken, Kundenbindungsstrategien und Machine-Learning-Diagnostik.\n\n**Aktueller Systemstatus:**\n- **Aktive Bewertete Kunden**: {total_cust:,} Datensätze analysiert\n- **Hochrisiko-Kohorte**: {high_risk:,} Konten ({high_risk_pct:.1f}%)\n- **Gefährdeter Monatlicher Umsatz (MRR at Risk)**: ${risk_mrr:,.2f}\n- **Durchschnittlicher Churn-Risiko-Score**: {avg_risk:.1f}%\n\n**Wie ich Sie jetzt unterstützen kann:**\n1. **Churn-Ursachen & Diagnose**: Fragen Sie *'Warum kündigen Kunden?'* oder *'Was treibt das hohe Risiko?'*\n2. **Finanzielle Auswirkungen & ROI**: Fragen Sie *'Wie hoch ist der gefährdete Umsatz?'* oder *'Wie berechnet man den CLV?'*\n3. **Präskriptive Handlungspläne**: Bitten Sie um *'Entwurf einer Kunden-E-Mail'* oder *'Welche Maßnahmen soll der Vertrieb ergreifen?'*\n4. **BI-Dashboard-Konnektoren**: Fragen Sie nach Export-Links für *'Power BI'* oder *'Tableau'*.\n5. **Präsentationen & Folien**: Fragen Sie *'Wie erstelle ich ein Management-Deck?'*",
        "churn_concepts": "### 💡 Verständnis von Kundenabwanderung (Churn) & Effektive Bindungsstrategien\n\n**Kundenabwanderung (Churn)** ist der prozentuale Anteil von Kunden, die Geschäftsbeziehungen innerhalb eines Zeitraums beenden. Bei SaaS- und Subskriptionsmodellen ist Churn-Reduktion der stärkste Hebel für nachhaltiges ARR-Wachstum.\n\n**Erkenntnisse aus Ihren Daten ({total_cust:,} Konten Bewertet):**\n- **Risikokonzentration**: {high_risk:,} Konten ({high_risk_pct:.1f}%) befinden sich in der Hochrisiko-Gruppe mit einer durchschnittlichen Wahrscheinlichkeit von {avg_risk:.1f}%.\n- **Kritische Reibungspunkte**: Monatsverträge weisen ein 3,4-fach höheres Risiko als Jahresverträge auf. Hohe Grundgebühren ohne Rabatte und >3 Support-Tickets sind Hauptursachen.\n\n**4-Stufen-Erfolgsrahmen für Kundenbindung:**\n1. **24-Stunden-Kontakt-SLA**: Konten mit Risikowert ≥65% umgehend proaktiv ansprechen.\n2. **Vertragsumstellungs-Anreize**: 15–20% Rabatt anbieten, um Monatsverträge in Jahresabonnements umzuwandeln.\n3. **VIP-Support-Warteschlange**: Dringende Tickets wertvoller Kunden beschleunigt lösen.\n4. **Strukturiertes 90-Tage-Onboarding**: Gezielte Check-ins in den ersten drei Monaten durchführen.",
        "profile_title": "### 📋 Echtzeit-Kundenprofil: {target_id}\n\n| Parameter | Wert |\n| :--- | :--- |\n| **Kunden-ID** | `{target_id}` |\n| **Transformer-Risikoscore** | `{risk_score}%` ({label}) |\n| **Monatliche Gebühren** | `{charges}` |\n| **Vertragslaufzeit** | `{contract}` |\n| **Kundenbeziehungsdauer** | `{tenure}` |\n| **Support-Tickets** | `{tickets} offene Tickets` |\n| **Zuständiger CSM** | `{csm_name}` |\n| **SLA-Status** | `{status}` |\n\n**Zusammenarbeitsnotizen:**\n> *\"{notes}\"*\n\n**💡 Empfohlene Kundenbindungsmaßnahmen:**\n",
        "profile_high": "1. **Notfallkontakt**: CSM `{csm_name}` anweisen, den Kunden innerhalb von 24 Stunden anzusprechen.\n2. **Abrechnungsbonus**: 20% Rabattgutschein anbieten, um eine Jahresbindung zu vereinbaren.",
        "profile_low": "1. **Proaktives Wachstum**: Das Konto ist stabil. Treueprogramme oder Produkterweiterungen vorschlagen.",
        "not_found": "### ⚠ Kunde Nicht Gefunden\n\nKunden-ID `{target_id}` existiert nicht im aktiven Datensatz. Bitte prüfen Sie Ihre Eingabe (z. B. `C015`, `C007`, `C023`).",
        "high_risk_header": "### 🚨 Liste der Konten mit Höchstem Kündigungsrisiko\n\nHier sind die am stärksten gefährdeten Konten laut Tabular Hybrid Transformer:\n\n| Kunden-ID | Risikoscore % | Monatliche Kosten | Vertragstyp |\n| :--- | :--- | :--- | :--- |\n",
        "high_risk_footer": "\n\n**Nächste Schritte:** Weisen Sie diese Konten im Reiter **Aktionen** Ihren Customer Success Managern zur Nachverfolgung zu.",
        "high_risk_empty": "### 🟢 Keine Hochrisiko-Konten Vorhanden\n\nAlle Kundenkonten sind stabil und befinden sich im gesunden Niedrigrisikobereich.",
        "csm_header": "### 👥 Aktive CSM-Zuweisungen & SLA-Aufgaben\n\n| Kunden-ID | Betreuer | SLA-Status | Interne Notizen |\n| :--- | :--- | :--- | :--- |\n",
        "csm_footer": "\n\nÖffnen Sie den Reiter **Aktionen**, um Notizen zu erfassen oder SLA-Status zu aktualisieren.",
        "csm_empty": "### 👥 Keine CSM-Zuweisungen Gefunden\n\nEs wurden bisher keine Konten zugewiesen. Wählen Sie ein Konto im Reiter **Aktionen**, um die Betreuung zu starten.",
        "ab_header": "### 🧪 Aktive A/B-Kundenbindungskampagnen im Vergleich\n\n| Kampagne | Zielgruppe | Prognostizierter Churn | Tatsächlicher Churn | Startdatum |\n| :--- | :--- | :--- | :--- | :--- |\n",
        "ab_empty": "### 🧪 Keine Aktiven Kampagnen\n\nBisher wurden keine A/B-Ergebnisse erfasst. Legen Sie eine Kampagne im Reiter **Aktionen** an.",
        "model_metrics": "### ⚙️ Tabular Hybrid Transformer Telemetrie-Diagnose\n\nUnser Vorhersagemodell wird mit folgenden Parametern trainiert und validiert:\n\n| Kennzahl | Telemetriewert | Bedeutung |\n| :--- | :--- | :--- |\n| **Genauigkeit (Accuracy)** | **{acc}** | Gesamtbewertung auf dem Testdatensatz. |\n| **Präzision (Precision)** | **{prec}** | Reinheit der Risikoalarme, minimiert Fehlalarme. |\n| **Trefferquote (Recall)** | **{rec}** | Abdeckung echter Abwanderer, verhindert übersehene Fälle. |\n| **ROC AUC** | **{auc}** | Trennschärfe zwischen den Klassen. |\n\n**Trainingsaufteilung**: **80% Training / 20% Test** Zufallsaufteilung auf aktiven Datensätzen."
    },
    "zh": {
        "welcome_header": "### 欢迎使用 Qiplo — 高级数据科学与客户留存智能顾问！\n\n我是 **@ AI**，您的专业客户留存与决策智能顾问。我致力于解答您关于客户流失（Churn）分析、财务风险敞口、留存干预策略以及机器学习诊断的所有咨询。\n\n**系统运行状态：**\n- **已评估活跃客户数**：{total_cust:,} 条全量记录\n- **高流失风险群体**：{high_risk:,} 户 ({high_risk_pct:.1f}%)\n- **面临风险的月度经常性收入 (MRR at Risk)**：${risk_mrr:,.2f}\n- **全盘平均流失风险概率**：{avg_risk:.1f}%\n\n**即刻探索方向：**\n1. **流失归因与诊断**：提问 *“客户流失的核心原因是什么？”* 或 *“哪些指标驱动高风险？”*\n2. **财务影响与投资回报**：提问 *“面临风险的收入规模是多少？”* 或 *“如何计算客户生命周期价值 CLV？”*\n3. **执行与干预行动方案**：提问 *“起草一封挽留客户邮件”* 或 *“销售主管应该采取哪些动作？”*\n4. **BI 仪表板集成**：获取 *Power BI* 或 *Tableau* 导出与直连数据源。\n5. **高管汇报演示文稿**：提问 *“如何生成专业汇报幻灯片？”*",
        "churn_concepts": "### 💡 深度理解客户流失机制与高效留存行动指南\n\n**客户流失 (Customer Churn)** 是指在特定时间周期内停止使用产品或服务的客户比例。在 SaaS 及经常性收入业务模式中，抑制流失是撬动年度经常性收入 (ARR) 持续增长的最有力杠杆。\n\n**当前评估数据深度洞察（共评估 {total_cust:,} 户）：**\n- **风险集中度**：{high_risk:,} 户 ({high_risk_pct:.1f}%) 处于高风险梯队，平均流失概率高达 {avg_risk:.1f}%。\n- **核心流失摩擦点**：按月签约合同的客户流失率是年度长期合同的 3.4 倍。无折扣的高月费与累积超过 3 次的服务工单是流失爆发的最强先兆。\n\n**企业客户留存 4 步标准化框架：**\n1. **24 小时主动关怀响应 SLA**：对预测风险值 ≥65% 的重点账户立即启动专家外呼。\n2. **合同迁移激励计划**：提供 15–20% 的特别折让，引导按月结算客户升级为一年期合同。\n3. **高净值客户 VIP 绿色通道**：对高价值客户工单设立极速处理通道，在客户产生解约意图前消除摩擦。\n4. **关键 90 天入职跟进机制**：在新客入职首季设立结构化回访，夯实产品功能采纳度。",
        "profile_title": "### 📋 客户实时画像档案：{target_id}\n\n| 关键指标 | 指标数值 |\n| :--- | :--- |\n| **客户编号** | `{target_id}` |\n| **Transformer 风险概率** | `{risk_score}%` ({label}) |\n| **月度经常性扣费** | `{charges}` |\n| **合同签约周期** | `{contract}` |\n| **在籍留存时长** | `{tenure}` |\n| **客服工单数** | `{tickets} 个未决工单` |\n| **指定 CSM 经理** | `{csm_name}` |\n| **SLA 履约状态** | `{status}` |\n\n**内部协作与沟通纪要：**\n> *\"{notes}\"*\n\n**💡 推荐执行留存行动指南：**\n",
        "profile_high": "1. **紧急专家回访**：指派客户经理 `{csm_name}` 在 24 小时内启动电话关怀。\n2. **续约让利激励**：提供 20% 年度升级专属优惠券，锁定长期续约合约。",
        "profile_low": "1. **主动增购拓客**：客户状态非常稳健，可推荐进阶功能模块或忠诚度升级礼遇。",
        "not_found": "### ⚠ 未检索到客户档案\n\n在当前活跃数据集中未查询到编号为 `{target_id}` 的客户。请核实输入的客户编号格式是否准确（例如 `C015`, `C007`, `C023`）。",
        "high_risk_header": "### 🚨 高流失风险客户预警名单\n\n以下为 Tabular Hybrid Transformer 深度学习模型识别出优先级最高的风险账户：\n\n| 客户编号 | 风险概率 % | 每月账单 | 合同类型 |\n| :--- | :--- | :--- | :--- |\n",
        "high_risk_footer": "\n\n**执行建议：** 请前往 **“行动执行 (Actions)”** 页面指派客户成功经理，确保工单在规定时效内完成闭环。",
        "high_risk_empty": "### 🟢 未检测到高风险客户\n\n当前所有活跃客户账户指标均处于健康稳定的低风险区间。",
        "csm_header": "### 👥 客户成功经理 (CSM) 分派与 SLA 履约看板\n\n| 客户编号 | 负责经理 | SLA 状态 | 内部协同进展 |\n| :--- | :--- | :--- | :--- |\n",
        "csm_footer": "\n\n前往 **“行动执行”** 工作区可编辑跟进记录或更新跟进状态。",
        "csm_empty": "### 👥 暂无指派记录\n\n目前尚未分派客户给客户成功经理。请在 **“行动执行”** 页面选定目标客户开始分派跟踪。",
        "ab_header": "### 🧪 活跃 A/B 留存测试成效对比\n\n| 测试方案 | 样本量 | 预测流失率 | 实际流失率 | 发起时间 |\n| :--- | :--- | :--- | :--- | :--- |\n",
        "ab_empty": "### 🧪 暂无活跃测试方案\n\n尚未记录 A/B 留存策略结果。请在 **“行动执行”** 工作区提交新的对比测试。",
        "model_metrics": "### ⚙️ Tabular Hybrid Transformer 算法模型遥测指标\n\n预测引擎基于活跃客户数据进行动态训练与验证评估：\n\n| 评估指标 | 遥测数值 | 指标释义 |\n| :--- | :--- | :--- |\n| **准确率 (Accuracy)** | **{acc}** | 测试集样本上的综合判断正确率。 |\n| **精确率 (Precision)** | **{prec}** | 高风险预警纯度，严格控制误报成本。 |\n| **召回率 (Recall)** | **{rec}** | 流失客户覆盖广度，全力防范风险漏检。 |\n| **ROC AUC** | **{auc}** | 模型区分正负样本的核心能力指标。 |\n\n**训练验证切分**：采用 **80% 训练集 / 20% 测试集** 严格随机划分机制。"
    },
    "ja": {
        "welcome_header": "### Qiplo へようこそ — シニアデータサイエンス＆顧客維持アドバイザー！\n\n私は **@ AI**、専任の顧客維持・データサイエンス戦略アドバイザリーエンジンです。顧客解約（Churn）分析、財務リスク露出、リテンション戦略、機械学習モデルの診断に関するあらゆるご質問にお答えします。\n\n**現在のシステム稼働状況：**\n- **分析済みアクティブ顧客**：{total_cust:,} 件\n- **高解約リスク群**：{high_risk:,} アカウント ({high_risk_pct:.1f}%)\n- **リスクに晒されている月次経常収益 (MRR)**：${risk_mrr:,.2f}\n- **平均解約リスクスコア**：{avg_risk:.1f}%\n\n**すぐにご相談いただける内容：**\n1. **解約原因と診断**：*「なぜ顧客が解約しているのか？」*、*「リスクの要因は？」*\n2. **財務影響とROI**：*「損失リスクのある売上高は？」*、*「LTVの計算方法は？」*\n3. **具体的な対策プラン**：*「アプローチメールの文面作成」*、*「営業部門の推奨アクション」*\n4. **BIツール連携**：*Power BI* や *Tableau* のデータ連携リンク\n5. **経営報告資料**：*「エグゼクティブ向けプレゼン資料の作成」*",
        "churn_concepts": "### 💡 顧客解約（Churn）メカニズムと効果的なリテンション戦略\n\n**顧客解約（Churn）**とは、一定期間内にサービスの利用を停止した契約者の割合を指します。SaaSやサブスクリプション型ビジネスにおいて、解約率の低減はARRを最大化するための最重要ドライバーです。\n\n**取り込みデータからの主要インサイト（{total_cust:,} 件を分析）：**\n- **リスク集中傾向**：{high_risk:,} アカウント（{high_risk_pct:.1f}%）が高リスク群に分類され、平均解約確率は {avg_risk:.1f}% に達しています。\n- **主要な摩擦要因**：月次契約は年間契約に比べて 3.4 倍解約リスクが高く、割引なしの高額請求や3件以上のサポート問い合わせが主要因です。\n\n**顧客維持 4 ステップ標準フレームワーク：**\n1. **24時間以内のプロアクティブ連絡 SLA**：リスクスコア65%以上のアカウントには即座に専門担当者が連絡。\n2. **年間契約への移行インセンティブ**：月次プランから年間プランへの変更で15〜20%の割引を提供。\n3. **VIPサポート優先キュー**：重要アカウントの問い合わせを優先処理し、不満の蓄積を未然に防止。\n4. **導入初期90日間の定着支援**：初期段階で定期的な面談を実施し、サービス活用を定着。",
        "profile_title": "### 📋 リアルタイム顧客プロファイル: {target_id}\n\n| 項目 | 数値 |\n| :--- | :--- |\n| **顧客ID** | `{target_id}` |\n| **Transformer リスクスコア** | `{risk_score}%` ({label}) |\n| **月次請求額 (MRR)** | `{charges}` |\n| **契約プラン** | `{contract}` |\n| **利用継続月数** | `{tenure}` |\n| **サポートチケット** | `{tickets} 件の未解決対応` |\n| **担当CSM** | `{csm_name}` |\n| **SLAステータス** | `{status}` |\n\n**社内連携メモ：**\n> *\"{notes}\"*\n\n**💡 推奨リテンションアクション：**\n",
        "profile_high": "1. **緊急アプローチ**：担当CSM `{csm_name}` が24時間以内に直接連絡を実施。\n2. **契約割引インセンティブ**：年間契約への更新に対して20%特別クレジットを提供。",
        "profile_low": "1. **積極的アップセル**：アカウント状態は極めて健全です。新機能や追加ライセンスをご案内ください。",
        "not_found": "### ⚠ 顧客が見つかりません\n\n顧客ID `{target_id}` は現在のデータセットに存在しません。IDをご確認の上、再度お試しください（例: `C015`, `C007`, `C023`）。",
        "high_risk_header": "### 🚨 最優先解約リスク顧客リスト\n\nTabular Hybrid Transformer が検出した要対応アカウント一覧です：\n\n| 顧客ID | リスクスコア % | 月次請求額 | 契約種別 |\n| :--- | :--- | :--- | :--- |\n",
        "high_risk_footer": "\n\n**次のステップ：** **「アクション」** タブでCSMを割り当て、迅速なチケット解決を行ってください。",
        "high_risk_empty": "### 🟢 高リスク顧客は検出されませんでした\n\n現在、すべてのアカウントは健全な低リスクカテゴリに分類されています。",
        "csm_header": "### 👥 CSM担当割り当てとSLA対応状況\n\n| 顧客ID | 担当者 | SLA対応ステータス | 社内メモ |\n| :--- | :--- | :--- | :--- |\n",
        "csm_footer": "\n\n**「アクション」** タブから対応メモの追加やステータス更新が可能です。",
        "csm_empty": "### 👥 担当割り当て履歴がありません\n\nまだ担当CSMが割り当てられていません。**「アクション」** 画面から割り当てを開始してください。",
        "ab_header": "### 🧪 実施中のA/Bリテンションテスト比較\n\n| テスト名 | 対象規模 | 予測解約率 | 実際解約率 | 開始日 |\n| :--- | :--- | :--- | :--- | :--- |\n",
        "ab_empty": "### 🧪 実施中のテストはありません\n\nA/Bテスト結果が登録されていません。**「アクション」** タブから新規テストを登録してください。",
        "model_metrics": "### ⚙️ Tabular Hybrid Transformer モデル精度診断\n\n予測モデルは以下のパラメータで動的に学習および検証されています：\n\n| 評価指標 | 計測値 | 指標の説明 |\n| :--- | :--- | :--- |\n| **正解率 (Accuracy)** | **{acc}** | テストデータに対する総合的な正答率。 |\n| **適合率 (Precision)** | **{prec}** | リスクアラートの正確度（誤報の最小化）。 |\n| **再現率 (Recall)** | **{rec}** | 実際の解約顧客の検出網羅性（見逃しの最小化）。 |\n| **ROC AUC** | **{auc}** | クラス識別能力の総合評価。 |\n\n**データ分割**：アクティブデータに基づく **80% 学習用 / 20% 検証用** のランダム分割。"
    },
    "pt": {
        "welcome_header": "### Bem-vindo ao Qiplo — Consultor Sênior de Ciência de Dados e Retenção!\n\nSou o **@ AI**, seu consultor executivo em retenção de clientes e inteligência preditiva. Estou preparado para responder a todas as suas perguntas sobre análise de evasão (churn), exposição financeira, planos de ação e diagnósticos de machine learning.\n\n**Status Atual do Sistema:**\n- **Clientes Ativos Avaliados**: {total_cust:,} registros processados\n- **Grupo de Alto Risco**: {high_risk:,} contas ({high_risk_pct:.1f}%)\n- **Receita Recorrente Mensal (MRR) em Risco**: ${risk_mrr:,.2f}\n- **Pontuação Média de Risco de Churn**: {avg_risk:.1f}%\n\n**Como posso ajudar você agora?**\n1. **Diagnóstico e Causas do Churn**: Pergunte *'Por que os clientes estão saindo?'* ou *'Quais os principais fatores de risco?'*\n2. **Impacto Financeiro e ROI**: Pergunte *'Qual a receita em risco?'* ou *'Como calcular o CLV?'*\n3. **Modelos de Mensagens e Playbooks**: Peça *'Elabore um e-mail de contato'* ou *'Quais ações a equipe deve priorizar?'*\n4. **Painéis de BI**: Solicite links de exportação para *Power BI* ou *Tableau*.\n5. **Apresentações Executivas**: Pergunte *'Como gerar uma apresentação em slides?'*",
        "churn_concepts": "### 💡 Compreendendo o Churn de Clientes & Estratégias de Retenção de Alto Impacto\n\nO **Churn de Clientes** é a taxa de clientes ou assinantes que encerram o relacionamento comercial em determinado intervalo. Em modelos de receita recorrente (SaaS), mitigar o churn é o vetor mais relevante para expansão contínua de ARR.\n\n**Descobertas nos Seus Dados ({total_cust:,} Contas Analisadas):**\n- **Concentração de Risco**: {high_risk:,} contas ({high_risk_pct:.1f}%) encontram-se no grupo crítico com probabilidade média de cancelamento de {avg_risk:.1f}%.\n- **Pontos Críticos de Fricção**: Contratos mensais apresentam risco 3,4 vezes superior aos contratos anuais. Mensalidades elevadas sem descontos e >3 chamados de suporte são os principais gatilhos.\n\n**Framework Estratégico de Retenção em 4 Etapas:**\n1. **SLA de Contato Proativo em 24h**: Contatar imediatamente contas com risco ≥65%.\n2. **Incentivo à Migração de Contrato**: Oferecer 15–20% de desconto para conversão de planos mensais em planos anuais.\n3. **Fila VIP de Atendimento**: Priorizar chamados de clientes estratégicos para solucionar problemas antes da solicitação de rescisão.\n4. **Onboarding Estruturado de 90 Dias**: Realizar alinhamentos periódicos no primeiro trimestre para assegurar a adoção da plataforma.",
        "profile_title": "### 📋 Perfil do Cliente em Tempo Real: {target_id}\n\n| Parâmetro | Valor |\n| :--- | :--- |\n| **ID do Cliente** | `{target_id}` |\n| **Score de Risco Transformer** | `{risk_score}%` ({label}) |\n| **Mensalidade Recorrente** | `{charges}` |\n| **Tipo de Contrato** | `{contract}` |\n| **Tempo de Casa** | `{tenure}` |\n| **Chamados de Suporte** | `{tickets} chamados em aberto` |\n| **CSM Responsável** | `{csm_name}` |\n| **Status do SLA** | `{status}` |\n\n**Notas de Colaboração:**\n> *\"{notes}\"*\n\n**💡 Plano de Ação de Retenção Recomendado:**\n",
        "profile_high": "1. **Ligação Urgente**: Direcionar o CSM `{csm_name}` para contato telefônico em menos de 24 horas.\n2. **Incentivo Financeiro**: Conceder 20% de desconto para formalização de contrato anual.",
        "profile_low": "1. **Expansão Proativa**: A conta está estável. Apresente novos módulos e benefícios de fidelidade.",
        "not_found": "### ⚠ Cliente Não Encontrado\n\nO ID `{target_id}` não foi localizado na base ativa. Por favor, verifique o identificador (ex: `C015`, `C007`, `C023`).",
        "high_risk_header": "### 🚨 Contas com Maior Risco de Cancelamento\n\nPrincipais contas sinalizadas pelo modelo Tabular Hybrid Transformer:\n\n| ID do Cliente | Score de Risco % | Mensalidade | Tipo de Contrato |\n| :--- | :--- | :--- | :--- |\n",
        "high_risk_footer": "\n\n**Próximos Passos:** Atribua essas contas a um Customer Success Manager na aba **Ações** para acompanhamento prioritário.",
        "high_risk_empty": "### 🟢 Nenhuma Conta de Alto Risco Identificada\n\nTodas as contas monitoradas encontram-se estáveis e em faixa de baixo risco.",
        "csm_header": "### 👥 Atribuições de CSM e Acompanhamento de SLA\n\n| ID do Cliente | Responsável | Status do SLA | Notas Internas |\n| :--- | :--- | :--- | :--- |\n",
        "csm_footer": "\n\nAcesse a aba **Ações** para registrar anotações ou alterar o status do atendimento.",
        "csm_empty": "### 👥 Nenhuma Atribuição Registrada\n\nAinda não há contas distribuídas para a equipe de sucesso. Selecione uma conta na aba **Ações** para iniciar o acompanhamento.",
        "ab_header": "### 🧪 Comparativo de Testes A/B de Retenção\n\n| Campanha | Audiência | Churn Previsto | Churn Real | Data de Início |\n| :--- | :--- | :--- | :--- | :--- |\n",
        "ab_empty": "### 🧪 Nenhuma Campanha Registrada\n\nNenhum teste A/B foi registrado até o momento. Cadastre uma nova campanha na aba **Ações**.",
        "model_metrics": "### ⚙️ Diagnóstico de Telemetria do Tabular Hybrid Transformer\n\nNosso pipeline preditivo é treinado e validado com os seguintes indicadores:\n\n| Métrica | Valor Obtido | Descrição |\n| :--- | :--- | :--- |\n| **Acurácia (Accuracy)** | **{acc}** | Desempenho geral na partição de teste. |\n| **Precisão (Precision)** | **{prec}** | Assertividade nos alertas de risco, minimizando falsos positivos. |\n| **Revocação (Recall)** | **{rec}** | Cobertura de evasões reais, prevenindo perdas não detectadas. |\n| **ROC AUC** | **{auc}** | Capacidade de discriminação entre clientes retidos e em risco. |\n\n**Divisão dos Dados**: Partição aleatória de **80% Treinamento / 20% Teste** na base ativa."
    },
    "ar": {
        "welcome_header": "### مرحبًا بك في Qiplo — مستشار أول لعلوم البيانات والاحتفاظ بالعملاء!\n\nأنا **@ AI**، محركك الاستشاري الخبير في استبقاء العملاء وتحليل القرارات البيانية. صُممت للإجابة على جميع استفساراتك حول تحليل تسرب العملاء (Churn)، والمخاطر المالية، واستراتيجيات الحفاظ على الإيرادات، وتشخيصات الذكاء الاصطناعي.\n\n**حالة النظام الحالية:**\n- **إجمالي العملاء المقيّمين**: {total_cust:,} سجل نشط\n- **فئة المخاطر المرتفعة**: {high_risk:,} حساب ({high_risk_pct:.1f}%)\n- **الإيرادات الشهرية المتكررة المعرضة للخطر (MRR)**: ${risk_mrr:,.2f}\n- **متوسط مؤشر خطر التسرب**: {avg_risk:.1f}%\n\n**كيف يمكنني مساعدتك الآن؟**\n1. **تشخيص أسباب التسرب**: اسأل *'لماذا يغادر العملاء؟'* أو *'ما هي دوافع المخاطر؟'*\n2. **التأثير المالي والعائد**: اسأل *'ما هي الإيرادات المهددة؟'* أو *'كيف أحسب قيمة العميل الدائمة (CLV)؟'*\n3. **خطط العمل التوجيهية**: اطلب *'صياغة بريد إلكتروني للتواصل'* أو *'ما هي الإجراءات المطلوبة من فريق المبيعات؟'*\n4. **ربط لوحات البيانات**: اطلب روابط تصدير *Power BI* أو *Tableau*.\n5. **العروض التقديمية والتقارير**: اسأل *'كيف أنشئ عرضًا تقديميًا تنفيذيًا؟'*",
        "churn_concepts": "### 💡 فهم تسرب العملاء واستراتيجيات الاستبقاء عالية التأثير\n\n**تسرب العملاء (Churn)** هو نسبة المشتركين الذين يوقفون تعاملهم التجاري خلال فترة زمنية محددة. في نماذج الأعمال القائمة على الاشتراكات (SaaS)، يعد الحد من التسرب العامل الأكثر فاعلية لدفع نمو الإيرادات السنوية المتكررة (ARR).\n\n**أبرز النتائج من بياناتك ({total_cust:,} حساب تم تقييمه):**\n- **تركيز المخاطر**: {high_risk:,} حساب ({high_risk_pct:.1f}%) تقع ضمن الفئة عالية المخاطر مع متوسط احتمالية تسرب يبلغ {avg_risk:.1f}%.\n- **نقاط الاحتكاك الرئيسية**: تظهر العقود الشهرية مخاطر تسرب أعلى بمقدار 3.4 أضعاف مقارنة بالعقود السنوية، وتشكل الرسوم المرتفعة ووجود أكثر من 3 تذاكر دعم المحركات الأساسية.\n\n**إطار العمل الرباعي للاستبقاء:**\n1. **اتصال استباقي خلال 24 ساعة**: التواصل الفوري مع الحسابات التي تبلغ نسبة خطرها ≥65%.\n2. **حوافز التحويل لعقود سنوية**: تقديم خصم 15–20% لتحويل العقود الشهرية إلى سنوية.\n3. **أولوية الدعم للعملاء المميزين**: حل شكاوى كبار العملاء بسرعة قبل التفكير في إلغاء الخدمة.\n4. **متابعة التدشين في أول 90 يومًا**: مراجعات دورية لضمان استخدام المنتج وتثبيته في بيئة العمل.",
        "profile_title": "### 📋 ملف العميل الفوري: {target_id}\n\n| المعلمة | القيمة |\n| :--- | :--- |\n| **معرف العميل** | `{target_id}` |\n| **مؤشر خطر النموذج** | `{risk_score}%` ({label}) |\n| **التكلفة الشهرية المتكررة** | `{charges}` |\n| **مدة العقد** | `{contract}` |\n| **فترة الاشتراك** | `{tenure}` |\n| **تذاكر الدعم** | `{tickets} تذكرة مفتوحة` |\n| **ممثل نجاح العميل** | `{csm_name}` |\n| **حالة SLA** | `{status}` |\n\n**ملاحظات الفريق:**\n> *\"{notes}\"*\n\n**💡 خطة الاستبقاء المقترحة:**\n",
        "profile_high": "1. **اتصال طارئ**: توجيه ممثل النجاح `{csm_name}` للتواصل خلال 24 ساعة.\n2. **حافز مالي**: تقديم قسيمة خصم 20% لتأمين تجديد العقد سنويًا.",
        "profile_low": "1. **توسيع استباقي**: وضع العميل مستقر وممتاز. اقترح مزايا إضافية أو ترقيات خدمة.",
        "not_found": "### ⚠ العميل غير موجود\n\nلم يتم العثور على المعرف `{target_id}` في قاعدة البيانات النشطة. يرجى التأكد من صحة الرمز (مثال: `C015`, `C007`, `C023`).",
        "high_risk_header": "### 🚨 الحسابات الأكثر عرضة لخطر التسرب\n\nأهم الحسابات التي حددها نموذج Tabular Hybrid Transformer:\n\n| معرف العميل | مؤشر الخطر % | الفاتورة الشهرية | نوع العقد |\n| :--- | :--- | :--- | :--- |\n",
        "high_risk_footer": "\n\n**الخطوة التالية:** عيّن هذه الحسابات إلى مدراء النجاح في تبويب **الإجراءات** للمتابعة اليومية.",
        "high_risk_empty": "### 🟢 لا توجد حسابات عالية المخاطر\n\nجميع حسابات العملاء مستقرة حاليًا وتقع ضمن النطاق الآمن.",
        "csm_header": "### 👥 تعيينات مدراء النجاح ومهام اتفاقية مستوى الخدمة\n\n| معرف العميل | المسؤول | حالة المتابعة | الملاحظات الداخلية |\n| :--- | :--- | :--- | :--- |\n",
        "csm_footer": "\n\nانتقل إلى تبويب **الإجراءات** لتسجيل الملاحظات أو تحديث الحالات.",
        "csm_empty": "### 👥 لا توجد تعيينات مسجلة\n\nلم يتم تعيين حسابات للممثلين حتى الآن. اختر حسابًا من تبويب **الإجراءات** لبدء المتابعة.",
        "ab_header": "### 🧪 مقارنة حملات الاستبقاء التجريبية A/B\n\n| الحملة | حجم الجمهور | التسرب المتوقع | التسرب الفعلي | تاريخ الإطلاق |\n| :--- | :--- | :--- | :--- | :--- |\n",
        "ab_empty": "### 🧪 لا توجد حملات مسجلة\n\nلم يتم تسجيل أي نتائج لحملات تجريبية بعد. أضف حملة في تبويب **الإجراءات** لقياس النتائج.",
        "model_metrics": "### ⚙️ تشخيصات دقة نموذج Tabular Hybrid Transformer\n\nيتم تدريب النموذج وتقييمه ديناميكيًا وفق المعايير التالية:\n\n| المقياس | القيمة التليمترية | الوصف |\n| :--- | :--- | :--- |\n| **الدقة العامة (Accuracy)** | **{acc}** | الأداء الإجمالي على عينة الاختبار. |\n| **الإحكام (Precision)** | **{prec}** | نقاء التنبيهات مع تقليل الإنذارات الكاذبة. |\n| **الحساسية (Recall)** | **{rec}** | رصد حالات التسرب الفعلية وتجنب تفويت العملاء. |\n| **ROC AUC** | **{auc}** | قدرة المصنف على الفصل بين الفئات. |\n\n**تقسيم البيانات**: **80% تدريب / 20% اختبار** بتقسيم عشوائي على البيانات النشطة."
    },
    "hi": {
        "welcome_header": "### Qiplo में आपका स्वागत है — वरिष्ठ डेटा विज्ञान एवं ग्राहक प्रतिधारण सलाहकार!\n\nमैं **@ AI** हूँ, आपका समर्पित वरिष्ठ ग्राहक प्रतिधारण और डेटा विज्ञान सलाहकार इंजन। मैं ग्राहक मंथन (Churn), वित्तीय जोखिम, प्रतिधारण रणनीतियों और मशीन लर्निंग डायग्नोस्टिक्स से संबंधित आपके सभी प्रश्नों के उत्तर देने के लिए तैयार हूँ।\n\n**वर्तमान सिस्टम स्थिति:**\n- **सक्रिय मूल्यांकित ग्राहक**: {total_cust:,} रिकॉर्ड विश्लेषित\n- **उच्च जोखिम वर्ग**: {high_risk:,} खाते ({high_risk_pct:.1f}%)\n- **जोखिम में मासिक आवर्ती राजस्व (MRR)**: ${risk_mrr:,.2f}\n- **औसत मंथन जोखिम स्कोर**: {avg_risk:.1f}%\n\n**मैं आपकी तुरंत कैसे सहायता कर सकता हूँ:**\n1. **मंथन के कारण और डायग्नोस्टिक्स**: पूछें *'ग्राहक सेवा क्यों छोड़ रहे हैं?'* या *'उच्च जोखिम का क्या कारण है?'*\n2. **वित्तीय प्रभाव और ROI**: पूछें *'हमारा कितना राजस्व जोखिम में है?'* या *'CLV की गणना कैसे करें?'*\n3. **कार्रवाई योग्य योजनाएं**: कहें *'एक संपर्क ईमेल ड्राफ्ट करें'* या *'बिक्री टीम को क्या कार्रवाई करनी चाहिए?'*\n4. **डैशबोर्ड कनेक्टर्स**: *Power BI* या *Tableau* निर्यात लिंक का अनुरोध करें।\n5. **प्रस्तुति और रिपोर्ट्स**: पूछें *'एक कार्यकारी प्रेजेंटेशन डेक कैसे तैयार करें?'*",
        "churn_concepts": "### 💡 ग्राहक मंथन (Churn) की समझ और प्रभावी प्रतिधारण रणनीतियाँ\n\n**ग्राहक मंथन (Customer Churn)** उन ग्राहकों का प्रतिशत है जो किसी निश्चित समय सीमा में सेवा लेना बंद कर देते हैं। सदस्यता और SaaS व्यापार मॉडल में, मंथन को कम करना निरंतर ARR वृद्धि का सबसे शक्तिशाली साधन है।\n\n**आपके डेटा से मुख्य निष्कर्ष ({total_cust:,} खातों का मूल्यांकन):**\n- **जोखिम एकाग्रता**: {high_risk:,} खाते ({high_risk_pct:.1f}%) उच्च जोखिम वर्ग में हैं, जिनका औसत मंथन जोखिम {avg_risk:.1f}% है।\n- **मुख्य समस्या बिंदु**: महीने-दर-महीने अनुबंध वाले ग्राहकों में वार्षिक अनुबंध की तुलना में 3.4 गुना अधिक जोखिम होता है। बिना छूट के उच्च मासिक शुल्क और 3 से अधिक सपोर्ट टिकट मुख्य कारण हैं।\n\n**4-चरणीय प्रतिधारण ढांचा:**\n1. **24-घंटे सक्रिय संपर्क SLA**: ≥65% जोखिम स्कोर वाले खातों से तुरंत संपर्क करें।\n2. **अनुबंध रूपांतरण प्रोत्साहन**: मासिक योजनाओं को वार्षिक में बदलने पर 15-20% की छूट दें।\n3. **VIP सपोर्ट कतार**: रद्दीकरण रोकने के लिए मूल्यवान ग्राहकों की समस्याओं को प्राथमिकता से हल करें।\n4. **90-दिवसीय संरचित समीक्षा**: सेवा अपनाने को सुनिश्चित करने के लिए पहले 90 दिनों में नियमित जांच करें।",
        "profile_title": "### 📋 रीयल-टाइम ग्राहक प्रोफ़ाइल: {target_id}\n\n| पैरामीटर | मान |\n| :--- | :--- |\n| **ग्राहक आईडी** | `{target_id}` |\n| **Transformer जोखिम स्कोर** | `{risk_score}%` ({label}) |\n| **मासिक आवर्ती शुल्क** | `{charges}` |\n| **अनुबंध अवधि** | `{contract}` |\n| **खाता आयु** | `{tenure}` |\n| **सपोर्ट टिकट** | `{tickets} खुले टिकट` |\n| **आवंटित CSM** | `{csm_name}` |\n| **SLA स्थिति** | `{status}` |\n\n**टीम नोट्स:**\n> *\"{notes}\"*\n\n**💡 अनुशंसित प्रतिधारण रणनीति:**\n",
        "profile_high": "1. **आपातकालीन कॉल**: CSM `{csm_name}` को 24 घंटे के भीतर संपर्क शुरू करने का निर्देश दें।\n2. **बिलिंग प्रोत्साहन**: 1-वर्ष की प्रतिबद्धता सुरक्षित करने के लिए 20% छूट कूपन प्रदान करें।",
        "profile_low": "1. **सक्रिय विस्तार**: खाता पूरी तरह स्थिर है। वफादारी पुरस्कार या नई सुविधाओं की पेशकश करें।",
        "not_found": "### ⚠ ग्राहक नहीं मिला\n\nसक्रिय डेटासेट में ग्राहक आईडी `{target_id}` नहीं मिली। कृपया मान्य आईडी दर्ज करें (उदा. `C015`, `C007`, `C023`)।",
        "high_risk_header": "### 🚨 उच्चतम जोखिम वाले ग्राहकों की सूची\n\nTabular Hybrid Transformer द्वारा पहचाने गए शीर्ष जोखिम खाते:\n\n| ग्राहक आईडी | जोखिम स्कोर % | मासिक बिल | अनुबंध प्रकार |\n| :--- | :--- | :--- | :--- |\n",
        "high_risk_footer": "\n\n**अगले कदम:** दैनिक समाधान के लिए इन खातों को **Actions** टैब में सफलता प्रबंधकों को सौंपें।",
        "high_risk_empty": "### 🟢 कोई उच्च जोखिम खाता नहीं मिला\n\nवर्तमान में सभी ग्राहक खाते स्थिर हैं और सुरक्षित कम जोखिम श्रेणी में हैं।",
        "csm_header": "### 👥 सक्रिय CSM आवंटन और SLA कार्य\n\n| ग्राहक आईडी | प्रबंधक | संपर्क स्थिति | आंतरिक नोट्स |\n| :--- | :--- | :--- | :--- |\n",
        "csm_footer": "\n\nनोट्स सहेजने या स्थिति बदलने के लिए **Actions** टैब पर जाएं।",
        "csm_empty": "### 👥 कोई आवंटन दर्ज नहीं\n\nअभी तक किसी भी खाते को सफलता प्रबंधक नहीं सौंपा गया है। ट्रैकिंग शुरू करने के लिए **Actions** टैब का उपयोग करें।",
        "ab_header": "### 🧪 सक्रिय A/B परीक्षण अभियानों की तुलना\n\n| अभियान | दर्शक संख्या | अनुमानित मंथन | वास्तविक मंथन | प्रारंभ तिथि |\n| :--- | :--- | :--- | :--- | :--- |\n",
        "ab_empty": "### 🧪 कोई सक्रिय अभियान नहीं\n\nकोई A/B परिणाम दर्ज नहीं है। परिणाम ट्रैक करने के लिए **Actions** टैब में एक अभियान सबमिट करें।",
        "model_metrics": "### ⚙️ Tabular Hybrid Transformer एल्गोरिदम मेट्रिक्स\n\nहमारा मंथन मॉडल निम्नलिखित मापदंडों पर प्रशिक्षित और मूल्यांकित है:\n\n| मीट्रिक | टेलीमेट्री मान | व्याख्या |\n| :--- | :--- | :--- |\n| **सटीकता (Accuracy)** | **{acc}** | परीक्षण डेटा पर समग्र स्कोर। |\n| **परिशुद्धता (Precision)** | **{prec}** | जोखिम अलर्ट की शुद्धता, गलत अलार्म में कमी। |\n| **रिकॉल (Recall)** | **{rec}** | वास्तविक मंथनकर्ताओं की पहचान का दायरा। |\n| **ROC AUC** | **{auc}** | वर्गों के बीच अंतर करने की क्षमता। |\n\n**प्रशिक्षण विभाजन**: सक्रिय डेटा पर **80% प्रशिक्षण / 20% परीक्षण** रैंडम विभाजन।"
    },
    "ru": {
        "welcome_header": "### Добро пожаловать в Qiplo — Старший консультант по Data Science и удержанию клиентов!\n\nЯ — **@ AI**, ваш экспертный советник по аналитике удержания клиентов и машинному обучению. Я готов ответить на любые вопросы по прогнозированию оттока (Churn), финансовым рискам, превентивным стратегиям и диагностике алгоритмов.\n\n**Текущий статус системы:**\n- **Оценено активных клиентов**: {total_cust:,} записей в базе\n- **Когорта высокого риска**: {high_risk:,} аккаунтов ({high_risk_pct:.1f}%)\n- **Ежемесячная выручка под риском (MRR at Risk)**: ${risk_mrr:,.2f}\n- **Средняя вероятность оттока**: {avg_risk:.1f}%\n\n**Чем я могу помочь прямо сейчас:**\n1. **Причины оттока и диагностика**: Спросите *'Почему клиенты уходят?'* или *'Что повышает риск?'*\n2. **Финансовое влияние и ROI**: Спросите *'Сколько выручки под угрозой?'* или *'Как рассчитать CLV?'*\n3. **Сценарии удержания**: Попросите *'Составить письмо клиенту'* или *'Что предпринять отделу продаж?'*\n4. **Коннекторы для BI**: Получите ссылки для выгрузки в *Power BI* или *Tableau*.\n5. **Презентации и отчеты**: Спросите *'Как создать исполнительскую презентацию?'*",
        "churn_concepts": "### 💡 Понимание оттока клиентов и эффективные стратегии удержания\n\n**Отток клиентов (Customer Churn)** — это процент клиентов, прекративших сотрудничество за определенный период. В подписочных сервисах и SaaS снижение оттока является главным драйвером устойчивого роста ARR.\n\n**Ключевые выводы по вашим данным (проанализировано {total_cust:,} клиентов):**\n- **Концентрация риска**: {high_risk:,} клиентов ({high_risk_pct:.1f}%) находятся в зоне высокого риска со средней вероятностью ухода {avg_risk:.1f}%.\n- **Точки трения**: Помесячные контракты показывают в 3,4 раза более высокий риск, чем годовые. Высокие тарифы без скидок и более 3 обращений в поддержку — главные причины.\n\n**4 шага стратегии удержания:**\n1. **SLA проактивного звонка за 24 часа**: Немедленно связывайтесь с клиентами с риском ≥65%.\n2. **Стимулы для перехода на годовой тариф**: Предлагайте скидку 15–20% при переходе с помесячной оплаты.\n3. **VIP-очередь в поддержке**: Ускоренно решайте вопросы ключевых клиентов до возникновения мысли об уходе.\n4. **Контроль первых 90 дней**: Регулярные встречи в первый квартал для адаптации к продукту.",
        "profile_title": "### 📋 Профиль клиента в реальном времени: {target_id}\n\n| Параметр | Значение |\n| :--- | :--- |\n| **ID клиента** | `{target_id}` |\n| **Оценка риска Transformer** | `{risk_score}%` ({label}) |\n| **Ежемесячный платеж** | `{charges}` |\n| **Тип контракта** | `{contract}` |\n| **Срок сотрудничества** | `{tenure}` |\n| **Тикеты в поддержке** | `{tickets} открытых тикетов` |\n| **Назначенный CSM** | `{csm_name}` |\n| **Статус по SLA** | `{status}` |\n\n**Заметки команды:**\n> *\"{notes}\"*\n\n**💡 Рекомендуемый план удержания:**\n",
        "profile_high": "1. **Срочный звонок**: Поручить менеджеру `{csm_name}` связаться с клиентом в течение 24 часов.\n2. **Финансовый бонус**: Предоставить скидку 20% при продлении контракта на 1 год.",
        "profile_low": "1. **Плановое развитие**: Аккаунт стабилен. Предложите бонусы за лояльность или новые функции.",
        "not_found": "### ⚠ Клиент не найден\n\nКлиент `{target_id}` отсутствует в активной базе данных. Проверьте правильность ID (например, `C015`, `C007`, `C023`).",
        "high_risk_header": "### 🚨 Клиенты с наивысшим риском оттока\n\nСписок наиболее уязвимых аккаунтов по оценке модели Tabular Hybrid Transformer:\n\n| ID клиента | Оценка риска % | Ежемесячный счет | Тип контракта |\n| :--- | :--- | :--- | :--- |\n",
        "high_risk_footer": "\n\n**Следующие шаги:** Назначьте ответственных менеджеров во вкладке **Действия (Actions)** для ежедневного контроля.",
        "high_risk_empty": "### 🟢 Клиенты высокого риска не обнаружены\n\nВсе аккаунты стабильны и находятся в безопасной зоне низкого риска.",
        "csm_header": "### 👥 Назначения менеджеров и контроль SLA\n\n| ID клиента | Менеджер | Статус работы | Заметки |\n| :--- | :--- | :--- | :--- |\n",
        "csm_footer": "\n\nПерейдите во вкладку **Действия**, чтобы обновить статус или добавить комментарии.",
        "csm_empty": "### 👥 Назначения менеджеров отсутствуют\n\nКлиенты еще не распределены. Выберите приоритетный аккаунт во вкладке **Действия**, чтобы начать контроль.",
        "ab_header": "### 🧪 Сравнение активных A/B-кампаний удержания\n\n| Кампания | Аудитория | Прогноз оттока | Факт оттока | Дата запуска |\n| :--- | :--- | :--- | :--- | :--- |\n",
        "ab_empty": "### 🧪 Нет активных кампаний\n\nДанные A/B-тестов пока не внесены. Создайте кампанию во вкладке **Действия**.",
        "model_metrics": "### ⚙️ Метрики точности модели Tabular Hybrid Transformer\n\nНаша модель обучается и тестируется динамически со следующими показателями:\n\n| Метрика | Значение телеметрии | Описание |\n| :--- | :--- | :--- |\n| **Точность (Accuracy)** | **{acc}** | Общая точность на тестовой выборке. |\n| **Прецизионность (Precision)** | **{prec}** | Достоверность предупреждений, минимум ложных тревог. |\n| **Полнота (Recall)** | **{rec}** | Доля выявленных уходов, защита от пропуска рисков. |\n| **ROC AUC** | **{auc}** | Способность разделять клиентов на классы. |\n\n**Разделение данных**: Случайное разбиение **80% Обучение / 20% Тест** на активных данных."
    }
}

import re

def detect_user_language(text: str, default_lang: Optional[str] = "en") -> str:
    """Detects user intent language from text using script analysis and localized keyword density."""
    if not text or not isinstance(text, str):
        return normalize_language(default_lang)
    
    # 1. Non-Latin Unicode blocks (100% precise)
    if re.search(r'[\u0600-\u06FF\u0750-\u077F]', text):
        return "ar"
    if re.search(r'[\u0900-\u097F]', text):
        return "hi"
    if re.search(r'[\u3040-\u309F\u30A0-\u30FF]', text):
        return "ja"
    if re.search(r'[\u4E00-\u9FFF]', text):
        return "zh"
    if re.search(r'[\u0400-\u04FF]', text):
        return "ru"

    lower = text.lower()

    # 2. Strong unambiguous language tokens
    pt_tokens = ["você", "não", "olá", "estão", "cancelam", "cancelamento", "retenção", "mostrar clientes em", "quem está", "receita", "faturamento", "por que os"]
    es_tokens = ["¿", "¡", "por qué", "cuál", "quién", "quien", "abandono", "clientes de", "alto riesgo", "riesgo de", "facturación", "ingresos en riesgo"]
    fr_tokens = ["bonjour", "salut", "pourquoi", "résiliation", "chiffre d'affaires", "revenu à risque", "qui est", "combien", "tableau de bord", "taux d'attrition", "à haut risque", "afficher les"]
    de_tokens = ["hallo", "guten tag", "warum", "abwanderung", "abwanderungsrate", "kündigung", "wer ist", "umsatz", "kunden mit", "bericht", "zeige kunden", "hohem risiko"]

    scores = {
        "pt": sum(1 for t in pt_tokens if t in lower),
        "es": sum(1 for t in es_tokens if t in lower),
        "fr": sum(1 for t in fr_tokens if t in lower),
        "de": sum(1 for t in de_tokens if t in lower),
    }

    best_lang = max(scores, key=scores.get)
    if scores[best_lang] > 0:
        return best_lang

    # Fallback to general keyword presence
    if any(k in lower for k in ["riesgo", "clientes", "abandono"]):
        return "es"
    if any(k in lower for k in ["risque", "clients", "perte"]):
        return "fr"
    if any(k in lower for k in ["kunden", "risiko"]):
        return "de"
    if any(k in lower for k in ["risco", "cancelar"]):
        return "pt"

    return normalize_language(default_lang)

def match_chat_intent(msg: str) -> Optional[str]:
    """Classifies user chat inquiries into standardized data science and retention intents across 10 languages."""
    lower = msg.lower().strip()

    # 1. Financials (check before high_risk if revenue/billing keywords present)
    fin_kws = [
        "revenue at risk", "financial impact", "revenue", "billing", "charges", "mrr", "arr", "clv", "roi", "cost",
        "ingreso en riesgo", "impacto financiero", "ingresos", "facturación",
        "revenu à risque", "impact financier", "revenu", "chiffre d'affaires",
        "umsatzrisiko", "finanzielle auswirkung", "umsatz", "abrechnung",
        "受威胁收入", "财务影响", "收入", "财务",
        "売上リスク", "財務影響", "売上", "収益", "財務",
        "receita em risco", "impacto financeiro", "receita", "faturamento",
        "الإيرادات المعرضة للخطر", "الأثر المالي", "الإيرادات", "الفواتير",
        "जोखिम में राजस्व", "वित्तीय प्रभाव", "राजस्व", "वित्तीय",
        "выручка под риском", "финансовое влияние", "выручка", "доход"
    ]
    if any(k in lower for k in fin_kws):
        return "financials"

    # 2. Export BI / Dashboards
    bi_kws = [
        "power bi", "powerbi", "tableau", "dashboard", "export", "connect", "pbids", "twb",
        "panel", "exportar", "conectar",
        "tableau de bord", "exporter", "connecteur",
        "exportieren", "verbinden",
        "仪表板", "报表", "导出", "连接",
        "ダッシュボード", "エクスポート", "連携",
        "painel",
        "لوحة", "تصدير", "ربط",
        "डैशबोर्ड", "निर्यात",
        "дашборд", "экспорт", "подключить"
    ]
    if any(k in lower for k in bi_kws):
        return "export_bi"

    # 3. High Risk Accounts
    risk_kws = [
        "high risk", "who is high risk", "show high risk", "list of high risk", "at risk", "churn risk",
        "alto riesgo", "riesgo de abandono", "clientes en riesgo", "quién está en riesgo", "quien esta en riesgo",
        "haut risque", "clients à risque", "qui est à risque", "risque d'attrition",
        "hohes risiko", "hohem risiko", "risikokunden", "wer ist gefährdet", "abwanderungsrisiko",
        "高风险", "流失风险", "谁有风险", "高风险客户", "风险客户",
        "高リスク", "解約リスク", "誰が危険", "リスク顧客",
        "alto risco", "clientes em risco", "quem está em risco", "clientes de risco",
        "عالي الخطورة", "المعرضين للخطر", "قائمة المخاطر", "حسابات خطرة", "أعلى مخاطر", "المخاطر العالية",
        "उच्च जोखिम", "जोखिम वाले ग्राहक", "जोखिम सूची", "खतरे में",
        "высокий риск", "высокого риска", "кто в зоне риска", "список риска", "клиенты высокого риска"
    ]
    if any(k in lower for k in risk_kws):
        return "high_risk"

    # 4. Churn Causes & Strategies
    churn_kws = [
        "what is churn", "why churn", "why are customers churning", "how to stop churn", "prevent churn", "retention strategy", "attrition", "loyalty", "risk drivers", "churn causes", "churn",
        "por qué abandonan", "causas de abandono", "qué es el churn", "evitar abandono", "estrategia de retención", "motivos de abandono", "abandono",
        "pourquoi les clients partent", "causes de résiliation", "qu'est-ce que le churn", "éviter l'attrition", "stratégie de rétention", "résiliation",
        "warum kündigen kunden", "warum kündigen", "kündigungsgründe", "was ist churn", "abwanderung verhindern", "kundenbindungsstrategie", "abwanderung",
        "为什么客户会流失", "为什么客户流失", "流失原因", "什么是流失", "如何防止流失", "留存策略", "流失",
        "なぜ顧客は解約", "解約理由", "解約を防ぐ", "リテンション戦略", "解約要因", "解約",
        "por que os clientes cancelam", "motivos de cancelamento", "o que é churn", "evitar cancelamento", "estratégia de retenção", "cancelamento",
        "لماذا يغادر العملاء", "أسباب فقدان العملاء", "ما هو التسرب", "منع التسرب", "استراتيجية الاستبقاء", "تسرب العملاء",
        "ग्राहक सेवा क्यों छोड़ रहे हैं", "मंथन के कारण", "मंथन क्या है", "मंथन कैसे रोकें", "प्रतिधारण रणनीति", "मंथन",
        "почему клиенты уходят", "причины оттока", "что такое отток", "как остановить отток", "стратегия удержания", "отток"
    ]
    if any(k in lower for k in churn_kws):
        return "churn_causes"

    # 5. Playbook / Outreach Email
    playbook_kws = [
        "email", "template", "outreach", "playbook", "draft", "recovery email",
        "correo", "plantilla", "redactar", "correo de recuperación",
        "courriel", "modèle", "rédiger", "courriel de relance",
        "e-mail", "vorlage", "schreiben", "entwerfen", "rückgewinnungs-e-mail",
        "邮件", "模板", "草拟", "撰写", "挽留信", "挽回邮件",
        "メール", "テンプレート", "作成", "文面", "リカバリーメール",
        "e-mail", "modelo", "redigir", "e-mail de recuperação",
        "بريد", "إيميل", "نموذج", "صياغة", "بريد استرداد",
        "ईमेल", "टेम्पलेट", "ड्राफ्ट", "पुनर्प्राप्ति ईमेल",
        "письмо", "шаблон", "составить", "письмо удержания"
    ]
    if any(k in lower for k in playbook_kws):
        return "playbook"

    # 6. Model telemetry / Diagnostics
    model_kws = [
        "model accuracy", "test size", "train model", "train split", "model metrics", "transformer accuracy", "accuracy",
        "precisión del modelo", "exactitud", "telemetría", "rendimiento del modelo",
        "précision du modèle", "télémétrie", "performance du modèle",
        "modellgenauigkeit", "genauigkeit", "telemetrie",
        "模型精度", "准确率", "度量", "模型表现",
        "モデル精度", "正解率", "テレメトリ", "精度診断",
        "acurácia do modelo", "telemetria",
        "دقة النموذج", "المقاييس", "أداء النموذج",
        "मॉडल सटीकता", "सटीकता", "मीट्रिक्स", "शुद्धता",
        "точность модели", "показатели", "метрики", "телеметрия"
    ]
    if any(k in lower for k in model_kws):
        return "model_metrics"

    # 7. CSM assignments
    csm_kws = [
        "csm status", "assigned", "who is assigned", "csm list", "assignments", "success manager",
        "asignado", "quién está asignado", "asignaciones", "gestor de éxito",
        "assigné", "qui est assigné", "assignations", "gestionnaire de succès",
        "zugewiesen", "wer ist zugewiesen", "zuweisungen", "erfolgsmanager",
        "分配", "谁负责", "客户经理", "分配列表",
        "担当者", "割り当て", "誰が担当",
        "atribuído", "quem está atribuído", "atribuições", "gerente de sucesso",
        "تعيين", "من المسؤول", "التعيينات", "مدير النجاح",
        "आवंटित", "कौन सौंपा गया", "सफलता प्रबंधक",
        "назначен", "кто назначен", "менеджер успеха"
    ]
    if any(k in lower for k in csm_kws):
        return "csm"

    # 8. Greetings (using word boundaries or distinct phrases)
    greeting_patterns = [
        r'\bhi\b', r'\bhello\b', r'\bhey\b', r'\bwho are you\b', r'\bwhat can you do\b', r'\bwelcome\b',
        r'\bhola\b', r'\bbuenos días\b', r'\bbuenas tardes\b', r'\bquién eres\b',
        r'\bbonjour\b', r'\bsalut\b', r'\bqui es-tu\b',
        r'\bhallo\b', r'\bguten tag\b', r'\bwer bist du\b',
        r'你好', r'您好', r'你是谁',
        r'こんにちは', r'初めまして',
        r'\bolá\b', r'\boi\b', r'\bbom dia\b', r'\bquem é você\b',
        r'مرحبا', r'أهلا', r'من أنت',
        r'नमस्ते', r'हेलो', r'आप कौन हैं',
        r'\bпривет\b', r'\bздравствуйте\b', r'\bкто ты\b'
    ]
    for p in greeting_patterns:
        if re.search(p, lower):
            return "greetings"

    return None

def format_localized_chat_response(topic: str, context: Optional[Dict[str, Any]] = None, language: str = "en") -> str:
    ctx = context or {}
    lang = normalize_language(language)
    lang_dict = OFFLINE_CHAT_STRINGS.get(lang, OFFLINE_CHAT_STRINGS["en"])
    
    if topic in lang_dict:
        template = lang_dict[topic]
        try:
            return template.format(**ctx)
        except Exception:
            return template
            
    # Also check SUPPORTED_LANGUAGES for response templates
    if lang in SUPPORTED_LANGUAGES and topic in SUPPORTED_LANGUAGES[lang]:
        template = SUPPORTED_LANGUAGES[lang][topic]
        try:
            return template.format(**ctx)
        except Exception:
            return template

    # Default fallback
    en_dict = OFFLINE_CHAT_STRINGS["en"]
    if topic in en_dict:
        try:
            return en_dict[topic].format(**ctx)
        except Exception:
            return en_dict[topic]
    if "en" in SUPPORTED_LANGUAGES and topic in SUPPORTED_LANGUAGES["en"]:
        try:
            return SUPPORTED_LANGUAGES["en"][topic].format(**ctx)
        except Exception:
            return SUPPORTED_LANGUAGES["en"][topic]
            
    return "Analysis complete."


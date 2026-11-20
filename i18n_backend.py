"""
Qiplo Backend Internationalization (i18n) Engine
Provides multilingual data processing, prompt guidance for Gemini / Ollama,
localized sandbox simulations, offline factual AI solver responses,
and localized presentation slide generators across the top 10 global languages:
en, es, fr, de, zh, ja, pt, ar, hi, ru.
"""

from typing import Dict, List, Any, Optional

SUPPORTED_LANGUAGES = {
    "en": {"name": "English", "native": "English", "dir": "ltr"},
    "es": {"name": "Spanish", "native": "Español", "dir": "ltr"},
    "fr": {"name": "French", "native": "Français", "dir": "ltr"},
    "de": {"name": "German", "native": "Deutsch", "dir": "ltr"},
    "zh": {"name": "Chinese", "native": "简体中文", "dir": "ltr"},
    "ja": {"name": "Japanese", "native": "日本語", "dir": "ltr"},
    "pt": {"name": "Portuguese", "native": "Português", "dir": "ltr"},
    "ar": {"name": "Arabic", "native": "العربية", "dir": "rtl"},
    "hi": {"name": "Hindi", "native": "हिन्दी", "dir": "ltr"},
    "ru": {"name": "Russian", "native": "Русский", "dir": "ltr"}
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

def format_localized_chat_response(topic: str, context: Dict[str, Any], language: str = "en") -> str:
    lang = normalize_language(language)
    lang_dict = OFFLINE_CHAT_STRINGS.get(lang, OFFLINE_CHAT_STRINGS["en"])
    
    if topic in lang_dict:
        template = lang_dict[topic]
        try:
            return template.format(**context)
        except Exception:
            return template
            
    # Default fallback
    en_dict = OFFLINE_CHAT_STRINGS["en"]
    if topic in en_dict:
        try:
            return en_dict[topic].format(**context)
        except Exception:
            return en_dict[topic]
            
    return "Analysis complete."


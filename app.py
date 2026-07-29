import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Mapeamento e Bússola de Valores", page_icon="🧭", layout="wide")

# Conexão com a planilha do Google Sheets via Secrets
conn = st.connection("gsheets", type=GSheetsConnection)

SENHA_TERAPEUTA = "314159"  # <--- Mude para a sua senha pessoal

# Lista das Áreas da Vida
AREAS_VIDA = [
    "1. Relações familiares (não contando as relações com o cônjuge, companheiro(a) ou filhos)",
    "2. Casamento / Companheiro(a) / Relacionamento Afetivo",
    "3. Ser pai ou mãe (ou exercer esse papel)",
    "4. Amizades / Relações Sociais",
    "5. Trabalho / Carreira / Atividade Laboral",
    "6. Finanças / Dinheiro / Independência Financeira",
    "7. Educação / Aprendizagem",
    "8. Lazer / Bem Estar / Hobbies",
    "9. Espiritualidade / Sentido da Vida / Religião",
    "10. Vida em Comunidade / Cidadania / Direitos e Deveres",
    "11. Autocuidado (descansar, dormir, exercício físico e alimentação)",
    "12. Gerenciamento do Tempo / Disciplina",
    "13. Amor e intimidade / Sexualidade",
    "14. Coragem / Habilidades para correr riscos",
    "15. Percepção Emocional / Flexibilidade Cognitiva",
    "16. Estética (arte, música, literatura e beleza)"
]

# Lista de Valores
LISTA_VALORES = [
    "1. Aceitação – Estar aberto(a) e aceitar a si mesmo(a), aos outros e à vida",
    "2. Aventura – Ser aventureiro(a); buscar, criar ou explorar experiências novas ou estimulantes",
    "3. Assertividade – Defender respeitosamente meus direitos e solicitar o que desejo",
    "4. Autenticidade – Ser autêntico(a), genuíno(a), real; ser fiel a mim mesmo(a)",
    "5. Beleza – Apreciar, criar, nutrir ou cultivar a beleza em mim, nos outros e no ambiente",
    "6. Cuidado – Ser cuidadoso(a) comigo, com os outros e com o ambiente",
    "7. Desafio – Continuar me desafiando para crescer, aprender e melhorar",
    "8. Compaixão – Agir com bondade diante do sofrimento alheio",
    "9. Conexão – Me envolver plenamente no que estou fazendo e estar presente com os outros",
    "10. Contribuição – Ajudar, apoiar ou fazer diferença positiva para mim ou para os outros",
    "11. Conformidade – Respeitar e obedecer regras e obrigações",
    "12. Cooperação – Ser cooperativo(a) e colaborar com os outros",
    "13. Coragem – Ser corajoso(a) ou persistir diante do medo, ameaça ou dificuldade",
    "14. Criatividade – Ser criativo(a) ou inovador(a)",
    "15. Curiosidade – Ser curioso(a), de mente aberta e interessado(a); explorar e descobrir",
    "16. Incentivo – Encorajar e recompensar comportamentos que valorizo em mim ou nos outros",
    "17. Igualdade – Tratar os outros como iguais a mim",
    "18. Empolgação – Buscar, criar e participar de atividades empolgantes ou estimulantes",
    "19. Justiça – Ser justo(a) comigo ou com os outros",
    "20. Boa forma – Manter ou melhorar minha saúde física e mental",
    "21. Flexibilidade – Adaptar-me facilmente a circunstâncias em mudança",
    "22. Liberdade – Viver livremente; escolher como viver e me comportar ou ajudar os outros a fazerem o mesmo",
    "23. Amizade – Ser amigável e agradável com os outros",
    "24. Perdão – Perdoar a mim mesmo(a) ou aos outros",
    "25. Diversão – Ser divertido(a); criar e participar de atividades prazerosas",
    "26. Generosidade – Ser generoso(a), compartilhar e doar a mim mesmo(a) ou aos outros",
    "27. Gratidão – Ser grato(a) e apreciar aspectos positivos de mim, dos outros e da vida",
    "28. Honestidade – Ser honesto(a), verdadeiro(a) e sincero(a) comigo e com os outros",
    "29. Humor – Ver e apreciar o lado divertido da vida",
    "30. Humildade – Ser humilde ou modesto(a); deixar que minhas conquistas falem por si",
    "31. Diligência – Ser trabalhador(a), dedicado(a) e esforçado(a)",
    "32. Independência – Ser autossuficiente e escolher meu próprio modo de fazer as coisas",
    "33. Intimidade – Abrir-me e compartilhar-me emocional ou fisicamente em relações próximas",
    "34. Justiça (legal/social) – Defender a justiça e a equidade",
    "35. Bondade – Ser gentil, compassivo(a) e cuidadoso(a) comigo ou com os outros",
    "36. Amor – Agir com amor ou afeto comigo ou com os outros",
    "37. Atenção plena – Estar consciente, aberto(a) e curioso(a) sobre minha experiência no momento presente",
    "38. Ordem – Ser organizado(a) e manter a ordem",
    "39. Abertura de mente – Considerar outros pontos de vista e avaliar evidências de forma justa",
    "40. Paciência – Esperar calmamente pelo que quero",
    "41. Persistência – Continuar apesar de problemas ou dificuldades",
    "42. Prazer – Criar e proporcionar prazer a mim ou a outros",
    "43. Poder – Influenciar fortemente ou liderar os outros",
    "44. Reciprocidade – Construir relações com equilíbrio justo de dar e receber",
    "45. Respeito – Tratar a mim ou aos outros com respeito e consideração",
    "46. Responsabilidade – Ser responsável e assumir minhas ações",
    "47. Romance – Ser romântico(a); expressar amor ou afeição intensa",
    "48. Segurança – Proteger e garantir a segurança minha ou de outros",
    "49. Autoconsciência – Estar ciente dos meus próprios pensamentos, sentimentos e ações",
    "50. Autocuidado – Cuidar da minha saúde e bem-estar e atender às minhas necessidades",
    "51. Autodesenvolvimento – Continuar crescendo e aprimorando conhecimento, habilidades, caráter ou experiências de vida",
    "52. Autocontrole – Agir de acordo com meus próprios ideais",
    "53. Espiritualidade – Conectar-me com algo maior do que eu",
    "54. Habilidade – Praticar e melhorar continuamente minhas habilidades e aplicá-las plenamente",
    "55. Apoio – Ser prestativo(a), encorajador(a) e disponível para mim ou para os outros",
    "56. Confiança – Ser confiável, leal, sincero(a) e consistente"
]

def carregar_dados():
    try:
        return conn.read(ttl="0s")
    except Exception:
        return pd.DataFrame()

df_dados = carregar_dados()

st.sidebar.title("Navegação")
modo = st.sidebar.radio("Selecione o modo:", ["Área do Paciente", "Painel do Psicólogo"])

# -------------------------------------------------------------------
# MODO PACIENTE
# -------------------------------------------------------------------
if modo == "Área do Paciente":
    st.title("🧭 Avaliação dos Valores de Vida")
    
    paciente_id = st.text_input("Digite seu Código de Acesso:").strip().lower()

    if paciente_id:
        if df_dados.empty or "Paciente_ID" not in df_dados.columns:
            st.error("❌ Nenhum paciente cadastrado no sistema. Por favor, solicite seu acesso ao psicólogo.")
            st.stop()
            
        registros_paciente = df_dados[df_dados["Paciente_ID"].astype(str).str.lower() == paciente_id]

        if registros_paciente.empty:
            st.error("❌ Acesso não encontrado. Certifique-se de que digitou seu código exatamente como enviado pelo psicólogo.")
            st.stop()

        status_atual = registros_paciente["Status"].iloc[0] if "Status" in registros_paciente.columns else "Pendente Etapa 1"

        # --- CASO 1: EXERCÍCIO TOTALMENTE CONCLUÍDO ---
        if status_atual == "Concluido":
            st.info("✅ **Exercício Concluído!** Suas respostas das 3 etapas foram salvas com segurança e serão analisadas em conjunto nas próximas sessões.")
            st.stop()

        # Explicação geral e visão das 3 etapas
            st.markdown("""
            ### 💡 O que são Valores?
            Valores são como **bússolas internas**. Eles representam aquilo que é mais importante para você como ser humano,
            indicando as direções em que deseja caminhar. 
            Diferente de *metas* (que têm um fim), valores são um *modo de viver contínuo*.
    
            ---
            📌 **Este exercício é dividido em 3 etapas:**
            * **Etapa 1:** Serão listadas as áreas da vida valorizadas pela maioria das pessoas.
            Você classificará cada área de acordo com a sua visão pessoal, atribuindo notas de 1 a 10 sob 6 perspectivas diferentes.
            * **Etapa 2:** Você classificará uma lista de valores em grau de importância (*Muito Importante*, *Importante* ou *Não Importante*).
            * **Etapa 3:** Você definirá quais são os seus 3 Valores Principais e 1 Valor Secundário.
    
            *💡 Seu progresso é salvo automaticamente ao final de cada etapa!*
            ---
            """)

        # --- ETAPA 1 DE 3: AVALIAÇÃO DAS ÁREAS DA VIDA ---
        elif status_atual in ["Pendente Etapa 1", "Pendente"]:
            st.header("📌 Etapa 1 de 3: Avaliação das Áreas da Vida")
            st.markdown("""
            Avalie a importância que você dá a cada uma dessas áreas para a sua vida.
            Nem todas as pessoas irão valorizar ou avaliá-las da mesma forma.
            Solicito que pense na importância que você atribui a cada uma delas para a sua vida, independentemente da sua situação atual.
            Por exemplo, atualmente você pode não estar trabalhando ou não ser pai ou mãe, mas valorizar o trabalho ou desejar ser pai ou mãe durante a sua vida.
            
            ---
            **A avaliação de cada área será a partir de 6 aspectos.**
            Avalie cada aspecto em uma escala de 1 a 10.
            * **Possibilidade:** O quanto é possível que alguma coisa *muito significativa* aconteça nessa área da sua vida?
            1 significa que não é possível de forma alguma, e 10 significa que é muito possível. 
            * **Imp. Atual:** O quanto esta área é importante *neste momento* na sua vida?
            1 significa que não é importante de forma alguma, e 10 significa que é muito importante.
            * **Imp. Geral:** O quanto esta área é importante *como um todo*?
            1 significa que não é importante de forma alguma, e 10 significa que é muito importante. 
            * **Ação:** O quanto você atuou a serviço desta área durante a *semana passada*?
            1 significa que você não foi ativo de forma alguma com este valor, e 10 significa que você foi muito ativo. 
            * **Satisfação:** O quanto você está satisfeito com seu nível de ação nesta área durante a *semana passada*?
            1 significa que você não está satisfeito de forma alguma, e 10 significa que você está plenamente satisfeito com seu nível de ação nesta área. 
            * **Preocupação:** O quanto você está preocupado com a possibilidade de esta área não progredir como você deseja?
            1 significa que você não está preocupado de forma alguma, e 10 significa que você está muito preocupado. 
            ---
            """)

            with st.form("form_etapa_1"):
                respostas_areas = []
                for area in AREAS_VIDA:
                    st.subheader(f"📍 {area}")
                    c1, c2, c3 = st.columns(3)
                    with c1:
                        pos = st.slider(f"Possibilidade", 1, 10, 5, key=f"pos_{area}")
                        imp_at = st.slider(f"Imp. Atual", 1, 10, 5, key=f"impat_{area}")
                    with c2:
                        imp_ge = st.slider(f"Imp. Geral", 1, 10, 5, key=f"impge_{area}")
                        act = st.slider(f"Ação (Últ. Semana)", 1, 10, 5, key=f"act_{area}")
                    with c3:
                        sat = st.slider(f"Satisfação c/ Ação", 1, 10, 5, key=f"sat_{area}")
                        pre = st.slider(f"Preocupação", 1, 10, 5, key=f"pre_{area}")
                    
                    respostas_areas.append({
                        "Area": area, "Possibilidade": pos, "Imp_Atual": imp_at,
                        "Imp_Geral": imp_ge, "Acao": act, "Satisfacao": sat, "Preocupacao": pre
                    })

                salvar_etapa_1 = st.form_submit_button("💾 Salvar Etapa 1 e Ir para a Etapa 2 ➡️")
                
                if salvar_etapa_1:
                    data_hoje = datetime.now().strftime("%d-%m-%Y %H:%M")
                    
                    novos_registros = []
                    for item in respostas_areas:
                        item.update({
                            "Data": data_hoje,
                            "Paciente_ID": paciente_id,
                            "Top_1": "", "Top_2": "", "Top_3": "", "Top_4": "",
                            "Status": "Etapa 1 Concluida",
                            "Valores_Muito_Importantes": "",
                            "Valores_Importantes": ""
                        })
                        novos_registros.append(item)
                    
                    df_novos = pd.DataFrame(novos_registros)
                    df_limpo = df_dados[df_dados["Paciente_ID"].astype(str).str.lower() != paciente_id]
                    df_atualizado = pd.concat([df_limpo, df_novos], ignore_index=True)
                    
                    conn.update(data=df_atualizado)
                    st.success("🎉 **Etapa 1 concluída!** Avançando para a Etapa 2...")
                    st.rerun()

        # --- ETAPA 2 DE 3: CLASSIFICAÇÃO DOS VALORES ---
        elif status_atual == "Etapa 1 Concluida":
            st.header("📌 Etapa 2 de 3: Classificação Inicial dos Valores")
            st.markdown("""
            **O que são Valores?**
            Valores são como **bússolas internas**. Eles representam aquilo que é mais importante para você como ser humano.
            
            Leia a lista de valores abaixo e classifique cada um como **Muito Importante**, **Importante** ou **Não Importante** para você neste momento da sua vida:
            """)

            with st.form("form_etapa_2"):
                classificacao_valores = {}
                cols = st.columns(2)
                for i, val in enumerate(LISTA_VALORES):
                    col = cols[i % 2]
                    classificacao_valores[val] = col.radio(
                        f"**{val}**",
                        ["Sem Resposta", "Não Importante", "Importante", "Muito Importante"],
                        index=0,
                        key=f"val_{val}",
                        horizontal=True
                    )

                salvar_etapa_2 = st.form_submit_button("💾 Salvar Etapa 2 e Ir para a Etapa 3 ➡️")

                if salvar_etapa_2:
                    muito_imp = [val for val, cat in classificacao_valores.items() if cat == "Muito Importante"]
                    imp = [val for val, cat in classificacao_valores.items() if cat == "Importante"]
                    
                    str_muito_imp = " | ".join(muito_imp)
                    str_imp = " | ".join(imp)

                    # Atualiza os registros existentes do paciente
                    indices = registros_paciente.index
                    for idx in indices:
                        df_dados.at[idx, "Valores_Muito_Importantes"] = str_muito_imp
                        df_dados.at[idx, "Valores_Importantes"] = str_imp
                        df_dados.at[idx, "Status"] = "Etapa 2 Concluida"

                    conn.update(data=df_dados)
                    st.success("🎉 **Etapa 2 concluída!** Avançando para a Etapa 3...")
                    st.rerun()

        # --- ETAPA 3 DE 3: DEFINIÇÃO DAS BÚSSOLAS PRINCIPAIS ---
        elif status_atual == "Etapa 2 Concluida":
            st.header("🎯 Etapa 3 de 3: Definição dos Seus Principais Valores")
            st.markdown("Com base na sua classificação da etapa anterior, escolha agora os seus **3 Valores Principais** e **1 Valor Secundário** (opcional).")

            str_muito = registros_paciente["Valores_Muito_Importantes"].iloc[0] if "Valores_Muito_Importantes" in registros_paciente.columns else ""
            str_imp = registros_paciente["Valores_Importantes"].iloc[0] if "Valores_Importantes" in registros_paciente.columns else ""

            muito_importantes = str(str_muito).split(" | ") if pd.notna(str_muito) and str_muito != "" else []
            importantes_extras = str(str_imp).split(" | ") if pd.notna(str_imp) and str_imp != "" else []

            if len(muito_importantes) < 4:
                opcoes_finais = muito_importantes + importantes_extras
                st.caption("ℹ️ *Como você marcou menos de 4 valores como 'Muito Importante', incluímos também os marcados como 'Importante' para sua seleção.*")
            else:
                opcoes_finais = muito_importantes

            if not opcoes_finais or opcoes_finais == ['']:
                opcoes_finais = LISTA_VALORES

            with st.form("form_etapa_3"):
                top_1 = st.selectbox("1º Valor Principal (Mais Importante):", ["Selecione..."] + opcoes_finais)
                top_2 = st.selectbox("2º Valor Principal:", ["Selecione..."] + opcoes_finais)
                top_3 = st.selectbox("3º Valor Principal:", ["Selecione..."] + opcoes_finais)
                top_4 = st.selectbox("4º Valor (Secundário):", ["Selecione..."] + opcoes_finais)

                finalizar = st.form_submit_button("Concluir e Enviar Exercício ✅")

                if finalizar:
                    if top_1 == "Selecione..." or top_2 == "Selecione..." or top_3 == "Selecione...":
                        st.error("Por favor, selecione pelo menos os 3 Valores Principais antes de finalizar.")
                    else:
                        indices = registros_paciente.index
                        for idx in indices:
                            df_dados.at[idx, "Top_1"] = top_1
                            df_dados.at[idx, "Top_2"] = top_2
                            df_dados.at[idx, "Top_3"] = top_3
                            df_dados.at[idx, "Top_4"] = top_4
                            df_dados.at[idx, "Status"] = "Concluido"
                        
                        conn.update(data=df_dados)
                        st.balloons()
                        st.success("✅ **Exercício finalizado com sucesso!** Suas respostas foram salvas.")
                        st.rerun()

# -------------------------------------------------------------------
# MODO TERAPEUTA
# -------------------------------------------------------------------
elif modo == "Painel do Psicólogo":
    st.title("🔒 Painel de Análise Clínica")
    senha = st.sidebar.text_input("Senha de Acesso:", type="password")

    if senha == SENHA_TERAPEUTA:
        aba1, aba2 = st.tabs(["👤 Gestão e Cadastro de Pacientes", "📊 Análise Clínica"])

        # --- ABA 1: CADASTRAR PACIENTES ---
        with aba1:
            st.subheader("➕ Cadastrar Novo Paciente")
            st.write("Cadastre o código do paciente para pré-autorizar o acesso dele ao sistema.")

            with st.form("form_novo_paciente"):
                novo_nome = st.text_input("Código do Paciente:").strip().lower()
                cadastrar = st.form_submit_button("Autorizar Acesso do Paciente")

                if cadastrar:
                    if not novo_nome:
                        st.warning("Digite o código do paciente.")
                    else:
                        ja_existe = False
                        if not df_dados.empty and "Paciente_ID" in df_dados.columns:
                            ja_existe = not df_dados[df_dados["Paciente_ID"].astype(str).str.lower() == novo_nome].empty

                        if ja_existe:
                            st.error("Este paciente já está cadastrado no sistema!")
                        else:
                            data_cadastro = datetime.now().strftime("%d-%m-%Y %H:%M")
                            novo_df = pd.DataFrame([{
                                "Paciente_ID": novo_nome,
                                "Data": data_cadastro,
                                "Status": "Pendente Etapa 1",
                                "Area": "", "Possibilidade": "", "Imp_Atual": "", "Imp_Geral": "",
                                "Acao": "", "Satisfacao": "", "Preocupacao": "",
                                "Top_1": "", "Top_2": "", "Top_3": "", "Top_4": "",
                                "Valores_Muito_Importantes": "", "Valores_Importantes": ""
                            }])
                            df_atualizado = pd.concat([df_dados, novo_df], ignore_index=True) if not df_dados.empty else novo_df
                            conn.update(data=df_atualizado)
                            st.success(f"✅ Paciente **'{novo_nome}'** cadastrado com sucesso!")
                            st.rerun()

            st.divider()
            st.subheader("📋 Lista de Pacientes Cadastrados e Status")
            if not df_dados.empty and "Paciente_ID" in df_dados.columns:
                resumo = df_dados.groupby("Paciente_ID").agg({
                    "Data": "first",
                    "Status": "first"
                }).reset_index()
                st.dataframe(resumo, use_container_width=True)
            else:
                st.info("Nenhum paciente cadastrado até o momento.")

        # --- ABA 2: ANÁLISE CLÍNICA ---
        with aba2:
            if df_dados.empty or "Paciente_ID" not in df_dados.columns:
                st.warning("Nenhum registro encontrado na planilha até o momento.")
            else:
                pacientes_com_dados = df_dados[df_dados["Status"].isin(["Etapa 1 Concluida", "Etapa 2 Concluida", "Concluido"])]["Paciente_ID"].unique().tolist()

                if not pacientes_com_dados:
                    st.info("Nenhum paciente concluiu etapas do exercício ainda.")
                else:
                    paciente_sel = st.selectbox("Selecione o Paciente para Análise:", pacientes_com_dados)

                    if paciente_sel:
                        d_pac = df_dados[df_dados["Paciente_ID"] == paciente_sel]
                        
                        st.header(f"📊 Análise Clínica: {paciente_sel.capitalize()}")
                        st.caption(f"Status do Exercício: **{d_pac['Status'].iloc[0]}**")
                        
                        st.subheader("1. Mapeamento Multidimensional das Áreas da Vida")
                        metricas_selecionadas = st.multiselect(
                            "Selecione as métricas para sobrepor no gráfico:",
                            ["Imp_Geral", "Imp_Atual", "Acao", "Satisfacao", "Preocupacao", "Possibilidade"],
                            default=["Imp_Geral", "Acao", "Preocupacao"]
                        )

                        fig = go.Figure()
                        for metrica in metricas_selecionadas:
                            fig.add_trace(go.Scatterpolar(
                                r=d_pac[metrica],
                                theta=d_pac["Area"],
                                fill='toself',
                                name=metrica
                            ))

                        fig.update_layout(
                            polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
                            showlegend=True,
                            height=650
                        )
                        st.plotly_chart(fig, use_container_width=True)

                        st.divider()
                        st.subheader("2. Principais Valores do Paciente")
                        
                        if d_pac["Status"].iloc[0] == "Concluido":
                            top1 = d_pac["Top_1"].iloc[0]
                            top2 = d_pac["Top_2"].iloc[0]
                            top3 = d_pac["Top_3"].iloc[0]
                            top4 = d_pac["Top_4"].iloc[0]

                            c1, c2, c3, c4 = st.columns(4)
                            c1.metric("1º Valor", top1)
                            c2.metric("2º Valor", top2)
                            c3.metric("3º Valor", top3)
                            c4.metric("4º Valor (secundário)", top4)
                        else:
                            st.warning("⚠️ O paciente ainda não concluiu a Etapa 3 (Seleção dos Principais Valores).")

                        st.markdown("### Outros Valores Destacados como 'Muito Importante':")
                        muito_imp_list = d_pac["Valores_Muito_Importantes"].iloc[0] if "Valores_Muito_Importantes" in d_pac.columns else ""
                        if pd.notna(muito_imp_list) and muito_imp_list:
                            valores_tags = [f"`{v.strip()}`" for v in str(muito_imp_list).split("|")]
                            st.write(" ".join(valores_tags))
                        else:
                            st.write("Nenhum valor classificado ou etapa ainda não realizada.")

                        st.divider()
                        if st.button("🗑️ Excluir/Resetar Paciente"):
                            df_dados = df_dados[df_dados["Paciente_ID"] != paciente_sel]
                            conn.update(data=df_dados)
                            st.success("Paciente removido com sucesso!")
                            st.rerun()
    else:
        if senha != "":
            st.error("Senha incorreta.")

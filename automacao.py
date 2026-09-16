from playwright.sync_api import sync_playwright
import datetime
import time
import gspread

# --- CONFIGURAÇÕES ---
NOME_PLANILHA_GOOGLE = "EAD 2026 - MOODLE - Controle Geral / CheckList" 

def executar_automacao_em_massa(data_filtro):
    print("1. Conectando ao Google Sheets (Autenticação Definitiva)...")
    
    # --- A MUDANÇA PRINCIPAL ESTÁ AQUI ---
    # Autenticação via Conta de Serviço (Lê o JSON e NUNCA expira o token)
    cliente = gspread.service_account(filename='credenciais.json')
    
    planilha = cliente.open(NOME_PLANILHA_GOOGLE)
    planilha_geral = planilha.worksheet("GERAL")
    
    print("Baixando dados da planilha...")
    # Pega todos os dados da aba de uma vez (muito mais rápido na nuvem)
    dados_planilha = planilha_geral.get_all_values()
    
    cursos_para_processar = []
    data_filtro_limpa = str(data_filtro).strip()
    
    # Processa os dados baixados (enumerate começa em 1 para alinhar com as linhas da planilha)
    for num_linha, linha in enumerate(dados_planilha, start=1):
        if num_linha == 1:
            continue # Pula a primeira linha (cabeçalhos)
            
        # O gspread retorna os dados em uma lista. Listas começam no índice 0.
        # Portanto: Coluna 1 = linha[0] | Coluna 4 = linha[3] | Coluna 7 = linha[6]
        
        if len(linha) < 7: # Se a linha for mais curta que a coluna 7, ignora
            continue
            
        nome_curso = linha[0]
        data_inicio = linha[3]
        link = linha[6]
        
        if not data_inicio or not link or "TurmaId=" not in link:
            continue
            
        data_str = str(data_inicio).strip()
        
        # Filtro inteligente
        if data_filtro_limpa in data_str:
            turma_id = str(link).split("TurmaId=")[-1]
            
            cursos_para_processar.append({
                "linha": num_linha,
                "id": turma_id,
                "nome": nome_curso
            })

    print(f" -> Encontrados {len(cursos_para_processar)} cursos válidos para o filtro ({data_filtro}).\n")

    if len(cursos_para_processar) == 0:
        print(" -> ATENÇÃO: Nenhum curso encontrado com essa data.")
        return

    with sync_playwright() as p:
        # Tenta abrir o Google Chrome instalado na máquina; se não achar, usa o Chromium padrão
        try:
            navegador = p.chromium.launch(headless=False, channel="chrome")
        except:
            navegador = p.chromium.launch(headless=False)
            
        pagina = navegador.new_page()
        
        print("2. Acessando o sistema EGOV...")
        pagina.goto("https://sistemas.df.gov.br/egov/")
        print("Faça o login! O robô vai aguardar 30 segundos...")
        time.sleep(30) 
        
        # --- INÍCIO DO LOOP DOS CURSOS ---
        for curso in cursos_para_processar:
            print(f"--------------------------------------------------")
            print(f"Analisando: {curso['nome']}")
            
            url_direta = f"https://sistemas.df.gov.br/egov/ConfirmarInscricao.aspx?TurmasID={curso['id']}"
            pagina.goto(url_direta)
            
            # VALIDAÇÃO DE PÁGINA FANTASMA
            try:
                pagina.wait_for_selector(".Counter_label", timeout=3000)
            except:
                print(" -> Turma fantasma (sem inscritos ou não publicada no EGOV). Pulando...")
                continue 
            
            # 1. VERIFICA PENDÊNCIAS
            try:
                label_pre = pagina.locator(".Counter_label", has_text="Pré-inscritos").first
                id_num_pre = label_pre.get_attribute("id").replace("wtLabel", "wtNumber")
                pendentes_inscricoes = int(pagina.locator(f"#{id_num_pre}").inner_text(timeout=2000))
                
                label_ouv_pend = pagina.locator(".Counter_label", has_text="Solicita").first
                id_num_ouv_pend = label_ouv_pend.get_attribute("id").replace("wtLabel", "wtNumber")
                pendentes_ouvintes = int(pagina.locator(f"#{id_num_ouv_pend}").inner_text(timeout=2000))
            except:
                print(" -> Nenhuma pendência encontrada.")
                pendentes_inscricoes = 0
                pendentes_ouvintes = 0
            
            # 2. DECIDE SE PRECISA CLICAR
            if pendentes_inscricoes > 0 or pendentes_ouvintes > 0:
                print(f" -> Encontrados: {pendentes_inscricoes} pré-inscritos e {pendentes_ouvintes} ouvintes.")
                print(" -> Confirmando novas inscrições...")
                try:
                    pagina.click('input[value="Confirmar todas as inscrições"]', timeout=3000)
                    print(" -> Processando no servidor (Aguardando 7 segundos)...")
                    time.sleep(7) 
                except:
                    print(" -> Botão não estava disponível.")
            else:
                print(" -> Zero pendências novas. Sincronizando apenas os números confirmados...")
            
            # 3. LEITURA DIRETA DOS NÚMEROS (Versão 100% blindada)
            qtd_inscricoes = 0
            qtd_ouvintes = 0
            
            # --- BUSCA DE INSCRIÇÕES ---
            try:
                label_insc = pagina.locator("text=/Inscrições.*Confirmadas/i").first
                id_label = label_insc.get_attribute("id", timeout=3000)
                
                if id_label and "wtLabel" in id_label:
                    id_num = id_label.replace("wtLabel", "wtNumber")
                    texto_insc = pagina.locator(f"#{id_num}").inner_text(timeout=2000).strip()
                else:
                    try:
                        texto_insc = label_insc.locator("xpath=preceding-sibling::div[contains(@class, 'Counter_number')]").inner_text(timeout=2000).strip()
                    except:
                        texto_insc = label_insc.locator("xpath=following-sibling::div[contains(@class, 'Counter_number')]").inner_text(timeout=2000).strip()

                if texto_insc.isdigit():
                    qtd_inscricoes = int(texto_insc)
            except Exception as e:
                pass

            # --- BUSCA DE OUVINTES ---
            try:
                label_ouv = pagina.locator("text=/Ouvintes.*Confirmados/i").first
                id_label_ouv = label_ouv.get_attribute("id", timeout=3000)
                
                if id_label_ouv and "wtLabel" in id_label_ouv:
                    id_num_ouv = id_label_ouv.replace("wtLabel", "wtNumber")
                    texto_ouv = pagina.locator(f"#{id_num_ouv}").inner_text(timeout=2000).strip()
                else:
                    try:
                        texto_ouv = label_ouv.locator("xpath=preceding-sibling::div[contains(@class, 'Counter_number')]").inner_text(timeout=2000).strip()
                    except:
                        texto_ouv = label_ouv.locator("xpath=following-sibling::div[contains(@class, 'Counter_number')]").inner_text(timeout=2000).strip()

                if texto_ouv.isdigit():
                    qtd_ouvintes = int(texto_ouv)
            except Exception as e:
                pass
            
            total_planilha = qtd_inscricoes + qtd_ouvintes
            
            # ATUALIZAÇÃO AO VIVO NO GOOGLE SHEETS
            planilha_geral.update_cell(curso["linha"], 8, total_planilha)
            planilha_geral.update_cell(curso["linha"], 19, qtd_ouvintes)
            
            print(f" -> [SUCESSO] Linha {curso['linha']} atualizada na nuvem: Total={total_planilha} | Ouvintes={qtd_ouvintes}")
        # --- FIM DO LOOP ---
        navegador.close()
        
        print(f"--------------------------------------------------")
        print("\n3. Processo finalizado com sucesso! Pode conferir o Google Sheets.")
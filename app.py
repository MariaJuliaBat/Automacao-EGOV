import customtkinter as ctk
import threading
from datetime import datetime
from tkinter import messagebox
from automacao import executar_automacao_em_massa

# Forçando o modo claro para o visual clean
ctk.set_appearance_mode("light")

class AppEGOV(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Automação EGOV - Confirmador de Inscrições")
        self.geometry("500x460")
        self.resizable(False, False)

        # Cor de fundo da metade inferior da tela (Off-White)
        self.configure(fg_color="#F2EEE7")

        # Faixa superior azul preenchendo exatamente a metade da tela
        self.faixa_topo = ctk.CTkFrame(self, fg_color="#435892", height=230, corner_radius=0)
        self.faixa_topo.place(x=0, y=0, relwidth=1.0)

        # Cartão central flutuante
        self.card = ctk.CTkFrame(
            self, 
            fg_color="#FFFFFF", 
            corner_radius=12, 
            width=380, 
            height=340, 
            border_width=1, 
            border_color="#E0E0E0"
        )
        self.card.place(relx=0.5, rely=0.5, anchor="center")
        
        self.card.grid_propagate(False) 
        self.card.pack_propagate(False)

        # Título
        self.label_titulo = ctk.CTkLabel(
            self.card, 
            text="Confirmador de Inscrições", 
            font=("Century Gothic", 20, "bold"), 
            text_color="#393F50" 
        )
        self.label_titulo.pack(pady=(30, 5))

        self.label_sub = ctk.CTkLabel(
            self.card, 
            text="Selecione a data de início do curso", 
            font=("Century Gothic", 13), 
            text_color="#7A7A7A"
        )
        self.label_sub.pack(pady=(0, 20))

        # --- SELETOR DE DATA MODERNO (3 Dropdowns: Dia, Mês, Ano) ---
        self.frame_data = ctk.CTkFrame(self.card, fg_color="transparent")
        self.frame_data.pack(pady=10)

        dias = [str(i).zfill(2) for i in range(1, 32)]
        meses = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
        
        ano_atual = datetime.now().year
        anos = [str(a) for a in range(ano_atual, ano_atual + 3)]

        # Dropdown de Dias
        self.combo_dia = ctk.CTkComboBox(
            self.frame_data, values=dias, width=75, height=35,
            font=("Century Gothic", 12), fg_color="#F2EEE7", text_color="#393F50",
            button_color="#435892", button_hover_color="#393F50", dropdown_fg_color="#FFFFFF"
        )
        self.combo_dia.grid(row=0, column=0, padx=5)
        self.combo_dia.set(datetime.now().strftime("%d"))

        # Dropdown de Meses
        self.combo_mes = ctk.CTkComboBox(
            self.frame_data, values=meses, width=75, height=35,
            font=("Century Gothic", 12), fg_color="#F2EEE7", text_color="#393F50",
            button_color="#435892", button_hover_color="#393F50", dropdown_fg_color="#FFFFFF"
        )
        self.combo_mes.grid(row=0, column=1, padx=5)
        self.combo_mes.set(datetime.now().strftime("%m"))

        # Dropdown de Anos
        self.combo_ano = ctk.CTkComboBox(
            self.frame_data, values=anos, width=95, height=35,
            font=("Century Gothic", 12), fg_color="#F2EEE7", text_color="#393F50",
            button_color="#435892", button_hover_color="#393F50", dropdown_fg_color="#FFFFFF"
        )
        self.combo_ano.grid(row=0, column=2, padx=5)
        self.combo_ano.set(str(ano_atual))

        # Botão principal
        self.botao_iniciar = ctk.CTkButton(
            self.card, 
            text="INICIAR SINCRONIZAÇÃO", 
            command=self.clicou_no_botao,
            font=("Century Gothic", 13, "bold"),
            fg_color="#435892",       
            hover_color="#393F50",    
            text_color="white",
            corner_radius=6,
            height=40,
            width=260
        )
        self.botao_iniciar.pack(pady=(25, 10))
        
        # Status
        self.label_status = ctk.CTkLabel(
            self.card, 
            text="", 
            font=("Century Gothic", 12), 
            text_color="#BCAA8A"      
        )
        self.label_status.pack(pady=10)

    def clicou_no_botao(self):
        dia = self.combo_dia.get()
        mes = self.combo_mes.get()
        ano = self.combo_ano.get()
        
        data_digitada = f"{dia}/{mes}/{ano}"
            
        self.label_status.configure(text=f"Processando cursos do dia {data_digitada}...", text_color="#393F50")
        self.botao_iniciar.configure(state="disabled") 
        
        thread_robo = threading.Thread(target=self.rodar_automacao_em_segundo_plano, args=(data_digitada,))
        thread_robo.start()

    def rodar_automacao_em_segundo_plano(self, data_alvo):
        try:
            executar_automacao_em_massa(data_alvo)
            
            self.label_status.configure(text="Concluído com sucesso!", text_color="#435892") 
            self.botao_iniciar.configure(state="normal")
            
            # --- POP-UP DE SUCESSO ---
            messagebox.showinfo("Sucesso", "A automação foi finalizada e a planilha foi atualizada na nuvem com sucesso!")
            
        except Exception as e:
            self.label_status.configure(text="Ocorreu um erro. Veja o terminal.", text_color="red")
            self.botao_iniciar.configure(state="normal")
            
            # --- POP-UP DE ERRO ---
            messagebox.showerror("Erro", f"Ocorreu um erro durante a execução:\n{e}")
            print(f"Erro na execução: {e}")

if __name__ == "__main__":
    app = AppEGOV()
    app.mainloop()
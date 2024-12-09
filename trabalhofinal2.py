import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Título da campanha
st.title('Campanha de Doação de Sangue')

# Adicionando uma imagem
st.image("Campanha.png")

# Descrição da campanha
st.markdown("""
## Junte-se a nós para salvar vidas!

A doação de sangue é um ato de solidariedade que pode salvar até três vidas. 
Participe da nossa campanha e ajude a promover a doação de sangue na sua comunidade.

### Por que doar sangue?
- **Salvar Vidas**: Cada doação pode ajudar até três pessoas.
- **Doações Necessárias**: Os hospitais sempre precisam de sangue.
- **Solidariedade**: Ajudar quem precisa é um ato nobre.

### Como funciona a doação?
1. **Registro**: Preencha o formulário abaixo.
2. **Coleta**: Dirija-se ao local de coleta mais próximo.
3. **Doação**: O processo de doação é rápido e seguro.

### Perguntas Frequentes
- **Quem pode doar sangue?**: Adultos saudáveis entre 18 e 69 anos.
- **Quanto tempo leva?**: O processo leva cerca de 30 minutos.
- **Com que frequência posso doar?**: Homens podem doar a cada 3 meses e mulheres a cada 4 meses.
""")

# Formulário de doação
st.subheader('Formulário de Doação')

with st.form('Formulário de Doador', clear_on_submit=True):
    col1, col2 = st.columns(2)

    nome = col1.text_input('Nome:')
    sobrenome = col2.text_input('Sobrenome:')
    email = col1.text_input('E-mail:')
    telefone = col2.text_input('Telefone:')
    
    idade = col1.number_input('Idade:', min_value=18, max_value=69)
    tipo_sanguineo = col2.selectbox('Tipo Sanguíneo:', ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'])
    
    submitted = st.form_submit_button("Enviar")

# Função para verificar elegibilidade
def pode_doar(doenças):
    doenças_restritivas = ['Hipertensão', 'Doenças cardíacas', 'Doenças sanguíneas', 'Gripe ou tosse recente']
    
    # Se a lista de doenças estiver vazia ou contiver apenas "Nenhuma doença acima"
    if 'Nenhuma doença acima' in doenças:
        return "Você pode doar sangue!"
    
    # Verifica se alguma doença restritiva está presente
    if any(d in doenças for d in doenças_restritivas):
        return "Você não pode doar sangue."
    
    return "Você pode doar sangue!"

# Sidebar para entrada de dados
st.sidebar.title("Verificação de Elegibilidade para Doação de Sangue")
doenças = st.sidebar.multiselect("Selecione suas doenças:", 
                                  ['Nenhuma doença acima', 'Hipertensão', 'Doenças cardíacas', 
                                   'Doenças sanguíneas', 'Gripe ou tosse recente', 
                                   'Outra doença'])

# Botão para verificar elegibilidade
if st.sidebar.button("Verificar"):
    resultado = pode_doar(doenças)
    st.sidebar.write(resultado)

col3, col4 = st.columns(2)
dm = col3.date_input('Data de inscrição:', format="DD/MM/YYYY")
obs = col4.text_area('Observações (medicamentos usados e doenças não citadas):')

# Botão de envio
enviar = st.button("enviar")
if enviar:
    if nome and sobrenome and email:
        # Verifica se a pessoa pode doar
        if not doenças:
            st.success('Obrigado por se registrar como doador! Você pode doar!')
        
        # Criação do DataFrame com os dados do formulário
        dados = {
            "Nome": [nome],
            "Sobrenome": [sobrenome],
            "Email": [email],
            "Telefone": [telefone],
            "Idade": [idade],
            "Tipo Sanguíneo": [tipo_sanguineo],
            "Observações": [obs],
            "Data de Inscrição": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
        }
        df = pd.DataFrame(dados)

   # Definindo o caminho do arquivo
        pasta = "dados_doadores"
        if not os.path.exists(pasta):  # Se a pasta não existir, cria a pasta
            os.makedirs(pasta)
        
        # Criando o nome do arquivo com data e hora para garantir que seja único
        arquivo_csv = os.path.join(pasta, f'doador_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv')

        # Salvando o DataFrame em um arquivo CSV dentro da pasta 'dados_doadores'
        df.to_csv(arquivo_csv, sep=';', index=False)

        # Mensagem de sucesso
        st.write(f'Dados salvos em: {arquivo_csv}')

# Título para a seção de feedback
st.subheader("Deixe seu Feedback sobre a Doação de Sangue")

# Formulário para o feedback
with st.form('feedback_form', clear_on_submit=True):
    feedback = st.text_area('Como foi sua experiência ao doar sangue? (Compartilhe seus pensamentos e sugestões)')
    enviar_feedback = st.form_submit_button('Enviar Feedback')

    if enviar_feedback:
        if feedback:
            # Criação do DataFrame para salvar o feedback
            feedbacks_pasta = "feedbacks"
            if not os.path.exists(feedbacks_pasta):
                os.makedirs(feedbacks_pasta)
            arquivo_feedback = os.path.join(feedbacks_pasta, f'feedback_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv')

            # Criação do DataFrame com os dados do feedback
            feedback_dados = {
                "Feedback": [feedback],
                "Data de Envio": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
            }
            df_feedback = pd.DataFrame(feedback_dados)

            # Salvando o feedback no arquivo CSV
            df_feedback.to_csv(arquivo_feedback, sep=';', index=False)

            st.success('Obrigado por compartilhar seu feedback!')

# Exibindo feedbacks anteriores (opcional)
st.subheader("Feedbacks Anteriores")
feedbacks_anteriores = []

# Verifica se há feedbacks salvos
feedbacks_pasta = "feedbacks"
if os.path.exists(feedbacks_pasta):
    feedback_files = [f for f in os.listdir(feedbacks_pasta) if f.endswith('.csv')]
    
    for feedback_file in feedback_files:
        df_feedbacks = pd.read_csv(os.path.join(feedbacks_pasta, feedback_file), sep=';')
        feedbacks_anteriores.append(df_feedbacks)

# Exibindo todos os feedbacks na tela
if feedbacks_anteriores:
    for df in feedbacks_anteriores:
        for index, row in df.iterrows():
            st.write(f"**Feedback:** {row['Feedback']}")
            st.write(f"**Data:** {row['Data de Envio']}")
            st.markdown("---")
else:
    st.write("Ainda não há feedbacks disponíveis.")

# Sidebar para agendar doação
st.sidebar.header('Agende sua doação')
col5, col6 = st.sidebar.columns(2)

data_agendamento = col5.date_input('Data de agendamento:', format="DD/MM/YYYY")
horario_agendamento = col6.selectbox('Horário:', ['7:30', '8:00', '8:30', '9:00', '9:30', '10:00', '10:30', '11:00', '11:30'])

# Seção de contato
st.markdown('---')
st.subheader('Entre em contato conosco')

st.write('Se você tiver alguma dúvida ou quiser mais informações, entre em contato:')
st.write('📧 Email: contato.sjr.captacao@hemominas.mg.gov.br')
st.write('📞 Telefone: (32) 3322-2900')
st.write('[🌐 Facebook](https://m.facebook.com/hemominas/photos/)')
st.write('[🐦 Twitter](https://twitter.com/hemominas)')
st.write('[📸 Instagram](https://www.instagram.com/hemominas/)')


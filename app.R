#
# This is a Shiny web application. You can run the application by clicking
# the 'Run App' button above.
#
# Find out more about building applications with Shiny here:
#
#    http://shiny.rstudio.com/
#

# Pacotes

library(shiny)
library(reticulate)
library(shinythemes)

source_python("utils/Pagamentos.py")

################################################################################

# Interface do usuario

ui <- shinyUI(fluidPage(theme = shinytheme("flatly"),

    titlePanel("Transformador de relatórios", windowTitle = "Transformador de relatórios"),

    fluidRow(

        column(4,
            fileInput("balancete", h4("Arquivo balancete")),
            dataTableOutput("verb1"),
            selectInput("select", h4("Selecione aqui o grupo:"), 
                        choices = list("Selecione" = 1,
                                       "Coopideal" = 2, 
                                       "Rede Local" = 3,
                                       "Outros" = 4), selected = 1)
        ),

        column(4,
            fileInput("relatorio", h4("Arquivo relatório")),
            textOutput("verb2"),
            textInput("duplicatas", h3("Conta Duplicatas"))
        ),
        
        column(3,
               helpText(h3("PROCESSAMENTO\n"), hr(), h4("\nAguardando início do processamento..."))), 

    ),
    
    fixedRow(
        column(1,offset=4,
               actionButton("pro", "Processar")
        ),
        column(1,
               actionButton("clean","Limpar dados"))
    ),
    

    fluidRow(br(),
            hr(),h2("Ajuda", align='center'),
            h3("ATENÇÃO! INSTRUÇÕES DE USO:", align="Center"),
            h4(helpText("Se for do grupo coopideal/rede local,",
                     strong("especificar com _coop ou _rede no fim do nome do arquivo de balancete"), 
                     br(), 
                     "O Balancete deve ser somente com os fornecedores;",
                     br(),
                     "Todos os arquivos devem estar no formato .csv;",
                     br(),
                     br(),
                     "As colunas principais que o programa utiliza devem seguir esse padrão de nome:",
                     br(),
                     br(),
                     strong("Razão Social, Valor Líquido, Valor Acréscimo, Valor Abatimento;"),
                     br(),
                     strong("Data Pagamento, Observação, Nome Banco, Tipo Entrada;"),
                     br(),
                     br(),
                     div(strong("Qualquer problema não me procure."), style="color:red"), align='center'))
            )
        )
    )

################################################################################

# Servidor

server <- function(input, output){
    
}    

################################################################################

# Rodar aplicativo

shinyApp(ui=ui, server=server)
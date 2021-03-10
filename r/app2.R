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

ui <- shinyUI(fluidPage(
  
  sidebarLayout(
    
    sidebarPanel(
      
      titlePanel("Transformador de relatórios", windowTitle = "Transformador de relatórios"),
      
      tabsetPanel(id = "Panel",
                  tabPanel("Preencha aqui!",
                  fileInput("balancete", h4("Arquivo balancete"), accept= ".csv"),
                  fileInput("relatorio", h4("Arquivo relatório"), accept= ".csv"),
                  selectInput("select", h4("Selecione aqui o grupo:"), 
                              choices = list("Selecione" = 1,
                                             "Coopideal" = 2, 
                                             "Rede Local" = 3,
                                             "Outros" = 4), selected = 1),
                  textInput("duplicatas", h3("Conta Duplicatas")),
                  actionButton("pro", "Processar"),
                  actionButton("clean","Limpar dados")
            )
        )
    ),
    
    mainPanel(helpText(h3("PROCESSAMENTO\n")),textOutput("plot"))
    ),
  
    fluidRow(hr(),h2("Ajuda", align='center'),
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

server <- function(input, output, session){
    
    v <- reactiveValues(init = "\nAguardando iniciar processamento...", 
                        proc = "\nProcessando...")

    
    processa <- eventReactive({
      
      if(is.null(input$duplicatas)) 
        return(v$init)
      else 
        pagamentos(input$balancete, input$relatorio, input$duplicatas)
        return(v$proc)
      
      })
    
    output$plot <- renderPrint({processa()})
}

################################################################################

# Rodar aplicativo

shinyApp(ui=ui, server=server)

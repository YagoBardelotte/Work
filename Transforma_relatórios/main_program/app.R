# Pacotes

library(shiny)
library(reticulate)

source_python("utils/Pagamentos.py")

################################################################################

# Interface do usuario

ui <- shinyUI(fluidPage(

    titlePanel("Transformador de relatórios"),

    fluidRow(

        column(4,
            fileInput("balancete", h4("Arquivo balancete")),
            dataTableOutput("verb1")
        ),

        column(4,
            fileInput("relatorio", h4("Arquivo relatório")),
            textOutput("verb2")
        ),
        
        column(3,
               selectInput("select", h4("Selecione aqui o grupo:"), 
                           choices = list("Selecione" = 1,
                                          "Coopideal" = 2, 
                                          "Rede Local" = 3,
                                          "Outros" = 4), selected = 1),
               textInput("duplicatas", h3("Conta Duplicatas"))
        )
    ),
    
    fixedRow(
        column(1,offset=4,
               submitButton("Processar")
        ),
        column(1,
               submitButton("Limpar dados"))
    ),
    
    fluidRow(
        textOutput("balancete")
    ),

    fluidRow(br(),
            h2("Ajuda", align='center'),
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
    
    #if (is.null(input$balancete)) {
    
    #    output$verb1 <- renderPrint({"Aguardando arquivo"})
    #} 
    #else {
    #    output$verb1 <- renderPrint({input$balancete})
    #}
    
    output$verb2 <- renderDataTable({input$relatorio})
}

################################################################################

# Rodar aplicativo

shinyApp(ui=ui, server=server)